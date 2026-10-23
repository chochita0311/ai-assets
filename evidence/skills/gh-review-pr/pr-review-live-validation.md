---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-pr-review-live-validation",
  "revision": 4,
  "audience": "public",
  "subjects": [{"kind": "skill", "key": "skills/gh-review-pr", "source_revision": null, "content_sha256": null}],
  "work": {"basis": "planned-work", "state": "open", "readiness": "not-assessed"},
  "knowledge": {"state": "not-assessed"},
  "evidence": {"kinds": [], "maturity": "none", "execution": "unknown", "coverage": "not-assessed"},
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": [], "supersedes": []}
}
---

# PR review controlled live validation

## Context And Applicability

Validate schema-v2 gh-review-pr publication, receipt accessibility, same-snapshot behavior and reply races on github.com and the current corporate GHES. These are controlled live checks whose individual writes retain explicit per-turn authorization.

## Evidence And Evaluation

No original task output or comparable execution is attached to this item.
Historical execution and the source revision/content fingerprint are unknown;
current package bytes cannot establish past use. Result, Coverage and change
effect are not assessed for the requested work. The record supplies a work
question, not a proven defect, success or reusable technique.

## Work And Acceptance

### Eligibility And Authority

Only when the user explicitly authorizes each relevant write in that turn, complete the controlled live checks below. Resolve each host and safe review target; preparation, a prior turn’s authorization or this record do not authorize a new write.

Readiness and task-specific budget must be established at selection. No active
task/run/performer is assigned by this record.

### Required Checks

- Only when the user explicitly authorizes each relevant write in that turn, complete controlled schema-v2 live checks on github.com and the current corporate GHES.
  - Publish one safe test review on each host and inspect the two-column receipt, conditional warning with one bullet per gap, blank-line hierarchy, linearized plain-text reading order, restrained `✅` semantics, and always-expanded evidence visually and with assistive-technology-oriented inspection.
  - Verify that an explicit publish request creates exactly one review and that an exact same-snapshot rerun returns `noop-existing-snapshot`.
  - Verify that a newly confirmed finding or summary-count change on an already reviewed same snapshot returns a corrected draft without writing or bypassing the snapshot guard.
  - Forward-test `reply` after the PR head advances; the result must distinguish the original review head from the current head and stop on a preparation-time race.

### Completion

Completion requires observed results on both hosts for the publication/receipt checks, exact-snapshot no-op, corrected-draft-without-write and advanced-head reply/race branches below. Retain untested host, accessibility or concurrency branches as gaps. Never infer live success from source/schema checks.

## Outcome And Reuse

Controlled live validation remains open. No review or reply has been posted by this consolidation; no future live write is preauthorized.

## History

- Revision 1, 2026-10-21: retained the existing unresolved work and available
  historical evidence in the common record; no execution or closure occurred.
- Revision 2, 2026-10-21: resolved the item into its specific question, evidence,
  eligibility, required checks and closure conditions. Preserved original task
  predicates and any frozen baseline; removed dependence on a separate work list.
- Public fitness: author reviewed the generalized text and metadata for private
  identifiers, dependencies and revealing relationships. This is disclosure
  review, not validation of the pending work. Source editing establishes no
  publication, consumer refresh or observed runtime activation.
- Revision 3, 2026-10-23: moved to component-owned skill evidence with the
  same record ID, task conditions and assessment states. Updated discovery and
  applicable links; no execution, closure or new empirical support was added.
- Revision 4, 2026-10-23: moved into the repository-level evidence layer,
  retaining the same subject ownership, record ID, conditions and assessment
  states. This location change adds no execution, closure or empirical support.
