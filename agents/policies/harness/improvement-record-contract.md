# Improvement Record And Exchange Contract

## Contents

- [Scope And Owners](#scope-and-owners)
- [Public Record Placement](#public-record-placement)
- [Record Format](#record-format)
- [State And Evidence Semantics](#state-and-evidence-semantics)
- [Export To The Common Source](#export-to-the-common-source)
- [Import And Local Use](#import-and-local-use)
- [Feedback And Revision](#feedback-and-revision)
- [Version Changes And Consolidation](#version-changes-and-consolidation)

## Scope And Owners

Use **Improvement Record v1** as the common improvement and exchange unit for
harness, skill, resource, design, UX and runtime/tool/environment experience.
Asset differences belong in subjects, applicability and domain checks; they do
not create separate record or transport formats.

The [Harness Improvement policy](harness-improvement.md) owns observed application,
comparison, privacy, authority and return rules. This contract owns the record's
format, identity, state meanings and export/import admission. The
[schema](../../schemas/improvement-record.schema.json) defines metadata shape;
the [template](../../templates/harness-improvement-record.md) defines its body.
The [operation](../../operations/harness-improvement.md) performs the lifecycle.

| Artifact | Canonical responsibility |
|---|---|
| Private stage, comparison and original artifacts | Original observations, comparisons and actual outputs at the authorized private evidence owner |
| Private improvement record | Reusable conclusions, improvement work and exchange identity at the consumer's local owner, by default `docs/evidence/improvements/` under the [store policy](harness-improvement.md#consumer-evidence-layout); link original evidence instead of copying it |
| Public improvement record | One canonical file under `evidence/agents/<component>/` or `evidence/skills/<component>/` in ai-assets, following the placement rules below; owns generalized experience, reusable pending work, evidence limits and its revision history |
| Public catalog/private index | Discovery of the same logical record collection, with no independent work state or separate format; `evidence/README.md` lists public records across subject domains |
| Feature/spec/run/evaluation | Actual execution and acceptance at the existing task owner, linked when they exist |
| Adopted instruction or resource | Its policy, role, flow, operation, profile, template, skill or design/interaction owner; a record is not a second rule authority |

Create a record only for a reusable improvement question, supported experience
or retained maintenance need. Ordinary work need not create one. Product-only
bugs and UI/UX requests keep their existing project planning/heuristic owner;
create a common improvement candidate only when an asset-level lesson or need
is justified. The agent fills the record from evidence; no operator form is
required. Unknown facts stay unknown with reasons.

## Public Record Placement

Use the repository-level `evidence/` layer, separate from reusable asset
packages and adopted instructions. Choose the subject domain and component
from the improvement subject and responsible asset owner, not the role that
performed the observation. A folder identifies
the question's owner; it does not establish a cause or a measured effect.

| Subject owner | Public record path relative to ai-assets |
|---|---|
| Harness role, flow, operation, policy, profile, template, adapter or review asset | `evidence/agents/<component>/<record>.md` |
| Skill, skill resource or shared skill-maintenance concern | `evidence/skills/<component>/<record>.md` |

Use a descriptive component name: for example `fix-agent`, `workflow`,
`design-evaluation`, `interaction-evaluation` or `harness-improvement` under
`evidence/agents/`, and `refine-skill` or `gh-review-pr` under `evidence/skills/`.
`harness-improvement` is the subject when improving the collection/comparison/
exchange procedure itself; it is not a container for every asset's records.
Keep the full logical subject keys in metadata. Qualify an ambiguous component
name by its owning kind rather than combining unrelated owners.

For one question spanning assets, choose its primary responsible owner or a
named shared concern, retain every relevant subject and explain that ownership
in Context And Applicability. Shared skill concerns may use `documentation`,
`skill-distribution`, `skill-benchmark` or `skill-discovery`. Keep one record;
use related IDs for independent questions instead of copying an event into
several component folders and counting it as new evidence. Resolve unclear
ownership before placing a new public record.

The [common catalog](../../../evidence/README.md) discovers this collection
across `agents/` and `skills/` subject domains. Query the collection across
domains when matching IDs, subjects, questions or contrary evidence. IDs are
unique throughout `evidence/`. A missing catalog row is not proof that a record
is absent: inspect the actual files before adding or admitting an ID.
The catalog projects each record once; it owns no work state or rule authority.
Do not create separate domain catalogs or follow-up lists. The evidence layer
is repository maintenance material, not an installable skill or harness role;
selecting a record does not install its subject asset.

Create component directories only when a record needs them. There is no
intermediate `records/` directory, required empty component tree or legacy alias.
For an authorized move, preserve the stable ID and meaningful content, reconcile
links and the common catalog, and remove the old copy. A path-only move with
identical bytes retains content revision; changed links or history increment it
under the ordinary content-change rule. Record source/rendered paths and hashes
in exchange provenance; a relocated file is not a new observation.

## Record Format

A record is one UTF-8 Markdown file with **JSON front matter**: an opening line
`---`, one JSON object, a closing line `---`, then its narrative. JSON is used
so metadata can be read without a YAML-specific parser. No comments, duplicate
keys or trailing commas are allowed. Use the supplied schema; unknown fields,
unsupported schema versions, invalid values or missing required sections fail
admission before writing a shared or installed record. Preserve the input and
report the incompatibility; do not guess or silently discard fields.

`schema_version` identifies this format, `revision` identifies this record's
content, and each subject's source revision/fingerprint identifies an asset.
They are different identities. A record's source/rendered file hashes and the
shared checkout commit belong to the exchange receipt/import manifest, not a
self-referential hash field inside the record.

| Metadata | Meaning |
|---|---|
| `format`, `schema_version` | `ai-assets-improvement-record`, integer `1` |
| `record_id`, `revision`, `audience` | Stable logical identity, positive integer content revision, `private` or `public` |
| `subjects[]` | Kind and logical asset key; source Git commit and content SHA-256 when known/applicable, otherwise null with the reason in the body; other package/model/runtime versions belong in the evidence narrative |
| `work` | Basis, work state and readiness; records next work independently of knowledge or adoption |
| `knowledge.state` | Whether a reusable conclusion is unassessed, a candidate, supported, superseded or withdrawn |
| `evidence` | Disclosed evidence kinds, maturity, execution and coverage; mixed evidence is qualified by component/trial in the body |
| `adoption` | Public-fitness review, case acceptance and normative adoption as separate states |
| `relations` | Related and superseded record IDs in the same audience; public records must not expose private IDs |

Required narrative sections, in order:

1. **Context And Applicability:** problem, purpose/cue, target and current owner,
   eligibility and exclusions, preserved problem structure and changed conditions.
2. **Evidence And Evaluation:** original evidence or explicit absence, actual
   application/source/import/installed identities when known, requested/observed
   actors and conditions, Result/Coverage, per-edit effects, controls,
   counterevidence, generalization and verification limits. Link the existing
   evidence owner; do not invent a run for planned work. State `not assessed`
   without a comparison. Public accounts expose only reviewed public evidence.
3. **Work And Acceptance:** bounded next action, required checks and successful/
   regression controls, trigger/date/dependencies, action authority and budget,
   readiness/block reason, active task/performer only if established, and closure
   conditions. Preserve task-specific predicates verbatim where needed.
4. **Outcome And Reuse:** actual result or pending state, supported lesson or
   none, confidence/reasons, remaining work, revisit/withdrawal conditions and
   actual source-change/publication/refresh/activation observations separately.
5. **History:** dated content revisions, evidence added or corrected and why,
   supersession/withdrawal and preserved earlier observations. A newly migrated
   entry does not become a newly executed observation.

These sections retain the complete six-field follow-up meaning: identity/owner,
reason/evidence, next action/criteria, eligibility/authority/budget, actual work
state and resolution/evidence retention. Static shape checks cannot establish
meaning preservation, public fitness, evidence truth or runtime improvement.

## State And Evidence Semantics

- `work.state` owns the improvement effort, not a product run's status. An open
  investigation may have `knowledge.state: not-assessed` and no execution.
  An active task requires an actual task reference and authority. A resolved
  work item needs its completion evidence or a deliberate no-change reason;
  unmet runtime, discovery, stability or installation checks remain open.
- Readiness is assessed from applicability, dates/events, dependencies, evidence,
  authority and budget. Import, a due date and recurrence alone authorize no
  execution. `not-assessed`, `waiting` and `blocked` cannot be treated as ready.
- A supported lesson may coexist with open work for another condition. A closed
  item need not establish a lesson. Case acceptance does not adopt a rule.
  Preserve the policy's separate effect, maturity, coverage and disposition axes.
  `candidate` can describe a provisional hypothesis; identify whether it is
  untested or evidence-backed with pending scope/owner review. `supported`
  requires evidence and current applicability. Knowledge and work live in this
  record; original outputs and comparisons stay with their evidence owners.
- Evidence metadata describes the disclosed evidence, not successful parsing of
  this file. `mixed` execution must identify which parts ran and which did not.
  Declared historical evidence stays declared; migration/import adds no support.
  An illustrative synthetic scenario remains `not-run` until actually run.
- Record resolution retains the record and necessary evidence. Work selection
  filters `work.state: open` or `active` from the common collection; closed
  records remain available for knowledge reuse and historical review.
  Supersession records the relationship and reason instead of erasing a contrary
  outcome. An uncommitted history edit is not a commit or publication.

## Export To The Common Source

1. **Select and normalize privately.** Apply the active request's categories,
   time range and commonization/case-only/review-only scope. Convert the reusable
   portion of an existing task, observation or comparison into this format
   at the authorized private staging owner. No legacy-history backfill is needed.
   Resolve the actual common checkout, affected asset owners and current public
   record across the evidence layer before writing. Resolve its placement under
   the subject owner. If unavailable, keep the candidate private/session-only.
2. **Reconstruct the public projection.** Assign a separate public ID for a
   private origin, or use its already-linked public ID. Keep that association,
   private identities, private-source paths/hashes/traces and confidential context only
   on the private side. Review credentials, personal/company facts, metadata and
   revealing relationships as well as strings. Preserve the problem, predicates,
   evidence/counterevidence and limits. If privacy or meaning cannot be retained,
   hold locally; do not stage unresolved private content in ai-assets.
3. **Check public admission.** Require valid format/schema/body, a standalone
   account and `adoption.public_fitness: approved` based on actual semantic
   review. Other states are not public-source admission. State what is synthetic,
   generalized private observation or actual public execution. Changed inputs
   do not inherit private outcomes. An unresolved task is allowed when its basis
   and limits are truthful; do not label it a validated lesson.
4. **Match and reconcile.** Match public ID, subjects, problem and applicability.
   New items start at revision 1. For an existing ID, capture its revision and
   exact source hash, reread immediately before replacement and stop on drift.
   Identical content is a no-op. Reuse existing IDs and filenames; append new
   independent support/counterevidence, correct or narrow claims with reasons,
   and increment revision for any record-content change. Same revision with
   different source bytes is a conflict. A materially different predicate may
   use a new related ID; a copied event never counts as independent evidence.
5. **Write the bounded common result.** Store the record at its resolved
   component path, then reconcile the common catalog/index. A failure partway through
   leaves a reported partial write; resume from the saved record and its identity.
   Commonization may update reusable pending work and separately authorized
   owned rules. Case-only export updates reference/evidence content and its
   catalog entries, not work assignments/readiness/closure or normative rules;
   use `work.state: not-applicable` for a new reference-only record. A review-only
   request writes nothing to the common source. No eligible item is a valid no-op.
6. **Receipt and distribution.** At the private owner, retain the public ID,
   new revision/source hash, expected prior revision/hash, decision and exact
   committed source or uncommitted candidate identity. If no private owner is
   configured, report session-only receipt and its gap. Do not force a ledger.
   Commit/push, consumer refresh and observed use remain separate authorized acts.

## Import And Local Use

Select the capability before wildcards. Import its complete core; select public
records separately by ID with a declared purpose of **reference** (default) or
explicit **work-candidate**. A reference supports bounded inspection; only supported,
currently applicable knowledge can guide reuse within existing rules. A work
candidate is an investigation/improvement proposal, not an adopted instruction
or an automatically scheduled task. Selection may be narrowed by subject type.
Never infer selection of all records, all pending work or private original data.

Admission and write order:

1. Resolve source and destination, exact selection and purpose. Require an
   attributable committed source for an accepted installed manifest; dirty
   candidates can be reviewed/prepared but must not be attributed to HEAD.
2. Check format version, metadata/body, unique IDs/locations across the evidence layer,
   public audience and approved public fitness. Verify record ID/revision, source commit and
   exact source bytes/hash before rendering. Preserve unsupported input for
   diagnosis and stop the dependent record installation on a failed check.
3. Compare the recorded baseline: same ID/revision/source hash is unchanged;
   same ID/revision with a different source hash conflicts; an older revision
   is stale and needs an explicit rollback decision; a later revision is an
   update candidate, not overwrite permission. Also check current installed
   rendered bytes against the manifest. Preserve `local` entries and report
   managed drift under the adoption guide's existing ownership rules.
4. Render selected records and exactly their common catalog rows into the
   consumer mapping. Track both source and rendered hashes; link rewriting does not
   change logical record identity or revision. Preserve source asset identity
   values as provenance, not as local runtime paths. Unselected related record
   IDs remain plain text with unavailable-evidence limits. Omitted links to
   uninstalled assets become labeled logical references; never auto-expand the
   selection or leave broken navigation.
5. Complete content/link/conflict checks before saving the installed manifest
   as the final local import-state write. This does not authorize a Git commit.
   Record the local receipt privately: public ID/revision, source commit/source hash, installed path and
   rendered baseline reference, selected purpose, applicability/exclusions,
   local decision, actual task/run/evaluation if any, and later feedback state.
   If its private owner is unresolved, finish only permitted source installation
   and report session-only receipt; do not claim persistent reuse tracking.

An installed record is a reference snapshot. Its `work.state` remains a report
of the source effort, not local execution state. Accepting a work candidate
creates or links a local task only within current planning/action authority.
Local outcomes belong to that task and the private evidence/receipt; do not edit
the installed snapshot to impersonate an upstream update or mark the source task
done. Preserve compatibility and current skill/model/tool assumptions at use.

## Feedback And Revision

The recursive path is:

`record selection -> local applicability decision -> authorized work -> actual
outcome/contrary evidence -> reviewed public update -> later import/reassessment`.

Link the local feedback to the **public record ID and revision actually used**,
its source/rendered baseline and observed component use. A later current file
cannot prove an earlier run's input. On export, compare with the latest public
revision; reconcile new support and contradictions without double-counting the
same event. Update or supersede the same public record as appropriate, retaining
historical observations. A new source revision is not automatically eligible in
another project; import and re-evaluate its conditions there.

No background service, unrestricted self-editing, automatic replay, shared-rule
adoption, publication or cross-project installation is implied. The same contract
applies when this improvement procedure itself is the affected harness asset.
Record failures and costs of the procedure rather than assuming recursion helped.

## Version Changes And Consolidation

- Record schema v1, record content revision, harness mapping v8 and import
  manifest schema 1 are distinct. The manifest carries exact selection and
  source/rendered provenance; the private receipt carries purpose and feedback.
- Each reusable improvement has one current record owner, including its knowledge
  and work. Resolve older scattered notes by meaning: identify the question,
  evidence, predicates, acceptance and unresolved work; match the current record
  before adding. Preserve unique task/control lists, dates, approvals, tables,
  historical limits and original output references in their appropriate fields.
  Unknown facts remain unknown; normalization is not task execution or closure.
- When authorized consolidation makes an old note/list/template redundant,
  update its inbound references and remove it after the meaning check. Do not
  retain a compatibility view, pointer file or parallel record format. Preserve
  meaningful history inside the canonical record; no current instruction should
  depend on the deleted path.
- A source format transition does not authorize rewriting a consumer's private
  history or deleting local edits. During an authorized adoption, resolve an
  older selected source by stable identity and inspect its actual content; use
  the adoption guide's ownership/retirement procedure for replaced targets.
  Missing/ambiguous identity requires reconciliation before dependent writes.
- Unsupported future schemas require an explicit compatible migration; preserve
  source and installed baselines on failure. Completing normalization authorizes
  no pending experiment, commit, publication or cross-project installation.
