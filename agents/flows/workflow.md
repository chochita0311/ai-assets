# Agent Workflow

## Purpose
- Define the baton flow for bounded, repeatable product work.
- Keep creative scope decisions separate from implementation loops.

## Ownership
- This document owns sequence.
- Use it to understand the order of operations, stop points, and handoff moments between planning and execution.
- It does not own the structural contract for PRDs or features.
- It does not own the operator-facing run-start prompts.
- In a consuming repo, use `docs/policies/harness/prd-feature-management.md` for required document content, approval criteria, traceability rules, allowed ambiguity, and change control.
- In a consuming repo, use `docs/policies/harness/execution-loop-governance.md` for fail classification, execution routing, heuristic handling, and execution-artifact ownership.
- In a consuming repo, use `docs/policies/harness/execution-profiles.md` for profile selection, surface lanes, and evaluator routing.
- In a consuming repo, use `docs/agents/operations/runner.md` when you need to actually start or continue one run through prompts.

## Workflow Assembly
- Workflows are composable, not universal.
- A project may use only the roles and steps it actually needs.
- Some projects may stop at planning roles, while others may extend into spec, build, evaluator, and fixer loops.
- Monorepo or multi-surface systems may require additional lanes, gates, or parallel branches beyond the default sequence shown here.
- The flow below is a strong general-purpose example, not a mandatory full pipeline for every repo.
- Keep role contracts stable and vary profiles, sequence, gates, lanes, or evaluator mix as the project grows.

## Step-By-Step Flow
1. Human request
   - Provide the request, golden sources, and any strong constraints.
2. `PRD Normalizer`
   - Normalize the raw input into a bounded PRD draft.
3. Write or update a PRD in `docs/plans/prd/`
   - Record confirmed scope, exclusions, uncertainty, and constraints.
4. Human PRD review
   - Stop here.
   - Ask and answer questions.
   - Correct scope, exclusions, and ambiguity until the boundary is acceptable.
   - Some bounded open items may remain if they are recorded and do not block safe feature planning.
   - If uncertainty would materially change scope or feature direction, ask the human owner directly before approval.
5. PRD approval
   - Mark the PRD `approved` only after the boundary is accepted.
6. `Feature Planner`
   - Decompose the approved PRD into loop-sized proposed features.
7. Write proposed feature docs in `docs/plans/feature/`
   - One feature document per proposed loop unit.
8. Human feature-boundary review
   - Stop here.
   - Split, merge, reorder, defer, or reject features until the boundaries are acceptable.
   - Remove ambiguity until the chosen feature is concrete enough for spec handoff.
   - If material uncertainty remains, ask the human owner directly before approval.
9. Feature approval
   - Mark only the chosen execution target as `approved`.
10. `Orchestrator`
   - Select the active feature, active spec target, execution profile, surface lanes, and evaluator set.
11. `Spec Agent`
   - Write or update one implementation-facing spec in `docs/plans/spec/`.
12. `Builder`
   - Implement only the approved feature boundary from the active spec.
13. `Contract Evaluator`
   - Check contract, schema, generated-output, route, command, source-of-truth, or integration boundaries when they matter.
14. `Design Evaluator`
   - Check source and design-surface fidelity when the feature is visually sensitive.
15. `Functional Evaluator`
   - Check behavior, state handling, transitions, and regressions.
16. `UX Heuristic Evaluator`
   - Emit blocking UX failures or non-blocking suggestions.
17. `Fix Agent`
   - Fix only the approved feature defects surfaced by evaluators.
18. Re-evaluate
   - Repeat the needed evaluator and fix steps until pass or until the work must return to planning or spec review.
19. Post-run human review
   - After the automated run reports its result, the human owner decides whether to accept, return to spec, or return to planning.
   - Start a new run from the corrected layer instead of treating that return as an in-progress interruption to the earlier run.

## Operator Briefing Hooks

The workflow may expose user-facing continuity without adding a workflow phase.

- On orientation requests, explain the active destination, current position, available next work, and material blockers.
- After canonical target resolution and before work begins, emit one target-specific Work Briefing when prior context materially affects understanding or execution.
- During work, emit a Direction Alert only when direction, scope, evidence, safety, authority, or review obligations materially change.
- At completion, planning return, block, handoff, or approval boundary, emit a Review Receipt only when the operator has a meaningful delta to understand.
- Apply [Operator Briefing And Review Receipts](../policies/harness/operator-briefing-and-review-receipts.md); these hooks do not change workflow routing or state transitions.

## Role Boundaries
- Human:
  - sets product direction
  - supplies or approves golden sources
  - approves feature boundaries before implementation loops begin
- PRD Normalizer:
  - organizes source material into bounded scope
  - separates confirmed, excluded, and uncertain items
- Feature Planner:
  - proposes loop-sized feature units and dependency order
  - does not own final scope decisions
- Orchestrator:
  - controls the active loop, execution profile, lane order, and evaluator set
  - routes failures to fix, spec review, or planning review
- Spec Agent:
  - translates one approved feature into implementation-ready execution detail
  - does not redefine the feature boundary
- Builder:
  - implements one approved spec
  - does not add adjacent scope opportunistically
- Contract Evaluator:
  - checks APIs, schemas, messages, generated outputs, source-of-truth ownership, and integration boundaries
- Design Evaluator:
  - checks visual fidelity, responsive behavior, and presentation regressions
- Functional Evaluator:
  - checks behavior, state transitions, error paths, and regressions
- UX Heuristic Evaluator:
  - checks clarity and friction within the approved feature boundary
  - defaults to side-channel suggestions unless the issue is severely blocking
- Fix Agent:
  - applies targeted corrections from evaluator findings
  - returns to planning or spec review when findings expose boundary or contract problems

## Approval Rule
- Planning output is not executable truth until a human locks the boundary.
- PRD and feature planning should pause at their review steps instead of flowing forward automatically.
- PRDs may carry explicitly recorded open items when they do not block safe feature planning.
- Approved features must be concrete enough for the spec agent to proceed without guesswork.
- If material ambiguity remains during planning and would block safe feature planning or spec handoff, stop and ask the human owner instead of carrying the ambiguity forward.
- If a later evaluator detects a likely missing behavior, it may suggest it, but that behavior must return to spec approval before implementation.
- Use the consuming repo's planning-governance policy as the operating rule for where PRDs and features live and how they change.
- Use `docs/plans/spec/` for implementation-facing specs tied to one approved feature.
- Use the consuming repo's execution-loop governance policy for execution-layer fail classification and return paths.

## Reusable Prompt Frame
Use this framing when invoking the early planning roles:

```text
Input:
- human request
- one or more golden sources
- supporting docs or implementation context if available

Process:
1. Run PRD Normalizer to stabilize scope.
2. Stop for PRD review and resolve uncertainty.
3. Record bounded open items if they do not block safe feature planning.
4. If uncertainty would block safe feature planning, ask the human owner before approval.
5. Run Feature Planner on the approved PRD only.
6. Stop for feature-boundary review and lock the chosen feature.
7. If uncertainty is still material, ask the human owner before approval.
8. Hand the locked feature to Spec Agent, Builder, evaluator roles, and Fix Agent as needed.
```

## Execution Loop Guidance
- `Orchestrator` should keep only one feature in active loop unless the human owner explicitly opts into parallel execution.
- Select the execution profile, surface lanes, and evaluator set through the consuming repo's execution-profile policy; this flow does not redefine that matrix.
- `Spec Agent` is the first execution role and should create one spec per active feature.
- `Builder` should work from the active spec, not directly from rough feature prose.
- `Fix Agent` should consume findings from the active evaluator set and preserve the same feature boundary.
- Classify evidence gaps, failures, and return paths through the consuming repo's execution-loop governance policy instead of restating those rules here.
- Apply the execution-loop governance policy's post-contract regression check before closing a run when its stated boundary applies.

## Example Variations
- Planning-only:
  - Human -> PRD Normalizer -> PRD review -> Feature Planner -> feature review
- Standard single-surface loop:
  - Human -> PRD Normalizer -> Feature Planner -> Orchestrator -> Spec Agent -> Builder -> Functional Evaluator -> Fix Agent
- UI-heavy loop:
  - Human -> PRD Normalizer -> Feature Planner -> Orchestrator -> Spec Agent -> Builder -> Design Evaluator -> Functional Evaluator -> UX Heuristic Evaluator -> Fix Agent
- Foundation contract loop:
  - Human -> PRD Normalizer -> Feature Planner -> Orchestrator -> Spec Agent -> Builder or contract updater -> Contract Evaluator -> Fix Agent
- Multi-surface product loop:
  - Human -> PRD Normalizer -> Feature Planner -> Orchestrator -> Spec Agent -> ordered or parallel surface lanes -> Contract Evaluator -> needed evaluator set -> Fix Agent

## Design Note
- A single golden screen can be enough to bootstrap later work if it yields a stable design grammar.
- If later features introduce patterns that the sources do not cover, treat them as uncertainty and request more source material instead of improvising.
