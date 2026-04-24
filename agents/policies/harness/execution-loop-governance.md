# Execution Loop Governance

## Purpose
- Define how approved features move through spec, build, evaluation, fix, escalation, and post-run review.
- Keep execution loops traceable, bounded, profile-aware, and type-aware.
- Make return semantics explicit so teams can distinguish in-run fixes from post-run returns to spec or planning.

## Ownership
- This document owns execution-loop rules and return semantics.
- In a consuming repo, use `docs/agents/flows/workflow.md` for sequence examples.
- In a consuming repo, use `docs/policies/harness/prd-feature-management.md` for planning-layer rules and approval criteria.
- In a consuming repo, use `docs/policies/harness/execution-profiles.md` for profile selection, surface lanes, and evaluator routing.
- In a consuming repo, use `docs/policies/harness/traceability-and-link-hygiene.md` for portable reference and source-of-truth path rules.

## Execution Artifacts
- In a consuming repo, `docs/plans/run/` owns active run records.
- In a consuming repo, `docs/plans/spec/` owns implementation-facing specs.
- In a consuming repo, `docs/plans/evaluation/` owns evaluator reports.
- In a consuming repo, `docs/plans/fix/` owns fix logs.
- In a consuming repo, `docs/plans/heuristic/` owns heuristic backlog records.

## Core Operating Rules
- Only one feature should normally be `in-loop` at a time.
- Do not execute from raw planner output.
- Do not silently expand scope during build, evaluation, or fix.
- Every execution artifact must reference the active feature ID, active spec ID, run ID, execution profile, and relevant attempt.
- If a blocker belongs to planning or spec, route upward instead of normalizing it as an implementation defect.
- Treat one active run as an automated execution unit.
- Human review normally happens after the run reports its result, unless the run is technically blocked and cannot continue.
- Scope, spec, or planning returns should be recorded as post-run routing decisions, not hidden in-run redirects.

## Execution Return Model
The normal operating structure is:

1. Run from one approved feature.
2. Complete the automated execution loop or stop on a technical blocker.
3. Report the result to the human owner.
4. Let the human owner decide whether to accept, return to spec, return to planning, or unblock locally.
5. Correct the owning layer.
6. Start a new run from the corrected point.

Use this model instead of ambiguous phrases such as "go back", "resolve", or "fix" without classification.

### Continue In Loop
- Use this when the issue is an `implementation bug`.
- The approved feature and active spec are still valid.
- Stay inside the current execution loop.
- Apply targeted fixes.
- Re-run only the needed evaluators.

### Post-Run Return To Spec
- Use this when the approved feature boundary is still valid, but the active spec is too weak, contradictory, or underspecified.
- Record the run result and post-run recommendation.
- Update the spec first.
- Start a new run from build or targeted fix work against the corrected spec.

### Post-Run Return To Planning
- Use this when the problem changes approved scope, mode meaning, dependency meaning, contract ownership, or user-visible intent.
- Return to feature review or PRD review.
- Re-approve the corrected boundary before resuming spec or build.
- Start a new run after the corrected planning artifact is trustworthy.

### Technical Block Exception
- A run may stop early only when it is technically blocked and cannot continue safely.
- Record the run as `blocked`.
- Report the blocker to the human owner.
- Only after that report should the human owner decide whether the next step is local unblock, return to spec, or return to planning.

## Practical Decision Rule
Ask these questions in order:

1. Is the approved feature boundary still correct?
2. Is the active spec still correct?
3. Is only the implementation wrong?

Route based on the first broken layer:
- boundary wrong after run review: return to planning
- boundary correct but spec weak after run review: return to spec
- boundary and spec correct but implementation wrong: continue in loop

## Optional Capability Rule
- A role may have optional local skills or optional MCP tools that improve execution quality.
- Document those capabilities in the role contract when omission would reduce consistency.
- If the capability exists in the current environment and is relevant to the active feature, it should be used.
- If the capability does not exist in the current environment, the role must still remain operable through its base contract.
- Do not turn optional capabilities into hard blockers unless the project explicitly promotes them into required tooling.

## Dependency Depth Guidance
- Prefer dependency depth of `2` or less for any active feature.
- If dependency depth exceeds `2`, the planner or orchestrator should:
  - justify why the deeper chain is still stable
  - or split the feature or contract work before execution continues
- Treat this as a warning rule, not a hard universal ban.

## Feature-Type-Aware Loops
- `foundation` feature default loop:
  - Spec Agent
  - Builder or contract updater
  - Contract Evaluator
  - Functional Evaluator only when runtime behavior also changes
  - Fix Agent
  - re-evaluate
- `product` feature default loop:
  - Spec Agent
  - Builder
  - Contract Evaluator when contracts, generated artifacts, source-of-truth ownership, or integration boundaries matter
  - Design Evaluator when visual surfaces matter
  - Functional Evaluator
  - UX Heuristic Evaluator as side-channel
  - Fix Agent
  - re-evaluate

## Fail Classification
Every blocking finding should be classified as one of:

- `implementation bug`
  - the approved spec is clear and the implementation does not satisfy it
- `spec gap`
  - the feature is approved, but the active spec is too weak or contradictory to execute safely
- `planning gap`
  - the issue changes approved scope, unresolved dependency meaning, contract ownership, or product-boundary intent

## Classification Examples
- `implementation bug`
  - an API response omits a field required by the active spec
  - a generated artifact has the right contract but is not regenerated after source changes
  - an approved interaction stops working even though the spec defines the expected behavior
- `spec gap`
  - a feature needs a schema or payload rule, but the spec does not define the value shape
  - a multi-surface feature does not define which lane owns the shared contract
  - a UI feature changes rerender behavior, but the spec does not define whether controls must survive or be rebound after rebuild
- `planning gap`
  - execution reveals that the approved feature combined foundation and product outcomes that should have been split
  - execution reveals a missing mode, ownership decision, or dependency order that should have been resolved before spec

## Return Path
- `implementation bug`:
  - continue in loop
  - apply targeted fix
  - re-evaluate as needed
- `spec gap`:
  - finish the current automated run unless a technical blocker prevents continuation
  - report to the human owner
  - return to spec review only after human decision
  - start a new run from build or targeted fix work after spec correction
- `planning gap`:
  - finish the current automated run unless a technical blocker prevents continuation
  - report to the human owner
  - return to feature or PRD review only after human decision
  - re-approve before starting a new run into spec or build

## Heuristic Side-Channel Rule
- `UX Heuristic Evaluator` is a signal emitter, not a default blocking gate.
- It may return:
  - `PASS`
  - `PASS WITH SUGGESTIONS`
  - `FAIL`
- `PASS WITH SUGGESTIONS` does not block feature completion.
- Suggestions should be recorded in heuristic backlog artifacts and considered in later planning.
- `FAIL` should be reserved for:
  - dead-end interaction
  - severe orientation loss
  - unrecoverable navigation confusion
  - contradiction inside already approved scope
- If a heuristic failure implies new scope, report it for post-run human review instead of fixing ad hoc inside the run.

## Heuristic Severity Guidance
- `low` and `medium` heuristic findings should default to backlog suggestions.
- `high` heuristic findings should still default to backlog unless they contradict the already approved feature contract.
- Only clearly blocking heuristic failures should stop the active loop.

## Spec Readiness Gate
Do not start executable spec work when:
- a required foundation feature is not `passed`
- an open PRD item still changes the active feature
- the user-visible outcome or contract outcome is still ambiguous
- required fallback behavior is still undefined
- required execution profile, surface lanes, or evaluator ownership are undefined for multi-surface work

## Traceability Rules
- Use one run identifier such as `run-YYYYMMDD-01` for each active execution pass.
- Use one spec document per active feature loop.
- A run may include multiple attempts when execution loops locally or is retried after a technical blocker.
- Record return-to-spec or return-to-planning as post-run human decisions rather than as silent in-run redirects.
- Use evaluator reports that name:
  - run ID
  - attempt number when relevant
  - feature ID
  - spec ID
  - execution profile
  - surface lane when relevant
  - evaluator type
  - pass/fail result
  - fail classification when blocked
- Use fix logs that reference the evaluator reports they addressed.
- Use fix logs that also reference the active run ID.
- Use fix logs that reference the active attempt when the same run has multiple passes.
- Use heuristic backlog entries for non-blocking suggestion accumulation.

## Post-Contract Regression Check
- When a run changes a source-of-truth contract, generated-data contract, identity model, route contract, schema, payload, command contract, or integration boundary, the run should check for stale assumptions in:
  - runtime code
  - consumers and producers
  - generators, scripts, fixtures, and generated artifacts
  - adjacent policy, architecture, or contract docs
- Treat this as a default post-run verification step, not an optional question for the human owner.
- Record the result in the run report when the changed contract could plausibly leave stale paths behind.

## Invalidation Rule
- If later evidence proves that an earlier execution pass was based on a wrong feature boundary, wrong spec basis, wrong execution profile, or materially invalid assumption:
  - do not keep the earlier pass implied as valid
  - mark the run or continuity notes so the earlier pass is explicitly invalidated or replaced
  - preserve the correction path clearly enough that later readers can see why the current truth changed
- Normal project work should prefer explicit attempt history over rewriting the same pass invisibly.

## Compact Mental Model
- `implementation bug`:
  - fix here
- `spec gap`:
  - report, then human may send back to spec
- `planning gap`:
  - report, then human may send back to feature or PRD
- after correction:
  - start a new run from the corrected layer

## Termination Conditions
- The loop may end with:
  - `passed`
  - `blocked`
  - `returned-to-spec`
  - `returned-to-planning`
