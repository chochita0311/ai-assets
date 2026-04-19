# Agent System Adoption Guide

## Purpose
- Explain how to adopt this shared harness package into a consuming repo.
- Keep the export pattern repeatable without turning the package into repo-specific automation.

## When To Use This Guide
- A consuming repo does not yet have the harness package.
- A consuming repo has an older local copy and needs a controlled sync from `../ai-assets/agents/`.
- The operator wants the resulting repo to look like a normal local agent system, not like a mounted external dependency.

## Shared Source Package
- Shared source lives in `../ai-assets/agents/`.
- Shared harness governance lives in `../ai-assets/agents/policies/`.
- Shared templates live in `../ai-assets/agents/templates/`.

## Target Shape In A Consuming Repo
After export, the consuming repo should normally own:

- `docs/agents/`
  - `role/`
  - `flow/`
  - `operation/`
- `docs/plans/`
  - `prd/`
  - `feature/`
  - `spec/`
  - `run/`
  - `evaluation/`
  - `fix/`
  - `heuristic/`
- `docs/policies/harness/`
  - planning and execution governance
- `docs/policies/design/` and `docs/policies/experience/`
  - review assets when the consuming repo wants durable visual and interaction evaluation rules

## Export Mapping
Use this mapping when exporting from the shared package into a consuming repo:

- `../ai-assets/agents/role/*.md`
  -> `docs/agents/role/*.md`
- `../ai-assets/agents/flow/*.md`
  -> `docs/agents/flow/*.md`
- `../ai-assets/agents/operation/*.md`
  -> `docs/agents/operation/*.md`
- `../ai-assets/agents/templates/prd.md`
  -> `docs/plans/prd/template-prd.md`
- `../ai-assets/agents/templates/feature.md`
  -> `docs/plans/feature/template-feature.md`
- `../ai-assets/agents/templates/spec.md`
  -> `docs/plans/spec/template-spec.md`
- `../ai-assets/agents/templates/run.md`
  -> `docs/plans/run/template-run.md`
- `../ai-assets/agents/templates/evaluation.md`
  -> `docs/plans/evaluation/template-evaluation.md`
- `../ai-assets/agents/templates/fix-log.md`
  -> `docs/plans/fix/template-fix-log.md`
- `../ai-assets/agents/templates/heuristic-backlog.md`
  -> `docs/plans/heuristic/template-heuristic-backlog.md`
- `../ai-assets/agents/policies/harness/*.md`
  -> `docs/policies/harness/*.md`
- `../ai-assets/agents/policies/review/design-evaluation.md`
  -> `docs/policies/design/design-evaluation.md`
- `../ai-assets/agents/policies/review/interaction-evaluation.md`
  -> `docs/policies/experience/interaction-evaluation.md`

## Local Ownership Rules
- The consuming repo should own the final installed copy.
- After export, local docs should read as if they belong to that repo directly.
- Do not leave the consuming repo depending on `../ai-assets/...` paths for normal operation.

## What Must Stay Local
Do not overwrite repo-local material that is not part of the shared harness package:

- architecture rules
- content contracts
- product-specific design constitutions
- project-specific developer guides
- existing run artifacts
- product PRDs and feature plans

## Operator Prompts
Use prompts like these when asking a local coding agent to install or refresh the package in a repo.

### Fresh Export
```text
Export the agent system from `../ai-assets/agents/` into this repo.

Install it as a local docs-owned system, not as a runtime dependency.
Map the shared package into:
- `docs/agents/`
  - `role/`
  - `flow/`
  - `operation/`
- `docs/plans/`
- `docs/policies/harness/`
- `docs/policies/design/`
- `docs/policies/experience/`

Keep the exported docs general unless this repo already needs local specialization.
Update local entrance docs and references so the resulting layout is coherent.
```

### Refresh Or Resync
```text
Refresh the local agent system in this repo from `../ai-assets/agents/`.

Keep repo-specific policy or product docs that are not part of the shared harness package.
Update only the shared role, template, and harness-policy layer.
If local docs have drifted, reconcile references and ownership cleanly instead of duplicating guidance.
```

### Controlled Merge
```text
Adopt the shared agent system from `../ai-assets/agents/`, but merge it into the current local structure instead of overwriting blindly.

Preserve repo-specific architecture, product policy, and content contracts.
Replace or align only the reusable harness layer:
- role docs
- templates
- harness governance
- review assets
```

## Post-Export Checks
After export into a consuming repo:

1. Check entrance docs and cross-links.
2. Check that local harness policy paths are correct.
3. Check whether review assets belong under local `design/` and `experience/` policy owners.
4. Add a short execution gate to the consuming repo's `AGENTS.md` so planning requests stop at PRD or feature review instead of being reinterpreted as implementation approval.
5. Keep repo-specific rules outside the shared role package.
6. Commit the imported harness layer separately from unrelated product work when possible.

## Local AGENTS Gate
When a consuming repo uses the shared planning workflow, its local `AGENTS.md` should restate the stop conditions that must be visible at task start:

- PRD requests are planning-only until the human owner approves the boundary.
- `draft` PRDs and unapproved feature proposals must not trigger spec work, code changes, or evaluation.
- If open points can still change scope, acceptance, dependency, or user-visible behavior, stop and ask instead of implementing.

## Non-Goals
- automatic installer scripting
- runtime linking back to `../ai-assets/agents/`
- replacing repo-specific product planning artifacts
