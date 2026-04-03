# Workflow Context Sync Checklist

Use this checklist before concluding the context-sync stage.

## Contract Check

- Is `workflow root` explicit?
- Is `current repo` explicit or tracked as an open question with a resolution plan?
- Is one canonical context path selected?
- Are related repos resolved or clearly marked unresolved?
- Are in-scope sources listed with type and identifier/location?
- Is each source assigned a role?
- Are source relationships (for example parent/child or dependencies) captured when relevant?
- Are source-of-truth rules recorded?

## Reconciliation Check

- Are key claims compared across sources?
- Are statuses labeled as `aligned`, `conflict`, or `open`?
- Are working assumptions explicit?
- Are follow-up update targets defined for mismatches?

## Gate Check

- Was a context summary or diff shown to the user?
- Are conflicts and open questions presented before implementation?
- Is `user review status` still `pending` until explicit proceed signal?
- Did implementation start only after a valid signal?

## Maintenance Check

- Are confirmed facts separated from open questions?
- Is `drift watchlist` updated?
- Is source sync status (checked sources + deltas) updated?
- Does handoff note give a clear next-session restart point?

## Final Question

- Can the next session continue from canonical context without re-deriving source scope and conflicts?
