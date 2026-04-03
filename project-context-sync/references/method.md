# Project Context Sync Method

## Purpose

This file owns detailed operating logic for `project-context-sync`.
`SKILL.md` is the entry contract; this file is the execution procedure.

## Baseline Behavior Model

The skill should produce:
- one canonical context file per workflow
- stable startup inputs (`project root`, `current repo`, `reference scope`)
- low drift when work moves across repos and sessions

## Procedure

### 1. Intake Normalization

Extract and normalize:
- `project root`
- `current repo`
- `related repos`
- optional `reference scope` (free-text)
- optional `references in scope` (type + identifier/link)
- optional `reference relationships` (for example parent/child)
- `shared context path` or `follow context`

If user input defines relationships (for example parent/child tickets), record that relation explicitly.
If no reference is provided, continue with local-context-first flow.
If `current repo` is missing, resolve it only when one explicit path candidate is unambiguous; otherwise keep it as an open question.
If input is in the form `related project like in <root>, <repo-a>, <repo-b>...`, parse `<root>` as project root and remaining items as related repo tokens.
If input says `follow-up ticket <KEY> and below tickets`, set relationship note as `parent=<KEY>, children=in-scope`.

### 2. Resolve Repo Paths

For each related repo token:
1. resolve exact path under `project root`
2. if not found, attempt alias resolution only when unambiguous
3. if ambiguous, keep as open question
4. record mapping in context (`token -> resolved path`)

Do not silently invent repo names.
If related inputs mix absolute paths and repo tokens, normalize both into one resolved list.
Never promote unresolved related repo tokens to `current repo` without explicit evidence.

### 3. Resolve Canonical Context File

Use this order:
1. explicit `follow context` path
2. explicit `shared context path`
3. current repo `inter-context.md`
4. root-level `inter-context.md`

If none exists, initialize from `templates/inter-context.md`.

### 4. Read Context Before Deep Search

Read current context first, then open `working targets`.
Treat the context as baseline state for this session.

### 5. Pause and Confirm Before Implementation

After creating/updating/reading context:
- report synced context status to user
- pause and wait for explicit confirmation
- allow user to revise context before implementation begins

Do not edit code, run implementation commands, or start refactoring before this confirmation.

### 6. Verify Code by Priority

1. current repo implementation
2. related repo behavior only when coupling exists
3. downstream/scheduler roles only when they affect current decision

### 7. Decide External Recheck

If no references are in scope, skip external recheck by default.
Use external sources only when one of these is true:
- reference policy is missing from local context
- latest decision freshness is uncertain
- reference sync is explicitly requested
- rollout/payload/schema details are externally owned

Otherwise, skip external recheck and continue on local context + code.

### 8. Update Context in Same Session

When code or policy facts change, update context immediately:
- confirmed facts
- open questions
- working targets
- recent decisions
- reference sync status
- reference deltas vs local context
- external recheck needed flag
- next handoff note

### 9. End with Handoff

Handoff should include:
- what was confirmed
- what remains open
- where to start next session

## Failure Diagnosis

Common failures and fixes:

1. Reference-scope drift
- Symptom: declared references and actually-used references diverge.
- Fix: keep a minimal explicit reference list and update it when scope changes.

2. Repo-name drift
- Symptom: user token and local directory diverge (`service-api` vs actual local directory name).
- Fix: record alias mapping and resolved absolute path in context.

3. External-source overuse
- Symptom: every session starts with external sources regardless of need.
- Fix: apply the external recheck decision gate in step 6.

4. Context not updated after code change
- Symptom: next session repeats discovery work.
- Fix: enforce step 7 in same session as the change.

5. Premature implementation start
- Symptom: agent starts changing code immediately after context sync.
- Fix: enforce step 5 pause gate and require explicit user "proceed" signal.
