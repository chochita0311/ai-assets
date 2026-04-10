# Design Document Governance Template

## Purpose
- Define the ownership, hierarchy, and update rules for the repo's main design documents.
- Keep creative intent, durable design law, and future planning clearly separated.
- Prevent design drift as the product expands across screens, states, and features.

## Governance Model
- Creative source:
  - usually `DESIGN.md` or another repo-specific design-intent document
- Durable design source of truth:
  - `design-constitution.md`
- Optional future planning track:
  - `docs/plans/design/` when the repo later needs tracked design planning

These documents are related, but they are not peers. Each one owns a different kind of information and should be updated for different reasons.

## Source Hierarchy
1. `design-constitution.md` governs implementation and evaluation.
2. The creative source document provides intent, direction, and source material.
3. Any future design plan tracks active sequencing and unresolved work only when needed.

If documents conflict:
- The constitution wins for durable rules.
- A future plan wins only for active sequencing and open work.
- The creative source may justify a future rule change, but it does not override locked rules by itself.

## Document Ownership

### Creative Source
- Owns:
  - creative north star
  - visual intent
  - tone and atmosphere
  - source-material interpretation
  - early system direction from screens or artifacts
- Should not contain:
  - final token governance
  - enforceable implementation rules
  - detailed rollout sequencing

### `design-constitution.md`
- Owns:
  - durable design law
  - implementation contract
  - evaluation baseline
  - reusable system constraints
- Should not contain:
  - temporary work notes
  - speculative one-off experiments
  - build order
  - unresolved uncertainty that belongs outside durable policy

### Future Design Plan
- Owns, only when it exists:
  - active design scope
  - sequencing
  - unresolved decisions
  - current deltas between the desired system and the implemented one
- Should not contain:
  - a rewritten constitution
  - locked token tables already owned elsewhere
  - stable creative rationale already owned by the creative source

## Update Rules
- Update the creative source when the creative direction, visual rationale, or source-material interpretation meaningfully changes.
- Update `design-constitution.md` when a durable rule changes.
- Update a future design plan only when active scope, sequencing, or uncertainty needs durable tracking.
- Do not update all documents by default. Update only the document that owns the change.

## Rule Promotion
When new design input appears:
1. Review the input against the creative source and `design-constitution.md`.
2. Identify what changed: intent, durable rule, or active work.
3. Promote a change into the constitution only if it is durable, reusable, and likely to affect more than one screen, state, or component family.
4. Keep one-off experiments and temporary polish out of the constitution.
5. If later sequencing becomes substantial, record it in a separate design planning track instead of expanding this governance doc.

## Evaluation Rules
- Evaluate implementation primarily against `design-constitution.md`.
- Use the creative source as supporting context for tone, intent, and rationale.
- Use any future design plan to understand current deltas and active work, not to redefine the system.

## Drift Prevention
- Do not treat the creative source and the constitution as equal sources of truth.
- Do not mechanically sync documents after every visual tweak.
- Do not promote temporary screen polish into durable system law.
- Do not introduce new tokens, component families, or layout primitives in implementation without a constitution update.

## Practical Summary
- The creative source explains why the design should feel this way.
- `design-constitution.md` defines what the system must consistently obey.
- A future design plan, if later needed, defines what is being changed now.
