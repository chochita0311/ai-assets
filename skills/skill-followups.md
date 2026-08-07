# Skill Follow-Ups

## Purpose
- Keep one shared place for later additions, refinements, and cross-skill follow-up work.
- Capture durable backlog items without scattering temporary notes across skill packages.
- Track future contract improvements separately from the current implementation pass.

## Current Follow-Ups

### Cross-skill
- Decide whether there should be one shared handoff vocabulary for `docs-structuring`, `docs-shaping`, and `refine-skill`.
- Revisit whether the repo wants a lightweight convention for cross-skill follow-up statuses such as `proposed`, `ready`, and `deferred`.
- Revisit whether every reusable skill should expose a minimal common contract surface:
  - explicit trigger boundary
  - explicit output location or output handling
  - explicit stopping point or downstream handoff

### Repository-wide skill quality
- Decide whether every reusable package should require `agents/openai.yaml`; it remains optional until supported target requirements justify a repository-wide mandate.
- Consider a dedicated skill adoption guide or automated sync tooling only after canonical-source transitions, target-specific file rules, and deletion behavior are agreed.
- Consider a shared benchmark suite only after comparable task corpora and risk-based forward-test thresholds exist.

### `maintain-context-freshness`
- After the next real `maintain` run:
  - verify that only approved content-state changes reach the smallest owning documents; finding IDs, ledger rows, and review, approval, or action status must remain session-only unless the user explicitly requests a named durable audit artifact
  - confirm that historical markers, `as-of` dates, successor links, and any condensation preserve unique content, provenance, and discoverability
- After the next archive or delete request:
  - verify that no operation occurs without the exact source and action, plus the exact archive destination when applicable
  - confirm that the session report distinguishes proposed, not applied, approved, and applied states plainly
- Confirm in fresh Codex and Claude sessions that the canonical symlinked package is discovered and can run standalone.
- Reopen refinement only when a real run exposes a repeatable contract failure or materially new domain case; record run-specific evidence outside the skill package.

## Notes
- Keep this file concise and durable.
- Record follow-ups that are likely to matter across sessions.
- Do not turn this file into a run log or a temporary scratchpad.
