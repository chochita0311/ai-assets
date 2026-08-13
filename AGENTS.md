# Repository Guidelines

## Purpose
- This repo stores reusable AI assets, including Codex skills.
- Each skill should remain portable, checkable, and maintainable across projects.
- Optimize for strong contracts, clean file roles, and harness-friendly expansion.
- Use [README.md](README.md) for the user-facing repository overview.

## Codebase Map
- Scan the repo root before assuming structure.
- [agents/](agents/) holds reusable harness roles, flows, operations, profiles, policies, and templates.
- [agents/adapters/](agents/adapters/) holds platform-specific runtime bindings and installable policy fragments derived from shared policy.
- [agents/templates/](agents/templates/) holds shared planning, execution, evaluation, and non-persistent response scaffolds for consuming repos.
- [agents/profiles/](agents/profiles/) holds reusable execution-profile presets for consuming repos.
- [pets/](pets/) holds reusable Codex-compatible pet packages and their runtime assets; use [Pet Package Guide](pets/README.md) for the package contract.
- [scripts/](scripts/) holds repository-level validation and maintenance tools; keep skill-local deterministic operations inside the owning skill package instead.
- [skills/](skills/) holds the reusable skill packages.
- [skills/skill-followups.md](skills/skill-followups.md) owns durable unresolved skill follow-up work across the repository; it is not a skill entry contract.
- Each skill package's `SKILL.md` is its entry contract.
- Within each skill package, `agents/` holds UI-facing skill metadata.
- Within each skill package, `references/` holds detailed method, logic, and validation material.
- Within each skill package, `templates/` holds output scaffolds.
- [agents/policies/](agents/policies/) holds shared harness and evaluation governance.

## Source Of Truth
- Keep `AGENTS.md` short and operational.
- Keep [README.md](README.md) as the overview and navigation doc for humans entering the repo.
- Keep shared harness and evaluation governance under [agents/policies/](agents/policies/) rather than scattering it across role files.
- Keep platform-neutral delegation rules under [agents/policies/](agents/policies/) and concrete runtime model bindings under [agents/adapters/](agents/adapters/).
- Keep the repository-wide skill acceptance bar in [Skill Quality Guide](skills/SKILL-QUALITY.md).
- Keep repository-wide package-name and named cross-skill-reference validation in [validate_skill_packages.py](scripts/validate_skill_packages.py); the quality guide remains normative, and other applicable static checks remain separate.
- Let each skill package own its own domain instructions; do not duplicate skill-local rules in `AGENTS.md`.

## Working Rules
- Prefer strengthening an existing skill contract over adding parallel guidance.
- Prefer strengthening the shared harness package over keeping divergent project-local copies once the shared version is proven stable.
- Follow [Skill Quality Guide](skills/SKILL-QUALITY.md) for package anatomy, file-role boundaries, evidence maturity, and distribution lifecycle.
- Prefer reusable rules over repo-specific examples unless a concrete example is necessary.
- When a skill changes, update nearby metadata, templates, and validation material if they became stale.
- After changing a skill package, run `python3 scripts/validate_skill_packages.py <skill-name>` plus applicable link, referenced-file, metadata, and resource checks; omit the name to validate every package.
- Do not create permanent by-product docs unless they have a clear durable owner.

## Documentation Rules
- Keep each doc responsible for one clear purpose.
- Use docs to define what a good skill looks like, not to restate every skill package.
- Prefer links and ownership pointers over repeated prose.
