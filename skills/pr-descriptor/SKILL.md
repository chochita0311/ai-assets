---
name: pr-descriptor
description: Create, rewrite, normalize, or evaluate consistent, review-ready pull request titles and descriptions from repository context, diffs, commits, issues, and validation evidence. Use when Codex needs a Korean or English PR artifact for frontend, web, backend, API, library, data, CI/CD, Jenkins, scripting, infrastructure, configuration, dependency, security, migration, test, or documentation changes.
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

## Follow instruction precedence

Apply rules in this order:

1. Follow the user's explicit output, language, and formatting requirements
2. Preserve mandatory repository templates and contribution rules
3. Apply this skill's default structure and style contract

Map the required information into repository-owned headings, checklists, and metadata instead of duplicating them.

## Build the description

### 1. Gather evidence

- Read applicable `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, PR templates, and release instructions
- Inspect the base and head branches, current diff, changed-file summary, commits, issue context, existing PR text, and user-provided notes
- Treat the final head as the PR subject; use reverted or test-only commits only as historical or validation context
- Preserve explicit user-provided validation evidence unless stronger evidence contradicts it
- Avoid reproducing secrets, credentials, tokens, or unnecessary sensitive values

Read [evidence-model.md](references/evidence-model.md) for claim provenance, the concern ledger, validation acquisition, and deployment or rollback wording. Do not claim a motivation, behavior change, test result, deployment result, or risk reduction unless its evidence state permits that wording.

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

<State what changed and why in one to three complete sentences.>

## Changes

- <Group the current-head changes by reviewer concern>

## Validation

- <State completed evidence and uncovered concerns>
```

Apply these boundaries:

- `Summary`: explain what changed and why in exactly one prose paragraph of one to three complete sentences; do not use lists, subheadings, tables, code blocks, or fragments
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
- Use complete sentences with terminal punctuation in prose paragraphs
- Use concise, parallel noun or verb phrases without terminal periods in bullet and numbered lists
- Split a list item that needs multiple sentences
- Wrap code identifiers, file paths, commands, configuration keys, and literal values in backticks
- Prefer reviewer-relevant behavior and decisions over exhaustive implementation narration
- State limitations, untested paths, compatibility concerns, and rollout risks plainly
- Keep Korean and English prose from mixing unnecessarily
- Preserve established terminology rather than translating identifiers or product names
- Scale detail with risk: keep small PRs compact and use concern subheadings plus `Review Guide` for large or mixed PRs

## Return a paste-ready artifact

- Return Markdown without an outer code fence unless the user asks for one
- Return only the artifact required by the selected output mode
- Preserve correct facts from an existing description while normalizing structure and style
- Keep requested audit or refinement notes visibly separate from the PR body

## Check before returning

- `Summary` communicates both what and why in one prose paragraph
- Every material claim has an appropriate evidence state
- Concern labels and order remain aligned across applicable sections
- Every material concern has completed validation or an explicit unverified status
- Completed, not-run, provided-manual, inferred, and unknown information are not conflated
- Conditional sections are present in the required order and keep distinct roles
- Deployment and rollback bullets disclose whether they are confirmed, recommended, or unverified
- Links, facts, file guidance, and reviewer actions are not duplicated across sections
- Language, list form, and punctuation are consistent
- No sensitive value is exposed unnecessarily
- The response contains only the requested artifact and any explicitly requested separate notes

Read [examples-ko.md](references/examples-ko.md) for Korean calibration or [examples-en.md](references/examples-en.md) for English calibration when an example is needed. Use examples for structure and tone, never as factual evidence.
