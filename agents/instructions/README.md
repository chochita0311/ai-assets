# Shared Local AI Instructions

Use this directory for shared instruction delivery and for agent-led review and
import of personal guidance into a local AI runtime's global instruction file.
The managed bundle is common to local AI runtimes. Each runtime adapter owns its
actual discovery paths, loading behavior, and installation procedure.

## What To Reuse

| Reference | Scope |
|---|---|
| [general.md](general.md) | Common personal preferences: PR descriptions, local writes, temporary artifacts, and Go caches |
| [environment.template.md](environment.template.md) | Optional rules for a company or other environment: hosts, connectors, and GitHub Enterprise commands |
| [machine.template.md](machine.template.md) | PC-specific path aliases and examples |
| [standard.md](standard.md) | Generated common instructions: meaning-preserving response defaults, code quality guidance, delegation, and conditional context continuity |

The personal references and templates illustrate what to consider; use only the
parts relevant to the destination. Actual company values and local paths belong
in the destination's global instructions. This public repository keeps generic
placeholders and examples. In `general.md`, temporary-artifact rules and Go
cache rules remain selectable operating guidance. Reconcile the destination's
temporary-artifact policy before importing those rules, and select Go-cache
guidance for environments that use Go.

## Generated Shared Instructions

The policy documents own the editable rules. The generated bundle packages
their marked runtime sections without rewriting their text:

| Managed region | Policy source |
|---|---|
| `response-clarity` | [Response Clarity And Meaning Preservation](../policies/baseline/response-clarity.md#runtime-instructions) |
| `code-quality` | [Code Quality](../policies/baseline/code-quality.md#decision-rules) |
| `competence-routing` | [Competence-First Delegation](../policies/harness/competence-first-delegation.md#runtime-instructions) |
| `operator-context-continuity` | [Operator Briefing And Review Receipts](../policies/harness/operator-briefing-and-review-receipts.md#runtime-recognition-instructions) |

Edit the owning policy's marked rules, keep its detailed guidance consistent,
then run these commands from the repository root:

```sh
python3 scripts/render_global_agent_instructions.py
python3 scripts/render_global_agent_instructions.py --check
```

The [renderer](../../scripts/render_global_agent_instructions.py) rejects missing,
duplicate, reversed, empty, or nested source regions. `--check` reports a missing
or stale bundle without changing files. Do not edit the bundle directly. Sources,
review examples, rationale, and evaluation material outside the marked rules
remain in their policy owners.

Generation updates only this repository's bundle. Runtime installation is a
separate, authorized merge that preserves existing local instructions and
values. Installed copies do not synchronize automatically. Use the
[Codex adapter](../adapters/codex/README.md#baseline-installation) for Codex; a
different runtime needs its own verified discovery and installation procedure.
Sharing `AGENTS.md` content does not imply that runtimes discover the same
global file or use the same model, tool, or permission settings.

The four regions remain independently installable. The continuity region is
only a recognition hook when the consuming repo exposes its detailed policy.
Install repository-local continuity policy and templates through the
[adoption guide](../ADOPTION-GUIDE.md); generating or installing the global
bundle does not export a harness or implicitly install the global baselines
when a harness is exported.

## Response Clarity

The `response-clarity` block applies the [shared response policy](../policies/baseline/response-clarity.md) without a skill command or repository-local dependency. Its first priority is preserving substantive meaning; readability changes must not remove conditions, evidence, alternatives, uncertainty, or necessary explanations. Sources and review examples remain in the shared policy rather than expanding every runtime's instruction load.

For substantive source synthesis, the installed block keeps the [source-first preservation pass](../policies/baseline/response-clarity.md#claim-review-and-clarification) self-contained: inventory complete claims, resolve scope, preserve each subject and condition, draft and reread, then compare actual final passages with their sources. The block also requires a readability check after preservation and another preservation check after editing. Working records stay in task-owned private scratch with local file tools; simple answers do not require them. Keep records through verification and any active evaluation or recovery, then remove them.

The shared policy owns the detailed method and [evaluation criteria](../policies/baseline/response-clarity.md#validation-and-evidence-limits); runtime adapters own installation. The review is executed by the agent. It is not an enforced runtime interception or a guarantee that every omission is detected.

No worker, model, profile, runtime hook, or external summarizer is required. The mandatory rules are in the installed block itself; following a link or reading this checkout is not needed before each answer. The runtime adapter is the installation mechanism, not a separate post-processing stage.

The response baseline and operator-context recognition block can coexist. Keep the continuity block's trigger and repetition rules: it owns when an additional briefing is useful, while the response block governs how the resulting answer preserves meaning. A repository with only the harness retains its existing continuity and evidence contracts; installing the global baseline is separate and is not part of harness export or refresh.

## Code Quality

The `code-quality` block applies the [shared code quality policy](../policies/baseline/code-quality.md) to code work across sessions. Its complete decision rules are in the installed block; using them requires no skill invocation, repository harness, or access to this checkout.

Project rules, contracts, actual versions, and existing quality tools determine implementation choices. The block guides simplicity, scoped legacy improvements, version-aware official documentation, and honest verification. Maintain language and tool specifics in their owning projects and official sources. Runtime adapters install the instructions into their effective global instruction files; the bundle adds no runtime hook or automatic lint or test runner.

Use the runtime installation procedure, such as [Codex Baseline Installation](../adapters/codex/README.md#baseline-installation), to merge only the approved block. A source update requires an authorized synchronization into each intended runtime owner; installed blocks do not synchronize themselves. Static equality establishes installation, while improvement over the prior baseline remains unproven until representative code tasks are compared.

## Agent Import Procedure

1. Resolve the runtime's effective global instruction file through its adapter,
   then read that destination and these references. If the destination is a
   symlink, resolve its owner before editing.
2. Compare common, environment-specific, and PC-specific rules separately. Keep
   existing useful instructions and identify duplicates or conflicting rules.
3. Resolve environment values and paths from the destination and confirmed user
   context. Ask only about conflicts or missing values that cannot be resolved;
   never install placeholder or invented values as actual settings.
4. When import is requested, merge applicable rules directly into the destination,
   preserving unrelated content, examples, exceptions, and instruction strength.
   Keep the existing shared managed markers when importing their marked blocks.
   For response and code quality baselines, follow the runtime's installation
   procedure, such as [Codex Baseline Installation](../adapters/codex/README.md#baseline-installation);
   their essential rules work without a repository harness or skill invocation.
5. Verify that no unique existing guidance was lost, and summarize what changed.

## Codex Example Request

> ai-assets/agents/instructions를 참고해서 이 PC의
> ~/.codex/AGENTS.md를 확인하고 필요한 내용을 import해줘. 기존 지침은 보존하고,
> 기업 환경과 PC 경로는 현재 설정을 기준으로 맞춰줘.
