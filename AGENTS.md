# Repository Guidelines

## Purpose
- This repo stores reusable AI assets, including Codex skills.
- Each skill should remain portable, checkable, and maintainable across projects.
- Optimize for strong contracts, clean file roles, and harness-friendly expansion.
- Use `README.md` for the user-facing repository overview.

## Codebase Map
- Scan the repo root before assuming structure.
- `agents/` holds reusable top-level agent role contracts.
- `agents/templates/` holds reusable PRD and feature templates for consuming repos.
- `skills/` holds the reusable skill packages.
- `SKILL.md` is the entry contract for a skill.
- Within each skill package, `agents/` holds UI-facing skill metadata.
- Within each skill package, `references/` holds detailed method, logic, and validation material.
- Within each skill package, `templates/` holds output scaffolds.
- `docs/` holds repo-level skill guidance and governance.

## Source Of Truth
- Keep `AGENTS.md` short and operational.
- Keep `README.md` as the overview and navigation doc for humans entering the repo.
- Keep durable repo-level guidance under `docs/policies/`.
- Keep future tracking or planning docs under `docs/plans/` if this repo later needs them.
- Let each skill package own its own domain instructions; do not duplicate skill-local rules in `AGENTS.md`.

## Working Rules
- Prefer strengthening an existing skill contract over adding parallel guidance.
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
