---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-pr-review-semantic-corpus",
  "revision": 7,
  "audience": "public",
  "subjects": [{"kind": "skill", "key": "skills/gh-review-pr", "source_revision": null, "content_sha256": "eca6c95927d8395b1266740e3ecef61e4605ba95eec6f7ba6b35173114208595"}],
  "work": {"basis": "planned-work", "state": "open", "readiness": "not-assessed"},
  "knowledge": {"state": "candidate"},
  "evidence": {"kinds": ["static-observation", "illustrative-synthetic"], "maturity": "fresh-forward-test", "execution": "mixed", "coverage": "partial"},
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": ["ir-pr-review-live-validation", "ir-codex-review-challenger-validation"], "supersedes": []}
}
---

# PR review semantic corpus and comparisons

## Context And Applicability

Create a reusable privacy-safe semantic corpus for gh-review-pr and compare review strategies without leaking expected findings. The corpus must represent substantive defect and legitimate-zero/duplicate cases and preserve review-mode semantics while measuring recall and noise.

The comparison inputs were the [Anthropic review workflow](https://claude.dev/blog/solving-code-review-at-anthropic/), [Claude Code Review documentation](https://code.claude.com/docs/en/code-review), and [the associated discussion](https://news.ycombinator.com/item?id=50122951). Fresh-context review, code-backed verification and trusted guidance motivated the local changes; cost, false fixes and transferability remain evaluation questions. Those sources are design inputs, not measurements of this package, and reviewer agreement is not proof that a finding is true.

The selected scope is the portable skill contract and an optional Codex implementation of the omission-review role. Shared harness repair loops, runtime spending limits and budget-exhaustion escalation routing are deferred to a separate broader harness review. The skill's finite snapshot-attempt allowance is an operational instruction, not a time/token/cost cap, automatic repair loop or implemented escalation service. The initial allowance of three is not an empirically optimal review count.

## Evidence And Evaluation

Earlier historical execution was not established by this record. The following
2026-10-31 observations add bounded evidence without completing the full corpus
or matched strategy comparisons. Original tool results and producer outputs are
in the originating conversation. Disposable frozen copies, local git fixtures,
plans and API-call logs were removed after assessment; this record retains the
reviewed synthetic account, not a replayable agent trace or permanent fixture
corpus. A reconstructed fixture needs a new execution before its outcomes count.

### Source identity and completed corrections

The committed baseline was `a16698813773ea74c310bb6bb5f1493e1b6addeb`.
The tested candidate was uncommitted, so `source_revision` is null rather than
attributing revised bytes to that baseline. The subject fingerprint is SHA-256
of sorted package-relative `<path>\0<file SHA-256>\n` entries for all eight
package files. It identifies the candidate actually loaded in the two trials,
including `SKILL.md` SHA-256
`36a07f89d907a70505a369c1b50f66659005f3cee719c8e7eec9c693c4cebfee`.
No installed or cached skill revision was established.

- [Trusted guidance](../../../skills/gh-review-pr/references/review-criteria.md#trusted-review-guidance) now separates frozen code, immutable repository criteria and actual injected instructions. Optional guidance is not a prerequisite; a head-authored suppression cannot govern its own review, and recording a SHA does not undo injected context.
- [Full-task delegation and omission support](../../../skills/gh-review-pr/references/review-criteria.md#full-review-handoff) have distinct authority and outputs. The review works without a specific adapter, worker name or model. Full-task handoff carries the original current request, evidence, mode/profile/event, scope, prior review/duplicate state, allowance, validation/write boundaries, reserved decisions and delegation limits. The narrower challenger does not acquire publication or acceptance authority.
- [Continuity](../../../skills/gh-review-pr/references/review-criteria.md#review-continuity-and-convergence) keeps a one-shot review at one completed result, counts abandoned attempts, preserves current base/head causality alongside the previous-head repair delta, invalidates affected reused evidence, and distinguishes finding validity, disposition and resolution. No source-fixing or extra publication authority was added; zero new findings does not resolve old concerns.
- An independent portability audit found an ambiguous task owner in the earlier wording. The correction defines a direct or delegated task-owning reviewer while preserving decisions retained by higher instructions or the caller. Ordinary `refresh` returns a draft unless the current request explicitly authorizes publication. Lack of a second execution preserves the actual fresh/self-review classification; it does not automatically make a fresh reviewer an author.

### Observed resources and forward tasks

| Observation | Actual result | Scope and counterevidence |
|---|---|---|
| Publication interleaving | Before correction, A passed preflight, B completed the same user's PR/base/head/finding plan, then A also submitted: two reviews and four fake POSTs. After a PR-target OS lock, one caller published, the competitor stopped safely, and a sequential rerun was a no-op: one review and two fake POSTs. | The defect predated the new prose; the earlier helper matched the committed baseline. The [regression tests](../../../skills/gh-review-pr/scripts/test_gh_review_transaction.py) retain interleaving, separate-process exclusion/release, case aliases, different PRs, unavailable locks, failure release and new-snapshot controls. The [protocol](../../../skills/gh-review-pr/references/github-publishing.md#publication-concurrency) limits coordination to cooperating calls sharing a local OS user/home and lock-capable filesystem; outside writers require coordination or a draft. No live-server result is implied. |
| Resource checks and independent audits | The revised transaction suite passed 63 tests; adapter-related offline tests passed 7. Package/reference checks, TOML checks and 110 combined local links/anchors passed. Initial adapter audit was PASS WITH SUGGESTIONS; the skill audit found the publication race. After corrections, both separate refine audits returned PASS with partial coverage. | Configuration and audit-runner fixtures do not demonstrate the configured worker's loading, actual permissions, semantic competence or cost. Passing deterministic checks do not decide finding truth. |
| Fresh delegated review, `balanced` | A raw pagination change from `stop = start + size` to `stop = start + size - 1` produced one blocking/medium correctness draft, anchored to the added line and traced through the terminal `rows` consumer. Base tests passed 3/3; head failed 2/3. Of 270 input combinations, base mismatches were 0 and head mismatches 68. | A normal-risk local change; no custom adapter, named worker or child spawning was used. The producer received the frozen skill and raw task artifacts, without authoring discussion or expected findings. |
| Fresh delegated re-review, `focused` | An equivalent inlining of the slice end produced zero material findings and zero notes, with six pass-specific counterevidence entries. The reviewer compared both deltas, retained `fresh-review`, recorded the supplied prior round plus this round as 2/3, and returned `refresh` to draft. Three tests and 2,100 input combinations across base, prior head and current head passed. | An ordinary re-review request supplied no publication authority. The two producers handled different cases; they are not repetitions of one task or a matched self/fresh or model-strategy comparison. |

Repository closeout also passed 63 transaction tests and 23 repository utility
tests, including the same seven adapter-related tests; all 11 skill packages;
the generated-instruction check; 16 record schema/identity/catalog checks;
four TOMLs, three quoted metadata fields and 189 local links/anchors across
12 documents. These are repository/resource checks, not additional semantic
trials. The earlier 110-link count used the narrower pre-consolidation scope.

Each forward task logged 13 fixture GETs and no write attempt, and left its
checkout unchanged. These were generic fresh review executions, not invocations
of `review_challenger`. The highest semantic evidence is two fresh forward-tests of the revised
candidate; the race has a comparable resource-level reproduction.
There is no comparable v1 agent-review run, broad recall/noise estimate or cost
measurement. Result is PASS for the checked corrections and cases; Evidence
Coverage remains partial.

High-risk independence, snapshot churn/exhaustion, guidance conflicts and the
full profile/strategy matrix remain unrun. The optional named worker's remaining
checks belong to [Codex review-challenger validation](../../agents/codex/review-challenger-validation.md);
live publication, receipts/accessibility and platform/provider limits belong to
[controlled live validation](pr-review-live-validation.md). Do not count the two
ordinary delegated tasks as evidence that either unrun capability works.

## Work And Acceptance

### Eligibility And Authority

Use the adjudicated case families below after public-safe reconstruction and with an authorized bounded comparison. Give producers sufficient task evidence while withholding expected findings; apply comparable fixtures across the paired strategies and modes.

Readiness and task-specific budget must be established at selection. No active
task/run/performer is assigned by this record.

### Required Checks

- Build one privacy-safe reusable semantic fixture corpus from the adjudicated behavior-removal, security, cross-boundary consumer-frontier, mixed managed-and-vendored dependency-selection, legitimate-zero, and hard-duplicate cases.
  - Run blinded matched self-review versus fresh-review and latency-first versus quality-first evaluations without revealing expected findings.
  - Score material-finding recall, duplicate and false-positive control, and whether the structured receipt distinguishes a supported zero-material-finding result from a hollow summary.
  - On comparable fixtures, verify that `focused` emits no review notes, `balanced` keeps low-severity observations out of inline threads, and explicitly selected `assertive` permits only anchored high-confidence non-blocking low suggestions, without lowering semantic depth or increasing speculative noise.
- Add trusted-guidance controls: absent optional guidance still permits review; merged root/ancestor rules and included files use the selected immutable revision; head-authored suppression does not govern its own review; explicit higher-priority authority is preserved; injected-instruction conflicts are disclosed rather than hidden behind a recorded SHA.
- Exercise the portable independent-reviewer brief through an authorized competent fresh execution without requiring a particular adapter, worker name or model. A missing adapter with another suitable reviewer is a success control. When independent execution is unavailable, retain the actual fresh-review or self-review classification and the existing high-risk draft restriction; a new runtime configuration alone is not an independent semantic result.
- Distinguish an end-to-end delegated reviewer from an omission-only challenger. Carry the original current request, mode/profile/event, raw evidence, validation and write authority, reserved decisions, and further-delegation limits. Verify normal-risk review completion without an adapter or child-spawning capability, and compare ordinary re-review drafts with explicitly authorized refresh publication; delegation alone must not create write authority.
- Compare one-shot and authorized multi-snapshot review: no unsolicited fix/review loop; initial and abandoned snapshot attempts included in the allowance; repeated IDs or changed heads do not reset it; the previous-head repair delta supplements current base/head causality; changed consumers, dependencies or guidance invalidate affected evidence; same-cause occurrences are individually adjudicated. Verify final-allowed-round success, exhausted-series drafts, missing historical evidence, and zero new threads while old blocking concerns remain unresolved.
- Include reviewed public-safe reconstructions of incidents and fixes when source evidence is available, plus legitimate clean cases where a mistaken finding would induce a harmful change. Keep validity, disposition and resolution distinct; thread closure alone is not a truth label. Score harmful false fixes, repeated concerns, rounds and observed human/tool cost alongside recall and noise, leaving unavailable measurements unknown.

### Completion

Completion requires the corpus and actual blinded matched evaluations for every listed case/strategy/mode obligation, with recall/noise/receipt evidence. A fixture inventory alone cannot establish behavior; keep missing comparisons open and preserve any adverse result.

## Outcome And Reuse

The bounded source corrections and two normal-risk delegated draft tasks are
complete within the observed conditions. Corpus construction and matched
semantic comparisons remain open. Reuse only reviewed fixtures and supported,
scope-limited outcomes; no review strategy, model or configured runtime binding
is declared superior or generally reliable here. Source changes, repository
publication, consumer synchronization and actual runtime activation remain
separate events.

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
- Revision 5, 2026-10-31: expanded the planned skill controls for trusted
  guidance, runtime-independent reviewer roles, review continuity and harmful
  false fixes. Preserved all original case/strategy/profile obligations and
  the open, unassessed state. This source-contract update supplies no semantic
  comparison, runtime activation or closure; the generalized additions were
  reviewed for public fitness without copying private runtime evidence.
- Revision 6, 2026-10-31: added full-task delegation and refresh-authority
  controls, keeping task ownership distinct from an omission-only challenge.
  Preserved the actual fresh/self-review classification when no second
  independent execution is available. These additions leave the full corpus
  and matched strategy/profile comparisons open; they do not claim runtime
  activation, semantic reliability, or completion.
- Revision 7, 2026-10-31: retained the completed contract corrections, local
  publication-race comparison, two synthetic delegated forward tasks and
  independent audit results with their actual source fingerprint and limits.
  Preserved every full-corpus acceptance obligation and the open work state;
  runtime and live checks remain with their distinct owners. The generalized
  additions were reviewed for public fitness; no private paths, identifiers or
  original runtime data were copied into the public record.
