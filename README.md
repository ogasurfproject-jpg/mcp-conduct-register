# MCP Conduct Register

> Part of **[Awesome HORIZON SHIELD](https://github.com/ogasurfproject-jpg/awesome-horizon-shield)** — the checkable index of every dataset, MCP server and ledger we run.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21970931.svg)](https://doi.org/10.5281/zenodo.21970931)
[![Rebuilt daily from a public API](https://img.shields.io/badge/rebuilt-daily%20from%20a%20public%20API-2f6feb)](https://gate.horizonshield.dev/register)
[![Rows chosen by](https://img.shields.io/badge/rows%20chosen%20by-nobody-6e7681)](https://github.com/ogasurfproject-jpg/mcp-conduct-register/blob/main/scripts/build_register.py)
[![Atom feed](https://img.shields.io/badge/feed-atom-e36209)](https://raw.githubusercontent.com/ogasurfproject-jpg/mcp-conduct-register/main/feed.xml)
[![License MIT](https://img.shields.io/badge/license-MIT-2ea043)](https://opensource.org/licenses/MIT)

**MCP Conduct Register is a machine generated public record of how Model Context Protocol servers
behaved when they were measured.** It is not a curated list of good servers. Nobody selects the rows,
placement cannot be bought, and records that embarrass the operator are retained because the code
contains no route for removing them.

**This is not a curated list of good servers. It is a record of what was measured.**

Nobody chose these rows. They are generated from a public API once a day by a script in this
repository, and the script has no opinion. A row appears because an endpoint is on the
measurement schedule, not because anyone liked it. A green row means the conditions that were
measured passed on that date. It does not mean the numbers a server returns are correct, or
that the business behind it is any good.

Absence is not a negative verdict. An endpoint that is not here has simply never been measured here.

## Why this exists

An agent choosing between tens of thousands of MCP servers can only read what each vendor wrote
about itself. This register adds the missing layer: records of conduct that the vendor did not
author and cannot delete.

Every verdict carries a `record_sha256` that anyone can recompute from the published bytes.
The measurement code, the gate that runs it, and this generator are all public.

<!-- REGISTER:START -->
Generated from <https://gate.horizonshield.dev/register> at 2026-08-29 01:53 UTC.

**8 rows.** Nobody chose them. This table is written by a script, not a person.

| Server | Endpoint | Latest verdict | Measured | Public measurements | record_sha256 | History |
|---|---|---|---|---|---|---|
| KIRA fair price audit (the flagship MCP server)<br><sub>KIRA適正診断</sub> | `https://mcp.horizonshield.dev/mcp` | verified | 2026-08-28 | 30 | `dd55e4c14f70` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Fmcp.horizonshield.dev%2Fmcp) |
| YAKUMO verified contractor directory<br><sub>YAKUMO加盟店ディレクトリ</sub> | `https://hearing.horizonshield.dev/mcp` | verified | 2026-08-28 | 30 | `e67f16a8b678` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Fhearing.horizonshield.dev%2Fmcp) |
| KIRA intake desk for renovation questions<br><sub>KIRA相談窓口</sub> | `https://web.horizonshield.dev/mcp` | verified | 2026-08-28 | 30 | `0bf2d176a456` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Fweb.horizonshield.dev%2Fmcp) |
| JIDEC, the Bitcoin anchored public ledger<br><sub>JIDEC 公開検証台帳</sub> | `https://jidec.horizonshield.dev/mcp` | verified | 2026-08-28 | 21 | `ddeb7ea047be` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Fjidec.horizonshield.dev%2Fmcp) |
| Reform Shokunin Co., Ltd. (member No.001, Aichi)<br><sub>リフォーム職人株式会社（加盟No.001）</sub> | `https://p001.horizonshield.dev/mcp` | pending | 2026-08-28 | 30 | `eacfe0777339` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Fp001.horizonshield.dev%2Fmcp) |
| Mineo Toyo Juki Co., Ltd. (member No.002)<br><sub>ミネオトーヨー住器株式会社（加盟No.002）</sub> | `https://p002.horizonshield.dev/mcp` | verified | 2026-08-28 | 30 | `5d286c0a7143` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Fp002.horizonshield.dev%2Fmcp) |
| The verification gate, measuring itself<br><sub>検証ゲート（この検査機自身）</sub> | `https://gate.horizonshield.dev/mcp` | verified | 2026-08-28 | 30 | `083eba63195e` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Fgate.horizonshield.dev%2Fmcp) |
| Femtech source registry (verify sources, never diagnose)<br><sub>フェム情報源レジストリ</sub> | `https://femtech.horizonshield.dev/mcp` | verified | 2026-08-28 | 2 | `13a6a1c69d22` | [history](https://gate.horizonshield.dev/history?endpoint=https%3A%2F%2Ffemtech.horizonshield.dev%2Fmcp) |

Measured by gate commit `unpinned: this deployment did not inject a commit (deploy_gate.sh not used)`. The commit that produced each verdict is inside the hashed record.

> The public register. Rows are scheduled measurements, not endorsements. An endpoint that is absent has simply never been measured here; absence is NOT a negative verdict. Webhooks are never published. Every stored verdict carries a record_sha256 you can recompute yourself. The operator_label field is a display name assigned by the operator, not a measurement.
<!-- REGISTER:END -->

## Verify any row yourself

```
curl -s "https://gate.horizonshield.dev/history?endpoint=<the endpoint>"
```

Recompute the hash of any record and compare it with the `record_sha256` in the response. If they
disagree, that disagreement is itself worth publishing, and the ledger below will accept it.

## Get listed

Two ways, both free, neither changes the verdict.

**One command:**

```
curl -s -X POST https://gate.horizonshield.dev/watch \
  -H 'content-type: application/json' \
  -d '{"endpoint":"https://your-server/mcp"}'
```

**Or open a pull request** against `requests/` in this repository with a file named after your
server. See CONTRIBUTING.md. A maintainer adds the endpoint to the measurement schedule. Nothing
else about the listing is negotiable, including the verdict.

## The ledger behind this

Measurements accumulate into monthly rings anchored to Bitcoin through OpenTimestamps. Anyone can
submit an observation of any endpoint as a witness, under their own name and vantage. The operator
holds no veto in code.

- Witness intake, GET returns a self description: <https://ledger.horizonshield.dev/witness>
- The ledger: <https://ledger.horizonshield.dev/ledger>
- Specification, anchored at Bitcoin block 962507: [NENRIN_SPEC_v1](https://github.com/ogasurfproject-jpg/horizon-shield/blob/main/workers/hs-ledger/nenrin/NENRIN_SPEC_v1.md)
- The founding discrepancy record, two witnesses disagreeing about the operator's own server, both correct, anchored at block 962511: [NENRIN_DISCREPANCY_0001](https://github.com/ogasurfproject-jpg/horizon-shield/blob/main/workers/hs-ledger/nenrin/NENRIN_DISCREPANCY_0001.md)

## What this register does not do

It does not rank. It does not score. It does not accept payment for placement, and there is no
placement to buy: the order of the table is the order the API returns. It will not remove an
unflattering record, including about the operator's own servers. The operator is the first test
subject under these rules and the failing records are still here.

## How to cite this register

Archived on Zenodo with a permanent identifier, so a citation survives this repository moving or
disappearing.

```
Oga, Toshikatsu (2026). MCP Conduct Register: a machine generated register of measured MCP server
conduct. Zenodo. https://doi.org/10.5281/zenodo.21970931
```

BibTeX and APA forms are generated by the "Cite this repository" button on GitHub, which reads
`CITATION.cff`. The author is identified by ORCID 0009-0000-9180-903X, so this register sits in the
same record as the open dataset and the preprints it was built from.

When citing a single row rather than the register, cite the endpoint's history URL and the
`record_sha256` of the verdict you are relying on. That pair is enough for a reader to recompute the
record and confirm you quoted it correctly.

## Questions people actually ask

**How is this different from an awesome list?**
An awesome list is a human recommending things. This is a script reporting measurements. No human
chose any row here, and the generator is in this repository so you can check that claim.

**Can I pay to be listed, or to be listed higher?**
No, and there is nothing to buy. The order of the table is the order the API returns. There is no
ranking and no score.

**What does a green row prove?**
That the conditions which were measured passed on that date, from the vantage that measured them.
It does not prove the numbers a server returns are correct, or that the business behind it is
competent, or that it is safe to use.

**What if your own server fails?**
It has, and the record is still published. The gate measures its own endpoint under the same rules.
The founding record of the ledger behind this register is a disagreement between two witnesses about
the operator's own server, in which both witnesses turned out to be correct.

**Can I dispute a verdict?**
Yes, and that is the point. Measure the endpoint yourself and submit your observation to the public
ledger under your own name and vantage. If your report conflicts with this register, the conflict
becomes a permanent citable record. The operator has no veto in code.

**Who runs this?**
Toshikatsu Oga, The HORIZONs Co., Ltd., Hiratsuka, Japan. A carpenter of thirty years.
ORCID [0009-0000-9180-903X](https://orcid.org/0009-0000-9180-903X).

**How do I cite this register?**
See CITATION.cff, or use the "Cite this repository" button on GitHub. A machine readable snapshot of
the current table is published as `register.json` in this repository.

## License

Code MIT. The measurement records are facts and are not claimed as property.
