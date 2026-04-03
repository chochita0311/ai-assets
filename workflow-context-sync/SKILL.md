---
name: workflow-context-sync
description: Reconcile and maintain one canonical working context across repositories, tickets, docs, and runtime signals before downstream implementation. Use when work spans multiple sources (for example Jira, Confluence, multi-repo codebases, runbooks, or server observations), when source-of-truth conflicts must be resolved, or when cross-session drift causes repeated re-discovery.
---

# Workflow Context Sync

Use this skill to integrate multi-source workflow context into one canonical state and keep it synchronized across sessions.
Treat this skill as a context reconciliation and maintenance layer, not an implementation shortcut.

## Core Outcome

Produce and maintain:
- one canonical context file per active workflow
- explicit source inventory, role classification, and source-of-truth rules
- explicit reconciliation results (aligned, conflict, open)
- low-drift handoff context that allows the next session to start immediately

## Scope Model

Always model context at these levels:
- `workflow root`: local workspace boundary for the workflow
- `current repo`: actively edited repo for this session
- `related repos`: coupled repos that affect current decisions
- `external sources` (optional): tickets, docs/wiki/specs, runbooks, runtime signals

## Source Inventory Contract

Record every in-scope source in the canonical context.
For each source, capture:
- source id
- source type (`repo`, `ticket`, `doc`, `runtime`, `runbook`, `other`)
- location or identifier
- role
- freshness state
- owner or update path (if known)

Do not treat all sources as equal.

## Source Role Classification

Assign one role per source (or multiple if explicitly needed):
- `implementation truth`: current code behavior
- `authoritative spec`: approved policy/spec contract
- `planned work`: future intent and task tracking
- `operational signal`: observed runtime reality
- `historical note`: prior decisions or legacy context

If source role is unclear, keep it in `open questions`.

## Source-of-Truth Rules

Define explicit priority rules in context.
Default interpretation order:
1. runtime facts for current observed behavior
2. current repo code for implementation truth
3. approved specs/policies for intended contract
4. ticket planning fields for future intent
5. historical notes for background only

If project policy uses another order, record the override explicitly.

## Reconciliation Contract

For every important claim (payload, schema, ownership, rollout, policy), capture:
- which source says what
- status (`aligned`, `conflict`, `open`)
- working assumption for this session
- follow-up update target (code, ticket, doc, runbook)

This reconciliation output is the primary artifact.

## Operating Procedure

Use this sequence unless repo-local policy is stricter:
1. normalize intake (`workflow root`, `current repo`, `goal`, optional sources)
2. resolve canonical context path
3. read canonical context before deep scanning
4. refresh only the minimum sources required for this decision
5. write/update source inventory, role map, and reconciliation notes
6. present a concise context summary (including conflicts and deltas)
7. enforce reconciliation approval gate before implementation work
8. after approval, do downstream work using `working targets`
9. update context in the same session when facts or decisions change
10. end with a next-session handoff note

### Reconciliation Approval Gate

Do not start code edits, refactors, or execution workflows before user review.

Gate behavior:
- default mode: `strict`
- optional modes: `optional`, `skip` (only when user explicitly requests in current session)

Before the gate, always show:
- what context changed (summary or diff)
- current conflicts/mismatches
- open questions and working assumptions

Valid proceed signals:
- `proceed`
- `go ahead`
- `apply changes`
- `start implementation`

If no valid signal is given, keep `user review status` as `pending` and continue only context-sync operations.

## Entry Contract

At session start, capture at least:
- `workflow root`
- `current repo` (or unresolved with explicit resolution plan)
- `current goal`

When available, also capture:
- `related repos`
- `shared context path` or `follow context`
- `sources in scope`
- `source relationships` (for example parent ticket and child tickets)
- `initial known facts`

## Required Context Fields

Maintain these fields in the canonical context file:
1. `scope`
- workflow root
- current repo
- related repos
- repo alias mapping

2. `workflow identity`
- workflow name
- branch purpose
- current goal
- user review status (`pending|confirmed`)
- approval mode (`strict|optional|skip`)

3. `source inventory`
- source id, type, location, role, freshness, owner

4. `source relationships`
- parent/child, dependency, upstream/downstream links between sources

5. `source-of-truth rules`
- priority interpretation rules used for this workflow

6. `reconciliation notes`
- claim-by-claim alignment/conflict/open status
- working assumptions
- follow-up targets

7. `confirmed facts`
- facts that are currently validated

8. `open questions`
- unresolved ambiguity, missing ownership, unknown freshness

9. `drift watchlist`
- assumptions likely to go stale

10. `working targets`
- files/modules/jobs to inspect first (current + related repos)

11. `recent decisions`
- decisions made this session

12. `source sync status`
- sources checked this session
- source deltas vs canonical context
- external recheck needed flag

13. `next handoff note`
- concise restart point for next session

## Context Placement Patterns

Use one pattern per workflow:
- Pattern A: `<workflow-root>/inter-context.md` for shared multi-repo workflows
- Pattern B: `<workflow-root>/<repo>/inter-context.md` when one repo owns context
- Pattern C: hybrid (root summary + repo detail files) only when required

Avoid parallel canonical files for the same workflow.

## Optional Source Integrations

Keep integrations optional and environment-specific.
Use only when freshness is required for in-scope sources.

### Atlassian Integration (Optional)

Use when Jira/Confluence sources are in scope and need freshness checks.

Codex MCP integration file:
`~/.codex/config.toml`

Example:

```toml
[mcp_servers.atlassian]
url = "https://mcp.atlassian.com/v1/mcp"
```

Use Atlassian reads selectively, not as mandatory first step.

## Drift Maintenance Lifecycle

Maintain context as lifecycle state:
1. capture baseline
2. detect drift
3. reconcile conflicts
4. record deltas and assumptions
5. hand off with restart-ready note

## Guardrails

Do:
- keep one canonical context per workflow
- separate confirmed facts from assumptions
- treat source roles and priority rules as first-class data
- require review before downstream implementation

Do not:
- auto-read every external source each session
- begin implementation before reconciliation approval
- mix plan data and implementation truth without role labels
- keep stale assumptions after contract/schema changes

## Bundled Files

- Use [templates/inter-context.md](templates/inter-context.md) to initialize or reset canonical workflow context.
- Use [templates/session-kickoff.txt](templates/session-kickoff.txt) as reusable intake input.
- Use [references/method.md](references/method.md) for execution details and diagnostics.
- Use [references/checklist.md](references/checklist.md) for final validation.

## File Role Boundaries

- `SKILL.md`: trigger scope, source model, reconciliation policy, operating order.
- `references/method.md`: detailed step logic and failure diagnosis.
- `references/checklist.md`: compact completion checklist.
- `templates/*`: reusable kickoff and context artifacts.
