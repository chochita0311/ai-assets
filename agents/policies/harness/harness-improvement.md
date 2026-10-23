# Harness Improvement

## Contents

- [Purpose And Ownership](#purpose-and-ownership)
- [Activation And Private Store](#activation-and-private-store)
- [Ordinary Stage Lifecycle](#ordinary-stage-lifecycle)
- [Evidence Of Application](#evidence-of-application)
- [Diagnosis And Return Routes](#diagnosis-and-return-routes)
- [Comparison Contract](#comparison-contract)
- [Effects And Decisions](#effects-and-decisions)
- [Improvement Records](#improvement-records)
- [Public Cases And Promotion](#public-cases-and-promotion)
- [Cost, Stopping, And Compatibility](#cost-stopping-and-compatibility)

## Purpose And Ownership

Make a harness change reviewable: connect the components supplied to a task, the
observed behavior before and after a change, and the evidence supporting reuse.
This is an optional capability. Once selected and configured, ordinary work
includes relevant experience retrieval, application evidence and a closing
reflection without a separate user command. An explicit improvement request or
a relevant observed problem, including model or tool changes and repeated cost,
can warrant a comparison. Completing an ordinary stage or run does not itself
require an experiment or a retained improvement record.

This policy owns cross-component evidence, comparison records, common follow-up
semantics, and the boundary between private experience and public records.
The [Improvement Record contract](improvement-record-contract.md) owns their
common format, identity and import/export admission across all asset types.
Skill-specific diagnosis stays in the owning skill.
[Execution governance](execution-loop-governance.md) owns task
acceptance and return timing; this policy does not change those criteria.

Keep reusable skills independent of this optional capability. The consuming
harness owns mapping available skill outputs and observations into the common
record lifecycle; skill packages need no knowledge of its schema, storage layout
or import/export procedures. A standalone skill invocation does not select or
configure this capability. When the capability is selected and configured, its
coordinator applies the existing stage lifecycle while preserving the skill's
entry, output, authority and evidence contracts.
The coordinator keeps observed skill work at the existing private stage/evidence
owner and uses the experiment owner only for an actual comparison and its
per-edit effects.

| Artifact | Owner and persistence |
|---|---|
| Shared procedure and templates | Shared harness source; imported copies follow the adoption contract |
| Private binding, experience index, stage records, original evidence and private-to-public links | Consumer-owned `docs/evidence/` by default, or an existing configured private owner; original task artifacts retain their own owners |
| Private improvement record | Configured private owner; owns reusable knowledge and improvement work under the common format, linking original observations |
| Public experience or unresolved reusable improvement | One canonical Improvement Record at its subject owner under `evidence/agents/` or `evidence/skills/`; `evidence/README.md` discovers the collection |
| Adopted policy, skill behavior, or design/interaction criterion | Its existing policy, skill package, or review-asset owner |

Use the consumer's `docs/evidence/` as the default local evidence layer beside
`docs/agents/` and `docs/plans/`. Private here describes the intended audience
and publication boundary, not a requirement to store files outside the repo.
An authorized, ignored consumer-local store is valid even in a public repo;
establish the storage and exclusion rules below before writing private records.
If that cannot be resolved, report session-only observations without claiming
accumulation. Reuse authorization that already applies.
Keep task scratch bounded and remove it after its diagnostic purpose ends.
Transfer evidence needed later to its explicit owner before removing temporary
copies; shared assets must not depend on a temporary plan or private path.

## Activation And Private Store

| State | Normal work behavior |
|---|---|
| Capability not selected | Existing workflow; no experience hook or migration requirement |
| Installed, private binding unresolved or unavailable | Supported session-only observation; report the persistence gap without inventing a store or claiming accumulation |
| Installed, authorized binding resolved and accessible | Perform the ordinary stage lifecycle automatically within the existing task |

During authorized adoption of this capability, configure `docs/evidence/` once
for the consumer and environment, including its audience, storage authority and
discovery path. Use this default without a separate destination question when
the existing authorization and repository rules permit it. Reuse an existing
configured owner instead of creating another store. An explicit external or
equivalent owner remains valid when selected or required by the environment;
the new default does not relocate existing history.

### Consumer Evidence Layout

| Consumer location | Owner and purpose |
|---|---|
| `docs/evidence/STORE.md` | Local binding, improvement index, target pointers and receipts when no existing receipt owner applies |
| `docs/evidence/stages/` | Local observations for actual stages and attempts |
| `docs/evidence/improvements/` | Local reusable knowledge and improvement work, created when warranted |
| `docs/evidence/experiments/` | Local comparisons once an authorized trial actually starts, including incomplete or interrupted comparisons |
| `docs/evidence/agents/`, `docs/evidence/skills/` and `docs/evidence/README.md` | Explicitly selected public source records and their catalog, managed by the import contract |

Local records are consumer outputs. Never add them to the harness import
manifest, replace them from a template on refresh, or copy them to another
consumer as part of import. Managed public snapshots keep their source identity;
local observations and feedback belong to the local owners above. Do not replace
the whole evidence directory to refresh selected shared files.

Keep the default local paths excluded from Git tracking and publication. Reuse
effective existing exclusions or add these repository-relative rules through
the repo's existing ignore mechanism during setup:

```gitignore
/docs/evidence/STORE.md
/docs/evidence/stages/
/docs/evidence/improvements/
/docs/evidence/experiments/
```

Preserve broader existing ignores, including a fully ignored harness tree;
do not force imported references into Git. Confirm the resolved local targets
are writable, excluded and not already tracked or staged, and do not overlap
managed import targets or redirect into publishable source. Ignore rules do not
untrack existing files or establish publication permission. Preserve conflicting
files and resolve ownership before dependent private writes; never silently
untrack, overwrite or reset them. An alternative owner follows its applicable
storage and publication rules. Public export still requires reviewed
generalization; local storage does not authorize it.

### Binding And Continuity

`STORE.md` owns the private binding and improvement index. Stage records own
what happened; experiments own comparisons. Improvement Records own reusable
conclusions, improvement work and exchange identity; they link original
evidence and actual execution tasks.
Keep observation-only investigations and proposed comparison contracts at the
existing private task/stage evidence owner. Prepare the comparison contract
there before execution; create an experiment only when its first authorized
trial actually starts, retaining that prior contract. A proposal cancelled
before any trial starts remains unexecuted at its preparation owner.
Link original task artifacts instead of duplicating them. Preserve
the input/output snapshot identity and evidence needed for a continuing claim
at its authorized owner before a mutable or temporary original disappears.

The standard relative locator `docs/evidence/STORE.md` may appear in entrance
instructions so later sessions find the default store. Keep its actual binding
contents, identifying IDs and machine-specific or external private locators in
the local store or an approved private instruction/context surface. Resolve an
existing override through that surface. Do not copy private bindings or local
experience records into public docs or the import manifest. Installation,
binding readiness, successful record writes and observed reuse are distinct
facts. A later machine must resolve its own binding; an imported harness does
not transport private history. Do not join company and personal stores or
synchronize them without applicable authorization.

Keep stable stage, improvement-record and export identities within the store. A resumed
stage uses its existing identity; a genuinely new attempt appends its own
identity. Before editing an existing record or index, reread its current state
and preserve concurrent work. Missing, contradictory or unreadable binding/index
state is not permission to reset it. Report the gap and use session-only
observation until resolved. This gap does not itself block the domain task;
required task evidence still follows its normal acceptance rules.

## Ordinary Stage Lifecycle

Apply this lifecycle to each role actually performed: PRD normalization,
feature planning, orchestration, spec writing, build, evaluation, fix and
reevaluation, including planning-only work and controlled direct continuations.
Skipped roles produce no execution claims. Use a stage and attempt identity
linked to the real planning artifact or session before a run exists; attach a
run ID only after that run exists.

1. **Enter:** resolve the active target, role and private binding. With a ready
   binding, find and reuse the existing stage or save a new active stage before
   performing the role, then save its target pointer when existing audience-safe
   task references do not suffice. Recover a missing pointer from identifiable
   saved stage evidence before creating a new identity; an ambiguous match is a
   continuity gap, not permission to duplicate or reset records. Select relevant
   private and selected public improvement records by stage, component, cue and
   scope. Recheck eligibility, exclusions, current facts and the actual rule
   owner. Record selected IDs, the decision and reason as `applicable`,
   `inapplicable` or `uncertain`. Record `no match` or `unavailable` honestly.
   An uncertain case cannot authorize an automatic patch; an applicable case
   informs work only within current scope, authority and owned rules.
2. **Work:** connect the components actually observed, task input identities,
   role/actor and relevant read or invocation events using the evidence contract
   below. Append newly used components or changed snapshots. Reuse a captured
   snapshot only when its identity is known to be unchanged. Do not scan or
   claim to trace every installed asset or inaccessible runtime input.
3. **Exit:** at completion, handoff, return or block, append the outcome,
   evidence boundary, interventions and reflection to the stage record. Keep
   domain Result, Coverage and acceptance impact where the role already owns
   them; planning approval remains a separate human decision. A normal outcome
   without a comparison has change effect `not assessed`. Save the stage before
   refreshing its target pointer with that saved state, whether or not an
   Improvement Record is warranted.
4. **Retain and reuse:** reconcile supported knowledge and actionable unresolved
   work in the matching [Improvement Record](#improvement-records), then update
   its index. An evidence gap can justify work without a supported lesson; a
   stage need not produce a reusable record. Preserve contrary evidence and
   supersession; link a comparison only when one actually ran. Surface common
   candidates at the existing review boundary without implying export or
   shared-rule adoption from stage completion.

The stage performer supplies evidence; the active planning or run coordinator
owns entry/closing writes, target pointers and any improvement-index update.
One primary agent may perform both.
When evidence arrives later, append it without inventing an earlier observation.
On resumption, fill a missing close only from recoverable evidence and mark the
gap. Repeated entry through a role, flow and runner must reuse one stage record,
not create duplicate observations. Human review and the runner's existing
design/interaction candidate and acceptance sequence retain their timing.

## Evidence Of Application

The harness includes the role contract, workflow/runner, execution profile,
policies, templates, skills and their resources, and relevant runtime/model/tool
configuration. A PRD, feature, spec or evaluation report is a task input or
output; its producing role and the rules/template used are harness components.
Record both relationships separately. A logical evaluator or planner role is
not evidence of a separate agent, subprocess or model invocation.

Identify each relevant component **per stage or trial**, including baseline trials:

- logical source, full source revision when known, component path and content
  fingerprint, and dirty or local changes;
- accepted import baseline's source revision, source hash, rendered hash, and
  mapping version when available;
- actual installed content fingerprint, distinct from the import baseline;
- input snapshot, requested and observed model/settings, tools, runtime,
  inherited instructions, caches, and execution profile;
- supplied and used content, the event that supports each claim, and the
  observation boundary.

Identify the actual performer when observable, the logical role, stage/attempt
and related artifact; preserve `unknown` for hidden runtime identity. Link
evaluation criteria to their policy/spec owners and findings to the evaluated
artifact. A template's existence is not evidence that the stage used it.

A revision and a component fingerprint are separate facts. Source, rendered,
and current installed hashes are also separate facts. For an uncommitted
candidate, record the base revision plus the actual candidate snapshot/diff and
hashes; never attribute that content to a commit that does not contain it.
Reading the current file cannot reconstruct a past trial's loaded content.
Record `unknown` with a reason when it cannot be recovered.

| Claim | Required support | Limit |
|---|---|---|
| Installed | Observed file and content at the resolved target | Does not establish supply or use |
| Provided | Observed effective runtime input, or equivalent direct evidence of the specific supplied content | Configuration, a request, or an agent statement alone is `declared`; actual provision remains `unknown` |
| Not provided | Complete relevant observation establishing absence from the effective input | A missing input event in a partial trace leaves provision `unknown` |
| Used | Relevant read, invocation, or tool event tied to the component and trial | Catalog presence and installation are insufficient; reading does not establish semantic compliance |
| Not used | Complete relevant observation covering the opportunity for use and establishing absence | Absence in a partial trace is `unknown`, not `not_used` |
| Behavior changed | Original outputs and actions showing the difference | Expected outcomes and author explanations are not observations |

For each claim, distinguish `observed`, `declared`, and `unknown` support; record
the actual state separately. A read event can support a narrow use claim without
proving that the runtime automatically selected or obeyed the whole package.
No state above automatically establishes the next one or a causal effect.

## Diagnosis And Return Routes

Connect expected behavior, observed mismatch, evidence, likely cause, and owner.
Consider skill contract/resource, model/execution, tool/environment,
input/evidence, and surrounding workflow causes. Allow mixed or uncertain
causes and choose a bounded check that distinguishes them. A failure does not
by itself justify another instruction.

Preserve the existing execution routes:

- When the approved feature and active spec remain valid and only the
  implementation is wrong, stay in the loop for targeted fixes and the needed
  evaluator reruns.
- A weak, incomplete or contradictory spec under a valid feature is reported
  with a post-run recommendation. After human review and spec correction, start
  a new run from build or targeted fix work.
- A problem changing approved scope, unresolved dependency meaning, mode
  meaning, contract ownership or user-visible intent goes to post-run human
  planning review. Re-approve the corrected boundary before spec or build and
  start a new run.
- A technical blocker that prevents safe continuation can stop the run early.
  Record `blocked` and report it before the human decides on local unblock,
  spec review or planning review.

Do not patch the harness to redefine success or conceal a spec/planning gap.
When changing models, first establish the old harness on the new model; compare
the candidate on that same model. If model and harness both changed, preserve
that attribution limit.

## Comparison Contract

Before starting a comparison, fix the following in proportion to the hypothesis:

1. The component owner, hypothesis, baseline including the no-change option,
   candidate identities/diffs, expected behavior, success and falsification
   checks, and authorized change scope.
2. The task inputs and snapshots, requested versus observed model/settings,
   tools/environment, inherited global instructions, cached context, and
   isolation limits. A fresh conversation alone is not instruction isolation.
3. Which facts each producer receives and which the evaluator receives.
   Supply necessary task evidence to every compared producer. Evaluator-only
   facts cannot prove a producer omission: repair the input or mark the check
   evidence-limited. For an independent forward-test, withhold the answer key,
   proposed fix, prior outputs and authoring conclusions. Historical outputs
   remain legitimate inputs when auditing those outputs is the task.
4. The failure case and relevant passing, authorized-success, no-change and
   regression controls. Explain excluded controls. A broader transfer claim
   needs materially different cases. Do not require a universal task count or
   multiple agents.
5. Maximum trials, elapsed time and available cost limits, allowed side effects,
   and stop conditions. Replaying a task must remain within its authorization;
   isolate or substitute live side effects before rerunning.

Keep each first output, relevant actions/errors, interventions, completion
evidence and attempt identity. Append retries; do not replace an inconvenient
output with a later pass or keep sampling until a preferred result appears.
Do not count inherited copies of one event as independent runs.

Use an answer-isolated producer where available and permitted. If the author
performs the task with prior knowledge, label it an **author check**. Another
evaluator does not make it independent. Record contamination and condition
differences rather than calling the baseline candidate-free without evidence.

## Effects And Decisions

For every candidate edit, including rejected candidates, record component,
candidate IDs, change, observed difference, evidence locator, effect, and limits.

| Effect | Meaning |
|---|---|
| `helped` | Observed improvement on the declared checks under the recorded comparison conditions |
| `hurt` | Observed regression on those checks, including a blocked authorized success path |
| `no observed effect` | The observed checks did not distinguish the change; not proof of equivalence |
| `confounded` | Conditions or co-occurring changes prevent attribution, or evidence is insufficient |

Separate a directional observation from a causal conclusion. Prefer
`confounded` for causal attribution in a single comparison or when several edits
changed together; a better-looking selected result is not per-edit proof.
Useful edits may exist in a rejected candidate. Keep the baseline selectable,
counterexamples visible, and no change a valid result. One success establishes
neither stability nor general reliability.

Keep these axes independent:

| Axis | Record |
|---|---|
| Record lifecycle | Draft, reviewable, closed, or superseded; does not replace feature/run status |
| Execution evaluation | Existing `PASS / PASS WITH SUGGESTIONS / FAIL` |
| Evidence Coverage | Existing `complete / partial / unavailable`, gaps and their acceptance impact |
| Evidence maturity | Static validation, resource execution, observed stage execution, fresh forward-test, or comparable rerun; qualify independence and comparability |
| Effect | The four values above, per edit |
| Disposition | Keep baseline, apply locally, propose common promotion, hold, or discard |
| Common adoption | Proposed, accepted, implemented, superseded, or withdrawn, with owner and scope |
| Distribution | Publication, consumer refresh, and observed runtime activation, each separately |

`not assessed` is the ordinary-stage value when no change comparison exists;
it is not a fifth comparison result. A single successful stage or repeated
copies of its report do not establish that a harness change helped.
`Observed stage execution` means task-bound evidence of work actually performed;
it establishes neither an independent forward-test nor a controlled comparison.

An experiment can finish correctly while its candidate is rejected. Static
validation or resource execution does not establish agent behavior. Compare
original failure recurrence and controls before claiming stability; unavailable
required evidence retains its acceptance impact under the feature/spec/profile.

## Improvement Records

Use the [common record contract](improvement-record-contract.md) for both
reusable knowledge and improvement work. A skill follow-up, harness question,
UI/UX lesson or public reference is selected from the repository-level evidence
collection, not maintained as a separate agenda or lesson format. Product-specific bugs and
UI/UX suggestions retain their existing planning/heuristic owner; normalize
only a justified reusable asset-level need. Actual tasks/evaluations own execution
and acceptance; evidence artifacts own original observations and comparisons.

### Knowledge And Reuse

Retain a supported lesson in `knowledge` only when evidence supports it. Prefer
one core question/conclusion per record; separate independent questions when
their predicates, evidence or owners differ. Preserve:

- **Cue:** recognizable situation, eligibility and exclusions.
- **Lesson:** component/method to consider, how and why.
- **Evidence:** original events/outputs and maturity, including contrary results.
- **Confidence:** reasons tied to evidence and scope, not an invented probability.
- **Limits:** tested conditions, counterexamples and unknowns.
- **Revisit triggers:** model/tool/contract changes, new failures or contrary
  evidence, and supersession relationships.

Knowledge state is independent of work state. `supported` is bounded by evidence,
not universal reliability. Use `candidate` for a provisional claim, explicitly
marking an untested hypothesis versus evidence-backed knowledge awaiting owner
or scope review. Only supported, currently applicable knowledge may guide reuse
within current owned rules. A hypothesis can justify open work without becoming
a proven lesson, and a normal-stage lesson need not prove a causal edit effect.

Retrieve relevant records by stage/subject, cue and scope from the available
common catalog or private index; read eligibility, knowledge/evidence limits,
work/readiness, adoption and contrary
or superseding records. Keep retrieval within the task budget. Missing/partial
retrieval cannot establish absence of contrary evidence; retain current rules
and report that limit. A new task does not inherit a patch automatically. Age
alone does not invalidate knowledge.

### Work Selection And Closure

For a relevant stage or maintenance request, choose bounded work by impact,
recurrence, evidence readiness and cost. Check current applicability, date/event,
dependencies, evidence, action-specific authority and budget. An explicitly wider
audit belongs to its selected authorized task; do not scan all projects/stores
by default. A date, recurrence or imported record grants no execution, live-write
or test authority. Reuse existing authorization and retain per-turn requirements.
Leave unmet conditions waiting with their next trigger; stop unchanged exploration
without new evidence or a changed condition.

Use the domain maintenance method and existing planning/return routes. Preserve
actual Result/Coverage and per-edit effects, or `not assessed` without comparison.
Close only satisfied work or a reasoned no-change/withdrawal/supersession. Keep
unmet discovery/runtime/stability/distribution checks open; retain the original
outcome, counterevidence and resolution evidence. The shared record's work state
and a consumer's task state remain distinct, as do rule adoption, publication,
refresh and observed use. Uncommitted edits are not Git resolution history.

### Reconciliation

Match record ID, subjects, problem and predicates before creating an item.
Append independent evidence; a resumed stage, inherited event or copied report
adds no support. Narrow or supersede contradicted claims with reasons and
historical evidence intact. Save the record before updating its common index;
repair partial index writes from the record instead of creating a duplicate.
Select open/active work by metadata when needed; do not maintain a second list.
Public records contain reviewed generalized content only; unresolved private
ownership leaves observations session-only. Shared writes still require the
applicable export scope and public-fitness review.

## Public Cases And Promotion

Construct a separate public candidate from the minimum information needed to
understand the problem, intervention, conditions, counterexamples and limits.
Do not automatically copy private text, task/run IDs, paths, internal URLs,
identities, raw traces, or private file hashes. Masking strings and automated
scans alone cannot establish publication fitness; review both content and the
relationships that could reveal private context.

`ai-assets` is public. Treat its publishable checkout as a public-content
boundary even before a commit or push. Only reusable, public-appropriate
material belongs there. Exclude actual credentials, tokens and passwords,
private personal data and confidential company/project facts, including those
embedded in private logs, screenshots, source excerpts, filenames or metadata.
Review combinations of otherwise innocuous details as well as individual strings.
Use placeholders or synthetic values when a public example needs that shape,
and retain the changed conditions and execution-status limits below.

Generalization must preserve the problem structure, eligibility/exclusions,
evidence, counterexamples and limits while removing private dependencies.
If publication fitness cannot be established, or removing private facts would
destroy the meaning needed to support the case, keep the item private as
`local` or `hold`. Do not place a raw or unresolved private draft in the shared
checkout for later cleanup. No eligible common content is a valid no-change
result; do not invent an example or dilute a claim just to produce an export.

Distinguish:

- **Illustrative synthetic:** expected behavior, with `not run` when unexecuted.
- **Generalized private observation:** a bounded account of original private
  evidence, with what public readers cannot verify stated explicitly.
- **Public reproduction:** actual outputs from the disclosed inputs and
  conditions, separate from any original private observation.

Changing identifiers or inputs does not reproduce the original outcome. State
which problem structure was preserved, which conditions changed, and whether
the public version was rerun. A public record must stand alone. Use the common record format for both cases
and reusable remaining work. Keep the private-to-public record-ID link private; do not publish a backlink
to private evidence.

Case review, normative rule adoption, source editing, external publication,
consumer refresh and active runtime use are separate decisions and observations.
An accepted case is a reviewed reference, not an installed instruction.
Use the existing adoption guide's `promote / local / discard` decision:
policies go to their policy owner, skill changes to that package, and design or
interaction criteria to their review assets. The common record catalog only supports discovery.
Source and installed copies continue to follow import ownership and conflict
rules; this capability grants no automatic push, posting or installation rights.
Complete actions already within the authorized scope without redundant approval.

### Export Request Scope

When the active request or established conversation means common-asset promotion
to `ai-assets`, a short request such as `export해줘` invokes common export.
The user need not repeat generalization, privacy review or every asset category.
This interpretation does not take over an unrelated application/data export;
resolve a genuinely ambiguous destination or edit scope before dependent writes.

Without a narrower selection, consider the current project's available relevant
experience across harness roles/workflows/operations/profiles/policies/templates,
skill selection/execution/resources and tool/environment use, and design/UI
and interaction/UX evaluation. This is a candidate-review scope, not a
requirement to produce a change in every category or inspect unrelated projects,
machines, company stores or personal stores.

| Requested intent | Scope and authorized outcome |
|---|---|
| Commonize/export to ai-assets, without a category restriction | Review all categories above; write qualified reference cases, bounded existing-owner common-asset changes and eligible unresolved follow-ups entailed by the request, after evidence and disclosure review |
| Export usage cases, with or without an explicit "only" | Prepare or update qualified reference/evidence content in common records and their catalog; existing work state/assignments and normative adoption are unchanged |
| Review/find export candidates only | Report candidates and limits; no common-source write |
| A named category, skill, case or time range | Restrict the selected mode to that boundary; do not silently widen it |

Commonization authority covers source changes that are supported, generalizable,
within the existing owner's purpose and compatible with the current contracts.
It does not imply unrelated redesign, deletion of established rules, changes to
runtime/model bindings or new approval schemes. For an unresolved consequential
contract, scope or ownership decision, prepare a concrete bounded proposal and
identify the needed decision; complete unaffected eligible exports. Do not ask
again for an ordinary source write already authorized by the request.

Start from the current project's available experience index and linked evidence.
Include relevant unresolved Improvement Records or scattered notes being resolved;
an open item exports a reviewed problem/next action, not a claimed proven lesson.
Consider unexported lessons and new support, counterevidence or changed conditions
for previously exported lessons; do not copy unchanged cases again. When the
index or history is unavailable, use accessible relevant session/task evidence
and state its coverage. A one-off export does not require retroactively creating
a ledger, nor does it justify claiming complete historical review. Preserve all
evidence and public/private rules above, even for a short request.

### Consumer To Shared Source Export

Export for common reuse resolves the canonical shared checkout and intended
asset owner first. An installed consumer copy or the current working directory
is not sufficient proof of that destination. Store a local source binding only
privately; portable sources use the logical `ai-assets` owner and relative
paths. A missing or unavailable shared checkout leaves the candidate at its
authorized private owner until the destination is resolved.

| Reusable result | Destination relative to the canonical `ai-assets` root |
|---|---|
| Reviewed public experience, reference case or reusable pending improvement | The subject-owned `evidence/agents/<component>/<record>.md` or `evidence/skills/<component>/<record>.md` and its row in `evidence/README.md`, following [Public Record Placement](improvement-record-contract.md#public-record-placement); the record owns its stable ID, content revision and independent work/knowledge/evidence/adoption states |
| Shared harness governance | The existing owner under `agents/policies/harness/`; flow, role, operation, profile and template changes stay with their respective owners under `agents/` |
| Skill behavior or resource change | The owning package under `skills/<skill-name>/`, following its quality and distribution contract |
| Reusable visual evaluation criterion | `agents/policies/review/design-evaluation.md` |
| Reusable interaction/UX evaluation criterion | `agents/policies/review/interaction-evaluation.md` |
| Project-specific experience or insufficient generalization | Private owner; `local` or `hold`, with no common-source write |

For design/UI or interaction/UX commonization, reconcile accepted reusable
checks and cautions into the relevant **Reusable Evaluation Notes** section of
the existing design or interaction evaluation policy. Update a matching entry
before adding a new one. Supporting improvement questions, comparisons and
outcomes may live under `evidence/agents/design-evaluation/` or
`evidence/agents/interaction-evaluation/`; those records do not replace the
evaluation criteria or duplicate their rule authority. A case-only export
retains reference experience without editing those normative sections. Actual
project evaluation reports remain with their existing task/evidence owners.

These source destinations are not consumer runtime dependencies. A reviewed
case can be exported without adopting a rule, and an authorized rule change
need not produce a redundant case. For `discard`, retain required historical
evidence at its owner; do not publish the discarded candidate as an adopted rule.
Preserve existing case IDs and filenames; a descriptive filename need not equal
the public ID.

Before a shared write, follow the record contract's format, revision/hash and
concurrency admission, then compare the public record ID, component, problem structure
and applicability with the existing collection. Reuse an existing matching
case; add new supported evidence or counterevidence without counting the same
event twice. A materially different predicate may warrant a separate linked
case. Narrow, supersede or withdraw contradicted claims with the reason while
preserving their historical observation. Recheck the current shared file before
writing so concurrent edits are not overwritten.

Keep the export decision, public ID, actual source path/revision or uncommitted
snapshot, and later publication/refresh/activation observations on the private
side. The public case and its index contain only public relationships. An index
row projects canonical record metadata; read the record's actual evidence kind,
execution status and limits before use.
Routine reflection may identify candidates; shared writes require the already
applicable common-edit scope and reviewed disclosure. An approval to accumulate
private experience alone is not an approval to export it.

## Cost, Stopping, And Compatibility

Record measured elapsed time, tool/task calls, retries, interventions and cost
when available, including the cost of recording and reflection. Use `unknown`
with a reason for unmeasured quantities; do not infer savings.

Stop when the declared scope is complete, a budget is reached, evidence cannot
be obtained, or remaining work is optional polish. Escalate the same failure
class after two attempts without meaningful progress under the existing
orchestrator rule. Report limits and the next discriminating check; do not
invent improvement to close the loop.

The capability is opt-in. Existing consumers and past runs need no migration,
new evaluator, automatically generated harness edits, or empty experiment record.
Use session-only reporting when persistence is unresolved. Installation does
not schedule experiments or load all historical cases into every task.
Configured stage hooks are duties performed by the agent using the imported
contracts; they are not a background collector or a guarantee that a runtime
loaded and followed them. Record actual hook execution and limits. Keep ordinary
retrieval/reflection bounded; an observed opportunity for comparison does not
authorize extra task replays or spending.
