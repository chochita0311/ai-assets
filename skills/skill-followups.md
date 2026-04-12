# Skill Follow-Ups

## Purpose
- Keep one shared place for later additions, refinements, and cross-skill follow-up work.
- Capture durable backlog items without scattering temporary notes across skill packages.
- Track future contract improvements separately from the current implementation pass.

## Current Follow-Ups

### Cross-skill
- Decide whether there should be one shared handoff vocabulary for `docs-structuring`, `docs-shaping`, and `refine-skill`.
- Revisit whether the repo wants a lightweight convention for cross-skill follow-up statuses such as `proposed`, `ready`, and `deferred`.
- Evaluate whether skill-discovery docs should point to this file explicitly or keep it as a maintainer-only backlog.
- Revisit whether every reusable skill should expose a minimal common contract surface:
  - explicit trigger boundary
  - explicit output location or output handling
  - explicit stopping point or downstream handoff

### Skill-specific
- `init-serena`:
  - add a minimal trigger and output contract so the skill is not just a workflow stub
  - state what must be reported back after activation, onboarding check, and initial instruction load
- `design-plan`:
  - add explicit source-priority guidance for constitution, current screens, and user direction
  - add a clearer stop/handoff boundary so design planning does not drift into constitution rewriting or implementation work
- `refactor-plan`:
  - add a shorter trigger/do-not-use summary near the top so the skill boundary is visible before the long workflow
  - evaluate whether the plan/log output lifecycle should be stated more explicitly for temporary versus durable planning artifacts
- `docs-structuring`:
  - evaluate whether it should state its default operating mode more explicitly when both incremental cleanup and larger restructure are possible
  - evaluate whether a short approval-boundary summary should appear earlier in `SKILL.md`, not only in deeper references

## Notes
- Keep this file concise and durable.
- Record follow-ups that are likely to matter across sessions.
- Do not turn this file into a run log or a temporary scratchpad.
