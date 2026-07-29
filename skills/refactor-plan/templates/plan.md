# Refactor Plan Form

Use this form when creating a new refactor tracking file or reshaping an existing one.

Use [../references/method.md](../references/method.md) for create-versus-extend, phase, parity, and artifact-selection decisions.

## Standard Template

```md
# [Refactor Plan Title]

## Purpose

[One short paragraph describing the objective and why this plan exists now.]

## Refactor Type

- Primary type: `Structural | Behavioral | Semantic`
- Parity target: `Behavior-preserving | Intentional delta`
- Compare baseline: `[branch, commit, release, or agreed target]`
- Baseline pin: `[resolved commit SHA when available; otherwise explain why provisional]`

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
- [when parity is required: explicit baseline-compare audit tasks]
- [when parity is required: explicit side-effect and failure-mode compare tasks]

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
- Parity audit coverage (required when parity is requested):
  - `[baseline pinned with resolved commit SHA when available]`
  - `[old->new source mapping complete]`
  - `[query/write semantics audited at logic-unit level]`
  - `[payload/output mapping audited]`
  - `[side-effect paths audited explicitly]`
  - `[failure-mode paths audited explicitly]`

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
