#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# patch25: make the data itself citable. The JSON snapshot becomes schema.org
# Dataset shaped, so a crawler that finds only the JSON still learns what it is,
# who made it, how it was measured and what it does not claim. The same run
# writes an Atom feed, so a subscriber learns when a verdict changes without
# polling. Run this inside the mcp-conduct-register checkout.
# Default is dry-run. --apply writes. Anchors expect exactly 1 hit each.
import sys, os, subprocess, tempfile, json

APPLY = "--apply" in sys.argv
EDITS = [('scripts/build_register.py', 'REGISTER_URL = "https://gate.horizonshield.dev/register"\nREADME = "README.md"', 'REGISTER_URL = "https://gate.horizonshield.dev/register"\nREPO_URL = "https://github.com/ogasurfproject-jpg/mcp-conduct-register"\nRAW_BASE = "https://raw.githubusercontent.com/ogasurfproject-jpg/mcp-conduct-register/main"\nFEED = "feed.xml"\nREADME = "README.md"', 'url constants'), ('scripts/build_register.py', 'def build(data):', 'def xml_escape(s):\n    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")\n            .replace(\'"\', "&quot;").replace("\'", "&apos;"))\n\n\ndef write_feed(rows, stamp, gate_commit):\n    """An Atom feed of the current verdicts. A crawler that subscribes learns when a\n    verdict changes without polling the API, and each entry links to the full public\n    history for that endpoint rather than summarising it here."""\n    parts = []\n    parts.append(\'<?xml version="1.0" encoding="utf-8"?>\')\n    parts.append(\'<feed xmlns="http://www.w3.org/2005/Atom">\')\n    parts.append("<title>MCP Conduct Register</title>")\n    parts.append("<subtitle>Measured conduct of MCP servers. Not a curated list, not a ranking, not an endorsement.</subtitle>")\n    parts.append(\'<link href="%s" rel="alternate"/>\' % REPO_URL)\n    parts.append(\'<link href="%s/feed.xml" rel="self"/>\' % RAW_BASE)\n    parts.append("<id>%s</id>" % (REPO_URL + "#feed"))\n    parts.append("<updated>%s</updated>" % stamp)\n    parts.append("<author><name>The HORIZONs Co., Ltd.</name><uri>https://shield.the-horizons-innovation.com/</uri></author>")\n    if gate_commit:\n        parts.append("<generator>hs-verify-gate %s</generator>" % xml_escape(gate_commit))\n    for r in rows:\n        label = r.get("operator_label") or {}\n        name = label.get("en") or label.get("ja") or r.get("endpoint", "")\n        latest = r.get("latest") or {}\n        verdict = latest.get("status") or "not measured yet"\n        when = latest.get("at") or stamp\n        sha = latest.get("record_sha256") or ""\n        n = r.get("measurements")\n        summary = "Verdict: %s. Public measurements: %s." % (verdict, n if isinstance(n, int) else "unknown")\n        if sha:\n            summary += " record_sha256 %s, recomputable from the published bytes." % sha\n        summary += " Listing is not endorsement. A passing verdict means the measured conditions passed on that date, from the vantage that measured them."\n        parts.append("<entry>")\n        parts.append("<title>%s: %s</title>" % (xml_escape(name), xml_escape(verdict)))\n        parts.append(\'<link href="%s" rel="alternate"/>\' % xml_escape(r.get("history_url", REPO_URL)))\n        parts.append("<id>%s</id>" % xml_escape(r.get("endpoint", "")))\n        parts.append("<updated>%s</updated>" % xml_escape(when))\n        parts.append("<summary>%s</summary>" % xml_escape(summary))\n        parts.append("</entry>")\n    parts.append("</feed>")\n    open(FEED, "w", encoding="utf-8").write("\\n".join(parts) + "\\n")\n    print("feed.xml written with %d entries" % len(rows))\n\n\ndef build(data):', 'atom feed writer'), ('scripts/build_register.py', '    snapshot = {\n        "source": REGISTER_URL,\n        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),\n        "what_this_is": "A machine generated record of measured MCP server conduct. Not a curated list, not a ranking, not an endorsement.",\n        "rows_are_selected_by": "nobody, the script copies whatever the API returns",\n        "count": len(data.get("rows") or []),\n        "gate_commit": data.get("gate_commit"),\n        "note": data.get("note"),\n        "rows": data.get("rows") or [],\n    }\n    open("register.json", "w", encoding="utf-8").write(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\\n")\n    print("register.json written with %d rows" % snapshot["count"])', '    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")\n    rows = data.get("rows") or []\n    # The snapshot is itself schema.org Dataset shaped, so a crawler that finds the\n    # JSON without ever seeing the page still learns what it is, who made it, how it\n    # was measured, and what it does not claim.\n    snapshot = {\n        "@context": "https://schema.org",\n        "@type": "Dataset",\n        "@id": REPO_URL + "#dataset",\n        "name": "MCP Conduct Register: measured conduct of Model Context Protocol servers",\n        "description": (\n            "A machine generated record of how Model Context Protocol servers behaved when measured. "\n            "Not a curated list, not a ranking, not an endorsement. Rows are produced by a scheduled "\n            "measurement and copied here by a script with no editorial input. Every verdict carries a "\n            "SHA-256 recomputable from the published bytes, and records unflattering to the operator are "\n            "retained because the code contains no route for removing them."\n        ),\n        "url": REPO_URL,\n        "license": "https://opensource.org/licenses/MIT",\n        "isAccessibleForFree": True,\n        "creator": {\n            "@type": "Organization",\n            "name": "The HORIZONs Co., Ltd.",\n            "url": "https://shield.the-horizons-innovation.com/",\n            "founder": {\n                "@type": "Person",\n                "name": "Toshikatsu Oga",\n                "identifier": "https://orcid.org/0009-0000-9180-903X",\n            },\n        },\n        "measurementTechnique": (\n            "Scheduled HTTP measurement of the MCP initialize handshake, agent card retrieval, payer "\n            "disclosure and determinism. Every verdict discloses the route that measured it and the "\n            "commit that produced it."\n        ),\n        "variableMeasured": ["reachability", "agent card", "payer disclosure", "determinism", "record_sha256"],\n        "distribution": [\n            {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": REGISTER_URL},\n            {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": RAW_BASE + "/register.json"},\n            {"@type": "DataDownload", "encodingFormat": "text/markdown", "contentUrl": RAW_BASE + "/README.md"},\n        ],\n        "dateModified": stamp,\n        "source": REGISTER_URL,\n        "generated_at": stamp,\n        "what_this_is": "A machine generated record of measured MCP server conduct. Not a curated list, not a ranking, not an endorsement.",\n        "what_this_is_not": "It is not proof that a listed server returns correct numbers, that the business behind it is competent, or that it is safe to use.",\n        "rows_are_selected_by": "nobody, the script copies whatever the API returns",\n        "disputes": {\n            "how": "Measure any listed endpoint yourself and submit the observation to the public ledger under your own name and vantage.",\n            "intake": "https://ledger.horizonshield.dev/witness",\n            "operator_veto": "none, the code has no route to refuse a schema valid submission",\n        },\n        "count": len(rows),\n        "gate_commit": data.get("gate_commit"),\n        "note": data.get("note"),\n        "rows": rows,\n    }\n    open("register.json", "w", encoding="utf-8").write(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\\n")\n    print("register.json written with %d rows" % snapshot["count"])\n    write_feed(rows, stamp, data.get("gate_commit"))', 'schema.org shaped snapshot'), ('.github/workflows/build.yml', '          git add README.md register.json', '          git add README.md register.json feed.xml', 'workflow commits feed')]

def main():
    if not os.path.exists("scripts/build_register.py"):
        print("ABORT: run this inside the mcp-conduct-register checkout.")
        sys.exit(1)
    contents = {}
    ok = True
    for path, old, new, name in EDITS:
        if path not in contents:
            contents[path] = open(path, encoding="utf-8").read()
        n = contents[path].count(old)
        print("[anchor] %s: %d occurrence(s) (expect 1)" % (name, n))
        if n != 1: ok = False
    if not ok:
        print("ABORT: anchor mismatch. Nothing written.")
        sys.exit(1)
    for path, old, new, name in EDITS:
        contents[path] = contents[path].replace(old, new, 1)

    gn = contents["scripts/build_register.py"]
    wf = contents[".github/workflows/build.yml"]
    checks = [
        ('"@context": "https://schema.org"' in gn, "snapshot: schema.org context"),
        ('"@type": "Dataset"' in gn, "snapshot: declares itself a Dataset"),
        ("what_this_is_not" in gn, "snapshot: states what it does not claim"),
        ("orcid.org/0009-0000-9180-903X" in gn, "snapshot: author identified by ORCID"),
        ("def write_feed" in gn, "generator: feed writer present"),
        ("def xml_escape" in gn, "generator: xml escaping present"),
        ("feed.xml" in wf, "workflow: commits the feed"),
    ]
    tf = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8"); tf.write(gn); tf.close()
    r = subprocess.run([sys.executable, "-m", "py_compile", tf.name], capture_output=True, text=True)
    os.unlink(tf.name)
    checks.append((r.returncode == 0, "generator: python syntax ok" + ("" if r.returncode == 0 else " :: " + r.stderr.strip()[:200])))
    allok = True
    for good, label in checks:
        print(("[ok]  " if good else "[FAIL] ") + label)
        allok = allok and good
    if not allok:
        print("ABORT: invariant failed. Nothing written.")
        sys.exit(1)
    if not APPLY:
        print("DRY-RUN OK. Nothing written. Run with --apply to write.")
        return
    for path in contents:
        open(path, "w", encoding="utf-8").write(contents[path])
        print("[written] " + path)
    print("APPLY done. Commit, push, then run the workflow once to generate feed.xml.")

if __name__ == "__main__":
    main()
