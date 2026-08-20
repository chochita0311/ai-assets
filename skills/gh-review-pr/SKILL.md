---
name: gh-review-pr
description: Review, draft, publish, audit, refresh, amend, or reply to skill-owned GitHub and GitHub Enterprise pull request reviews from a frozen base-to-head snapshot, producing a useful review summary and high-confidence inline threads while preventing duplicate, unanchored, or partially published comments. Use when Codex is asked to review a PR, post inline code-review findings, rerun an automated review, audit existing human or skill-owned review feedback, correct the wording of a skill-owned finding, or respond to a skill-owned finding; do not use for editing PR titles or descriptions, posting replies to human-authored review threads, or general local code review without a PR.
---

# GitHub PR Reviewer

Produce one review for one immutable PR `(base SHA, head SHA)` snapshot, or safely maintain that review's skill-owned findings after submission. Keep semantic judgment separate from every GitHub write transaction.

## Choose the operating mode

- `publish`: use for an explicit `$gh-review-pr <PR URL>` invocation or a clear request to review and post; publish one review after all gates pass
- `draft`: use when the user says draft, preview, or do not post; return the summary and proposed threads without any GitHub write
- `audit`: inspect existing reviews, duplicate state, anchors, a prior run, or human-authored feedback without writing
- `refresh`: re-review an explicitly requested snapshot whose base or head changed; never add a second skill-owned review to the same base/head pair
- `amend`: correct only the wording of one submitted skill-owned finding after an explicit request; preserve its classification, anchor, marker, and review summary
- `reply`: respond to one submitted skill-owned finding after an explicit request; target the original review snapshot even when the current PR head has advanced, and never use this mode for human-authored threads

The operating `audit` mode is a complete read-only review task. The transaction script's `audit` subcommand is only the snapshot and ownership preflight required before semantic work in the review-building modes; it does not perform the review itself.

Treat a full PR URL as the canonical target. Resolve a missing URL only when the current repository and branch identify exactly one PR. A generic request to inspect code without an identifiable PR is outside this skill.

Use `COMMENT` by default. Use `APPROVE` or `REQUEST_CHANGES` only when the user explicitly requests that review decision; never infer it from finding counts.

The transaction accepts `APPROVE` only with zero blocking findings and `REQUEST_CHANGES` only with at least one blocking finding. These are compatibility guards for an explicitly chosen event, not rules for choosing the event.

## Preserve hard invariants

- Freeze the base SHA and head SHA before reviewing, and bind every artifact to that pair
- Review the committed base-to-head diff; exclude dirty and untracked working-tree state
- Cover every human-authored changed line or name every generated, vendored, binary, truncated, or otherwise unreviewed gap
- Publish at most one skill-owned review per PR base/head snapshot and at most eight inline findings
- Anchor every inline thread to the exact added or deleted line that introduces or materially worsens the trigger or impact; never move it to merely reachable nearby code
- Publish only current-snapshot, reachable findings with `critical`, `high`, or `medium` severity and `high` confidence
- Keep low-confidence possibilities, style-only preferences, and mechanical lint in private analysis unless a repository rule makes them material
- Never force an inline finding to make a review look useful; make a zero-finding result earn its conclusion through explicit negative evidence
- Never expose literal secrets; describe the class, location, and remediation without repeating the value
- Never convert a failed inline thread into an issue comment, summary detail, or unanchored fallback
- Never retry an ambiguous write until remote state has been reconciled
- Never use an amendment to change a finding's disposition, severity, category, anchor, marker, or summary counts
- Never reply outside a verified skill-owned finding; re-read the current PR pair immediately before a new reply and report both the review head and current head
- Never edit or delete a human-authored review, thread, or pending review

## Review the PR

### 1. Resolve authority and freeze the target

Read applicable repository instructions, including nested `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, pull request templates, and explicit review guidance. Treat repository style guidance such as `.gemini/styleguide.md` as criteria below executable behavior and repository rules.

Use the full PR URL for every GitHub operation. For GitHub Enterprise, set `GH_HOST` to the URL host; the bundled transaction script does this automatically.

Resolve the directory containing this `SKILL.md`, then set `GH_REVIEW_TRANSACTION` to the script's absolute path. Never resolve it from the target repository's working directory.

```bash
GH_REVIEW_TRANSACTION="<absolute-gh-review-pr-skill-dir>/scripts/gh_review_transaction.py"
python3 "$GH_REVIEW_TRANSACTION" audit --pr <full-pr-url>
```

Record the returned base and head SHAs. The audit result establishes snapshot and transaction ownership state only; it is not the semantic review evidence bundle. Separately fetch the PR diff and file patches, changed files, commits, checks, PR body, review bodies, inline threads, issue comments, and unresolved-thread state through authorized read-only GitHub tooling. The bundled-script-only rule applies to review writes, not to those reads.

Re-read both SHAs before adjudication and again through the transaction script before publishing. If either changed, discard snapshot-bound analysis and restart on the new pair.

### 2. Build evidence before findings

Use this source priority when inputs disagree:

1. Frozen base-to-head diff and code behavior
2. Applicable repository rules
3. Tests, checks, and reproducible validation for that snapshot
4. Explicitly supplied issue, design, incident, or operational context
5. PR body and commits as claimed intent
6. Existing comments as discussion and duplicate context, not behavioral truth

Use a local checkout only when it can represent the exact frozen base and head commits; otherwise inspect immutable remote content. Read [review-criteria.md](references/review-criteria.md) before classifying or publishing findings. It owns [review depth and independence](references/review-criteria.md#review-depth-and-independence), [change mapping and review passes](references/review-criteria.md#change-map-and-review-passes), severity, confidence, causality, reachability, counterevidence, the internal finding ledger, [zero-finding adjudication](references/review-criteria.md#zero-finding-gate), and [human-feedback audits](references/review-criteria.md#human-feedback-audits).

Classify the semantic pass as `fresh-review` or `self-review`. If the active session authored or extensively designed the change, treat its earlier explanations only as claimed intent and run a clean-room adversarial pass from the frozen artifacts. For security-sensitive, cross-service, behavior-removal, migration, or otherwise complex changes, obtain a quality-first semantic pass and, when the runtime and user authority permit it, a separate no-history omission challenge before publication—even when the first pass found issues. Reconcile the union through the same publication gates. If adequate depth or independence is unavailable, stop in `draft` with that gap; never treat one discovered finding as proof that coverage is complete.

When the runtime provides suitable named workers, `evidence_scout` may gather bounded multi-file call-path or test evidence and `bounded_verifier` may run an exact validation packet. A separately configured review-capable worker may challenge candidate coverage only when its competence and no-history input meet the repository's delegation rules. Pass only frozen task artifacts. The primary agent must retain scope, security judgment, final adjudication, publication, and completion approval. The skill does not bind a model name.

### 3. Adjudicate before composing

Build the change map and complete the boundary, behavioral-delta, integration, test, design, and adversarial passes before applying publication gates. Do not begin with the question “what can I comment on?”; first establish what changed, which invariant it can break, and which concrete evidence disproves each serious candidate. A zero-finding result requires the [zero-finding gate](references/review-criteria.md#zero-finding-gate).

Apply every authoritative [publication gate](references/review-criteria.md#publication-gates), including its counterfactual current-delta and exact-anchor checks. If any gate fails, omit the candidate or record a material evidence gap instead of publishing it. Do not publish first and investigate later. A question disposition still requires high confidence that the ambiguity creates a material review risk.

### 4. Compose separate artifacts

Create the summary as exactly one paragraph under `## Review summary`. Give a concise change-and-risk synopsis and name the main review focus, then include the abbreviated head SHA, reviewed file count, exact numeric counts, and any material coverage, independence, or review-depth gap. Use language-appropriate order: `blocking N`, `non-blocking N`, and `question N` in Korean, or `N blocking`, `N non-blocking`, and `N question` findings in English. Do not repeat thread titles, detailed evidence, or remediation. For zero findings, say that no high-confidence finding was found within the stated coverage; do not claim the change is safe or defect-free.

Write one concern per inline thread. Start it with:

```text
issue (<blocking|non-blocking|question>, <critical|high|medium>, <category>): <concise title>
```

Then state the triggering behavior, impact, and smallest safe correction or decision. Do not add praise, nits, generic review advice, or duplicated summary prose. Read [examples-ko.md](references/examples-ko.md) or [examples-en.md](references/examples-en.md) only when language calibration is useful.

### 5. Complete the selected mode safely

For `audit`, return the frozen base/head pair, ownership and duplicate state, pending-review state, the requested review or anchor findings, and material evidence gaps. When auditing human feedback, classify each concern and provide evidence, the smallest recommended action, and a concise response draft, but never post the response. Stop without creating or submitting a review.

For `draft`, stop after returning the proposed summary, frozen base/head pair, coverage and review-depth gaps, plus publish-ready metadata for every proposed thread: `finding_id`, path, line, side, severity, confidence, disposition, category, and body. With zero proposed threads, also return the compact [session-only evidence receipt](references/review-criteria.md#artifact-writing); keep it outside the GitHub summary and JSON plan.

For `publish` or `refresh`, create a temporary JSON plan and follow [github-publishing.md](references/github-publishing.md). It owns the plan schema, commands, status meanings, pending-review protocol, reconciliation rules, and failure handling.

Use the already resolved absolute script path for review creation and submission:

```bash
python3 "$GH_REVIEW_TRANSACTION" validate --pr <full-pr-url> --plan <plan-json>
python3 "$GH_REVIEW_TRANSACTION" publish --pr <full-pr-url> --plan <plan-json>
```

Pass `--event APPROVE` or `--event REQUEST_CHANGES` only for the user's explicit decision request. Do not reconstruct the write with ad hoc `gh api`, GraphQL, MCP, `curl`, browser actions, or individual comment calls if the script stops. If `gh` fails, report its sanitized error and the transaction status; do not switch providers.

After publication, report the final review URL or ID, bound base/head SHAs, event, inline count, and any evidence gap. When the inline count is zero, also return the compact zero-finding evidence receipt in the session so the user can distinguish a supported empty review from a hollow summary. Delete the temporary plan unless the user explicitly asks to retain it.

## Maintain a submitted skill-owned finding

Use `amend` or `reply` only when the user explicitly requests that mutation. Do not rerun the semantic review unless the user also asks for a refresh.

For `amend`, require the current PR base/head pair to still match the submitted review's frozen pair and preserve the existing finding classification. If the correction would change disposition, severity, category, anchor, or summary counts, stop: body-only amendment cannot keep the review artifact internally consistent.

For `reply`, bind the target fields to the original review marker. A newer current PR head is allowed because fixes are normally pushed before a response, but the transaction must prove the owned target and re-read the current PR pair before writing. Follow the amendment and reply schemas, commands, status meanings, and reconciliation rules in [github-publishing.md](references/github-publishing.md). Keep the temporary mutation file until the result is verified or a failed write is reconciled; remove it afterward unless the user asks to retain it.

After an amendment, report its status, review and comment IDs, finding ID, and comment URL. After a reply, also distinguish the original `review_head_sha` from `current_head_sha`.

## Keep adjacent work separate

This skill owns reviewer artifacts only. It does not edit source code, PR titles, PR descriptions, issues, or human review threads. Treat requested PR title or body work as a separate task governed by whatever available capability explicitly owns PR metadata; do not assume a named companion skill is installed. When both artifacts are produced, bind them to the same frozen base/head snapshot without making either workflow a dependency of the other.

## Stop without an unsafe fallback

If a later pass finds a material omission in an already submitted skill-owned review for the same snapshot, follow the [same-snapshot omission rule](references/github-publishing.md#refresh-and-duplicate-handling): return a corrected draft and stop without an ad hoc write.

Stop without writing when the target is ambiguous, a review-building mode's frozen SHA changes, an amendment no longer matches the current PR pair, a reply's current PR pair changes while the write is being prepared, required diff data is truncated at a proposed anchor, permissions fail, a human pending review could be affected, duplicate state cannot be resolved, or read-after-write verification is incomplete.
