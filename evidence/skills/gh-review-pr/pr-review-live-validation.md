---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-pr-review-live-validation",
  "revision": 5,
  "audience": "public",
  "subjects": [{"kind": "skill", "key": "skills/gh-review-pr", "source_revision": null, "content_sha256": "eca6c95927d8395b1266740e3ecef61e4605ba95eec6f7ba6b35173114208595"}],
  "work": {"basis": "planned-work", "state": "open", "readiness": "not-assessed"},
  "knowledge": {"state": "not-assessed"},
  "evidence": {"kinds": [], "maturity": "none", "execution": "not-run", "coverage": "unavailable"},
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": ["ir-pr-review-semantic-corpus"], "supersedes": []}
}
---

# PR review controlled live validation

## Context And Applicability

Validate schema-v2 gh-review-pr publication, receipt accessibility, same-snapshot behavior and reply races on github.com and the current corporate GHES. These are controlled live checks whose individual writes retain explicit per-turn authorization.

## Evidence And Evaluation

No live task output or comparable live execution is attached to this item.
Earlier historical use was not established; the 2026-10-31 work performed no
GitHub/GHES review publication or reply. The source fingerprint identifies the
uncommitted package using the algorithm in the [semantic record](pr-review-semantic-corpus.md#source-identity-and-completed-corrections),
not an installed or live-tested revision. `source_revision` is null because
the candidate was not committed when evaluated.

The semantic record owns the observed local lock reproduction and two ordinary
delegated draft tasks. They supply no live evidence here and are not counted
twice. Live Result is not assessed and Evidence Coverage is unavailable;
source/schema checks cannot establish provider visibility, receipt behavior,
accessibility, delegated publication authority handling or server consistency.

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
- Exercise the [publication coordination boundary](../../../skills/gh-review-pr/references/github-publishing.md#publication-concurrency) with controlled overlapping callers sharing the supported local lock. Verify one submitted review, a competing safe stop, and a later same-snapshot no-op. Test Windows and other relevant lock-capable filesystems separately; do not extrapolate the observed Unix resource checks.
- For writers outside that shared user/home/filesystem boundary, establish caller-side coordination or keep the review in draft. No cross-host lock is supplied. Separately verify an explicitly publication-authorized full-task delegation while retaining reserved decisions and the original current-request authority.

### Completion

Completion requires observed results on both hosts for the publication/receipt checks, exact-snapshot no-op, corrected-draft-without-write and advanced-head reply/race branches above, plus the selected coordination/platform and delegated-publication controls. Retain untested host, accessibility or concurrency branches as gaps. Never infer live success from source/schema checks.

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
- Revision 5, 2026-10-31: identified the revised source candidate, separated
  completed offline evidence from unrun live work, and retained local-writer,
  platform, cross-host and full-task publication controls. No live review or
  reply was executed or preauthorized; public-fitness review covers only the
  generalized source and pending checks.
