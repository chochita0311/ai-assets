---
name: refactor-plan
description: Create or update refactoring plans, phased tracks, and tracking documents for structural, behavioral, or intentional semantic changes. Use when the task needs explicit refactoring scope, invariants, phase boundaries, validation gates, or a refactor parity or merge checkpoint. Do not use for ordinary implementation or cleanup that needs no planning artifact or parity/merge decision, general code reviews, or PR publication.
---

# Refactor Plan

Use this skill to plan refactoring work, record tracked execution, or assess parity or merge safety.

This skill is general-purpose. It should travel well across repositories, stacks, and languages.

Use it without requiring a harness, runtime adapter, or particular reviewer. The method owns refactor review decisions; available reviewers supply bounded evidence under the task's authority.

## Workflow

1. Choose the [artifact role](#artifact-roles) from the request. Read the [method](references/method.md), the target repository's guidance, relevant existing plans, architecture notes, and affected code.
2. Classify the work as `Structural`, `Behavioral`, or `Semantic`, and separate parity-preserving work from intentional deltas.
3. For a parity, merge-safety, or completion judgment, apply the method's frozen-comparison, independent-challenge, adjudication, and re-review gates.
4. Write only the requested artifact using the routed template or established equivalent. Finish with the applicable questions in [the checklist](references/checklist.md).

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

- Use the detailed planning and parity method in [references/method.md](references/method.md): sections 0–3 for planning, 4 for frozen comparisons and review, and 5–7 for validation and merge scope.
- Use the final validator in [references/checklist.md](references/checklist.md).
- Use the plan template in [templates/plan.md](templates/plan.md).
- Use the log template in [templates/log.md](templates/log.md).
- Use the merge-check template in [templates/merge-check.md](templates/merge-check.md).

If the project already has a numbered scheme such as `REFACTOR-0001`, reuse that style. If not, adapt the same structure to the local naming convention.

## Artifact Roles

- **Active plan.** Extend the existing track or create one under the method's ownership and continuity rules. Record its scope, baseline, invariants, and exit goal. Give each bounded step targets, validation, and an exit gate.
- **Execution log.** Record meaningful tracked execution such as a completed step or batch, a blocker, runtime verification, wrap-up, or handoff. Use the existing durable record for that event or the general log template if it has no such owner.
- **Merge-check.** When the question is parity or merge safety for a step, batch, or track, identify the scope, baseline, and candidate. Link the active plan if one exists. A standalone checkpoint needs no new plan.

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

Keep each log as a durable record of the event or decision. Follow the [logging method](references/method.md#artifact-selection-and-logging) for selection, adaptation, naming, and evidence requirements.

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
- Freeze the explicit compare baseline and actual candidate using the method's [comparison identity rules](references/method.md#40-freeze-the-comparison-and-review-allowance); a complete immutable uncommitted bundle is allowed.
- Build a source mapping of affected old-path to new-path for the full execution flow.
- Apply the strict baseline audit in [references/method.md](references/method.md), including relevant query, write, output, side-effect, and failure-mode semantics.

Claim rules:
- If any relevant path is not audited, parity status must be `Unknown/Provisional`.
- Keep required independence gaps and material unresolved objections explicit; they prevent an unqualified completion or merge-safety claim.
- Do not use confidence language to mask missing audit coverage.
- `Behavioral parity = Preserved` is valid only when strict audit coverage is complete, including side-effect and failure-mode coverage.
- If drift is found mid-audit, report it immediately and revise prior parity claims.
- If a previous parity-safe statement is later contradicted by audit evidence, explicitly retract and correct that statement.
