# Repository Guidelines

## Purpose
- This repo stores reusable AI assets, including Codex skills.
- Each skill should remain portable, checkable, and maintainable across projects.
- Optimize for strong contracts, clean file roles, and harness-friendly expansion.
- Use `README.md` for the user-facing repository overview.

## Codebase Map
- Scan the repo root before assuming structure.
- `agents/` holds reusable harness roles, flows, operations, profiles, policies, and templates.
- `agents/templates/` holds shared planning and execution templates for consuming repos.
- `agents/profiles/` holds reusable execution-profile presets for consuming repos.
- `skills/` holds the reusable skill packages.
- `SKILL.md` is the entry contract for a skill.
- Within each skill package, `agents/` holds UI-facing skill metadata.
- Within each skill package, `references/` holds detailed method, logic, and validation material.
- Within each skill package, `templates/` holds output scaffolds.
- `agents/policies/` holds the shared harness governance package.

## Source Of Truth
- Keep `AGENTS.md` short and operational.
- Keep `README.md` as the overview and navigation doc for humans entering the repo.
- Keep shared harness governance under `agents/policies/` and keep skill-specific quality rules under `skills/`.
- Keep shared harness and evaluation governance in `agents/policies/` rather than scattering it across role files.

- Let each skill package own its own domain instructions; do not duplicate skill-local rules in `AGENTS.md`.

## Working Rules
- Prefer strengthening an existing skill contract over adding parallel guidance.
- Prefer strengthening the shared harness package over keeping divergent project-local copies once the shared version is proven stable.
- Preserve clear separation between:
  - `SKILL.md` for trigger/scope/output contract
  - `references/method.md` for procedure and decision logic
  - `references/checklist.md` for pass/fail validation
- Prefer reusable rules over repo-specific examples unless a concrete example is necessary.
- When a skill changes, update nearby metadata, templates, and validation material if they became stale.
- Do not create permanent by-product docs unless they have a clear durable owner.

## Documentation Rules
- Keep each doc responsible for one clear purpose.
- Use docs to define what a good skill looks like, not to restate every skill package.
- Prefer links and ownership pointers over repeated prose.
