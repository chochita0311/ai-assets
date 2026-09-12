# Reusable Personal Instructions

Use this directory as a small reference library when asking an agent to review
and import personal instructions into an existing `AGENTS.md`.

## What To Reuse

| Reference | Scope |
|---|---|
| [general.md](general.md) | Common personal preferences: PR descriptions, local writes, temporary artifacts, and Go caches |
| [environment.template.md](environment.template.md) | Optional rules for a company or other environment: hosts, connectors, and GitHub Enterprise commands |
| [machine.template.md](machine.template.md) | PC-specific path aliases and examples |
| [Shared adapter instructions](../global-agents-managed-section.md) | Existing delegation and context-continuity rules |

The templates illustrate what to consider; use only the parts relevant to the
destination. Actual company values and local paths belong in the destination
`AGENTS.md`. This public repository keeps generic placeholders and examples.

## Agent Import Procedure

1. Read the destination `AGENTS.md` and these references. If the destination is a
   symlink, resolve its owner before editing.
2. Compare common, environment-specific, and PC-specific rules separately. Keep
   existing useful instructions and identify duplicates or conflicting rules.
3. Resolve environment values and paths from the destination and confirmed user
   context. Ask only about conflicts or missing values that cannot be resolved;
   never install placeholder or invented values as actual settings.
4. When import is requested, merge applicable rules directly into the destination,
   preserving unrelated content, examples, exceptions, and instruction strength.
   Keep the existing shared adapter markers when importing their marked blocks.
5. Verify that no unique existing guidance was lost, and summarize what changed.

## Example Request

> ai-assets/agents/adapters/codex/instructions를 참고해서 이 PC의
> ~/.codex/AGENTS.md를 확인하고 필요한 내용을 import해줘. 기존 지침은 보존하고,
> 기업 환경과 PC 경로는 현재 설정을 기준으로 맞춰줘.
