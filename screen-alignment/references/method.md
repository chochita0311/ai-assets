# Screen Alignment Method

## Goal

Keep a current implementation visually aligned with an existing design system without silently redesigning it.

This method supports four modes:

1. `match`
2. `adapt`
3. `extend`
4. `reframe`

Authority is mode-specific:

- `match`: constitution -> target -> current -> family
- `adapt`: constitution -> current -> current product truth -> target -> family
- `extend`: constitution -> current -> family -> optional references
- `reframe`: stop and redefine instead of forcing a normal precedence order

## Step 0: Select The Mode

Choose one mode before substantial edits.

Use `match` when:

- there is a specific screen to match
- user intent is direct current-versus-target comparison
- screenshots or overlays show visible drift

Use `adapt` when:

- a target exists
- user wants movement toward target
- user also wants to preserve current content, sourcing model, and constitution
- target may be only a sketch, pilot, or generated direction source rather than a trustworthy data contract

Use `extend` when:

- user wants to add or revise a screen area
- no exact target controls the change
- the primary requirement is native consistency with current family

Use `reframe` when:

- target would materially change product framing or screen family
- target uses a different visual language than constitution
- honest matching would require constitution revision
- request is functionally redesign phrased as parity

If work mixes intents, run in order:

1. restore parity in stable existing area
2. extend under constitution

If no honest alignment/adaptation path exists, stop and mark `reframe`.

## Step 1: Read Constitution First

If constitution exists, extract:

- locked tokens and primitives
- locked hierarchy and component behavior
- forbidden drift
- flexible or unresolved areas

If constitution does not exist:

- in `match`, target becomes temporary visual truth for the task
- in `adapt` and `extend`, current implementation and family behavior stay primary unless the user explicitly reframes the work

## Step 1.5: Compatibility Judgment

Before mismatch lists, decide if target is compatible with constitution and current screen family.

Ask:

- Is this the same family, just expressed better?
- Does target preserve core hierarchy and interaction model?
- Would matching target keep constitution honest?
- Is this alignment work or redesign disguised as parity?

Decision outcomes:

- `match`: compatible and should be matched closely
- `adapt`: useful direction, not literal copy contract
- `extend`: no single target governs, extend natively
- `reframe`: redesign/constitution revision must be clarified first

## Step 2: Collect Rendered Reference Surface

Do not rely on memory.

For `match`, inspect:

- target screen
- current screen
- live screen when useful
- user-marked screenshots, if available

For `adapt`, inspect:

- current screen
- target screen
- constitution
- explicit preservation constraints
- related family screens when useful
- current repo data model, currently implemented content fields, supported interactions, and actual content currently shown on the screen

If the user froze regions explicitly, record those regions as no-change scope before building mismatch lists.

For `extend`, inspect:

- current screen
- constitution
- related family screens
- user examples, sketches, or partial references

For `reframe`, inspect only enough to explain conflict clearly.

## Step 3: Inspect Target Or Family Pattern

In `match` and `adapt`, inspect target as rendered output:

- major layout regions
- type hierarchy
- spacing rhythm
- control geometry
- border/shadow strength
- color and tonal balance

In `extend`, inspect family pattern:

- layout grammar
- hierarchy behavior
- component family
- spacing rhythm
- framing style for new areas

Goal: identify system behavior, not isolated decoration.

In `adapt`, treat target content and controls as suspect until checked against the current repo.
Directional targets often contain pilot-only labels, sorting affordances, read-time metadata, placeholder actions, hover actions, stateful controls, or entirely fabricated note copy that are not real product data or supported behavior.

## Step 4: Inspect Current Screen Render

Open current implementation and compare on rendered output.

Build comparison surface with:

- current local screen
- target or family reference
- live/published screen when useful
- user-marked screenshots when available

## Step 5: Build Concrete Mismatch Or Consistency List

For `match`, write visual mismatches.
For `extend`, write consistency requirements.
For `adapt`, write both directional borrow list and preservation constraints.

For `adapt`, preservation constraints should include product-truth constraints such as:

- do not add sort controls unless current screen or repo data actually supports sorting
- do not add read-time metadata unless the current repo has that field
- do not add badges, counters, actions, or utility rows that exist only in the sketch target
- do not add filters, bulk actions, saved views, menus, pagination, keyboard affordances, or other workflow controls unless the current repo actually supports them
- do not replace current repo titles, excerpts, tags, or note instances with target sketch copy unless the user explicitly wants content remapping
- do not reconstruct frozen shell areas loosely; preserve them literally or leave them outside the adaptation deliverable

Good statements are concrete:

- search field sits too far right
- title is one weight too heavy
- active radius is rounder than family
- new area introduces heavier card language than surrounding sections
- constitution-critical controls are no longer discoverable
- local override is present but not labeled temporary/durable

Avoid vague statements (`feels off`, `still ugly`, `close but not right`).

## Step 6: Classify Issues

Classify each issue into one category:

- structure
- spacing
- size
- type weight
- type tone
- radius/shape
- border strength
- shadow strength
- color/tint
- data-driven density difference

Use the same categories for consistency checks in `extend`.

## Step 7: Edit Only The Owning Layer

Typical ownership:

- structure: markup and major layout structure
- layout rhythm: layout rules
- component geometry/tone: component rules
- typography: base rules
- color/shadow/radius: token rules

Do not edit multiple layers for one narrow issue unless truly dependent.

Token discipline:

- if existing token/semantic variable can express the change, use it
- if no token exists and value is temporary, mark override explicitly temporary
- if no token exists and value is intended to be durable, escalate constitution/token-system revision

## Step 8: Match By Mode

In `match`:

- match explicit target values when clearly established
- do not choose cleaner abstraction if visible drift increases

In `adapt`:

- borrow only target aspects that improve intent alignment
- keep constitution, content, behavior, and family integrity primary
- keep user-frozen regions literally stable
- preserve the current repo's real data model, currently available fields, and actual supported interaction contract
- preserve the current repo's actual content instances unless remapping content is part of the explicit task
- if target shows extra metadata, controls, or behaviors not backed by current repo truth, drop them rather than approximating them

In `extend`:

- prefer native consistency over novelty
- keep hierarchy, spacing grammar, and component family aligned

## Step 9: Verify After Each Narrow Pass

After each small batch:

- reload current screen
- compare edited region against target/family
- confirm direction of change

In shell-preserving work, always recheck:

- topbar/sidebar controls required by constitution remain visible and usable

## Step 10: Browser-Level Verification

Use rendered verification, not source-only review:

- side-by-side inspection
- screenshots
- computed style checks
- geometry checks (width, height, spacing, radius)
- typography, color, border, and shadow checks

Automation is optional; use it when repeatability helps.

## Step 11: Control Caching

If expected change is not visible, rule out caching first:

- hard reload or query-busted reload
- asset version query update
- local preview server restart

## Step 12: Separate Style Drift From Data Drift

Do not confuse content differences with style differences.

Common data-driven drift:

- longer titles
- more rows
- different labels
- different pagination state

Also separate:

- legitimate new functional content vs accidental new visual language
- directional borrowing vs literal copying
- temporary prototype shortcuts vs accidental durable local drift
- real current-repo data fields vs target-only sketch fields
- real current-repo content vs target placeholder or fabricated content

## Step 13: Escalate If Convergence Stops

If narrow passes stop converging:

1. stop guessing
2. identify structural root cause
3. compare DOM/style ownership more literally with target or family rules
4. rebuild directly where needed

If issue is misclassification:

1. stop parity edits
2. reclassify as `reframe`
3. request redesign or constitution-revision direction before continuing
