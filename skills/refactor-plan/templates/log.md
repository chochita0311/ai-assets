# Refactor Log Form

Use this template for a step, batch, blocker, runtime-smoke, wrap-up, or handoff event. Use [merge-check.md](merge-check.md) for parity and merge-safety decisions, and [../references/method.md](../references/method.md) for artifact-selection and adaptation rules.

## Canonical Log Template

```md
# [Log Title]

## Log Type

- Type: `Step | Batch | Blocker | Runtime Smoke | Wrap-Up | Handoff`
- Date: `YYYY-MM-DD`
- Related track: `[path/to/active-plan.md]`
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
- Parity claim status:
  - `Preserved | Provisional | Unknown`
- Parity confidence basis:
  - `Strict audit complete | Partial audit | Test-only evidence | Runtime-only evidence`
- If `Preserved`, strict baseline audit completed:
  - `Yes | No`

## Validation

- Baseline or compare target:
  - `...`
- Baseline resolved commit SHA (if available):
  - `...`
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
