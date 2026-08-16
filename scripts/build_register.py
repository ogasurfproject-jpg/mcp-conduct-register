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
REPO_URL = "https://github.com/ogasurfproject-jpg/mcp-conduct-register"
RAW_BASE = "https://raw.githubusercontent.com/ogasurfproject-jpg/mcp-conduct-register/main"
FEED = "feed.xml"
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


def xml_escape(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&apos;"))


def write_feed(rows, stamp, gate_commit):
    """An Atom feed of the current verdicts. A crawler that subscribes learns when a
    verdict changes without polling the API, and each entry links to the full public
    history for that endpoint rather than summarising it here."""
    parts = []
    parts.append('<?xml version="1.0" encoding="utf-8"?>')
    parts.append('<feed xmlns="http://www.w3.org/2005/Atom">')
    parts.append("<title>MCP Conduct Register</title>")
    parts.append("<subtitle>Measured conduct of MCP servers. Not a curated list, not a ranking, not an endorsement.</subtitle>")
    parts.append('<link href="%s" rel="alternate"/>' % REPO_URL)
    parts.append('<link href="%s/feed.xml" rel="self"/>' % RAW_BASE)
    parts.append("<id>%s</id>" % (REPO_URL + "#feed"))
    parts.append("<updated>%s</updated>" % stamp)
    parts.append("<author><name>The HORIZONs Co., Ltd.</name><uri>https://shield.the-horizons-innovation.com/</uri></author>")
    if gate_commit:
        parts.append("<generator>hs-verify-gate %s</generator>" % xml_escape(gate_commit))
    for r in rows:
        label = r.get("operator_label") or {}
        name = label.get("en") or label.get("ja") or r.get("endpoint", "")
        latest = r.get("latest") or {}
        verdict = latest.get("status") or "not measured yet"
        when = latest.get("at") or stamp
        sha = latest.get("record_sha256") or ""
        n = r.get("measurements")
        summary = "Verdict: %s. Public measurements: %s." % (verdict, n if isinstance(n, int) else "unknown")
        if sha:
            summary += " record_sha256 %s, recomputable from the published bytes." % sha
        summary += " Listing is not endorsement. A passing verdict means the measured conditions passed on that date, from the vantage that measured them."
        parts.append("<entry>")
        parts.append("<title>%s: %s</title>" % (xml_escape(name), xml_escape(verdict)))
        parts.append('<link href="%s" rel="alternate"/>' % xml_escape(r.get("history_url", REPO_URL)))
        parts.append("<id>%s</id>" % xml_escape(r.get("endpoint", "")))
        parts.append("<updated>%s</updated>" % xml_escape(when))
        parts.append("<summary>%s</summary>" % xml_escape(summary))
        parts.append("</entry>")
    parts.append("</feed>")
    open(FEED, "w", encoding="utf-8").write("\n".join(parts) + "\n")
    print("feed.xml written with %d entries" % len(rows))


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
    # Machine readable snapshot, so an agent can read the register without parsing Markdown.
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = data.get("rows") or []
    # The snapshot is itself schema.org Dataset shaped, so a crawler that finds the
    # JSON without ever seeing the page still learns what it is, who made it, how it
    # was measured, and what it does not claim.
    snapshot = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": REPO_URL + "#dataset",
        "name": "MCP Conduct Register: measured conduct of Model Context Protocol servers",
        "description": (
            "A machine generated record of how Model Context Protocol servers behaved when measured. "
            "Not a curated list, not a ranking, not an endorsement. Rows are produced by a scheduled "
            "measurement and copied here by a script with no editorial input. Every verdict carries a "
            "SHA-256 recomputable from the published bytes, and records unflattering to the operator are "
            "retained because the code contains no route for removing them."
        ),
        "url": REPO_URL,
        "license": "https://opensource.org/licenses/MIT",
        "isAccessibleForFree": True,
        "creator": {
            "@type": "Organization",
            "name": "The HORIZONs Co., Ltd.",
            "url": "https://shield.the-horizons-innovation.com/",
            "founder": {
                "@type": "Person",
                "name": "Toshikatsu Oga",
                "identifier": "https://orcid.org/0009-0000-9180-903X",
            },
        },
        "measurementTechnique": (
            "Scheduled HTTP measurement of the MCP initialize handshake, agent card retrieval, payer "
            "disclosure and determinism. Every verdict discloses the route that measured it and the "
            "commit that produced it."
        ),
        "variableMeasured": ["reachability", "agent card", "payer disclosure", "determinism", "record_sha256"],
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": REGISTER_URL},
            {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": RAW_BASE + "/register.json"},
            {"@type": "DataDownload", "encodingFormat": "text/markdown", "contentUrl": RAW_BASE + "/README.md"},
        ],
        "dateModified": stamp,
        "source": REGISTER_URL,
        "generated_at": stamp,
        "what_this_is": "A machine generated record of measured MCP server conduct. Not a curated list, not a ranking, not an endorsement.",
        "what_this_is_not": "It is not proof that a listed server returns correct numbers, that the business behind it is competent, or that it is safe to use.",
        "rows_are_selected_by": "nobody, the script copies whatever the API returns",
        "disputes": {
            "how": "Measure any listed endpoint yourself and submit the observation to the public ledger under your own name and vantage.",
            "intake": "https://ledger.horizonshield.dev/witness",
            "operator_veto": "none, the code has no route to refuse a schema valid submission",
        },
        "count": len(rows),
        "gate_commit": data.get("gate_commit"),
        "note": data.get("note"),
        "rows": rows,
    }
    open("register.json", "w", encoding="utf-8").write(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    print("register.json written with %d rows" % snapshot["count"])
    write_feed(rows, stamp, data.get("gate_commit"))
    if new == src:
        print("README unchanged")
        return 0
    open(README, "w", encoding="utf-8").write(new)
    print("README updated with %d rows" % len(data.get("rows") or []))
    return 0


if __name__ == "__main__":
    sys.exit(main())
