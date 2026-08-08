# Operator Briefing And Review Receipts

## Purpose

Reduce the human operator's need to reconstruct project direction from prior conversations and scattered artifacts during long-running work.

This policy adds a user-facing continuity projection. It does not add a workflow stage, source of truth, lifecycle state, approval gate, or persistent artifact requirement.

## Authority And Non-Interference

- Existing PRDs, policies, research, features, specs, runs, evaluations, open-point owners, and human decisions remain canonical.
- A briefing or receipt summarizes and links canonical facts; it never becomes the authority for those facts.
- Do not change task selection, approval, execution, evaluation, or persistence semantics merely to produce a briefing.
- Do not create a permanent briefing, map, ledger, or session log unless an existing owner contract or an explicit user request requires one.
- Do not require the user to remember or invoke a command. Apply this policy from request and lifecycle context.
- If no relevant context or meaningful delta exists, remain silent and preserve the normal response shape.

## Work Episode

Use the work episode, not the chat session, as the repetition boundary.

A work episode starts when one canonical target becomes actionable, including a PRD, feature, run, evaluation, handoff, or other explicit objective. It ends when that target is completed, blocked, returned, handed off, or replaced by another target.

A new chat may resume an existing episode. One chat may also contain multiple episodes.

## Output Types

### Orientation Brief

Use when the user asks what is next, where the effort stands, what remains, or what is blocked without yet activating a work target.

Explain:

- the active destination or effort;
- the current position in that effort;
- the most relevant available next work;
- work that is not ready and why;
- any human review that is already due.

Do not emit a receipt when orientation does not change direction or durable state.

### Work Briefing

Use once when a new canonical target is activated or resumed and prior context materially affects how it should be understood or executed.

Explain:

- the larger objective;
- the prior events that led to the current state;
- why this target is the correct current step;
- what the target can and cannot change;
- relevant unresolved decisions, evidence limits, or approval boundaries;
- what the agent will do now;
- what the human must decide now, later, or not at all.

### Direction Alert

Use during an active episode only when new input or evidence materially changes or conflicts with direction, scope, acceptance, evidence admission, safety, authority, or a review obligation.

Explain the previous direction, the proposed or discovered change, its impact, and whether work must stop. Do not repeat the full Work Briefing.

### Review Receipt

Use at a meaningful completion, planning return, block, handoff, approval boundary, or durable change when the operator needs to understand what changed.

Explain:

- what was established;
- what remains unresolved;
- any assumption introduced or invalidated;
- any direction or open-point impact;
- what the human must review now;
- the event that should surface the matter again;
- canonical references for audit.

If durable work changed no direction, review obligation, or open point, prefer one sentence such as: `Direction, approval scope, and open points are unchanged.` Omit even that sentence when it adds no user value.

## Trigger Rules

| Situation | Output |
| --- | --- |
| User asks what is next, current, remaining, or blocked | Orientation Brief |
| User activates a PRD, feature, run, evaluation, or named objective | Work Briefing when prior context is material |
| User names only an area and the agent must resolve the canonical target | Resolve the target first, then Work Briefing |
| New chat resumes a named target | Work Briefing with enough resume context |
| User says continue without a target | Resolve the active target or handoff, then brief |
| User supplies a handoff | Reconcile it with canonical state, then brief the material differences |
| Same target receives a small follow-up | No repeated briefing |
| Multiple requested tasks share one objective | One combined briefing that explains ordering and blockers |
| Target changes within the conversation | Start a new episode and brief the new target |
| User makes or reverses a material decision | Direction Alert, then a Review Receipt when the turn concludes |
| New evidence changes an assumption or admission boundary | Direction Alert and later Receipt |
| Implementation reaches an unapproved planning boundary | Explain the boundary and return path before proceeding |
| Evaluation passes with partial or narrower evidence | Explain exactly what passed and what remains unproven |
| Work returns to planning, blocks, or hands off | Review Receipt |
| High-risk live, release, destructive, or irreversible action approaches | Expanded briefing; existing approval rules still govern |
| Simple explanation, lookup, or unrelated small question | No briefing or receipt |

## Detail Selection

Choose the shortest form that remains self-contained.

- `compact`: one to three sentences for a same-target continuation or unchanged boundary;
- `standard`: a short causal explanation for a newly activated, well-understood target;
- `expanded`: enough prior events and definitions for a new session, stale handoff, long gap, partial evidence, planning return, or high-risk boundary;
- `decision`: the actual decision, alternatives, consequences, and authority when the human must choose.

Do not optimize for a fixed word count. Optimize for the operator being able to understand the situation without opening a linked artifact.

## Self-Contained Explanation Contract

A standard or expanded briefing must let the operator answer these questions without another lookup:

1. What are we trying to accomplish?
2. What happened previously?
3. Why is the work not already complete?
4. Why is this the current step?
5. What will and will not change?
6. What, if anything, must the operator decide or review?

Use a causal narrative rather than a list of status labels.

- Introduce a title or plain-language name before an internal ID.
- Explain unfamiliar terms, evidence grades, markers, states, and abbreviations on first use.
- Explain why a fact matters now instead of merely listing it.
- Distinguish implementation acceptance from broader operational, product, or release readiness.
- Make links optional for comprehension and useful for audit.
- State uncertainty rather than filling missing context with an inference.

A briefing fails when the operator must open links merely to understand the event sequence or the meaning of its status terms.

## Bounded Context Loading

Resolve the canonical target before loading continuity context. Read the smallest connected evidence set that can satisfy the explanation contract.

Prefer, in order:

1. the active target;
2. its parent destination or approved boundary;
3. the latest relevant run, evaluation, or handoff;
4. directly linked open points or review obligations;
5. the latest human decision that materially affects the target.

Do not load every historical run, every open point, all sibling features, or full conversation history by default. Expand only when the target is ambiguous, sources conflict, a handoff may be stale, or a safety or authority decision depends on older context.

Stop gathering continuity context when the six self-contained questions can be answered and canonical conflicts have been resolved.

## Repetition And Frequency

- Emit at most one full Work Briefing for the same unchanged target in one episode.
- Do not repeat an Orientation Brief when the user immediately selects one of its targets; provide only any missing target-specific context.
- Do not repeat unchanged facts on follow-up turns.
- Emit a Direction Alert only for a material change or conflict.
- Emit one consolidated Review Receipt at the end of the meaningful turn or episode transition rather than one receipt per internal step.
- When several deltas belong to the same target, combine them by consequence rather than artifact order.
- A new target starts a new episode and may justify a new briefing.

## Handoff Reconciliation

Treat a handoff as a context pointer, not as canonical truth.

Before resuming:

- resolve the target named by the handoff;
- compare its claims with current canonical artifacts;
- identify what still matches, what changed later, and what assumption is now invalid;
- explain the causal history needed to understand the safe resume point;
- resume from current canonical state, not from stale handoff instructions.

Do not present terse state labels as a handoff briefing. Explain what each material state means and why it affects the next action.

## Persistence

The briefing layer does not own persistence.

When a turn creates a real direction, decision, open point, or review obligation, update the existing canonical owner under its normal approval and persistence rules. The Receipt then points to that owner.

If no durable owner is resolved, report that the information remains session-only. Do not invent a storage path solely to preserve a Receipt.

## Template

Use [Operator Briefing Template](../../templates/operator-briefing.md) when a standard, expanded, decision, or handoff form is useful. Omit empty sections and rewrite the scaffold into natural prose rather than mechanically filling every heading.

## Acceptance Checks

Before emitting a briefing or receipt, confirm:

- it was triggered by a target or meaningful lifecycle event rather than habit;
- it does not alter canonical state or authority;
- it is relevant to the active target;
- it explains causality and material terms;
- the operator can understand it without following links;
- links point to canonical evidence rather than replacing explanation;
- unchanged information is not repeated;
- human action is explicit as `now`, `later at a named trigger`, or `none`;
- no permanent by-product was created merely for presentation.
