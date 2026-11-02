# Fullstack Product Profile

## Purpose
- Guide product work that spans two or more coupled surfaces.
- Make cross-surface contracts explicit before frontend, backend, integration, or generated-artifact lanes drift.

## Default Role Sequence
1. Orchestrator
2. Spec Agent
3. Builder for the contract or first producer lane when a boundary must be established
4. Contract Evaluator before dependent lanes are accepted
5. Builder for dependent lanes when the contract is stable
6. Design Evaluator when visible output changes
7. Functional Evaluator
8. UX Heuristic Evaluator as side-channel when interaction quality matters
9. Fix Agent when implementation defects are confirmed

## Surface Lanes
Declare only the lanes needed by the feature:
- `contract`
- `frontend`
- `backend`
- `integration`
- `data`
- `infra`
- `docs`

Each lane should declare:
- path roots
- owning role
- dependencies
- validation command or evidence
- evaluator ownership

## Required Inputs
- approved feature and parent PRD
- active spec with lane order and cross-surface contract
- producer and consumer expectations
- relevant local policies for each lane

## Required Evidence
- contract evidence before dependent lanes are accepted
- lane-specific build or implementation evidence
- integration evidence across the declared lane boundary
- regression evidence for existing consumers and user-visible surfaces

## Default Evaluators
- `contract` for cross-surface handoff
- `functional` for end-to-end behavior
- `design` and `ux-heuristic` only when visible or interaction surfaces are in scope

## Split Triggers
- The contract lane is unresolved.
- One lane can be completed and evaluated independently while another remains ambiguous.
- Different lanes require separate approval or validation gates.
