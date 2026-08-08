# Agent System Adoption Guide

## Purpose
- Explain how to adopt this shared harness package into a consuming repo.
- Keep the export pattern repeatable without turning the package into repo-specific automation.
- Keep personal Codex runtime installation separate; use [adapters/codex/README.md](adapters/codex/README.md) for global Codex policy and custom-agent bindings.

## When To Use This Guide
- A consuming repo does not yet have the harness package.
- A consuming repo has an older local copy and needs a controlled sync from `../ai-assets/agents/`.
- The operator wants the resulting repo to look like a normal local agent system, not like a mounted external dependency.

## Shared Source Package
- Shared source lives in `../ai-assets/agents/`.
- Shared harness governance lives in `../ai-assets/agents/policies/harness/`.
- Shared execution profiles live in `../ai-assets/agents/profiles/`.
- Shared templates live in `../ai-assets/agents/templates/`.

## Target Shape In A Consuming Repo
After export, the consuming repo should normally own:

- `docs/agents/`
  - `roles/`
  - `flows/`
  - `operations/`
  - `profiles/`
  - `templates/`
    - non-persistent agent response scaffolds such as `operator-briefing.md`
- `docs/plans/`
  - `prd/`
  - `feature/`
  - `spec/`
  - `run/`
  - `evaluation/`
  - `fix/`
  - `heuristic/`
- `docs/policies/harness/`
  - planning, execution, profile, traceability, and operator-continuity governance
- `docs/policies/design/` and `docs/policies/experience/`
  - review assets when the consuming repo wants durable visual and interaction evaluation rules

## Export Mapping
Use this mapping when exporting from the shared package into a consuming repo:

- `../ai-assets/agents/roles/*.md`
  -> `docs/agents/roles/*.md`
- `../ai-assets/agents/flows/*.md`
  -> `docs/agents/flows/*.md`
- `../ai-assets/agents/operations/*.md`
  -> `docs/agents/operations/*.md`
- `../ai-assets/agents/profiles/*.md`
  -> `docs/agents/profiles/*.md`
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
- `../ai-assets/agents/templates/operator-briefing.md`
  -> `docs/agents/templates/operator-briefing.md`
- `../ai-assets/agents/policies/harness/*.md`
  -> `docs/policies/harness/*.md`
- `../ai-assets/agents/policies/review/design-evaluation.md`
  -> `docs/policies/design/design-evaluation.md`
- `../ai-assets/agents/policies/review/interaction-evaluation.md`
  -> `docs/policies/experience/interaction-evaluation.md`

The harness-policy wildcard includes `operator-briefing-and-review-receipts.md`. Export that policy and the operator briefing template whenever roles or flows are exported so their continuity references remain complete.

## Exported Link Rewriting
The shared source tree and the consuming-repo tree intentionally use different roots. Rewrite these source-relative links during export instead of copying them unchanged:

- In exported role and flow docs, rewrite `../policies/harness/operator-briefing-and-review-receipts.md` to `../../policies/harness/operator-briefing-and-review-receipts.md`.
- In the exported operator policy, rewrite `../../templates/operator-briefing.md` to `../../agents/templates/operator-briefing.md`.
- Do not leave exported documents dependent on `../ai-assets/` or another external source path.

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
  - `roles/`
  - `flows/`
  - `operations/`
  - `profiles/`
  - `templates/`
- `docs/plans/`
- `docs/policies/harness/`
- `docs/policies/design/`
- `docs/policies/experience/`

Keep the exported docs general unless this repo already needs local specialization.
Rewrite source-relative cross-links for the consuming-repo layout.
Update local entrance docs and references so the resulting layout is coherent.
```

### Refresh Or Resync
```text
Refresh the local agent system in this repo from `../ai-assets/agents/`.

Keep repo-specific policy or product docs that are not part of the shared harness package.
Update only the shared role, profile, template, and harness-policy layer.
If local docs have drifted, reconcile references and ownership cleanly instead of duplicating guidance.
```

### Controlled Merge
```text
Adopt the shared agent system from `../ai-assets/agents/`, but merge it into the current local structure instead of overwriting blindly.

Preserve repo-specific architecture, product policy, and content contracts.
Replace or align only the reusable harness layer:
- role docs
- profile docs
- templates
- harness governance
- review assets
```

## Promotion From Consuming Repos
When a consuming repo improves the agent system:

1. Compare local docs against `../ai-assets/agents/`.
2. Classify each difference as:
   - `promote`: general reusable rule
   - `local`: project-specific rule
   - `discard`: historical note, accidental drift, or obsolete wording
3. Promote only general reusable rules into `ai-assets`.
4. Generalize examples before promotion so they do not depend on one product, framework, language, or local filesystem path.
5. Refresh consuming repos from the canonical package after promotion.

## Post-Export Checks
After export into a consuming repo:

1. Check entrance docs and cross-links.
2. Confirm that `docs/policies/harness/operator-briefing-and-review-receipts.md` and `docs/agents/templates/operator-briefing.md` exist when shared roles or flows are installed.
3. Confirm that links from the exported orchestrator, workflow, and operator policy resolve inside the consuming repo.
4. Check that all other local harness policy paths are correct.
5. Check whether review assets belong under local `design/` and `experience/` policy owners.
6. Add a short execution gate to the consuming repo's `AGENTS.md` so planning requests stop at PRD or feature review instead of being reinterpreted as implementation approval.
7. Keep repo-specific rules outside the shared role package.
8. Confirm that generated planning docs use repo-relative links instead of local absolute paths.
9. Commit the imported harness layer separately from unrelated product work when possible.

## Local AGENTS Gate
When a consuming repo uses the shared planning workflow, its local `AGENTS.md` should restate the stop conditions that must be visible at task start:

- PRD requests are planning-only until the human owner approves the boundary.
- `draft` PRDs and unapproved feature proposals must not trigger spec work, code changes, or evaluation.
- If open points can still change scope, acceptance, dependency, or user-visible behavior, stop and ask instead of implementing.
- When a canonical target starts or resumes and prior context materially affects understanding or execution, apply `docs/policies/harness/operator-briefing-and-review-receipts.md`; otherwise preserve the normal response shape.

## Repository-Local Operator Context
Repository adoption owns the detailed operator-context behavior. Install the policy and non-persistent response scaffold at the mapped local paths, then expose the conditional pointer above from the consuming repo's entrance layer.

- No project-specific command, state, tracker, map, or historical backfill is required.
- Existing project artifacts and source-of-truth ownership remain unchanged.
- Adopt the behavior prospectively; do not create permanent briefing logs for earlier conversations.
- The personal Codex adapter is optional and does not install these repo-local assets. Its managed hook only recognizes relevant triggers when the current repo already exposes the detailed policy.

## Non-Goals
- automatic installer scripting
- runtime linking back to `../ai-assets/agents/`
- replacing repo-specific product planning artifacts
