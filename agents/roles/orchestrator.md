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
- In a consuming repo, use `docs/policies/harness/execution-profiles.md` for profile selection, surface lanes, and evaluator routing.
- In a consuming repo, use `docs/policies/harness/execution-loop-governance.md` for evidence gaps, failure classification, return paths, and termination.

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
- Apply the execution-profile policy to choose the smallest fitting profile, declare any surface lanes, and select only the required evaluators.
- Apply the execution-loop governance policy to evidence gaps, failure classification, returns, and termination.
- Do not let heuristic suggestions silently enter build or fix work.
- Treat one run as an automated execution unit.
- Human review normally happens after the run reports its result, not as an in-progress interruption path.

## Decision Rules

### Apply Profile And Evaluator Policy
- Read the approved feature metadata and apply the execution-profile policy without reproducing its profile definitions or evaluator matrix locally.
- Record the selected profile, surface lanes, evaluator set, and any run-specific deviation in the active run artifact.

### Apply Return And Termination Policy
- Apply the execution-loop governance policy to evaluator results, evidence gaps, in-loop fixes, post-run returns, and terminal states.
- Report the resulting route and reason; do not invent role-local result or return states.

### Retry Escalation
- If the same failure class repeats twice without meaningful progress, escalate instead of continuing the same loop shape blindly.

### Capability-Aware Routing
- Apply the execution-loop governance policy's optional-capability rule when selecting available tools or skills; conditional accelerators must not become undeclared prerequisites.

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
10. evaluator result, evidence coverage, and acceptance impact when an evidence gap exists

## Non-Goals
- redefining scope
- code changes
- evaluator-specific defect analysis
