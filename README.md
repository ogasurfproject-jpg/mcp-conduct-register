# MCP Conduct Register

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
The table has not been generated yet. Run `python3 scripts/build_register.py` or wait for the
scheduled workflow.
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

## License

Code MIT. The measurement records are facts and are not claimed as property.
