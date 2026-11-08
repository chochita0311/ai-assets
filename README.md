# AI Assets

Reusable AI assets for project work, centered on portable Codex skills and shared agent-system materials.

## What Lives Here
- [skills/](skills/): reusable skill packages with `SKILL.md` entry contracts, references, templates, and skill-local metadata
- [harness/](harness/README.md): reusable runtime-neutral roles, flows, operations, profiles, workflow governance, and execution templates
- [agents/](agents/README.md): shared instructions, prompt presets, and platform-specific runtime adapters
- [evidence/](evidence/README.md): generalized improvement evidence, reusable knowledge and pending work, organized by asset domain and component
- [policies/](policies/README.md): session-wide defaults under `baseline/`, shared delegation policy, and evaluation criteria under `review/`
- [agents/instructions/](agents/instructions/README.md): generated shared local-AI instructions and selectable personal, environment, and machine guidance
- [agents/presets/codex/](agents/presets/codex/README.md): reusable Codex prompt presets with a numbered catalog and independent full or selective import into local configuration
- [pets/](pets/README.md): reusable Codex-compatible pet packages, metadata, and spritesheet assets
- [tools/](tools/README.md): standalone reusable utilities organized by provider and tool
- [scripts/](scripts/): repository-level validation and maintenance tools shared across asset packages

## How To Navigate
- Start with [AGENTS.md](AGENTS.md) for the operational repo map and working rules.
- Read [skills/SKILL-QUALITY.md](skills/SKILL-QUALITY.md) for the quality bar and maintenance reference for reusable skills.
- Use the [improvement record catalog](evidence/README.md) for reusable knowledge and pending improvements across asset domains, stored by component. The [record and exchange contract](harness/policies/improvement-record-contract.md) governs their shared format, placement, import, export and feedback.
- Read [harness/README.md](harness/README.md) for shared workflow roles, orchestration, and adoption; [agents/README.md](agents/README.md) covers independent runtime instructions, presets, and adapters.
- Use the [optional research workflow](harness/flows/research.md) for bounded, resumable investigation in a harness that explicitly adopts it.
- Use [Codex Prompt Presets](agents/presets/codex/README.md) to list prompts or import all or selected preset numbers on a PC; that package owns its import procedure separately from runtime adapters.
- Use [Shared Local AI Instructions](agents/instructions/README.md) for shared-bundle generation and agent-led import of applicable personal, environment-specific, and PC-specific guidance. Runtime adapters own local installation.
- Use [Response Clarity And Meaning Preservation](policies/baseline/response-clarity.md) for the global response baseline, its sources, and content-preservation checks; its generated runtime rules work without a repository harness or skill.
- Use [Code Quality](policies/baseline/code-quality.md) for session-wide guidance on project rules, simplicity, version-aware official documentation, and scoped verification. The Codex adapter installs either baseline for Codex.
- Use [harness/ADOPTION-GUIDE.md](harness/ADOPTION-GUIDE.md) when exporting or refreshing the harness package in a consuming repo.
- Read [pets/README.md](pets/README.md) before adding or changing a pet package.
- Run [validate_skill_packages.py](scripts/validate_skill_packages.py) after changing a skill package.
- Use each skill package's `SKILL.md` as the entry contract for that skill.

## Validate Skill Packages

Run the repository validator for every package or name one or more packages:

```bash
python3 scripts/validate_skill_packages.py
python3 scripts/validate_skill_packages.py gh-review-pr pr-descriptor
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The validator checks that each frontmatter `name` matches its package directory and inventories `$<skill-name>` references across every UTF-8 text file in the package. Self references pass. A reference to another skill passes only when the same line makes runtime availability explicit, or when both packages share an explicit bundle in the optional `skills/skill-bundles.json` contract. Every allowed external reference is still emitted as a `REVIEW` item for human confirmation.

Use a bundle only when the named skills are actually distributed together:

```json
{
  "schema_version": 1,
  "bundles": {
    "example-bundle": ["first-skill", "second-skill"]
  }
}
```

## Validate Shared Agent Instructions

Edit the marked rules in their policy owners, then regenerate and check the
shared bundle before distributing it:

```sh
python3 scripts/render_global_agent_instructions.py
python3 scripts/render_global_agent_instructions.py --check
python3 -m unittest discover -s scripts -p 'test_render_global_agent_instructions.py'
```

Generation changes the repository artifact only. Updating a local runtime is a
separate merge that preserves its existing instructions and settings; see the
[shared instruction guide](agents/instructions/README.md).

## Skill Catalog
- [clean-code](skills/clean-code/SKILL.md): simplify hard-to-read code and clarify responsibility boundaries within the requested scope
- [design-deslop](skills/design-deslop/SKILL.md): compare UI improvements through inspectable before/after HTML, choose whole changes or parts, and send preferences back for another preview before adoption
- [design-plan](skills/design-plan/SKILL.md): plan multi-screen design consistency and reconciliation work
- [docs-shaping](skills/docs-shaping/SKILL.md): reshape document composition while preserving meaning
- [docs-structuring](skills/docs-structuring/SKILL.md): organize layered repository documentation and ownership
- [gh-review-pr](skills/gh-review-pr/SKILL.md): review, draft, audit, refresh, publish, or safely maintain frozen-snapshot GitHub PR reviews with verified inline threads
- [init-design](skills/init-design/SKILL.md): derive a durable design constitution from an initial source set
- [maintain-context-freshness](skills/maintain-context-freshness/SKILL.md): audit and safely maintain context freshness without erasing unique evidence
- [pr-descriptor](skills/pr-descriptor/SKILL.md): create and evaluate evidence-based pull request artifacts, and safely apply explicitly requested description updates
- [refactor-plan](skills/refactor-plan/SKILL.md): plan bounded refactors with parity and merge-safety gates
- [refine-skill](skills/refine-skill/SKILL.md): audit or improve an existing skill through evidence, failure diagnosis, and comparable validation
- [research-sadr](skills/research-sadr/SKILL.md): investigate open questions with competing explanations, independent challenge, and evidence-based conclusions
- [screen-alignment](skills/screen-alignment/SKILL.md): align a screen with an existing design system
- [ui-atlas](skills/ui-atlas/SKILL.md): inspect existing screens, selectable DOM elements and payload-driven states on a local pan-and-zoom canvas; keep consumer outputs in `.artifacts/ui-atlas/` by default
- [workflow-context-sync](skills/workflow-context-sync/SKILL.md): reconcile multi-source workflow context into an explicitly owned target

## Repository Intent
- Keep assets portable across consuming repos.
- Prefer one clear owner for each durable rule.
- Strengthen existing contracts before adding parallel guidance.
