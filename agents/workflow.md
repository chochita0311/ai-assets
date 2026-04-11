# Agent Workflow

## Purpose
- Define the baton flow for bounded, repeatable product work.
- Keep creative scope decisions separate from implementation loops.

## Ownership
- This document owns sequence.
- Use it to understand the order of operations, stop points, and handoff moments between planning and execution.
- It does not own the structural contract for PRDs or features.
- Use `docs/policies/prd-feature-management.md` for required document content, approval criteria, traceability rules, allowed ambiguity, and change control.

## Workflow Assembly
- Workflows are composable, not universal.
- A project may use only the roles and steps it actually needs.
- Some projects may stop at planning roles, while others may extend into spec, build, evaluator, and fixer loops.
- Monorepo or multi-surface systems such as FE/BE stacks may require additional roles, gates, or parallel branches beyond the default sequence shown here.
- The flow below is a strong general-purpose example, not a mandatory full pipeline for every repo.

## Step-By-Step Flow
1. Human request
   - Provide the request, golden sources, and any strong constraints.
2. `PRD Normalizer`
   - Normalize the raw input into a bounded PRD draft.
3. Write or update a PRD in `<consumer-repo>/docs/plans/prd/`
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
7. Write proposed feature docs in `<consumer-repo>/docs/plans/feature/`
   - One feature document per proposed loop unit.
8. Human feature-boundary review
   - Stop here.
   - Split, merge, reorder, defer, or reject features until the boundaries are acceptable.
   - Remove ambiguity until the chosen feature is concrete enough for spec handoff.
   - If material uncertainty remains, ask the human owner directly before approval.
9. Feature approval
   - Mark only the chosen execution target as `approved`.
10. Spec generation
   - Generate implementation-facing spec only from an approved feature.
11. Build
   - Implement only the approved feature boundary.
12. Evaluate
   - Check the implementation against the feature boundary and regression surfaces.
13. Fix
   - Fix only the approved feature defects.
14. Re-evaluate
   - Repeat evaluate and fix until pass or until the work must return to planning.

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

## Approval Rule
- Planning output is not executable truth until a human locks the boundary.
- PRD and feature planning should pause at their review steps instead of flowing forward automatically.
- PRDs may carry explicitly recorded open items when they do not block safe feature planning.
- Approved features must be concrete enough for the spec agent to proceed without guesswork.
- If material ambiguity remains during planning and would block safe feature planning or spec handoff, stop and ask the human owner instead of carrying the ambiguity forward.
- If a later evaluator detects a likely missing behavior, it may suggest it, but that behavior must return to spec approval before implementation.
- Use `docs/policies/prd-feature-management.md` as the operating rule for where PRDs and features live and how they change.

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
8. Hand the locked feature to spec and implementation roles.
```

## Design Note
- A single golden screen can be enough to bootstrap later work if it yields a stable design grammar.
- If later features introduce patterns that the sources do not cover, treat them as uncertainty and request more source material instead of improvising.
