# Execution Profiles

## Purpose
- Define how execution profiles are selected, recorded, and applied during harness runs.
- Keep roles stable while allowing different project shapes to use different loop presets.
- Support frontend, backend, fullstack, infrastructure, documentation, and other consuming repos without creating parallel agent systems.

## Ownership
- This document owns profile-selection rules.
- The installed profiles package owns profile descriptions.
- The Orchestrator role contract owns the role behavior for applying a selected profile to one run.
- The execution-loop governance policy owns fail classification, return paths, and run lifecycle.

## Core Model
- A role is a stable lifecycle responsibility.
- A profile is a reusable loop preset.
- A surface is a coherent work area such as UI, service, data, infrastructure, docs, generated artifact, or integration boundary.
- A lane is a declared execution slice inside one feature when multiple surfaces must be coordinated.

## Feature Metadata
Every approved feature should identify:
- `Type`: `product` or `foundation`
- `Surface`: `frontend`, `backend`, `fullstack`, `data`, `infra`, `docs`, `mixed`, or a project-local equivalent
- `Execution Profile`: one profile from the installed profiles package
- `Surface Lanes`: only when the feature spans multiple surfaces
- `Required Evaluators`: evaluator roles expected for the run
- `Contract Surfaces`: APIs, schemas, events, generated outputs, routes, commands, config, docs ownership, or other boundaries that must be checked

## Profile Selection
- Choose the smallest profile that can evaluate the approved feature without guessing.
- Use `foundation-contract` when the primary outcome is a contract, invariant, ownership boundary, fallback rule, identity model, or generated-output shape.
- Use `fullstack-product` only when one feature must coordinate multiple coupled surfaces.
- Use a surface-specific product profile when the work can be evaluated within one primary surface.
- If no existing profile fits, use the closest profile and record the local specialization in the consuming repo's policy layer.

## Surface Lane Rules
- Declare surface lanes only when one approved feature must coordinate multiple surfaces.
- Each lane must state:
  - path roots or artifact roots
  - lane dependency order
  - owning role
  - required evidence or validation command
  - evaluator ownership
- If one lane defines a contract consumed by another, run the contract lane first.
- If lanes can proceed independently, the human owner may allow parallel execution.
- If lane failures cluster into different contracts, split the feature.

## Evaluator Routing
- `contract` evaluates schemas, payloads, generated outputs, source-of-truth ownership, route contracts, command contracts, and integration boundaries.
- `functional` evaluates runtime behavior, state transitions, workflows, command behavior, error handling, and regressions.
- `design` evaluates visual fidelity and layout behavior when visible surfaces are in scope.
- `ux-heuristic` emits interaction, clarity, and friction signals within the approved boundary.

## Default Evaluator Matrix
- `frontend-product`:
  - `design` when visible output changes
  - `functional`
  - `ux-heuristic` when interaction quality matters
  - `contract` when route, prop, generated type, API, or data assumptions change
- `backend-product`:
  - `contract`
  - `functional` when runtime behavior changes
- `fullstack-product`:
  - `contract`
  - `functional`
  - `design` and `ux-heuristic` when visible or interaction surfaces are in scope
- `foundation-contract`:
  - `contract`
  - `functional` only when runtime behavior also changes
- `infra-devtool`:
  - `functional`
  - `contract` when commands, config, artifacts, CI output, or environment assumptions change
- `docs-content`:
  - `contract` when ownership, policy, or source-of-truth routing changes
  - `functional` when generated docs, links, commands, or published output must be checked

## Split And Escalation Rules
- Split a product feature when it absorbs unresolved foundation work.
- Split a multi-surface feature when one lane can become a stable prerequisite for later lanes.
- Return to planning when the selected profile exposes a wrong feature boundary.
- Return to spec when the feature boundary is right but the active spec does not define the profile, lanes, contracts, or evaluation evidence clearly enough.

## Non-Goals
- replacing role contracts
- defining framework-specific implementation rules
- making every feature multi-surface
- requiring all evaluators for every run
