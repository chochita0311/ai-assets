# Refactor Plan Form

Use this form when creating a new refactor tracking file or reshaping an existing one.

Keep the file practical. It should guide execution, review, and merge decisions, not narrate the entire history.

## Decision Rules

### When to create a new plan

Create a new plan when at least one of these is true:
- the goal changes from structural parity to semantic redesign
- the dominant risk shifts to a new layer, such as runtime, platform, persistence, or domain behavior
- the previous track is complete and the next work needs a new scope boundary
- the old file would become confusing if the new work were appended

### When to extend an existing plan

Extend the current file when:
- the work is the next batch in the same initiative
- the same baseline, goals, and risk model still apply
- the file remains readable after adding the next step or handoff note

### How to organize steps well

Prefer step boundaries that follow one or more of these:
- blast radius
- dependency order
- runtime criticality
- contract surface
- validation strategy

Avoid steps that are only "misc cleanup" buckets.

## Standard Template

```md
# [Refactor Plan Title]

## Purpose

[One short paragraph describing the objective and why this plan exists now.]

## Refactor Type

- Primary type: `Structural | Behavioral | Semantic`
- Parity target: `Behavior-preserving | Intentional delta`
- Compare baseline: `[branch, commit, release, or agreed target]`

## Scope

1. [High-level scope item]
2. [High-level scope item]
3. [High-level scope item]

## Non-Goals

- [Explicitly excluded work]
- [Explicitly excluded work]

## Invariants

- Functional: [inputs, outputs, side effects, contracts]
- Runtime: [transactions, startup wiring, concurrency, registrations]
- Data: [defaults, statuses, schemas, semantics]

## Planned Work

### Step 1 - [Short title]

Goal:
- [What this step achieves]

Why this grouping:
- [Why this batch is safe and coherent]

Guardrails:
- [What this step will not change]
- [What would force the work into a later or different track]

Targets:
- `[path/or/component]`
- `[path/or/component]`

Validation:
- [build or compile gate]
- [targeted tests]
- [startup, registration, or runtime smoke if needed]

Exit gate:
- [What must be true before moving on]

### Step 2 - [Short title]

[Repeat as needed]

## Validation Gates

- Build or static validation:
  - `[command or proof target]`
- Tests:
  - `[targeted suites or smoke paths]`
- Review focus:
  - `[contract parity, persistence semantics, side effects, transaction shape, etc.]`

## Intentional Deltas

- `None yet` or [explicit list]

## Risks / Open Questions

- [Known risk]
- [Decision still needed]

## Exit Goal

- [What done looks like for this track]

## Handoff to Next Track

- [Only include when work is intentionally deferred or handed off]
```

## Usage Notes

- Default location for generated plans:
  - `./docs/refactoring/`
- If the repository already uses a numbered scheme such as `REFACTOR-0001`, keep that naming convention.
- If it does not, adapt the structure to the local planning style rather than forcing a new naming system.
- If the project already stores refactor plans in another folder, keep using that folder instead of introducing `./docs/refactoring/` in parallel.
- Leave handoff snapshots when work moves into a later track instead of silently deleting context.
- Do not describe intentional behavior changes as refactoring unless the plan explicitly marks them as intentional deltas.
- Use the section order exactly unless the repository has an explicitly stronger required format.
