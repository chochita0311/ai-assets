# AI Assets

Reusable AI assets for project work, centered on portable Codex skills and shared agent-system materials.

## What Lives Here
- [skills/](skills/): reusable skill packages with `SKILL.md` entry contracts, references, templates, and skill-local metadata
- [agents/](agents/): reusable harness roles, flows, operations, profiles, policies, runtime adapters, and execution templates
- [agents/policies/](agents/policies/): reusable harness governance and evaluation assets shared with the agent package
- [pets/](pets/README.md): reusable Codex-compatible pet packages, metadata, and spritesheet assets
- [scripts/](scripts/): repository-level validation and maintenance tools shared across asset packages

## How To Navigate
- Start with [AGENTS.md](AGENTS.md) for the operational repo map and working rules.
- Read [skills/SKILL-QUALITY.md](skills/SKILL-QUALITY.md) for the quality bar and maintenance reference for reusable skills.
- Review [skills/skill-followups.md](skills/skill-followups.md) for durable unresolved skill follow-up work across the repository.
- Read [agents/README.md](agents/README.md) for the shared agent package.
- Use [agents/ADOPTION-GUIDE.md](agents/ADOPTION-GUIDE.md) when exporting or refreshing the agent package in a consuming repo.
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

## Skill Catalog
- [design-plan](skills/design-plan/SKILL.md): plan multi-screen design consistency and reconciliation work
- [docs-shaping](skills/docs-shaping/SKILL.md): reshape document composition while preserving meaning
- [docs-structuring](skills/docs-structuring/SKILL.md): organize layered repository documentation and ownership
- [gh-review-pr](skills/gh-review-pr/SKILL.md): review, draft, audit, refresh, publish, or safely maintain frozen-snapshot GitHub PR reviews with verified inline threads
- [init-design](skills/init-design/SKILL.md): derive a durable design constitution from an initial source set
- [maintain-context-freshness](skills/maintain-context-freshness/SKILL.md): audit and safely maintain context freshness without erasing unique evidence
- [pr-descriptor](skills/pr-descriptor/SKILL.md): create and evaluate evidence-based pull request artifacts, and safely apply explicitly requested description updates
- [refactor-plan](skills/refactor-plan/SKILL.md): plan bounded refactors with parity and merge-safety gates
- [refine-skill](skills/refine-skill/SKILL.md): refine an existing skill from real output evidence
- [screen-alignment](skills/screen-alignment/SKILL.md): align a screen with an existing design system
- [workflow-context-sync](skills/workflow-context-sync/SKILL.md): reconcile multi-source workflow context into an explicitly owned target

## Repository Intent
- Keep assets portable across consuming repos.
- Prefer one clear owner for each durable rule.
- Strengthen existing contracts before adding parallel guidance.
