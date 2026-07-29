---
name: workflow-context-sync
description: Reconcile and maintain explicitly located workflow context across repositories, tickets, docs, notes, and runtime signals, while deciding whether the result should remain session-only, update an existing target, or be proposed for new persistence. Use when work spans multiple sources, source-of-truth conflicts or cross-session drift must be resolved, an existing local context target should be refreshed, or duplicate temporary contexts need consolidation without guessing a storage path from the current working directory.
---

# Workflow Context Sync

Use this skill to reconcile multi-source workflow context into one explicitly owned context target and keep it useful across sessions.

Preserve automatic source-integration behavior while separating invocation authority from persistence authority. An implicit trigger may inspect and reconcile relevant sources, but it never authorizes creation of a durable context artifact.

## Use This Skill When

- several repos, tickets, docs, notes, runbooks, or runtime signals must be reconciled
- an existing local context document or document set should be refreshed
- source-of-truth conflicts or stale assumptions must be made explicit
- a workflow needs a restart-ready handoff across sessions
- duplicate or misplaced context files need to be consolidated into a chosen target

Do not use this skill when:

- the user only wants to capture a standalone memo or rough note
- one source can answer the task without reconciliation or cross-session maintenance
- the task only needs an answer from already available context and no reconciliation or maintenance is needed

## Invocation And Persistence Boundary

Implicit invocation is supported when multi-source reconciliation, drift detection, or restart-ready maintenance is genuinely useful.

- An implicit invocation may read and reconcile sources, return a session-only synthesis, or update an already-existing canonical target when the current task calls for maintenance.
- An implicit invocation must not select `initialize`, create a file or directory, copy a context template, or manufacture an artifact merely to satisfy this skill's output shape.
- Creating a new durable context artifact requires an explicit user request to create, initialize, save, or persist workflow context at a chosen target.
- An existing memo, rough note, or other context-like file is evidence, not creation authority. Do not infer a canonical target from it or create a sibling `inter-context.md`.
- Target certainty is required for persistence, but it does not grant creation authority by itself.

## Requested Durability

Classify the user's durability requirement as an input to the decision:

- `session-only acceptable`: the user does not require a durable handoff
- `durable outcome requested`: the user explicitly wants context to survive the session
- `unspecified`: infer the appropriate disposition from the workflow evidence

Requested durability is not an output mode or storage target. A durable request authorizes a persistence proposal; creation still waits for target resolution and explicit approval.

## Persistence Decision Policy

Assess persistence before writing and tell the user which disposition applies.

- `session-only`: Use when the result is temporary, tentative, easy to reconstruct, or not needed for a later handoff. State briefly that session-only handling is sufficient; do not create a file or ask a blocking question.
- `maintain existing`: Use when an existing canonical target is already designated and durable facts, decisions, source freshness, or handoff state changed. Update only the owning artifact and report it.
- `propose persistence`: Use when no canonical target exists but the reconciled result is likely to matter across sessions, prevent repeated rediscovery, coordinate multiple sources, or preserve a durable decision. Explain what merits persistence, why session-only handling may be insufficient, and the proposed target and target kind. Do not create anything yet.
- `initialize after approval`: Use only after the user explicitly approves creation and the target and target kind are resolved.

Ask a blocking question only when new persistence is required to fulfill the user's requested durable outcome. If persistence would merely be helpful, present it as a non-blocking recommendation and keep the current result session-only.

## Core Outcome

Produce one of these explicit outcomes:

- a `session-only` synthesis with no persistence claim
- maintenance of one existing canonical target and its owning artifacts
- a persistence proposal that remains pending without creating files
- initialization of one explicitly approved canonical target

For a persisted outcome, identify the target kind as `document set` or `dedicated workflow context`, preserve source roles and reconciliation status, and leave a low-drift handoff. A mature context directory may already own truth through an entrance document and specialized child documents; do not force it into one `inter-context.md`.

## Context Model

Keep these locations distinct:

- `context home`: optional user-owned root for durable local context, which may be reached through an alias
- `context namespace`: the topic or workflow location inside the context home
- `canonical context target`: the existing document, document set, or explicitly approved new file that owns this workflow
- `working root`: the filesystem boundary used for the current work
- `current repo`: the repository being inspected or edited
- `related repos`: coupled repositories that affect the same decision

`working root`, `current repo`, and process `cwd` are evidence locations, not default context-storage locations.

## Operating Modes

### `maintain` (default write mode)

Use when an existing canonical context target can be resolved unambiguously.

- Read its entrance document and ownership map first.
- Update the smallest owning document or documents.
- Preserve the existing document-set shape.

### `initialize`

Use when the user wants a new durable workflow context and no target exists.

- Enter this mode only from an explicit request to create or persist durable workflow context.
- Require an explicit context target or an unambiguous namespace under an explicitly resolved context home.
- Confirm whether the new target should be a document set or a dedicated workflow context.
- Use [templates/inter-context.md](templates/inter-context.md) only for a dedicated workflow context.
- Do not create a fallback `inter-context.md` under `cwd`, the current repo, or the workflow root.

### `consolidate`

Use when several context candidates or misplaced temporary files cover the same workflow.

- Select the canonical target before merging.
- Compare candidates and preserve unique supported facts, decisions, provenance, and unresolved questions.
- Classify each non-canonical artifact as `keep`, `archive`, or `delete candidate`.
- Delete or archive files only when the user explicitly approves those exact targets.

## Canonical Target Resolution

Resolve the target in this order:

1. explicit file or document-set path supplied by the user
2. explicit context alias and namespace resolved through active entrance instructions
3. a recorded mapping in an existing context entrance document or context map
4. one unambiguous existing target inside an explicitly resolved context home
5. unresolved

Rules:

- Record the resolved path, not only the alias.
- Prefer an existing context entrance and its owned child documents over creating a parallel file.
- Do not infer a durable storage target from repository name similarity alone.
- If zero or multiple plausible targets remain, present the candidates and keep persistence pending.
- An implicit trigger may reconcile and report, and may update an already-existing mapped canonical target when maintenance is in scope.
- Never create a new durable artifact unless both the target is unambiguous and the user has explicitly granted creation authority.

## Source Model

Classify sources as:

- `implementation truth`
- `authoritative spec`
- `planned work`
- `operational signal`
- `working note`
- `historical note`

Define priority per claim domain rather than assuming one universal source order. Keep unclear roles and conflicts open.

For each important claim, record:

- what each relevant source says
- reconciliation status
- working assumption for the current session
- the source or target that must be updated to close a mismatch

## Workflow Summary

1. capture the goal, working root, current repo, invocation origin, requested durability, and creation authority
2. resolve context home, namespace, and any existing canonical target without using `cwd` as a fallback
3. assess whether the result should remain session-only, maintain the existing target, or be proposed for new persistence
4. choose `maintain`, `initialize`, or `consolidate` only when a persistence operation applies
5. read the canonical target before broad source scanning when one exists
6. refresh only the sources needed for the current decision
7. reconcile claims and update only the owning context artifacts
8. present the persistence assessment, context changes, conflicts, assumptions, and resolved target
9. enforce the reconciliation approval gate before downstream implementation
10. update persisted context again when approved work changes facts or decisions
11. end with a restart-ready handoff when persistence applies, or an honest session-only conclusion

Read [references/method.md](references/method.md) for detailed path resolution, mode procedure, document-set handling, consolidation, and failure diagnosis.

## Reconciliation Approval Gate

- Context reads, reconciliation, and approved target updates belong to this skill.
- Code edits, refactors, and downstream execution do not start before the user reviews the reconciliation result.
- Default approval mode is `strict`.
- `optional` or `skip` is allowed only when the user explicitly requests it for the current session.
- Keep the review state `pending` until the proceed signal required by the selected mode is satisfied.

## Output Contract

Report:

- operating mode when persistence applies, or `none` for session-only
- invocation origin and creation authority
- requested durability
- persistence disposition and rationale
- proposed target and target kind when new persistence is recommended
- resolved context home and namespace when used
- canonical target and target kind, or `unresolved`
- sources checked and meaningful deltas
- conflicts, open questions, and working assumptions
- files updated
- consolidation disposition when relevant
- user review status
- next-session handoff

Do not claim persistence when only a session summary was produced.

## Bundled Files

- Use [templates/session-kickoff.txt](templates/session-kickoff.txt) when structured intake helps.
- Use [templates/inter-context.md](templates/inter-context.md) only when initializing an explicitly approved dedicated workflow context.
- Use [references/method.md](references/method.md) for detailed execution and diagnostics.
- Use [references/checklist.md](references/checklist.md) for final validation.

## File Role Boundaries

- `SKILL.md`: trigger, context model, modes, hard placement rules, approval boundary, and output contract
- `references/method.md`: detailed target resolution, reconciliation, update, and consolidation procedure
- `references/checklist.md`: short final yes-or-no validation
- `templates/session-kickoff.txt`: optional structured intake
- `templates/inter-context.md`: scaffold for an explicitly chosen dedicated workflow context, not a default file for every context directory
