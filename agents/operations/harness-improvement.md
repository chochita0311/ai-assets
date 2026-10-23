# Harness Improvement Operation

## Purpose

Retrieve and retain supported experience during ordinary work, investigate a
harness problem, compare a bounded change when authorized, and export reviewed
common experience to its source owner. Use the
[Harness Improvement policy](../policies/harness/harness-improvement.md) for
evidence meanings, effect decisions, privacy and promotion boundaries. Use the
[Improvement Record contract](../policies/harness/improvement-record-contract.md)
for the common metadata/body format and import/export admission.
This operation requires no collection service or special runtime wrapper.

When completing a template at a record's actual owner, remove scaffold-only
instructions and replace its template-relative links with valid owned references.
Do not copy navigation that becomes broken after relocation or introduces a
private dependency into a public case.

## Select The Work

Choose the requested work and reuse authorization that already applies:

- **Ordinary stage work:** when the capability and private binding are ready,
  run entry/use/exit hooks as part of the active task without another command.
  Adoption performs the one-time binding setup below; it is not a per-run gate.
- **Maintain improvements:** select eligible unresolved work from its
  common record and use the procedure below. A request to review the queue
  remains a review; discovery alone does not start every listed task.
- **Observe:** resolve components and evidence, diagnose, and propose the next
  check. Do not start reruns merely to fill a template.
- **Compare:** execute the authorized comparison contract and decide among the
  baseline and candidates. Resolve missing inputs or side-effect authority
  before dependent execution.
- **Prepare a public case:** construct and review a standalone candidate from
  supported experience. Saving a candidate locally does not publish it.
- **Export common experience:** reconcile a reviewed public improvement record
  or authorized normative change into the resolved canonical shared source, following the
  export procedure below. It does not imply commit, push or consumer refresh.

These can form one authorized task. Observation alone does not authorize live
replays, source edits, publication or installation. Optional unavailable tooling
limits evidence; it does not require installing a new engine or adding workers.

## Recognize An Export Request

Use the policy's [request scope](../policies/harness/harness-improvement.md#export-request-scope)
to resolve mode, current project, intended common source and any category/time
limit. In established common-asset promotion context, a short export request
needs no special command syntax or repeated privacy/generalization instructions.

| Example request | Interpretation |
|---|---|
| `ai-assets로 export해줘`, or `export해줘` in that established context | Review available harness, skill/resource/tool, design/UI and interaction/UX experience; export qualified common content to its owner |
| `사용 사례를 ai-assets로 export해줘` or `사용 사례만 ai-assets로 export해줘` | Reference/evidence export across available categories; existing work assignments/state and normative rules are unchanged |
| `skill 사용 사례를 export해줘` or `skill 사용 사례만 export해줘` | Skill-case export only |
| `UI/UX 관점에서 공통화해줘` | Design/interaction commonization, including supported existing review-asset changes |
| `export할 만한 것만 검토해줘` | Candidate review; no shared-source write |

Explicit limits and applicable prior authorization take precedence over these
defaults. If export means a product/data operation in the active task, follow
that meaning. If the target or consequential edit scope remains ambiguous,
resolve it before writing rather than assuming every export means ai-assets.

Then use [Export Common Experience](#export-common-experience); the following
investigation prompt is optional, not a form the user must fill to export.

## Configure Local Experience

1. Confirm that the capability was selected. Resolve the consumer, environment,
   private audience and existing storage authority. Reuse an existing configured
   owner and its records; otherwise use the consumer's `docs/evidence/` under the
   [local layout policy](../policies/harness/harness-improvement.md#consumer-evidence-layout).
   Authorized adoption configures this default without a separate destination
   question. Use an alternative owner when existing rules or an explicit choice
   require it; a new default does not migrate prior history.
2. Establish effective exclusions for the local paths and check existing files,
   tracked/staged status, write access and separation from managed import targets
   before new private writes. Preserve existing broader ignores. Resolve a
   conflicting or unreadable store without overwriting, untracking or resetting
   it; if unresolved, keep observations session-only.
3. Initialize or map the [private store scaffold](../templates/harness-local-store.md)
   as `docs/evidence/STORE.md` at the default owner, or the configured equivalent.
   Record binding, record locations, applicable recording budget, retention and
   common improvement record owner. Create stage/improvement/experiment files
   only as needed. Local records and receipts are consumer outputs, excluded
   from the shared-file manifest and protected during refresh.
4. During adoption, expose the conditional operation pointer and standard
   `docs/evidence/STORE.md` locator in the consumer's entrance instructions.
   Keep actual binding contents and identifying or external private locators
   in the local store or approved private discovery surface, out of public docs
   and the import manifest. Later sessions follow the configured binding.
5. Confirm the binding is accessible, authorized and discoverable, with the
   applicable local exclusions in place, before claiming it is ready.
   If unresolved, report `installed, persistence unresolved` and use session-only
   observations. Do not keep asking for permission already supplied, reset
   existing records, or claim that template installation started collection.

No collection daemon or environment-variable convention is required. An agent
following the imported contracts performs the writes. An unavailable store or
interrupted agent can leave a gap; retain that distinction in the result.

## Ordinary Stage Work

The workflow/runner or direct stage performer invokes this procedure for each
actual stage/attempt. The coordinator owns the resulting record and index.

1. **Find the current stage.** Resolve the real target and role, available
   run/attempt identity and private binding. Before a run exists, use the
   planning artifact/session and stage identity. Find the existing target
   pointer on continuation; duplicate wrapper entry is the same stage.
   If the pointer is missing, use a bounded lookup of identifiable saved stage
   evidence to recover it; do not create another identity for that stage.
   With a ready binding, reuse the existing stage or save a new active stage,
   then save its pointer when existing audience-safe task references do not
   suffice, before performing the role. Do not reset an existing stage's state.
   Report an ambiguous match or failed write as a continuity gap and keep
   unsaved observations session-only under the policy's recovery rules.
2. **Retrieve before working.** Read the private improvement index and, when
   installed, the selected public record catalog. Filter by task, role/component,
   cue and scope; read matching records plus relevant counterevidence and
   supersession. Check knowledge status, current eligibility, exclusions,
   model/tool/contract assumptions and authority; only supported, applicable
   knowledge can guide reuse within current owned rules. Record
   `applicable / inapplicable / uncertain` with the action/reason, or
   `no match / unavailable`, in the
   [stage record](../templates/harness-stage-record.md). Stay within the task's
   recording budget. Do not turn an index absence or partial search into proof
   that no contrary case exists.
   Consult matching common records and their private import receipts. Recheck
   local eligibility and selected purpose; source work state is not a local
   task assignment. Keep pending hypotheses distinct from supported knowledge.
3. **Perform the existing role.** Capture relevant source/import/installed
   identities, actual performer, task inputs/outputs and observed supply/use
   events as work happens. Run participating skills through their own entry and
   output contracts. The coordinator records available skill-use evidence and
   maps ordinary results through steps 4 and 5. Apply the policy's evidence
   limits. Keep roles and runtime agents separate; do not recreate past effective
   input from current files. Existing source snapshots may be referenced only
   when known unchanged.
4. **Close at the real boundary.** At handoff, completion, return or block, save
   the observed outcome, domain evaluation reference where relevant, evidence
   gaps and reflection. Leave change effect `not assessed` unless a comparison
   exists. Preserve original observations and later recovery timestamps.
   Save the stage first, then refresh any target pointer with that saved state;
   this step applies even when no Improvement Record is created or updated.
5. **Reconcile the improvement.** For supported reusable knowledge or a
   grounded unresolved need, find the matching [Improvement Record](../templates/harness-improvement-record.md)
   at the authorized private owner. Use [Maintain Improvement Records](#maintain-improvement-records)
   to update its knowledge and work independently. Link original evidence/tasks;
   a hypothesis needs no lesson, and a completed stage need not create a record.
   Save the Improvement Record, then its index; avoid duplicate support.
6. **Return through the existing workflow.** Keep normal bug/spec/planning routes
   and human approvals. Surface qualified common candidates at the existing
   closing review, grouping design/interaction candidates with their owner
   review. An actual comparison and a shared export each retain their own
   authority and evidence requirements; neither starts from ordinary success.

If persistence becomes unavailable, report which writes succeeded, keep the
remaining observation session-only and name the recovery condition. On resume,
repair a missing target pointer from identifiable saved stage evidence, or an
improvement-index entry from its saved record, instead of duplicating either.
Task acceptance continues to depend on its original required evidence.

## Maintain Improvement Records

Use the [common record lifecycle](../policies/harness/improvement-record-contract.md)
for knowledge, pending work and reference experience across every asset type.
For ordinary reflection or record consolidation, use steps 1, 4 and 5 with the
existing evidence. Use steps 2 and 3 only when selecting and performing new
maintenance is within the active request; reflection alone starts no extra task.

1. **Resolve and discover.** Identify the requested scope and audit/improvement
   authority. Find relevant private or selected public records by subject and
   cue. Read scattered source notes for their actual question, evidence,
   eligibility, required action and completion criteria. Resolve these into the
   matching record fields, including satisfied versus still-open checks; do not
   merely wrap old prose or infer completion. When consolidation is authorized,
   update inbound links and remove the fully absorbed document after meaning
   review. Do not create compatibility views or scan unrelated private history.
2. **Select what is ready.** Check local applicability, date/event, dependencies,
   evidence, action-specific authority and budget. A source record's readiness
   does not establish local readiness. Choose bounded work by impact, recurrence,
   evidence readiness and cost. Honor an explicitly wider audit only for the
   selected authorized task. Report waiting reasons; no eligible item is valid.
3. **Perform the owned task.** Link or create the actual local task within
   existing planning/execution gates. Establish the real baseline and success
   checks. For skill maintenance, use $refine-skill when available, retaining
   audit/refine scope and its static/behavioral distinctions. When a skill is
   used, consume its normal report in step 4. This operation owns record
   normalization, persistence and exchange. Keep tool, model, product and policy
   defects with the appropriate owner. No comparisons or live actions
   follow merely from importing or reading a candidate.
4. **Reconcile the result.** Save original outputs, controls and counterevidence
   at the task/evidence owner. Update the local record/receipt using the public
   ID, revision and source/rendered baseline actually used. Retain supported
   knowledge in the same record only when warranted; effect is `not assessed`
   without a comparison. Link later reuse decisions, preserve the original
   failure and passing controls, and update the common index after the record.
   Close satisfied work or a reasoned no-change/withdrawal; keep unmet checks
   open. Do not mark the upstream record completed from local execution alone.
5. **Resume or export.** Record the next trigger and any partial write. Stop
   unchanged exploration without new evidence/conditions. When commonization
   is requested, export qualified feedback or remaining work through the record
   contract to a reconciled source revision. Case-only export does not assign
   or close work. Publication and consumer refresh remain separate actions.

## Investigation Inputs

- The request or observed problem, expected behavior and original evidence.
- The component owner and source, installed and execution identities available.
- Existing feature/run/attempt or session reference when relevant.
- Authorized changes, replay side effects and stopping budget for a comparison.
- The private record owner when persistence is requested or needed.

Use the configured local owner or the default established by
[Configure Local Experience](#configure-local-experience). If evidence or that
owner is unavailable, complete the supported session analysis and name the
missing condition. Do not invent an experiment result; an arbitrary ignored
directory is not a substitute for the configured owner.

## Procedure

1. **Resolve and route.** Identify the task boundary and actual component owner.
   Apply the policy's diagnosis and existing bug/spec/planning return routes.
   Keep the task's acceptance criteria fixed.
2. **Capture the baseline.** Read the minimum original inputs, outputs and
   relevant events. Distinguish current source, installed content, declared
   settings, and what the particular trial actually received and used.
   Save observations at the existing private task/stage evidence owner, reusing
   the active stage when one exists. Do not save completed records in the
   installed template directory. Observation-only work and public-candidate
   preparation do not create an experiment.
3. **Consult experience selectively.** Read the private improvement index and any
   installed record catalog, then matching and relevant contrary/superseding
   records. Record chosen IDs, eligibility/exclusions and why current conditions
   fit, fail to fit or remain uncertain. No matching cases is a valid state.
4. **Set the comparison contract when comparing.** For observe-only work, return
   with a proposed check and evidence limits at the existing evidence owner.
   For an authorized comparison, prepare the
   [comparison contract](../templates/harness-experiment.md#comparison-contract--before-execution)
   at that private task/stage owner. Fill hypothesis, candidates, inputs, checks,
   successful and contrary controls, producer/evaluator evidence, isolation,
   budgets and side effects before launching. Keep no change selectable.
5. **Run and retain.** Execute the baseline and candidates within the contract.
   When the first authorized trial actually starts, create the
   [experiment record](../templates/harness-experiment.md) at the resolved private
   comparison owner, retaining the prepared contract and its original timing.
   If cancelled before any trial starts, retain the unexecuted proposal at its
   preparation owner without creating an experiment. Record an interrupted or
   incomplete comparison with the actual trials and missing evidence.
   Capture the first outputs and relevant actions; append attempts and
   interventions. Explicitly label author checks and contamination. If a
   required condition is missing, stop or narrow the claim without fabricating
   execution. Reading the package is not a behavioral rerun of its domain task.
6. **Compare edits.** Inspect every candidate, including rejected ones. Fill the
   per-edit effect table, keep original results and counterexamples, and state
   attribution limits. Record execution Result, Coverage and acceptance impact
   separately from effect and disposition.
7. **Close the comparison.** Stop at the declared boundary and record actual
   overhead and unknown measurements. Keep baseline, apply locally, propose
   promotion, hold or discard. Update record knowledge only when supported; otherwise
   state that no durable lesson was established. Route any domain-task
   acceptance back to its existing run/spec owner.
8. **Prepare a public candidate when in scope.** Follow the reconstruction and
   review steps in [Export Common Experience](#export-common-experience), using
   the [common record template](../templates/harness-improvement-record.md) when a public case is
   useful. Candidate preparation may stop before any shared-source write.
9. **Promote through the owner.** Complete only the authorized export steps.
   Keep case review, rule adoption, source edits, publication, refresh and
   activation statuses separate.
10. **Revisit and dispose.** On later relevant evidence, reassess conditions and
    preserve contradictions or supersession. Move evidence needed later to its
    agreed owner before cleaning task-owned scratch. A public asset must remain
    usable without the private record.

## Export Common Experience

Use [record export](../policies/harness/improvement-record-contract.md#export-to-the-common-source)
and the policy's [source destinations](../policies/harness/harness-improvement.md#consumer-to-shared-source-export).
This direction is consumer to common source, independent of Git ignore rules.

1. **Resolve scope and source.** Apply the request mode/category/time limits and
   resolve the actual ai-assets checkout. Select relevant records, observations, comparisons
   or scattered improvement notes from available current-project evidence.
   Include new support, counterevidence and changed conditions; do not scan all
   raw history or unrelated environments. Report missing history and retain
   local/hold candidates when scope, source or evidence is unresolved. For a
   normative delta compare accepted import baseline and current shared rule.
2. **Normalize privately.** Use the common template and schema for a reusable
   improvement record. Preserve original task/evidence owners. Reconstruct the
   minimum public account with eligibility, exclusions, evidence/counterexamples,
   proposed action and limits. Label synthetic, private observation and public
   execution honestly. Missing comparison means `not assessed`; a truthful open
   item needs no proven lesson. No unauthorized rerun is required to export.
3. **Review and reconcile.** Apply semantic disclosure and meaning review before
   any publishable common-source write. Keep credentials, identifying details, original
   private paths/IDs/hashes and revealing context private. Resolve stable public
   identity and expected revision/hash across the public evidence layer;
   resolve the [subject-owned location](../policies/harness/improvement-record-contract.md#public-record-placement)
   and match subjects/problem/predicates and
   independent events. Hold privately if meaning or public fitness is unresolved.
   Validate the format and approval state; same-revision changed bytes or a
   concurrent source update require reconciliation, not a blind overwrite.
4. **Write the common result.** Write the normalized record to the resolved
   `evidence/agents/<component>/` or `evidence/skills/<component>/` source location,
   incrementing content revision for an update. Preserve original observations,
   contrary evidence and history. Reconcile the common catalog/index
   after the record; a move also removes its old entry and copy after references
   are resolved. Generic commonization may retain grounded remaining work and
   apply bounded supported changes at the actual policy/skill/review owner.
   Reflect work actually completed by this export; do not create a new pending
   item for an already completed correction. Preserve any unmet checks separately.
   Case-only mode updates reference/evidence content, keeping existing work
   assignments/readiness/closure and normative rules unchanged. A new reference
   uses not-applicable work state. No-op is valid; report partial writes.
5. **Receipt privately.** Record public ID/revision, old/new source hashes,
   actual source commit or uncommitted snapshot, decision and unresolved steps.
   Keep the private-to-public association private. Use an existing private
   record/task owner or session-only receipt with a gap; do not invent a ledger.
6. **Distribute within authority.** Source changes establish neither commit/push,
   installation nor runtime use. Accepted imports require the committed-source
   baseline and existing ownership/conflict rules. Other consumers choose public
   records as references or work candidates; private original history never moves.

## Import Improvement Records

Use [record admission and local use](../policies/harness/improvement-record-contract.md#import-and-local-use)
with the adoption guide's complete capability and mapping v8. An installed
record is a source snapshot, not a local task or silently adopted instruction.

1. Resolve exact record IDs across evidence domains and purpose: reference
   or work-candidate. Resolve
   an older selection by its stable identity and actual content before rendering;
   reconcile ambiguity without recreating source aliases. Do not select all work by default.
2. Admit only supported format/schema, unique public identity/revision, approved
   public fitness and attributable committed source/hash. Compare record revision
   and current installed baseline; stop unknown-version, same-revision/different-
   hash, stale-revision-without-rollback or managed-drift conflicts. Preserve local
   ownership and invalid-manifest recovery rules before dependent writes.
3. Render only selected records and their common catalog rows, retaining
   repository-relative source locators, source/rendered provenance and safe
   references to omitted evidence. Normalize an older manifest's package-root
   locators without changing their effective baseline paths or detached local
   baselines. Complete checks before
   the final manifest write. Reconcile superseded installed content and inbound
   references, then retire old managed targets when covered by the authorized
   refresh. Preserve local ownership or unresolved drift; do not recreate aliases.
4. At the authorized private owner, retain the receipt: selected ID/revision,
   source commit/hash and rendered baseline reference, purpose, local applicability
   decision and any actual task/evaluation. If unavailable, report session-only
   receipt and the persistence gap. Installation is distinct from observed use.
5. During later relevant work, recheck eligibility, current rules and authority.
   A candidate starts work only through normal planning/action gates. Retain
   actual outcomes with the revision used; export reviewed new evidence through
   the preceding procedure, never by editing the installed snapshot as upstream.

## Output And Exit

Report the investigated component, observed application state, diagnosis,
comparison performed or not performed, per-edit effects, evidence limits,
disposition, actual overhead and next owner/action. Link an existing private
record only in an appropriately private output. A public run or evaluation
must not contain a private locator or identifying experiment ID.

For ordinary work, report only meaningful reuse, recording gaps, supported
knowledge or promotion decisions; do not narrate every bookkeeping action. Keep a
safe stage/improvement reference in existing artifacts only when their audience may
see it. Private recording may proceed without putting a link in a public PRD,
run or evaluation. Do not copy an experiment's effect table into several owners.
The existing design/interaction review and human acceptance sequence remains.

For improvement maintenance, report the selected work and why it was eligible,
actual results and closure evidence, unmet conditions or remaining work, and
the next revisit trigger. A queue review or static correction must not imply
that a listed behavioral check ran or that other waiting items were completed.

For export, report the interpreted mode, considered categories and evidence
coverage, actual common-source writes and their owners, and items left
`local / hold / discard / unchanged` with reasons. Identify remaining concrete
decisions and partial writes. Keep identifying excluded details in private
outputs, not public review notes. If no candidate meets reuse, evidence and
public-fitness requirements, report that no common-source change was warranted.
Do not imply a limited review covered all historical work or force a case into
every category.

## Prompt Frame

```text
Use the installed Harness Improvement operation for this bounded problem.

Work requested: observe / compare / maintain improvements / prepare a public case / export common experience
Problem and original evidence:
Component and actual source owner:
Common record ID/revision, private evidence owner and eligibility, when applicable:
Related feature/run/attempt or session:
Private record owner and existing storage authorization, or session-only:
Authorized edits and replay side effects:
Comparison inputs, controls, success checks and budget, if comparing:
Known model/tool/context or loading limits:
Public candidate destination and authorized promotion steps, if applicable:

Keep the baseline selectable. Distinguish observed, declared and unknown
application states. Preserve original outputs and counterexamples. Report
Result, Evidence Coverage, effect and disposition separately; do not infer
publication, installation or activation from a source change.
```

Ordinary stage work uses the installed entrance/flow/runner hooks and does not
require the human to fill this investigation prompt.
