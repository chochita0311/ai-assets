# Design Evaluation

## Purpose

- Keep reusable design-evaluation assets derived from real review history.
- Preserve concrete evaluator rules that should be applied again in future features.
- Strengthen design review consistency without forcing every rule into the full design constitution.

## Ownership

- This document owns reusable design-evaluation checks and cautions.
- In a consuming repo, use `docs/agents/roles/design-evaluator.md` for the role contract.
- Use the consuming repo's design constitution or design policy for broader durable design law when one exists.
- Use the consuming repo's design-document governance when it defines how visual rules are promoted.

## Use

- Apply these notes when evaluating visible implementation work.
- Add new entries when the same class of design failure proves reusable beyond one feature.
- Promote an entry into the constitution only when it becomes a broader product-wide visual law.

## Reusable Evaluation Notes

### Layout Containment And Readability

#### Card Content Containment

- Text must not escape card bounds.
- Tags must wrap or truncate without spilling outside the card.
- Metadata and footer content must remain contained inside the card.
- Long titles, dense tags, or narrow widths must not break the card box.

#### Breakpoint Containment Stability

- Grid cards must preserve containment across supported breakpoints.
- Responsive column changes must not cause content overlap, spill, or collapse.
- A layout that works only at one width is not a pass.

#### Readability Before Density

- Browse surfaces must stay readable under realistic content length.
- When density rises, the system should preserve hierarchy and containment before adding more visible information.
- A visually compact layout that causes clipping, overlap, or scan breakdown is a failure, not a stylistic preference.

### Boundary And Scope Discipline

#### Shell Boundary Preservation

- Visual inspiration from a source artifact must not override the current approved shell boundaries.
- When a feature is scoped to one surface, unchanged shell regions must remain visually intact unless the approved feature explicitly includes them.
- Local surface redesign must not quietly restyle the left, top, or bottom shell.

#### Shell Handoff Visual Continuity

- When navigation changes the active surface while keeping a shared shell, evaluate outgoing, mid-handoff, incoming, and settled frames separately.
- Persistent shell regions such as topbars, sidebars, reserved action slots, and search areas should not visibly jump, resize, or disappear unless the feature intentionally stages that change.
- If a control is hidden on one surface, preserve or intentionally animate its layout footprint when removing it would make the shell feel reloaded instead of continuous.

#### Source-Use Discipline

- A source artifact may guide layout direction inside the approved surface.
- A source artifact must not justify importing new controls, data, or shell behavior that the approved feature did not include.
- Visual borrowing is valid only inside the approved boundary.

#### Single Boundary Ownership

- When two stacked surfaces meet, only one of them should own the boundary line unless a double-divider effect is explicitly intended.
- Repeated items may keep internal separators, but the final item before a footer or next section should usually drop its divider if the following surface already provides the section boundary.
- Evaluators should check last-item states, pagination edges, and empty states rather than validating only repeated middle items.

### Typography, Alignment, And Accent Consistency

#### Font Source And Fallback Evidence

- When a feature changes a webfont or type stack, evaluators should confirm both the declared CSS stack and the actual loaded font assets.
- Self-hosted display fonts should include source and license evidence near the committed assets; missing evidence is a design-system risk, not only a repository hygiene issue.
- Fallback stacks should be intentionally short enough to maintain readability while still covering expected language scripts and failed webfont loading.

#### Font Weight Token Semantics

- Font-weight tokens should be named for the weight they actually represent, such as regular, semibold, or extrabold.
- If a token named `medium` resolves to normal text weight or a token named `bold` resolves to semibold, evaluators should flag the naming drift because future UI tuning becomes harder to reason about.
- Compact navigation and label surfaces should be compared by role before applying one global weight; top navigation, sidebar labels, tag chips, counts, and metadata may need different thickness even at the same font size.

#### Topbar Parity Drift Check

- When matching or preserving an existing topbar, evaluators should compare typography and spacing tokens before comparing copy or menu structure.
- Visual drift often appears first in `font-size`, `line-height`, `letter-spacing`, and reserved icon spacing rather than in the text labels themselves.
- Hidden or conditional icons must not leave idle-state spacing that makes one navigation item look wider or visually misaligned than its peers.

#### Conditional Topbar Affordance Parity

- Topbar items that sometimes own dropdowns, icons, or active states should still read as the same navigation family across surfaces.
- If a surface suppresses a dropdown, the hover and focus styling should match plain navigation items and should not leak reserved icon spacing or disclosure affordance.
- Evaluators should compare both idle and hovered states on each surface, including route-entry hold states.

#### Small Text Role Legibility

- Small navigation, metadata labels, sidebar captions, and footer copy may share a font size only when their weight, letter spacing, and contrast still match their role.
- A 12 px label can pass for compact metadata or navigation, but evaluators should check that it does not become too heavy, too faint, or visually dominant compared with adjacent body text.
- Size normalization should use durable component classes or tokens rather than one-off selector overrides that make future typography changes brittle.

#### Small Accent Token Consistency

- Small accent surfaces such as category labels, chips, and compact action buttons should stay inside the approved token family before introducing custom in-between hex values.
- When tone tuning is needed, prefer existing foreground and container tokens that already belong to the active palette over ad hoc near-matches.
- Evaluators should compare compact accents against nearby chips, labels, and control states to catch subtle tonal drift that makes the interface feel less system-driven.

### Card Metadata And Footer Structure

#### Card Footer Baseline Consistency

- Repeated cards in the same grid should keep footer metadata on the same visual levels even when title or summary length differs.
- Tag rows, collection labels, dates, or similar footer metadata must align card-to-card instead of drifting with content height.
- If footer content belongs to a fixed metadata zone, that zone should be anchored to the card box rather than to the variable text block above it.

#### Metadata Layer Separation

- Distinct metadata layers inside a compact card should not visually occupy the same horizontal band.
- Tag chips and collection or locator labels should read as separate rows or clearly separated zones, not as partially overlapping content.
- Evaluators should check long-content cases, multi-tag cases, and short-summary cases to confirm the metadata hierarchy still reads cleanly.

#### Footer Control Row Separation

- Footer control rows and footer credit or attribution rows should be evaluated as separate information layers when they serve different purposes.
- Pagination, page-size, page labels, or similar active controls should not be compressed into the same visual row as passive credit text if that reduces scan clarity.
- Evaluators should confirm that row separation remains readable across desktop and smaller breakpoints.

#### Width-Based Title Truncation Consistency

- In repeated card grids, title truncation should respond to real card width rather than to the longest content in the dataset.
- Short titles should keep their natural width, while long titles should truncate cleanly with ellipsis once they exceed the available title band.
- Evaluators should check mixed-length title sets to confirm the title row reads as one consistent horizontal band across the grid.

#### Overflow Metadata Reveal Shape

- Hover or focus disclosure for overflow metadata should preserve the compact default card while revealing hidden items in a readable expanded panel.
- The expanded panel should align to its trigger in a predictable direction and should not imply a different disclosure direction than the control actually uses.
- Hidden metadata chips shown in the disclosure should size to their own content unless a stronger system rule explicitly requires uniform widths.

### First-State And Viewport Checks

#### First-State Surface Separation

- When a feature introduces a landing-first or overlay-first entry state inside an existing shell, the first-state surface should read as the primary canvas until the handoff completes.
- Downstream browse or read surfaces may remain technically mounted, but they should not visually compete so strongly that the first state feels like a weak layer floating over the real screen.
- Evaluators should inspect initial load, mid-transition, and handoff moments separately rather than judging only the static landing composition.

#### Viewport-Range Hero Anchor Stability

- When a hero or first-state surface intentionally anchors primary copy to a specific vertical band, that anchor should remain perceptually stable across common laptop and desktop viewport ranges rather than drifting because of mixed `vh` and `vw` tuning.
- Headline scale should also stay proportionate across those same ranges; smaller laptop widths should not make the same title feel meaningfully larger or heavier than intended when the surrounding shell typography remains stable.
- Evaluators should compare at least one narrower laptop-sized viewport and one wider desktop viewport and confirm both the copy position and headline scale still match the intended composition.

## Classification Guidance

- Usually classify as `implementation bug` when the spec already requires stable containment or shell preservation.
- Usually classify as `spec gap` when the spec failed to define wrapping, truncation, breakpoint behavior, or shell-boundary expectations clearly enough.
- Classify as `planning gap` when the visual failure reveals that the approved feature boundary itself was wrong.
