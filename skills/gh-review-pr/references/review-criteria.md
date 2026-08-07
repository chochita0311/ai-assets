# Review Criteria

Use this reference to decide what belongs in a GitHub review. The transaction script can validate structure and anchors; it cannot decide whether a finding is true or useful.

## Contents

- Coverage model
- Candidate ledger
- Publication gates
- Severity and disposition
- Confidence
- Review categories
- Existing discussions and duplicates
- Artifact writing
- Sensitive information

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

## Candidate ledger

Keep this internal ledger before writing review artifacts:

```text
finding_id | concern | path | line | side | severity | confidence | disposition | category | current-snapshot evidence | reachability | impact | counterevidence | safe path | duplicate state
```

Use a stable lowercase hyphenated `finding_id` that names the semantic concern rather than its wording or line number. Reuse it while reconciling the same concern; never mint a new identifier merely to bypass duplicate detection.

## Publication gates

Publish a candidate only when every answer is `yes`:

1. Is the behavior introduced or materially worsened by the frozen base-to-head diff?
2. Is there a concrete reachable trigger rather than a hypothetical possibility?
3. Does direct code, test, runtime, or protocol evidence support the claim?
4. Has relevant counterevidence been inspected and resolved?
5. Is the severity at least `medium` and confidence `high`?
6. Is an exact added (`RIGHT`) or deleted (`LEFT`) line available as the anchor?
7. Is the concern absent from existing review threads and skill markers?
8. Can the thread state impact and a minimal safe path without prescribing a broad redesign?

Omit pre-existing defects unless this PR makes them reachable, more severe, or harder to recover from. Do not report speculative future misuse, purely aesthetic preferences, or issues a deterministic check already communicates better.

## Severity and disposition

Assign severity by impact, not by fix size:

- `critical`: credible compromise, irreversible loss, or broad production outage with no practical containment
- `high`: material security, correctness, data, compatibility, or availability failure on a realistic path
- `medium`: bounded but meaningful behavior, reliability, operability, or maintainability failure worth fixing in this PR
- `low`: small improvement, style preference, local cleanup, or unlikely edge case; do not publish inline by default

Assign one disposition:

- `blocking`: the PR should not merge with the finding unresolved
- `non-blocking`: material and actionable, but safe to follow up without holding the merge
- `question`: intent or contract must be resolved before the impact can be handled correctly

Disposition does not replace severity. A `question` is not a license to publish a low-confidence guess.

## Confidence

Use `high` only when the relevant execution or data path is directly supported and competing explanations have been eliminated. Typical evidence includes a reproducible failure, a contradicted invariant, an API or schema mismatch, or a traceable path from changed input to impact.

Use `medium` when the concern is likely but depends on an unverified caller, environment, or contract. Use `low` when it is primarily speculative. Gather more evidence when practical; otherwise keep medium- and low-confidence candidates out of inline publication and state only the resulting coverage gap when material.

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

## Existing discussions and duplicates

Read existing reviews, inline threads, issue comments, and unresolved conversations before composing. They are evidence of prior discussion, not proof of current behavior.

Treat a concern as duplicate when an existing thread identifies the same trigger and impact, even if wording, line, or suggested fix differs. Continue the human conversation only when the user explicitly asks; this skill does not edit or reply to human threads. A skill-owned `finding_id` is a hard duplicate signal across reruns.

When a new snapshot resolves an old finding, do not post a congratulatory or closure thread. When it leaves an old finding unresolved, keep the existing thread as the discussion location instead of reposting it under a new identifier.

## Artifact writing

The summary has one heading and one prose paragraph:

```markdown
## Review summary

<head, reviewed file count, blocking/non-blocking/question counts, and material coverage gap>
```

Do not enumerate findings there. Keep “no findings” scoped to the evidence: say no high-confidence finding was found within reviewed coverage, not that the PR is safe.

Each thread begins with one Conventional Comments-style label:

```text
issue (blocking, high, correctness): Preserve the previous value on a rejected update
```

Follow with concise evidence, impact, and the smallest safe correction or decision path. Prefer observable behavior over author intent. Do not use rhetorical questions, self-reference, compliments, or boilerplate.

## Sensitive information

Never copy credentials, tokens, cookies, private keys, personal data, or secret configuration values into a review. Name the secret class and code location, redact the value, and describe rotation or containment when relevant. Treat a suspected live secret as a security finding; do not test it against an external service.
