#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the register table in README.md from the public gate API.

No human input. No curation. The script fetches the register, formats every row it
receives, and replaces only the block between the REGISTER markers. If the API is
unreachable, the README is left exactly as it was: a stale table is honest, an
invented one is not.
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

REGISTER_URL = "https://gate.horizonshield.dev/register"
README = "README.md"
START = "<!-- REGISTER:START -->"
END = "<!-- REGISTER:END -->"


def fetch():
    req = urllib.request.Request(REGISTER_URL, headers={"user-agent": "mcp-conduct-register/1.0 (+https://github.com/)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def row_line(r):
    label = r.get("operator_label") or {}
    name = label.get("en") or label.get("ja") or r["endpoint"]
    ja = label.get("ja")
    if ja and label.get("en"):
        name = name + "<br><sub>" + ja + "</sub>"
    latest = r.get("latest") or {}
    verdict = latest.get("status") or "not measured yet"
    when = (latest.get("at") or "")[:10]
    n = r.get("measurements")
    n_txt = str(n) if isinstance(n, int) else "?"
    hist = r.get("history_url") or ""
    sha = (latest.get("record_sha256") or "")[:12]
    sha_txt = "`" + sha + "`" if sha else ""
    return "| {name} | `{ep}` | {verdict} | {when} | {n} | {sha} | [history]({hist}) |".format(
        name=name, ep=r["endpoint"], verdict=verdict, when=when, n=n_txt, sha=sha_txt, hist=hist
    )


def build(data):
    rows = data.get("rows") or []
    out = []
    out.append("Generated from <" + REGISTER_URL + "> at " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC") + ".")
    out.append("")
    out.append("**" + str(len(rows)) + " rows.** Nobody chose them. This table is written by a script, not a person.")
    out.append("")
    out.append("| Server | Endpoint | Latest verdict | Measured | Public measurements | record_sha256 | History |")
    out.append("|---|---|---|---|---|---|---|")
    for r in rows:
        out.append(row_line(r))
    out.append("")
    gc = data.get("gate_commit")
    if gc:
        out.append("Measured by gate commit `" + str(gc) + "`. The commit that produced each verdict is inside the hashed record.")
    note = data.get("note")
    if note:
        out.append("")
        out.append("> " + note)
    return "\n".join(out)


def main():
    try:
        data = fetch()
    except Exception as e:
        print("register unreachable: %s" % e, file=sys.stderr)
        print("README left unchanged. A stale table is honest, an invented one is not.", file=sys.stderr)
        return 0
    body = build(data)
    src = open(README, encoding="utf-8").read()
    if START not in src or END not in src:
        print("markers missing in README", file=sys.stderr)
        return 1
    new = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        START + "\n" + body + "\n" + END,
        src,
        flags=re.S,
    )
    if new == src:
        print("no change")
        return 0
    open(README, "w", encoding="utf-8").write(new)
    print("README updated with %d rows" % len(data.get("rows") or []))
    return 0


if __name__ == "__main__":
    sys.exit(main())
