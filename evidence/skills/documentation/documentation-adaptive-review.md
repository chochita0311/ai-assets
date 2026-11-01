---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-documentation-adaptive-review",
  "revision": 6,
  "audience": "public",
  "subjects": [
    {
      "kind": "skill",
      "key": "skills/docs-structuring",
      "source_revision": null,
      "content_sha256": null
    },
    {
      "kind": "skill",
      "key": "skills/docs-shaping",
      "source_revision": null,
      "content_sha256": null
    }
  ],
  "work": {
    "basis": "evidence-gap",
    "state": "open",
    "readiness": "waiting"
  },
  "knowledge": {
    "state": "candidate"
  },
  "evidence": {
    "kinds": [
      "generalized-private-observation",
      "static-observation"
    ],
    "maturity": "observed-stage-execution",
    "execution": "run",
    "coverage": "partial"
  },
  "adoption": {
    "public_fitness": "approved",
    "case_status": "not-requested",
    "rule_status": "not-proposed"
  },
  "relations": {
    "related": [
      "ir-documentation-content-role-validation"
    ],
    "supersedes": []
  }
}
---

# Documentation skill adaptive-review follow-up

## Context And Applicability

This record is owned by the shared documentation-skill maintenance concern; both named skills remain improvement subjects.

Evaluate whether the September 2026 adaptive-review changes to docs-structuring and docs-shaping improve efficiency while preserving useful documentation review and cleanup. Both skills and paired end-of-task use are in scope; the frozen baseline below is a comparison basis, not a representative distribution or proven saving.

## Evidence And Evaluation

The September baseline below was reported as executed. A first observational
follow-up ran on 2026-10-31 and was discussed and retained on 2026-11-01; its
bounded results follow the frozen baseline. Original private session histories
and the originating audit conversation retain the observations, outputs and
analysis provenance. Public readers cannot verify the raw histories from this
record alone. Disposable reconstruction and analysis files were removed after
verification; this record does not depend on them.

The original baseline did not capture loaded source revisions or content
fingerprints. The later audit matched available entry-file bodies to repository
snapshots, but did not recover a complete frozen effective instruction set or
whole-package loaded-byte fingerprint for every run. Current package bytes do
not establish historical loading. Subject revision/fingerprint fields remain
null because this is a multi-revision observational collection, not one fixed
executed package snapshot.

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

### First practical follow-up: observed through 2026-10-31

The user clarified the practical question: does ordinary use select necessary
edits, leave valid content unchanged and expand discovery when needed, and what
does one documentation cleanup cost on average? Model capability and task
context naturally change over time. A perfectly isolated A/B is not required
for that field assessment; the limits below still prevent attributing every
observed difference to the skill revision. Review breadth and edit breadth are
separate: a necessary whole-target review is not an unnecessary whole-target
rewrite.

The audit inspected 2,419 locally available log files from two Codex stores and
one Claude store, spanning 2026-06-16 through 2026-10-31 on one observed machine
and 19 identifiable working directories. These are discovery counts, not
independent skill executions. Source loading was distinguished from catalog
mentions, inherited context and reading a package as audit material. Replayed
parent/child evidence and cumulative usage counters were not counted twice.

The available corpus yielded 384 identifiable dedicated reviewer sessions; 231
mixed primary sessions were excluded from whole-session cost attribution, and
53 source-loading candidates were excluded because actual use/usage was not
established or they belonged to controlled refinement/closeout checks. Those
filters are evidence boundaries, not a population-wide invocation census.
Claude had no post-change execution sample; unavailable/deleted histories and
other machines remain outside coverage.

The quantitative comparison further selected entry-file-identified ordinary
reviewer executions: 59 from September 1–18 and 164 from September 19–October 30.
The source references were:

- pre-change entry body: repository snapshot
  `29b3caf8ae6e9e562bfd6a6920f3ea7b46ef1d87`;
- adaptive-review entry bodies: snapshots
  `13850084da7fcfda9ddf39a67a4619bd0f14f093` and
  `043653134d651f4fddaa4b0b18d1c7af0d3fcf88`;
- the October 31 content-role revision
  `ec12bf137e21d8f35734ba9bb78777958c67ff00` was outside this before/after window.
  Its separate [content-role validation](documentation-content-role-validation.md)
  is not evidence of September efficiency or stable later real-use behavior.

An entry-body match identifies that inspected input, not every reference,
inherited instruction, installed cache or effective setting. The baseline
cohort used GPT-5.6 Sol and GPT-6 Astra; the later cohort also used GPT-6 Sol,
GPT-6.1 Sol, GPT-6 Luna and GPT-6.1 Terra. Models, settings, document-set sizes,
requests and surrounding instructions were not held constant.

#### Cost unit and observed per-run comparison

The table measures each reviewer's **first review turn**, separating subsequent
edits, re-reviews and additional assignments in the same thread. It excludes
parent-agent preparation, integration and editing, so it is not the final
end-to-end cleanup bill. Some long-lived reviewer threads later accumulated
substantial new work; treating that entire thread as one initial review would
change the denominator.

A separate-session pair is the **sum of two reviewers' costs for the same
parent task event**, averaged across pairs. A joint invocation is one reviewer
applying both skill perspectives, averaged across such invocations. The joint
value is the entire invocation's cost, not its cost divided by two skills.
Separate sessions do not by themselves prove answer isolation or independence.
Pairs are a subset of the single-skill rows, not additional executions to add
to their totals. Joint invocations retain one usage total rather than charging
it to both skill rows.

In the following table, each triplet is **mean / median / P90**. P90 uses linear
interpolation at `(n - 1) * 0.9` in sorted observations.

| Review unit | Before / after count | Input MTok, before | Input MTok, after | API-equivalent USD, before | API-equivalent USD, after |
|---|---:|---|---|---|---|
| docs-structuring alone | 21 / 50 | 2.25 / 1.26 / 4.26 | 2.21 / 1.60 / 4.56 | 2.19 / 1.83 / 3.14 | 1.86 / 0.99 / 4.29 |
| docs-shaping alone | 23 / 64 | 1.75 / 0.80 / 4.42 | 1.92 / 1.02 / 4.39 | 1.69 / 1.64 / 2.79 | 1.79 / 0.89 / 3.93 |
| Both perspectives in one invocation | 15 / 50 | 3.27 / 2.74 / 6.35 | 2.10 / 1.50 / 4.67 | 3.05 / 3.06 / 5.39 | 1.41 / 0.81 / 2.68 |
| Sum of two separate-session reviewers | 19 / 45 pairs | 3.38 / 1.63 / 7.35 | 4.17 / 3.06 / 8.19 | 3.64 / 3.42 / 6.07 | 3.69 / 1.80 / 8.67 |

The observed separate-pair mean was about $3.7 per initial paired review, close
to its earlier $3.6 mean. Its median fell about 47%, while mean input grew about
23% and cost P90 rose about 43%. The joint-invocation sample averaged about
$1.4 for the entire initial invocation. These are descriptive costs for the
observed task groups, not a recommendation to replace an additional reviewer
or a guarantee that running two skills together causes that saving.

The original three selected pairs' input/cache/output counts and rounded
$2.87 / $4.12 / $8.17 estimates were reproduced from original logs. Their
approximately $5.05 mean and $4.12 median remain a separate, selected,
follow-up-inclusive historical reference, not the expanded first-turn mean.

#### Usage totals and cache/output distribution

The first three rows per period below partition the 59 and 164 compared
executions. The pair rows are overlapping subsets and must not be added again.
Aggregate currency totals use unrounded response values; displayed rows can
differ from their sum by rounding.
Input includes cached input; uncached input is `input - cached`. Output already
includes reasoning tokens. All token quantities in this table are millions.

| Period and review unit | Input | Cached input | Uncached input | Output | API-equivalent USD total |
|---|---:|---:|---:|---:|---:|
| Before: structuring alone | 47.224785 | 44.248320 | 2.976465 | 0.274982 | 45.94 |
| Before: shaping alone | 40.138707 | 37.398528 | 2.740179 | 0.256694 | 38.79 |
| Before: joint invocation | 49.051212 | 46.273664 | 2.777548 | 0.259909 | 45.78 |
| After: structuring alone | 110.556008 | 103.651712 | 6.904296 | 0.534850 | 93.07 |
| After: shaping alone | 122.587642 | 115.656448 | 6.931194 | 0.601606 | 114.60 |
| After: joint invocation | 104.993637 | 98.866688 | 6.126949 | 0.685303 | 70.47 |
| Before: separate-session pairs, subset | 64.212119 | 59.674112 | 4.538007 | 0.430198 | 69.20 |
| After: separate-session pairs, subset | 187.633761 | 176.183936 | 11.449825 | 0.897751 | 166.12 |

Across the non-overlapping first three rows for each period, observed first-turn
input total increased from 136.414704 to 338.137287 million tokens, and estimated
cost total increased from about $130.51 to $278.15 as the compared counts grew
from 59 to 164 over different-length periods. This larger period total is
compatible with a lower mean in a particular review group. It is not the sum
of two skills being relabeled as a per-skill average.

For the separate-session pairs, cache and output distributions were:

| Quantity | Before mean / median / P90 | After mean / median / P90 |
|---|---|---|
| Cached input MTok | 3.14 / 1.45 / 6.92 | 3.92 / 2.80 / 7.75 |
| Uncached input KTok | 238.84 / 181.28 / 374.74 | 254.44 / 254.22 / 403.27 |
| Output KTok | 22.64 / 16.00 / 43.37 | 19.95 / 18.51 / 31.73 |

Shared preparation and source reuse can plausibly reduce duplicated reading,
tool calls and reporting when both perspectives execute in one context. The
later joint group used about 2.10 million mean input tokens versus 4.17 million
for the sum of the separate reviewers. That is an observed processing-volume
difference, not a measured causal decomposition: model mix and task scope also
differed. The earlier conversational shorthand “joint use saved cost” is
narrowed to “the observed joint-invocation group had lower average usage and
estimated cost.”

#### Valuation and interpretation controls

The historical three-pair estimates retain the September 18 frozen rates above.
The expanded sample uses Standard short-context API rates checked on October
31. Rates are USD per million **uncached input / cached input / output**:

| Model | Rates |
|---|---|
| GPT-5.6 Sol | 4 / 0.40 / 20 |
| GPT-6 Astra | 10 / 1 / 50 |
| GPT-6 Sol | 2 / 0.20 / 10 |
| GPT-6.1 Sol | 2 / 0.10 / 10 |
| GPT-6 Luna | 0.10 / 0.01 / 0.50 |
| GPT-6.1 Terra | 1 / 0.05 / 5 |

The first two rates were unchanged from the frozen reference. Sources were the
[official pricing page](https://developers.openai.com/api/docs/pricing) and
[GPT-6 Sol model page](https://developers.openai.com/api/docs/models/gpt-6-sol).
The same uncached/cache/output formula above was applied response by response.
Selected records contained no cache-write input. Actual billed/subscription
cost, Fast/other service tiers, long-context adjustments and tool charges are
not established or included; parent work and later phases are also excluded.

A same-project/GPT-6 Astra subset had eight earlier and six later pairs. Its
initial-review mean estimate rose from $3.55 to $8.48, with different document
sizes and scope. That counterevidence prevents treating the aggregate median
fall as a uniform saving, but it does not prove a skill regression.

#### Bounded quality observations

Twelve historical reviewer execution records were selected across focused,
whole-set, non-Git, paired, follow-up and unchanged cases. Three were pre-change
and nine post-change; related/paired reviews are not twelve independent
experiments. Principal findings, scope reports and relevant actions were
compared with returned source passages and tool traces. This was not a new
forward-test or an exhaustive semantic re-audit of every source document, and
other executions received no such semantic inspection.

- Focused follow-ups reread a corrected temporal qualification and nearby
  context, then stopped without restarting an unrelated whole-set audit.
- A non-Git case followed the owning common procedure and found that a
  work-specific plan required destructive cleanup that the common owner did
  not require. A whole-set case detected unique operator steps and acceptance
  gates at risk of being lost when a document was removed.
- Valid no-change outcomes left the target unchanged. Reports distinguished
  whole-tree mechanical inventory from the smaller set of bodies actually
  reviewed, rather than declaring the unreviewed history current.
- Useful temporal, ownership and preservation findings also occurred before
  the September change. The observations support practical scope selection
  and necessary cleanup in these cases, not a new failure-to-success transition
  or a general post-change quality guarantee.

**Audit Result: PASS WITH SUGGESTIONS. Evidence Coverage: partial.** The token
arithmetic, frozen-reference reproduction and bounded source comparisons
completed. The practical question has a first field assessment; the highest
behavioral evidence here is observed historical task execution. Stable savings,
population-wide quality, full-workflow cleanup cost and per-edit causal effects
remain unestablished. No skill source, installed runtime or policy was changed
by this audit.

## Work And Acceptance

### Eligibility And Authority

The first observational review is complete; keep the work open for another
check after additional ordinary use, retaining November–December 2026 as the
revisit window. A concrete recurrence of unnecessary rewriting, missed drift
or excessive repeated review can justify an earlier selected check. The next
audit still covers all locally available stores/projects within its authority,
not only the current repo. Resolve its scope and budget when selected. This is
a revisit trigger, not an automatically scheduled job or advance authority for
new model executions.

Readiness and task-specific budget must be established at selection. No active
task/run/performer is assigned by this record.

### Required Checks

- Around November–December 2026, after a few months of real use, evaluate the September 2026 adaptive-review changes for both usage and documentation quality:
  - Cover all locally available session stores and projects, not only the current repository; distinguish actual skill executions from catalog mentions, inherited history, and duplicated parent/child records. State date range, machine coverage, sample counts, and missing usage data; keep private transcripts and machine-specific paths outside this public repository.
  - Report invocation frequency, total usage, and per-run mean, median, and upper-tail usage for each skill and paired end-of-task reviews. Separate input, cached input, uncached input, and output without double-counting cumulative counters. Compare similar task scopes, document-set sizes, models, and loaded skill revisions before and after the change; distinguish token usage, any price-based estimate, and actual billed cost.
  - Inspect representative focused, whole-set, non-Git, paired-review, follow-up, and unchanged outcomes against their source documents. Check factual/status correctness, ownership, composition, preservation, useful findings, and whether broader exploration occurred naturally when needed without requiring a known local defect or an explicit full-audit prompt. State which outcomes were inspected rather than implying every run received semantic review.
  - Accept efficiency gains only when required coverage and useful document cleanup remain intact. Check for missed drift, unjustifiably narrow reviews, redundant rereading, unnecessary rewrites, and unsupported claims that unreviewed material is current. Refine only defects supported by the observed runs; do not reduce capability merely to lower token counts.

### Next Bounded Check

- Keep the practical questions explicit: appropriate necessary changes,
  justified no-change outcomes, useful broader discovery and average dollars
  per completed cleanup. An always-whole-tree rewrite is not the desired
  success condition; neither is artificially narrow reading.
- Continue reporting first review, authorized edits, follow-up/review and
  parent preparation/integration separately. When their complete evidence is
  available, also report their summed end-to-end cleanup cost. Do not relabel
  an initial-review estimate as the whole cleanup cost or divide a two-skill
  invocation's cost by two to compare it with a summed reviewer pair.
- Retain counts, mean, median, upper tail and raw token/cache splits for each
  execution style, together with model, task scope/document-set size and the
  actually loaded revision where observable. Compare similar ordinary work
  where available; disclose expected model/context drift without requiring a
  perfect A/B before making a bounded practical assessment.
- Reinspect representative source-backed necessary-edit, no-change,
  whole-set-discovery and follow-up cases, including contrary outcomes. Keep
  the separate October content-role question distinct and do not count its
  synthetic trials as efficiency evidence.

### Completion

Conclude the selected practical review with the usage and semantic-quality
checks above, explicit coverage/gaps and the observed comparison conditions.
A practical field result does not require a perfectly controlled A/B; an
attributed revision effect or stable improvement still needs suitably comparable
support. Accept an efficiency gain only while required coverage and useful
cleanup survive. Keep unreviewed outcomes and unavailable total-workflow cost
unresolved; refine only defects supported by observed runs.

## Outcome And Reuse

The first practical follow-up is complete within its observed scope. Targeted
maintenance, valid no-change behavior and necessary expansion were observed;
separate-pair first-review mean cost was approximately unchanged, while the
joint-invocation group had lower observed mean cost and input. Original period
totals, per-invocation averages and skill-count denominators remain distinct.
The provisional reuse is those bounded observations, not a universal preference
for joint execution or proof of causal savings.

Work remains open and waiting for additional ordinary-use evidence and a
selected follow-up. Retain the September frozen-rate reference separately from
the October valuation. No package change is justified by these observations
alone. Normative adoption, Git publication, consumer refresh and actual runtime
activation are separate events; this record update establishes none of them.

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

- Revision 5, 2026-11-01: retained the October 31 practical usage/quality
  follow-up and the user's clarified per-cleanup question, source/version and
  population limits, initial-versus-later phase boundary, aggregate-versus-mean
  and joint-versus-summed-pair distinctions, and the noncausal reading of lower
  joint-group cost. Preserved the original three-pair frozen reference and all
  pending quality/control obligations. Kept a further ordinary-use check open;
  no repeated execution or automatic schedule was created. Semantic public-
  fitness review covered these generalized observations, public asset identities
  and aggregate figures; private projects, paths, transcripts, associations and
  raw runtime identities are excluded. No publication or consumer activation is
  claimed by the local source edit.
- Revision 6, 2026-11-01: corrected execution metadata from `mixed` to `run`
  for the disclosed historical executions and completed observational audit.
  No unexecuted evidence component is disclosed; future validation belongs to
  the open/waiting work state. Partial coverage, candidate knowledge and all
  remaining checks are unchanged. This metadata correction adds no new run or
  causal support.
