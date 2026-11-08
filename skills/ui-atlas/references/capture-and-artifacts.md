# DOM states and artifacts

## Contents
- [Owners and prerequisites](#owners-and-prerequisites)
- [Recipe](#recipe)
- [Generate and replay](#generate-and-replay)
- [DOM materialization and limits](#dom-materialization-and-limits)
- [Canvas and feedback](#canvas-and-feedback)
- [Refresh and migration](#refresh-and-migration)

## Owners and prerequisites

The app owns its executable UI, data fixtures and state recipes. The atlas owns
generated observations and feedback; the skill owns the reusable runner and viewer.
Keep these roles explicit even when their files share a directory. Do not copy a
product's UI into the viewer as a second editable implementation.
Use [artifact workspace](artifact-workspace.md) for the default
`<repo>/.artifacts/ui-atlas/` owner, overrides, Git/docs boundaries and retention.

`scripts/atlas.py` uses Python 3.9+ and the standard library. Browser work in
`scripts/capture.py` additionally needs Playwright in that Python environment
and an installed Chromium browser. It was exercised with Playwright 1.64.1;
use the project's compatible installation rather than silently adding packages
to the app. An existing browser can be selected with `--browser`.

Playwright is a dependency of this bundled runner, not a requirement for using
the skill or opening a delivered canvas. Existing browser tools or app-owned
previews can supply observations that satisfy the same DOM and evidence contract
below. Automated generation executes authored journeys and checkpoints; it does
not discover every page or reachable state by itself.

Keep package size, browser/runtime dependencies and generated app observations
separate when reporting storage. The reusable package contains instructions,
scripts and viewer assets; generated sheets embed app DOM and resources and
grow with the selected states and retained runs. An example sheet's size is not
the skill's fixed installation cost.

Start the app with its isolated data/fixture setup. The runner blocks unmatched
non-GET/HEAD requests and requests outside its base origin. It blocks service
workers. These controls are not a security sandbox and do not isolate backend
startup, server-to-server calls, WebSockets or side effects performed by GETs.
Keep the environment isolated independently. Mocked requests bypass their real
service; they establish UI presentation under those inputs, not end-to-end success.

## Recipe

Use a persistent `recipe.json` with stable atlas, journey and checkpoint IDs.
Supply ephemeral server origins through the CLI rather than saving a dead URL.
Include shared styles, rendering code, fixture generators and other relevant
dependencies in `source_files`; source checks cover only this declared set.
Response `file` inputs are hashed automatically relative to the recipe's owner.
List other recipe-owned dependencies, such as a fixture launcher, in optional
`support_files`. Changes to these bytes also invalidate the previous evidence;
undeclared dependencies are not discovered automatically.

```json
{
  "schema": "ui-atlas.recipe/v1",
  "id": "example-app",
  "title": "Example · UI Atlas",
  "scope": "Inbox loading and populated content; other screens unexamined.",
  "source_files": ["index.html", "app.js", "styles.css"],
  "journeys": [{
    "id": "inbox-load",
    "surface": "Inbox",
    "label": "Initial load",
    "description": {"purpose": "Review inbox loading copy", "action": "Open the inbox and return the items response", "result": "Loading and populated states", "exceptions": "Offline recovery is unexamined"},
    "evidence": "synthetic",
    "conditions": "Items response held until the loading checkpoint.",
    "viewport": {"width": 1200, "height": 800},
    "locale": "en-US",
    "routes": [{"id": "items", "url": "/api/items", "hold": true}],
    "regions": [{"id": "results", "label": "Results", "selector": "#results", "source": "app.js"}],
    "steps": [
      {"action": "goto", "url": "/"},
      {"action": "wait", "selector": "#results", "text": "Loading…"},
      {"action": "frame", "id": "inbox.loading", "label": "Loading"},
      {"action": "respond", "route": "items", "response": {"json": ["Example item"]}},
      {"action": "wait", "selector": "#results", "text": "Example item"},
      {"action": "frame", "id": "inbox.populated", "label": "Populated"}
    ]
  }],
  "coverage": [{"id": "inbox.offline", "label": "Offline recovery", "surface": "Inbox", "journey": "unexamined", "status": "unverified", "reason": "No recovery recipe has been established."}]
}
```

Every journey gets a fresh browser context. Its steps share a page and state;
their frames form one ordered sequence. Browser isolation does not reset the
server database. Keep server fixtures immutable or reset them through their owner.
One continuous flow may include reopening, failure and recovery; separate
unrelated variations into separate journeys rather than implying a transition.

Actions:

| Action | Fields |
| --- | --- |
| `goto` | `url`, relative to the supplied app origin |
| `click`, `hover`, `focus` | unique `selector` |
| `fill` | `selector`, string `value` |
| `press` | `key`, optional `selector`; otherwise page keyboard |
| `wait` | `selector`, optional `state` (`visible` default), optional exact `text` |
| `wait-ms` | `ms`, for an intentional observed interval, not a readiness substitute |
| `respond` | route ID in `route`, `response`; release pending requests and set future replies |
| `scroll` | optional container `selector`, numeric `x`, `y` |
| `advance-clock` | `ms`; requires journey `clock` (ISO datetime) installed before navigation |
| `frame` | stable `id`, `label`, optional replacement `regions`; legacy `capture` is an alias |

Routes match URL paths (including query) with Python shell-style globs; absolute
patterns match the complete URL. They default to method `GET`; specify `method`
for actions. A response accepts `status` and `json`, `body`, or a relative `file`,
plus optional `content_type`. Files must be inside the recipe owner.
`{"forward": true}` releases a held same-origin GET to the isolated backend.
An optional `merge` object recursively replaces fields of that backend's JSON
response, retaining unrelated fixture fields. Forwarding never permits a real
POST. A synthetic API failure can use status 500 and the product's error shape.

Journeys can set `theme` (`light`/`dark`), `reduced_motion`, a string-valued
`storage` object for localStorage, and `clock`. Regions need stable `id`, `label`
and a unique CSS `selector`. Optional `source` is an author-verified locator,
not an automatically inferred source map. A region absent from one state remains
visible as unavailable; the runner does not invent a crop.

Optional journey `description` fields `purpose`, `action`, `result` and
`exceptions` are plain strings summarizing verified behavior. They travel with
the observed frames. Conditions remain in `conditions`; ordered checkpoints
remain in `steps`. Without authored descriptions the viewer uses recorded
journey labels, conditions, actions and checkpoint labels, explicitly leaving
unprovided exceptions undescribed. Put proposed changes in proposal notes,
not in descriptions presented as observed behavior.

## Generate and replay

```sh
python scripts/atlas.py init --source-root /path/to/app
python scripts/capture.py recipe.json --source-root /path/to/app \
  --base-url http://127.0.0.1:8000
python scripts/capture.py recipe.json --source-root /path/to/app \
  --base-url http://127.0.0.1:8000 --replay inbox.loading
python scripts/atlas.py check /path/to/atlas/runs/new-run/atlas.json
python scripts/atlas.py build /path/to/atlas/runs/new-run/atlas.json \
  --out /path/to/atlas/runs/new-run/index.html
```

Without `--out`, `capture.py` creates a uniquely named run in the default workspace
and refreshes its entry catalog. Its `--workspace` selects an alternative owner.
An explicit `capture.py --out` must name a new directory and leaves workspace
management to the caller. `atlas.py build --out` names the output HTML
file rebuilt from a retained manifest. The capture runner produces `frames/*.html`, a
`ui-atlas/v2` manifest in `atlas.json` and a self-contained `index.html` canvas.
It generates no screen images. The filename `capture.py` remains compatible
with existing launchers. The manifest carries conditions, actual DOM elements,
source hashes including uncommitted bytes, recipe identity and incomplete states.
The payload panel shows route rules at that checkpoint, storage, clock and steps
so far. Forwarded responses are represented by their forwarding/merge rules;
the panel is not a recording of every response body or server-side input.

A failure invalidates the remaining checkpoints in that journey and exits with
code 2; other journeys still run. Failed actions after the final checkpoint
remain in `journey_failures`, appear in the information panel and also exit with
code 2. Earlier frames remain usable observations, not proof that the journey
finished. Inspect the partial canvas instead of calling it a complete result.

Alternative materializers must provide an inert local `document` and nonempty
`elements` inventory with unique IDs, tags, selectors and known parent IDs.
Use one explicit `html`/`head`/`body` envelope with opening and closing tags in
that order. Tag names may use uppercase. The builder rejects omitted/repeated or
misordered envelope tags and records parsed insertion positions for the policy
and inspection bridge; tag-like comments or attribute text are not insertion points.
Document `data-atlas-node` markers must exactly match that inventory. Each
rendered frame also requires `regions` and `texts` arrays, even when empty.
Text items need actual `text`, `selector`, viewport `rect` and known `regions`
IDs (or an empty array). A region needs a measured `rect`, or an unavailable
reason. The builder rejects active document scripts/handlers, missing inspection
fields, paths outside the artifact owner and image substitutes. Supply geometry,
scroll, properties and payload using the runner's manifest shape for full inspection.
Document constructs such as `plaintext`, `xmp`, `noembed`, `noframes`, `noscript`
and `template` are not accepted from alternative materializers. `style`, `title`
and `textarea` need explicit closing tags, including when their text contains
markup-like strings. SVG animation elements are refused here as well as by the
bundled materializer, rather than accepting a frame that continues changing.

Replay opens a fresh headed browser and follows the same steps to the selected
checkpoint. It keeps the app and route mocks alive for inspection; close the
browser or press Ctrl-C to finish. It requires the app server to be running.
`--headless --replay-seconds 2` is useful for bounded smoke verification.
An app-specific launcher can provision its fixture server before calling this
runner and stop/delete its owned runtime afterward. Store that launcher with
the durable recipe; optional `replay` text explains its command using `STATE_ID`
as the substitution marker. Viewer controls only show or copy instructions;
they do not execute local commands.

## DOM materialization and limits

`snapshot.js` clones the app's actual light DOM, freezes computed styles and
embeds fonts, images (including image-input buttons) and supported SVG resources.
Imported static SVG sprite IDs and local gradient references are renamed together.
External sprites containing stylesheets, nested resource/use elements or the
unsupported surfaces below require an app-owned preview; their styles are not
allowed to affect unrelated elements in the materialized document.
It preserves form values,
selected options (including an explicitly empty single-select), checked/indeterminate controls, open details, native modal
dialogs and scroll positions. Window and container positions restore instantly
before readiness, including when source styles use smooth scrolling. The viewer
establishes each iframe's layout before loading its document; the bridge waits
for parsing before restoring native state.
Hover/focus appearance is retained through resolved
styles. Shared computed defaults apply only to pseudo-elements observed in the
source, so common generated content does not create extra decorations elsewhere.
The original viewport stays fixed while the canvas scales the frame.
CSS Typed OM preserves computed `height: auto` on block containers where child
margins can collapse, instead of forcing a fixed-height layout. Other resolved
heights stabilize native/normal line boxes. The bundled materializer requires
that browser API; geometry checks still govern acceptance. The distinction uses
CSS Typed OM's [computed values](https://www.w3.org/TR/css-typed-om-1/) rather than
the used values sometimes returned by `getComputedStyle()`.
Scroll deliberately and add checkpoints for content below it. A narrow viewport
is not evidence of a real mobile or native-host environment.

The source app's scripts, event handlers and navigation are removed. `frame.js`
restores the observed display state and supplies DOM hit testing in an iframe
sandbox with only scripts enabled. Its CSP permits the trusted inspection bridge,
embedded styles and data assets, and prevents app network calls. Canvas clicks
select elements, including disabled controls; they do not operate the product.
Use actual replay to execute interactions. HTML/SVG nodes remain elements;
original raster assets remain assets whose pixels are not individually selectable.
CSS pseudo-elements and native control internals are inspected through their
owning DOM element, not invented as separate nodes.

The bundled materializer refuses detected shadow roots, nested frames, canvas,
object/embed, video/audio, SVG foreignObject, SVG SMIL animation elements,
obsolete raw-text surfaces (`plaintext`, `xmp`, `noembed`, `noframes`) and
transformed native modal dialogs. A file input with selected files also requires
an app-owned preview: HTML cannot retain its FileList, so the bundled materializer
refuses that state instead of showing an empty control. Empty file inputs and
ordinary static SVG remain supported.
Unreadable stylesheets and unavailable or nonisolated resources also fail the
state. Closed shadow roots and OS/native surfaces cannot be inventoried reliably;
declare them unsupported and use an app-owned preview if they are in scope.
Popover restoration exists but has no dedicated regression witness. Do not
substitute a screenshot or claim these surfaces have complete element coverage.

Each captured document first passes the builder's inert-DOM validation inside
the checkpoint boundary. An unsupported document becomes a failed state while
other journeys can still produce a partial canvas.
For each visible inventoried element, the runner compares source and restored
DOM rectangles at the original viewport. A delta above 3 CSS pixels fails the
state; a delta above 1 pixel within that tolerance is a recorded warning. Source
text and region geometry must also match before and after materialization.
Control real inputs/timing when these checks fail, or retain the missing state.
They do not prove pixel equivalence, compositor timing, animation quality or
complete interaction coverage. Complex transforms, masks, occlusion and native
controls still need visual review. Blocked requests and browser errors remain
attached as limitations.

The copy observer reads light-DOM text and clips it to the viewport and ancestor
overflow boundaries, rejecting invisible/covered text heuristically. Partially
clipped quotes retain full DOM text and are marked in the inspector, notes and
exports; check the actual frame before using them. The element inventory and
selection bridge use the same viewport/overflow clipping helper. Elements keep
their full source `rect` for geometry checks and a `visibleRect` for visible
selection. Hidden elements remain in the inventory but not in search or visible
hierarchy. For absolute/fixed HTML boxes and their descendants, clipping follows
the browser's layout parent (`offsetParent`): positioned elements escape unrelated
DOM overflow wrappers, while their actual containing blocks still clip when they
have overflow boundaries, including transform/filter/containment boundaries for
fixed elements. Root overflow and body overflow propagated through a root with
both overflow axes `visible` use the viewport boundary. A body whose overflow is
not propagated retains its own clipping boundary. Native modal/popover roots also escape outer
overflow; their own clipping remains effective. This does not resolve every CSS
paint/occlusion case. Older inventories get viewport rejection and bridge checks; recapture
for complete recorded overflow visibility. The inventory includes form and SVG nodes, but
neither inventory establishes complete copy or accessibility coverage. Switching
frozen states is an ordered sequence, not video or a live app transition.

## Canvas and feedback

Opening a workspace entry shows its last selected sheet directly. Use the sheet
selector above the screen/element/opinion tabs to switch, or choose the full
catalog to search sheets and inspect earlier, partial or interrupted runs. Sheet
switching preserves target-owned drafts and pending note operations in tab memory;
export saved opinions for durable transfer. The full catalog is an in-view dialog.
A standalone run opens without the workspace selector.

Drag the sheet to pan; wheel to zoom around the pointer. `V` selects, `H` or held
Space pans, `Shift+1` fits all frames and `Shift+2` fits the selection. Drag a frame
header to reposition it; drag a section title to move its frames together.
Section bounds follow their member frames. Frame layout is saved locally and
can be reset from the file menu. Titles use bounded ellipsis and collision
suppression; overview zoom prioritizes section labels, with full frame names in
the sidebar and title tooltip. Click a supported element, then use breadcrumbs,
the collapsible element tree or Enter on the canvas to select its parent.
Named regions retain verified source references. Search results locate and
select matching elements without rebuilding or filtering the canvas itself.
Search pages expose all matches in groups of 200. Fit-all can zoom below 6% for
large sheets; overview labels remain subject to collision suppression.

The zoom menu exposes percentage entry, fit-all, fit-selection and 100%, plus
description-card and note-pin visibility. The panel toggle provides a focused
canvas view. Section explanation cards scale with the sheet; selecting one opens
its full description and ordered states in the inspector.
At narrow widths the inspector occupies a separate bottom area. The canvas keeps
its own controls and usable space; the screen list opens as a dismissible panel.

Previous/next state navigation retains the zoom and selected element's screen
position only when named-region, stable selector or unique semantic evidence
identifies a counterpart. Sequential inventory IDs and positional selectors
alone are insufficient. A named region supplies identity only with recorded
visible bounds and exactly one inventory root; unavailable or ambiguous regions
cannot become a first-match fallback. Semantic fallback must be unique in both source and
target within the recorded region context. It cannot substitute a target already
identified as a different source control merely because its label changed.
Missing or ambiguous counterparts leave selection empty,
retain the inspected position and display that limit; stepping onward can find
the original element again. These comparison rules also apply in the narrow
layout; its usual fit-on-selection does not reset comparison zoom. This
correspondence does not verify app transitions. Non-rendering tree wrappers are
omitted while their visible descendants remain under the nearest visible ancestor.

The compact shell keeps provenance, coverage gaps and failures in the information
panel. Element properties, payload, state navigation and notes appear in the
selection inspector. `canvas.js` owns camera/gestures; `catalog.js` owns section
membership, readable names, search and conservative correspondence;
`sections.js` owns section bounds, explanation cards and label visibility;
`notes.js` owns feedback persistence. `sheet-picker.js` owns the in-view selector,
catalog dialog and draft-status bridge; `workspace.js` owns sheet hosting and the
last selected sheet. `viewer.js` connects these resources with
selection, trusted frame messages and controls.

Unsubmitted drafts stay attached to their state/element during navigation, in
that tab's memory. Closing with pending text prompts the browser's unsaved-work
guard when supported. Add drafts as notes before export or moving the atlas.
Saved notes use local browser storage when available and export/import
`ui-atlas.notes/v1` JSON. Preserve exports when moving the atlas; local-file
storage is browser-dependent. Separate per-note keys and storage events preserve
independent additions/deletions across tabs. Pending failed writes/deletions remain
in memory across reads and other-tab updates, and later note operations retry them.
The unsaved-work guard also covers these pending operations. The file menu offers
a retry while operations remain pending. Export added/updated opinions before
closing if storage remains unavailable; memory is not a durable backup. Exports
contain the current opinion list, not deletion commands. A failed deletion must
be retried in the open tab or performed again later; importing an export does
not delete existing browser notes absent from that file.
Imports merge new IDs and compare differing same-ID records. The user chooses
current or imported content for each conflict, with current content selected by
default; cancellation applies none of the file. No timestamp infers which copy
is newer. Identical duplicate entries are combined; conflicting duplicate IDs
inside one file are refused. Immediately before applying, the store is read
again: if an affected local record changed since comparison, import stops for a
fresh review. A read failure also stops import. A subsequent write failure keeps
the chosen values pending for retry/export and does not report successful saving.
An import cannot begin or apply while an affected note has a pending storage
operation: retry first, or export the pending opinions and import in a fresh
viewer after storage recovers. This prevents the pending overlay from hiding a
competing saved version during import. Conflict rows identify the current
screen/element and show differing fields; retaining current content is explicit.
Unknown states and changed DOM/renderer/source/recipe identities stay in exported
requests with a recheck notice. A rebuild's current-source check also qualifies
notes, pins, review filters and grouped requests: changed files and unavailable
files get distinct warnings without rewriting the original observation identity.
A later matching check clears only that current-source warning; independent
missing-frame or identity warnings remain. Portable note JSON retains the saved
evidence identity; it does not freeze a transient source-check result. An imported
note is qualified against the destination viewer's observation and last source
check. Autosaving or importing a note is not
approval to change the product.

Notes optionally carry `kind` (`proposal` or `observation`) and `status` (`open`
or `reviewed`); older notes default to proposal/open without losing their IDs or
quoted evidence. The opinion list supports search and review/staleness filters,
location links and export. Pins group notes on the same element, or per frame
at overview scale. Missing or changed targets fall back explicitly to their
frame, and absent frames keep their notes in the list and exports. Review status
does not clear a stale-evidence warning or assert that a fix was applied.

## Refresh and migration

Run `check` on resumption and after source edits. It returns 0 for matching
declared source/recipe/support files, 2 for changed or unavailable evidence, and 1
for malformed input. `build` repeats that check and labels its result/time. When
source changed, rebuilding labels drift but does not rerender states; run the
recipe again to refresh DOM. An offline artifact cannot monitor later edits.

Image-only `ui-atlas/v1` manifests need a new recipe run; rectangles cannot recover
their missing DOM. Existing recipes accept the legacy `capture` checkpoint name.
Keep atlas/state IDs stable and retain old notes: the v1 note format and storage
keys remain compatible, with old evidence marked for recheck. Do not remove a
historical run while an active comparison or decision still depends on it.
