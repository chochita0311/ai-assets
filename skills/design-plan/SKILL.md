---
name: design-plan
description: Use when a project already has multiple screens, artifacts, or existing UI drift and you need a concrete design planning track for BX, UI, UX consistency, phased cleanup, or design-system reconciliation. This skill creates or updates a tracked design plan rather than a durable design constitution.
---

# Design Plan

Use this skill when the problem is no longer "define the design system from a base artifact" and is instead "plan how to reconcile, sequence, and validate design work across an existing product."

## Use This Skill When
- Several pages or screen artifacts already exist and design consistency needs active coordination.
- BX, UI, or UX drift has appeared across screens, components, or flows.
- The design constitution exists but implementation has drifted away from it.
- A project needs phased design cleanup, rollout sequencing, or reconciliation across multiple artifacts.
- The user explicitly asks for a design plan, design consistency plan, UX consistency plan, BX plan, or phased design refactor.

## Do Not Use This Skill When
- The main task is to derive durable design law from a first artifact. If `init-design` is available, that skill is usually a better fit.
- The user only wants a constitution or a one-shot design baseline.
- The issue is a single isolated component polish with no broader planning need.

## Output
- Write or update a design planning track under `./docs/plans/design/` by default.
- Use [templates/plan.md](templates/plan.md) as the default scaffold when the repository does not already have a stronger planning format.
- Prefer a specific descriptive file name when the repository does not already have one:
  - `design-consistency-plan.md`
  - `bx-ux-alignment-plan.md`
  - `design-reconciliation-plan.md`
- If the repo already has an active design plan, extend it instead of creating a parallel file.

## Source Priority
Use this order unless the repository defines a stricter owner:
1. explicit user direction for the current planning scope
2. the current design constitution and durable design policies
3. accepted decisions in the active design plan
4. current rendered screens and implementation as evidence of present state
5. cautious inference

- Record an explicit user-approved exception when current direction intentionally changes durable design law.
- Treat implementation drift as a finding to reconcile, not as authority that silently overrides the constitution.
- If the sources conflict and the conflict changes scope or durable law, keep it open rather than resolving it by preference.

## Core Rule
- Treat this as a planning and reconciliation workflow, not as a second constitution.
- Keep durable visual law in `docs/policies/design/`.
- Use the design plan only for active sequencing, scoped batches, open design decisions, validation, and rollout tracking.

## Plan Should Include
- purpose
- baseline or audited sources
- scope
- non-goals
- invariants
- findings or drift categories
- planned work in bounded batches
- validation gates
- risks or open questions
- exit goal

## Plan Should Not Include
- a restatement of the full design constitution
- locked token tables already owned by design policy docs
- speculative redesign directions with no execution boundary
- implementation-free summaries that do not affect sequencing

## Recommended Structure
1. `Purpose`
2. `Plan Type`
3. `Baseline`
4. `Scope`
5. `Non-Goals`
6. `Invariants`
7. `Findings` or `Consistency Problems`
8. `Planned Work`
9. `Validation Gates`
10. `Risks / Open Questions`
11. `Exit Goal`
12. `Handoff to Next Track` when needed

## Planned Work Expectations
- Split work into bounded batches by screen family, pattern family, or drift category.
- For each batch include:
  - `Goal`
  - `Why this grouping`
  - `Guardrails`
  - `Targets`
  - `Validation`
  - `Exit gate`

## Validation
- Prefer side-by-side artifact review, runtime smoke checks, and constitution-alignment checks.
- State clearly whether the plan is for:
  - visual consistency
  - interaction consistency
  - information hierarchy consistency
  - brand-experience consistency
  - or a combination

## Handoff Rule
- If the outcome becomes stable design law, move it into `docs/policies/design/`.
- If the outcome remains active cleanup or rollout work, keep it in the design plan.
- Stop after creating or updating the planning track unless the user separately asks for constitution changes or implementation.
