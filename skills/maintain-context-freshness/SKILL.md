---
name: maintain-context-freshness
description: Audit and safely maintain the temporal correctness of an explicitly selected context document or document set by reconciling claims with current evidence, classifying current, active, reusable, historical, superseded, and unresolved information, refreshing current-state surfaces, and proposing reversible cleanup without deleting unique evidence. Use when context contains outdated status, completed work left as pending, dated snapshots presented as current, superseded branches, versions, or decisions, resolved incidents mixed with active work, or accumulated history that obscures what matters now. Do not use to choose or initialize context storage, reorganize repository-wide documentation ownership, or merely rewrite a document for readability.
---

# Maintain Context Freshness

Maintain the temporal correctness and usefulness of an existing context target without treating age, completion, or apparent duplication as permission to discard information.

Allow high freedom in domain-specific truth judgment and low freedom in information disposal.

## Scope Boundary

Require an explicitly selected, already-existing context file or document set.

- If the canonical target, persistence location, cross-context reconciliation, or creation of new durable context is unresolved, stop and report the exact decision required; do not infer or create it.
- Do not reorganize repository-wide document ownership, layering, navigation, or duplication. Report that separate structural work is required after the freshness findings are settled.
- Do not reshape content merely for readability when the facts are already settled. Report that separate composition work is required.
- Do not create a fallback context file, archive hierarchy, or replacement document merely to satisfy this skill.
- Do not expand a freshness pass into code changes, ticket updates, or other downstream execution without separate user authority.

## Core Model

Evaluate information at claim or section level before making a file-level disposition.

Keep three axes separate:

1. `freshness status`: `aligned`, `stale`, `time-scoped`, `unverified`, or `conflict`
2. `lifecycle role`: `current`, `active`, `reusable`, `historical`, `superseded`, or `unresolved`
3. `action disposition`: `keep`, `annotate`, `refresh`, `reclassify`, `condense-and-link`, `archive candidate`, or `delete candidate`

A document may contain several lifecycle roles at once. Do not label the whole file stale merely because one current-state claim drifted.

## Operating Modes

### `audit` (default)

Inspect sources, classify claims, and produce an exact disposition report without editing the audited target.

- Start here for an unreviewed target even when the user asks generally to clean it up.
- Treat proposed actions as awaiting user review and keep that working state in the session report.
- Do not archive, delete, move, or rewrite target content.

### `maintain`

Apply an approved audit or an already reviewed, exact maintenance scope.

- Refresh current facts in the smallest owning locations.
- Add scope or `as-of` markers where they prevent present-day misreading.
- Reclassify completed or superseded material instead of erasing its provenance.
- Condense repetition only after verifying that no unique constraint, rationale, example, or evidence is lost.
- Do not archive or delete material in this mode.

### `dispose`

Archive or delete only exact source targets that the user explicitly approved after reviewing the evidence and proposed disposition. Archive approval must also name the exact destination.

- Recheck the target immediately before acting.
- Apply only the approved source target, action, and, for archive, destination.
- Treat archive moves as approval-gated because they can break discovery and links.
- If the archive destination is unresolved, do not enter this mode or move anything; report `not applied — exact archive destination required`.

## State And Persistence

Keep run-control state separate from document content.

- In `audit`, keep findings, the claim ledger, review state, and proposed actions session-only by default. Persist an audit artifact only when the user explicitly requests it and names a destination or confirms an established audit-state owner; never invent a log location.
- In `maintain`, write only approved content-state changes to the smallest owner, such as a refreshed fact, lifecycle marker, `as-of` date, or successor link. Do not write finding IDs, review state, approval status, action status, or other run metadata into target documents.
- In `dispose`, keep approval inputs and execution status in the session report. Persist only the exact approved file operation and necessary link or successor repairs; do not add approval metadata to retained documents.

## Hard Preservation Rules

- Never infer staleness from age, modification time, completion, inactivity, or apparent duplication alone.
- Preserve unknown and conflicting claims as open; do not turn missing evidence into a settled conclusion.
- Preserve historical identifiers, timelines, decisions, incident evidence, and snapshots with their original scope.
- Prefer successor links, superseded markers, and dated scope labels over rewriting history to look current.
- Never bulk-replace historical versions, branch names, commit identifiers, or observed values merely because a newer equivalent exists.
- Do not delete a working note merely because it is non-canonical or tentative.
- Do not treat a newer summary as proof that all unique detail was absorbed.
- Require exact user approval before any archive or deletion action.

## Workflow Summary

1. confirm the existing target, audit scope, requested mode, and prior review state
2. read the target's entrance and owner documents and select freshness-sensitive claims
3. prioritize the selected claims by decision consequence, then freeze a bounded initial claim and source map
4. expand only for sources that can change a named finding's disposition or confidence, recording checked and materially important unchecked sources without turning source inventory into the audit
5. assign stable finding IDs and classify each atomic claim's freshness status, lifecycle role, disposition, and confidence
6. prove preservation before proposing condensation, archive, or deletion
7. present the audit and wait for the review signal required by the mode
8. apply only the smallest approved maintenance or disposal actions
9. validate the requested mode, target outcome, evidence coverage, historical traceability, links, and remaining uncertainty

## Reference Routing

- For `audit`, read steps 1 through 8 and step 11 under [Detailed Procedure](references/method.md#detailed-procedure).
- For `maintain`, use the `audit` route, then read [Apply Maintenance Safely](references/method.md#9-apply-maintenance-safely) and only the relevant [Maintenance Patterns](references/method.md#maintenance-patterns).
- For `dispose`, use the `audit` route, then read [Disposal Proof](references/method.md#disposal-proof) and [Apply Disposal Exactly](references/method.md#10-apply-disposal-exactly).
- Read [Failure Diagnosis](references/method.md#failure-diagnosis) only when the pass encounters one of its failure signals.
- Before freshness classification, read [Universal Indicator Principles](references/indicators.md#universal-indicator-principles), [Strong Freshness Signals](references/indicators.md#strong-freshness-signals), and [Weak Or Misleading Signals](references/indicators.md#weak-or-misleading-signals), then load only the relevant domain subsection under [Cross-Domain Indicator Families](references/indicators.md#cross-domain-indicator-families).
- Use [references/checklist.md](references/checklist.md) before finalizing any audit, maintenance, or disposal pass.

## Disposal Proof Gate

Propose material as an `archive candidate` or `delete candidate` only when the report addresses the first four proof areas:

- `ownership`: the material no longer owns a current or distinct responsibility
- `coverage`: every unique fact, constraint, rationale, example, and provenance item is preserved or mapped
- `future value`: diagnostic, learning, audit, rollback, legal, research, and reproducibility value were considered
- `dependency`: inbound links, references, and successor navigation are known

In `audit`, report a candidate as `proposed only — not executed`; choosing an archive destination can wait until the user requests that action. On a `dispose` request, if any required source target, action, or archive destination is missing, report `not applied` and name the exact missing input. Use `approved` only after the exact execution inputs are authorized, and `applied` only after the action and its validation succeed. Do not use `authorization: pending` as a user-facing status.

Enter `dispose` and execute the action only after the user approves the exact source target and exact archive or delete action; archive approval must also include the exact destination. If there is no disposal candidate, omit disposal status or report `not applicable`.

If any of the first four proof areas is uncertain, preserve or reclassify the material instead of proposing disposal.

## Output Contract

Use this minimum report order:

1. operating mode, review state, resolved target, bounded scope, and effective `as-of` date or evidence window
2. sources checked, their roles, and important sources not checked
3. a compact claim ledger with stable finding IDs
4. information deliberately preserved, conflicts, unresolved questions, and working assumptions
5. proposed or applied actions plus exact delete targets and archive source targets; for archive, name the exact destination when approved or applied, or the exact missing input that prevented a requested execution
6. files changed, or an explicit no-change statement
7. `Result`, `Target Outcome`, and `Evidence Coverage`

Each ledger row must cover one atomic claim or a section whose claims share the same evidence, classifications, confidence, and disposition. Include:

- finding ID
- claim or section and evidence `as-of`
- freshness status
- lifecycle as `observed → proposed` in `audit`, or actual `before → after` in `maintain` and `dispose`
- action disposition, confidence, and concise rationale
- for material `unverified` or `conflict` findings, the source or condition needed to close the finding

Reference finding IDs from preservation, conflict, and action sections instead of repeating the full evidence and rationale.

Keep the user-facing report decision-focused:

- give ledger rows to material drift, lifecycle decisions, proposed actions, and unresolved blockers
- summarize checked sources by role; name individual files only when they own, contradict, or can close a material finding
- group routine aligned evidence and non-material checked or unchecked sources compactly
- do not add an aligned row merely to prove that a source was read
- ledger every material signal surfaced during the bounded scan, or name its explicit exclusion and why it cannot change the current decision

For validation:

- `Result` (`PASS`, `PASS WITH SUGGESTIONS`, or `FAIL`) evaluates whether the requested mode's checks and actions completed correctly; it does not grade the target's freshness.
- `Target Outcome` summarizes the material target findings or applied effects for the requested mode.
- `Evidence Coverage` (`complete`, `partial`, or `unavailable`) reports coverage of the selected material claims and their decision-required source map, not the percentage of files scanned.
- Target drift, unresolved findings, and partial `Evidence Coverage` do not by themselves lower `Result` when the requested mode completed correctly.

## Package Roles

- `SKILL.md`: trigger, modes, hard preservation rules, approval boundary, and output contract
- `agents/openai.yaml`: UI-facing display and invocation metadata
- `references/method.md`: detailed audit, maintenance, disposal, and failure-diagnosis procedure
- `references/indicators.md`: cross-domain freshness signals and false-positive guards
- `references/checklist.md`: short final yes-or-no validation
