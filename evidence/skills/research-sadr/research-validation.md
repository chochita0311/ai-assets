---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-research-sadr-validation",
  "revision": 3,
  "audience": "public",
  "subjects": [
    {"kind": "skill", "key": "skills/research-sadr", "source_revision": null, "content_sha256": null},
    {"kind": "harness", "key": "harness/flows/research.md", "source_revision": null, "content_sha256": null},
    {"kind": "harness", "key": "harness/operations/research-runner.md", "source_revision": null, "content_sha256": null},
    {"kind": "harness", "key": "harness/policies/research-governance.md", "source_revision": null, "content_sha256": null},
    {"kind": "harness", "key": "harness/policies/workflow-governance.md", "source_revision": null, "content_sha256": null},
    {"kind": "harness", "key": "harness/roles/orchestrator.md", "source_revision": null, "content_sha256": null},
    {"kind": "harness", "key": "harness/ADOPTION-GUIDE.md", "source_revision": null, "content_sha256": null},
    {"kind": "runtime", "key": "agents/adapters/codex/custom-agents/research_worker.toml", "source_revision": null, "content_sha256": null},
    {"kind": "resource", "key": "agents/adapters/codex/README.md", "source_revision": null, "content_sha256": null}
  ],
  "work": {"basis": "evidence-gap", "state": "open", "readiness": "waiting"},
  "knowledge": {"state": "candidate"},
  "evidence": {
    "kinds": ["static-observation", "generalized-private-observation"],
    "maturity": "fresh-forward-test",
    "execution": "run",
    "coverage": "partial"
  },
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": ["ir-harness-mapping-v10-validation"], "supersedes": []}
}
---

# Research SADR standalone and harness validation

## Context And Applicability

What evidence supports standalone and harness-mediated independent research,
including the optional `research_worker`, and what remains unverified? This
single acceptance question belongs to the primary method owner,
[research-sadr](../../../skills/research-sadr/SKILL.md). Harness and runtime
subjects remain in this record because loading, delegation and observed
activation affect that question; the same events are not separate evidence in
multiple owner folders.

The implemented method serves open questions in general domains: framing the
decision, finding useful alternative explanations and methods, inspecting raw
evidence, testing claims, adjudicating criticism and reporting a supported
answer or justified null finding. It works without a harness, a particular tool
or an independent worker; a narrow lookup or small defined correction does not
require this research process. A missing capable independent actor permits
explicit self-review while any acceptance requiring that independence stays
open. These are current method duties, not claims of demonstrated general
research effectiveness.

The method selects useful SADR dimensions rather than requiring all four:
Speed seeks lower time and cost while preserving needed quality and independent
checks; Altitude connects the requested artifact's outcome to needed tools,
materials and observable decision criteria without enlarging scope or authority;
Depth connects expert work, raw
material, methods/instruments and external checks; Range transfers useful
methods from other fields only with their assumptions and data conditions.
Speed is optional, and speed alone establishes no truth. Ambitious goals do
not promise findings; failures and limits must remain grounded in evidence.
Better results need not mean a larger scope or more deliverables.

The [research flow](../../../harness/flows/research.md),
[runner](../../../harness/operations/research-runner.md),
[research governance](../../../harness/policies/research-governance.md),
[shared workflow governance](../../../harness/policies/workflow-governance.md)
and [orchestrator](../../../harness/roles/orchestrator.md) retain sequence,
invocation, lifecycle, shared authority/resources and primary control. They
consume the complete pinned method at `docs/agents/methods/research-sadr/`
under the [adoption contract](../../../harness/ADOPTION-GUIDE.md#optional-research).
A discovered global skill of the same name does not substitute for that local
package. Harness Improvement is independently selected, and research does not
require delivery artifacts for each hypothesis. The
[Codex adapter](../../../agents/adapters/codex/README.md#research_worker-optional)
owns the optional binding and installation. None of these delegates the
primary's scope, authority, persistence, integration or final acceptance decisions.

Actual caller or environment limits remain binding in their recorded scope;
retain each limit's source. Agent estimates are revisable planning checkpoints,
not automatic whole-task stopping or quality-FAIL criteria. The primary may revise its
own allocation within existing authority and actual caps, with reasons and
expected information gain, without approval solely for changing that estimate;
a critic may challenge its adequacy. Cumulative usage, pending commitments and
closeout capacity carry across sessions and runs. Sufficiency depends on
evidence, material unresolved concerns, information value and acceptance. A
query ceiling stops further queries, not other permitted analysis, and a
worker's return boundary does not establish whole-task completion. These
existing [resource rules](../../../harness/policies/workflow-governance.md#resource-governance)
remain distinct from the historical trial limits below.
Further passes need useful new information or a material unresolved concern;
the same evidence and method do not justify endless repetition.

## Evidence And Evaluation

### Evidence basis and identity

The following are generalized reports of actual private executions using
synthetic research inputs, plus inspection of the public source contracts.
They are not public replay fixtures or unrun illustrative examples. For the
earlier synthetic trials, retained conversation and handoff reports describe the
observations; original task-owned trial logs and fixtures were removed after
their prior audit and recovery purposes ended. The later application audit below
retains its frozen sources, fixtures, raw results and review registers in private
archives. This record does not reconstruct the deleted logs or expose private
identities, source paths, hashes, traces or their associations. Readers can
inspect the current contracts but cannot independently replay these executions
from this record.

Subject revisions and fingerprints are null because this account spans evolving
source snapshots and the retained reports do not establish one exact public
commit and content fingerprint for each subject across those observations.
Current files and any later commit must not be attributed retrospectively to
every trial. Reported input/installed-copy hash checks below remain historical
observations, not a complete public import manifest. `fresh-forward-test` is the
highest reported historical stage, with the narrower conditions of each trial
preserved below. `run` describes those executed observations; it neither claims
new research/runtime trials during this record reconciliation nor includes future checks
in Work And Acceptance. Overall Evidence Coverage remains **partial**.

### Early method and resource trials

The first implementation phase reports separate author/refine review, general
research tasks and temporary adoption/resume checks, including passing
source/task checks within their reported scope and partial overall coverage.
One research trial exceeded
its **1,440-second** trial limit by **25.2 seconds**. Its strict aggregate
**FAIL** remains, separately from useful findings. An indirectly exposed research
fixture and a harness finish instruction also limit the independence and
intervention claims for that phase. The limit is test history, not a default
research cap; later planning rules do not erase the failure. These observations
do not establish comparative improvement, stability or enforced timeouts.

Later general-domain tasks observed continued research and validation after an
agent-set estimate, and continued local analysis after an actual query limit
prevented further queries. Research arithmetic was independently reproduced.
A predeclared rubric's particular visitor/operating-hours calculation was
absent from the producer output and remains an unmet rubric detail. The task
and method did not require that exact formula and the producer supplied other
relevant analysis, so rubric over-specification is distinct from a demonstrated
task failure. Reused synthetic data, self-review, no earlier-version control
and incomplete independent visibility into full context/tool history prevent
claims of general stability, comparative benefit, quota enforcement or successful
independent research-reviewer operation from these tasks.

### Local method loading

Two fresh-context producers followed frozen research-only and
research-plus-improvement consumer payloads through their entry points,
runner, common control, governance and local method. Both analyzed the same
synthetic ticket data. The reports distinguished files checked only by hash
from files recorded as semantically read; the primary separately checked
recorded hashes, payload immutability and arithmetic. The analyses separated
an increased overall average from improvement within difficulty groups,
adjusted for case composition, considered alternatives and causal limits, and
proposed a next observation.

Both paths ran without additional delivery artifacts or a global skill install.
An unconfigured private Improvement binding did not block research; no stored
experience or source-change effect was claimed. Investigation, criticism and
judgment within each run were **self-review**, despite the fresh producer
contexts. The trials did not establish an independent internal reviewer, new
validation sample, full tool trace, actual model binding, OS isolation or
general research utility. Each producer received one progress-status
intervention; initial outputs and later expression improvements remained
distinguishable. The task was not changed after seeing results. No numeric
deadline or cost cap was supplied or added after seeing results, and unmeasured
usage remained unknown. This supports local
payload use, not real consumer rollout or comparative efficacy.

### Fresh research, criticism and informed correction

A later frozen-source audit ran standalone research and a **13-file
research-only consumer payload** in separate fresh contexts. A critic initially
saw only raw evidence; a separate adjudicator later received the results. The
adjudicator found a confusion between **processing time and whole-visit time**
and returned it to the authors. Both research paths then reanalyzed changed
staffing data, updating affected conclusions while preserving initial
observations, counterevidence and history.

The retained audit reports static **PASS** and executed behavior **PASS WITH
SUGGESTIONS after correction**, with partial coverage. The initial exploration
and raw-evidence criticism are distinct from informed adjudication and
follow-up. This was package-direct standalone loading before the optional
runtime installation; a user-level discovery entry was not present at that
checkpoint. The existing named roles could leave ordinary independent research
at self-review fallback. That observation motivated an optional suitable research
binding, not mandatory permanent critics/judges or an expansion of the code
reviewer's role. The trial itself changed no reusable source or runtime setting
and did not establish real rollout, long-term usefulness or multi-agent superiority.

### Optional worker installation and observed activation

The subsequent source change added
[`research_worker`](../../../agents/adapters/codex/custom-agents/research_worker.toml)
and complete standalone-package discovery/installation guidance. The configured
binding is **`gpt-6.1-sol` / `max`**. The four method files, three existing worker
bindings and research flow/governance were unchanged by that addition. Separate
author/refine review reports passing source-contract checks, three skill
validators, renderer freshness and seven offline audit tests. Those checks do
not establish runtime activation.

The private installation reports describe a regular-file worker copy in the
initial selected runtime home and a shared skill-discovery link to the maintained
source package. This is separate from harness adoption's pinned local method.
Fresh CLI trials observed explicit research invocation, selection of the research
role without the caller naming it, informed disputed-claim adjudication, and a
simple-question negative control. Later stdio event evidence exposed child
identity, start/completion, **`gpt-6.1-sol` / `max`**, actual child commands and
returns. That later trace supports those event trials only; it does not turn
earlier configuration or worker self-reports into independently observed runtime
facts. A missing cost source was neither replaced by another service nor used
to invent a cost conclusion.

The last original worker return omitted calculable raw-input hashes, describing
uncomputed values as unexposed. Its provenance-completeness check was **FAIL**.
The primary subsequently computed hashes matching the originally frozen inputs
and repaired the execution-evidence record: that **post-hoc repair passed**.
The original return still failed, and no corrected-worker rerun occurred in
that case. Numerical, causal, source-judgment and missing-source handling checks
passed with partial coverage. The defect concerns the response's source record,
not the entire installation or every research conclusion. The existing method
already required obtainable fingerprints, so this did not justify a duplicate
source rule.

A later correction covered an initially omitted **second approved runtime
home**. The source and both regular-file worker copies had equal SHA-256 values;
existing configuration, the other three workers and the shared skill package
were preserved. A new session in that second home observed simple-question
non-delegation, independent-research role selection, child start/completion and
**`gpt-6.1-sol` / `max`**. The child actually calculated two raw-file hashes and
the method-manifest hash in three successful commands. A separate verifier
passed 14 checks of fixed logs, files and hashes. This case's relevant checks
were **PASS**, but the caller explicitly reminded it to report source hashes
and distinguish uncomputed from inaccessible values. Those changed conditions
make it a separate case, not a comparable rerun, a reversal of the original
FAIL or evidence of general stability improvement.

Actual live app/connector use, enforcement of individual feature reductions,
complete hidden input/history visibility and long-term research quality remain
unverified. Role restrictions and configuration do not prove an independent OS
sandbox. Reasoning-context independence, method diversity, source independence
and untouched validation data remain separate; fresh contexts or same-data
recalculation do not establish all four.

### Later producer/consumer investigation with frozen repair rounds

A later generalized private application audit applied the complete SADR method
and required references from a fixed source snapshot. The primary framed
competing causes for broken text, reconstructed state and background execution;
source and runtime probes distinguished decoding, glyph coverage, cell width,
parser continuation and input ownership instead of treating one visual symptom
as a single encoding diagnosis. Reference application and dependency observations
were kept separate from assumptions about an installed engine.

Fresh bounded inquiries received frozen source and normative requirements before
prior reviewer conclusions. They returned source-backed candidates and requested
small discriminators; the primary performed implementation and actual tests.
Useful distinctions included an unopened model versus a focused browser cursor,
ordinary text flood versus unread automatic replies, and a never-reading peer
versus cooperative duplex progress. Repair rounds found integration defects in
previously proposed fixes. Each round retained its fixed input, first return,
contrary evidence and later adjudication; follow-up was informed confirmation,
not another independent discovery.

One normative contract included earlier delivery claims, and one reviewer briefly
consulted a live-tree reference outside the intended frozen packet. Those limits
were disclosed, the live outputs excluded from candidate evidence, and context
independence was not reported as complete. Full matching manifests did not erase
those exposures or prove an independent OS sandbox. A later timezone cause was
found by the primary, not retroactively credited to a fresh worker.

The product checks ran privately; this public projection and the related
[review-challenger account](../../agents/codex/review-challenger-validation.md)
are not public replays or separate independent support. The final scoped product
result passed with explicit environment limits after correction. No controlled
single-agent/multi-agent or old/new-method comparison established effectiveness,
universal stability or cost benefit. This audit supplies additional method-use
and adversarial-test evidence while leaving the broader acceptance and runtime
proof below open. The applied method files had obtainable fingerprints in the
private receipt; that does not fill the unknown historical fingerprints of the
earlier trials above.

## Work And Acceptance

The source implementation is complete within its reported scope; broader
research acceptance remains **open**, **waiting** for a selected new consumer or
runtime target, or genuinely new comparative evidence. No runtime run, performer,
deadline or future budget is assigned by this record. It does not schedule
research, install anything or require a standing judge. The primary resolves
the selected target, authority, evidence access, actual limits and suitable
actors before dependent execution under the existing owners.

For an authorized new target, perform one bounded acceptance assessment: fix the
question, inputs, method and instruction revisions **and** fingerprints, record
source/import/installed/used identities, actual actor and exposed binding/history,
tool access, resource use and enforcement limits. Verify the complete local
method or requested discovery path, then select controls appropriate to the
remaining claim: alternative framing in answer-isolated exploration; a
legitimate null challenge and a false critique; informed adjudication with both
sides' evidence; changed-input reanalysis preserving history; actual resource
limits versus planning estimates; a simple-question non-delegation control;
obtainable source fingerprints and an honestly reported missing source. If
approved connector-only evidence is part of the target, observe that actual
access instead of inferring it from inherited configuration. Keep each result
and coverage gap explicit. These checks are pending, not newly executed evidence.

A comparative-effect claim requires a separately authorized comparison with
fixed question, materials, constraints, model/tool access, applicable instructions
and total resource accounting. Compare single-context review, fresh criticism
and criticism plus adjudication only where those conditions make the comparison
meaningful. Predefine task-specific criteria for valid omissions, false positives,
unnecessary revisions, decision-relevant insights, repeated user prompting and
time/token/tool/cost use; disclose measurement limits and changed conditions.
Do not infer the value of independent contexts from unequal configurations or
reuse exploration material as untouched validation. No improvement rate or
default research budget is established by the historical trials.

Close only the selected acceptance scope when its required evidence and controls
pass, or retain an explicit partial/no-change/withdrawal decision with its reasons.
Missing independence or a required source stays an acceptance gap. Preserve
original failures and historical usage; newer success with changed inputs does
not erase them. Revisit affected conclusions after method, binding, tools,
permissions, inputs or assumptions change, or when contrary outcomes arrive.

## Outcome And Reuse

The bounded evidence supports that the method was used standalone and through
local harness payloads, that criticism and informed adjudication corrected a
material measurement distinction, and that optional named-worker activation was
observed in later local cases. A useful provisional lesson is to keep source
completeness, installed-copy equality, activation, response provenance and
research efficacy as separate checks. The original missing-hash FAIL and later
reminded PASS show why an installation or narrow numerical success cannot stand
in for complete provenance or stable behavior. The retained reports support
these scoped observations; unavailable raw replay material and the stated
interventions limit confidence beyond them.

General efficacy, comparative advantage, reduced long-term prompting, real
consumer rollout and full runtime enforcement remain unassessed. Keep the
implemented method and optional adapter within their existing contracts; this
record proposes no additional normative rule or model substitution. Its
cross-asset placement follows the method owner's one acceptance question.

The primary reviewed this public projection for reusable meaning, complete
qualifications, standalone reading and exclusion of private identities, paths,
source hashes, traces and revealing relationships. Public fitness is approved;
separate human case acceptance is not requested. The canonical record is
`evidence/skills/research-sadr/research-validation.md`, listed once in the common
catalog. Its related mapping record owns the distinct consumer-compatibility
question; a linked event is not additional independent evidence. Record admission
establishes neither external publication nor consumer refresh. Historical local
activation remains limited to the cases above. Original trial scratch was already
removed; retained generalized observations have no durable temporary-path dependency.

Revision 2 retains the earlier method, worker-installation observations, failures
and open comparative acceptance. It adds one later observed investigation with
honest independence, caller-budget and repair-round boundaries. No skill,
research governance, runtime binding or installation changes are made. Public
fitness was reviewed by the primary for standalone meaning and disclosure;
source integration alone establishes no public reproduction or guidance effect.

## History

- **2026-11-02 — revision 1:** Prepared one research-acceptance record from
  retained reports of method, local-payload and optional-runtime trials. Preserved
  the early 1,440-second bound failure, self-review versus fresh/informed stages,
  metric correction and changed-input reanalysis, original missing-hash failure,
  post-hoc repair and later reminded success as distinct observations. Recorded
  partial coverage and waiting follow-up without assigning execution. This
  migration is not a new trial, comparable rerun, public replay or evidence of
  general research improvement; it does not supersede the contrary outcomes.

- 2026-11-12 — Revision 2. Added a later frozen application investigation, discriminating runtime checks and informed repair rounds. Preserved initial-review exposures, primary discovery, earlier failures and all open acceptance states; no source-method or binding change.

- 2026-11-12 — Revision 3. Scoped the deleted-log statement to the earlier synthetic trials and clarified private archival of the later application audit. Preserved historical deletion, unknown historical fingerprints and the public-replay limit; no new execution or state change.
