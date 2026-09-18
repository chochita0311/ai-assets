# Codex Runtime Adapter

## Purpose
- Adapt the shared competence-first delegation policy to a personal Codex runtime.
- Keep stable role names separate from replaceable model bindings.
- Provide installable custom-agent files and a model-neutral managed section for the global Codex `AGENTS.md`.
- Provide reusable personal guidance and generic environment and machine templates for agent-led import.
- Provide an optional operator-context recognition hook without moving repo-local continuity policy into the personal runtime.
- Provide a root-only, read-only lifecycle audit and a terminal-native weekly runner without making the audit a source of replacement authority.

## Ownership
- [Competence-First Delegation](../../policies/harness/competence-first-delegation.md) owns the platform-neutral policy.
- [Operator Briefing And Review Receipts](../../policies/harness/operator-briefing-and-review-receipts.md) owns detailed continuity triggers, output semantics, and non-interference rules.
- [Operator Briefing Template](../../templates/operator-briefing.md) owns the non-persistent response scaffold.
- [custom-agents/](custom-agents/) owns the canonical Codex custom-agent files and their concrete model bindings.
- [profiles/](profiles/) owns canonical non-interactive root-agent profiles and their concrete model bindings.
- [global-agents-managed-section.md](global-agents-managed-section.md) owns the installable, model-neutral entrance-policy blocks; it recognizes operator-context triggers but does not own or install the detailed policy.
- [Personal Codex Instructions](instructions/README.md) is the reference library and import guide for common, environment-specific, and PC-specific guidance. Its personal preferences are distinct from the shared harness entrance blocks.
- [model-binding-audit.md](model-binding-audit.md) owns the read-only, CLI-first model-lifecycle audit contract.
- [run-model-binding-audit.sh](scripts/run-model-binding-audit.sh) owns the canonical terminal runner. [The LaunchAgent template](launchd/model-binding-audit.template.plist) and [its renderer](scripts/render-model-binding-launchagent.py) define portable schedule behavior; generated machine-local plists own only installation paths and approved local settings.
- Shared adapter blocks and linked bindings under a Codex home are installed views of these sources. Actual personal, environment, and machine settings remain in the destination `AGENTS.md`.

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
├── instructions/
│   ├── README.md
│   ├── general.md
│   ├── environment.template.md
│   └── machine.template.md
├── custom-agents/
│   ├── evidence_scout.toml
│   └── bounded_verifier.toml
├── profiles/
│   └── model-binding-audit.config.toml
├── scripts/
│   ├── run-model-binding-audit.sh
│   └── render-model-binding-launchagent.py
└── launchd/
    └── model-binding-audit.template.plist
```

## Source-To-Target Mapping

| Canonical source | Runtime target |
|---|---|
| `global-agents-managed-section.md` | managed block inside `<codex-home>/AGENTS.md` |
| applicable guidance from `instructions/` | selected rules merged into the destination `AGENTS.md` after comparison |
| `custom-agents/evidence_scout.toml` | per-file symlink at `<codex-home>/agents/evidence_scout.toml` |
| `custom-agents/bounded_verifier.toml` | per-file symlink at `<codex-home>/agents/bounded_verifier.toml` |
| `profiles/model-binding-audit.config.toml` | per-file symlink at `<codex-home>/model-binding-audit.config.toml` |
| `scripts/run-model-binding-audit.sh` | executed in place by the installed LaunchAgent |
| `launchd/model-binding-audit.template.plist` | rendered machine-local file at `~/Library/LaunchAgents/<approved-label>.plist` after approval; never a symlink to the template |

Preserve unrelated personal content in the global `AGENTS.md` and `config.toml`. Merge shared adapter policy only through its marked regions; use the [personal instruction import guide](instructions/README.md) for other applicable guidance. Link each named TOML separately instead of linking the entire `agents/` directory so the runtime home can still own unrelated local agents.

The audit runner executes from its canonical path under `scripts/`; it is not copied into a runtime home.

Existing installations that link an old machine-specific plist require a separately approved local-file migration before that source is retired. Preserve the installed label, schedule, model binding, and paths unless their change is also approved; see [Installation And Operation](model-binding-audit.md#installation-and-operation).

This mapping installs personal runtime assets only. It does not export the shared operator policy or template into a consuming repo. Follow [Agent System Adoption Guide](../../ADOPTION-GUIDE.md) for that repository-local installation.

## Model Binding Lifecycle

The `model` value in each custom-agent or root-profile TOML is the sole canonical binding for that role. The global `AGENTS.md` section intentionally contains no concrete model names or binding table; it routes by stable worker role and competence constraints instead.

Codex loads the standalone custom-agent TOMLs, identifies each agent by its `name`, and uses its `description` as guidance for when to use it. Therefore, a model-name table in `AGENTS.md` is not required for worker discovery or role-based routing.

When a named worker has a different binding from the primary agent, invoke it with no inherited history or the smallest bounded recent-turn fork. A full-history fork inherits primary-thread behavior and can invalidate the custom binding before the worker starts.

Use [Controlled Migration After An Alert](model-binding-audit.md#controlled-migration-after-an-alert) as the single replacement procedure. Candidate evaluation, replacement approval, and post-install verification are distinct steps; approval to review a candidate does not authorize changing a live binding.

No `AGENTS.md` regeneration or merge is required for a model-only change. Update the managed section only when the durable routing policy itself changes.

Treat any of the following as a binding-review trigger:

- official deprecation, retirement, or availability changes
- a named invocation returning unavailable or selecting a different actual model
- a new model generation that plausibly fits the worker's narrow role
- observed quality falling below the role's competence floor

A trigger starts evaluation; it does not authorize automatic substitution. Keep the existing binding until the candidate passes the role-specific smoke test and the user approves replacement, then follow the canonical procedure.

Use [model-binding-audit.md](model-binding-audit.md) for the CLI-first weekly detection workflow. The audit reports candidate drift; it never edits a TOML or treats a similarly positioned lightweight model as an automatic successor.

## Installation Boundary

This package does not install itself automatically. Installation changes personal runtime state and should occur only after explicit approval.

For an approved installation:

1. Merge only the approved marked blocks from the managed section into each distinct target `AGENTS.md`. Treat the competence-routing and operator-context blocks as independent managed regions. For personal guidance, compare the destination with [Personal Codex Instructions](instructions/README.md) and import the applicable rules. If one Codex home's `AGENTS.md` is already a symlink to another, update the resolved owner only once.
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

## Operator Context Continuity

The managed AGENTS fragment includes a low-noise operator-context recognition hook. It lets imported Codex agents notice relevant ordinary-language triggers without requiring a skill command.

The hook is supported only when the current consuming repo exposes [Operator Briefing And Review Receipts](../../policies/harness/operator-briefing-and-review-receipts.md). Target activation or resumption produces a Work Briefing only when prior context materially affects understanding or execution. If the policy is unavailable or no meaningful delta exists, the hook preserves the normal response without creating a substitute artifact.

Install the detailed policy and template through the repository-local [Agent System Adoption Guide](../../ADOPTION-GUIDE.md), not under `~/.codex/`. The personal adapter remains an entrance-level recognition layer and never becomes a second source of continuity truth.
