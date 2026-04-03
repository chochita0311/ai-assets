# Workflow Context Sync Method

## Purpose

Own the detailed execution logic for `workflow-context-sync`.
Treat `SKILL.md` as contract and this file as procedure.

## Behavior Model

The skill should yield:
- one canonical context file per workflow
- source-role-aware reconciliation output
- explicit review state before implementation
- low context drift across sessions

## Procedure

### 1. Normalize Intake

Extract and normalize:
- `workflow root`
- `current repo`
- `related repos` (if any)
- `current goal`
- optional `follow context` or `shared context path`
- optional `sources in scope`
- optional `source relationships`

If `current repo` is missing, resolve only when one path is unambiguous; otherwise mark open.

### 2. Resolve Repo Paths and Aliases

For each related repo token:
1. resolve path under `workflow root`
2. apply alias mapping only when unambiguous
3. record `token -> resolved path` mapping
4. keep unresolved tokens in `open questions`

Never invent repo ownership.

### 3. Resolve Canonical Context Path

Use this order:
1. explicit `follow context`
2. explicit `shared context path`
3. current repo `inter-context.md`
4. root `inter-context.md`

If none exists, initialize from `templates/inter-context.md`.

### 4. Read Canonical Context First

Load existing context before broad scanning.
Treat it as baseline state, not final truth.

### 5. Build Source Inventory and Roles

For each in-scope source, record:
- type, location, role, freshness, owner/update path
- source relationships when dependencies or ticket hierarchies matter

If role is uncertain, keep it open and avoid hard conclusions.

### 6. Apply Source-of-Truth Rules

Apply defined priority rules to key claims (schema, payload, ownership, policy, rollout).
If rules are missing, use defaults and record that default set was used.

### 7. Reconcile Multi-Source Claims

For each key claim:
- capture claims from each source
- mark status: `aligned`, `conflict`, `open`
- define working assumption for this session
- add follow-up target to close mismatch

### 8. Pause at Reconciliation Approval Gate

Before implementation:
- show context change summary/diff
- show conflicts and open questions
- show working assumptions
- set `user review status: pending`

Proceed only when user sends a valid signal:
- `proceed`
- `go ahead`
- `apply changes`
- `start implementation`

Then set `user review status: confirmed`.

If signal is ambiguous, ask for explicit proceed confirmation and do not start implementation.

### 9. Run Downstream Work After Approval

After confirmation only:
1. open `working targets` first
2. verify current repo behavior
3. verify related repos when coupling matters
4. recheck external sources only when freshness is required

### 10. Update Context in the Same Session

When facts or decisions change, update:
- source inventory freshness
- reconciliation notes
- confirmed facts/open questions
- drift watchlist
- recent decisions
- source sync status and deltas
- next handoff note

## Failure Diagnosis

1. Premature implementation
- Symptom: code edits begin before review confirmation.
- Fix: enforce step 8 and keep review status `pending`.

2. Source role confusion
- Symptom: ticket text treated as implementation fact.
- Fix: classify source roles and re-run reconciliation.

3. Truth-priority mismatch
- Symptom: conflicting sources resolved inconsistently.
- Fix: declare explicit source-of-truth rules in context.

4. External-source overfetch
- Symptom: every session reads all tickets/docs regardless of need.
- Fix: refresh only in-scope sources with freshness risk.

5. Multiple canonical contexts
- Symptom: conflicting context files in same workflow.
- Fix: choose one canonical owner path and merge deltas.

6. Drift accumulation
- Symptom: repeated rediscovery in later sessions.
- Fix: update reconciliation and handoff in same session.
