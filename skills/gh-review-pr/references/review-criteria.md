# Review Criteria

Use this reference to decide what belongs in a GitHub review and how reviewer-supplied content should communicate it. The [GitHub publishing protocol](github-publishing.md) owns the exact plan schema, renderer behavior, transaction, and recovery; those deterministic checks cannot decide whether a finding is true or useful.

## Contents

- [Coverage model](#coverage-model)
- [Review depth and independence](#review-depth-and-independence)
- [Change map and review passes](#change-map-and-review-passes)
- [Counterfactual adjudication](#counterfactual-adjudication)
- [Severity and disposition](#severity-and-disposition)
- [Confidence](#confidence)
- [Review categories](#review-categories)
- [Candidate ledger](#candidate-ledger)
- [Publication gates](#publication-gates)
- [Zero-finding gate](#zero-finding-gate)
- [Existing discussions and duplicates](#existing-discussions-and-duplicates)
- [Human feedback audits](#human-feedback-audits)
- [Artifact writing](#artifact-writing)
  - [Summary content](#summary-content)
  - [Zero-material-finding session receipt](#zero-material-finding-session-receipt)
  - [Inline thread content](#inline-thread-content)
- [Sensitive information](#sensitive-information)

## Coverage model

Start from the frozen base-to-head diff. Classify every changed file as one of:

- `reviewed`: all human-authored changed lines and relevant surrounding behavior inspected
- `generated`: reproducibly generated output reviewed only at its source or generator
- `vendored`: third-party material whose provenance or checksum is the meaningful review surface
- `binary`: no textual diff available
- `truncated`: the provider did not return enough diff data
- `excluded`: explicitly outside the requested review scope

Follow changed behavior across file boundaries when necessary to establish reachability. A line-by-line pass without checking callers, schemas, configuration, tests, or failure handling is not complete coverage.

Report material non-reviewed classes in the summary. Never translate incomplete coverage into a safety claim.

## Review depth and independence

Classify the semantic pass before reviewing:

- `fresh-review`: the reviewer receives the frozen PR artifacts without the implementation conversation or intended findings
- `self-review`: the active session authored, edited, or extensively designed the change, or already argued for a particular implementation

In a self-review, prior explanations are intent evidence only. Reconstruct behavior from the base, head, tests, and runtime contracts, and deliberately look for evidence that contradicts the earlier design narrative.

Match review depth to risk. A routine, local change may use a normal pass. Security-sensitive, cross-service, migration, behavior-removal, concurrency, data-integrity, or broad control-flow changes require a quality-first pass capable of cross-file reasoning and relevant validation. Model names are not the contract, but a latency-first or low-reasoning pass alone is not adequate evidence for those changes.

For a high-risk change, one semantic pass is candidate evidence rather than coverage proof, even when it finds an issue. When an authorized, competent fresh reviewer is available, give it only the frozen artifacts and ask specifically for omissions and counterexamples without revealing expected findings. Reconcile the union of independently discovered candidates through the same gates; never publish a challenge candidate automatically. If the independent challenge is unavailable, keep the result in `draft` and record the independence gap.

Starting a new session helps only when it removes authoring assumptions and loads the intended skill revision. It does not replace repository context, runtime evidence, or the review passes below.

## Change map and review passes

Before generating findings, build a compact internal map:

```text
changed behavior | prior invariant | new path | affected callers/consumers | consumer frontier | failure boundary | relevant tests
```

Run every applicable pass and mark a pass not applicable only with a reason:

1. **Diff-boundary pass**: inspect added and deleted delimiters, comments, templates, condition order, early returns, exception scopes, and adjacent unchanged behavior that a changed block may accidentally capture.
2. **Behavioral-delta pass**: compare base and head for normal, empty, null, malformed, retry, partial-failure, and recovery inputs that matter to the changed contract.
3. **Integration pass**: follow callers and consumers across schemas, configuration, authorization, persistence, deployment, lifecycle, observability, rollback, user interaction, accessibility, and localization boundaries as applicable. Do not stop at a handler or endpoint when it returns another view, payload, job, or persisted value.
4. **Test pass**: verify that tests exercise the production path, would fail for the suspected regression, preserve intentional compatibility, and do not merely restate the implementation. Treat tests and diagnostic utilities as executable risk surfaces when they authenticate to real systems, handle production-like data, or persist output; an opt-in flag reduces reachability but does not make secret disclosure or destructive behavior harmless.
5. **Design pass**: check responsibility, complexity, duplication, names, comments, and documentation where they can make this change incorrect or materially harder to evolve; do not turn ordinary style preferences into findings.
6. **Adversarial pass**: ask what the diff can silently disable, broaden, leak, misroute, partially initialize, falsely report as success, or leave unrecoverable.

The consumer frontier for a changed value or control edge ends only at the first stable parse, render, authorization, persistence, execution, or recovery boundary. Enumerate every material branch that carries it there. An HTTP endpoint, helper call, queue publish, or view name is an intermediate hop when downstream code reparses, rerenders, stores, or executes the value.

Record each branch as `caller or action | intermediate hops | exact terminal artifact | parse/render/execution context | evidence`. For a controller that returns a view, name and inspect the concrete template and the context where it consumes the value. If a material terminal artifact cannot be resolved, coverage is incomplete; do not use that branch as negative evidence for a zero-finding result.

The purpose is candidate discovery, not comment volume. Do not weaken the publication gates merely because a pass produced no candidate, and do not stop the remaining passes after finding the first issue.

## Counterfactual adjudication

Before assigning severity or disposition, compare the same concrete trigger in base and head:

```text
trigger | base path and impact | head path and impact | changed enabling or worsening edge | net capability | external evidence or gap
```

Name what the PR adds: a new trigger, greater frequency or duration, wider blast radius, weaker recovery, or a newly reachable product flow. “The requirement is not fully solved” is not enough. A remediation PR may leave an old risk in place without causing it; publish only when executable or operational changes introduce or materially worsen a `medium+` impact.

An unchanged missing guard, probe, rollback, or recovery path can still be relevant when the diff adds a new material failure trigger that the safeguard needed to contain. Anchor the new trigger, prove how it increases failure likelihood or persistence, and avoid claiming that the missing safeguard itself was introduced by the PR.

Treat PR prose, code comments, and validation claims as intent or supporting evidence, not as the runtime delta itself. A comment-only changed line cannot anchor a runtime finding. When a new test or diagnostic appears, determine whether it gates build, deploy, or runtime behavior or merely observes and reports it; do not attribute enforcement impact to an opt-in observer.

For external state such as credential rotation, deployed configuration, stored data, or traffic routing, do not infer the current state from a fingerprint, migration claim, or successful test alone. Require frozen-artifact evidence or explicitly supplied runtime evidence that connects the state to the PR. Otherwise keep the uncertainty as a session-only gap.

An unchanged defect becomes publishable through new reachability only when all of these are explicit:

- the same realistic user or system trigger in base and head
- the barrier that prevented the product flow in base
- the exact changed edge that removes that barrier in head
- the unchanged sink and its observable `medium+` impact

Direct endpoint availability is not automatically product-flow reachability. If head leaves the complained-of behavior unchanged while reducing its reachability or impact, classify it as pre-existing or a coverage gap rather than an inline finding.

## Severity and disposition

Assign severity by impact, not by fix size:

- `critical`: credible compromise, irreversible loss, or broad production outage with no practical containment
- `high`: material security, correctness, data, compatibility, or availability failure on a realistic path
- `medium`: bounded but meaningful behavior, reliability, operability, or maintainability failure worth fixing in this PR
- `low`: small but concrete improvement, local cleanup, or unlikely edge case; keep it private in `focused`, use a PR-level note when appropriate in `balanced`, and publish it inline only as a high-confidence non-blocking `suggestion` in explicitly selected `assertive`

Assign one disposition:

- `blocking`: the PR should not merge with the finding unresolved
- `non-blocking`: material and actionable, but safe to follow up without holding the merge
- `question`: intent or contract must be resolved before the impact can be handled correctly

Disposition does not replace severity. A `question` is not a license to publish a low-confidence guess.

Choose disposition from the explicit acceptance scope, the base-to-head net user or operator capability, and recoverability—not severity alone. A valid medium finding against a pre-existing sink that becomes reachable only in a newly enabled optional branch can be non-blocking when the PR is still a net capability gain. Keep it blocking when the changed path regresses a previously working capability, violates an explicit acceptance condition, or creates material security, data-integrity, or availability exposure. Net improvement never makes a real current-delta defect disappear; it affects the merge decision, not truth or severity.

## Confidence

Use `high` only when the relevant execution or data path is directly supported and competing explanations have been eliminated. Typical evidence includes a reproducible failure, a contradicted invariant, an API or schema mismatch, or a traceable path from changed input to impact.

Use `medium` when the concern is likely but depends on an unverified caller, environment, or contract. Use `low` when it is primarily speculative. Gather more evidence when practical; otherwise keep medium- and low-confidence candidates out of inline publication and state only the resulting coverage gap when material.

Repository silence is not proof that a framework, pinned dependency, base image, container, or platform does not provide a lifecycle behavior. When a finding depends on that behavior, inspect the exact pinned implementation through an authorized local artifact or primary documentation. If it remains unavailable, a competing explanation remains and the candidate cannot have `high` confidence.

When dependency behavior is material, enumerate every plausible implementation that can reach the packaged or deployed runtime, including managed declarations, lockfile resolutions, vendored or shaded copies, application-server modules, and image-provided libraries. Prove which implementation wins with evidence such as the built artifact, dependency resolution output, classloader order, or authorized runtime provenance. If selection remains unresolved, rely only on behavior shared by every plausible implementation or record the ambiguity as a coverage gap; do not name one version as effective or assign `high` confidence from that version alone.

## Review categories

Use a short lowercase category such as:

- `correctness`
- `security`
- `data-integrity`
- `reliability`
- `compatibility`
- `performance`
- `concurrency`
- `operability`
- `testing`
- `maintainability`

Testing is a finding category only when the missing or invalid test creates a concrete regression blind spot. Lack of a test by itself is not automatically a defect.

## Candidate ledger

Keep this internal ledger before writing review artifacts:

```text
finding_id | review lens | concern | path | line | side | severity | confidence | disposition | category | artifact lane | base behavior | head behavior | current-snapshot evidence | causal delta | anchor rationale | reachability | impact | counterevidence | safe path | duplicate state
```

Use a stable lowercase hyphenated `finding_id` that names the semantic concern rather than its wording or line number. Reuse it while reconciling the same concern; never mint a new identifier merely to bypass duplicate detection.

Record `causal delta` as the exact behavior this PR introduces or materially worsens. Record `anchor rationale` as why the selected changed line is the causal review location rather than merely nearby reachable code.

Choose `artifact lane` from `issue-thread`, `suggestion-thread`, `review-note`, or `private`. Treat this as routing: the [publication gates](#publication-gates) own thread eligibility, and [artifact writing](#artifact-writing) owns the visible form and note eligibility. Keep any candidate that does not qualify for a visible lane `private`.

For a candidate centered on an unchanged caller, consumer, or sink, also record the same trigger's base barrier, the head enabling edge, endpoint-level versus product-flow reachability, the sink's observable impact, and the resulting net capability.

## Publication gates

Publish a candidate only when every answer is `yes`:

1. Is the issue behavior introduced or materially worsened by the frozen base-to-head diff, or is the low suggestion attached to a concrete pattern introduced by that diff?
2. For an issue, is there a concrete reachable trigger rather than a hypothetical possibility? For a suggestion, is there a bounded maintainability or clarity cost rather than a generic preference?
3. Does direct code, test, runtime, or protocol evidence support the claim?
4. Has relevant counterevidence been inspected and resolved?
5. Is confidence `high`, and is severity at least `medium` for an issue thread—or exactly `low` for an explicitly selected `assertive` non-blocking suggestion?
6. Is an exact added (`RIGHT`) or deleted (`LEFT`) line that introduces or materially worsens the trigger or impact available as the anchor?
7. Is the concern absent from existing review threads and skill markers?
8. Can the thread state the impact or bounded benefit and a minimal safe path without prescribing a broad redesign?

Omit pre-existing defects unless the counterfactual check proves that this PR makes them reachable, more severe, or harder to recover from. Do not report speculative future misuse, purely aesthetic preferences, or issues a deterministic check already communicates better.

A changed line is not a valid anchor merely because execution passes through it. Anchor the causal delta itself. If the provider cannot represent that exact changed line, fix the publication transport or omit the finding; never move the thread to a semantically weaker line to make publication succeed.

When an opening and closing delimiter jointly define the faulty scope, prefer the delimiter whose smallest adjustment repairs the boundary. If both remain causal anchors, use the tighter line and make the paired boundary explicit in the evidence.

## Zero-finding gate

Zero material issue findings can be the correct result. Do not invent a nit, praise comment, or speculative question to avoid it. Review notes and `assertive` low suggestions do not change the material-finding count. Before returning or publishing zero material findings, verify all of the following:

- the change map covers every reviewed human-authored file
- every applicable review pass has concrete negative evidence, not merely “looked fine”
- changed control-flow and block boundaries were compared against the base
- relevant callers, consumers, and tests were inspected rather than inferred from the PR body
- every mapped changed value or control edge was followed to a named terminal artifact and parse/render/execution context rather than stopping at an intermediate endpoint or helper
- the strongest plausible unchanged caller, consumer, or sink was counterfactually tested and its inclusion or exclusion was recorded
- passing checks were treated as counterevidence for only the behavior they actually exercise
- material coverage, independence, and review-depth gaps are stated in the structured receipt
- high-risk coverage received an independent omission challenge, or the result remains a draft with that explicit gap
- the GitHub-visible review evidence contains at least three concrete, sanitized entries spanning the applicable passes rather than a generic claim that the review was thorough

A zero-finding result that depends only on passing tests, agreement with the PR description, or absence of an obvious local bug does not pass this gate. For a high-risk change without an adequate quality-first semantic pass, stop in `draft` instead of publishing a conclusive-looking empty review.

## Existing discussions and duplicates

Read existing reviews, inline threads, issue comments, and unresolved conversations before composing. They are evidence of prior discussion, not proof of current behavior.

Treat a concern as duplicate when an existing thread identifies the same trigger and impact, even if wording, line, or suggested fix differs. Continue the human conversation only when the user explicitly asks; this skill does not edit or reply to human threads. A skill-owned `finding_id` is a hard duplicate signal across reruns.

When a new snapshot resolves an old finding, do not post a congratulatory or closure thread. When it leaves an old finding unresolved, keep the existing thread as the discussion location instead of reposting it under a new identifier.

## Human feedback audits

In a read-only audit of human-authored feedback, classify each concern as one of:

- `valid-current-delta`: the PR introduces or worsens the stated behavior
- `partially-valid`: the risk is real but the stated path, scope, or remedy is incomplete
- `pre-existing`: the behavior exists but this PR does not cause or worsen it
- `contradicted`: code, tests, or runtime evidence disproves the concern
- `contract-decision`: the impact depends on an unresolved product or operational contract

For each concern, cite the exact code or runtime path, state the smallest action, and draft a response that records either the bounded fix plus validation or the evidence-based reason for leaving the code unchanged. Prefer durable code or test clarification over an explanation that exists only in the review thread. Keep the tone collaborative, but do not let generic thanks, praise, or defensive language replace the disposition and evidence. Do not post to a human-authored thread from this skill.

## Artifact writing

The [review plan schema](github-publishing.md#review-plan-schema) owns exact JSON fields, renderer-created Markdown, counts, cardinality, and presentation validation. This section owns the meaning and quality of reviewer-supplied content.

### Summary content

Write one overview paragraph that names the changed behavior and principal risk surfaces. The reviewer owns the overview, scope, focus, evidence, coverage gaps, and optional notes; the transaction owns snapshot and finding-count rendering. Do not enumerate finding titles or fixes in the summary. When there are no material issue findings, keep the conclusion scoped to the evidence: say that no high-confidence `medium+` issue met the issue-thread threshold within reviewed coverage, not that the PR is safe. A suggestion-only review must not say that no finding or feedback met the selected profile threshold because its suggestion did.

Provide compact, sanitized evidence from distinct completed pass areas. Summarize only work actually completed. Do not expose the internal ledger, rejected-candidate speculation, secret material, or private runtime data. The schema owns the allowed evidence labels and cardinality; the [zero-finding gate](#zero-finding-gate) owns the stronger semantic evidence requirement for reviews without material issue findings, including suggestion-only reviews.

Review notes are non-findings. Keep them current-snapshot, high-confidence, concise, useful at PR level, and within the selected profile. Never place a `medium+` defect, material ambiguity, failed inline anchor, duplicate finding, or speculative concern there.

Use presentation as information hierarchy, not decoration. Do not use task-list semantics as review evidence, hide core receipt or evidence content, or add decorative status cues. A validation checkmark must accompany an exact completed validation fact and must not imply zero findings, safety, approval, or merge readiness. Keep inline threads emoji-free.

### Zero-material-finding session receipt

When there are zero material issue findings, including a suggestion-only result, return a detailed session-only evidence receipt with one terse entry for each applicable review pass: the inspected base/head behavior or artifact, the strongest candidate considered, the counterevidence that rejected it, and any remaining gap. Only the compact sanitized evidence belongs in the JSON plan and GitHub review.

```text
review pass | inspected base/head path or artifact | rejected candidate and counterevidence | remaining gap
```

### Inline thread content

Use the exact `issue` or `suggestion` first-line contract defined by the [review plan schema](github-publishing.md#review-plan-schema). Write one concern per thread.

Follow with concise evidence, impact, and the smallest safe correction or decision path. Prefer observable behavior over author intent. Do not use rhetorical questions, self-reference, compliments, or boilerplate.

An `assertive` low-severity suggestion still needs high confidence, non-blocking disposition, exact current-delta anchoring, and a concrete improvement. Do not reclassify a speculative or style-only preference merely to increase comment volume.

When the sink is pre-existing, the body must distinguish it from the PR's changed enabling or worsening edge in one concise sentence; do not imply that the PR authored the sink.

## Sensitive information

Never copy credentials, tokens, cookies, private keys, personal data, or secret configuration values into a review. Name the secret class and code location, redact the value, and describe rotation or containment when relevant. Treat a literal credential introduced by the current diff as a security finding. For a historical value suspected to remain live, apply the external-state counterfactual rule above and do not test it against an external service.
