# Skill Follow-Ups

## Purpose
- Keep one shared place for later additions, refinements, and cross-skill follow-up work.
- Capture durable backlog items without scattering temporary notes across skill packages.
- Track future contract improvements separately from the current implementation pass.
- Keep only unresolved work; remove an item after it is implemented or deliberately closed and rely on Git history for resolution history.

## Current Follow-Ups

### Repository-wide skill quality
- Define a skill-specific adoption, synchronization, and removal contract before automating installation. Cover canonical symlinks versus copied targets, Codex and Claude discovery paths, target-specific metadata, pre-existing paths, cache refresh, and safe unlink behavior.
- Consider a shared benchmark suite only after at least two skill families have reusable, privacy-safe task corpora and comparable pass/fail contracts; keep forward-tests skill-local until then.

### `maintain-context-freshness`
- Repeat `maintain` in an independent post-creation run:
  - verify that only approved content-state changes reach the smallest owning documents; finding IDs, ledger rows, and review, approval, or action status must remain session-only unless the user explicitly requests a named durable audit artifact
  - confirm that historical markers, `as-of` dates, successor links, and any condensation preserve unique content, provenance, and discoverability
- After the next real user-requested archive or delete operation:
  - verify that no operation occurs without the exact source and action, plus the exact archive destination when applicable
  - confirm that the session report distinguishes proposed, not applied, approved, and applied states plainly
- Confirm in a fresh Claude session that the canonical symlinked package is discovered and can complete one standalone audit or maintain run.

### `gh-review-pr`
- Decide and test the same-snapshot amendment contract for a submitted skill-owned review when the user requests a summary replacement or a newly verified inline finding. If GitHub cannot amend it atomically, define the safe stop and handoff instead of permitting ad hoc standalone writes.
- Repeat `draft` mode with findings and require publish-ready metadata for every proposed thread: `finding_id`, path, line, side, severity, confidence, disposition, and category. Tighten the draft output contract if omission repeats.
- Complete a real fresh-snapshot `publish` run with at least one inline finding through the bundled transaction, then rerun the exact snapshot to verify duplicate no-op behavior.
- Run matched `draft` reruns against the same frozen snapshots across intended harness and model combinations—at least one security-sensitive PR and one ordinary PR—to distinguish model variance from a reusable review-criteria gap before changing severity or security rules.
- Forward-test an unavailable named-worker case and confirm that evidence collection returns to the primary agent without generic-worker substitution or weakened publication gates.

## Notes
- Keep this file concise and durable.
- Record follow-ups that are likely to matter across sessions.
- Do not turn this file into a run log or a temporary scratchpad.
