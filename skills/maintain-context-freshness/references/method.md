# Maintain Context Freshness Method

## Contents

- [Purpose](#purpose)
- [Behavior Model](#behavior-model)
- [Detailed Procedure](#detailed-procedure)
- [Disposal Proof](#disposal-proof)
- [Maintenance Patterns](#maintenance-patterns)
- [Failure Diagnosis](#failure-diagnosis)

## Purpose

Own the detailed procedure for auditing and safely maintaining the temporal correctness of an already-selected context target.

Keep current surfaces concise and useful while retaining the evidence layer needed for learning, diagnosis, audit, rollback, and future reinterpretation.

## Behavior Model

Produce a claim-level freshness judgment before changing document structure or removing information.

The normal flow is:

```text
current sources and existing context
              ↓
       read-only freshness audit
              ↓ user review
      minimal context maintenance
              ↓ separate exact approval
       archive or delete disposal
```

Do not make domain truth rules universal. Standardize the evidence process, lifecycle vocabulary, preservation requirements, and approval gates instead.

## Detailed Procedure

### 1. Confirm Target And Authority

Capture:

- exact existing file or document-set path
- requested scope
- requested mode: `audit`, `maintain`, or `dispose`
- whether a comparable audit was already reviewed
- user exclusions and protected areas
- sources the user expects to be considered
- current working date and relevant evidence window

If the target is missing, ambiguous, or would need to be newly created, do not infer a location. Return a session-only unresolved finding that names the exact target or persistence decision the user must supply.

Do not treat the current repository, process working directory, or a nearby note as storage authority.

### 2. Read The Context Surface First

For a document set:

1. read the entrance or status document
2. identify the smallest current-state owners
3. identify known historical, reference, incident, decision, and runbook areas
4. note explicit source-of-truth and scope statements

For one document:

1. identify its purpose and audience
2. separate present-tense claims from dated evidence and reusable explanation
3. note linked owners and successors

Treat the target as the baseline representation, not as automatically current truth.

### 3. Select Freshness-Sensitive Claims

Prioritize claims that can change the user's next decision:

- current status, pending work, next steps, blockers, and owners
- branch, version, release, deployment, configuration, and runtime assertions
- issue, pull request, incident, decision, policy, or approval state
- time-limited snapshots presented without a date or scope
- resource names, paths, links, commands, identifiers, and dependencies
- statements that one artifact is canonical, active, complete, or safe to remove

Order the selected claims by consequence:

1. destructive, irreversible, access-affecting, recovery, or operational-safety claims
2. current status, next action, ownership, and preservation decisions
3. unresolved material claims that have an accessible closure source
4. routine aligned background only when it bounds or explains a material decision

Before broad refresh, freeze an initial working map of the selected claims and the sources most likely to decide them. Later evidence may split a claim or add a directly coupled source, but it must not silently turn the audit into an inventory of every linked artifact.

Do not spend equal effort on stable explanations, timeless concepts, or clearly dated historical observations unless new evidence directly challenges them.

Split compound statements when their evidence, freshness status, lifecycle role, confidence, or disposition differs. Aggregate a section only when all material claims in it share those fields. Keep high-stakes and conflicting claims atomic even when they appear in one paragraph or table.

For resources and pipelines, distinguish existence or declaration, configuration, deployment, population or ingestion, and actual consumer use whenever the evidence for those states differs.

### 4. Build A Decision-Relevant Source Map

For each important claim, record only the sources needed to decide it:

- source and location
- source role for this claim
- observation or statement
- effective date or observation window
- authority and known limitations
- checked, inaccessible, or intentionally not checked

Choose priority per claim domain. Examples:

- implementation can decide what code exists but not whether it is deployed
- runtime evidence can decide observed behavior but not whether a ticket is formally closed
- a ticket can decide workflow status but may lag implementation or production
- user confirmation can establish an observed operational fact within its stated scope but must not silently settle unrelated formal states
- plans express intent and expected work, not completed reality
- historical notes prove what was known at a time, not what remains true now

Avoid refreshing every linked external source. Refresh only what can change the disposition or confidence of a material claim.

Before opening an additional source, name the existing finding or prospective material claim it could affect and how it could change the disposition or confidence. If that impact cannot be stated, do not open the source merely to increase coverage.

Check directly coupled sources when a selected claim makes their consequence material:

- when storage, configuration, identifiers, permissions, or dependencies drift, check the directly affected destructive, reprocessing, rollback, or recovery procedure
- when completion or current status changes, check an accessible entrance-linked check-in, result, achievement, or status owner that could close the finding
- when the target defines a freshness, retention, disposal, or age-based cleanup rule, compare that rule with this skill's hard preservation and proof requirements and report any conflict

When the target contains the policy, skill, checklist, or process that defines its own audit, do not count its self-description as independent quality evidence. Use separate owner guidance, version history, validation results, runtime evidence, or reviewed decisions where available. If independent evidence is unavailable, keep the claim `unverified` rather than failing it merely for being self-referential.

### 5. Evaluate Claims On Three Axes

Assign one freshness status:

- `aligned`: supported for the claimed current scope
- `stale`: presented as current but contradicted by stronger or newer relevant evidence
- `time-scoped`: valid for a named period or snapshot but not a current assertion
- `unverified`: important but not checked or not decidable from available evidence
- `conflict`: relevant sources disagree and authority is not sufficient to close the mismatch

Choose the status in this order:

1. normalize whether the claim asserts current truth or a named historical window
2. use `time-scoped` only when a dated claim remains valid for that stated window and is not presented as current
3. use `stale` when a current claim is directly contradicted by stronger relevant evidence
4. use `conflict` when relevant sources disagree and authority or scope cannot close the mismatch
5. use `unverified` when a material current claim cannot be decided because required evidence was not checked or is unavailable
6. otherwise use `aligned` for the claimed scope

Do not let a time-scoped parent label settle its child claims. For example, an expired schedule heading may need reclassification while the actions beneath it remain active or unverified. Likewise, narrow completion evidence does not close a broader task or responsibility; split the scope first.

Assign one lifecycle role:

- `current`: present truth or current contract
- `active`: unfinished work, open action, blocker, or watch item
- `reusable`: durable learning, procedure, reference, or explanation
- `historical`: dated evidence, timeline, prior observation, or completed record
- `superseded`: replaced by a successor while retaining decision or provenance value
- `unresolved`: uncertainty or conflict that must remain visible

Assign one action disposition:

- `keep`
- `annotate`
- `refresh`
- `reclassify`
- `condense-and-link`
- `archive candidate`
- `delete candidate`

Record confidence:

- `high`: authority and evidence agree; preservation impact is understood
- `medium`: best-supported disposition is clear but one material limitation remains
- `low`: sources, scope, ownership, or future value remain ambiguous

Do not propose disposal for low-confidence findings.

In `audit`, record lifecycle as `observed → proposed`; the right-hand value is a recommendation, not an applied transition. In `maintain` and `dispose`, record the actual `before → after` state after the approved action. If no lifecycle change is proposed or applied, say `no transition` rather than implying one.

For each material `unverified` or `conflict` finding, name the source type, owner, or observation needed to decide it and the condition that would close the finding. This is a closure path, not authority to broaden the audit or access an external system.

### 6. Build The Audit Ledger

Use a compact working ledger:

| ID | Atomic claim or section | Evidence and as-of | Freshness | Lifecycle transition | Disposition | Confidence | Reason or closure path |
|---|---|---|---|---|---|---|---|

Keep the ledger, finding IDs, review state, and proposed-action state session-only by default. Persist an audit artifact only when the user explicitly requests it and names a destination or confirms an established audit-state owner. Never infer a log path from the target, current directory, or a nearby context file.

In `maintain`, persist only approved content-state changes in the smallest owning document, such as refreshed facts, lifecycle markers, `as-of` dates, and successor links. Do not insert finding IDs, review state, approval status, action status, or other run metadata merely to record that maintenance occurred.

In `dispose`, keep approval inputs and execution status in the session report. The approved file operation and necessary link or successor repairs are the only persisted effects.

Group the user-facing report into:

- safe current-state refreshes
- active items that must remain visible
- reusable material to preserve
- historical or superseded material to relabel
- unresolved conflicts
- archive or delete candidates awaiting approval

Reference ledger IDs from these groups instead of repeating their full evidence and rationale.

### 7. Apply The Decision-Sufficient Stop Condition

Stop expanding a document-set audit when every selected material claim has:

- a current owner or owning surface
- the strongest decision-relevant source that is accessible within scope
- freshness, lifecycle, disposition, and confidence classifications
- any important unchecked blocker and closure path
- no accessible unchecked source that is likely to change its disposition or confidence
- no unchecked destructive, reprocessing, rollback, recovery, or status-closure procedure directly coupled to its consequence

Every material signal surfaced during the bounded scan must be in the ledger or have an explicit exclusion explaining why it cannot change the current decision. Then finalize immediately: group routine aligned evidence and non-material source inventory instead of continuing to expand the report. List excluded areas explicitly. Do not claim whole-target completeness merely because this stop condition was met.

Use the frozen selected-claim and source map as the audit denominator, not the number of files in the target tree. Do not scan every document or run a post-stop completeness sweep unless the user explicitly requested exhaustive coverage.

### 8. Enforce The Review Gate

The default review mode is strict.

- In `audit`, stop after presenting the report.
- Enter `maintain` only after the user approves the audit or provides an exact previously reviewed scope.
- Enter `dispose` only after the user approves exact source targets and actions from a reviewed disposition list, plus exact destinations for archive actions.

A broad request such as "clean stale context" authorizes the audit, not irreversible disposal.

### 9. Apply Maintenance Safely

In `maintain`:

1. reread each owning target immediately before editing
2. update present-tense facts in the smallest current owner
3. separate genuinely active work from optional evidence collection and completed history
4. add dates, scopes, or successor links where present-day misreading is likely
5. preserve original observations and identifiers inside clearly historical material
6. condense only verified repetition
7. update entrance navigation only when current routing changed

Do not create a new archive folder, split files, or redesign navigation merely because historical content exists. Suggest such restructuring first unless the user already approved it.

When ownership or composition becomes the dominant problem, stop freshness expansion and report the settled disposition plus the separate structural or composition work required. Do not perform that adjacent work under this skill.

### 10. Apply Disposal Exactly

In `dispose`:

1. resolve every approved source target and, for archive, destination literally
2. verify that the source target has not changed materially since the audit
3. rerun the disposal proof
4. archive or delete only the approved source target, action, and, for archive, destination
5. repair affected links and successor navigation
6. report what was removed or moved and whether recovery is possible

Do not extend approval from one file to siblings, generated matches, glob results, or similar-looking content.

### 11. Validate The Result

For every mode, confirm:

- reusable learning and operational guidance remain discoverable
- historical and superseded material retains provenance and scope
- unresolved conflicts remain explicit
- links and owner pointers checked within scope remain valid

Then validate the requested mode:

- `audit`: the report enables a safe next decision, identifies unchecked blockers, makes no target changes, and leaves every action pending review
- `maintain`: current entry surfaces no longer present the approved stale claims as current, active work remains distinguishable from completed history, and no unique information disappeared during condensation
- `dispose`: the exact approved source targets, actions, and archive destinations were applied, dependency repairs were checked, and recovery status was reported

Report three separate fields:

- `Result`: whether the requested mode completed correctly for the checks and actions actually performed
  - `PASS`: the mode contract completed without a material execution or validation issue
  - `PASS WITH SUGGESTIONS`: the mode completed safely, but non-blocking process or validation improvements remain
  - `FAIL`: the mode could not complete safely or a performed action failed its validation
- `Target Outcome`: the material drift, unresolved evidence, proposed maintenance, applied maintenance, or disposal effects found for the target
- `Evidence Coverage`: coverage of the selected material claims and their decision-required source map
  - `complete`: every decision-required source was checked and no material unchecked source could change a disposition or confidence level
  - `partial`: useful evidence was checked, but at least one material source or scenario remains unchecked
  - `unavailable`: required evidence could not be accessed or was insufficient to evaluate the material claims

Target drift is a normal audit finding and does not by itself make `Result` fail. Evidence coverage is not the percentage of files read in the target tree.

Calibrate `Result` against execution quality as well as safety:

- if the user or supervising agent had to correct scope expansion or force finalization, report no better than `PASS WITH SUGGESTIONS`
- use `FAIL` when the report cannot support a safe next decision, a material selected claim is omitted without disclosure, or an applied action fails validation
- do not use `PASS WITH SUGGESTIONS` solely because target drift or unresolved findings exist or `Evidence Coverage` is `partial`; report those conditions in their own fields
- do not downgrade `Result` for an unrelated transport or platform interruption when the mode contract itself still completed and the interruption did not hide material evidence

## Disposal Proof

### Ownership Proof

Confirm that the target no longer owns:

- a current fact or contract
- a distinct operational procedure
- an unresolved question or active action
- a unique decision rationale
- a required entry or navigation role

### Coverage Proof

Compare the candidate against its proposed successor or retained material.

Account for:

- unique facts and constraints
- exceptions and force words
- examples that encode rules
- identifiers, timestamps, and evidence references
- source provenance and confidence
- decision and failure rationale

A summary that preserves the conclusion but drops the reasoning is not full coverage.

### Future-Value Proof

Consider whether the material supports:

- incident diagnosis or recurrence prevention
- audit, compliance, or accountability
- rollback and recovery
- learning and onboarding
- research reproducibility
- interpretation of later decisions

If future value is plausible and cheap to preserve, prefer historical classification or archive candidacy over deletion.

### Dependency Proof

Identify inbound links, references, indexes, automation, and human navigation that depend on the target.

Do not infer that no dependency exists merely because repository search found no literal path.

### Authorization Proof

Record the exact approved source path or section and whether the action is archive or delete. For archive, also record the exact approved destination.

In an audit report, label a candidate `proposed only — not executed`; an archive destination does not need to be chosen until the user requests the move. On a `dispose` request, if the exact source, action, or archive destination is unresolved, do not enter the mode; report `not applied` and name the exact input the user must supply.

Do not expose `authorization: pending` as a user-facing status. Use `approved` only after all exact execution inputs are authorized, and use `applied` only after the action and its validation succeed. If there is no disposal candidate, omit disposal status or report `not applicable`.

Approval for maintenance is not approval for disposal. Approval for one target is not approval for a similar target.

## Maintenance Patterns

### Completed Work In A Pending List

- refresh the current fact
- retain only genuinely open follow-up as `active`
- move or condense implementation chronology into a historical owner when one already exists
- preserve reusable validation or rollback guidance

### Rebased Or Superseded Version Evidence

- update current branch or version references in current-state owners
- retain old identifiers in historical evidence
- add an old-to-new mapping when it materially supports traceability
- do not globally replace identifiers

### Resolved Incident

- change current impact and mitigation state to resolved
- keep root cause, timeline, evidence, rollback, and lessons as historical or reusable
- keep unfinished preventive actions active with owners or tracking references

### Dated Investigation Snapshot

- add the observation date, source set, and intended decision scope
- distinguish the snapshot from current implementation or runtime truth
- retain methodology and evidence needed for reproduction

### Superseded Decision Or Policy

- preserve the original context and rationale
- mark the state as superseded
- link the successor and effective date
- avoid editing the old decision as though the newer decision had always applied

## Failure Diagnosis

### Age-Based Purge

- Symptom: old files or sections are treated as stale without claim verification.
- Cause: modification time was mistaken for semantic freshness.
- Fix: evaluate present-tense claims and lifecycle value separately from age.

### Whole-File Staleness

- Symptom: one drifted status line makes an entire incident, runbook, or research file a deletion candidate.
- Cause: freshness was classified at file level first.
- Fix: classify claims and sections before file disposition.

### History Rewritten As Current

- Symptom: old identifiers, observations, or decisions are replaced everywhere with new values.
- Cause: current-state maintenance was applied to historical evidence.
- Fix: update current owners and preserve dated history with mappings or successor links.

### Unknown Treated As Obsolete

- Symptom: inaccessible or unchecked material is removed as stale.
- Cause: absence of verification was mistaken for contradiction.
- Fix: mark it `unverified` or `unresolved` and name the source needed to decide it.

### Partial Consolidation Loss

- Symptom: a concise summary remains but caveats, examples, or rationale disappear.
- Cause: conclusion-level equivalence was mistaken for full coverage.
- Fix: rerun coverage proof and restore or map unique information.

### Freshness Scope Explosion

- Symptom: every linked source is refreshed regardless of decision impact.
- Cause: completeness was pursued without a bounded audit question.
- Fix: freeze the initial claim and source map, apply the source-impact gate, and finalize as soon as the decision-sufficient stop condition is met.

### Premature Sufficiency

- Symptom: the report is polished but omits a consequential procedure, accessible closure source, or material signal already surfaced during the bounded scan.
- Cause: brevity or an early stop was treated as more important than consequence coverage.
- Fix: check directly coupled consequential sources, ledger every surfaced material signal or its explicit exclusion, and only then compact routine aligned evidence.

### Compound Claim Collapse

- Symptom: one ledger row contains several claims with different evidence, statuses, or lifecycle roles.
- Cause: a paragraph, table, or checklist heading was treated as one semantic unit.
- Fix: split atomic claims first; for resources and pipelines, separate declaration, configuration, deployment, population or ingestion, and actual use; aggregate only claims with the same evidence basis and classifications.

### Result Referent Drift

- Symptom: one run uses `Result` for audit quality while another uses it to grade target freshness.
- Cause: execution validation and target outcome were collapsed into one field.
- Fix: use `Result` for the requested mode, `Target Outcome` for the context findings or effects, and `Evidence Coverage` for the source-map denominator.

### Target And Persistence Blur

- Symptom: the freshness pass creates a new context or archive location without user choice.
- Cause: content maintenance was confused with storage authority.
- Fix: stop and request an explicit target or persistence decision without creating or inferring a location.
