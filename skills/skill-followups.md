# Skill Follow-Ups

## Purpose
- Keep one shared place for later additions, refinements, and cross-skill follow-up work.
- Capture durable backlog items without scattering temporary notes across skill packages.
- Track future contract improvements separately from the current implementation pass.
- Keep only unresolved work; remove an item after it is implemented or deliberately closed and rely on Git history for resolution history.

## Current Follow-Ups

### [Repository-wide skill quality](SKILL-QUALITY.md)
- Define a skill-specific adoption, synchronization, and removal contract before automating installation. Cover canonical symlinks versus copied targets, Codex and Claude discovery paths, target-specific metadata, pre-existing paths, cache refresh, and safe unlink behavior.
- Consider a shared benchmark suite only after at least two skill families have reusable, privacy-safe task corpora and comparable pass/fail contracts; keep forward-tests skill-local until then.

### [`maintain-context-freshness`](maintain-context-freshness/SKILL.md)
- Repeat `maintain` in an independent post-creation run:
  - verify that only approved content-state changes reach the smallest owning documents; finding IDs, ledger rows, and review, approval, or action status must remain session-only unless the user explicitly requests a named durable audit artifact
  - confirm that historical markers, `as-of` dates, successor links, and any condensation preserve unique content, provenance, and discoverability
- After the next real user-requested archive or delete operation:
  - verify that no operation occurs without the exact source and action, plus the exact archive destination when applicable
  - confirm that the session report distinguishes proposed, not applied, approved, and applied states plainly
- Confirm in a fresh Claude session that the canonical symlinked package is discovered and can complete one standalone audit or maintain run.

### [`gh-review-pr`](gh-review-pr/SKILL.md)
- Forward-test the documented same-snapshot omission safe stop against a submitted skill-owned review: verify that a newly verified inline finding or summary-count change returns a corrected draft without mutating GitHub or bypassing the snapshot guard.
- Rerun an exactly published snapshot through the bundled transaction to verify `noop-existing-snapshot` behavior in a real session; unit coverage exists, but the live duplicate no-op remains unproven.
- Forward-test `reply` on a submitted skill-owned finding after the PR head advances, and verify that the result distinguishes the original review head from the current head without permitting a preparation-time race.
- Convert the adjudicated behavior-removal, security, and cross-boundary consumer-frontier cases into privacy-safe semantic fixtures; add a legitimate zero-finding control; then run matched self-review versus fresh-review and latency-first versus quality-first evaluations without revealing the expected findings.
- Forward-test an unavailable named-worker case and confirm that evidence collection returns to the primary agent without generic-worker substitution or weakened publication gates.

## Notes
- Keep this file concise and durable.
- Record follow-ups that are likely to matter across sessions.
- Do not turn this file into a run log or a temporary scratchpad.
