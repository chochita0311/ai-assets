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

## Category Index

- [Layout Containment And Readability](#layout-containment-and-readability)
- [Information Hierarchy And Metric Meaning](#information-hierarchy-and-metric-meaning)
- [Boundary And Scope Discipline](#boundary-and-scope-discipline)
- [Typography, Alignment, And Accent Consistency](#typography-alignment-and-accent-consistency)
- [Card Metadata And Footer Structure](#card-metadata-and-footer-structure)
- [Stateful Navigation And Selection](#stateful-navigation-and-selection)
- [First-State And Viewport Checks](#first-state-and-viewport-checks)
- [Evaluation Evidence](#evaluation-evidence)
- [Classification Guidance](#classification-guidance)

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

#### Scrollable Disclosure Frame Integrity

- A bounded disclosure, menu, or popover with a long list should keep one stable outer frame for background, border, radius, shadow, and clipping.
- Vertical scrolling should normally belong to an inner content region so scrollbars and overflowing children do not erase, split, or square off the visible frame.
- Evaluators should inspect short, threshold, and long-list states and compare all four edges, corner radii, and overflow behavior.

#### Composite Record State Continuity

- A repeated record split into sibling interactive regions may use one continuous hover or focus-within surface so the regions still read as one record.
- Shared visual feedback must not merge distinct destinations or make non-clickable space advertise the wrong action.
- Optional child actions or disclosures should use a reserved or separately anchored utility layer so common metadata does not shift between otherwise equivalent records.
- A pressed or selected utility action may change its glyph, accessible state, or approved emphasis, but it should not resize its hit area, recolor an unrelated parent surface, or move sibling metadata.
- Evaluators should compare the full row tone, individual focus targets, pointer cursor, click boundaries, rows with and without optional children, and idle, hover, focus, and pressed states together.

#### Readability Before Density

- Browse surfaces must stay readable under realistic content length.
- When density rises, the system should preserve hierarchy and containment before adding more visible information.
- A visually compact layout that causes clipping, overlap, or scan breakdown is a failure, not a stylistic preference.

#### Long Technical Asset Containment

- Commands, code, schemas, diagrams, traces, and similarly wide technical assets must remain inside a bounded presentation region rather than widening the outer document.
- Choose the internal scrolling axis from the content shape, and keep the asset's label, purpose, and any essential instruction or action readable without requiring the user to traverse the full overflow region first.
- Evaluators should exercise representative maximum-length content at supported viewport boundaries and verify both that the asset remains keyboard- and touch-reachable without hover dependence and that the outer document does not acquire unintended overflow.
- Locate overflow ownership at the document, outer surface, reading body, generated wrapper, and leaf asset. Intentional horizontal overflow should belong to one bounded local owner; an equal document `clientWidth` and `scrollWidth` alone does not prove that intermediate cards or transformed leaves are contained.

#### Content-Triggered Rendering Evidence

- Technical prose, logs, paths, identifiers, URLs, stack traces, and code-like output must remain literal unless they unambiguously match an approved rich-content syntax. A punctuation pair such as dollar signs, brackets, backticks, angle brackets, or underscores must not silently convert unrelated text into math, links, emphasis, or another semantic element.
- A generic long string or lorem-ipsum fixture is not equivalent evidence for a content-triggered defect. Preserve the reported trigger's structural shape in a privacy-safe witness, including the relevant punctuation, indentation, line breaks, nesting, and unbroken-token behavior.
- Inspect the produced semantic DOM as well as the screenshot. Unexpected `math`, anchor, `pre`, `code`, table, or other generated elements can change sizing and accessibility even when the visible text initially looks plausible.
- After a correction, retain a deterministic regression at the lowest shared renderer or component that owns the trigger and render at least one representative consumer when the failure depends on browser layout.

#### Technical Canvas Control And Fallback Legibility

- Dense diagrams, maps, and other technical canvases should expose visible controls for supported navigation such as zoom, reset, or fit; a modifier gesture may accelerate the task but should not be the only discoverable path.
- Keep the control group, current scale or state, diagram legend, and canvas visually related without collapsing them into one ambiguous action cluster. Controls that depend on successful rendering should remain truthfully unavailable until the canvas is ready.
- Evaluators should compare wide and narrow layouts, long labels, disabled and bounded states, render failure, keyboard and touch reachability, and the non-interactive or textual fallback. Canvas navigation must not widen the outer document or make the fallback feel like an error residue.

#### Scrollable Table Frame And Fill

- A table that scrolls locally should keep overflow and outer frame ownership in a wrapper while retaining native table layout inside it. When columns are narrower than the reading region, header and row surfaces should fill that region instead of ending at intrinsic cell width.
- Evaluators should compare short or two-column tables with wide multi-column tables. Check the wrapper edge, table edge, final header-cell edge, border and radius continuity, local overflow, and outer-document overflow rather than accepting the presence of a scrollbar as sufficient evidence.
- If one renderer or table primitive serves several reading surfaces, apply [Shared Owner And Propagation Evidence](#shared-owner-and-propagation-evidence) instead of treating the reported document or route as the entire defect scope.

#### Technical Reading Surface Role Separation

- Code embedded in a reading surface does not automatically share the visual role of a terminal, Run console, status panel, brand accent, or provenance marker merely because both use monospace text.
- Evaluators should inspect whether background, border, label, default text, and syntax colors express sustained reading without borrowing semantic roles that imply execution or status. Dedicated semantic reading roles are preferable when existing console or feedback roles create the wrong meaning or an unnecessarily harsh tone.
- A visual reference may calibrate hierarchy, contrast, and palette variety, but it does not require importing the reference theme, decorative chrome, gradients, or shell. Compare generic and highlighted code across every shared reading consumer in scope.

### Information Hierarchy And Metric Meaning

#### Presentation Eligibility Is A Separate Contract

- Persisted evidence is not automatically eligible for a user-facing metric, rank, date range, or category row.
- Diagnostic, synthetic, fallback, or error records may remain valuable for traceability while being excluded from ordinary analytical presentation when they do not represent the measured concept.
- Evaluators should confirm that summary, history, composition, coverage, and linked counts use one coherent eligible set so an excluded record does not leak through a secondary consumer.

#### Secondary Metric Explanatory Burden

- A derived or supporting metric should earn its space by improving a decision or interpretation beyond the primary observed values.
- If a secondary value needs extensive qualification, provenance, coverage, state, and timestamp copy but still adds little practical value, removing it may preserve hierarchy better than explaining it more loudly.
- Evaluators should compare information value, false-precision risk, and explanatory burden before accepting another KPI block or repeated estimate.

#### Instructional Copy Entitlement And Redundancy

- Persistent helper or explanatory copy should earn its place by adding a consequence, decision boundary, validation rule, recovery path, or other information not already conveyed by the field label, status, control state, bounded preview, or nearby feedback.
- When a heading, badge, helper, preview, and validation region repeat the same fact, keep one clear owning explanation instead of distributing near-equivalent prose across the task. Optional setup should not appear required merely because its explanation is louder or repeated more often than the primary action; use the consuming repo's `interaction-evaluation.md` section `Optional Setup Must Not Become A Prerequisite` as the canonical interaction contract for required fields, validation, submission, and success conditions.
- When copy is removed, evaluators should confirm that required labels, errors, recovery guidance, and accessibility semantics remain discoverable and that the layout closes the vacated space without leaving a dead band or breaking responsive rhythm.

#### Adjacent Metric Denominator Clarity

- Adjacent totals, costs, counts, and activity metrics may legitimately use different eligible populations, but the layout and labels must not imply that they reconcile one-to-one.
- When one metric includes background or child activity while another counts only primary work, the distinction should be visible at the point of comparison or in a bounded trust explanation.
- Evaluators should inspect denominator definitions together with hierarchy and supporting copy rather than assuming shared placement means shared scope.

#### User-Facing Terminology Boundary And Consistency

- Internal storage, schema, or type names do not automatically own the user-facing vocabulary; visible labels should express the user's concept without requiring the internal contract to be renamed.
- Once a user-facing term is chosen, apply it consistently across summaries, details, empty or unavailable states, errors, trust or calculation explanations, and accessibility text, including singular, plural, and number formatting.
- Evaluators should confirm that nearby labels still distinguish the concept from adjacent records or events and that internal aliases do not leak through secondary presentation consumers.

#### Authority Region Separation

- A detail or inventory surface may combine externally observed facts, user-authored local memory, source evidence, organization state, execution history, and related context, but those authorities should not read as one interchangeable content block.
- Cached or last-known external facts must not visually imply a live read. Local notes or classifications must not look provider-owned, and evidence or execution status must not compete with the primary record as if it were current source content.
- A related or contextual item should state why it appears and where it came from; global proximity or recency alone should not look like an explained relationship.
- Evaluators should inspect fully populated, partially available, stale, failed, and secondary-panel error states together. Headings, provenance, timestamps, relationship reasons, status copy, and explicit external-navigation or refresh actions should make each authority and its update path understandable without relying on color alone.

#### Subject-Relative Relationship Evidence

- A relationship label should describe the observed evidence from the current record's perspective, not reuse an external resource title, transport name, parser label, or storage relation merely because that value is available.
- Distinguish direct evidence such as mention, lookup, attachment, or explicit reference from ambient coincidence such as a shared folder, workspace, tenant, or recent activity. Weak proximity should be omitted when it adds volume without helping the current task.
- Failed attempts may remain useful evidence, but they should be labeled as failed rather than presented as a successful relationship or silently removed from a group whose purpose includes traceability.
- When direct evidence is numerous, keep an intentionally bounded initial slice per semantic group, preserve the true total, and provide reversible disclosure. One noisy group should not consume the visibility budget of another.

#### Source Identity Cue Propagation And Redundancy

- A stable source identity should produce the same compact cue across inventory rows, pinned or saved views, detail headers, and parent-owned child rows. Derived child presentation should follow the owning record's source instead of falling back to a provider-wide default.
- Compact lettermarks, icons, and color accents require an accessible text identity; color alone must not distinguish sources that otherwise share a parser or visual family.
- Do not repeat a full provider or source label in every card, heading, badge, and child row when one nearby cue already establishes identity. Evaluators should remove redundant visible copy only after confirming that direct entry, mixed-source lists, assistive output, and narrow layouts remain understandable.

#### Independent State-Axis Legibility

- Content coverage, freshness, availability, attention, classification, and work organization are independent when the product contract says they can change separately. Do not compress them into one vague tracked, active, or synchronized treatment.
- Labels, badges, filters, and metadata order should let users distinguish meaningful combinations such as current reference-only content, stale indexed content, archived but recoverable content, or locally classified content with no work grouping.
- Evaluators should exercise cross-axis combinations and repeated visible identifiers from different source or tenant boundaries. Source identity and text labels must keep records distinguishable without assuming that one key, color, or status owns the whole record.

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
- A single golden screen may bootstrap later work only when it yields a stable design grammar.
- When later features require patterns the approved sources do not cover, record the gap as uncertainty and request additional source material instead of improvising.

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

#### Reference Geometry Uses Internal Insets

- When a control must match a reference, compare text-relative padding, content width, selected-surface bounds, and indicator position in addition to the outer width and height.
- Equal outer tracks can still fail parity when labels have different lengths or the reference sizes segments from their content.
- Evaluators should test short and long labels and measure the selected geometry rather than inferring parity from one shared minimum width.
- For controls with a disclosure indicator, including native selects, measure the selected-text reserve, indicator bounds, and indicator-to-edge inset as separate relationships. Verify that one indicator remains legible without duplication and that focus, disabled, invalid, compact, narrow, and touch states preserve the intended alignment.

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

### Stateful Navigation And Selection

#### Visible And Programmatic Selection Parity

- A visible active or selected treatment should have the matching programmatic current or selected state when the control represents navigation or selection; color or background treatment alone is not sufficient evidence.
- The current item should remain visibly reachable after navigation. In hierarchical surfaces, required ancestors should expose the item rather than leaving an active descendant hidden inside a collapsed group.
- Compact and narrow states should preserve the consuming product's approved target geometry, contrast, and readable state labels without forcing desktop density rules into touch-oriented layouts.
- Evaluators should compare visible selection, accessibility semantics, focus treatment, ancestor disclosure, and narrow-screen reachability as one state contract.

### First-State And Viewport Checks

#### First-State Surface Separation

- When a feature introduces a landing-first or overlay-first entry state inside an existing shell, the first-state surface should read as the primary canvas until the handoff completes.
- Downstream browse or read surfaces may remain technically mounted, but they should not visually compete so strongly that the first state feels like a weak layer floating over the real screen.
- Evaluators should inspect initial load, mid-transition, and handoff moments separately rather than judging only the static landing composition.

#### Viewport-Range Hero Anchor Stability

- When a hero or first-state surface intentionally anchors primary copy to a specific vertical band, that anchor should remain perceptually stable across common laptop and desktop viewport ranges rather than drifting because of mixed `vh` and `vw` tuning.
- Headline scale should also stay proportionate across those same ranges; smaller laptop widths should not make the same title feel meaningfully larger or heavier than intended when the surrounding shell typography remains stable.
- Evaluators should compare at least one narrower laptop-sized viewport and one wider desktop viewport and confirm both the copy position and headline scale still match the intended composition.

### Evaluation Evidence

#### Rendered State And Viewport Evidence

- Claims about geometry, overflow, contrast, selection visibility, focus, or responsive composition should use rendered evidence when those properties cannot be established from source inspection alone.
- Broad screen-family work should sample the consuming product's supported viewport boundaries and representative long-content, empty, unavailable, error, and active-interaction states. Exact widths and required states belong to the consuming product's contract.
- Record the effective viewport rendered by the page rather than assuming that a requested window size was applied exactly. Browser minimum-window constraints, device-pixel ratio, zoom, or tool clamping can change the observed width; use viewport or device emulation when needed to reach a required minimum boundary.
- Use synthetic or explicitly approved content when captures, fixtures, or audit artifacts could otherwise expose private runtime data.
- If the required rendered evidence cannot be collected, record the evidence gap explicitly and do not describe unobserved runtime behavior as a verified pass. The owning feature, active spec, or selected profile decides whether that gap blocks acceptance.

#### Shared Owner And Propagation Evidence

- A mismatch first observed in one record, route, or fixture may belong to a shared renderer, component, token, or layout primitive. Evaluators should identify that owning layer before describing the finding as instance-specific.
- When the owner is shared, evidence should include the reported exemplar plus representative peer content or consumer surfaces, including narrow and wide states when geometry is involved. A one-record patch is not sufficient evidence for a shared-owner defect.
- Record the propagation boundary explicitly: which consumers receive the correction, which remain intentionally outside it, and whether already mounted pages require reload or asset refresh before comparison.

#### Positive-State Suppression Evidence

- When a change removes, hides, or excludes previously eligible content, an empty fixture is not sufficient evidence that the presentation boundary works.
- Evaluators should exercise a positive producer or read-model state that would have rendered the content before the change and verify that the current consumer still suppresses it.
- When storage retention is intentional, evidence should confirm both sides of the boundary: the record remains inspectable at its owning layer and does not leak into the excluded presentation consumers.

## Classification Guidance

- Usually classify as `implementation bug` when the spec already requires stable containment or shell preservation.
- Usually classify as `spec gap` when the spec failed to define wrapping, truncation, breakpoint behavior, or shell-boundary expectations clearly enough.
- Classify as `planning gap` when the visual failure reveals that the approved feature boundary itself was wrong.
