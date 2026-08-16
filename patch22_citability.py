#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# patch22: citation and machine readability. Adds CITATION.cff (so GitHub shows
# a Cite button and the register enters academic indexes), llms.txt (an explicit
# brief for language models), a register.json snapshot written by the generator,
# a one sentence definition at the top of the README, and a question and answer
# section. All of these make the register easier to quote correctly.
# Run this inside the mcp-conduct-register checkout.
# Default is dry-run. --apply writes. Anchors expect exactly 1 hit each.
import sys, os, subprocess, tempfile

APPLY = "--apply" in sys.argv
EDITS = [('README.md', '# MCP Conduct Register\n\n**This is not a curated list of good servers. It is a record of what was measured.**', '# MCP Conduct Register\n\n**MCP Conduct Register is a machine generated public record of how Model Context Protocol servers\nbehaved when they were measured.** It is not a curated list of good servers. Nobody selects the rows,\nplacement cannot be bought, and records that embarrass the operator are retained because the code\ncontains no route for removing them.\n\n**This is not a curated list of good servers. It is a record of what was measured.**', 'readme definition sentence'), ('README.md', '## License', '## Questions people actually ask\n\n**How is this different from an awesome list?**\nAn awesome list is a human recommending things. This is a script reporting measurements. No human\nchose any row here, and the generator is in this repository so you can check that claim.\n\n**Can I pay to be listed, or to be listed higher?**\nNo, and there is nothing to buy. The order of the table is the order the API returns. There is no\nranking and no score.\n\n**What does a green row prove?**\nThat the conditions which were measured passed on that date, from the vantage that measured them.\nIt does not prove the numbers a server returns are correct, or that the business behind it is\ncompetent, or that it is safe to use.\n\n**What if your own server fails?**\nIt has, and the record is still published. The gate measures its own endpoint under the same rules.\nThe founding record of the ledger behind this register is a disagreement between two witnesses about\nthe operator\'s own server, in which both witnesses turned out to be correct.\n\n**Can I dispute a verdict?**\nYes, and that is the point. Measure the endpoint yourself and submit your observation to the public\nledger under your own name and vantage. If your report conflicts with this register, the conflict\nbecomes a permanent citable record. The operator has no veto in code.\n\n**Who runs this?**\nToshikatsu Oga, The HORIZONs Co., Ltd., Hiratsuka, Japan. A carpenter of thirty years.\nORCID [0009-0000-9180-903X](https://orcid.org/0009-0000-9180-903X).\n\n**How do I cite this register?**\nSee CITATION.cff, or use the "Cite this repository" button on GitHub. A machine readable snapshot of\nthe current table is published as `register.json` in this repository.\n\n## License', 'readme faq section'), ('scripts/build_register.py', '    if new == src:\n        print("no change")\n        return 0\n    open(README, "w", encoding="utf-8").write(new)\n    print("README updated with %d rows" % len(data.get("rows") or []))\n    return 0', '    # Machine readable snapshot, so an agent can read the register without parsing Markdown.\n    snapshot = {\n        "source": REGISTER_URL,\n        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),\n        "what_this_is": "A machine generated record of measured MCP server conduct. Not a curated list, not a ranking, not an endorsement.",\n        "rows_are_selected_by": "nobody, the script copies whatever the API returns",\n        "count": len(data.get("rows") or []),\n        "gate_commit": data.get("gate_commit"),\n        "note": data.get("note"),\n        "rows": data.get("rows") or [],\n    }\n    open("register.json", "w", encoding="utf-8").write(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\\n")\n    print("register.json written with %d rows" % snapshot["count"])\n    if new == src:\n        print("README unchanged")\n        return 0\n    open(README, "w", encoding="utf-8").write(new)\n    print("README updated with %d rows" % len(data.get("rows") or []))\n    return 0', 'generator writes register.json'), ('.github/workflows/build.yml', '          git add README.md', '          git add README.md register.json', 'workflow commits register.json')]
NEW_FILES = {
    "CITATION.cff": 'cff-version: 1.2.0\ntitle: "MCP Conduct Register: a machine generated register of measured MCP server conduct"\nmessage: "If you cite or quote this register, please cite it as below. The measurement records themselves are facts and are not claimed as property."\ntype: dataset\nauthors:\n  - family-names: Oga\n    given-names: Toshikatsu\n    alias: ogasurfproject-jpg\n    affiliation: "The HORIZONs Co., Ltd."\n    orcid: "https://orcid.org/0009-0000-9180-903X"\n    country: JP\nrepository-code: "https://github.com/ogasurfproject-jpg/mcp-conduct-register"\nurl: "https://shield.the-horizons-innovation.com/verify-directory/"\nabstract: >-\n  A register of Model Context Protocol (MCP) servers that records what was\n  measured rather than what anyone recommends. Rows are generated daily from a\n  public API by a script with no editorial input. Every verdict carries a\n  SHA-256 that any third party can recompute from the published bytes, and the\n  accumulated records are anchored to Bitcoin through OpenTimestamps. Records\n  unflattering to the operator are retained, including failures of the\n  operator\'s own servers, because the code contains no route for removing them.\nkeywords:\n  - Model Context Protocol\n  - MCP\n  - AI agents\n  - transparency log\n  - verifiable records\n  - OpenTimestamps\n  - Bitcoin anchoring\n  - vendor neutral registry\nlicense: MIT\n',
    "llms.txt": "# MCP Conduct Register\n\n> A register of Model Context Protocol servers that records what was measured, not what anyone recommends. Rows are generated daily from a public API by a script. Every verdict carries a SHA-256 that anyone can recompute. Unflattering records are retained, including the operator's own failures.\n\n## What this is\n\nMCP Conduct Register is a machine generated public record of how MCP servers behaved when measured. It exists because an agent choosing between tens of thousands of servers can only read what each vendor wrote about itself. This register adds records of conduct that the vendor did not author and cannot delete.\n\n## What this is not\n\nIt is not a curated list, a ranking, a score, or an endorsement. Nobody selects the rows. Placement cannot be bought because there is no placement to buy: the table order is the order the API returns.\n\n## Key facts\n\n- Rows: generated from https://gate.horizonshield.dev/register once per day\n- Verification: every verdict carries a record_sha256 recomputable from published bytes\n- Anchoring: accumulated records are timestamped to Bitcoin via OpenTimestamps\n- Operator neutrality: the code has no route to delete a valid record, including records that embarrass the operator\n- Cost: free, no account, no API key\n\n## Machine readable data\n\n- Register table, human readable: https://github.com/ogasurfproject-jpg/mcp-conduct-register\n- Register data, JSON: https://raw.githubusercontent.com/ogasurfproject-jpg/mcp-conduct-register/main/register.json\n- Live API: https://gate.horizonshield.dev/register\n- Per endpoint history: https://gate.horizonshield.dev/history?endpoint=<url>\n\n## The ledger behind it\n\n- Witness intake, open to anyone: https://ledger.horizonshield.dev/witness\n- Ledger index: https://ledger.horizonshield.dev/ledger\n- Specification NENRIN v1, anchored at Bitcoin block 962507\n- Founding discrepancy record, anchored at Bitcoin block 962511: two independent witnesses reported incompatible observations of the same server and both were correct\n\n## Getting listed\n\nPOST an endpoint to https://gate.horizonshield.dev/watch or open a pull request. Listing changes nothing about the verdict.\n\n## Author\n\nToshikatsu Oga, The HORIZONs Co., Ltd., Hiratsuka, Japan. A carpenter of thirty years. ORCID 0009-0000-9180-903X.\n",
}

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
    for f in NEW_FILES:
        exists = os.path.exists(f)
        print("[anchor] %s not present yet: %s (expect yes)" % (f, "yes" if not exists else "NO"))
        if exists: ok = False
    if not ok:
        print("ABORT: anchor mismatch. Nothing written.")
        sys.exit(1)
    for path, old, new, name in EDITS:
        contents[path] = contents[path].replace(old, new, 1)

    rd = contents["README.md"]
    gn = contents["scripts/build_register.py"]
    wf2 = contents[".github/workflows/build.yml"]
    checks = [
        ("MCP Conduct Register is a machine generated public record" in rd, "readme: quotable definition sentence"),
        ("Questions people actually ask" in rd, "readme: q and a section"),
        ("<!-- REGISTER:START -->" in rd and "<!-- REGISTER:END -->" in rd, "readme: generator markers intact"),
        ("register.json" in gn, "generator: writes the json snapshot"),
        ("register.json" in wf2, "workflow: commits the json snapshot"),
        ("orcid" in NEW_FILES["CITATION.cff"], "citation: orcid present"),
        ("cff-version" in NEW_FILES["CITATION.cff"], "citation: valid cff header"),
        ("What this is not" in NEW_FILES["llms.txt"], "llms.txt: states what it is not"),
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
    for f, body in NEW_FILES.items():
        open(f, "w", encoding="utf-8").write(body)
        print("[written] " + f)
    print("APPLY done. Now: git add -A && git commit && git push, then run the workflow once.")

if __name__ == "__main__":
    main()
