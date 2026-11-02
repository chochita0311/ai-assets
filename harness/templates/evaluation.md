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

For `docs-content`, replace the Spec example with the designated writing contract’s real ID and repository-relative file or section anchor. Do not invent a spec file.

## Scope
- Active feature:
- Active spec:
- Evaluated build or commit:

## Checks
- List the checks actually performed.

## Evidence
- Environments checked: source inspection, automated tests, fresh isolated runtime, active long-running runtime, rendered browser, or another relevant surface.
- Record only directly observed evidence and identify synthetic fixtures or approved runtime data boundaries.
- Select applicable detailed checks from [Design Evaluation](../../policies/review/design-evaluation.md) and [Interaction Evaluation](../../policies/review/interaction-evaluation.md) when those review assets are installed. Record the concrete witness, owner, peer consumers, state transitions, and limitations required by the active feature.
- For source normalization, complex collection or scroll behavior, remote or multi-target actions, and long-running work, follow the relevant owned checks rather than treating a generic fixture or successful endpoint as sufficient evidence.
- For generated analysis, identify comparison inputs and configuration, original outputs, review scope, and observed variation. Separate content, interface, application, and user-outcome evidence using the corresponding Interaction Evaluation checks; identify settings that were only requested and outcomes that were not observed.
- When Harness Improvement is selected and configured, use its [ordinary stage operation](../operations/harness-improvement.md#ordinary-stage-work) for evaluator-role provenance, relevant experience and closing reflection. A logical evaluator role does not establish a separate runtime agent. Keep an audience-safe stage/improvement reference only when useful and permitted.
- When a related harness comparison's first authorized trial has actually started, use [Harness Improvement](../operations/harness-improvement.md) if installed and record an audience-safe experiment reference. Keep per-edit effects with that record's owner; Result and Evidence Coverage here still evaluate this run's declared criteria. Ordinary evaluation alone leaves a change effect `not assessed`. Omit references that are unused or would expose private locators or identifying record IDs; this does not prevent authorized private recording.

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

## Code Review Evidence
- Use when the [independent code challenge gate](../policies/execution-loop-governance.md#independent-code-challenge) is assessed; omit for unrelated evaluation.
- Risk, challenge decision, and acceptance impact:
- Frozen baseline and candidate identities (full commits or bundle/manifests); requested moving-reference recheck:
- Each side's dependency/configuration/environment state and guidance source, revision, content fingerprint:
- Raw packet, observation time, evidence locators, and actual access limits:
- Actual hard limits: source, units, scope, original/current bound, observability/enforcement, authorized changes:
- Review planning allocation/checkpoints; revisions, new information or expected information gain and rationale:
- Observed usage, spent attempts including stale/interrupted attempts, pending commitments, remaining capacity and closeout reserve:
- Worker stop/return boundaries, reassessment and stop/resume conditions; unaffected feasible work after a scoped limit:
- Review stage: `initial discovery` | `informed dispute` | `repair confirmation` | `self-review`:
- Actual reviewer/history/instruction/tool/permission exposure; unobserved runtime fields:
- Context, method, source-lineage, and validation-data independence/limits:
- Inspected paths, callers/terminal consumers, witnesses/method/results, and unaudited reasons:
- Initial return, bounded validation requests/results, fixture/oracle checks, and adjudication evidence:
- Candidate trigger, reachability, baseline/candidate behavior, causal delta/location, impact, support/counterevidence, severity/confidence:
- Candidate category: `new regression` | `pre-existing defect` | `authorized intentional delta` | `unproven concern`:
- Claim status: `supported` | `refuted` | `unresolved`; action: `fixed` | `accepted intentional delta` | `retained` | `deferred`; reason and remaining limit:
- Significant dispute/self-adjudication conflict and informed adjudicator or discriminating validation, when needed:
- Baseline -> current whole-scope and previous candidate -> current delta checks; changed inputs and invalidated/renewed witnesses:
- Carried unresolved claims/actions, corrected or retracted prior claims, and remaining acceptance gaps:
- Apply [shared resource governance](../policies/workflow-governance.md#resource-governance): planning revisions do not reset usage or waive strict parity, independence, coverage or unresolved-objection gates. Keep any actual hard-limit stop/overrun separate from Result and Evidence Coverage.

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
