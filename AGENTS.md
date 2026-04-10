# Repository Guidelines

## Purpose
- This repo stores reusable Codex skills.
- Each skill should be portable, checkable, and maintainable across projects.
- Optimize for strong contracts, clean file roles, and harness-friendly expansion.

## Codebase Map
- Scan the repo root before assuming structure.
- Each top-level folder is one skill package.
- `SKILL.md` is the entry contract for a skill.
- `agents/` holds UI-facing skill metadata.
- `references/` holds detailed method, logic, and validation material.
- `templates/` holds output scaffolds.
- `docs/` holds repo-level skill guidance and governance.

## Source Of Truth
- Keep `AGENTS.md` short and operational.
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

