# Design De-slop regression cases

This evaluation resource belongs to the [validation record](../validation.md),
outside the runtime skill. It contains synthetic product content only.

`inputs/` holds three dependency-free local pages and their design rules.
`inputs/TASKS.md` holds seven ordinary requests. `criteria.md` is evaluator-only
acceptance guidance, not a preferred visual answer. `input-manifest.json`
identifies the frozen source bytes.

[Discovery requests](discovery-requests.md) provide the original twelve metadata
interpretation probes plus three HTML-specific requests. Their context qualifications belong to `criteria.md`;
do not supply those judgments to a fresh classifier.

`observed/` contains portable patches from the original executions in the parent record.
They preserve actual outputs for inspection and replay; they are not expected
answers to give a fresh worker. Each patch starts from a separate unchanged
copy of `inputs/`, and patches for alternative notebook layouts must not be
combined. From that copy, apply one with `patch -p1 -i /absolute/path/to/file.patch`,
then render it and run the relevant checks.

| Patch | Executed request | Skill snapshot |
|---|---|---|
| `selected.patch` | Apply the selected list option: R1 only | Second |
| `stale.patch` | Resume the earlier list proposal: E1 | Third |
| `expressive.patch` | Expressive night sky: focused Evening watch improvement | Third |
| `delegated.patch` | [Explicitly delegated notebook implementation](observed/requests.md) | Third |
| `html-selected.patch` | [N02 application after actual HTML selection](observed/requests.md#html-review-and-selected-application) | HTML workflow intermediate |

The first four snapshots predate the user’s required HTML preview before adopting unseen
changes. Their authority expectations are retained as historical evidence. The last row
is the newer preview/selection/application continuation.
Snapshot identities and limitations are in the parent record. Patch replay
reconstructs an observed output; it is not a new agent execution.

Three images retain representative actual comparison output from the initial synthetic
review task: [desktop](observed/compare-desktop.png),
[record alternatives](observed/compare-options.png), and
[phone](observed/compare-phone.png). They show proposed choices, not adopted
changes or measured usability gains. The complete temporary preview workspace
is not archived here.

For a fresh trial, copy all runtime files plus `README.md` and `DESIGN.md` into
one task-owned project directory. Supply exactly one request, only its named
handoff, and the frozen candidate skill. Exclude `TASKS.md`, unused handoffs,
criteria, prior results and this resource's validation record from the worker's
packet. Use a separate clean project for each case. Keep independence limits
explicit when isolation is by instructions rather than filesystem permissions.

The evaluator compares the actual diff and renders with the criteria. Check
unselected regions through computed styles or element screenshots as well as
file hashes; a shared stylesheet can alter an untouched HTML file. Compare
proposals under matching viewport, content and state, and distinguish observed
geometry from a predicted usability benefit. No-change and conflict resolution
can be correct outcomes without a source edit.

`check.py` exercises the fixture's named controls at 1440×1000 and 390×844 through
Playwright. It requires Python, Playwright and an available Chromium browser in
the evaluation environment; these are not skill dependencies. From this folder:

```sh
python check.py --root /path/to/isolated/project --out /path/to/task-owned/checks \
  --browser /path/to/chromium
```

Omit `--browser` when Playwright's managed Chromium is already available. Use
`--pages notebook`, `galaxy` or `queue` for a relevant subset. The checker closes
its browser and local server on success or failure. Remove task-owned output
after recording necessary results at their agreed evidence owner.

The checker uses fixture selectors. Adapt selectors when a valid redesign
changes markup, preserving the behavioral assertions. It does not prove all
record content, semantic accessibility, unselected-region isolation, design
quality, human preference, or real host skill discovery. The review request in
the corpus and held-out ideas in the criteria are inputs, not claims that every
possible case has been executed; completed runs are listed in the parent record.

## Interactive HTML review

Open the [self-contained synthetic example](observed/review.html) in a browser.
It uses actual Fieldbook renders: shorter introduction, quieter cards or aligned
rows, and both valid introduction/list combinations. Its DOM-only view retains
actual HTML/CSS and source elements for native DevTools inspection. Pick an
element to copy its qualified selector or add it to feedback. These are frozen
rendered states; product interactions do not execute in the inspection frames.

Switch between whole-screen context and the introduction, a representative note,
or the note list. Choose N01 plus N02-A or N02-B, then **Selected combination**
to view the actual combined whole page. Component focus does not split an
inseparable proposal's adoption scope. Choose **Take part / request changes**
for a narrower request and describe what to take and preserve; that proposal is
excluded from the accepted combination until its revised result is reviewed.
The viewer has no capture-mode toggle and this example embeds no PNG evidence.
Legacy image-only manifests still support measured crops. The
[earlier component screenshot](observed/compare-components.png) records the
capture-only iteration before DOM support. The earlier
[component DOM view](observed/compare-dom.png) and
[phone integrated view](observed/compare-dom-phone.png) show the actual viewer;
they predate the quieter controls and partial-request workflow. Open the current
HTML to inspect and choose elements.

Its choices are draft
preferences; the HTML never edits source or sends an agent a message. **Share
with agent → Copy request** produces a readable message to paste into the
conversation. The default asks for another preview. After inspecting the accepted
combination, choose **Apply accepted** for an application request. **Keep original**
ends the round without adoption. JSON is an optional structured handoff inside
the dialog; the helper checks that exact artifact and baseline before application.

`build_review_demo.py` reproduces the example from the frozen synthetic inputs
and the historical selected-row patch. It captures real independent previews
at desktop and phone sizes, serializes actual DOM with the bundled snapshot
resource, verifies each reloaded snapshot's geometry, text and representative
rendered styles against the source, builds the DOM-only HTML, and removes its
temporary copies. `--verify-raster` additionally requires identical temporary
PNGs; that optional diagnostic may expose browser raster differences and is not
the default DOM evidence gate. Captures are never embedded in this example.
This is an author-built resource example, not a new agent trial or preferred
visual answer. From this folder:

```sh
python build_review_demo.py --output /path/to/review.html --browser /path/to/chromium
```

The [viewer itself before and after](observed/viewer-review.html) compares the
previous tool with the component workspace before the DOM extension, using the same N02-A task
and product data. Inspect its comparison canvas, choice list and feedback area
individually or return to the whole viewer. This records a local implemented
tool change, so adoption controls are locked and feedback remains editable;
it is not an applied product-design selection or global installation.

`build_viewer_review.py` captures explicit preserved-before and current HTML
inputs. The result embeds both sets of PNGs and does not need those inputs or
a server at viewing time. To reproduce with two available review versions:

```sh
python build_viewer_review.py --before-html /path/to/previous-review.html \
  --after-html /path/to/current-review.html --output /path/to/viewer-review.html \
  --browser /path/to/chromium
```

`test_review_artifact.py` runs stdlib builder/consumer cases. Add `--browser`
when Playwright and Chromium are available to exercise actual viewer controls:

```sh
python test_review_artifact.py
DESIGN_DESLOP_BROWSER_EXECUTABLE=/path/to/chromium python test_review_artifact.py --browser
DESIGN_DESLOP_BROWSER_EXECUTABLE=/path/to/chromium python test_review_artifact.py --headed
DESIGN_DESLOP_BROWSER_EXECUTABLE=/path/to/chromium python test_dom_review.py --browser
DESIGN_DESLOP_BROWSER_EXECUTABLE=/path/to/chromium python test_dom_review.py --headed
python test_review_workflow.py
```

Tests create and normally remove their own isolated fixtures. To diagnose a
failure, set `DESIGN_DESLOP_TEST_WORK_ROOT` to a task-owned directory and
`DESIGN_DESLOP_KEEP_TEST_ARTIFACTS=1`; remove that directory after diagnosis.
The browser tests use synthetic colored PNGs to test the viewer's evidence and
selection mechanics. The example uses real rendered DOM; temporary captures
check its snapshot parity. `test_review_workflow.py` covers optional PNG evidence,
partial-choice receipts and the handoff workflow. Neither alone proves
skill workflow, aesthetic preference, or live-site readiness. See the parent
record for the separate fresh skill execution and actual coverage.

The DOM suite also inspects native nodes through Chrome's DevTools protocol,
checks fixed viewport geometry, exact integrated documents, selector references,
snapshot state/assets and exploratory-edit/reset behavior. For clean viewer
screenshots in Playwright, use `caret="initial", animations="allow"`; automatic
caret-hiding injects CSS into frames and correctly marks the inspected DOM dirty.

`--headed` runs the same DOM assertions in a visible browser. In the recorded
Chrome environment, a headless modal-button click sometimes reached the background
iframe before the download handler ran; the corresponding visible-browser probe
downloaded successfully. Keep headless and visible-browser results distinct;
the parent record reports the actual full-suite outcomes and this remaining limit.

The DOM suite includes controlled loading-time CSS/form edits and delayed picker
delivery, preserving native element clicks and dirty/reset checks. Legacy crop
geometry is measured after the pair is visible, separately from image decoding.
The [parent record](../validation.md#closeout-verification-and-initialization-corrections)
owns the current results, corrected defects and historical failure limits,
including the earlier picker failure whose exact cause remains unattributed.
