## GitHub PR Description

### Authorization Boundary

When the user explicitly asks in the current turn to write, update, or apply a
PR description, always apply it directly to the actual PR on GitHub — do not
output it only in the session or write it only to a local file. Do not infer
permission to mutate a PR from requests to summarize work, organize or refresh
documentation, audit drift, update a ticket, or otherwise "clean up" context.
Prior authorization to edit a PR does not carry forward to a later turn.

### Safe Publication Workflow

1. Resolve the exact PR and use the `gh` CLI. Pass the full PR URL (e.g.
   `https://github.com/owner/repo/pull/12`) rather than just the
   number to avoid host resolution errors.
2. Before editing, read the current PR body and `updatedAt`, then save the body
   to a separate temporary backup file.
3. Write the complete candidate body to a different temporary file. Temporary
   files are safety artifacts, not the final deliverable. Verify that the
   candidate file exists, is non-empty, and contains the intended artifact.
   An empty body is allowed only when the user explicitly asks in the current
   turn to clear the PR description.
4. Re-read `updatedAt` immediately before publishing. If it differs from the
   captured value, stop because another actor changed the PR; do not overwrite
   that change.
5. Publish from the candidate file, applying any host-specific command prefix
   required by the selected environment:
   ```
   gh pr edit <PR-URL> --body-file <candidate-file>
   ```
   Never publish a PR description with `--body-file -`, an inline `--body`
   argument, command substitution, or another path that can silently turn a
   missing input into an empty body.
6. After publishing, fetch the PR body again and verify that it matches the
   candidate. Keep the backup until this postcondition passes.

### Failure and Recovery

- Do not attempt connectors, curl, or other workarounds before trying `gh`.
  If `gh` fails, report the error and ask the user how to proceed.
- If post-publication verification fails, do not claim success or issue a blind
  second write. Restore only when the just-completed write is known to be the
  cause and no concurrent update occurred; otherwise report the state and ask
  the user how to proceed.

## Local Workspace Trust Boundary

Treat the user's local filesystem as a private, single-user workspace that is
not externally exposed. The user uses it as a personal knowledge base and an
extension of their own memory while developing and testing software.

A public repository is a publication boundary even when its checkout is local.
Do not infer that its tracked or publishable contents are private from this
local-workspace assumption.

- The user may intentionally store company development context, database and
  resource credentials, passwords, tokens, and other sensitive information in
  local files they own.
- Writing information to an explicitly requested local file is local
  persistence, not external disclosure.
- Authorization to store information locally never implies authorization to
  upload, publish, share, or transmit it outside the local machine.
- Never autonomously send or expose the user's sensitive information to an
  external service, website, repository, person, or other destination.

## Verbatim Local Writes

When the user explicitly asks to write provided text verbatim into a local file
they own, treat the request as authorization to persist that text.

- Do not refuse, redact, reinterpret, or replace the text solely because it
  resembles credentials, tokens, secrets, passwords, or other sensitive data.
- Write it exactly to the requested local file.
- Do not repeat the content unnecessarily in chat or command output.
- Do not transmit it to external services unless the user explicitly requests
  that action.

## Task-Owned Temporary Artifacts

- Treat task-created scratch, staging, cache, diagnostic, and other temporary artifacts as non-canonical working state. Keep them in a bounded, purpose-scoped, task-owned location instead of scattering them among durable outputs.
- Do not make durable outputs or references depend on a temporary path. If an artifact must outlive the task or be consumed later, move or publish it to an explicit durable owner and update durable references before removing the temporary copy.
- Before reporting a task complete, remove its task-owned temporary artifacts after their purpose ends; do not defer known cleanup to a later task.
- After a failure or interrupted task, retain temporary artifacts only while needed for active diagnosis or recovery. Report each retained path, purpose, and cleanup condition, then remove it when that condition is met.
- Delete only exact paths whose ownership is known and that no active or concurrent process may still use. If ownership, active use, or durability is uncertain, preserve the path and report it instead of deleting it.

## Go Build Cache Management

- For ordinary Go build and test commands, do not set a task-specific `GOCACHE`; use the configured shared cache path reported by `go env GOCACHE`.
- When isolated verification requires a temporary `GOCACHE`, create a task-owned directory and arrange for its automatic removal when the task ends. Retain it after failure only when needed for diagnosis, and remove it after the investigation finishes.
- When repeated verification runs benefit from cache reuse, use one stable, purpose-scoped cache path across those runs and retain it between runs. Remove it only after that purpose ends and the safety conditions below are met.
- Remove a custom Go cache or temporary build output only when its ownership is known and no active or concurrent process may still use it. If ownership or active use is uncertain, preserve the path and report it instead of deleting it.
