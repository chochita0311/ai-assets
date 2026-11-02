# Run Template

## Metadata
- ID: `run-YYYYMMDD-01`
- Status: `active`
- Feature: `[feat-0000-title](../feature/feat-0000-title.md)`
- Parent PRD: `[prd-0000-title](../prd/prd-0000-title.md)`
- Active Spec: `[spec-0000-title](../spec/spec-0000-title.md)`
- Surface:
- Execution Profile:
- Required Evaluators:
- Created: `YYYY-MM-DD`
- Updated: `YYYY-MM-DD`

For `docs-content`, replace both spec-file examples with the designated writing contract’s real ID and repository-relative file or section anchor. Do not create a spec file just to fill this template.

## Goal
- Record one active execution pass for one approved feature.
- Treat one run as an automated execution unit that reports back to the human owner.

## Selected Loop
- Feature type:
- Surface:
- Surface lanes:
- Required evaluators:
- Current phase:

## Surface Lanes
- Use only when the feature spans multiple surfaces.
- Lane:
  - path roots:
  - dependencies:
  - owning role:
  - validation evidence:
  - evaluator ownership:

## Contract Surfaces
- APIs, schemas, messages, generated outputs, routes, commands, config, source-of-truth ownership, or integration boundaries checked in this run.

## Invocation Context
- Golden sources:
- Relevant policies:
- Optional skills or tools expected:

## Resources When Relevant

Use the existing run for applicable facts under
[shared resource governance](../policies/workflow-governance.md#resource-governance).
Do not invent numeric limits to fill fields; keep unobserved values unknown.

- Actual hard limits: source, units, scope, original/current bound and observability/enforcement:
- Authorized actual-limit changes, reason and authority; preserve consumed resources:
- Planning checkpoints/allocations and revisions, rationale and new information or expected information gain:
- Observed usage, stale/interrupted attempts when applicable, pending commitments, remaining capacity and closeout reserve:
- Worker stop/return boundaries, reassessment and stop/resume conditions; feasible unaffected work after a scoped limit:
- Actual hard-limit overrun or resource-block reason, affected work and unmet acceptance, separate from evaluator Result and Evidence Coverage:
- Resource-blocked predecessor/follow-up run and post-report human decision, when applicable:
- Verified resumption capacity/authority and feature/spec validity; cumulative task usage and commitments carried into the new run:

## Optional Harness Experience

- When Harness Improvement is selected and configured, the
  [ordinary stage operation](../operations/harness-improvement.md#ordinary-stage-work)
  handles relevant retrieval, stage evidence and common improvement records.
- Stage/improvement references and meaningful reuse or persistence gaps, only when
  this record's audience may access them:
- Related experiment reference, only when a comparison's first authorized trial
  has actually started and this record's audience may access that reference:
- Use [Harness Improvement](../operations/harness-improvement.md) when installed.
  Keep records and effects with their private owners; do not put private
  locators or identifying record IDs in public runs. Omit this section when
  unused or unsafe to reference; private recording does not require a public link.

## Current Artifacts
- Active Spec: `[spec-0000-title](../spec/spec-0000-title.md)`
- Contract evaluation: `[eval-0000-contract-title](../evaluation/eval-0000-contract-title.md)`
- Design evaluation: `[eval-0000-design-title](../evaluation/eval-0000-design-title.md)`
- Functional evaluation: `[eval-0000-functional-title](../evaluation/eval-0000-functional-title.md)`
- UX heuristic evaluation: `[eval-0000-ux-title](../evaluation/eval-0000-ux-title.md)`
- Fix log: `[fix-0000-title](../fix/fix-0000-title.md)`
- Heuristic backlog: `[heur-0000-title](../heuristic/heur-0000-title.md)`

## Evaluation Coverage
- Evaluator:
  - Result: `PASS` | `PASS WITH SUGGESTIONS` | `FAIL`
  - Evidence Coverage: `complete` | `partial` | `unavailable`
  - Environments or states checked:
  - Unverified claims:
  - Acceptance impact: `blocking` | `non-blocking` | `not applicable`

## Current Route
- Next role:
- Current blocker classification:
- In-run route:
- Post-run recommendation for human review:

## Attempts
- Attempt 1:
  - status:
  - outcome:
  - notes:

## Post-Contract Regression Check
- Needed:
- Result:
- Notes:

## Human Review Outcome
- Decision:
- Returned layer if any:
- Follow-up run:

## Continuity Notes
- `YYYY-MM-DD`: run initialized
