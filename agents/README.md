# Agent Runtime Assets

## Purpose

Keep shared instructions, prompt presets, and runtime adapters independently
reusable. Portable workflow orchestration belongs to the peer
[harness package](../harness/README.md); shared policy rules belong to
[policies/](../policies/README.md).

## Shared Instructions Package
- [agents/instructions/README.md](instructions/README.md): generate common local-AI instructions from their policy owners and selectively import personal, environment, and machine guidance
- [agents/instructions/standard.md](instructions/standard.md): generated, self-contained response and code quality baselines, delegation rules, and conditional operator-context recognition
- [policies/README.md](../policies/README.md): ownership map for session-wide baselines, shared delegation, evaluation criteria, and related harness governance

## Prompt Presets Package
- [agents/presets/codex/README.md](presets/codex/README.md): reusable prompt sources, a numbered catalog, selection rendering, and full or selective import into local Codex configuration
- Prompt presets own their catalog and import procedure independently of runtime adapters. An import request can select all entries or specific catalog numbers; it configures prompts without executing them.

## Runtime Adapters Package
- [agents/adapters/codex/README.md](adapters/codex/README.md): install the shared instruction bundle and applicable personal guidance, named worker and profile bindings, and a read-only model-lifecycle audit into a personal Codex runtime
- Keep portable policies and shared instructions outside adapters. Adapters own platform-specific discovery and installation of their runtime assets, concrete model and capability bindings, and platform-specific audit, runner, and schedule assets. The current packaged adapter is Codex; another runtime can reuse the common instructions through its own verified adapter.

## Related Shared Docs

- [policies/baseline/response-clarity.md](../policies/baseline/response-clarity.md): session-wide meaning preservation, reader-oriented composition, sources, and the boundary between global response defaults and repository harness behavior
- [policies/baseline/code-quality.md](../policies/baseline/code-quality.md): session-wide decision guidance for project conformity, simplicity, version-aware documentation, and verification evidence
- [policies/competence-first-delegation.md](../policies/competence-first-delegation.md): platform-neutral admission, capability, fallback, context-transfer, and final-ownership rules for delegated work
- [harness/README.md](../harness/README.md): runtime-neutral workflow roles, flows, operations, profiles, governance, and templates
- [harness/ADOPTION-GUIDE.md](../harness/ADOPTION-GUIDE.md): export and refresh harness contracts into a consuming repo, independently of personal runtime installation

## Packaging Rule

Keep instructions under `agents/instructions/`, prompt presets under
`agents/presets/`, and runtime-specific bindings and installation assets under
`agents/adapters/`. Public improvement records stay in repository-level
`evidence/` under their subject domain and component. Harness adoption does not
implicitly install personal runtime files or select a runtime adapter.
