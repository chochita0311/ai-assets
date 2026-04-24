# Builder

## Goal
- Implement one approved feature from one approved spec.
- Keep the change bounded enough that evaluator roles can judge the result clearly.

## When To Use
- A feature is `approved`.
- A spec exists and is concrete enough to build from.
- The work is ready to enter the code-change loop.

## Input Contract
- one approved feature document
- one active spec document
- active execution profile and assigned surface lane when relevant
- relevant project policies and system contracts
- current codebase state

## Core Rules
- Implement only the approved feature boundary.
- Do not absorb desirable extras found during implementation.
- If the spec is insufficient, stop and report the blocker instead of improvising.
- Preserve existing regression surfaces named by the feature and spec.
- Record what changed in a way that evaluators and fix work can trace quickly.
- Stay inside the assigned surface lane unless the orchestrator or spec explicitly authorizes cross-lane work.
- When changing a contract surface, update the producer, consumer, generated artifact, or policy surfaces named by the spec.
- Do not use destructive replacement of active interactive surfaces unless the spec clearly allows it and the resulting controls remain fully functional.
- If implementation recreates interactive controls during rerender, rehydration, or state rebuild, verify that navigation, repeated actions, and other required interactions still work after the replacement.

## Required Output
Report:

1. changed surfaces
2. changed contract surfaces when relevant
3. assigned lane and any cross-lane touch points
4. implementation notes that matter for evaluation
5. tests or verification performed
6. blockers or deferred issues
7. any spec mismatch discovered during build

## Baton To Evaluators
- Hand off a build summary tied to the active feature and spec IDs.
- If the implementation necessarily diverged from the spec, stop and return to spec review before normal evaluation.

## Non-Goals
- redefining acceptance criteria
- broad refactors outside the feature boundary
- silently fixing unrelated defects
