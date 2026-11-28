# Refactor Log Form

Use this template for a step, batch, blocker, runtime-smoke, wrap-up, or handoff event. Record a parity or merge-safety decision in [the merge-check](merge-check.md). The [logging method](../references/method.md#artifact-selection-and-logging) explains how an event can cite that decision.

## Canonical Log Template

```md
# [Log Title]

## Log Type

- Type: `Step | Batch | Blocker | Runtime Smoke | Wrap-Up | Handoff`
- Date: `YYYY-MM-DD`
- Related track: `[path/to/existing-plan.md] | None`
- Scope: `[step, batch, slice, or decision scope]`

## Summary

- Goal:
  - `...`
- Outcome:
  - `Pass | Partial | Blocked | Reverted`
- Short conclusion:
  - `...`

## What Changed

- Added:
  - `...`
- Updated:
  - `...`
- Moved/Renamed:
  - `...`
- Removed:
  - `...`

## Behavior / Parity Notes

- Behavior-preserving intent:
  - `...`
- Intentional deltas:
  - `None` or `...`
- Important compatibility or contract notes:
  - `...`
- Existing parity or merge decision for the same baseline, candidate, and scope (choose one):
  - `No matching decision`
  - `[link to merge-check] — [its verdict, evidence basis, and material qualifications, including any confirmed regression]`
  - `[link to merge-check] — Verdict withheld pending reassessment. [What changed, what remains established, and the next check.]`

## Validation

- Baseline or compare target:
  - `...`
- Baseline resolved commit SHA (if available):
  - `...`
- Candidate used for this event:
  - `[commit, immutable bundle, or observed artifact identity and evidence locator] | Unknown | No candidate involved`
- Build / compile:
  - command: `...`
  - result: `...`
- Targeted tests:
  - command: `...`
  - result: `...`
- Runtime / smoke / manual verification:
  - `...`

## Risks / Limitations

- Known residual risks:
  - `...`
- What this log does not prove:
  - `...`

## Next Action

- Next step:
  - `...`
- Handoff note:
  - `None` or `...`
```
