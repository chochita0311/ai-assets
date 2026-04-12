# Execution Loop Governance

## Purpose
- Define how approved features move through spec, build, evaluation, fix, and escalation.
- Keep execution loops traceable, bounded, and type-aware.

## Ownership
- This document owns execution-loop rules.
- In a consuming repo, use `docs/agents/flow/workflow.md` for sequence examples.
- In a consuming repo, use `docs/policies/harness/prd-feature-management.md` for planning-layer rules and approval criteria.

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
- Every execution artifact must reference the active feature ID and active spec ID.
- If a blocker belongs to planning or spec, route upward instead of normalizing it as an implementation defect.

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
  - Functional Evaluator
  - Fix Agent
  - re-evaluate
- `product` feature default loop:
  - Spec Agent
  - Builder
  - Design Evaluator when visual surfaces matter
  - Functional Evaluator
  - UX Heuristic Evaluator as side-channel
  - Fix Agent
  - re-evaluate

## Fail Classification
Every blocking finding should be classified as one of:

- `implementation bug`
  - the approved spec is clear and the code does not satisfy it
- `spec gap`
  - the feature is approved, but the active spec is too weak or contradictory to execute safely
- `planning gap`
  - the issue changes approved scope, unresolved dependency meaning, or product-boundary intent

## Classification Examples
- `implementation bug`
  - tags or titles spill outside an approved card even though the spec already requires stable containment
  - an approved content surface no longer opens its detail path even though the spec preserves click-through
  - pagination or other existing controls stop working because a rerender replaced interactive nodes without preserving or rebinding their interaction handlers
- `spec gap`
  - the feature clearly needs stable card containment, but the spec failed to define title clamp, tag overflow, or breakpoint behavior
  - the visual direction is approved, but the build has no precise rule for how summaries should compress inside the new card
  - the feature changes a rerender path, but the spec never defined whether the affected controls must survive interactive-surface replacement or be rebound after rebuild
- `planning gap`
  - execution reveals that the approved feature boundary was wrong, such as “replace the current surface” when the real intended scope was “keep the current surface and add a mode toggle”
  - execution reveals a missing user-visible mode or scope decision that should have been resolved before spec

## Return Path
- `implementation bug`:
  - continue normal build or fix loop
- `spec gap`:
  - stop normal fix work
  - return to spec review
- `planning gap`:
  - stop normal execution
  - return to feature or PRD review

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
- If a heuristic failure implies new scope, return to spec or planning instead of fixing ad hoc.

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

## Traceability Rules
- Use one run identifier such as `run-YYYYMMDD-01` for each active execution pass.
- Use one spec document per active feature loop.
- A run may include multiple attempts when execution loops, fails, or returns upward.
- Record attempt boundaries in the run document when one pass is invalidated, returned to planning, returned to spec, or retried after a blocking issue.
- Use evaluator reports that name:
  - run ID
  - attempt number when relevant
  - feature ID
  - spec ID
  - evaluator type
  - pass/fail result
  - fail classification when blocked
- Use fix logs that reference the evaluator reports they addressed.
- Use fix logs that also reference the active run ID.
- Use fix logs that reference the active attempt when the same run has multiple passes.
- Use heuristic backlog entries for non-blocking suggestion accumulation.

## Invalidation Rule
- If later evidence proves that an earlier execution pass was based on a wrong feature boundary, wrong spec basis, or materially invalid assumption:
  - do not keep the earlier pass implied as valid
  - mark the run or continuity notes so the earlier pass is explicitly invalidated or replaced
  - preserve the correction path clearly enough that later readers can see why the current truth changed
- Normal project work should prefer explicit attempt history over rewriting the same pass invisibly.

## Termination Conditions
- The loop may end with:
  - `passed`
  - `blocked`
  - `returned-to-spec`
  - `returned-to-planning`
