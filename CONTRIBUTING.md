# Getting an endpoint onto the measurement schedule

This register measures MCP endpoints on a schedule and publishes what it finds. Adding your
endpoint does not buy you anything except measurement. The verdict is whatever the measurement
says, and an unflattering result stays published.

## The fast way

```
curl -s -X POST https://gate.horizonshield.dev/watch \
  -H 'content-type: application/json' \
  -d '{"endpoint":"https://your-server/mcp"}'
```

You appear on the next rebuild of the table.

## By pull request

Add a file at `requests/<your-server-name>.json`:

```json
{
  "endpoint": "https://your-server/mcp",
  "contact": "optional, so we can tell you if the endpoint stops answering"
}
```

Open the pull request. A maintainer puts the endpoint on the schedule. The pull request does not
decide the verdict, and no maintainer can.

## What we will not do

- Rank, score, or sort servers by anything except the order the API returns
- Accept payment for placement or for a better verdict
- Remove a record because it is unflattering, including our own
- Publish a webhook, a contact address, or anything else you did not put in the endpoint itself

## What you can do that we cannot

Measure us. Anyone can submit an observation of any endpoint on this register to the public ledger,
under their own name and vantage, and there is no route in the code for the operator to refuse a
schema valid submission.

```
curl -s https://ledger.horizonshield.dev/witness
```

If what you observe conflicts with what this register says, that disagreement becomes a permanent
citable record. The founding record of the ledger is exactly such a conflict about the operator's
own server, and both witnesses turned out to be right.
