---
name: refactor-plan
description: Plan or update structured refactoring work when the user asks to refactor, split a refactor into phases, preserve behavior while changing structure, introduce intentional semantic cleanup with explicit scope, or create a reusable refactoring tracking document. Use when a codebase needs a clear phased refactor plan, invariants, validation gates, and merge-ready checkpoints.
---

# Refactor Plan

Use this skill when the task is to plan refactoring work, not to immediately implement the full refactor blindly.

This skill is general-purpose. It should travel well across repositories, stacks, and languages.

## Workflow

1. Read [references/method.md](references/method.md) and the target repository's guidance, nearby plans, architecture notes, and actual code boundaries.
2. Classify the work as `Structural`, `Behavioral`, or `Semantic`, and separate parity-preserving work from intentional deltas.
3. Extend the existing track or create a new one according to the method's ownership and continuity rules.
4. Build bounded steps around an explicit baseline, invariants, targets, validation, and exit gates.
5. Write only the requested plan, log, or merge-check artifact using the routed template.
6. Finish with [references/checklist.md](references/checklist.md) as the short final validation pass.

## General Rules

- Keep behavior-preserving work clearly separate from intentional semantic redesign.
- If behavioral parity is requested, treat parity as a proof task, not an assumption.
- For exploratory planning without merge judgment, keep parity status provisional by default.
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
- Do not claim "parity preserved", "no drift", or "safe to merge" before strict comparison evidence is recorded.
- Do not hide risky deltas inside broad step names like "cleanup", "modernization", or "polish".
- Do not use phases as a vague backlog dump; each phase needs a purpose, scope boundary, and exit gate.
- Do not assume a repository needs numbered plans if it already has a better local convention.
- Do not delete prior rationale from existing plan files unless the repository explicitly treats them as disposable working notes.
- Do not create a second refactor-planning folder when the project already has one established.

## Bundled References

- Use the detailed planning and parity method in [references/method.md](references/method.md).
- Use the final validator in [references/checklist.md](references/checklist.md).
- Use the plan template in [templates/plan.md](templates/plan.md).
- Use the log template in [templates/log.md](templates/log.md).
- Use the merge-check template in [templates/merge-check.md](templates/merge-check.md).

If the project already has a numbered scheme such as `REFACTOR-0001`, reuse that style. If not, adapt the same structure to the local naming convention.

## Artifact Roles

Use the skill outputs as a small coordinated document set rather than one interchangeable file type.

- Active plan:
  - the main tracking document for scope, invariants, planned steps, validation gates, and exit goals
- Refactor log:
  - the default execution record when tracked refactor work changes code, confirms a blocker, records runtime verification, or closes a handoff event
- Merge-check log:
  - a decision record used when the active question is whether a step, batch, or track is safe to merge or parity-safe against its baseline

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

- Treat logs as durable event records rather than casual notes.
- Use the general log for step, batch, blocker, runtime-smoke, wrap-up, and handoff events.
- Use the dedicated merge-check only when parity or merge safety is the active decision.
- Read [references/method.md](references/method.md) for log selection, adaptation, naming, and evidence rules.

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

## Parity-Strict Mode

When the user prioritizes behavioral parity, this mode is mandatory.

Activation boundary:
- Use this mode when parity, no-drift, or safe-to-merge claims are explicitly requested or clearly implied.
- If the user is only exploring plan options without merge judgment, keep parity provisional and do not force strict conclusions.

Required behavior:
- Pin an explicit compare baseline (branch/commit/release target) and record an immutable reference (resolved commit SHA) when available.
- Build a source mapping of affected old-path to new-path for the full execution flow.
- Apply the strict baseline audit in [references/method.md](references/method.md), including relevant query, write, output, side-effect, and failure-mode semantics.

Claim rules:
- If any relevant path is not audited, parity status must be `Unknown/Provisional`.
- Do not use confidence language to mask missing audit coverage.
- `Behavioral parity = Preserved` is valid only when strict audit coverage is complete, including side-effect and failure-mode coverage.
- If drift is found mid-audit, report it immediately and revise prior parity claims.
- If a previous parity-safe statement is later contradicted by audit evidence, explicitly retract and correct that statement.
