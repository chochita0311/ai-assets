# Workflow Context Sync Checklist

Use this as the final yes-or-no pass.

## Placement

- Is invocation origin classified as explicit or implicit?
- Is creation authority recorded separately from target certainty?
- Is requested durability classified as session-only acceptable, durable outcome requested, or unspecified?
- Is the disposition explicitly `session-only`, `maintain existing`, `propose persistence`, or `initialize after approval`?
- Does the disposition include a concise reason?
- Is context home explicit when one is used?
- When persistence applies, is the canonical target resolved independently from `cwd`, working root, and current repo?
- When a target exists, is its kind identified as a document set or dedicated workflow context?
- If the target was ambiguous, was persistence left pending without creating a fallback file?
- If a new artifact was created, did an explicit user request authorize `initialize`?
- Was disposition selected after checking for an existing canonical target?

## Reconciliation

- Was the canonical target read before broad scanning?
- Were only decision-relevant sources refreshed?
- Does each source have a role and freshness state?
- Are conflicts and open claims preserved instead of blended?
- Were durable changes written only to their owning context artifacts?

## Boundaries

- If invocation was implicit, was creation withheld even when a plausible target or note existed?
- If session-only handling was sufficient, was unnecessary target selection or questioning avoided?
- If new persistence was only beneficial, was it offered non-blockingly without creating anything?
- If new persistence was required, were the target and kind proposed for explicit approval before creation?
- Was a working note kept non-canonical unless explicitly promoted?
- Was the note treated only as source evidence rather than as a target mapping?
- Was a session-only synthesis reported honestly as unsaved?
- Did downstream implementation wait for the required review signal?
- Did the final report name the resolved target, files updated, and review status?

## Consolidation

- Was the canonical target selected before merging candidates?
- Were unique facts, provenance, and unresolved questions preserved?
- Were keep, archive, and delete-candidate dispositions separated?
- Were destructive cleanup actions withheld until explicitly approved?

## Final Question

- Can a new session start from the resolved target without creating another context file or repeating the same source discovery?
