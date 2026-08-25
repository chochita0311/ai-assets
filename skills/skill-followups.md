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
- Build one privacy-safe reusable semantic fixture corpus from the adjudicated behavior-removal, security, cross-boundary consumer-frontier, mixed managed-and-vendored dependency-selection, legitimate-zero, and hard-duplicate cases.
  - Run blinded matched self-review versus fresh-review and latency-first versus quality-first evaluations without revealing expected findings.
  - Score material-finding recall, duplicate and false-positive control, and whether the structured receipt distinguishes a supported zero-material-finding result from a hollow summary.
  - On comparable fixtures, verify that `focused` emits no review notes, `balanced` keeps low-severity observations out of inline threads, and explicitly selected `assertive` permits only anchored high-confidence non-blocking low suggestions, without lowering semantic depth or increasing speculative noise.
- Only when the user explicitly authorizes each relevant write in that turn, complete controlled schema-v2 live checks on github.com and the current corporate GHES.
  - Publish one safe test review on each host and inspect the two-column receipt, conditional warning with one bullet per gap, blank-line hierarchy, linearized plain-text reading order, restrained `✅` semantics, and always-expanded evidence visually and with assistive-technology-oriented inspection.
  - Verify that an explicit publish request creates exactly one review and that an exact same-snapshot rerun returns `noop-existing-snapshot`.
  - Verify that a newly confirmed finding or summary-count change on an already reviewed same snapshot returns a corrected draft without writing or bypassing the snapshot guard.
  - Forward-test `reply` after the PR head advances; the result must distinguish the original review head from the current head and stop on a preparation-time race.

## Notes
- Keep this file concise and durable.
- Record follow-ups that are likely to matter across sessions.
- Do not turn this file into a run log or a temporary scratchpad.
