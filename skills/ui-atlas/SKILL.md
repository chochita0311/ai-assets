---
name: ui-atlas
description: Build or refresh a local pan-and-zoom HTML atlas of an existing app, organized from its entry and menus into topics, features, selectable DOM elements and connected states. Use for a Figma-like product map, inspecting payloads, tracing dropdowns and action results, or collecting element-specific feedback. Not for inventing screens, redesigning the source product, or claiming exhaustive coverage.
---

# UI Atlas

Put a magnifying glass over the existing product. Organize real rendered screens
into selectable DOM elements, inspectable regions and repeatable states, retaining their whole-screen
context. The atlas is an observation layer; product code and reproducible state
recipes remain the source, and the HTML is a generated view.

## Boundary and outcome

- Creating or refreshing an atlas authorizes observation and its supporting
  artifacts, not an unsolicited rewrite of the app. Apply corrections only when
  the user's request includes them; follow the meaning and scope of their notes.
- Preserve the actual UI, including awkward copy, transient states and missing
  capabilities. Never draw an approximation and call it an observed app state.
- Deliver a working local HTML canvas, its reusable recipe and enough source
  identity to regenerate or detect drift. Name the covered surfaces and states,
  unexamined areas, rendering failures and relevant environment limits. A list of
  URLs or an image contact sheet without focused inspection is insufficient.
- Resolve the artifact owner before persistence. Default to
  `<repo>/.artifacts/ui-atlas/`; an explicit user destination or established
  repository owner takes precedence. Follow [artifact workspace](references/artifact-workspace.md)
  for recipes, new runs, notes, ignore rules and cleanup. Keep reusable tool code
  separate from app observations. Reuse atlas/state IDs across refreshes and do
  not publish local observations implicitly.

## Map the existing app

1. Read the app's entry rules, actual routes, templates/components, state owners
   and existing stories or browser fixtures. Inspect rendered behavior as well
   as code. Product contracts govern intended behavior; code and actual renders
   establish implemented behavior. Record differences without silently fixing
   or treating a stale design export as current UI.
2. Establish the product entry, actual menu order and topic/feature hierarchy
   before choosing capture batches. Give each observed state one primary topic;
   use references for genuinely shared contexts. Keep editions or other real
   product boundaries explicit. Loading/error/empty states and viewport sizes
   belong under their feature or in view filters, not competing top-level topics.
   Read [menu topics and state links](references/menu-topics.md) before composing
   a multi-screen workspace or reorganizing existing sheets.
3. Inventory the requested pages, tabs, dialogs, menus and meaningful regions.
   Trace a region's shared usage before assuming it belongs only to one page.
   Select regions through actual elements and measure them in each rendered state.
   Do not split an inseparable interaction into supposedly independent fixes.
   For each consequential control, account for the relevant closed/open,
   input/selection, pending/result, cancel and recovery states. Record an explicit
   observation or a qualified gap; a visible trigger alone does not cover its menu.
4. Enumerate meaningful reachable states: pending/skeleton, empty data, empty
   search results, populated content, unavailable/error, hover/focus/disclosure,
   and relevant action outcomes. Include initial entry, retained/reopened state,
   refresh and recovery when they can change what the user sees. Only use states
   relevant to that surface; do not generate every Cartesian combination.
5. Keep uncertain, unimplemented, not-applicable and failed states visible and
   distinct. Static code discovery and a finite crawl cannot establish that all
   states were found. A state type or a proposed design is not reachability proof.

## Reproduce and materialize

Read [DOM states and artifacts](references/capture-and-artifacts.md) before using
the bundled helpers or writing a recipe. Use existing fixtures/stories when
possible; the bundled browser runner is optional and framework independent.

- Use the actual app renderer with controlled data and response conditions.
  Keep server-rendered data, browser storage, network responses and time under
  the relevant owner. A browser response mock alone cannot control server-side
  rendering, OS dialogs or native-host behavior.
- Use isolated synthetic data for actions such as sync, installation or deletion.
  Do not click through a user's live side effects merely to populate the canvas.
  Requests and server work outside browser interception need their own isolation.
- Wait for the condition being inspected, not universal network idle. Hold and
  release responses to inspect intermediate phases. Record synthetic conditions;
  a deliberately held loading state does not measure real loading duration.
- Preserve the viewport, language, theme, scroll, interaction and data conditions.
  Observe transitions in one continuous scenario and retain their order. Frozen
  DOM states help inspect copy and geometry; switching states does not verify
  animation or interaction. Offer the corresponding actual replay separately.
- Render frames with actual HTML/CSS/SVG from the app, using isolated live
  previews or inert materialized DOM. Preserve text, buttons, inputs, icons and
  containers as individually selectable elements. An image with hit rectangles
  is not an element-level DOM canvas; do not substitute screenshots as its frames.
- Preserve native dialogs, form values, hover/focus appearance and scroll state.
  Compare the materialized DOM's rendered geometry with the source. Mark
  unsupported surfaces or excessive divergence explicitly instead of silently
  redrawing, flattening or removing them. Original raster assets can remain assets;
  their pixels are not separate DOM elements.

## Show and use the atlas

Use [viewer.html](assets/viewer.html) through the bundled
[builder](scripts/atlas.py), or an equivalent viewer preserving these semantics:

- Place related states on one spatial canvas, with drag-to-pan, pointer-centered
  wheel zoom, fit-all/fit-selection and movable frame positions. Keep the source
  viewport fixed: zoom the sheet without reflowing the app.
- Present the product map in menu/topic order independently of capture files,
  timestamps or test categories. Compose a topic's related feature states on one
  canvas; retain original observations, identities, payloads and feedback owners.
  Expose viewport variants as a view choice. Keep required original observations
  as backing evidence. Do not repeat fully mapped capture batches in the menu map;
  expose unassigned observations and any retained earlier runs separately.
- Group states by their actual journey, with named section bounds that follow
  frame movement and an ordered state list. Keep section and frame labels from
  colliding as zoom changes; prioritize section names at overview scale and the
  selected frame, with full names available on hover or in the inspector.
- Preserve real journey boundaries inside feature groups. Show recorded action
  links and result branches beside the corresponding control/state; do not imply
  a sequence merely because independent captures are adjacent. Keep element
  inspection separate from following recorded states. Neither executes product
  actions; actual replay remains separate.
- Supply concise, evidence-backed purpose, conditions, actions, results and
  exceptions alongside a journey when known. Scale explanation cards with the
  sheet and disclose full details on selection. Distinguish recorded behavior
  from proposed changes; missing explanations are not proof of missing behavior.
- Let the user select any supported visible DOM element, including disabled
  controls and SVG icons, then choose its ancestors or named regions. Preserve
  the full-screen context and expose the selected element's text and properties.
- Use named regions and readable, collapsible ancestors for navigation. Search
  should locate the matching element, not merely filter whole screens. When
  stepping through states, retain a uniquely identified element and zoom; report
  absent or ambiguous counterparts instead of selecting a positional substitute.
- Keep the shell compact and neutral. Use short frame labels and a small tool
  strip; put scope, provenance, limitations and detailed instructions in accessible
  disclosures. Show element properties, payload and notes on selection instead of
  filling the canvas with explanatory prose.
- Open the last selected topic directly at the workspace entry, or the first
  topic in product order when no choice can be restored. Without a topic map,
  retain the existing standalone/sheet entry behavior. Put product scope and topic
  selection above the screen/element/opinion tabs. Offer the full menu map,
  unassigned captures, retained earlier runs and incomplete-run diagnostics through
  the selector. Omit empty history controls. Retain target-owned drafts
  and pending note operations when switching sheets; closing still needs the
  existing unsaved-work guard.
- Keep notes attached to stable state/region IDs, element locators, quoted text and selectors. Add
  source-file or message-key references only when verified, otherwise leave the
  source relationship unresolved. Export readable grouped requests and portable
  notes so feedback does not depend solely on one browser's storage.
  Preserve draft ownership when selection changes and retain clipping qualifications
  beside quoted evidence, in saved notes and in exports.
- Link the opinion list and canvas markers back to their observed element or
  explicitly fall back to the frame. Keep observation notes, proposed changes,
  review status and evidence staleness distinct. A reviewed note is not proof
  that a source change was applied or approved.
- Mark feedback for reconsideration when its DOM, renderer, source or recipe evidence changes. Saving
  or importing notes is not authorization to apply them. The viewer does not
  edit source, execute copied commands, or send messages to an agent.
- Make missing states, rendering limitations and the last source-check time easy
  to inspect. A standalone HTML file cannot continuously check the filesystem;
  run the source check and rebuild when resuming or after UI changes.

## Refresh, repair and finish

Check relevant source and recipe identity before reusing a prior atlas or applying
its notes. Reconcile drift, preserve notes and stable IDs, then regenerate affected
flows including shared regions. Keep old evidence while a comparison or decision
still needs it; do not carry a prior approval onto changed meaning or scope.

For an expressly requested fix, modify the real source under its project rules,
then replay the affected states and update the atlas. An attractive canvas or
passing static check is not evidence that the transition or native host works.

Open the delivered canvas and exercise mouse pan/zoom, frame movement,
DOM/ancestor/region selection, payload inspection, search-to-element navigation,
notes export/import and location links, section movement, label density and state
comparison including missing counterparts. Verify source geometry and isolation of inert previews;
include below-fold/overflow visibility, search beyond its first result page,
large-sheet fit-all and canvas/inspector use at narrow widths when relevant;
check actual replay separately. Preserve older notes with a recheck marker when
migrating from image-only evidence. Report actual checks and gaps; distinguish
implemented tool capability from states observed in this run. Stop task-owned servers and remove scratch after
transferring needed outputs to their durable owner. Keep durable replay recipes
independent of temporary server URLs, profiles and runtime directories.

For a topic map, also follow an actual menu into a feature's ordinary and exception
states without choosing a capture batch. Exercise a dropdown from its trigger to
its recorded open/result/cancel states. Check viewport filtering, old links,
cross-topic drafts, original-note compatibility and unassigned-state diagnostics.
Run `scripts/test_topics.py` and `node --test scripts/test_topic_notes.mjs` when
changing composition or feedback ownership. State counts alone do not establish
that the product map is understandable or its control states are covered.

When cleanup is requested after reorganization, distinguish derived topic views
from their required source manifests/DOM. Follow the cleanup checks in
[artifact workspace](references/artifact-workspace.md#retain-move-and-clean-up)
before removing superseded runs; complete topic membership alone does not make
backing observations disposable.

If available, use $design-deslop for proposed design alternatives and selection;
the atlas can supply observed baselines without becoming that approval workflow.
If available, use $screen-alignment for a requested match to an established design.
