# Design Evaluation

## Purpose
- Keep reusable design-evaluation assets derived from real review history.
- Preserve concrete evaluator rules that should be applied again in future features.
- Strengthen design review consistency without forcing every rule into the full design constitution.

## Ownership
- This document owns reusable design-evaluation checks and cautions.
- Use [design-evaluator.md](../../role/design-evaluator.md) for the role contract.
- Use [design-constitution.md](./design-constitution.md) for broader durable design law.
- Use [design-document-governance.md](./design-document-governance.md) for document hierarchy.

## Use
- Apply these notes when evaluating visible implementation work.
- Add new entries when the same class of design failure proves reusable beyond one feature.
- Promote an entry into the constitution only when it becomes a broader product-wide visual law.

## Reusable Evaluation Notes

### 1. Card Content Containment
- Text must not escape card bounds.
- Tags must wrap or truncate without spilling outside the card.
- Metadata and footer content must remain contained inside the card.
- Long titles, dense tags, or narrow widths must not break the card box.

### 2. Breakpoint Containment Stability
- Grid cards must preserve containment across supported breakpoints.
- Responsive column changes must not cause content overlap, spill, or collapse.
- A layout that works only at one width is not a pass.

### 3. Shell Boundary Preservation
- Visual inspiration from a source artifact must not override the current approved shell boundaries.
- When a feature is scoped to one surface, unchanged shell regions must remain visually intact unless the approved feature explicitly includes them.
- Local surface redesign must not quietly restyle the left, top, or bottom shell.

### 4. Source-Use Discipline
- A source artifact may guide layout direction inside the approved surface.
- A source artifact must not justify importing new controls, data, or shell behavior that the approved feature did not include.
- Visual borrowing is valid only inside the approved boundary.

### 5. Readability Before Density
- Browse surfaces must stay readable under realistic content length.
- When density rises, the system should preserve hierarchy and containment before adding more visible information.
- A visually compact layout that causes clipping, overlap, or scan breakdown is a failure, not a stylistic preference.

### 6. Topbar Parity Drift Check
- When matching or preserving an existing topbar, evaluators should compare typography and spacing tokens before comparing copy or menu structure.
- Visual drift often appears first in `font-size`, `line-height`, `letter-spacing`, and reserved icon spacing rather than in the text labels themselves.
- Hidden or conditional icons must not leave idle-state spacing that makes one navigation item look wider or visually misaligned than its peers.

### 7. Card Footer Baseline Consistency
- Repeated cards in the same grid should keep footer metadata on the same visual levels even when title or summary length differs.
- Tag rows, collection labels, dates, or similar footer metadata must align card-to-card instead of drifting with content height.
- If footer content belongs to a fixed metadata zone, that zone should be anchored to the card box rather than to the variable text block above it.

### 8. Metadata Layer Separation
- Distinct metadata layers inside a compact card should not visually occupy the same horizontal band.
- Tag chips and collection or locator labels should read as separate rows or clearly separated zones, not as partially overlapping content.
- Evaluators should check long-content cases, multi-tag cases, and short-summary cases to confirm the metadata hierarchy still reads cleanly.

### 9. Single Boundary Ownership
- When two stacked surfaces meet, only one of them should own the boundary line unless a double-divider effect is explicitly intended.
- Repeated items may keep internal separators, but the final item before a footer or next section should usually drop its divider if the following surface already provides the section boundary.
- Evaluators should check last-item states, pagination edges, and empty states rather than validating only repeated middle items.

### 10. Small Accent Token Consistency
- Small accent surfaces such as category labels, chips, and compact action buttons should stay inside the approved token family before introducing custom in-between hex values.
- When tone tuning is needed, prefer existing foreground and container tokens that already belong to the active palette over ad hoc near-matches.
- Evaluators should compare compact accents against nearby chips, labels, and control states to catch subtle tonal drift that makes the interface feel less system-driven.

## Classification Guidance
- Usually classify as `implementation bug` when the spec already requires stable containment or shell preservation.
- Usually classify as `spec gap` when the spec failed to define wrapping, truncation, breakpoint behavior, or shell-boundary expectations clearly enough.
- Classify as `planning gap` when the visual failure reveals that the approved feature boundary itself was wrong.
