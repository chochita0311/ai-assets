# PRD And Feature Management

## Purpose
- Define how PRDs and feature plans are created, approved, updated, and traced during harness-driven work.
- Keep planning artifacts strict enough that later spec, build, evaluator, and fix loops can reference them without guesswork.
- Separate product-boundary decisions from per-feature implementation loops.

## Ownership
- This document owns the lifecycle, required content, approval gates, and change control rules for PRD and feature artifacts.
- Use it to understand what PRDs and features are, what they must contain, what may remain open, and what must be clear before approval.
- It does not own the full step-by-step baton sequence, execution-profile routing, execution return model, or portable link rules.
- In a consuming repo, use `docs/agents/flows/workflow.md` for the ordered flow, pause points, and handoff timing between planning and execution.
- In a consuming repo, use `docs/policies/harness/execution-profiles.md` for surfaces, lanes, profiles, and evaluator routing.
- In a consuming repo, use `docs/policies/harness/execution-loop-governance.md` for execution return paths.
- In a consuming repo, use `docs/policies/harness/traceability-and-link-hygiene.md` for portable links and source/generated artifact reference rules.

## Planning Layers
- In a consuming repo, `docs/plans/prd/` owns bounded PRD documents.
- In a consuming repo, `docs/plans/feature/` owns loop-sized feature documents derived from approved PRDs.
- In a consuming repo, `docs/plans/spec/` owns implementation-facing specs derived from approved features.
- In a consuming repo, `docs/policies/` continues to own durable project rules and contracts.

## Core Model
- A `PRD` is the upper planning boundary for one coherent product increment.
- A `Feature` is the execution unit for one harness loop target.
- A harness run should always be traceable back to exactly one feature plan.
- Every feature plan should trace back to exactly one parent PRD.

## Feature Types

Not every feature serves the same role in the harness workflow.

### Product Feature
- Purpose:
  - deliver a user-visible outcome
- Requirement:
  - must define clear user-visible behavior
  - must be evaluable through interaction, presentation, or user-observable state
- Examples:
  - authentication entry screen
  - display mode toggle

### Foundation Feature
- Purpose:
  - remove downstream ambiguity by fixing a contract, invariant, or ownership boundary
- Requirement:
  - must not rely on vague prep-work framing
  - must resolve one concrete contract or system-level ambiguity that later features depend on
- Allowed outcomes:
  - data ownership fixed
  - value shape fixed
  - fallback rule fixed
  - state model fixed
- Examples:
  - media metadata contract
  - session schema normalization

## Why This Split Exists
- PRDs define direction, scope, exclusions, and acceptance envelope.
- Feature plans define loop-sized implementation targets, dependencies, and pass or fail checks.
- Scope changes belong in the PRD layer, not inside evaluator feedback or implementation notes.

## Planning Gate Summary
- PRD drafting starts from the human request, golden sources, and relevant existing docs.
- PRD review must stop until confirmed scope, exclusions, uncertainty, constraints, and acceptance envelope are acceptable.
- Feature planning starts only from an approved PRD.
- Feature review must stop until the chosen feature boundary, dependencies, execution profile, surface, and pass/fail checks are concrete enough for spec handoff.
- Execution starts only from one approved feature at a time unless the human owner explicitly approves parallel execution.

## PRD Rules
- Create a new PRD when the requested increment introduces a new upper scope boundary.
- Update an existing PRD when the request is still part of the same bounded increment.
- Human intervention is expected and desirable while a PRD is still `draft`.
- A `draft` PRD may be questioned, narrowed, expanded, corrected, or restructured before approval.
- A PRD may retain bounded open questions or uncertainty as long as they are explicitly recorded and do not make the upper scope boundary unusable.
- Ask the human owner direct clarification questions when unresolved PRD ambiguity would materially change the upper scope boundary, exclusions, or candidate feature direction.
- Do not treat PRD output as executable truth until the human owner accepts the boundary.
- A PRD must explicitly define:
  - request summary
  - source set
  - confirmed scope
  - excluded scope
  - uncertainty
  - constraints
  - acceptance envelope
  - proposed feature candidates
- A PRD must not contain implementation steps, code tasks, or evaluator reports.

## PRD Open Item Versus Foundation Feature

- Keep an item in the PRD when it is still an open question or unresolved planning ambiguity.
- Create a foundation feature when the intended direction is chosen and now needs a bounded, traceable contract artifact.
- Move the rule into the consuming repo's `docs/policies/` instead when it becomes a durable repo-wide rule rather than a request-local planning outcome.

## Feature Rules
- Create one feature document for each loop-sized unit approved from a PRD.
- Human intervention is expected and desirable while feature boundaries are still being proposed.
- Proposed features may be split, merged, reordered, deferred, or rejected before approval.
- Every feature should declare a `Type` of `product` or `foundation`.
- Every feature should declare a `Surface` and `Execution Profile` before spec handoff.
- Multi-surface features should declare explicit `Surface Lanes`.
- A foundation feature must produce one concrete contract or invariant, not a vague preparation step.
- Foundation and product outcomes must be tracked in separate feature documents when the foundation outcome is a prerequisite contract.
- A product feature should not absorb unresolved contract questions that belong in a foundation feature.
- A product feature must not absorb required foundation implementation even when that foundation is only needed for one immediate downstream product feature.
- An approved feature must be concrete enough to hand off to the spec agent without guesswork about scope, dependencies, user-visible outcome, data ownership, interaction behavior, or pass/fail checks.
- If unclear, open, or weakly supported points remain in a feature boundary, ask the human owner direct clarification questions until the execution target is clear enough to approve.
- Do not start spec or implementation work from a feature document that has not been boundary-locked.
- A product feature must have one clear user-visible outcome.
- A foundation feature must have one clear system-level contract outcome.
- A feature must be small enough to converge in one to three build or fix loops in normal cases.
- A feature must explicitly define:
  - parent PRD
  - type, surface, and execution profile
  - surface lanes when relevant
  - scope boundary
  - dependencies
  - contract surfaces when relevant
  - pass or fail checks
  - regression surfaces
  - harness-trace fields
- A feature must not silently absorb missing scope discovered later.

## Status Model
Use these statuses for PRD and feature documents:

- `draft`: being prepared and not yet approved for downstream use
- `approved`: boundary accepted and ready for downstream planning or execution
- `in-loop`: currently being used by spec, build, evaluate, or fix work
- `blocked`: cannot proceed because of an unresolved dependency or decision
- `passed`: execution target satisfied and accepted
- `superseded`: replaced by a newer document or narrower split

## Change Control
- If evaluator output reveals a missing but desirable behavior:
  - do not silently implement it
  - decide whether it belongs in the parent PRD or the current feature
  - update the planning document first
- If a PRD or feature changes materially enough that its current filename becomes misleading:
  - rename the file when the ID should remain the same and the boundary is still the same planning object
  - create a new PRD or feature and mark the old one `superseded` when the boundary itself has changed into a different planning object
  - do not leave an active planning artifact with a semantically false filename
- If a feature grows beyond a stable loop size:
  - split it into new feature documents
  - mark the old feature as `superseded`
- If a change alters the upper scope boundary:
  - update the PRD first
  - then re-check linked feature documents

## Human Review Rights
- The human owner may interrupt and revise planning output at any time before PRD approval.
- The human owner may interrupt and revise feature boundaries at any time before feature approval.
- Questions, objections, and clarifications should be resolved in the planning layer instead of being pushed into spec or implementation.
- After approval, scope changes must return to the planning layer instead of being absorbed ad hoc during execution.

## Clarification Rule
- A PRD may be approved with explicitly recorded open items when those items do not block safe feature planning.
- Do not approve a feature boundary while material ambiguity remains.
- If the next planning or execution step depends on an unclear point, stop and ask the human owner.
- Prefer a short direct question over silent assumption when the ambiguity could change scope, dependency order, data ownership, interaction behavior, or acceptance checks.
- When the human owner asks to change an identifier, field, contract value, generated artifact, route, command output, or schema, clarify whether the request targets:
  - source content or source metadata
  - generated artifacts
  - runtime-only derived state
  - producer or consumer contract behavior
- Do not reinterpret a source-of-truth request as a generated-output-only change.
- Use `traceability-and-link-hygiene.md` for broader source/generated artifact ownership and stale-reference rules.

## Feature Approval Rule Extension

- A product feature must not be approved for spec handoff if a required foundation feature is unresolved.
- A foundation feature may be approved only when:
  - ambiguity is eliminated enough for downstream spec to proceed without guessing
  - ownership and dependency questions are no longer open
- A product feature may enter spec generation only after its required foundation features are `approved`.
- A product feature should enter build only after its required foundation features are `passed` when the dependency affects data shape, ownership, or acceptance logic.
- Do not approve a mixed feature boundary that combines a new foundation dependency with a downstream product outcome in the same execution target.
- Do not approve multi-surface execution until lane dependencies and evaluator ownership are explicit enough for the orchestrator to route the run.

## Traceability Rules
- Every PRD should have a stable ID such as `prd-0001`.
- Every feature should have a stable ID such as `feat-0001`.
- Every spec should have a stable ID such as `spec-0001`.
- Feature documents must link to their parent PRD by path and ID.
- Spec documents should link to exactly one parent feature and one parent PRD by path and ID.
- Harness runs, evaluator reports, or fix notes should reference the active feature ID.
- When a document is revised materially, add a short dated continuity note instead of rewriting history invisibly.

## Evaluator Behavior By Feature Type

- For product features:
  - validate user-visible behavior, interaction, layout, state transitions, and regression
- For foundation features:
  - validate contract completeness through Contract Evaluator
  - validate absence of blocking ambiguity
  - validate readiness for spec handoff
- Evaluators must not:
  - invent missing behavior
  - silently upgrade uncertainty into confirmed scope

## Naming Guidance
- Use filenames in the form `prd-####-slug.md` and `feat-####-slug.md`.
- Keep slugs short and outcome-focused.
- Prefer stable IDs over conversational filenames.

## Minimal Operating Pattern
- One PRD can yield several feature documents.
- Only one feature should normally be `in-loop` at a time unless the user explicitly wants parallel execution.
- Previous passed features become regression surfaces for later features.

## Split Trigger For Product Features

Split a product feature when one or more of these become true:
- multiple surfaces, modes, or lanes require substantially different structure
- fallback behavior diverges by surface
- evaluator failures cluster into different surfaces or contracts
- the feature absorbs a foundation contract that should pass before product behavior starts
- the feature repeatedly fails to converge within one to three loops

## Relationship To Agent Roles
- In a consuming repo, `docs/agents/roles/prd-normalizer.md` defines how to stabilize raw inputs into a bounded PRD.
- In a consuming repo, `docs/agents/roles/feature-planner.md` defines how to decompose an approved PRD into loop-sized features.
- In a consuming repo, `docs/agents/roles/spec-agent.md` defines how to convert one approved feature into a build-ready spec.
- In a consuming repo, `docs/policies/harness/execution-loop-governance.md` defines how approved features move through execution loops and how failures route upward.
- In a consuming repo, `docs/policies/harness/execution-profiles.md` defines how surfaces, lanes, profiles, and evaluator sets are selected.
- This guide defines where those outputs live and how they stay traceable over time.
