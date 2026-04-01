---
name: refactor-plan
description: Plan or update structured refactoring work when the user asks to refactor, split a refactor into phases, preserve behavior while changing structure, introduce intentional semantic cleanup with explicit scope, or create a reusable refactoring tracking document. Use when a codebase needs a clear phased refactor plan, invariants, validation gates, and merge-ready checkpoints.
---

# Refactor Plan

Use this skill when the task is to plan refactoring work, not to immediately implement the full refactor blindly.

This skill is general-purpose. It should travel well across repositories, stacks, and languages.

## Workflow

1. Gather planning context before proposing steps.
   - Read the bundled checklist in [references/checklist.md](references/checklist.md).
   - Inspect any repository-specific guidance already present in the target codebase.
   - List existing refactor plans, architecture notes, or tracking files and inspect the ones closest in scope.
   - Anchor the plan in actual files, modules, interfaces, data contracts, and runtime behavior.

2. Classify the refactor before designing phases.
   - Mark the work as primarily `Structural`, `Behavioral`, or `Semantic`.
   - State whether the goal is behavior-preserving parity or intentional semantic change.
   - Separate non-goals so unrelated infrastructure churn, package churn, and semantic redesign do not get mixed casually.

3. Decide whether to extend or create a tracking document.
   - Extend an existing plan when the new work is a direct continuation of that track.
   - Create a new numbered or named plan when the work starts a distinct new track.
   - Do not overwrite historical rationale from earlier plan files; preserve continuity and add explicit handoff notes when scope moves.
   - By default, place refactor tracking files under `./docs/refactoring/`.
   - If the project already uses another folder for refactor plans, follow that existing convention instead of forcing a new one.

4. Build the plan in bounded slices.
   - Define baseline compare target and invariants first.
   - Split work into steps/phases/batches with clear boundaries.
   - For each step, define goal, why the grouping is safe, representative targets, validation, and exit gate.
   - Keep risky interface, persistence, deployment, concurrency, or messaging changes late unless they are the direct objective.
   - Make each step small enough that completion can be proven, reviewed, and reverted without ambiguity.

5. Use architecture boundaries deliberately when planning semantic refactors.
   - Prefer clearer separation between entrypoints, orchestration, domain logic, and infrastructure concerns where that separation exists or is desired.
   - Keep externally visible contracts and operational behavior stable unless intentional deltas are explicitly approved.

6. Make the output immediately usable.
   - If asked to create the plan, write or update the actual tracking file.
   - Prefer `./docs/refactoring/` as the default location for refactor schemes, plans, and handoff notes.
   - Prefer `./docs/refactoring/logs/` as the default location for refactor logs.
   - If the project already uses a different planning folder, continue there rather than splitting refactor history across multiple locations.
   - If only asked for planning guidance, provide a concise draft using the same canonical structure without unnecessary prose.

## General Rules

- Keep behavior-preserving work clearly separate from intentional semantic redesign.
- Preserve interface, schema, config, and generated-artifact coupling awareness when types, packages, or module boundaries move.
- Include wiring or registration checks when moving framework configuration, plugins, containers, consumers, handlers, or adapters.
- Prefer targeted parity tests plus build, startup, and runtime smoke gates for touched paths rather than vague "test everything" plans.
- Call out any expected deltas in null handling, exceptions, logging, retry behavior, side effects, concurrency, or transaction shape.
- Do not mix unrelated modernization, formatting, naming churn, and semantic redesign into the same step unless the plan explicitly says that is the goal.
- Prefer evidence-first planning: if invariants, contracts, or affected paths are unclear, investigate before defining the step boundary.
- Preserve plan continuity: when a track hands work to a later track, leave a handoff snapshot instead of silently rewriting history.

## Planning Guardrails

- Do not present speculative architecture as if it were already approved.
- Do not label a step "behavior-preserving" if contracts, persistence semantics, or side effects are intentionally changing.
- Do not hide risky deltas inside broad step names like "cleanup", "modernization", or "polish".
- Do not use phases as a vague backlog dump; each phase needs a purpose, scope boundary, and exit gate.
- Do not assume a repository needs numbered plans if it already has a better local convention.
- Do not delete prior rationale from existing plan files unless the repository explicitly treats them as disposable working notes.
- Do not create a second refactor-planning folder when the project already has one established.

## Bundled References

- Use the reusable checklist in [references/checklist.md](references/checklist.md).
- Use the plan template in [templates/plan.md](templates/plan.md).
- Use the log template in [templates/log.md](templates/log.md).
- Use the merge-check template in [templates/merge-check.md](templates/merge-check.md).

If the project already has a numbered scheme such as `REFACTOR-0001`, reuse that style. If not, adapt the same structure to the local naming convention.

## Canonical Output Format

Unless the repository already has a stronger mandatory format, generate plans in this exact section order:

1. `Purpose`
2. `Refactor Type`
3. `Scope`
4. `Non-Goals`
5. `Invariants`
6. `Planned Work`
7. `Validation Gates`
8. `Intentional Deltas`
9. `Risks / Open Questions`
10. `Exit Goal`

For every step inside `Planned Work`, include these exact fields:
- `Goal`
- `Why this grouping`
- `Guardrails`
- `Targets`
- `Validation`
- `Exit gate`

When work moves to a later track, add a final handoff section:
- `Handoff to Next Track`

Use this stricter structure by default. Do not omit sections just because the answers are incomplete; mark them as provisional if needed.

## Log Guidance

Write refactor logs as durable execution records, not casual notes.

- Use logs to capture:
  - step completion
  - blocker discovery
  - runtime smoke results
  - merge or parity checks
  - wrap-up and handoff outcomes
- Prefer one log per meaningful event or batch.
- Keep logs factual and scoped:
  - what was attempted
  - what changed
  - what was validated
  - what remains risky
  - what comes next
- Do not mix multiple unrelated events into one log just because they happened on the same day.
- When a log is tied to a plan track, link the active tracking file near the top.
- Prefer `./docs/refactoring/logs/` as the default log folder unless the project already uses a different established location.

Unless the project already has a stronger mandatory format, generate logs in one of these canonical shapes:
- Step log
- Blocker log
- Runtime smoke log
- Wrap-up or handoff log
- Merge check log

Use the shared template and adapt the optional sections to the log type instead of inventing a new structure each time.
For merge or parity judgment logs, prefer the dedicated merge-check template instead of the general log form.
When baseline or parity expectations are not obvious from the project context, ask for the missing comparison target if needed; otherwise proceed with an explicit provisional assumption and record it in the merge check.

## Output Standard

Every refactor plan should make these items explicit:
- compare target or baseline
- invariants to preserve
- scope and non-goals
- step/phase boundaries
- validation gates
- intentional deltas
- residual risks or open questions

If any of those are unknown, mark them as provisional instead of pretending they are settled.
