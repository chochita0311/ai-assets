# Refactor Merge Check Form

Use this template when recording a merge-safety or parity checkpoint for a refactor track, step, or batch.

Default location:
- `./docs/refactoring/logs/`

This template is stricter than a normal execution log. It is for decisions, not narration.

## Recommended File Naming

Use a stable sortable pattern:

`YYYY-MM-DD_refactor-xxxx_<scope>-merge-check.md`

Examples:
- `2026-02-24_refactor-0001-level5-7-merge-check.md`
- `2026-02-26_refactor-0003-groupa-merge-check.md`
- `2026-03-18_refactor-0005-final-merge-check.md`

## Canonical Merge Check Template

```md
# [Merge Check Title]

## Scope

- Related track: `[path/to/active-plan.md]`
- Scope under review:
  - `...`
- Compare baseline:
  - `...`
- Baseline resolved commit SHA (if available):
  - `...`
- Baseline certainty:
  - `Confirmed | Provisional`

## Changed Surface

- Added:
  - `...`
- Updated:
  - `...`
- Moved/Renamed:
  - `...`
- Removed:
  - `...`

## Validation Run

- Working tree clean:
  - `Yes | No`
- Build / compile:
  - command: `...`
  - result: `Pass | Fail | Not run`
- Targeted tests:
  - command: `...`
  - result: `Pass | Fail | Not run`
- Full test suite:
  - command: `...`
  - result: `Pass | Fail | Not run`
- Runtime / smoke / manual verification:
  - `...`

## Strict Parity Audit Coverage

- Baseline pinned to immutable target (commit SHA):
  - `Yes | No`
- Source mapping complete (old -> new paths):
  - `Yes | No`
- Query/write semantics audited at logic-unit level:
  - `Yes | No`
- Payload/output mapping audited field-by-field:
  - `Yes | No`
- Side-effect paths audited explicitly:
  - `Yes | No`
- Failure-mode paths audited explicitly:
  - `Yes | No`
- Any unaudited relevant path:
  - `None | ...`

## Merge Assessment

- Safe to merge:
  - `Yes | No | Not yet`
- Behavioral parity vs baseline:
  - `Preserved | Intentional deltas present | Unknown`
- Parity confidence basis:
  - `Strict audit complete | Partial audit | Test-only evidence | Runtime-only evidence`
- External contract parity:
  - `Preserved | Intentional deltas present | Unknown`
- Client-visible change:
  - `No | Yes | Unknown`
- Required fixes before merge:
  - `None` or `...`

## Parity Proof

- Input contract parity:
  - `...`
- Output contract parity:
  - `...`
- Side-effect parity:
  - `...`
- Failure-mode parity:
  - `...`

## Intentional / Reviewed Deltas

- `None` or `...`

## Residual Risks

- `...`

## Next Action

- `...`
```

## Usage Rules

- Use this template when the main question is “is this scope safe to merge?”
- Keep it narrower than a branch diary. Only include the scope under current judgment.
- Treat build and test pass as necessary evidence, not sufficient evidence, for parity.
- If the project's comparison baseline is ambiguous, ask for it when needed; otherwise mark the baseline as provisional and say what assumption was used.
- Internal reordering or code-structure changes are acceptable only if externally observable behavior remains equivalent, unless intentional deltas are explicitly approved.
- If runtime evidence is user-verified or externally observed rather than directly executed, say that explicitly.
- If the full test suite was not run, record that plainly instead of implying broader confidence.
- If the answer is “not yet,” the log should still say what blocks merge and what to do next.
- `Behavioral parity vs baseline = Preserved` is valid only when Strict Parity Audit Coverage is fully satisfied, including side-effect and failure-mode coverage.
