# GitHub Publishing Protocol

Use this reference for `audit`, `validate`, `publish`, `refresh`, and recovery. The bundled script is the sole write path for skill-owned GitHub reviews.

## Contents

- Requirements
- Review plan schema
- Read-only audit and validation
- Atomic publish protocol
- Statuses and exit behavior
- Refresh and duplicate handling
- Failure recovery
- Safety boundaries

## Requirements

- Install and authenticate the `gh` CLI for the PR host
- Use a full `https://<host>/<owner>/<repo>/pull/<number>` URL
- Keep the plan in a temporary local file and remove it after use
- Resolve the directory containing `SKILL.md` and use the transaction script's absolute path; never assume the current working directory is the skill package
- Use the full 40- or 64-character base and head SHAs returned by the same `audit`
- Ensure every plan comment has a stable semantic `finding_id` and an exact changed-line anchor

The script sets `GH_HOST` and passes `--hostname` from the PR URL. It never sends the plan to another provider.

Resolve the script once for all commands:

```bash
GH_REVIEW_TRANSACTION="<absolute-gh-review-pr-skill-dir>/scripts/gh_review_transaction.py"
```

## Review plan schema

```json
{
  "schema_version": 1,
  "base_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "head_sha": "0123456789abcdef0123456789abcdef01234567",
  "summary": "## Review summary\n\n`0123456` 기준 변경 파일 4개를 검토했으며 blocking 1건, non-blocking 0건, question 0건입니다. 생성 파일 1개는 source 기준으로 확인했습니다.",
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

- `schema_version` is exactly `1`
- `base_sha` and `head_sha` are full SHAs from the same frozen audit
- `summary` is one paragraph under `## Review summary`
- `summary` contains the abbreviated head and each exact count in either label-first form (`blocking N`) or count-first form (`N blocking`)
- `comments` contains zero to eight items
- `finding_id` values and `(path, line, side)` anchors are unique
- `line` is a positive integer and `side` is `RIGHT` or `LEFT`
- severity is `critical`, `high`, or `medium`; confidence is exactly `high`
- the first body line matches the disposition, severity, and category fields
- obvious secret literals and pre-existing skill markers are rejected

Use `RIGHT` only for an added line and `LEFT` only for a deleted line. The script rejects context-only, absent, binary, and truncated anchors.

## Read-only audit and validation

Audit before semantic review:

```bash
python3 "$GH_REVIEW_TRANSACTION" audit --pr https://github.example.com/owner/repo/pull/123
```

The JSON result includes the base/head SHAs, authenticated user, existing skill-owned reviews and findings, and pending-review conflicts. It is a snapshot and ownership preflight, not the semantic evidence bundle. It omits diff patches, commits, checks, the PR body, review bodies, inline-thread content, issue comments, and unresolved-thread state. Acquire those separately through authorized read-only GitHub tooling before semantic review; the sole-write-path restriction does not prohibit those reads.

Validate the completed plan immediately before writing:

```bash
python3 "$GH_REVIEW_TRANSACTION" validate \
  --pr https://github.example.com/owner/repo/pull/123 \
  --plan /tmp/gh-review-plan.json
```

`validate` reads current PR state, diff anchors, reviews, and comments. It performs no write. A no-op status means the exact base/head snapshot already has a skill-owned review; do not publish another one for that pair.

## Atomic publish protocol

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
6. Verify state, commit, marker ownership, count, path, line, side, body, and the unchanged base/head pair
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

Command errors, including invalid CLI usage, are emitted as sanitized JSON on stderr with a nonzero exit code. An `invalid-plan` or preflight `safety-stop` occurs before review creation; correct the input and run `validate` again. `validate` itself is read-only. After any nonzero `publish` result that may follow a write—especially `github-error`, `verification-failed`, timeout, or create/submit uncertainty—run a fresh `audit` before retrying.

## Refresh and duplicate handling

`refresh` is a semantic mode, not a force flag. When either base or head changes, audit the new pair, rebuild coverage and the ledger, retain existing threads as the discussion locations for old findings, and publish only genuinely new findings. The script permits one skill-owned review on the new snapshot but refuses a second one for the exact same pair.

Do not alter `finding_id` to evade duplicate detection. If the same concern remains on a new snapshot, omit a new thread. If only the wording is similar but the trigger or impact is materially different, use a genuinely distinct semantic identifier.

An exact owned pending transaction may be resumed after verification. A different owned pending transaction, a human pending review for the authenticated user, or mixed ownership stops the script for manual inspection.

## Failure recovery

- Base or head changed before submit: the script deletes only a provably skill-owned pending review, then stops; restart semantic review on the new snapshot
- Invalid or missing anchor: correct the plan from the frozen diff; do not move the comment to a nearby context line
- Permission denied: report the `gh` error; do not use another API, browser, issue comment, or summary-only fallback
- Create or submit response ambiguous: run `audit`; the script itself reconciles markers once and never blindly retries
- Pending verification failed: the script deletes the pending review only when its marker and every present comment prove exclusive skill ownership
- Final verification failed after submission: report the review ID and observed state; do not add a replacement review
- Human pending review present: leave it untouched and ask the user to submit or discard it before publishing

If safe deletion cannot be proven or confirmed, report the pending review ID and stop. Never delete a review merely because it is pending.

## Safety boundaries

- Do not hand-build `comments[][line]` fields; use the JSON plan
- Do not accept `line: null`, legacy `position`, file-level comments, or context-only anchors
- Do not copy review text into the summary when an inline anchor fails
- Do not retry a timeout by creating another review
- Do not edit, dismiss, resolve, reply to, or delete human review material
- Do not treat a static validation result as evidence that findings are semantically correct
- Do not claim successful publication until the final read verifies the expected state and comment count
