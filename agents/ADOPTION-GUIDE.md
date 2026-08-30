# Agent System Adoption Guide

## Purpose
- Explain how to adopt this shared harness package into a consuming repo.
- Keep the export pattern repeatable without turning the package into repo-specific automation.
- Record enough per-repo import state to distinguish later upstream changes from intentional local changes.
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
- The generalized import-manifest example lives at `../ai-assets/agents/harness-import-manifest.example.json`.

## Target Shape In A Consuming Repo
After export, the consuming repo should normally own:

- `docs/agents/`
  - `harness-import-manifest.json`
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

Do not export `harness-import-manifest.example.json` as a managed shared file. Use it to initialize the consuming repo's own `docs/agents/harness-import-manifest.json` only after the fresh export and its finalization checks succeed.

## Exported Link Rewriting
The shared source tree and the consuming-repo tree intentionally use different roots. Rewrite these source-relative links during export instead of copying them unchanged:

- In exported role and flow docs, rewrite `../policies/harness/operator-briefing-and-review-receipts.md` to `../../policies/harness/operator-briefing-and-review-receipts.md`.
- In the exported operator policy, rewrite `../../templates/operator-briefing.md` to `../../agents/templates/operator-briefing.md`.
- Do not leave exported documents dependent on `../ai-assets/` or another external source path.

## Local Ownership Rules
- The consuming repo should own the final installed copy.
- The consuming repo should own `docs/agents/harness-import-manifest.json` as operational import state.
- After export, local docs should read as if they belong to that repo directly.
- Do not leave the consuming repo depending on `../ai-assets/...` paths for normal operation.
- Treat the manifest as a refresh baseline, not as a source of harness policy or product truth.

## What Must Stay Local
Do not overwrite repo-local material that is not part of the shared harness package:

- architecture rules
- content contracts
- product-specific design constitutions
- project-specific developer guides
- existing run artifacts
- product PRDs and feature plans

## Harness Import Manifest

### Role And Location

- The shared example is [harness-import-manifest.example.json](harness-import-manifest.example.json).
- A consuming repo stores its actual manifest at `docs/agents/harness-import-manifest.json`.
- The example is a schema-shaped illustration. Do not copy placeholder hashes or treat its one sample file as a complete installation.
- The actual manifest must enumerate every selected harness-origin file that the consuming repo tracks. One file entry owns one exact source-to-target mapping and its last accepted baseline provenance and hashes.
- Do not include the manifest itself in `files`; it is the repo-owned index of the other tracked artifacts.
- Do not list unrelated repo-local architecture, product, planning, or run artifacts.
- Do not record an absolute local source path. Resolve the current `ai-assets` checkout explicitly for the active session and record only the logical repository, package root, and full Git revision.

### Required Fields

- `schema_version`: manifest contract version. Start with `1`.
- `source.repository`: logical source repository name, normally `ai-assets`.
- `source.package_root`: package-relative root, normally `agents`.
- `source.revision`: full Git commit SHA for the latest accepted upstream snapshot used by the import or refresh operation. Import from a committed shared-source state.
- `selection.repository_surfaces`: consuming-repo capability surfaces used to choose the exported set.
- `selection.excluded_capabilities`: intentionally omitted optional capabilities such as `design` or `ux`.
- `mapping.version`: latest export-mapping and link-rewrite contract version used by the import or refresh operation. Start with `1` and increment it when those semantics change materially.
- `files`: the resolved tracked file list for the consuming repo.

Each `files` entry must record:

- `source`: path relative to `source.package_root`
- `target`: path relative to the consuming-repo root
- `ownership`: `managed` for a shared file eligible for controlled refresh, or `local` for a harness-origin file intentionally detached for repo-local ownership
- `baseline_source_revision`: full Git commit SHA containing the source content identified by `source_sha256`
- `baseline_mapping_version`: mapping and link-rewrite contract version used to produce `rendered_sha256`
- `source_sha256`: SHA-256 of the source file at the entry's accepted baseline
- `rendered_sha256`: SHA-256 of the installed content after target-layout and link-rewrite transforms at that baseline

Keep `files` deterministically sorted by `target`, reject duplicate source or target mappings, and record hashes as lowercase 64-character hexadecimal values.

For a `managed` entry, compare the current target hash with `rendered_sha256` before refresh. A mismatch is a local modification and must not be overwritten automatically. After accepting a managed refresh, advance its baseline provenance and hashes together to the accepted source and rendered result.

For a `local` entry, preserve the target unconditionally and keep its per-entry baseline provenance and hashes together as the detachment baseline for later review or promotion. The top-level source revision and mapping version may advance for the refresh as a whole, but the local entry's baseline fields must not advance during ordinary refresh. Rebase or reattach it only through an explicit ownership decision.

### Manifest Lifecycle

- Generate and update the manifest from resolved files; do not hand-edit hashes.
- After content and link checks pass, generate and validate a candidate manifest before replacing the installed manifest.
- Replace the installed manifest only as the final successful refresh step.
- Leave the prior manifest unchanged when export, refresh, conflict resolution, candidate-manifest validation, or another required check fails.
- Keep the manifest in the same harness-only commit as the imported or refreshed shared layer when possible.
- Do not update a recorded hash to match unexplained local drift. Classify the difference first as an accepted upstream result, intentional local ownership, or an unresolved conflict.
- When the shared example's `mapping.version` differs from the installed manifest, treat the mapping or link transforms as changed and re-render the selected file set before comparing target hashes.
- Do not remove a previously tracked target merely because the new selection omits it. Report it as a retirement candidate and remove it only after explicit review.

## Adoption Mode Resolution

Resolve the mode before writing:

- No manifest and no installed local harness: use `Fresh Export`.
- No manifest but local harness files already exist: use `Existing Installation Bootstrap`.
- Valid manifest exists: use `Refresh Or Resync` from the recorded baseline.
- Invalid manifest exists: use `Manifest Recovery`; preserve it and stop before harness-content writes.
- A missing or invalid manifest is never proof that existing local files are safe to overwrite.

### Manifest Recovery

When an installed manifest fails schema, path, uniqueness, hash, or provenance validation, preserve it unchanged as evidence and do not use any of its values as a refresh baseline. Build and validate a separate recovery candidate from supported source, target, and Git evidence, using the evidence steps from `Existing Installation Bootstrap` when needed. Resume controlled refresh only after the recovered baseline candidate is valid and every unexplained difference is classified; replace the installed manifest only as the final successful step.

### Existing Installation Bootstrap

When a repo already has imported harness files but no manifest:

1. Inspect the consuming repo's entrance docs, current harness layout, Git history, and repo-local ownership rules.
2. Resolve the intended repository surfaces and optional capability exclusions.
3. Identify the previous harness-only import or refresh commit and its `ai-assets` revision when possible.
4. Render the candidate shared source into the consuming layout before comparing it with current targets.
5. Classify exact or historically supported shared matches as `managed`.
6. Classify confirmed intentional specializations as `local`.
7. Treat unexplained differences as conflicts. Do not overwrite them or manufacture baseline hashes.
8. Complete the controlled merge and finalization checks.
9. Create the manifest only after every tracked entry has a supported source, target, ownership, and baseline.

Bootstrap existing installations lazily on their next refresh. Do not require an immediate repository-wide migration solely to add manifests.

## Operator Prompts
Use prompts like these when asking a local coding agent to install or refresh the package in a repo.

`Fresh Export` and `Refresh Or Resync` have mode-matched prompts below. `Existing Installation Bootstrap` and `Manifest Recovery` follow the procedures above; bootstrap uses `Controlled Merge` for its merge step, but `Controlled Merge` is not an additional manifest-state mode.

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
After content and link checks pass, generate and validate a complete candidate from the shared example using the full source revision and every tracked file. Write `docs/agents/harness-import-manifest.json` only as the final successful export step.
```

### Refresh Or Resync
```text
Refresh the local agent system in this repo from `../ai-assets/agents/`.

Read `docs/agents/harness-import-manifest.json` first when it exists.
If the manifest is missing but local harness files already exist, bootstrap the existing installation instead of performing a blind fresh export.
If the manifest exists but fails validation, preserve it unchanged and stop before harness-content writes. Build and validate a separate recovery candidate from supported source, target, and Git evidence; never refresh from invalid values or replace the installed manifest before the final successful step.
Keep repo-specific policy or product docs that are not part of the shared harness package.
Update only the shared role, flow, operation, profile, template, and harness-policy layers.
If local docs have drifted, reconcile references and ownership cleanly instead of duplicating guidance.
Compare source and rendered hashes before writing, preserve `local` entries, and report unexplained differences as conflicts.
If the current shared mapping version differs from the manifest, re-render the selected file set before comparing targets.
Generate and validate the next manifest only after content and link checks pass. Replace the installed manifest only as the final successful refresh step.
```

### Controlled Merge
```text
Adopt the shared agent system from `../ai-assets/agents/`, but merge it into the current local structure instead of overwriting blindly.

Preserve repo-specific architecture, product policy, and content contracts.
Replace or align only the reusable harness layer:
- role docs
- flow docs
- operation docs
- profile docs
- templates
- harness governance
- review assets

Use the import manifest when available to distinguish managed shared files from intentional local ownership. Do not normalize unexplained local differences into a new baseline.
```

## Promotion From Consuming Repos
When a consuming repo improves the agent system:

1. Compare local docs against `../ai-assets/agents/`.
   - When a manifest exists, start from its recorded rendered baseline so upstream evolution is not confused with local delta.
2. Classify each difference as:
   - `promote`: general reusable rule
   - `local`: project-specific rule
   - `discard`: historical note, accidental drift, or obsolete wording
3. Promote only general reusable rules into `ai-assets`.
4. Generalize examples before promotion so they do not depend on one product, framework, language, or local filesystem path.
5. Refresh consuming repos from the canonical package after promotion.

## Export And Refresh Finalization Checks
Before finalizing an export or refresh in a consuming repo:

1. Check entrance docs and cross-links.
2. Confirm that `docs/policies/harness/operator-briefing-and-review-receipts.md` and `docs/agents/templates/operator-briefing.md` exist when shared roles or flows are installed.
3. Confirm that links from the exported orchestrator, workflow, and operator policy resolve inside the consuming repo.
4. Check that all other local harness policy paths are correct.
5. Check whether review assets belong under local `design/` and `experience/` policy owners.
6. Add a short execution gate to the consuming repo's `AGENTS.md` so planning requests stop at PRD or feature review instead of being reinterpreted as implementation approval.
7. Keep repo-specific rules outside the shared role package.
8. Confirm that generated planning docs use repo-relative links instead of local absolute paths.
9. Confirm that the candidate manifest uses full source commit SHAs from committed shared-source states and contains no absolute source or target paths.
10. Confirm that every selected harness-origin file is represented once, mappings are unique and deterministically ordered, every entry has attributable baseline provenance, and every `managed` target matches its recorded `rendered_sha256` after the operation.
11. Confirm that the manifest does not list itself and that repo-local product and planning artifacts are absent.
12. Write or replace the installed manifest only after checks 1-11 pass.
13. Commit the imported harness layer and its manifest separately from unrelated product work when possible.

## Local AGENTS Gate
When a consuming repo uses the shared planning workflow, its local `AGENTS.md` should restate the stop conditions that must be visible at task start:

- PRD requests are planning-only until the human owner approves the boundary.
- `draft` PRDs and unapproved feature proposals must not trigger spec work, code changes, or evaluation.
- If open points can still change scope, acceptance, dependency, or user-visible behavior, stop and ask instead of implementing.
- When a canonical target starts or resumes and prior context materially affects understanding or execution, apply `docs/policies/harness/operator-briefing-and-review-receipts.md`; otherwise preserve the normal response shape.

## Repository-Local Operator Context
Repository adoption owns the detailed operator-context behavior. Install the policy and non-persistent response scaffold at the mapped local paths, then expose the conditional pointer above from the consuming repo's entrance layer.

- No additional operator-context command, tracker, map, or historical backfill is required; the import manifest is separate adoption state and does not persist briefing content.
- Existing project artifacts and source-of-truth ownership remain unchanged.
- Adopt the behavior prospectively; do not create permanent briefing logs for earlier conversations.
- The personal Codex adapter is optional and does not install these repo-local assets. Its managed hook only recognizes relevant triggers when the current repo already exposes the detailed policy.

## Non-Goals
- automatic installer scripting
- runtime linking back to `../ai-assets/agents/`
- replacing repo-specific product planning artifacts
