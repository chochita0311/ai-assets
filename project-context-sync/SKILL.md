---
name: project-context-sync
description: Keep local project context synchronized across sessions and repositories. Use when work spans one or multiple repos, when repeated re-explanations slow progress, and when optional external references must stay aligned.
---

# Project Context Sync

Use this skill to keep work context accurate and reusable across sessions.
Its core purpose is local project working-context continuity across sessions.
It supports:
- no-reference workflows
- reference-backed workflows (tickets, wiki pages, site URLs, docs, or mixed)
- follow-up workflows with linked references (for example parent/child tickets)

## Core Goal

Preserve momentum by reducing three recurring costs:
- search cost: re-finding files and modules
- re-explanation cost: repeating known facts each session
- drift cost: stale context that no longer matches code

## Scope Model

Always model context at two levels:
- `project root`: local workspace boundary, for example `<project-root>`
- `current repo`: actively edited repository inside the root

Optionally add:
- `related repos`: producer, consumer, scheduler, downstream, interface readers

## Reference Scope (Flexible)

Reference handling is optional and extensible.
Use it only when external references are needed to keep local context correct.

When references exist:
- record a short `reference scope` statement
- record concrete `references in scope` (type + identifier/link)
- record relationship hints when relevant (for example parent/child, base spec/change log)

Do not hardcode source types in the contract.
New source types should be addable without changing the core workflow.

## Source Priority

Use sources in this order.

1. Local shared context doc
- `inter-context.md` or `working-context.md`
- read first and treat as session baseline

2. Current repo code
- verify implementation state and detect context drift

3. Related repo code
- confirm cross-repo data flow, ownership, and compatibility

4. External source (optional)
- issue tracker, wiki, design/spec docs, runbooks, site URLs
- only when policy/source-of-truth recheck is needed

External sources are optional, not mandatory entry points.

## When To Use External Sources

Use external references only when needed, such as:
- rollout, payload, schema, or policy is defined externally
- latest decision may have changed since last session
- external document must be updated to stay authoritative
- upcoming planned job/module exists only in external docs

Skip external rereads when:
- local context already captures stable facts
- implementation does not depend on changing external policy

## Optional Source Integrations

Portability note:
- The core workflow of this skill is tool-agnostic.
- Source connectors are optional and environment-specific.

When external recheck is needed and a connector is available, it can be used as an optional source.
Do not make connector reads a mandatory first step for every session.

### Atlassian Integration (Optional)

Use this when Jira/Confluence references are in scope and freshness matters.

Codex MCP integration file:
`~/.codex/config.toml`

Example configuration snippet:

```toml
[mcp_servers.atlassian]
url = "https://mcp.atlassian.com/v1/mcp"
```

Usage rule:
- use Atlassian MCP when Jira/Confluence freshness matters
- skip it when local context already has stable confirmed facts

### Add Another Integration Later

For any new source connector, add a sibling subsection with:
- connector name
- configuration location
- minimal config snippet
- freshness/when-to-use rule

## Entry Contract

At session start, capture at least:
- `project root`
- `current repo`
- `current goal`

When provided, also capture:
- `related repos`
- `reference scope` (optional, free-text)
- `references in scope` (optional list)
- `shared context path` or `follow context path`

If a chain relationship is explicit (for example "ticket X and child tickets"), treat that as a required boundary.
If `current repo` is not explicit, do not assume from related-repo lists unless one candidate is unambiguous.

Invocation pattern guidance:
- If input says `related project like in <root>, <repo-a>, <repo-b>...`, treat `<root>` as `project root` and remaining tokens as `related repos`.
- If input says `follow-up ticket <KEY> and below tickets`, record `<KEY>` as parent reference and child scope as an explicit relationship in `reference relationships`.
- Do not collapse unresolved repo tokens into `current repo`; keep them in `open questions` until resolved.

## Session Startup Contract

At session start, provide at least:

```text
project root:
current repo:
current goal:
```

Recommended:

```text
project root:
current repo:
related repos:
shared context path:
confirmed facts:
current goal:
```

If following existing context:

```text
current repo:
follow context:
```

Reference-aware form:

```text
project root:
current repo:
related repos:
shared context path:
follow context:
reference scope:
references in scope:
reference relationships:
current goal:
```

## Required Context Fields

Maintain these fields in the shared context document.

1. `scope`
- `project root`
- `current repo`
- `related repos`
- `repo alias mapping` (if any)

2. `work identity`
- reference scope (optional)
- references in scope (optional list; each with type + identifier/link)
- reference relationships (optional)
- branch purpose
- current goal
- planned work not implemented yet (if reference-defined)

3. `confirmed facts`
- proven architecture or policy facts
- cross-repo explanation if provided
- role mapping (producer/consumer/scheduler/downstream)

4. `open questions`
- unresolved decisions
- uncertain assumptions
- explicit recheck points

5. `working targets`
- files/classes/modules to open first
- grouped by project
- include `planned targets` when code does not exist yet

6. `recent decisions`
- naming decisions
- query/schema/index decisions
- payload contract decisions

7. `next handoff note`
- concise starter context for the next session

8. `reference sync status`
- only when external references are in scope
- references checked this session
- what changed in external docs vs local context
- whether another reference recheck is required

## Context Placement Patterns

Use one of these patterns.

Pattern A. Root shared context
- `<project-root>/inter-context.md`
- best when multiple repos share one active workflow

Pattern B. Repo-owned context
- `<project-root>/<repo-name>/inter-context.md`
- best when one repo is the context owner

Pattern C. Hybrid
- root-level overview + repo-specific context files
- use only when A or B is insufficient

## Related Repo Resolution Under One Root

For each related repo name/path:
1. Resolve to an absolute path under `project root`.
2. If exact path is missing, allow a local alias only when unambiguous.
3. Record the alias mapping in context so future sessions do not drift.
4. If ambiguous, leave it as an open question; do not fabricate ownership.

Generic example:
- user token: `service-api`
- resolved path: `<project-root>/service-api` (or recorded alias mapping when naming differs)

Input can include mixed forms (absolute paths + short repo tokens).
Normalize both forms into one resolved repo list before deep exploration.

## Propagation Workflow

For inter-repo work, follow this flow.

1. Create/update context in owner location
2. Record confirmed facts and working targets
3. In next repo/session, read owner context first
4. Add new facts and decisions back to the same context
5. Keep one canonical context per workflow to avoid divergence

## Operating Procedure

Use this sequence unless repository-local rules are stronger:
1. confirm root/repo/goal and optional reference scope
2. read canonical shared context
3. create or update context draft and show it to the user
4. stop and wait for user confirmation to proceed with implementation work
5. after confirmation, open `working targets` first
6. verify current repo implementation state
7. verify related repos only when coupling exists
8. if references are declared and freshness matters, recheck external references only when needed
9. update shared context in the same session as code or policy changes
10. end with a short handoff note

### Mandatory Pause Gate

After context is created/read/updated, do not start code edits or execution immediately.

You must:
- present the synced context summary or file update status
- wait for explicit user confirmation (for example: "proceed", "go ahead")
- allow user to revise/add context before implementation starts

Detailed decision logic and failure diagnosis live in `references/method.md`.

## Stale Context Protocol

Treat context as synchronized state, not static notes.

Context is stale when any of these changes:
- query conditions
- payload fields
- message schema
- table/index/config shape
- module/class ownership
- inter-repo role boundaries

Protocol:
1. When code changes, update context in the same session
2. Mark obsolete assumptions clearly
3. Before next run, re-validate only high-risk assumptions

## Optional Reference Sync

If requested or required, sync context updates back to references.

Typical cases:
- payload/query/schema in reference docs is outdated
- policy page or spec doc lags behind implementation
- planned job/module sections need to stay aligned with code plan and docs

Recommended order:
1. code change
2. local context update
3. optional reference update

## Context Lifecycle

Treat context as lifecycle-managed notes.

At job completion, either approach is valid based on user preference and reuse value:
- ephemeral memo mode: remove or archive the context once the job is done
- durable document mode: keep and expand the context when it is likely to be reused

Practical rule:
- low reuse value -> close and remove
- high reuse value -> normalize and keep as a maintained document

## Guardrails

Do:
- keep one canonical context file per workflow
- prioritize working targets to reduce search time
- distinguish confirmed facts vs open questions
- include planned targets when implementation does not exist yet

Do not:
- start every session by reading external tools automatically
- re-scan all related repos without a concrete reason
- keep stale assumptions after code contract changes
- maintain multiple conflicting context files for the same workflow
- lose declared reference boundaries while syncing context

## Bundled Files

- Use [templates/inter-context.md](templates/inter-context.md) to initialize or reset a context file.
- Use [templates/session-kickoff.txt](templates/session-kickoff.txt) as a reusable session input block.
- Use [references/method.md](references/method.md) for detailed operating procedure and diagnostics.
- Use [references/checklist.md](references/checklist.md) for final quick validation.

## File Role Boundaries

- `SKILL.md`: trigger rules, scope model, source priority, context schema, and operating order.
- `references/method.md`: detailed execution logic, decision gates, and failure diagnosis.
- `references/checklist.md`: short final validation checklist.
- `templates/*`: initialization artifacts for context and session kickoff inputs.
