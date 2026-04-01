# Refactor Log Form

Use this template when writing a refactor execution log.

Default location:
- `./docs/refactoring/logs/`

Keep logs event-shaped and decision-useful. A log should help someone understand what changed, what was proven, and what remains.

## Recommended File Naming

Use a stable sortable pattern:

`YYYY-MM-DD_refactor-xxxx_<event-slug>.md`

Examples:
- `2026-03-18_refactor-0005-step3-completion.md`
- `2026-03-09_refactor-0005-platform-cutover-blocked.md`
- `2026-02-25_refactor-0003-runtime-smoke-baseline.md`
- `2026-03-18_refactor-0005-final-wrapup.md`

If the project does not use numbered refactor tracks, replace `refactor-xxxx` with the local track name.

## Canonical Log Template

```md
# [Log Title]

## Log Type

- Type: `Step | Batch | Blocker | Runtime Smoke | Merge Check | Wrap-Up | Handoff`
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

## Validation

- Baseline or compare target:
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

## Log-Type Adaptation Rules

### Step or Batch Log

Use the canonical template as-is.

Emphasize:
- exact scope completed
- compatibility adjustments made during the step
- validation that makes the step merge-safe or reviewable

### Blocker Log

Keep:
- `Log Type`
- `Summary`
- `Behavior / Parity Notes`
- `Validation` if there is failure evidence
- `Risks / Limitations`
- `Next Action`

In `Summary`, state:
- what was attempted
- first confirmed blocker
- whether the code was reverted to a stable baseline

### Runtime Smoke Log

Replace `What Changed` with:

```md
## Environment / Assumptions

- `...`

## Checks Performed

- `...`
```

In `Validation`, record:
- endpoints, services, queues, commands, or runtime checks used
- observed results
- scope limits, especially what was not verified end-to-end

### Wrap-Up or Handoff Log

Keep the canonical structure, but compress `What Changed` into high-level closure points.

Emphasize:
- scope closed
- final validation status
- accepted deltas
- deferred work
- destination of the next track

## Writing Rules

- Prefer facts over narrative.
- Prefer scoped bullet points over long prose.
- Do not bury blockers inside generic “notes”.
- If a change was reverted, say so explicitly.
- If a validation was not run, say so explicitly.
- If a log only proves a narrow scope, say so explicitly.
- Keep the title aligned with the actual event, not the whole initiative.
