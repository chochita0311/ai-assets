# Frontend Product Profile

## Purpose
- Guide user-facing screen, component, route, interaction, and presentation work.
- Keep visual, interaction, and runtime checks explicit without making frontend assumptions global.

## Default Role Sequence
1. Orchestrator
2. Spec Agent
3. Builder
4. Contract Evaluator when route, generated type, API, prop, or data assumptions change
5. Design Evaluator when visual output matters
6. Functional Evaluator
7. UX Heuristic Evaluator as side-channel when interaction quality matters
8. Fix Agent when implementation defects are confirmed

## Required Inputs
- approved feature and parent PRD
- relevant design source, design constitution, or visual policy when present
- affected routes, screens, components, state surfaces, and browser behaviors
- active spec with interaction, state, and regression expectations

## Required Evidence
- runtime behavior evidence from a browser, test, or deterministic local check
- responsive or viewport evidence when layout is affected
- interaction-continuity evidence when controls, navigation, or rerender behavior changes
- contract evidence when the feature depends on routes, generated types, API assumptions, or component prop boundaries

## Default Evaluators
- `design` when visible layout or presentation changes
- `functional` for behavior, state, navigation, and regression checks
- `ux-heuristic` for non-blocking friction and clarity findings
- `contract` when the feature changes route contracts, generated client types, component props, API assumptions, or data shape

## Split Triggers
- The feature introduces a new data, API, route, or generated-type dependency that is not already stable.
- Visual work and data-contract work can pass independently and should not block each other in one loop.
- Evaluation failures cluster into separate surfaces such as route contract, component rendering, and interaction behavior.
