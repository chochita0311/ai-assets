---
name: screen-alignment
description: Use when a current screen must stay visually consistent with an existing design system, either by matching a target screen closely or by extending the current screen under a design constitution or durable style rules without introducing foreign visual drift.
---

# Screen Alignment

Use this skill when the task is to keep a current implementation visually aligned with an existing design system.

## Quick Mode Map

- Use `match` when the target is the visual contract.
- Use `adapt` when the target is directional, but current content and constitution stay primary.
- Use `extend` when extending current system behavior with no exact target.
- Use `reframe` when target and constitution are structurally incompatible.

## Use This Skill When

- a current screen exists in code
- a target screen exists as mockup, screenshot, static HTML, styleguide page, or published page
- the user says the implementation is close but visually degraded
- a refactor preserved behavior but changed visual fidelity
- a design constitution exists and should constrain drift
- the user wants to evolve a page while preserving current design language

## Do Not Use This Skill When

- the task is open-ended redesign
- the user explicitly wants a new visual language
- the work requires constitution revision and no constitution-preserving option is acceptable

## Invocation Examples

- `Use $screen-alignment to turn this exported Stitch page into a repo-native page. Keep only useful structure and resolve styling through the current design constitution.`
- `Use $screen-alignment in extend mode. Preserve topbar and sidebar, and rebuild only the main content area so it feels native.`
- `Use $screen-alignment in adapt mode. Borrow layout direction from target detail view but keep current shell, tokens, spacing rhythm, and component language.`
- `Use $screen-alignment to compare current index and target detail page, then resolve conflicts in favor of the current constitution.`

## Order Of Authority

Use the authority order for the selected mode unless project rules override it.

For `match`:

1. design constitution or durable design rules
2. task target screen
3. current implementation screen
4. related family screens as supporting context

For `adapt`:

1. design constitution or durable design rules
2. current implementation screen
3. current product truth: real content model, available fields, supported behavior, and frozen user-scoped regions
4. task target screen as directional reference
5. related family screens as supporting context

For `extend`:

1. design constitution or durable design rules
2. current implementation screen
3. related family screens
4. optional references, sketches, or examples

For `reframe`:

- do not force a normal authority stack
- stop and redefine the task before implementation continues

If target conflicts with constitution, do not silently copy target styling. Preserve constitution unless the user explicitly requests constitution revision.

## Required Operating Rules

1. Treat current screen, target screen, and constitution as separate inputs.
2. Classify mode explicitly before editing: `match`, `adapt`, `extend`, or `reframe`.
3. Compare rendered screens, not code alone.
4. Build a concrete mismatch or consistency list before broad edits.
5. Fix narrow mismatch groups one pass at a time and verify after each pass.
6. Prefer literal visual matching in `match` when target values are clear.
7. Prefer native family consistency in `extend`.
8. In `adapt`, borrow direction without importing foreign system assumptions.
9. If the user freezes specific regions or shell areas, preserve those regions literally or omit them from the adaptation artifact rather than reconstructing them loosely.
10. In `adapt`, preserve the current repo's real content model, available fields, supported behavior, interaction contract, and actual content instances; do not invent or replace controls, metadata, note data, stateful workflows, or content slots based only on the target sketch.
11. Keep constitution-critical controls discoverable (for example search and primary navigation).
12. In constitution-preserving work, prefer existing shared style/component layers before page-local styling.
13. If local-only overrides are unavoidable, mark them explicitly as temporary and isolate them for clean removal.
14. Avoid AI-assistant or profile framing cues in archive shell composition unless the constitution explicitly allows them.
15. Remove temporary screenshots, metrics, and parity-check by-products before closing.

## Common Failure Modes

- copying embedded target design systems, utility classes, or token layers into a constitution-preserving repo
- keeping target shell styling when current shell is supposed to persist
- letting generated page rhythm or surface model override constitutional styling
- rebuilding frozen or out-of-scope regions loosely instead of preserving them literally or excluding them from the adaptation artifact
- letting a pilot or AI-generated target introduce data fields, controls, or metadata that do not exist in the current repo's real content model
- letting a pilot or AI-generated target introduce unsupported interactions, workflows, or stateful controls that the current repo does not actually implement
- letting a pilot or AI-generated target replace current repo note titles, excerpts, tags, or other real content with sketch copy
- silently hiding constitution-critical controls during extension or adaptation
- introducing raw spacing, radius, color, or motion values when existing token families should be used
- treating target export code as production-ready instead of separating reusable structure from foreign styling assumptions
- treating structurally foreign redesign work as normal parity work

## Workflow

- Read [references/method.md](./references/method.md) for full mode contracts, compatibility judgment, rendered comparison, browser verification, and failure diagnosis.
- Use [references/checklist.md](./references/checklist.md) as final closure validation.

## Optional Tool Integration

Browser automation is optional. Use it when rendered comparison, screenshot capture, computed-style inspection, or repeatable geometry verification is required. Keep setup and browser-level procedure in [references/method.md](./references/method.md).

## Expected Result

A successful pass should:

- make current screen read materially closer to target when a target exists
- keep new or revised areas native when no exact target exists
- preserve constitutional rules and avoid accidental redesign
- leave no temporary parity-inspection debris behind
