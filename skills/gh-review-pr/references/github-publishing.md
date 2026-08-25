# GitHub Publishing Protocol

Use this reference for the exact review plan schema, renderer behavior, `audit`, `validate`, `publish`, `refresh`, `amend`, `reply`, and recovery. The bundled script is the sole write path for skill-owned GitHub reviews. Use [review-criteria.md](review-criteria.md) for semantic coverage, adjudication, and reviewer-supplied content quality.

## Contents

- [Requirements](#requirements)
- [Read-only audit](#read-only-audit)
- [Review plan schema](#review-plan-schema)
- [Validate and publish atomically](#validate-and-publish-atomically)
- [Statuses and exit behavior](#statuses-and-exit-behavior)
- [Refresh and duplicate handling](#refresh-and-duplicate-handling)
- [Failure recovery](#failure-recovery)
- [Owned finding amendments](#owned-finding-amendments)
- [Owned finding replies](#owned-finding-replies)
- [Safety boundaries](#safety-boundaries)

## Requirements

- Install and authenticate the `gh` CLI for the PR host
- Use a full `https://<host>/<owner>/<repo>/pull/<number>` URL
- Keep each review plan, amendment, or reply in a temporary local file through verification and any failure reconciliation; remove it after a verified result unless the user asks to retain it
- Resolve the directory containing `SKILL.md` and use the transaction script's absolute path; never assume the current working directory is the skill package
- For a review plan, use the current full base/head pair returned by the same `audit`. For an amendment or reply, use the target review marker's full pair from that audit. An amendment also requires the marker pair to match the current PR pair; a reply does not.
- Ensure every plan comment has a stable semantic `finding_id` and an exact changed-line anchor

The script sets `GH_HOST` and passes `--hostname` from the PR URL. It never sends the plan to another provider.

Resolve the script once for all commands:

```bash
GH_REVIEW_TRANSACTION="<absolute-gh-review-pr-skill-dir>/scripts/gh_review_transaction.py"
```

## Read-only audit

Audit before semantic review:

```bash
python3 "$GH_REVIEW_TRANSACTION" audit --pr https://github.example.com/owner/repo/pull/123
```

The JSON result includes the base/head SHAs, authenticated user, existing skill-owned reviews and findings, and pending-review conflicts. It is a snapshot and ownership preflight, not the semantic evidence bundle. It omits diff patches, commits, checks, the PR body, review bodies, inline-thread content, issue comments, and unresolved-thread state. Acquire those separately through authorized read-only GitHub tooling before semantic review; the sole-write-path restriction does not prohibit those reads.

## Review plan schema

```json
{
  "schema_version": 2,
  "base_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "head_sha": "0123456789abcdef0123456789abcdef01234567",
  "profile": "balanced",
  "summary": {
    "overview": "이 PR은 빈 권한 목록의 갱신 의미를 변경하며, 권한 회수와 실패 원자성이 주요 위험 표면입니다.",
    "scope": "Human-authored 변경 파일 4개를 검토했고 생성 파일 1개는 generator와 schema 기준으로 확인했습니다.",
    "focus": [
      "빈 목록에서의 권한 회수",
      "갱신 실패 시 상태 원자성"
    ],
    "evidence": [
      {
        "area": "boundary-behavior",
        "detail": "Base와 head의 빈 목록 분기 및 저장 순서를 직접 대조했습니다."
      },
      {
        "area": "integration-consumers",
        "detail": "권한 값이 최종 authorization check에 소비되는 경로를 추적했습니다."
      },
      {
        "area": "tests-validation",
        "detail": "권한 회수 및 갱신 실패 테스트를 확인했습니다."
      }
    ],
    "coverage_gaps": [],
    "review_notes": [
      {
        "label": "positive",
        "text": "생성 client를 schema source와 함께 갱신해 계약 추적성이 유지됩니다."
      }
    ]
  },
  "comments": [
    {
      "finding_id": "retain-permission-on-empty-update",
      "path": "src/permissions.ts",
      "line": 84,
      "side": "RIGHT",
      "severity": "high",
      "confidence": "high",
      "disposition": "blocking",
      "category": "security",
      "body": "issue (blocking, high, security): 빈 권한 목록에서 기존 권한이 유지됩니다\n\n현재 분기는 빈 목록을 갱신 없음으로 처리해 회수 요청을 무시합니다. 빈 목록도 명시적 교체로 적용해 기존 권한이 남지 않게 해주세요."
    }
  ]
}
```

Rules enforced by the script:

- `schema_version` is exactly `2`; marker-aware audit and maintenance continue to recognize submitted version 1 reviews
- `base_sha` and `head_sha` are full SHAs from the same frozen audit
- `profile` is `focused`, `balanced`, or `assertive`
- `summary` is an object with exactly `overview`, `scope`, `focus`, `evidence`, `coverage_gaps`, and `review_notes`
- summary values are bounded plain one-line content so they cannot inject headings, lists, HTML markers, or a second review structure
- the transaction renders a stable two-column GitHub Markdown `Review receipt`, escapes table separators in reviewer-supplied cells, and owns the surrounding blank-line hierarchy
- the transaction renders the abbreviated head, profile, exact material-finding counts, and a separate assertive-suggestion count; only nonzero counts are bold
- material coverage gaps produce one `WARNING` alert after the receipt with one blockquoted bullet per gap, while an empty gap list produces no alert
- summary content may contain at most one `✅`, only as the trailing status cue on an exact `tests-validation` evidence fact
- `focus` contains one to four items; `evidence` contains two to five objects with unique `area` values and at least three when there is no `medium+` issue thread, including suggestion-only reviews; `coverage_gaps` contains zero to four items
- each evidence object has exactly `area` and `detail`; `area` is one of `boundary-behavior`, `integration-consumers`, `tests-validation`, `design-adversarial`, or `independence`
- `focused` permits no review notes, `balanced` permits up to three, and `assertive` permits up to five; each note is labeled `optional`, `fyi`, or `positive`
- `comments` contains zero to eight items
- `finding_id` values and `(path, line, side)` anchors are unique
- `line` is a positive integer and `side` is `RIGHT` or `LEFT`
- severity is `critical`, `high`, or `medium` with confidence exactly `high`; explicitly selected `assertive` also permits high-confidence `low` comments only as non-blocking `suggestion` threads
- a `medium+` body starts with `issue (<blocking|non-blocking|question>, <critical|high|medium>, <category>): <concise title>` and matches its disposition, severity, and category fields
- an explicitly selected `assertive` low body starts with `suggestion (non-blocking, low, <category>): <concise title>`
- obvious secret literals and pre-existing skill markers are rejected

Use `RIGHT` only for an added line and `LEFT` only for a deleted line. The script rejects context-only, absent, binary, and truncated anchors.

## Validate and publish atomically

Validate the completed plan immediately before writing:

```bash
python3 "$GH_REVIEW_TRANSACTION" validate \
  --pr https://github.example.com/owner/repo/pull/123 \
  --plan /tmp/gh-review-plan.json
```

`validate` reads current PR state, diff anchors, reviews, and comments. It performs no write. A no-op status means the exact base/head snapshot already has a skill-owned review; do not publish another one for that pair.

Run only after `validate` succeeds:

```bash
python3 "$GH_REVIEW_TRANSACTION" publish \
  --pr https://github.example.com/owner/repo/pull/123 \
  --plan /tmp/gh-review-plan.json
```

For an explicitly requested decision, append `--event APPROVE` or `--event REQUEST_CHANGES`. Otherwise omit the flag and keep `COMMENT`.

`APPROVE` is compatible only with zero blocking findings. `REQUEST_CHANGES` is compatible only with at least one blocking finding. These guards validate the user's explicit event; they never infer or select it.

The script performs this transaction:

1. Re-fetch the PR base/head pair, changed-file patches, reviews, comments, and the authenticated user
2. Reject stale base/head pairs, invalid anchors, prior finding identifiers, same-snapshot reviews, and human pending-review conflicts
3. Add stable hidden run and finding markers to the payload
4. Create one review in `PENDING` state with all inline comments in one JSON request
5. Re-fetch the pending review and its comments
6. Verify state, commit, marker ownership, count, path, exact frozen-diff anchor, body, and the unchanged base/head pair. Prefer returned `line` and `side`; only when both are absent, accept the exact legacy `original_position` computed from the same complete frozen patch and bound to the planned head commit.
7. Delete the owned pending review and stop if pre-submit verification fails
8. Submit the verified pending review with the requested event and summary
9. Read after write and verify final state, markers, count, and anchors

The script never posts issue comments and never falls back to individual inline calls.

## Statuses and exit behavior

Successful JSON statuses include:

- `audit`: read-only state returned
- `valid`: the plan can create a new pending review
- `resume-ready`: an exact skill-owned pending transaction can be resumed
- `noop-existing-snapshot`: a submitted skill-owned review already exists for this exact base/head pair
- `published`: creation, submission, and read-after-write verification completed
- `published-reconciled`: a write response was ambiguous, but remote reconciliation proved the intended final review exists
- `amended`: one submitted skill-owned finding was updated and verified
- `amended-reconciled`: the amendment response was ambiguous, but read-after-write verification proved the requested body exists
- `replied`: one reply to a submitted skill-owned finding was created and verified
- `replied-reconciled`: the reply response was ambiguous, but reconciliation proved exactly one requested reply exists
- `noop-existing-reply`: an identical authenticated-user reply already exists on the owned finding, so no write occurred

Command errors, including invalid CLI usage, are emitted as sanitized JSON on stderr with a nonzero exit code. An `invalid-plan` or preflight `safety-stop` occurs before review creation; correct the input and run `validate` again. `validate` itself is read-only. After any nonzero `publish` result that may follow a write—especially `github-error`, `verification-failed`, timeout, or create/submit uncertainty—run a fresh `audit` before retrying.

## Refresh and duplicate handling

`refresh` is a semantic mode, not a force flag. When either base or head changes, audit the new pair, rebuild coverage and the ledger, retain existing threads as the discussion locations for old findings, and publish only genuinely new findings. The script permits one skill-owned review on the new snapshot but refuses a second one for the exact same pair.

Do not alter `finding_id` to evade duplicate detection. If the same concern remains on a new snapshot, omit a new thread. If only the wording is similar but the trigger or impact is materially different, use a genuinely distinct semantic identifier.

If a later semantic pass finds a material omission in an already submitted skill-owned review for the exact same base/head pair, return a corrected draft and stop. The current transaction cannot atomically replace the submitted summary and add new inline findings, so never work around the same-snapshot guard with a standalone comment or an altered `finding_id`.

An exact owned pending transaction may be resumed after verification. A different owned pending transaction, a human pending review for the authenticated user, or mixed ownership stops the script for manual inspection.

## Failure recovery

- Base or head changed before submit: the script deletes only a provably skill-owned pending review, then stops; restart semantic review on the new snapshot
- Invalid or missing anchor: correct the plan from the frozen diff; do not move the comment to a nearby context line
- Permission denied: report the `gh` error; do not use another API, browser, issue comment, or summary-only fallback
- Create or submit response ambiguous: run `audit`; the script itself reconciles markers once and never blindly retries
- Amendment or reply result remains ambiguous after the script's reconciliation: keep the mutation file, inspect the target comment or thread through authorized read-only GitHub tooling, and do not retry until the intended remote state is conclusively present or absent
- Amendment read-after-write verification fails: do not blindly restore the prior body or issue another patch; report the target review and finding identifiers and reconcile the current comment first
- Pending verification failed: the script deletes the pending review only when its marker and every present comment prove exclusive skill ownership
- Final verification failed after submission: report the review ID and observed state; do not add a replacement review
- Human pending review present: leave it untouched and ask the user to submit or discard it before publishing

If safe deletion cannot be proven or confirmed, report the pending review ID and stop. Never delete a review merely because it is pending.

## Owned finding amendments

When the user explicitly asks to correct the wording of a submitted skill-owned finding, use `amend` rather than an ad hoc API call. The amendment file uses this exact schema; `base_sha` and `head_sha` identify the submitted review snapshot, and `body` omits the hidden marker.

```json
{
  "schema_version": 2,
  "base_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "head_sha": "0123456789abcdef0123456789abcdef01234567",
  "review_id": 456,
  "finding_id": "retain-permission-on-empty-update",
  "body": "issue (blocking, high, security): 빈 권한 목록의 실패 경로를 명확히 합니다\n\n변경된 분기가 기존 권한을 유지하는 조건과 영향, 최소 수정 경로를 정확히 설명합니다."
}
```

```bash
python3 "$GH_REVIEW_TRANSACTION" amend \
  --pr https://github.example.com/owner/repo/pull/123 \
  --amendment /tmp/gh-review-amendment.json
```

The script permits wording-only corrections after proving the review and comment are submitted, authored by the authenticated user, owned by matching review/finding markers, and still bound to the current frozen base/head pair. The replacement header's disposition, severity, and category must exactly match the submitted finding so the review summary counts remain valid. It preserves the original run marker, performs one PATCH, and reads the comment back. It never moves the anchor or changes human-authored material. If classification or summary must change, stop; that requires a separately designed review-level amendment contract.

A successful result reports the status, PR, frozen base/head pair, review ID, comment ID, finding ID, and comment URL. Remove the temporary amendment file after the verified result unless the user asks to retain it.

## Owned finding replies

When the user explicitly asks to respond to a submitted skill-owned finding, use `reply`. The reply file uses this exact schema. Its `base_sha` and `head_sha` identify the original submitted review snapshot, not necessarily the current PR snapshot, and `body` is a plain response without a skill marker.

```json
{
  "schema_version": 2,
  "base_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "head_sha": "0123456789abcdef0123456789abcdef01234567",
  "review_id": 456,
  "finding_id": "retain-permission-on-empty-update",
  "body": "수정 커밋 89abcde에서 빈 목록도 명시적 교체로 처리했습니다."
}
```

```bash
python3 "$GH_REVIEW_TRANSACTION" reply \
  --pr https://github.example.com/owner/repo/pull/123 \
  --reply /tmp/gh-review-reply.json
```

The script proves ownership of the original target finding without requiring the current PR head to equal the review head. It prevents an identical reply from being posted twice, re-reads the current base/head pair immediately before a new write to stop a preparation-time race, performs one reply write, and reads the created reply back. It never replies to human-authored review material.

A reply result reports both the original `review_base_sha` / `review_head_sha` and the pre-write `current_base_sha` / `current_head_sha`; the legacy `base_sha` / `head_sha` fields also identify the original review snapshot. It also reports the review, target comment, reply comment, and finding IDs plus the comment URL. Remove the temporary reply file after the verified result unless the user asks to retain it.

## Safety boundaries

- Do not hand-build `comments[][line]` fields; use the JSON plan
- Do not accept `line: null`, legacy `position`, file-level comments, or context-only anchors in a plan or write payload. A read-back response may be verified through its legacy `original_position` only under the exact frozen-patch and planned-head checks in the atomic protocol.
- Do not copy review text into the summary when an inline anchor fails
- Do not retry a timeout by creating another review
- Do not edit, dismiss, resolve, reply to, or delete human review material
- Do not treat a static validation result as evidence that findings are semantically correct
- Do not claim successful publication until the final read verifies the expected state and comment count
