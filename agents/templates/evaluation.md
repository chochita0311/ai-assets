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
- For a content-triggered presentation defect, record the privacy-safe witness shape, generated semantic DOM, overflow owner at relevant container levels, and the deterministic regression retained at the shared owner. Generic long-content evidence is not a substitute when punctuation, indentation, nesting, or transformation caused the failure.
- For parallel or nested scrolling regions, record the document and local scroll owners at each relevant breakpoint, the short and long content combinations exercised, and the input, focus, edge-inset, and scroll-chaining behavior observed.
- For imported transcript, history, audit, or activity normalization, record the source roles or envelopes, retained raw evidence, visible projection, unknown-envelope fallback, and sparse or command-only cases exercised.
- For grouped, nested, or sequentially disclosed collections, record the semantic levels, owning headings, per-level ordering rules, overflow or disclosure boundaries, control placement in closed and expanded states, visual and DOM order, keyboard focus order, any deliberate focus handoff, and representative single, multiple, and narrow-layout states.
- For inherited identity cues, record the cross-surface states checked, including direct entry and parent-owned child presentation when applicable.
- For multi-target actions, record the per-target states and outcomes checked, including partial outcomes and user-visible consequences when applicable.
- For a remote, costly, destructive, or multi-target action, record preview or preflight evidence separately from execution evidence, including scope, target or operation counts, readiness gating, and any verified no-side-effect path.
- For a long-running action, record the observed phase sequence, progress unit and denominator when determinate, exceptional-run reason, interruption or fallback path, and terminal handoff.

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
