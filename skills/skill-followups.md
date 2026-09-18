# Skill Follow-Ups

## Purpose
- Keep one shared place for later additions, refinements, and cross-skill follow-up work.
- Capture durable backlog items without scattering temporary notes across skill packages.
- Track future contract improvements separately from the current implementation pass.
- Keep only unresolved work; remove an item after it is implemented or deliberately closed and rely on Git history for resolution history.

## Current Follow-Ups

### [Repository-wide skill quality](SKILL-QUALITY.md)
- Define a skill-specific adoption, synchronization, and removal contract before automating installation. Cover canonical symlinks versus copied targets, Codex and Claude discovery paths, target-specific metadata, pre-existing paths, cache refresh, and safe unlink behavior.
- Consider a shared benchmark suite only after at least two skill families have reusable, privacy-safe task corpora and comparable pass/fail contracts; keep forward-tests skill-local until then.

### [`refine-skill`](refine-skill/SKILL.md)
- Validate static-only audits and explicit, implicit, and out-of-scope selection in the discovery environment.
- Extend matched A/B runs to document/template corrections and repeat cases to check stability; capture actual tool traces alongside output checks.

### [`docs-structuring`](docs-structuring/SKILL.md) and [`docs-shaping`](docs-shaping/SKILL.md)
- Around November–December 2026, after a few months of real use, evaluate the September 2026 adaptive-review changes for both usage and documentation quality:
  - Cover all locally available session stores and projects, not only the current repository; distinguish actual skill executions from catalog mentions, inherited history, and duplicated parent/child records. State date range, machine coverage, sample counts, and missing usage data; keep private transcripts and machine-specific paths outside this public repository.
  - Report invocation frequency, total usage, and per-run mean, median, and upper-tail usage for each skill and paired end-of-task reviews. Separate input, cached input, uncached input, and output without double-counting cumulative counters. Compare similar task scopes, document-set sizes, models, and loaded skill revisions before and after the change; distinguish token usage, any price-based estimate, and actual billed cost.
  - Inspect representative focused, whole-set, non-Git, paired-review, follow-up, and unchanged outcomes against their source documents. Check factual/status correctness, ownership, composition, preservation, useful findings, and whether broader exploration occurred naturally when needed without requiring a known local defect or an explicit full-audit prompt. State which outcomes were inspected rather than implying every run received semantic review.
  - Accept efficiency gains only when required coverage and useful document cleanup remain intact. Check for missed drift, unjustifiably narrow reviews, redundant rereading, unnecessary rewrites, and unsupported claims that unreviewed material is current. Refine only defects supported by the observed runs; do not reduce capability merely to lower token counts.

#### Comparison baseline recorded on 2026-09-18

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

### [`maintain-context-freshness`](maintain-context-freshness/SKILL.md)
- Repeat `maintain` in an independent post-creation run:
  - verify that only approved content-state changes reach the smallest owning documents; finding IDs, ledger rows, and review, approval, or action status must remain session-only unless the user explicitly requests a named durable audit artifact
  - confirm that historical markers, `as-of` dates, successor links, and any condensation preserve unique content, provenance, and discoverability
- After the next real user-requested archive or delete operation:
  - verify that no operation occurs without the exact source and action, plus the exact archive destination when applicable
  - confirm that the session report distinguishes proposed, not applied, approved, and applied states plainly
- Confirm in a fresh Claude session that the canonical symlinked package is discovered and can complete one standalone audit or maintain run.

### [`gh-review-pr`](gh-review-pr/SKILL.md)
- Build one privacy-safe reusable semantic fixture corpus from the adjudicated behavior-removal, security, cross-boundary consumer-frontier, mixed managed-and-vendored dependency-selection, legitimate-zero, and hard-duplicate cases.
  - Run blinded matched self-review versus fresh-review and latency-first versus quality-first evaluations without revealing expected findings.
  - Score material-finding recall, duplicate and false-positive control, and whether the structured receipt distinguishes a supported zero-material-finding result from a hollow summary.
  - On comparable fixtures, verify that `focused` emits no review notes, `balanced` keeps low-severity observations out of inline threads, and explicitly selected `assertive` permits only anchored high-confidence non-blocking low suggestions, without lowering semantic depth or increasing speculative noise.
- Only when the user explicitly authorizes each relevant write in that turn, complete controlled schema-v2 live checks on github.com and the current corporate GHES.
  - Publish one safe test review on each host and inspect the two-column receipt, conditional warning with one bullet per gap, blank-line hierarchy, linearized plain-text reading order, restrained `✅` semantics, and always-expanded evidence visually and with assistive-technology-oriented inspection.
  - Verify that an explicit publish request creates exactly one review and that an exact same-snapshot rerun returns `noop-existing-snapshot`.
  - Verify that a newly confirmed finding or summary-count change on an already reviewed same snapshot returns a corrected draft without writing or bypassing the snapshot guard.
  - Forward-test `reply` after the PR head advances; the result must distinguish the original review head from the current head and stop on a preparation-time race.

## Notes
- Keep this file concise and durable.
- Record follow-ups that are likely to matter across sessions.
- Do not turn this file into a run log or a temporary scratchpad.
