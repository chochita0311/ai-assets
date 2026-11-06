# HTML review contract

## Contents

- [Build the comparison](#build-the-comparison)
- [Manifest](#manifest)
- [Inspectable DOM](#inspectable-dom)
- [Component inspection](#component-inspection)
- [Choices and evidence](#choices-and-evidence)
- [Receive a decision](#receive-a-decision)
- [Rounds and retention](#rounds-and-retention)
- [Sources](#sources)

## Build the comparison

Produce one self-contained HTML artifact with the original on the left and the
active proposal or exact selected combination on the right. Keep both panes
visible together, including on a narrow screen; use equal scaling, internal
scrolling and zoom rather than stacking before above after. Separate the captured
viewport from the size of the review browser. A phone capture can be inspected
in a desktop review window without pretending it is a desktop layout.

Use the bundled [viewer](../assets/review.html) through the standard-library
[helper](../scripts/review.py):

```sh
python3 <skill>/scripts/review.py build <manifest.json> --output <review.html>
```

The manifest is authoring data, not the user-facing deliverable. Render actual
before and candidate screens in isolated project copies; the helper packages
their DOM and decisions but does not invent designs, render pages, change a
project or start a server. Complete DOM previews need no PNG files. The viewer
embeds their real HTML/CSS in isolated frames so the file works after the preview
server stops. It has no DOM/capture toggle. Where a side/view has no declared DOM
descriptor, a supplied PNG remains inspectable as a labeled legacy fallback.
Source selection is automatic per side/view, so mixed and image-only reviews
remain reachable without adding duplicate controls to complete DOM reviews.

Use a new artifact identity for each changed review. A short date-prefixed local
filename is useful; choose a bounded task-owned location outside the product
checkout or its established private artifact owner. Do not put private captures
in a public repository. Link the actual HTML in the response, show the paired
view when possible, and explain the few choices that matter.

## Manifest

Use UTF-8 JSON. Paths to PNG captures and DOM HTML files resolve relative to the
manifest; absolute local paths also work. Remote document/image URLs are not
supported; DOM assets must already be embedded in their snapshot.
Each image's intrinsic width must match its declared view width. Capture full
screens with matching route, content, theme, viewport and interaction state;
different full-page heights are legitimate consequences of a layout change.

| Field | Content |
|---|---|
| `version` | `1` |
| `review_id`, `round` | Unique review identity and positive integer round |
| `language` | `en` or `ko`; defaults to `en` |
| `stage` | `proposal` (default), `applied` or `retained` |
| `title`, `summary` | Human-readable context; summary may be empty |
| `baseline` | `label`, `description`, and `files` mapping relative source paths to SHA-256 strings |
| `views` | Nonempty list of rendered comparison conditions described below |
| `proposals` | List of independently reviewable alternatives; empty for no-change |
| `combinations` | Optional list of actually rendered exact selections |
| `applied` | IDs actually applied; empty except in applied stage |
| `components` | Optional list of `{id, label}` objects naming inspectable components |

Fingerprint only relevant target files and shared dependencies, including binding
rules when their change could alter the proposal. Do not invalidate a selection
merely because an unrelated sibling file changed. Record source access limits in
`baseline.description`; an empty `files` map supports visual discussion but
cannot support an application-ready receipt. Source paths must stay within the
source root supplied at decision checking, including resolved symlinks.

Each view has `id`, `label`, positive `width` and `height`, a `conditions` string,
and an optional `before` (a local PNG path, or null when unavailable). Omit PNG
paths for DOM-only reviews. Conditions name the
route, relevant state, content, theme, scroll position and motion timing. Use
separate views for relevant screen sizes or interaction states. Preserve enough
surrounding content to judge the proposed region. An optional `regions` map
associates component IDs with rectangles in this baseline capture, or null.
An optional `document` contains the matching DOM snapshot and component selectors.

Each proposal has these fields:

| Field | Content |
|---|---|
| `id`, `title` | Stable selectable identity and meaningful name |
| `group` | Optional mutually exclusive alternative group; defaults to its own ID. Another proposal explicitly naming that ID joins the same group |
| `observation`, `benefit`, `tradeoff` | What is visible, what might improve, and what the user gives up |
| `question` | A concrete comparison question for human judgment |
| `scope` | A list of affected regions/files, shared reach and any owner-rule changes |
| `preserved` | Optional list of content, behavior and intentional character retained |
| `checks` | Optional list of checks actually performed and relevant limits |
| `requires`, `conflicts` | Optional lists of other proposal IDs; never silently select them |
| `evidence` | `rendered`, `concept` or `unavailable` |
| `captures` | Optional map containing every view ID, with local PNG paths or null; omitted normalizes to all-null |
| `components` | Optional list of affected component IDs; no entries means whole-screen inspection |
| `regions` | Optional `{view_id: {component_id: rectangle_or_null}}` for this exact proposal |
| `documents` | Optional sparse `{view_id: document_or_null}` for this exact proposal |

Use meaningful decision units, not one checkbox for every CSS declaration.
Bundle inseparable edits under one proposal with the full scope visible. Keep
alternative compositions in the same group, such as `N02-A` and `N02-B` in
`N02`. A familiar treatment can remain as an alternative or the original; do not
make every option converge on the same supposedly correct style.

Each combination has `id`, a set of two or more `proposals`, `evidence` and
optional `captures` and `documents`. It must satisfy group, dependency and
conflict rules. Its DOM or fallback images must come from that exact integrated
selection, not pasted pieces of individual proposals. Its optional `regions` has the same shape as proposal regions, for
components affected by its member proposals. Pre-render useful likely combinations without generating every
possible subset by rote. A single selected proposal uses its own rendered preview.
A combination may also supply `documents` in the same shape as a proposal;
these must preserve the actual integrated result and its own selectors.

IDs contain letters, digits, hyphens or underscores. The helper rejects unknown
fields/IDs, malformed fingerprints, invalid captures and impossible dependency
graphs or combinations. For each baseline/result view, a declared DOM descriptor
is authoritative, including explicit null; a PNG cannot conceal that missing
DOM. Where no descriptor key is declared, a PNG may supply legacy evidence.
Application requires complete rendered evidence across all declared views and
the ready, unchanged active inspection surface. A missing PNG does not block a
complete DOM review. Missing evidence in either form stays visible and prevents
application while feedback remains available.
Do not label a sketch as rendered product evidence to enable a button.

For motion or interaction work, include matching state/time sequences and
reduced-motion observations. When still captures cannot communicate the change,
extend the paired review with real local replays or live isolated previews while
retaining the same decision contract. The image viewer alone does not verify
animation, control behavior or accessibility.

## Inspectable DOM

Preserve real rendered elements, their IDs/classes, styles and the stated page
state. Do not recreate a screenshot as decorative HTML or wrap it in an image
and call that DOM inspection. Use the browser's native DevTools to inspect actual
elements; the viewer also provides a picker for adding a qualified selector to
feedback. A frozen snapshot is inspectable HTML/CSS, not a running product:
application scripts, navigation and backend actions do not execute inside it.

After the source page has settled at the declared viewport and state, evaluate
[snapshot.js](../assets/snapshot.js) in that page and write its returned HTML to
an artifact-owned file. For example, using an already available Playwright page:

```python
snapshot = page.evaluate(Path("<skill>/assets/snapshot.js").read_text())
Path("<review>/before-desktop.html").write_text(snapshot, encoding="utf-8")
```

The resource preserves current form and disclosure state, inlines accessible
styles and supported image/font assets, and removes application scripts and event
handlers. It rejects known unsupported content and resource cases; a successful
serialization still requires the parity check below.
Read the reported limitation; do not remove intentional product features merely
to make the serializer succeed. Use an accurately labeled capture fallback or
an equivalent isolated real preview whose comparison conditions are verified.
Validate the serialized view against the original rendered page, including
relevant geometry, styles, content and state. Temporary screenshots may help
verification but are not a required viewer mode or deliverable. Successful
packaging alone does not prove visual parity or interaction behavior.

The bundled serializer supports HTML5 standards-mode rendered light DOM, readable
stylesheets, static PNG/JPEG/WebP/SVG images and embedded fonts. It preserves
leading newlines in native text controls and preformatted content. Unsupported
cases include quirks/legacy document modes, open top-layer popovers, modal dialogs
and fullscreen; canvas/media/nested frames, shadow/custom elements, adopted
sheets, active or paused animations, certain dynamic CSS asset/import forms,
inaccessible assets, animated images, and form states that cannot be serialized.
An ordinary nonmodal open dialog is supported. If decoding the embedded current
image changes its intrinsic width or height, such as a density-selected `srcset`
image, the serializer refuses it rather than silently changing its layout.
Programmatic fonts not represented by stylesheet font-face rules are rejected
when detected.
A closed shadow root on an ordinary element is not observable through standard
page JavaScript: exclude it explicitly and verify actual parity instead of
assuming a successful serializer detected every hidden rendering dependency.
Navigation destinations become inert fragments to retain native link appearance;
the final viewer prevents their activation.
Sanitization can still change CSS that depends on a rewritten attribute, such as
`a[href^="https:"]`, or on removed nodes, such as `article:last-child` followed by
an application script. Include those dependencies in the source-to-replay style
and geometry check. If they differ, use a verified equivalent isolated preview
or a labeled capture fallback; packaging success does not make the changed view
faithful to the source.

A baseline view's descriptor is:

```json
"document": {
  "html": "before-desktop.html",
  "selectors": {"header": ".site-header", "record": "#record-1"}
}
```

Use the same descriptor beneath each proposal/combination's `documents` view
key. `html` is a local file path during authoring and embedded HTML in the
normalized payload. It must have one leading `<!doctype html>` and complete,
balanced `html`, `head` and `body` markup. `selectors` maps known component IDs
to nonempty CSS selectors; it may be empty or sparse. Proposal selectors must belong to its
affected components; combination selectors to their union. The browser checks
that a focused selector is valid and resolves to exactly one visible element.
Missing DOM or a missing/ambiguous selector stays visible as missing evidence;
do not hide the failure by switching to a PNG. Old manifests may omit these fields;
their normalized identity and receipt schema remain unchanged.

The frame retains the declared viewport width **and height**, including when the
page is taller than that viewport. Its page scroll exposes the rest of the
composition without changing viewport-dependent CSS. DOM component focus moves
to and highlights the actual element; it does not promise a PNG-style isolated
crop. Component Fit uses both measured element widths at one scale and pans to
the focused elements; keep 100% and whole-screen navigation available. The **Selected combination**
action enters selection mode and whole-screen focus together. Only an actual
document for that exact selected set is a combined result; a missing combination
must not show an individual proposal as if it were integrated.

An element reference records before/after side, view, preview identity, unique
selector, short text and known component where applicable. Add individual-preview
references to that proposal's note and integrated references to overall feedback.
Picking an element never changes adoption decisions. Copy/manual text fallback
keeps the reference usable outside the viewer; native context-menu inspection
remains available.

DevTools edits are exploratory and do not update the embedded proposal or source.
The viewer marks DOM/CSS changes and requires resetting the recorded preview
before application export; reset preserves decisions and feedback. Export checks
the current frames again, including stylesheet-rule changes, instead of relying
only on an earlier ready message. Turn a desired exploratory edit into a new
rendered proposal before treating it as selected work. Source fingerprints,
rendered-evidence checks, exact-set constraints and actual user submission still
apply. The frame bridge is isolated from the review document and accepts only
messages from the current frame instance; its readiness is not human approval.

## Component inspection

Use meaningful UI components such as a header, filter bar, list or representative
record, rather than arbitrary CSS fragments. Top-level component IDs are unique;
their namespace is independent of proposal, combination and view IDs. A component
may have several alternative proposals. One inseparable proposal may affect
several components: inspecting a crop does not authorize only that fragment of
the proposal. Name the complete affected set beside its choice.

For captured-image inspection, measure regions from the same actual page captures
used for the whole-screen comparison. A rectangle is exactly `{x, y, width, height}` in intrinsic PNG pixels.
Values must be finite numbers, with nonnegative origins and positive dimensions;
the rectangle must fit entirely inside its image. Capture at device scale 1, or
convert measured browser coordinates to actual PNG pixels. A non-null rectangle
requires an existing capture. Measure each viewport/state and integrated result
separately: header changes can move a list, so individual-preview coordinates
cannot stand in for a combined render.

Baseline region example, inside one view:

```json
"regions": {"header": {"x": 40, "y": 56, "width": 1200, "height": 180}}
```

For a proposal affecting `header`, the corresponding result uses:

```json
"components": ["header"],
"regions": {
  "desktop": {"header": {"x": 40, "y": 56, "width": 1200, "height": 96}}
}
```

Maps may omit unavailable regions or use null. The helper rejects unknown IDs,
regions outside the declared proposal/combined scope, malformed boxes and bounds
outside the real PNG. Missing component evidence leaves whole-screen evidence
usable; the viewer shows which region is unavailable and offers a whole-screen
return. Do not substitute a full image while labeling it a component crop. For
an added/removed component with no counterpart, retain that explicit gap and use
the whole-screen comparison for adoption.

Captured-image component focus clips the actual PNG without changing its pixels.
Both sides use one scale based on the wider component, capped at 100% in fit mode; differing
widths and heights remain meaningful. `100%` means one image pixel per CSS pixel.
The whole-screen view remains available for surrounding effects. Changing focus
or capture size preserves decisions and notes. Exact selected combinations use
their own measured regions, and their complete selected scope stays visible even
when one component is in focus. Application export keeps the existing checks and
also needs both displayed regions when focus is active; missing crop evidence
can be reviewed through the whole-screen mode instead.

Older artifacts without component fields still open and validate as whole-screen
reviews. The helper preserves absent optional fields in their normalized data so
adding this feature does not change old artifact fingerprints. Regions are visual
evidence, not new decision or source-ownership units; receipts remain proposal-based.

## Choices and evidence

Each option offers compact, accessibly named full-accept, partial/revise and
exclude controls plus a note. Defer and reset remain available for the active
proposal; clicking its current choice again clears it. Use icons and tooltips
where the action is clear instead of repeating explanatory text on every row.
An overall feedback field remains available even when there are no proposals,
so the user can challenge a no-change judgment or request another direction.
Accept can be undone; choosing another variant clears the previous choice in
that group. Dependencies and conflicts stay visible rather than being resolved
by automatic acceptance. Keep the comparison question and tradeoff near the
decision in expandable details. Free-text reasons help the next draft preserve what the user likes;
there is no universal aesthetic score or mandatory improvement quota.

The active individual preview is distinct from the accepted set. `Selected combination`
shows the exact known combination. If that composition has not been rendered,
the viewer says so and offers feedback export; it never calls the last selected
individual image the combined result. All-none selection shows the original.
Source/evidence gaps or concepts prevent application export. In DOM mode the
active frames must be ready and unchanged; PNG decoding is not a prerequisite.
Image-only reviews still require their actual captures to decode.

Browser autosave is a convenience scoped to this artifact's fingerprint. The
single **Share with agent** action opens a readable request to copy into the
conversation. Its default intent is another preview; applying accepted changes
and keeping the original are explicit alternatives. Include proposal identities,
statuses, notes, overall feedback and the review identity/fingerprint in the
request. Optional JSON download/copy lives inside that dialog; manual text
selection remains available if clipboard access fails. The HTML performs no
network request, project write or automatic transmission to an agent.

For partial adoption, select **Take part / request changes**, optionally pick an
element and add its reference to the note, then describe what to take and what
to preserve. For example: “Remove this card's shadow, but keep its colors and
corners.” Record this as `revise`, never `accept`; it is excluded from the accepted
combination. The agent turns those preferences into a new rendered proposal with
a new review identity, retaining the other choices and reasons. A reference names
an element; it does not extract a safe, independent CSS patch by itself. Explain
shared-style reach and clarify only material scope ambiguity. A narrow note
qualifying an accepted proposal also needs reconciliation before whole adoption.

## Receive a decision

The receipt contains `format: design-deslop-decisions`, version, review identity,
round, artifact fingerprint, intent, preview ID, selected IDs, per-proposal
status/note, `review_note` (an overall string, empty allowed) and export time.
Statuses are `pending`, `accept`, `revise`, `reject` and `defer`; only `accept`
belongs in `selected`. The schema remains version 1 and older status values stay
valid. `revise` preserves partial/revision intent without authorizing application.
Its intents are:

- `review-feedback`: revise an option or prepare a missing combination; no adoption.
- `apply-selected`: request the exact displayed, rendered selection.
- `retain-original`: keep the original, with no accepted IDs.

For a submitted receipt, validate it before applying:

```sh
python3 <skill>/scripts/review.py check <review.html> <decisions.json> \
  --source-root <project-root>
```

The helper verifies artifact/receipt identity, statuses, constraints, the exact
rendered selection and current source fingerprints. It reads source and reports
readiness; it never edits files or calls the result applied. A successful check
does not replace the user's actual application request, project verification or
the final freshness check when time or concurrent work could invalidate it.

The helper conservatively checks every file recorded in that artifact's baseline;
it cannot infer which changed region affects a partial selection. If drift is
confined to an unselected independent area, inspect the source difference and
refresh the affected captures and review. Preserve the submitted receipt and
explicitly map its unchanged selected scope to the refreshed result. Validate
that reconciled selection against the new artifact and source; a changed
fingerprint alone does not require another approval when the selected meaning
and impact are unchanged. If they changed, obtain a new decision. Never silently
edit the original receipt or claim it was submitted for the new artifact.

Do not convert feedback, stored draft preferences or an old receipt into approval.
Feedback may legitimately contain conflicts or an unrendered selection. A source
change or changed proposal needs a refreshed review; retain the user's comments
as context without transferring approval to a different selected design or impact.
A plain-language selection of the same reviewed result is equally valid and needs no extra JSON
ritual. Apply only that scope, then build applied-stage HTML using actual DOM or
necessary fallback evidence.
Applied/retained reports keep adoption controls locked so their buttons cannot
suggest a source rollback happened.

## Rounds and retention

Keep the current before state frozen through unaccepted iterations. Preserve the
initial original and distinguish it from the last actually accepted state when
starting a later round. Keep earlier HTML/receipts while they are needed to
understand active selections; do not silently overwrite them or treat more
iterations as progress. Respect a stop or retain decision immediately.

An unanswered review remains an active selection artifact after the turn ends.
Keep its source/preview material while needed to apply or revise the selection,
and name the owner and cleanup condition. For longer retention, use an explicit
durable owner. Once selection/application or the evaluation purpose is finished,
remove task-owned working copies and stop preview processes. The self-contained
HTML must not break merely because a temporary capture server was closed.

## Sources

The [Explain Diff HTML gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)
informs the idea of explaining a change and its reasons in a portable interactive
artifact. Its quiz and code-walkthrough structure are not design acceptance rules.
The [component variants example](https://thariqs.github.io/html-effectiveness/06-component-variants.html)
shows alternatives together so a person can inspect them. The
[feature-flag editor](https://thariqs.github.io/html-effectiveness/19-editor-feature-flags.html)
illustrates visible dependencies and exporting selected changes. The per-change
design decisions, evidence checks and application boundary above are this skill's
contract, not claims that those examples implement it.

[Chrome Inspect mode](https://developer.chrome.com/docs/devtools/inspect-mode)
documents native DOM/style selection. The frame implementation follows the
[srcdoc isolation guidance](https://developer.mozilla.org/en-US/docs/Web/API/HTMLIFrameElement/srcdoc)
and [postMessage source/identity checks](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage).
These platform references support mechanics, not visual quality or product approval.
