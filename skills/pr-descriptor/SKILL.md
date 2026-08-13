---
name: pr-descriptor
description: Create, rewrite, normalize, or evaluate consistent, review-ready pull request titles and descriptions from repository context, diffs, commits, issues, and validation evidence, and safely publish a description to an actual pull request only when explicitly requested in the current turn. Use when Codex needs a Korean or English PR artifact or an explicitly requested PR-description update for frontend, web, backend, API, library, data, CI/CD, Jenkins, scripting, infrastructure, configuration, dependency, security, migration, test, or documentation changes.
---

# PR Descriptor

Produce an evidence-based PR artifact that reviewers can paste and use without structural cleanup. Keep the format stable while adapting the depth and conditional sections to the actual change.

## Choose the output mode

Match the response to the user's request:

- `draft` or `create`: return the requested title and/or description
- `rewrite` or `normalize`: preserve supported facts and return the replacement artifact
- `evaluate` or `audit`: return findings and a verdict; rewrite only when requested
- `refine`: return the refined artifact; add refinement notes only when explicitly requested and keep them outside the PR body
- `title only` or `description only`: return only that artifact

For a complete PR draft, place `Title: <title>` before the body. Otherwise do not add an unrequested title, rationale, or commentary.

Treat publication as a separate delivery action layered onto the selected composition mode, not as an implied result of drafting, rewriting, normalizing, evaluating, or refining an artifact.

## Follow instruction precedence

Apply rules in this order:

1. Follow the user's explicit output, language, and formatting requirements
2. Preserve mandatory repository templates and contribution rules
3. Apply this skill's default structure and style contract

Map the required information into repository-owned headings, checklists, and metadata instead of duplicating them.

## Separate composition from publication

Treat PR-description publication as an overwrite-capable external mutation.

### Authorization boundary

- This skill composes or evaluates a PR artifact; invoking it does not by itself authorize publication
- Publish only when the user explicitly requests writing, updating, or applying the actual PR description in the current turn, or when a higher-priority instruction requires direct publication for that explicit request
- Do not infer publication authorization from requests to summarize work, organize or refresh documentation, audit drift, update a ticket, or otherwise clean up context; prior authorization does not carry forward
- Stop before mutation if the exact PR target or a safe publication procedure cannot be resolved

### Safe publication sequence

When publication is authorized, follow the applicable local or repository procedure while preserving these minimum safeguards:

When `gh` is supported, run [pr_description_transaction.py](scripts/pr_description_transaction.py); pass its publication flag only for current-turn authorization and its clear flag only for a current-turn explicit clear request.

1. Resolve the exact PR and the supported mutation mechanism
2. Capture the current body and a concurrency marker such as `updatedAt`, and keep the body as a separate backup
3. Write the complete candidate body to a different file, then verify that the file exists, contains the intended artifact, and is non-empty unless the user explicitly asked in the current turn to clear the description
4. Re-read the concurrency marker immediately before publishing and stop without writing if it changed
5. Publish from the candidate file; never use stdin such as `--body-file -`, an inline body argument, command substitution, or another mechanism that can silently turn missing input into an empty description
6. Fetch the published body and verify that it matches the candidate before reporting success

### Failure and recovery

- Keep the captured prior body until post-publication verification succeeds
- On failure, concurrency mismatch, or body mismatch, do not claim success or perform a blind follow-up write
- Restore the prior body only when the just-completed write is known to be the cause and no concurrent update occurred; otherwise report the state and request direction

## Build the description

### 1. Gather evidence

- Read applicable `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, PR templates, and release instructions
- Freeze the artifact snapshot before broader inspection: use the committed base-to-head diff for an existing PR, or the committed merge-base-to-`HEAD` diff for a branch draft
- Inspect the snapshot, changed-file summary, commits, issue context, existing PR text, and notes explicitly supplied for the current artifact
- Treat the frozen head as the PR subject; use reverted or test-only commits only as historical or validation context
- Treat earlier session details, discarded approaches, dirty working-tree changes, and untracked files as out-of-snapshot context unless the user explicitly asks to describe an intended future head
- Preserve validation evidence explicitly provided for the current artifact unless stronger evidence contradicts it
- Avoid reproducing secrets, credentials, tokens, or unnecessary sensitive values

Read [evidence-model.md](references/evidence-model.md) for snapshot boundaries, source priority, claim provenance, the concern ledger, validation acquisition, and deployment or rollback wording. Do not claim a motivation, behavior change, test result, deployment result, or risk reduction unless its evidence state permits that wording.

### 2. Build an internal concern ledger

Before drafting, group the diff into material reviewer concerns rather than individual files. Track each concern internally as:

```text
Concern | Current-head change | Why | Validation | Impact | Transition | Rollout source | Review entry point
```

Do not output this ledger unless requested. Reuse the same concern labels and order in `Changes`, `Validation`, and `Review Guide` where those sections apply. Every material concern must have completed validation or an explicit unverified status; atomic implementation bullets do not each need a separate validation line.

### 3. Select the language and title

- Use the language explicitly requested by the user
- Otherwise follow an established repository convention
- Otherwise use the language of the user's request
- Keep fixed English section headings unless a repository template or the user requires localized headings
- Preserve conventional code identifiers, commands, product names, and protocol terms
- Follow an established PR title convention when present
- Otherwise write a concise action or outcome title that stands alone
- Do not use only a branch name, ticket identifier, or vague title such as `Fix bug`

### 4. Classify the change

- Identify the primary intent and every affected project facet from changed behavior and files, not from the repository name
- Combine profiles for mixed application, data, infrastructure, dependency, or deployment changes
- Read [project-profiles.md](references/project-profiles.md) when project type or operational risk affects emphasis, validation, or conditional sections

### 5. Compose the core sections

Use this structure when no mandatory repository template overrides it:

```markdown
## Summary

<State what changed and why using the selected language's Summary form.>

## Changes

- <Group the current-head changes by reviewer concern>

## Validation

- <State completed evidence and uncovered concerns>
```

Apply these boundaries:

- `Summary`: explain what changed and why in exactly one prose paragraph; use one to three complete sentences in English or one to three concise report-style clauses in Korean; do not use lists, subheadings, tables, or code blocks
- `Changes`: state supported current-head behavior and decisions; group by concern and avoid exhaustive file narration
- `Validation`: state only completed checks and explicit evidence gaps; never turn a recommended check into a completed result

Use exact commands when they materially help reproduction. Do not repeat `Major files` lists; use a small ordered `Review Guide` for high-signal entry points. Include exact URLs, environment identifiers, paths, or configuration values only when their literal correctness is a review target.

### 6. Add triggered sections

Evaluate [project-profiles.md](references/project-profiles.md) before drafting. Append triggered sections after `Validation` in this order:

1. `## Impact`: user-visible, operational, security, performance, or compatibility consequences and risks
2. `## Migration`: one-time schema, data, state, public API, configuration cutover, or consumer transition work
3. `## Deployment and Rollback`: confirmed rollout or recovery procedures, recommended checks, and unresolved runbook gaps
4. `## Screenshots`: available or required visual UI evidence
5. `## Review Guide`: ordered review entry points, decision hotspots, and reviewer actions
6. `## Related Issues`: supplied issue, incident, design, dependency, or paired PR references

Treat every triggered section as required. Omit empty untriggered sections. If a repository template requires an inapplicable section, use its preferred marker or `N/A` with a short reason.

Keep the section roles distinct:

- Put consequences in `Impact`, not requests to reviewers
- Add `Migration` only for an actual one-time transition; a configuration file change alone is insufficient
- Distinguish confirmed deployment or rollback instructions from diff-inferred recommendations as required by [evidence-model.md](references/evidence-model.md)
- Put reviewer actions and uncertainty hotspots in `Review Guide`
- Mention each related item once, normally under `Related Issues`

Do not omit `Impact`, `Deployment and Rollback`, or `Review Guide` merely to shorten a material security, runtime, infrastructure, migration, or multi-domain PR.

## Enforce the style contract

- Write in a direct, professional, evidence-based tone
- Avoid conversational filler, self-reference, promotional language, and generated-by-AI commentary
- Use complete sentences with terminal punctuation in English prose paragraphs
- For Korean `Summary` text, use concise parallel report-style endings such as `추가`, `변경`, `정리`, `유지`, or `확인`; avoid polite narrative endings such as `-했습니다` or `-합니다` and omit terminal periods
- Use concise, parallel noun or verb phrases without terminal punctuation in bullet and numbered lists
- Split a list item that needs multiple sentences
- Wrap code identifiers, file paths, commands, configuration keys, and literal values in backticks
- Prefer reviewer-relevant behavior and decisions over exhaustive implementation narration
- State limitations, untested paths, compatibility concerns, and rollout risks plainly
- Keep Korean and English prose from mixing unnecessarily
- Preserve established terminology rather than translating identifiers or product names
- Scale detail with risk: keep small PRs compact and use concern subheadings plus `Review Guide` for large or mixed PRs

## Deliver the artifact

- For composition-only work, return Markdown without an outer code fence unless the user asks for one
- For composition-only work, return only the artifact required by the selected output mode
- After verified publication, report the exact PR target and verification result; return the body as well only when requested
- Preserve correct facts from an existing description while normalizing structure and style
- Keep requested audit or refinement notes visibly separate from the PR body

## Check before returning

- `Summary` communicates both what and why in one prose paragraph and follows the selected language's ending rule
- Every named change, file, and validation item belongs to the frozen snapshot or was explicitly supplied for the current artifact
- Every material claim has an appropriate evidence state
- Negative or exclusive claims such as `no impact`, `unchanged`, `not included`, or `only` have evidence covering the relevant scope
- Concern labels and order remain aligned across applicable sections
- Every material concern has completed validation or an explicit unverified status
- Completed, not-run, provided-manual, inferred, and unknown information are not conflated
- Conditional sections are present in the required order and keep distinct roles
- Deployment and rollback bullets disclose whether they are confirmed, recommended, or unverified
- Links, facts, file guidance, and reviewer actions are not duplicated across sections
- No bullet or numbered item ends with prose terminal punctuation
- Language, list form, and punctuation are consistent
- No sensitive value is exposed unnecessarily
- The response matches the delivery path: return only the requested artifact and explicitly requested separate notes for composition-only work; after publication, report the exact target and observed verification result, and include the body only when requested

Read [examples-ko.md](references/examples-ko.md) for Korean calibration or [examples-en.md](references/examples-en.md) for English calibration when an example is needed. Use examples for structure and tone, never as factual evidence.
