---
name: screen-alignment
description: Use when a current screen must stay visually consistent with an existing design system, either by matching a target screen closely or by extending the current screen under a design constitution or durable style rules without introducing foreign visual drift.
---

# Screen Alignment

Use this skill when the task is to keep a current implementation visually aligned with an existing design system.

This skill supports four modes:

1. `match`
Match a specific target screen as literally as possible without violating durable design rules.

2. `adapt`
Use a target as directional input while preserving current product contents, constitution, and core screen family.

3. `extend`
Add or revise screen areas when no exact target exists, while keeping results native to the current constitution and family patterns.

4. `reframe`
Stop parity work when the request is actually redesign or constitution-revision work.

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

## Mode Contracts

### `match`

Inputs:

- current screen
- target screen
- constitution, if it exists
- user screenshots or marked comparisons, when available

Output expectation:

- current screen reads materially closer to target
- constitutional rules are still honored

### `adapt`

Inputs:

- current screen
- target screen
- constitution
- explicit preservation constraints from user
- related family screens, when useful

Output expectation:

- directional qualities from target are borrowed intentionally
- current content, sourcing model, supported behavior, and screen family remain honest
- no target-only fields or controls are added unless the current repo actually supports them
- no target-only interactions, workflows, or stateful controls are added unless the current repo actually supports them
- current repo content instances are preserved unless the user explicitly asks to rewrite content or map to a different dataset
- target is directional input, not literal copy contract

### `extend`

Inputs:

- current screen
- constitution
- related family screens
- user direction for new area or behavior

Output expectation:

- new or revised areas read native to the existing system
- no foreign component language or visual drift is introduced

### `reframe`

Use when parity cannot be honest because target and constitution are too far apart.

Typical signs:

- different product framing rather than same screen family
- materially different navigation model
- materially different visual language
- change requires constitution revision to be coherent

Output expectation:

- task is explicitly reframed as redesign, constitution revision, or narrower constitution-preserving adaptation before implementation continues

## Workflow

- Read [references/method.md](./references/method.md) before substantial parity work.
- Use [references/checklist.md](./references/checklist.md) as final closure validation.

## Optional Tool Integration

Browser automation is optional. Use it when rendered comparison, screenshot capture, or computed-style verification is required.

### Playwright MCP (Optional)

Codex MCP integration file:
`~/.codex/config.toml`

Example:

```toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]
```

Use Playwright selectively for:

- opening current and target screens
- taking comparison screenshots
- checking computed styles
- validating geometry (width, height, spacing, radius)
- verifying that narrow parity edits landed

## Expected Result

A successful pass should:

- make current screen read materially closer to target when a target exists
- keep new or revised areas native when no exact target exists
- preserve constitutional rules and avoid accidental redesign
- leave no temporary parity-inspection debris behind
