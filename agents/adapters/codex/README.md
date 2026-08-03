# Codex Runtime Adapter

## Purpose
- Adapt the shared competence-first delegation policy to a personal Codex runtime.
- Keep stable role names separate from replaceable model bindings.
- Provide installable custom-agent files and a model-neutral managed section for the global Codex `AGENTS.md`.
- Provide a root-only, read-only lifecycle audit and a terminal-native weekly runner without making the audit a source of replacement authority.

## Ownership
- [Competence-First Delegation](../../policies/harness/competence-first-delegation.md) owns the platform-neutral policy.
- [custom-agents/](custom-agents/) owns the canonical Codex custom-agent files and their concrete model bindings.
- [profiles/](profiles/) owns canonical non-interactive root-agent profiles and their concrete model bindings.
- [global-agents-managed-section.md](global-agents-managed-section.md) owns the installable, model-neutral entrance-policy section.
- [model-binding-audit.md](model-binding-audit.md) owns the read-only, CLI-first model-lifecycle audit contract.
- [run-model-binding-audit.sh](scripts/run-model-binding-audit.sh) and [the LaunchAgent plist](launchd/com.jungcho.codex-model-binding-audit.plist) own the canonical terminal runner and macOS schedule definition. Installed runtime links do not become parallel sources of truth.
- A target under `~/.codex/` or another explicitly selected Codex home is an installed runtime view, not a parallel source of truth.

## Official Codex References
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): custom-agent locations, required fields, model precedence, sandbox overrides, and delegation behavior
- [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md): global and project instruction discovery
- [Models](https://learn.chatgpt.com/docs/models): recommended models, special-purpose models, and deprecation guidance
- [Codex changelog](https://learn.chatgpt.com/docs/changelog): model launches and lifecycle announcements
- [Profiles](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles): standalone `$CODEX_HOME/<name>.config.toml` layers selected with `--profile`
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode): `codex exec` usage for scripts and scheduled jobs

Recheck these references before adopting a future configuration-format change; custom-agent authoring may evolve independently from this adapter.

## Package Shape

```text
agents/adapters/codex/
├── README.md
├── global-agents-managed-section.md
├── model-binding-audit.md
├── custom-agents/
│   ├── evidence_scout.toml
│   └── bounded_verifier.toml
├── profiles/
│   └── model-binding-audit.config.toml
├── scripts/
│   └── run-model-binding-audit.sh
└── launchd/
    └── com.jungcho.codex-model-binding-audit.plist
```

## Source-To-Target Mapping

| Canonical source | Runtime target |
|---|---|
| `global-agents-managed-section.md` | managed block inside `<codex-home>/AGENTS.md` |
| `custom-agents/evidence_scout.toml` | per-file symlink at `<codex-home>/agents/evidence_scout.toml` |
| `custom-agents/bounded_verifier.toml` | per-file symlink at `<codex-home>/agents/bounded_verifier.toml` |
| `profiles/model-binding-audit.config.toml` | per-file symlink at `<codex-home>/model-binding-audit.config.toml` |
| `scripts/run-model-binding-audit.sh` | executed in place by the installed LaunchAgent |
| `launchd/com.jungcho.codex-model-binding-audit.plist` | symlink at `~/Library/LaunchAgents/com.jungcho.codex-model-binding-audit.plist` after approval |

Do not replace the whole global `AGENTS.md` or `config.toml`; they may own unrelated personal settings. Merge only the marked managed section. Link each named TOML separately instead of linking the entire `agents/` directory so the runtime home can still own unrelated local agents.

The audit runner executes from its canonical path under `scripts/`; it is not copied into a runtime home.

## Model Binding Lifecycle

The `model` value in each custom-agent or root-profile TOML is the sole canonical binding for that role. The global `AGENTS.md` section intentionally contains no concrete model names or binding table; it routes by stable worker role and competence constraints instead.

Codex loads the standalone custom-agent TOMLs, identifies each agent by its `name`, and uses its `description` as guidance for when to use it. Therefore, a model-name table in `AGENTS.md` is not required for worker discovery or role-based routing.

When a named worker has a different binding from the primary agent, invoke it with no inherited history or the smallest bounded recent-turn fork. A full-history fork inherits primary-thread behavior and can invalidate the custom binding before the worker starts.

To replace a model generation:

1. Change only the `model` value in the affected canonical TOML.
2. Confirm each runtime symlink still resolves to that TOML.
3. Start a fresh Codex session when runtime configuration may be cached.
4. Explicitly invoke the named worker or root profile once and verify the actual model and permissions.

No `AGENTS.md` regeneration or merge is required for a model-only change. Update the managed section only when the durable routing policy itself changes.

Treat any of the following as a binding-review trigger:

- official deprecation, retirement, or availability changes
- a named invocation returning unavailable or selecting a different actual model
- a new model generation that plausibly fits the worker's narrow role
- observed quality falling below the role's competence floor

A trigger starts evaluation; it does not authorize automatic substitution. Keep the existing binding until the candidate passes the role-specific smoke test, then update only the affected TOML.

Use [model-binding-audit.md](model-binding-audit.md) for the CLI-first weekly detection workflow. The audit reports candidate drift; it never edits a TOML or treats a similarly positioned lightweight model as an automatic successor.

## Installation Boundary

This package does not install itself automatically. Installation changes personal runtime state and should occur only after explicit approval.

For an approved installation:

1. Merge the content between the managed section's markers into each distinct target `AGENTS.md`. If one Codex home's `AGENTS.md` is already a symlink to another, update the resolved owner only once.
2. Create the target `agents/` directory when absent.
3. Create one symlink per named TOML from the target `agents/` directory to the canonical file under this adapter.
4. Create one profile symlink from each approved Codex home to the canonical audit profile.
5. Verify every link resolves to the intended canonical file. Do not replace a pre-existing file or link without reconciling its ownership first.
6. Leave unrelated global instructions and configuration untouched.
7. Start a fresh Codex session.
8. Explicitly invoke each named worker and root profile once and verify its actual model and sandbox behavior.
9. Test one positive auto-routing case and one case that must stay with the primary agent.

Install the weekly LaunchAgent separately and only after the manual audit succeeds. Follow [model-binding-audit.md](model-binding-audit.md#installation-and-operation) for validation, installation, status, and failure handling.

## Audit Profile

`model-binding-audit` is a dedicated non-interactive root profile, not a worker. It is read-only, disables subagents, and binds one reviewed lightweight model for official lifecycle detection. The runner preflights the current official Codex manual through `openai-docs`, rejects unavailable or mismatched execution instead of falling back, and returns any `REVIEW_REQUIRED` result to a competence-qualified primary agent for the replacement decision.

## Initial Worker Set

### `evidence_scout`
- bounded read-only multi-file exploration
- file, symbol, execution-path, existing-test, and branch-impact evidence
- no architecture, source-of-truth, persistence, or implementation decisions

### `bounded_verifier`
- exact test, lint, diff, and log-classification commands
- no source edits or independent fixes
- separates primary failures from cascading failures and reports evidence gaps

Do not add an automatically invoked code-writing worker until real runs show that its task class is consistently bounded, reversible, and cheaper to review than direct primary-agent work.

## Routing Validation Cases

| Case | Expected route |
|---|---|
| One immediately needed targeted search or test | primary agent |
| Multi-directory usage and call-path inventory | `evidence_scout` |
| Broad branch diff evidence with file and symbol citations | `evidence_scout` |
| Several exact test commands plus failure clustering | `bounded_verifier` |
| Requirement, architecture, security, persistence, or final review | primary agent |
| Optional worker unavailable | primary agent, without generic substitution |
| Explicitly requested worker unavailable | `REQUESTED_WORKER_UNAVAILABLE` |

## Future Extensions
- Add an optional Codex config fragment only when a shared concurrency or hook rule has been proven necessary.
- Add a sync script only after merge behavior for pre-existing personal files is explicitly specified and tested.
- Keep role contracts stable when replacing model generations.
