# Improvement Record Template

Use the [record contract](../policies/harness/improvement-record-contract.md) and
[metadata schema](../schemas/improvement-record.schema.json) for reusable
knowledge, improvement work and public reference cases. One record owns the
question and its evolving conclusions/actions. Original stages, comparisons
and actual task outputs stay at their evidence owners.

Complete only applicable details, retaining unknowns with reasons. A supported
lesson needs evidence; an open question may have no supported lesson. A new
reference-only case uses not-applicable work basis/state/readiness. The example
below is private and unassessed, so it cannot enter the public collection as-is.
Replace its example ID/subject. Start the completed file with `---`, the JSON
object, then `---`; remove scaffold instructions and repair owner-relative links.
For a public record, use the contract's
[component-owned placement](../policies/harness/improvement-record-contract.md#public-record-placement)
and match IDs across the repository-level evidence collection before writing.

```json
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-example",
  "revision": 1,
  "audience": "private",
  "subjects": [{"kind": "harness", "key": "replace-with-logical-asset-key", "source_revision": null, "content_sha256": null}],
  "work": {"basis": "evidence-gap", "state": "open", "readiness": "not-assessed"},
  "knowledge": {"state": "not-assessed"},
  "evidence": {"kinds": [], "maturity": "none", "execution": "unknown", "coverage": "not-assessed"},
  "adoption": {"public_fitness": "not-reviewed", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": [], "supersedes": []}
}
```

## Context And Applicability

- Improvement question or recognizable situation, task/stage/component types:
- Affected component, current rule owner and responsible reviewer/coordinator:
- Primary record owner or shared concern when several subjects are involved;
  distinguish the improvement subject from the observing performer:
- Expected behavior, baseline behavior and how known; proposed method/change and why:
- Eligibility, exclusions, current compatible action and when to keep the baseline:
- Input sufficient to understand/reproduce; preserved problem structure, changed
  conditions and what cannot transfer after generalization:

## Evidence And Evaluation

| Stage/trial and event | Input/output owner and snapshot | Observation and maturity | Counterevidence or limits | Independent support or already counted |
|---|---|---|---|---|

- Original evidence or explicit absence; versions/fingerprints and actual
  source/import/installed/provided/use relationship, with observation time:
- Requested versus observed actors/model/tools/settings, context/isolation and
  independence/comparability limits; a logical role is not a runtime actor:
- Actual Result, Coverage/maturity and acceptance impact, or not assessed:
- Baseline/candidate differences, first outputs/actions and per-edit effects;
  link actual comparisons, otherwise `not assessed`:
- Passing, authorized-success, negative, no-change and regression controls;
  executed versus planned, counterexamples and unknowns:
- Conditions actually covered, including model/tool/contract assumptions, and
  evidence needed before a broader claim:
- For public accounts: evidence kind, disclosed execution `run / not run`, only
  reviewed generalized private claims and what readers cannot verify; expected
  results are separate from observations. Changed public/synthetic inputs never
  inherit a private outcome; public reproduction needs its own evidence:

## Work And Acceptance

- Next bounded action, scope and required checks with completion criteria:
- Date/event trigger, evidence/dependencies, action-specific authority and budget:
- Readiness or waiting/block reason; current active task/run/performer, or none:
- Conditions for partial completion, no-change, withdrawal and remaining checks:
- Pending scope/owner review for a candidate conclusion, or none:

## Outcome And Reuse

- Actual outcome or pending state; supported lesson, provisional hypothesis or
  none, with method/component and reasons. Normal-stage evidence may support a
  lesson without proving a harness edit caused it:
- Confidence tied to evidence/scope, not an invented probability; exclusions,
  tested conditions, generalization limits and invalidation/revisit triggers:
- Later stage references that rechecked applicability and their decisions:
- Remaining work and original evidence retention owner:
- Disposition: keep baseline / apply locally / propose promotion / hold /
  discard, with reason; actual adoption authority/scope and source change or none:
- Common-source decision, when requested: promote / local / discard / hold,
  with scope and reason; case acceptance does not adopt a rule:
- Public-fitness review: reuse value, necessary information, preserved meaning,
  standalone reading, sensitive details and revealing relationships, reviewed
  by a publicly appropriate reviewer/role. Human case acceptance and its
  authority remain separate; writing a record supplies neither:
- Canonical relative source destination, record/index reconciliation and partial writes;
  publication, consumer refresh and observed activation are separate facts:
- For private records, link the [exchange receipt](harness-local-store.md#exchange-receipt)
  at its private owner. Public projections exclude that link and all private
  IDs, paths, source hashes, original traces, associations and identifying review notes:

## History

- Created/updated dates, revision, change and reason, including newly added or
  corrected evidence; retain original observations and contrary outcomes:
- Matching record and duplicate/new-event decision; copied events add no support:
- Narrowed scope, supersession/withdrawal and related record IDs in the same
  audience; keep private-to-public associations in the private receipt:
- Index update or recovery gap after saving the record:
