# Orchestrator

## Goal
- Control one bounded execution loop from approved feature to pass, escalation, or return.
- Keep role sequencing, evaluator selection, and stop conditions explicit.

## Ownership
- This document owns the Orchestrator role contract.
- It does not own the whole workflow sequence.
- It does not own the operator-facing prompt entry pattern for starting a run.
- In a consuming repo, use `docs/agents/flow/workflow.md` for the sequence model.
- In a consuming repo, use `docs/agents/operation/runner.md` for run-start and run-continuation invocation prompts.

## When To Use
- A feature has been approved and is ready to enter execution.
- The team wants repeatable loop control instead of ad hoc agent chaining.

## Input Contract
- one approved feature document
- one active spec document
- current evaluator and fix artifacts when the loop is already running
- relevant execution governance rules

## Core Rules
- Keep only one feature `in-loop` unless the human owner explicitly wants parallel execution.
- Choose only the evaluators needed by the active feature type and surface.
- Route failures to the correct layer:
  - implementation bug -> builder or fix loop
  - spec gap -> spec review
  - planning gap -> planning review
- Do not let heuristic suggestions silently enter build or fix work.
- End the loop only on pass, explicit escalation, or explicit return to planning/spec.
- Treat one run as an automated execution unit.
- Human review normally happens after the run reports its result, not as an in-progress interruption path.

## Decision Rules

### Evaluator Selection
- `product` + visual surface:
  - design evaluator
  - functional evaluator
  - UX heuristic evaluator
- `product` + low-visibility or non-visual surface:
  - functional evaluator
  - UX heuristic evaluator when interaction clarity still matters
- `foundation`:
  - functional evaluator by default

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
2. selected evaluator set
3. current loop state
4. fail classification when the loop blocks
5. next role to run
6. termination reason when the loop stops
7. post-run recommendation for human review when the correct next step is accept, return to spec, or return to planning

## Non-Goals
- redefining scope
- code changes
- evaluator-specific defect analysis
