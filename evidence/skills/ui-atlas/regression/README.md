# UI Atlas resource regression

These portable synthetic inputs exercise the runner and viewer from
[ui-atlas](../../../../skills/ui-atlas/SKILL.md). They do not reproduce a private
app and do not represent an independent agent using the skill.

Run the standard-library contract checks from the repository root:

```sh
python3 -B evidence/skills/ui-atlas/regression/test_atlas.py
```

For the browser checks, use a Python environment with Playwright and supply an
existing Chromium executable:

```sh
python -B evidence/skills/ui-atlas/regression/test_atlas.py --browser /path/to/chromium
```

Add `--workspace-only` to focus the browser run on workspace entry, sheet
navigation and retained drafts; the full command also runs existing viewer checks.

The test owns a temporary directory, loopback HTTP fixture and browser. It
removes its artifacts and stops its processes. It does not install dependencies.

The twenty contract checks cover standalone/inert packaging, source and recipe
support-file drift, DOM ownership/inventory, refusal of active DOM and screen-image
substitutes, incomplete evidence, required inspection arrays, region bounds and
optional observed-description validation/embedding, visible-element bounds,
default/custom workspace ownership, local ignore behavior, retained partial-run
catalogs and relocation without blessing changed recipe support files, atomic
manifest publication after interrupted writes, and isolation of malformed old
run manifests without deleting their original files, explicit document-envelope
validation, raw-text/declarative-animation rejection, unavailable-region bounds
and explicit refusal of a selected file input represented only as a value attribute.
They also check safe workspace payload embedding and encoded run paths.
The browser run materializes loading, populated, hover, focus, modal,
action-pending and failure states using the fixture's actual renderer.

It checks every visible fixture element's source/preview geometry within the
runner's 3 CSS pixel tolerance, no generated screen PNGs, HTML/SVG and disabled
control selection, ancestor selection, native modal restoration, pointer-centered
wheel zoom, sheet pan (including the hand tool and held Space), movable frame
persistence, payload history, filters,
notes in parallel tabs, JSON import/export including legacy identities,
narrow-screen provenance, clipped content and stacked-dialog observation.
Response holds, zero real backend POSTs, no HTTP requests from the standalone
canvas, bounded actual replay and a failed action after the last frame are
separate witnesses. Frozen DOM switching is not an interaction replay.

[Viewer navigation checks](viewer_checks.py) also exercise search-to-element
selection without remounting frames, readable collapsible hierarchy, description
and state order, element/zoom/position retention, a missing counterpart and its
recovery, rejection of positional identity substitutions, visible title collisions
at ten zoom levels from 6% through 400%, section dragging, description/panel
visibility, opinion pins, location links and review-state filtering.

[Usability checks](usability_checks.py) exercise target-owned drafts across
selection/clearing, clipped-quote qualifiers in notes, the review list and exports,
420-result pagination including Enter on later pages, viewport/overflow-hidden
targets, a 390px canvas with separate inspector, nested native modal selection
outside a clipping ancestor, auto-height margin collapse, and fit-all for 100
synthetic frames arranged in twenty rows or one long row. Repeated fixture frames
are a sheet stress input, not a claim about an app's discovered state count.
[Workspace checks](workspace_checks.py) retain old files and rebuild the catalog;
the browser suite also runs the capture CLI without `--out` and checks its default
repo path and visible terminal-failure status even beside a corrupt older run.
[Workspace navigation checks](workspace_browser_checks.py) exercise direct sheet
entry, the selector above the existing tabs, last-sheet restoration, catalog
search/status/history and browser back/forward. Drafts stay with their original
sheet and element through switching; failed note saves remain exportable after
their textarea clears. Clean-sheet eviction preserves saved notes, the root
unsaved-work guard includes inactive sheets, and 390px layout, standalone views,
blocked preference storage and untrusted selection messages have separate controls.

[Reliability checks](reliability_checks.py) inject quota/read/delete failures and
other-tab storage events, checking pending-note retention, export and recovery.
The real form's failed save also keeps the unsaved-work guard until a successful
retry. Fixed and absolute overlays escape unrelated clipping wrappers, while
their containing-block controls remain clipped; visible descendants, text and
mouse/ID selection are checked. Body overflow propagated to the viewport, body
clipping under a non-visible root overflow and positioned `display:contents`
wrappers have separate native-hit controls. Desktop and 390px comparisons retain 150% zoom
and the selected element's position, including a moved counterpart followed by
a missing counterpart and return.
Current-source changes and unavailable files qualify existing notes in filters,
pins, details and grouped requests without rewriting observed frame identities;
restoring matching files clears only that current-source warning while prior
identity and missing-frame warnings remain.

[Conflict checks](conflict_checks.py) cover repeated source labels, ambiguous
destinations and a surviving distinct control whose label changes. Stable
selectors, named regions and unique semantic correspondence remain successful
controls. Failed same-ID review updates are exported, the tab is closed, and a
fresh viewer imports the chosen version. Other controls cover keeping current
content from an older export, cancelling the complete import, conflicting and
identical duplicate IDs, read failures and another tab changing an opinion while
the import dialog is open. The conflict dialog is also exercised at 390px.
Pending operations for affected IDs block import until retried or exported and
reopened; the retry path remains exercised. Named-region identity also prevents
substitution of an already-distinct control.

[Projection checks](projection_checks.py) restore window and container scroll
positions before readiness for both `auto` and `smooth` styles and confirm that
positions remain fixed after readiness. Native form controls retain explicitly
empty single-selects, selected options, empty multi-selects, text values and empty
file inputs. Selected files are explicitly refused before emitting a false frame.
URL-backed image-input buttons embed alongside ordinary/data-source image controls.
External SVG gradients retain modern and legacy fragment references, quoted URL
references and one shared definition set; the delivered view makes no HTTP request.
Imported stylesheets and imported/inline SMIL fail their own journeys in an actual
CLI run, which returns status 2 and keeps the healthy static sprite's partial
canvas and original unrelated blue fill. No false frame is emitted for refusals.
Pseudo-element defaults retain decorative content on its observed owners without
creating extra root/body/control decorations, including a majority of decorated
spans and an absolute-positioned case where ordinary box checks can miss extras.
They preserve visible descendants under
`display:contents` and zero-height wrappers while hiding truly invisible nodes.
Accepted uppercase HTML receives its policy and bridge at parsed positions,
including markup-looking comments/attributes/style text and non-BMP Unicode.
Unavailable or multiply rooted named regions do not become correspondence
identities. SMIL color animation is explicitly refused, with static SVG retained
as the successful materialization control. These refusal checks also run through
the alternative-materializer builder boundary.

The current [package manifest](package-manifest.json) identifies the package with
direct workspace entry, sheet navigation and the hand/Space pan repair. The
[record-revision-8 closeout manifest](package-manifest-closeout-r8.json) preserves
the earlier package with its closeout documentation clarifications. The
[v6 manifest](package-manifest-v6.json) identifies the final repair candidate
reviewed and exercised before that earlier closeout; runtime code, the entry
contract and UI metadata were unchanged between v6 and the record-revision-8
snapshot. The current package changes runtime and the entry contract.
These manifests preserve package identities through file hashes; they are not
source archives. Re-executing an older implementation requires its separately
retained source, while the current package and checks are available here.
The [v5 manifest](package-manifest-v5.json) identifies the baseline with
the correspondence/recovery-import defects. The [v4 manifest](package-manifest-v4.json) preserves the pre-repair
workspace/usability baseline. The [v3 manifest](package-manifest-v3.json) preserves the pre-refinement
section/review viewer. The [v2 manifest](package-manifest-v2.json) preserves the earlier DOM
viewer baseline. The [v1 manifest](package-manifest-v1.json) preserves the earlier
image-board baseline; its checks are historical, not evidence for the new renderer.

[Validation](../validation.md) records actual outcomes and remaining gaps.
