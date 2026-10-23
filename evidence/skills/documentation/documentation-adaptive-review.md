---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-documentation-adaptive-review",
  "revision": 4,
  "audience": "public",
  "subjects": [{"kind": "skill", "key": "skills/docs-structuring", "source_revision": null, "content_sha256": null}, {"kind": "skill", "key": "skills/docs-shaping", "source_revision": null, "content_sha256": null}],
  "work": {"basis": "planned-work", "state": "open", "readiness": "not-assessed"},
  "knowledge": {"state": "not-assessed"},
  "evidence": {"kinds": ["generalized-private-observation"], "maturity": "unknown", "execution": "mixed", "coverage": "partial"},
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": [], "supersedes": []}
}
---

# Documentation skill adaptive-review follow-up

## Context And Applicability

This record is owned by the shared documentation-skill maintenance concern; both named skills remain improvement subjects.

Evaluate whether the September 2026 adaptive-review changes to docs-structuring and docs-shaping improve efficiency while preserving useful documentation review and cleanup. Both skills and paired end-of-task use are in scope; the frozen baseline below is a comparison basis, not a representative distribution or proven saving.

## Evidence And Evaluation

The pre-change sample below was reported as executed; the later adaptive-review
audit has no new output here. Evidence execution is therefore mixed, and the
private raw traces are unavailable to public readers. Source revisions and
content fingerprints were not captured; current files cannot reconstruct them.
The requested later Result/Coverage and per-edit effect remain not assessed.

### Comparison baseline recorded on 2026-09-18

The session audit searched 1,041 locally available log files across 17 identifiable working directories, covering 2026-06-16 through 2026-09-18. The cost figures below cover only three selected pre-change paired reviews (six child executions), not all discovered sessions. Each row combines one `docs-structuring` and one `docs-shaping` review; project labels and private source paths are omitted here.

| Review date | Model | Input tokens (including cached) | Cached input tokens | Output tokens | Estimated API-equivalent USD |
| --- | --- | ---: | ---: | ---: | ---: |
| 2026-09-14 | GPT-6 Astra | 1,110,223 | 989,568 | 13,473 | $2.87 |
| 2026-09-15 | GPT-5.6 Sol | 6,088,542 | 5,803,008 | 32,887 | $4.12 |
| 2026-09-18 | GPT-5.6 Sol | 12,890,290 | 12,379,776 | 58,711 | $8.17 |

- The selected three-pair sample has an unweighted mean of approximately **$5.05 per pair** and median **$4.12**. The earlier approximately $4 figure referred to the 2026-09-15 pair, not an established overall average. No population-wide mean was calculated.
- Preserve the valuation basis: Standard, short-context API rates in USD per million uncached-input / cached-input / output tokens were **4 / 0.40 / 20** for [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol) and **10 / 1 / 50** for [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), checked on 2026-09-18. Formula: `((input - cached) * input_rate + cached * cached_rate + output * output_rate) / 1,000,000`.
- Input is summed across unique response records, excluding replayed inherited usage; output already includes reasoning tokens. These are comparison estimates, not actual invoices or subscription charges. They exclude parent-agent work and do not model service-tier, long-context, cache-write, or tool-charge adjustments.
- At follow-up, retain this frozen-rate comparison separately from estimates using then-current prices, and compare matched scopes/models before attributing a difference to the skill changes. The three selected pairs are a reference baseline, not a representative usage distribution; savings and post-change quality remain unverified.

## Work And Acceptance

### Eligibility And Authority

Revisit around November–December 2026, after a few months of real use. The selected audit covers all locally available session stores and projects under the applicable access/analysis authority; it is not restricted to the current repo. Resolve comparison scope and budget before execution.

Readiness and task-specific budget must be established at selection. No active
task/run/performer is assigned by this record.

### Required Checks

- Around November–December 2026, after a few months of real use, evaluate the September 2026 adaptive-review changes for both usage and documentation quality:
  - Cover all locally available session stores and projects, not only the current repository; distinguish actual skill executions from catalog mentions, inherited history, and duplicated parent/child records. State date range, machine coverage, sample counts, and missing usage data; keep private transcripts and machine-specific paths outside this public repository.
  - Report invocation frequency, total usage, and per-run mean, median, and upper-tail usage for each skill and paired end-of-task reviews. Separate input, cached input, uncached input, and output without double-counting cumulative counters. Compare similar task scopes, document-set sizes, models, and loaded skill revisions before and after the change; distinguish token usage, any price-based estimate, and actual billed cost.
  - Inspect representative focused, whole-set, non-Git, paired-review, follow-up, and unchanged outcomes against their source documents. Check factual/status correctness, ownership, composition, preservation, useful findings, and whether broader exploration occurred naturally when needed without requiring a known local defect or an explicit full-audit prompt. State which outcomes were inspected rather than implying every run received semantic review.
  - Accept efficiency gains only when required coverage and useful document cleanup remain intact. Check for missed drift, unjustifiably narrow reviews, redundant rereading, unnecessary rewrites, and unsupported claims that unreviewed material is current. Refine only defects supported by the observed runs; do not reduce capability merely to lower token counts.

### Completion

Conclude the review with the usage and semantic-quality evidence required below, explicit coverage/gaps and comparable pre/post conditions. Accept an efficiency gain only with preserved required coverage and useful cleanup. Keep unsupported savings or unreviewed outcome claims unresolved; refine only defects evidenced by the runs.

## Outcome And Reuse

The later adaptive-review audit remains open. Retain the original frozen-rate basis separately from then-current-price estimates. No savings or post-change quality improvement has been established.

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
