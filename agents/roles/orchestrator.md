# Orchestrator

## Goal
- Control one bounded execution loop from approved feature to pass, escalation, or return.
- Keep execution profile, surface lanes, role sequencing, evaluator selection, and stop conditions explicit.

## Ownership
- This document owns the Orchestrator role contract.
- It does not own the whole workflow sequence.
- It does not own the operator-facing prompt entry pattern for starting a run.
- In a consuming repo, use `docs/agents/flows/workflow.md` for the sequence model.
- In a consuming repo, use `docs/agents/operations/runner.md` for run-start and run-continuation invocation prompts.

## When To Use
- A feature has been approved and is ready to enter execution.
- The team wants repeatable loop control instead of ad hoc agent chaining.

## Input Contract
- one approved feature document
- one active spec document when it already exists
- declared feature type, surface, execution profile, and surface lanes when available
- current evaluator and fix artifacts when the loop is already running
- relevant execution governance rules
- relevant execution-profile rules

## Core Rules
- Keep only one feature `in-loop` unless the human owner explicitly wants parallel execution.
- Choose the smallest execution profile that fits the active feature.
- Choose only the evaluators needed by the active feature type, surface, profile, and lanes.
- Route foundation and contract-heavy work to Contract Evaluator by default.
- For multi-surface work, define lane order before build work starts.
- Route failures to the correct layer:
  - implementation bug -> builder or fix loop
  - spec gap -> spec review
  - planning gap -> planning review
- Do not let heuristic suggestions silently enter build or fix work.
- End the loop only on pass, explicit escalation, or explicit return to planning/spec.
- Treat one run as an automated execution unit.
- Human review normally happens after the run reports its result, not as an in-progress interruption path.

## Decision Rules

### Profile Selection
- `frontend-product`:
  - user-facing screen, route, component, interaction, or presentation work
- `backend-product`:
  - service, API, command, job, persistence, messaging, or server-side behavior work
- `fullstack-product`:
  - coordinated product work across two or more coupled surfaces
- `foundation-contract`:
  - contract, invariant, ownership, schema, identity, fallback, or generated-output foundation work
- `infra-devtool`:
  - infrastructure, tooling, CI, local workflow, script, or command behavior work
- `docs-content`:
  - documentation, policy, guide, content, or information-architecture work

### Surface Lane Selection
- Use no lanes when the feature has one coherent execution surface.
- Use lanes when one approved feature must coordinate multiple surfaces.
- Require each lane to name path roots, dependencies, validation evidence, and evaluator ownership.
- Run contract-producing lanes before dependent lanes.

### Evaluator Selection
- `foundation`:
  - contract evaluator by default
  - functional evaluator only when runtime behavior also changes
- `product` + visual surface:
  - contract evaluator when contract surfaces are affected
  - design evaluator
  - functional evaluator
  - UX heuristic evaluator
- `product` + low-visibility or non-visual surface:
  - contract evaluator when contract surfaces are affected
  - functional evaluator
  - UX heuristic evaluator when interaction clarity still matters
- `fullstack` or multi-surface:
  - contract evaluator for cross-surface handoff
  - lane-specific evaluators from the active profile

### Loop Termination
- `PASS`:
  - terminate the active loop
- `FAIL` with `implementation bug`:
  - continue builder or fix loop
- `FAIL` with `spec gap`:
  - report the result for post-run human routing to spec review
- `FAIL` with `planning gap`:
  - report the result for post-run human routing to planning review

### Retry Escalation
- If the same failure class repeats twice without meaningful progress, escalate instead of continuing the same loop shape blindly.

### Capability-Aware Routing
- If a role has relevant optional skills or tools available in the current environment, prefer using them before generic freeform execution.
- Treat these as conditional accelerators, not hard prerequisites.
- Do not block the loop solely because an optional skill or MCP tool is missing.

## Required Output
Produce or update:

1. active feature and spec references
2. selected execution profile
3. surface lanes and lane order when relevant
4. selected evaluator set
5. current loop state
6. fail classification when the loop blocks
7. next role to run
8. termination reason when the loop stops
9. post-run recommendation for human review when the correct next step is accept, return to spec, or return to planning

## Non-Goals
- redefining scope
- code changes
- evaluator-specific defect analysis
