# Evaluation Template

## Metadata
- ID: `eval-0000`
- Status: `draft`
- Evaluator Type: `contract` | `design` | `functional` | `ux-heuristic`
- Result: `PASS` | `PASS WITH SUGGESTIONS` | `FAIL`
- Run ID:
- Attempt:
- Feature: `[feat-0000-title](../feature/feat-0000-title.md)`
- Spec: `[spec-0000-title](../spec/spec-0000-title.md)`
- Execution Profile:
- Surface Lane:
- Evidence Coverage: `complete` | `partial` | `unavailable`
- Created: `YYYY-MM-DD`

## Scope
- Active feature:
- Active spec:
- Evaluated build or commit:

## Checks
- List the checks actually performed.

## Evidence
- Environments checked: source inspection, automated tests, fresh isolated runtime, active long-running runtime, rendered browser, or another relevant surface.
- Record only directly observed evidence and identify synthetic fixtures or approved runtime data boundaries.
- Record whether each reported exemplar is instance-specific or exercises a shared renderer, component, token, control, or state owner; for shared owners, name the representative peer consumers or equivalent scopes checked.
- For a remote, costly, destructive, or multi-target action, record preview or preflight evidence separately from execution evidence, including scope, target or operation counts, readiness gating, and any verified no-side-effect path.

## Evidence Gaps
- List required but unavailable evidence and the claims that remain unverified.
- Owning requirement: feature acceptance point, spec requirement, or profile evidence rule.
- Acceptance impact: `blocking` | `non-blocking` | `not applicable`.
- Keep `Result` for the evaluator outcome; do not invent a new result label to encode evidence coverage.
- A `PASS` with partial or unavailable evidence must state whether the gap blocks acceptance under the owning feature, spec, or profile.

## Contract Evidence
- Use when evaluator type is `contract`.
- Producer surfaces:
- Consumer surfaces:
- Schemas, payloads, generated artifacts, commands, routes, config, or policy docs checked:
- Stale-assumption check:

## Findings
- For each finding, record:
  - severity
  - classification: `implementation bug` | `spec gap` | `planning gap` | `suggestion`
  - description
  - evidence
  - fix hint

## Regression Notes
- Name any regression surfaces checked and their status.

## Route
- Next action:
  - `fix`
  - `spec-review`
  - `planning-review`
  - `pass`

## Continuity Notes
- Add dated notes when this report is revised.
