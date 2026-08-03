# Codex Model Binding Audit

## Purpose

Detect official Codex model-lifecycle changes that may make a named custom-agent binding stale, while preserving competence-first routing and requiring user approval before any replacement.

This audit discovers and reports drift. It does not edit model bindings, select a successor automatically, or activate its own schedule.

## Ownership And Inputs

- Canonical worker bindings: [custom-agents/](custom-agents/)
- Canonical audit binding: [profiles/model-binding-audit.config.toml](profiles/model-binding-audit.config.toml)
- Binding and fallback policy: [Competence-First Delegation](../../policies/harness/competence-first-delegation.md)
- Codex adapter lifecycle: [README.md](README.md#model-binding-lifecycle)
- Authoritative lifecycle sources:
  - [Codex models](https://learn.chatgpt.com/docs/models)
  - [Codex changelog](https://learn.chatgpt.com/docs/changelog)
  - [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) when custom-agent schema or precedence changes

The official sources determine public lifecycle claims. The canonical TOMLs determine current local intent. The runtime model picker and an explicit named-worker smoke test determine account-specific availability and actual execution; a documentation-only audit must not claim those as verified.

## CLI-First Execution

Use `codex exec` as the single implementation for both manual and weekly runs. Validate the exact command interactively in a terminal before attaching it to any scheduler.

Recommended execution properties:

- working root: the local `ai-assets` repository
- agent: the primary root agent only; do not delegate to a named worker or generic subagent
- model: use the explicitly bound lightweight model in the dedicated audit profile
- sandbox: `read-only`
- web access: enable native live search with the top-level `--search` option
- approval policy: `never`, so unattended runs fail instead of waiting for input
- persistence: `--ephemeral`, so weekly audits do not accumulate session rollouts
- configuration: `--strict-config`, so stale CLI configuration fails visibly
- mutation: do not edit files, symlinks, configuration, or runtime state
- fallback: if the profile model is unavailable, fail visibly and do not invoke another model

Run the audit manually from any terminal:

```sh
codex --search --sandbox read-only --ask-for-approval never \
  exec --profile model-binding-audit --ephemeral --strict-config --color never \
  --cd /Users/jungcho/Projects/ai-assets \
  'Run the read-only Codex model-binding audit defined in agents/adapters/codex/model-binding-audit.md. Use $openai-docs. You are already inside the audit invocation: do not run codex or codex exec recursively. Remain in the root agent and do not invoke subagents. Return only the audit status and output contract with the status value on the same line as Status:.'
```

The command intentionally prints the final answer to stdout and progress to stderr. This makes manual inspection, redirection, and later `launchd` logging straightforward.

The profile also disables subagents, so the model under audit runs as the root agent rather than indirectly through a worker binding.

## Installation And Operation

The canonical automation assets are:

- [scripts/run-model-binding-audit.sh](scripts/run-model-binding-audit.sh): executes the exact profile, captures reports, and records attention state
- [launchd/com.jungcho.codex-model-binding-audit.plist](launchd/com.jungcho.codex-model-binding-audit.plist): runs the canonical runner every Monday at 09:00 local time

On macOS, install the plist as a user LaunchAgent only after the manual command has produced a correct result.

- cadence: weekly; Monday at 09:00 local time is a reasonable default
- mechanism: `launchd` `StartCalendarInterval`
- executable: use the absolute Codex path because LaunchAgents have a minimal environment
- logs: keep stdout and stderr under `~/Library/Logs/codex-model-binding-audit/`
- command: reuse the manually validated `codex exec` contract with the same profile, sandbox, and base prompt; append only the deterministic manifest generated from canonical TOMLs
- installation boundary: do not install or load the LaunchAgent without explicit user approval

Prefer `launchd` to `crontab` on macOS. A calendar LaunchAgent runs after wake when the scheduled time was missed, whereas cron skips an invocation while the computer is asleep. `launchd` also gives the job an explicit label, arguments, environment, and log destinations.

For an approved installation:

1. Link `profiles/model-binding-audit.config.toml` into each approved Codex home as `model-binding-audit.config.toml`.
2. Run the canonical shell runner manually and inspect `latest-status.txt`, `latest-report.txt`, and `latest-stderr.log` under `~/Library/Logs/codex-model-binding-audit/`.
3. Validate the canonical plist with `plutil -lint`.
4. Link the plist into `~/Library/LaunchAgents/` and bootstrap it in the current GUI user domain.
5. Confirm `launchctl print gui/$(id -u)/com.jungcho.codex-model-binding-audit` shows the Monday schedule and canonical runner path.

The runner first uses the installed `openai-docs` manual helper to freshness-check and cache the current official Codex manual. When that succeeds, the model receives the verified manual and outline paths and uses targeted local reads before live-search gap filling. If preflight and required live sources are both unavailable, the audit must return `SOURCE_UNAVAILABLE`.

The runner also generates a deterministic binding manifest from the canonical TOMLs and passes it to the audit model. It compares the actual model reported by Codex with the profile's exact `model` value. A mismatch invalidates the audit instead of being treated as a substitute.

The runner never falls back to another model. It removes the attention sentinel only after a valid `NO_BINDING_CHANGE` result. `REVIEW_REQUIRED` leaves an attention sentinel for a competence-qualified primary agent to review; it does not automatically invoke that agent or change a binding.

## Audit Procedure

1. Treat the runner-generated binding manifest as exact local input. When running without the runner, read each canonical custom-agent TOML and the canonical audit-profile TOML separately rather than concatenating them. Record each stable role, exact model binding, reasoning effort, sandbox mode, and whether subagents are enabled.
2. Read the competence-first binding lifecycle and fallback rules.
3. Use the `openai-docs` workflow. Prefer the freshness-checked manual and outline paths supplied by the runner, then use current official search only for material gaps.
4. Look for:
   - explicit deprecation or retirement of a bound model
   - an explicit official replacement mapping
   - a new generation of the same special-purpose model line
   - changes to entitlement, separate usage limits, modality, tool support, or custom-agent compatibility
   - changes to custom-agent model precedence or configuration schema
5. Distinguish an explicit successor from a merely newer or similarly lightweight model. Similar speed, cost, or positioning is not lineage or capability equivalence.
   - `REVIEW_REQUIRED` requires evidence tied to an exact bound model or its explicitly named special-purpose lineage.
   - Deprecation of a sibling, ancestor, adjacent general model, or unrelated older family is not a trigger for the bound model.
   - A newer recommended baseline, lower catalog priority, age, or general replacement posture is not a plausible successor relationship.
   - Mark a successor `plausible` only when an official name or announcement preserves the bound model's special-purpose lineage or explicitly describes succession without giving a final replacement mapping.
6. Do not invoke a candidate model, named worker, generic subagent, or any other delegated agent during the audit.
7. Do not invoke `codex`, `codex exec`, or the shell runner recursively; the current root session is already the audit execution.
8. Do not edit a TOML, alter a symlink, or modify `AGENTS.md` during the audit.
9. Report one status using the output contract below.

## Status Contract

- `NO_BINDING_CHANGE`: official evidence shows no lifecycle change relevant to current bindings.
- `REVIEW_REQUIRED`: official evidence identifies a deprecation, retirement, explicit successor, materially changed entitlement, or plausible same-line generation requiring human review.
- `SOURCE_UNAVAILABLE`: one or more required official sources could not be checked; do not infer that bindings are current.

`REVIEW_REQUIRED` is not replacement approval. It starts the controlled migration workflow.

If no exact-binding or explicitly preserved-lineage trigger exists, return `NO_BINDING_CHANGE` even when adjacent model families have newer recommendations, deprecations, or replacements.

The shell runner may emit these operational statuses when no valid audit result exists:

- `AUDIT_MODEL_UNAVAILABLE`: the explicitly bound audit model could not run; no substitute was attempted.
- `AUDIT_MODEL_MISMATCH`: the actual runtime model differed from the explicit audit-profile binding; the audit result was rejected.
- `AUDIT_RUN_FAILED`: Codex or the local runner failed for another reason; no substitute was attempted.
- `INVALID_AUDIT_OUTPUT`: the model completed without returning one of the three audit statuses.

## Output Contract

```text
Status: NO_BINDING_CHANGE | REVIEW_REQUIRED | SOURCE_UNAVAILABLE
Checked at:
Canonical bindings checked:
Official sources checked:
Relevant official changes:
Exact binding trigger evidence: <direct source and exact relationship, or none>
Successor relationship: explicit | plausible | none | unknown
Usage-limit continuity: confirmed | changed | unknown
Capability or configuration differences:
Account/runtime verification still required:
Recommended next action:
```

For `NO_BINDING_CHANGE`, keep the report brief. For `REVIEW_REQUIRED` or `SOURCE_UNAVAILABLE`, include direct official links and separate documented facts from inference.

## CLI Audit Prompt

The manual command above points the root agent to this document. Use the following expanded prompt when testing or debugging the contract directly:

```text
Run the Codex custom-agent model-binding audit in read-only mode.

Use the openai-docs skill and follow:
agents/adapters/codex/model-binding-audit.md

Remain in the primary root agent. Do not invoke any named worker, generic subagent,
candidate model, or other delegated agent; the bindings under audit may be stale.
You are already running inside the audit invocation. Do not run `codex`, `codex exec`,
or the audit shell runner recursively.

Read the canonical bindings under:
agents/adapters/codex/custom-agents/*.toml
agents/adapters/codex/profiles/model-binding-audit.config.toml

When the runner supplies a canonical binding manifest, treat its file paths and exact
TOML fields as authoritative local input. Otherwise, read each TOML separately and do
not infer a missing field from concatenated output.

Check only current official OpenAI Codex sources, including the Codex Models page,
Codex changelog, and Subagents documentation when configuration behavior is relevant.

Determine whether any bound model has been deprecated, retired, explicitly replaced,
given a same-line successor, or changed in entitlement, separate usage limits,
capability, modality, or custom-agent compatibility.

Do not treat a merely newer, faster, cheaper, or similarly lightweight model as a successor.
Deprecation or replacement of a sibling, ancestor, adjacent general model, or unrelated
older family is not evidence about the exact bound model. Model age, catalog priority,
or a newer recommended baseline is also not a review trigger.
Use `plausible` only when official naming or text preserves the same special-purpose
lineage or explicitly describes succession. Otherwise use `none`.
Do not recommend a generic newer model family when no explicit or plausible same-line
successor exists; keep the current binding unless a separate competence review is approved.
Do not edit any file, symlink, AGENTS.md, TOML, configuration, or schedule.
Do not invoke candidate models or silently substitute a binding.

Return exactly one audit status and the output fields defined in the audit document.
Write the status value on the same line as `Status:`.
If official sources are unavailable, return SOURCE_UNAVAILABLE rather than relying on memory.
```

## Controlled Migration After An Alert

After the user approves review of a candidate:

1. Confirm the candidate is available to the user's account through the model picker or another documented account-specific surface.
2. Compare the candidate with the worker role's competence floor and special usage semantics.
3. Change only the affected canonical TOML `model` value.
4. Confirm both Codex homes still resolve the canonical TOML through their existing symlinks.
5. Start a fresh session.
6. Explicitly invoke the named worker and verify the actual model, permissions, behavior, and expected usage accounting.
7. If any check fails, restore or replace the binding only through another reviewed decision; never fall back silently.

When the affected binding is the audit profile itself, run the profile directly instead of invoking a named worker, then confirm its root-agent model and disabled-subagent behavior before reloading the weekly schedule.
