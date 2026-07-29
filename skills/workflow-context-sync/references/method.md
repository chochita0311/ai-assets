# Workflow Context Sync Method

## Contents

- [Purpose](#purpose)
- [Behavior Model](#behavior-model)
- [Detailed Procedure](#detailed-procedure)
- [Document-Set Updates](#document-set-updates)
- [Working Notes And Session-Only Synthesis](#working-notes-and-session-only-synthesis)
- [Consolidation Procedure](#consolidation-procedure)
- [Failure Diagnosis](#failure-diagnosis)

## Purpose

This document owns the detailed execution logic for `workflow-context-sync`.

Use it to resolve the storage target independently from the session's working directory, reconcile only the sources needed for the decision, update the correct owner, and consolidate misplaced context safely.

## Behavior Model

The skill should yield:

- one explicit persistence disposition with a concise rationale
- one resolved canonical target when persistence applies, or an honest `unresolved` or session-only result
- no arbitrary context file created from `cwd`
- no new durable artifact created by an implicit invocation
- source-role-aware reconciliation
- explicit review state before downstream implementation
- low context drift across sessions

The target may be:

- a `document set` with an entrance file and specialized owner documents
- a `dedicated workflow context` created for one bounded workflow

Do not assume the second form is more canonical merely because it is one file.

## Detailed Procedure

### 1. Normalize Intake And Requested Durability

Capture:

- current goal
- working root
- current repo
- related repos when relevant
- invocation origin: `explicit` or `implicit`
- explicit context path, alias, or namespace when provided
- sources in scope
- requested durability:
  - `session-only acceptable`
  - `durable outcome requested`
  - `unspecified`
- creation authority: `granted` only when the user explicitly requested a new durable artifact; otherwise `not granted`

If the user only wants a memo, stop using this workflow as a canonical-context operation. Write only to the explicit note path the user requested.

Do not infer creation authority from the existence of a note, a plausible directory, an unambiguous namespace, or the fact that this skill was invoked automatically.

### 2. Resolve Aliases And Context Home

Apply alias mappings from active entrance instructions or explicit user direction.

Record:

- original token
- resolved absolute path
- mapping source
- status: `confirmed` or `open`

Never invent an alias or context home from common local folder names.

### 3. Resolve The Canonical Target

Use this order:

1. explicit target file
2. explicit document-set directory
3. explicit alias plus namespace
4. mapping recorded by an existing context entrance or context map
5. a single existing candidate inside an explicitly resolved context home

For a directory candidate:

1. inspect its entrance files such as `README.md`, `AGENTS.md`, `CLAUDE.md`, `index.md`, or a numbered overview
2. identify the document ownership map
3. determine whether the current workflow already has an owning document
4. classify the target as a document set or a dedicated workflow context

Do not:

- fall back to `<cwd>/inter-context.md`
- fall back to `<current-repo>/inter-context.md`
- fall back to `<workflow-root>/inter-context.md`
- select by repository basename alone when several namespaces could match
- treat a memo, rough note, or context-like filename as a target mapping
- create a sibling context artifact beside a note

If the target remains ambiguous, report candidate paths and continue only with session-only reconciliation until the user chooses.

### 4. Assess Persistence

Choose one disposition after checking for an existing target and before writing:

1. `session-only`
   - Prefer this for one-off analysis, tentative synthesis, easily reconstructed findings, or work with no expected handoff.
   - State why session-only handling is sufficient.
   - Do not create an artifact or ask for a target.
2. `maintain existing`
   - Choose this when an existing canonical target is resolved and durable facts, decisions, freshness, or handoff state changed.
   - Do not rewrite the target merely to record that it was inspected.
3. `propose persistence`
   - Choose this when no target exists and the result is expected to survive the session because it coordinates multiple sources, closes repeated rediscovery, records a durable decision, or supports a future handoff.
   - State the material that merits persistence, why session-only handling may be insufficient, and a proposed target and target kind.
   - Keep the current result session-only until approval.
4. `initialize after approval`
   - Choose this only after explicit creation approval and target resolution.

If the user's requested outcome explicitly requires durable storage and no target exists, ask for approval of the proposed target and kind. If persistence is only beneficial, make a non-blocking recommendation in the result instead of interrupting the task.

### 5. Choose The Operating Mode

- use no write mode for `session-only`
- choose `maintain` for `maintain existing`
- keep persistence pending for `propose persistence`
- choose `initialize` only for `initialize after approval`
- choose `consolidate` when multiple artifacts cover the same workflow and a canonical target has been selected

Implicit invocation must not select `initialize`. If it cannot resolve an existing canonical target, keep the result session-only and report the missing target decision without creating an artifact.

### 6. Read Canonical Context First

For a document set:

- read the entrance map first
- read only owner documents relevant to the current goal
- treat the set as baseline state, not automatically current truth

For a dedicated workflow context:

- read the file before scanning other sources
- preserve its source inventory, decisions, and handoff unless newer evidence supersedes them

### 7. Build The Source Inventory

For each source needed for the current decision, record:

- id
- type and location
- role
- freshness
- owner or update path
- source relationships when dependencies matter

Supported roles:

- `implementation truth`
- `authoritative spec`
- `planned work`
- `operational signal`
- `working note`
- `historical note`

Avoid broad external refresh when existing evidence already decides the current question.

### 8. Reconcile Claims

For each important claim:

- capture the relevant source statements
- apply the claim-domain source-priority rule
- mark `aligned`, `conflict`, or `open`
- record the current working assumption
- name the follow-up owner that can close any mismatch

Do not blend conflicting sources into an apparently settled summary.

### 9. Update The Canonical Target

If the target is a document set:

- update the smallest document that owns each durable fact
- update the entrance map only when navigation or current-status routing changed
- avoid creating a catch-all context file beside existing owner documents
- use `docs-structuring` only when the document set itself has an ownership problem

If the target is a dedicated workflow context:

- update the source inventory, reconciliation notes, decisions, drift watchlist, sync status, and handoff
- keep temporary investigation detail out unless it affects future decisions

If no existing target is resolved:

- create a new artifact only in `initialize` mode with explicit creation authority
- do not copy a template or emit a placeholder file simply because the skill was invoked

If persistence is unresolved:

- do not write a provisional local file
- return the reconciliation in the session and identify what target decision is missing

### 10. Present Reconciliation Before Downstream Work

Show:

- requested durability, persistence disposition and rationale, and operating mode when applicable
- invocation origin and creation authority
- proposed target and kind when persistence is recommended
- resolved target and target kind
- context changes or delta summary
- conflicts and open questions
- working assumptions
- files updated
- user review status

Keep review status `pending` until the selected approval mode permits downstream work.

### 11. Continue After Approval

After confirmation:

1. open the recorded working targets
2. verify current repo behavior
3. verify related repos only when coupling matters
4. recheck external sources only when freshness is required
5. perform only the separately requested downstream task

The approval gate does not silently authorize unrelated implementation.

### 12. Refresh Context In The Same Session

When downstream work changes facts or decisions, update the canonical target before closing:

- confirmed facts and open questions
- recent decisions
- drift watchlist
- source freshness and deltas
- next handoff

## Document-Set Updates

A document set is often the better canonical target when:

- an entrance document already maps the domain
- specialized files own architecture, operations, incidents, or feature context
- the user has intentionally organized context by topic or path

In this mode, canonicality belongs to the ownership system, not to one filename. Preserve the established structure and update only the owning files.

## Working Notes And Session-Only Synthesis

A `working note`:

- may be stored inside a context home
- remains tentative or personal
- is not automatically read on every workflow
- may be promoted only through explicit reconciliation
- does not designate its directory or a sibling file as the canonical target
- may later be reconciled as source evidence but must never be promoted silently

A `session-only synthesis`:

- is useful when source reconciliation is needed but persistence is not
- stays in the session response
- must not be described as a saved canonical context

Do not use `inter-context.md` as a generic notepad.

When implicitly invoked around a working note, use it as source evidence. Update an existing predesignated canonical target only when maintenance is in scope; otherwise return a session-only synthesis and create nothing.

A memo-only request should use ordinary file writing at the user's explicit path rather than this canonical-context workflow.

## Consolidation Procedure

Use `consolidate` when context was written to the wrong location or several candidates overlap.

1. identify and confirm the canonical target
2. inventory every candidate without editing
3. compare unique facts, decisions, provenance, open questions, and freshness
4. merge only supported material into the owning canonical artifacts
5. classify each candidate:
   - `keep`: still owns distinct material
   - `archive`: useful history but no longer active
   - `delete candidate`: fully absorbed temporary or misplaced artifact
6. show the exact disposition list
7. archive or delete only after explicit approval for those targets
8. rerun link and entrance-map checks after cleanup

Never delete a working note merely because it is not canonical.

## Failure Diagnosis

### Arbitrary Context Creation

- Symptom: a new `inter-context.md` appears under the session root or current repo.
- Cause: working location was treated as storage authority.
- Fix: remove the cwd fallback, resolve context home and target, then use `consolidate`.

### Mature Context Flattened Into One File

- Symptom: an existing domain document set gains a competing catch-all context.
- Cause: dedicated-file format was assumed to be universal.
- Fix: restore the entrance and specialized owner documents as the canonical target.

### Memo Promoted To Truth

- Symptom: tentative notes appear under confirmed facts or source-of-truth rules.
- Cause: artifact role was not classified before persistence.
- Fix: relabel the note as a source and reconcile its claims explicitly.

### Dummy Context Created Beside A Note

- Symptom: a placeholder or thin `inter-context.md` appears because a memo or context-like note was discovered.
- Cause: source discovery was mistaken for target selection and creation authority.
- Fix: remove the inferred target rule, keep the note as source evidence, and require an explicit creation request before entering `initialize`.

### Repeated Rediscovery

- Symptom: sessions scan all sources again despite current local context.
- Cause: canonical target was not read first or freshness was not recorded.
- Fix: load the target first and refresh only sources needed for the current decision.

### Unsafe Cleanup

- Symptom: temporary-looking files are deleted immediately after a merge.
- Cause: consolidation disposition was not separated from destructive cleanup.
- Fix: produce an exact keep/archive/delete-candidate list and wait for approval.
