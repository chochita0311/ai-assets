---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-documentation-content-role-validation",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {
      "kind": "skill",
      "key": "skills/docs-structuring",
      "source_revision": null,
      "content_sha256": "b62259c72c92069a9b7105aeed4dbfed0329c17689bb7a5fd53bf954f89aacef"
    },
    {
      "kind": "skill",
      "key": "skills/docs-shaping",
      "source_revision": null,
      "content_sha256": "0702d58b139084553fbbc85efdf81ec4d2bb573a5f8a77a3513d337c2b395e6e"
    }
  ],
  "work": {
    "basis": "evidence-gap",
    "state": "open",
    "readiness": "waiting"
  },
  "knowledge": {
    "state": "supported"
  },
  "evidence": {
    "kinds": [
      "static-observation",
      "generalized-private-observation"
    ],
    "maturity": "fresh-forward-test",
    "execution": "run",
    "coverage": "partial"
  },
  "adoption": {
    "public_fitness": "approved",
    "case_status": "draft",
    "rule_status": "implemented"
  },
  "relations": {
    "related": [
      "ir-documentation-adaptive-review"
    ],
    "supersedes": []
  }
}
---

# Documentation content-role validation

## Context And Applicability

This record belongs to the shared documentation-skill concern and retains both
skills as subjects. It asks whether content-role and reader-need checks keep
current explanations distinct from active work and execution evidence while
preserving information needed to understand, use or reproduce the subject.

A review of private historical use found both mixed-content outcomes and
successful separation. Some motivating cases used earlier revisions; they do
not establish a current-package failure or its cause. A shared topic can hide
different content responsibilities, and tidier headings alone can leave that
mixture in place. Preserving meaning also need not mean copying every source
fragment into one explanation.

The user authorized bounded improvements to both skills. The adopted design
keeps ownership and placement in [structuring's layer model](../../../skills/docs-structuring/references/layer-model.md#content-roles-and-reader-needs)
and passage composition in [shaping's method](../../../skills/docs-shaping/references/method.md#content-roles-and-reader-needs),
with self-contained procedures in each package. The executing agent judges
placement against the reader's task; the reader is not assigned that review.
A log may be authoritative evidence without owning the current rule. Accurate
traceability alone does not justify execution strings in reader-facing prose;
compatibility conditions, identifier formats and exact reproduction values can
still be essential there.

Existing scope, mode, preservation and intervention gates remain applicable.
Single-file selection does not authorize a working log inside an explanation;
an intentionally mixed working document can retain clearly scoped roles.
Unresolved ownership retains the original material and reports the gap.
Session receipts reuse authorized record owners rather than accumulating in
guides or generating new logs by default. Intake keeps its primary-artifact
and downstream-authoring boundaries. The package files own these instructions;
this record owns the observed evidence, counterevidence and remaining work.

This is a different question from the related [September adaptive-review
usage/cost audit](documentation-adaptive-review.md). That record's acceptance conditions, historical valuation
basis and open state are unchanged; these trials do not measure efficiency.

## Evidence And Evaluation

### Source identity and evidence availability

The comparison baseline is repository commit
`17e414f69d3323df98c2191b217fb4c3241e0350`. The tested candidate was an
uncommitted snapshot of the eleven package files, with combined content
SHA-256 `c98c818bdeb6af28cfdd73dd8b3f0d856fc084210a47131e575644856cad1631`.
It is not attributed to the baseline commit. Subject source revisions are null
because no candidate commit existed during execution; their content
fingerprints identify each tested package separately.

For each subject fingerprint, hash every regular package file with SHA-256,
map package-relative POSIX paths to lowercase digests, serialize that map with
Python `json.dumps(mapping, sort_keys=True)` using its default separators and
UTF-8 encoding, then hash those bytes. The combined fingerprint uses the same
procedure with repository-relative paths for both packages. These are public
asset-content identities, not hashes of private cases or traces.

The trials below actually ran on synthetic document inputs in private local
workspaces. This is a reviewed generalized account of those executions, not
publicly replayable evidence or an illustrative scenario relabeled as a run.
Original observations, outputs and tool traces remain associated with private
session history; task-owned staging copies were removed after evaluation.
Private source identities, paths, associations and traces are not published.
Public readers cannot independently verify the raw outcomes from this record
alone. Generalizing the account does not create another observation or transfer
an outcome to a changed public fixture.

### Executed checks and observed results

| Stage | Executed scope | Observation and limits |
|---|---|---|
| Author checks | Seven synthetic cases and two unchanged follow-ups | Passed the bounded author checks. The author knew the proposed change; these are not independent forward tests or additional producer sessions. |
| Initial independent source review | Three no-history reviewers, separately using structuring, shaping and refinement; all eleven baseline/candidate files | No supported current-delta defect candidate. Review agreement establishes neither reliable execution nor completion acceptance. |
| Matched ordinary-task execution | Two no-history producers, one per version; eleven tasks each | Both versions met the inspected task criteria. Exact conditions, distinct identities, evidence limits and authorized actions were preserved. Twenty-two task outcomes are not twenty-two independent sessions. |
| Single-package execution | Two additional no-history producers; one candidate package body per producer and three tasks each | Both handled existing-record relocation, an unresolved owner and an intentional single-file working note. Six outcomes close the dual-body-loading confound only for these three task classes. |
| Independent outcome evaluation | Refinement reviewer inspected every task, raw input/output, report and supplied access trace from the twenty-eight producer outcomes | No actual outcome failure or justified package correction. This is evaluation of the same executions, not new supporting executions. |
| Static validation | Both package validators, 34 local links/anchors, four YAML documents, metadata alignment, whitespace and thirteen complete unchanged mode/scope/approval sections | Passed. Five existing availability-qualified cross-skill-reference notices remain informational. These checks establish the inspected static properties, not runtime reliability. |

Both `SKILL.md` entry files and their required procedural references were loaded
in each matched producer context; optional example files were not loaded.
Individual-skill task choices therefore shared exposure to the neighboring
instructions; isolated package-body availability was checked only in the later
single-package follow-ups.

The eleven matched tasks covered: a guide/work/evidence set, passage reshaping
with an existing record, exact reproduction reference, an intentional mixed
working note, a guide-only unresolved owner, intake with existing work/evidence
sources, a paired unchanged recheck, an explicitly requested new review receipt,
implicit composition routing, implicit ownership routing and a typo-only
negative routing case. Required execution commands were document content and
were not run as product/runtime checks.

Both matched producers preserved mandatory compatibility, identifier and
safety conditions in explanation; kept exact source and input fingerprints
with their separate subjects; retained passed/skipped counts and environment
limits; kept proposed work conditional and unapproved; respected explicit
persistence; and avoided duplicate closeouts. In the unresolved-owner case,
the baseline clarified a heading and reported the missing destination, while
the candidate preserved the file unchanged and explicitly retained the
placement issue. Both reported the gap: this is not a failure-to-success
transition or causal proof of improvement.

In the additional single-package case, the published signing-key identifier
and an internal build commit had the same forty-hex-character shape. Each
producer kept the exact public identifier beside its executable use in the
guide and moved the build/archive identities and full dated observation to
the existing evidence owner. Minimum version, binding preconditions, upload
prohibition, offline-check result and the untested-online limitation survived.
The unresolved owner stayed unresolved without deleting evidence or inventing
a destination; the intentionally mixed note stayed unchanged. No neighboring
skill body was supplied or read in these follow-ups.

All producers used the recorded `gpt-6.1-sol` model at `max` reasoning effort.
The reviewed worker binding was also `gpt-6.1-sol` / `max`. Producers received
raw tasks and factual sources, not the implementation conversation, evaluator
answer key, other producer outputs or prior author outputs. Loaded file hashes
matched their assigned snapshots. Recorded reads stayed in assigned workspaces;
no prohibited source, history, network or evaluator access appeared in the
inspected traces. This is trace evidence, not an OS-enforced read sandbox.

**Result: PASS for the bounded static and task checks. Evidence Coverage:
partial.** Highest evidence: fresh ordinary-task executions, with matched-input
version comparison and candidate-only single-package follow-ups. Each version
or single-package packet used one producer context across multiple tasks.
Common inherited system/developer guidance and skill catalog metadata were
visible and were not completely frozen. Later routing requests reused loaded
skill bodies; they are not cold-discovery tests. Standalone follow-ups had no
standalone baseline comparison. Individual edit effects, population-wide
quality gains, cost savings and stable causal improvement are not established.

## Work And Acceptance

Completed work comprises the authorized eleven-file package update, aligned
metadata/checklists/examples, bounded author checks, independent source review,
matched executions and single-package follow-ups. No package correction was
justified by the independent reviews. There is no active experiment or assigned
performer in this record.

The remaining work is an evidence gap, not an unimplemented package fix. On a
new ordinary documentation-maintenance request, or a concrete recurrence of
mixed-content drift, select a small real guide/work/evidence set and establish
task-specific authority and budget before testing. Readiness is waiting for
that evidence and selection; this record, its related ID or a date does not
authorize a replay, publication or broader source change.

The next bounded check should pin source files, model/settings and effective
inherited instructions; retain original inputs, outputs and traces at their
private owner; compare compatible scopes; and verify all unique assertions,
conditions and source/destination identities. Cover individual-package intake,
active-work reconciliation, follow-up/persistence and routing, genuinely cold
or ambiguous discovery, ordinary authorized relocation, major-rewrite refusal
and explicit authorization, and relocation failure/recovery. Also inspect
actual accumulated documents and repeat independent executions before making a
stability claim. Include exact-value, intentional-mixed-document, unchanged
and authorized-success controls; unrun required checks remain unrun.

Close this broader gap only with accessible evidence that the original mixture
no longer recurs within the selected scope, required meaning and values remain,
authorized work completes without unnecessary refusal, valid no-change cases
stay unchanged, and relevant controls pass. Narrow or withdraw a conclusion
if new evidence contradicts it. The separate adaptive-review audit retains its
own eligibility, scope, budget and closure conditions.

## Outcome And Reuse

Supported conclusion: the explicit role/reader distinction was executable in
the observed fixtures, including when each package body was supplied alone;
no material regression was observed in the matched tasks. The baseline also
passed. Keep the bounded distinction and its preservation conditions, without
claiming that these edits caused a general improvement or guarantee clean
future documents. Required identifiers are judged by function and placement,
not by whether their strings look technical.

The package source changes are implemented under user authorization; a separate
human acceptance of this public case is not recorded. Public fitness was
reviewed for reusable meaning, standalone readability and exclusion of private
facts, identifiers and revealing relationships. Only generalized observations,
synthetic-task descriptions and public asset identities are included.

Source changes, Git publication, consumer refresh and observed use remain
separate facts. Existing local installations pointed at the canonical package
sources through symlinks, so changed bytes were available there; ordinary
already-running sessions were not cold-launch validated. Fresh test producers
loaded frozen task copies. No refresh or activation is claimed for other
consumers. The enclosing Git commit and remote ref, rather than this narrative,
are evidence of publication.

This file owns the improvement question, knowledge, work and record history.
Its common catalog row provides discovery only and owns no independent state.
Private original session history remains the evidence owner; temporary
reconstruction or staging is not a durable reference. No private-to-public
association is published.

## History

- Revision 1, 2026-10-31: retained the content-role decision, its reasons,
  actually executed synthetic checks and independent review, favorable and
  equivalent baseline outcomes, and the unresolved real-use/stability scope.
  Linked the distinct adaptive-review question without changing its work state
  or counting the same event as new support.
- Before publication, two additional closeout reviewers examined the thirteen-file
  publication set with supplied session context and prior evidence. The record
  was corrected to distinguish ownership from catalog discovery and explicitly
  state the matched producers' exposure to both skill bodies. These reviews and
  wording corrections add no behavioral trial and change no tested package bytes.
