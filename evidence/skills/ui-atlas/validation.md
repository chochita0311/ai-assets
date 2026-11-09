---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-ui-atlas-validation",
  "revision": 10,
  "audience": "public",
  "subjects": [
    {
      "kind": "skill",
      "key": "skills/ui-atlas",
      "source_revision": null,
      "content_sha256": "fde12dab7511314b6264155bb67ba231d17940ca5fa8c243b4e7303cf45fd202"
    }
  ],
  "work": {
    "basis": "observed-defect",
    "state": "resolved",
    "readiness": "ready"
  },
  "knowledge": {
    "state": "supported"
  },
  "evidence": {
    "kinds": [
      "static-observation",
      "illustrative-synthetic",
      "generalized-private-observation"
    ],
    "maturity": "resource-execution",
    "execution": "run",
    "coverage": "partial"
  },
  "adoption": {
    "public_fitness": "approved",
    "case_status": "not-requested",
    "rule_status": "implemented"
  },
  "relations": {
    "related": [],
    "supersedes": []
  }
}
---

# UI Atlas creation and refinement

## Contents

- [Context And Applicability](#context-and-applicability)
- [Evidence And Evaluation](#evidence-and-evaluation)
- [Work And Acceptance](#work-and-acceptance)
- [Outcome And Reuse](#outcome-and-reuse)
- [History](#history)

## Context And Applicability

The [package](../../../skills/ui-atlas/SKILL.md) adds an observation layer over
an existing app: a spatial canvas of actual HTML/SVG states, selectable elements,
measured regions, repeatable journeys and collected feedback. It preserves the
whole-screen context and the app's implemented behavior. It does not redraw
screens, perform unsolicited fixes or turn a finite inventory into a claim that
all states were found.

The skill owns portable materialization/viewer resources. An app owns its executable
renderer and reproducible state conditions. Generated observations and notes stay
with the explicitly selected artifact owner. Optional neighboring design skills
apply only when their separate task boundaries are requested.

The original problem was repeated copy and content cleanup encountered only
while using individual app screens. The selected solution keeps the screen,
region and state together on one inspectable sheet, including loading, empty,
populated, hover/focus and action-result states where they actually exist.
The early image board was superseded by selectable DOM at the user's request.
A neutral Figma-like canvas, readable section/frame labels and optional observed
flow descriptions serve inspection and planning; full editor authoring features
and automatic product redesign are outside this tool's purpose.

The user retained the name `ui-atlas` and selected `.artifacts/ui-atlas/` as the
general consumer default, with local ignore behavior. The reusable package stays
with the asset repository; app observations stay with their explicit consumer
owner. This separates generated evidence from product source and maintained
documentation without depending on a harness. Existing app-specific owners and
explicit destinations remain valid exceptions under the
[workspace contract](../../../skills/ui-atlas/references/artifact-workspace.md).
The [runner contract](../../../skills/ui-atlas/references/capture-and-artifacts.md#owners-and-prerequisites)
distinguishes optional browser automation, authored state discovery and generated
output size from the reusable skill itself.

## Evidence And Evaluation

### Consumer settings observations and explicit refresh (record revision 10)

A later generalized private observation reviewed settings, recovery and connected
source states in an isolated application. A recipe supplied an authored error
response whose detail reached the rendered alert. Its wording was initially
read as product copy; inspecting the controlled response identified the fixture
as its author. This observes rendering under injected failure, not an error
message required by the product or proof of its natural failure conditions.
Alert lifetime and recovery need their own interaction sequence.

The first map omitted a connected-source branch. A subsequent explicit refresh
captured connection, retained list entry, reopening, removal/cancellation,
reconnection and read-failure recovery. The application registration and rendering
paths were real; the external reader and relevant service/model responses were
synthetic. The execution did not request operating-system permissions, read
personal notes, transfer a real model or measure inference quality.

The refresh retained existing state identities, earlier runs and feedback
ownership, and marked removed disclosures inapplicable instead of silently
reusing their observations. Product edits, applied-comparison capture and Atlas
recapture were distinct acts. Later search-source edits did not retroactively
update that map. A static retained observation cannot establish current source
freshness or watch the running application.

These are bounded consumer/resource observations. No portable package or installed
skill was changed in this addition, and no fresh-agent execution or guidance-effect
comparison was performed. Existing package fingerprints and historical resource
checks retain their original revision boundaries. Private originals remain at
their consumer owner; they are not distributed as public fixtures.


### Workspace navigation and pan repair (record revision 9)

Observed on 2026-11-08. The current [package manifest](regression/package-manifest.json)
identifies the portable package after these changes. The earlier closeout identity
is preserved separately in the
[record-revision-8 manifest](regression/package-manifest-closeout-r8.json).
The metadata fingerprint identifies this pre-commit working tree; Git records
the subsequent publication rather than a self-referential commit inside it.

Result: **PASS** for the executed static/resource checks and the adjudicated
documentation criteria. Evidence Coverage: **partial**; highest level:
**resource-execution**. These are author-executed synthetic checks, not an
independent fresh-agent execution of the skill on an unfamiliar app.

The hand tool and held Space could enter a pan path with a false section value;
accessing its missing dataset then threw before dragging began. Optional dataset
access now handles that path, and browser witnesses check the actual camera
delta for both gesture modes while retaining the existing selection controls.

The workspace entry now opens the last selected sheet directly, or the first
available sheet when no choice can be restored. A selector above the existing
screen/element/opinion tabs opens other sheets and an in-view searchable catalog
with earlier runs, partial failures and interrupted/unreadable-run diagnostics.
Workspace selection uses retained run metadata; it does not invent observations
or alter the app. Standalone run viewers remain independently usable.

Sheets keep their own element/state selection, drafts and failed note writes
while mounted. Dirty sheets remain mounted through switching; a bounded cache
can evict inactive clean sheets and recreate their transient inspection state.
Successfully saved notes retain their existing atlas identity in embedded and
standalone views. Drafts and failed writes remain tab memory, and the root's
unsaved-work guard also covers inactive sheets. Closing is not a durable backup.
The workspace establishes iframe layout before loading a warm file so a desktop
sheet does not initialize at the iframe's default narrow width.

The primary executed all twenty standard-library contract tests and the full
Chromium suite with Playwright 1.64.1. New witnesses cover payload escaping and
encoded run paths, direct entry, selector hierarchy, last-choice restoration,
catalog search/status/history, back/forward, per-sheet drafts, failed-save export
and retry, clean-sheet eviction, saved-note identity, inactive-sheet unload
protection, 390px layout, standalone operation, blocked preference storage and
untrusted selection messages. Existing geometry, selection, replay, clipping,
correspondence, import-conflict and storage-recovery regressions also passed.
Package validation, JavaScript/Python syntax and whitespace checks passed.

Two independent read-only documentation reviews used docs-structuring and
docs-shaping. The primary accepted their current-versus-historical identity
corrections, scoped the capture-directory and build-file forms of `--out`, and
qualified inspection-state retention by the mounted-sheet lifetime. The existing
entry/reference/evidence owners remain in place; no new session log or hierarchy
was introduced. Final local-link and fingerprint checks support those properties,
not general skill reliability.

Private consumer observations and their current state remain at their private
owner. They are not public fixtures or evidence for unfamiliar frameworks,
native hosts, real devices/services, or wider browser/storage compatibility.
This session did not run a fresh-agent state-discovery task: it repaired and
checked the delivered viewer/resources. Those broader claims remain unverified.

### Historical repair: correspondence, recovery and projection boundaries

Record revision 7 records the authorized repair/verification loop after the two
open findings in record revision 6. The package revision-5 baseline remains in
the [preserved manifest](regression/package-manifest-v5.json), fingerprint
`790cd45ab9008260cc229485bb68a6446532bdb3ae349a924734e55e2b92db0b`.
The [revision-6 manifest](regression/package-manifest-v6.json) identifies the
final repair candidate; the
[record-revision-8 closeout manifest](regression/package-manifest-closeout-r8.json)
adds that closeout's documentation clarifications with the same runtime, entry
contract and UI metadata as v6. The name, default `.artifacts/ui-atlas/` owner, ignore/retention policy,
v1 portable note format and original app/output preservation remain unchanged.

Observed on 2026-11-08. Result: **PASS** for the final executed static/resource
checks and adjudicated review criteria; **partial** evidence coverage. Highest
level: **resource-execution**, including comparable synthetic failure/recovery
reruns. Eight bounded read-only semantic reviews were used during correction.
The last frozen review reported no remaining material candidate in its inspected
scope; a separate bounded verifier executed the final checks. This is not a
fresh agent discovering an unfamiliar app's states, nor exhaustive native/device,
browser, CSS or application coverage.

| Failure or boundary | Correction and executed evidence |
| --- | --- |
| Same-label A disappeared and surviving B was reported as A's counterpart. | Semantic matching requires uniqueness in both source and destination within the recorded region context. Stable-selector and named-region identity prevent substitution of an already-distinct control. Wide/narrow browser tests reject the original substitution; exact selectors, unique semantics, region-constrained meaning and genuine named-region matches remain controls. |
| A pending review-status change was exported, but importing after reopening silently retained the old stored value. | Import plans show differing same-ID records with screen/element context, default to retaining current work, and apply explicit per-note choices. The real viewer exports a failed `reviewed` update, closes, reopens and persists the chosen version. Older imports, cancel-with-new-IDs, invalid/duplicate records and storage read failures are exercised. No timestamp declares one version newer. |
| A saved record could change while an import decision was open. Pending overlays also needed an explicit import rule. | Affected records are read again before applying; detected changes abort the whole import before new additions. Affected pending operations prevent starting or applying import until retried, or exported and reopened in a fresh viewer. Tests preserve the competing saved version and exportable local pending value, then confirm retry and import still succeed. |
| Repeated region matches were recorded as unavailable but the catalog still used their first root. | Named-region identity requires recorded visible bounds and exactly one inventory root. The unique-to-duplicate browser witness now leaves selection empty and returns to the original element. Empty rectangle dictionaries are rejected rather than treated as unavailable bounds with a usable root. |
| `display:contents` or zero-height parents hid visible descendants from the element tree. | The tree skips non-rendering wrappers while retaining visible descendants under the nearest visible ancestor. Search/canvas selection, tree visibility and row selection pass for both wrapper types; truly hidden controls stay excluded. |
| Uppercase closing BODY was accepted but received no inspection bridge. | The builder records parsed head/body insertion positions and the viewer inserts policy/bridge there. Explicit envelope validation rejects missing/repeated/misordered envelopes. Browser controls cover uppercase tags, markup-like comments/attributes/style text, emoji and Unicode line separators, with a working trusted bridge and no HTTP requests. |
| Default Python 3.9.6 accepted `plaintext` that swallowed the injected bridge; Python 3.11.15 already refused that missing parsed envelope. | Unsupported special/raw-text constructs are now refused consistently. `title`/`textarea` boundaries and explicit closing-tag requirements are checked without relying on interpreter-specific permissiveness. Ordinary closed textarea content containing apparent body/html tags remains accepted. |
| SVG SMIL fill kept changing inside an accepted frozen view. | The source and alternative-materializer boundaries explicitly refuse declarative SVG animation tags. The pre-fix view produced four different RGB fills across timed samples without a geometry failure. The new refusal is explicit, while ordinary static SVG still materializes. This is a disclosed unsupported surface, not an invented frozen rendition. |
| A painted absolute-position control escaped a static overflow ancestor but was missing from inventory and copy observation. | Shared clipping follows the actual layout parent for generated absolute/fixed HTML boxes. Body overflow propagated to a visible-overflow root uses the viewport boundary. Native-hit, inventory, text and viewer-selection controls cover four overflow values, containing relative/transformed ancestors, short body/root boxes and positioned `display:contents` wrappers. Actual clipping remains effective. |
| Smooth scrolling started an asynchronous restore; the source/preview geometry differed by 1,000px. The delivered iframe also had zero layout dimensions when its bridge restored state. | The viewer establishes iframe layout before assigning its document. The bridge waits for parsing and restores window/container positions with explicit instant behavior before readiness. Source/capture/delivered-viewer controls cover `auto` and `smooth`, both scroll axes, immediate and later offsets, and selection. The 100-frame tests still pass for offscreen frames. |
| A selected file input silently became empty in the delivered frame. | The bundled materializer explicitly refuses selected-file states, and the builder refuses a file input represented by a nonempty value attribute. A source FileList of length 1 previously became 0 with unchanged geometry. The corrected source emits no false frame; empty-file and text-value controls still pass. An app-owned preview is required for the selected-file state. |
| A single-select deliberately set to index -1 acquired its first option after parsing. | A recorded empty-selection marker restores index -1 before readiness. The source -1/viewer 0 baseline witness now remains -1. Selected index 1 and empty multiple-selects remain successful controls. |
| A URL-backed image input passed capture but the final builder rejected its unembedded `src`. | Image-input sources now use the existing resource embedder. The original witness raised `Nonembedded DOM resource: src`; the corrected capture/build/viewer path retains that input alongside ordinary-image and data-source controls without HTTP requests from the delivered view. |
| External sprite IDs were prefixed while inherited-gradient fragment references still pointed at the old IDs. | Local `href`, `xlink:href` and quoted/unquoted URL references now receive the same prefix as their targets. The original delivered gradient reference had no target. Corrected modern/legacy inherited gradients resolve to the two-stop base, repeated uses share one definition set, and quoted fill references resolve. These checks verify references and geometry, not arbitrary pixel equivalence. |
| An imported sprite stylesheet recolored an unrelated frozen blue element red without changing its geometry. | Imported sprite stylesheets are explicitly refused; their external document scope is not flattened into the atlas. A direct-attribute static sprite remains supported and the unrelated element stays blue. |
| Imported SMIL bypassed normal traversal, passed capture and then aborted the final builder. | Imported resources share the unsupported-surface boundary. Capture also uses the builder's document validation before geometry checking or recording a rendered state. An actual four-journey CLI run returns status 2, records stylesheet/imported-SMIL/inline-SMIL states as failures without emitting false frame files, and delivers the healthy static state as a usable partial canvas. |
| Shared computed defaults created decorative pseudo-content on elements that had none. | Common styles apply only to the source's observed pseudo selectors. The sparse decoration control, dense normal-flow case and dense absolute-positioned case retain exact source `::before`/`::after` content on root, body, control and spans. Before repair, normal flow differed by 36px; the fixed layout incorrectly passed capture while changing body pseudo-content from `none` to a vertical bar (U+007C). |

The first review's named-region substitution was reproduced with the actual
catalog; the tree and uppercase-body cases produced zero target tree rows and
zero ready frames before correction. The second review's unavailable-region
case selected the first wrong button despite a null region rectangle. Its
raw-text candidate was checked under both installed Python runtimes before
adjudication, preserving the newer runtime's successful refusal as counterevidence.
SMIL was separately reproduced rather than inferred from the code.
The third review's smooth-scroll candidate and the fourth review's two native
form-state candidates were also reproduced against their frozen candidates.
The fifth review's image-input and external-sprite cases were reproduced before
repair as a builder rejection and a missing gradient target respectively.
The sixth review's imported-style and imported-animation candidates reproduced
blue-to-red computed fill drift and successful capture followed by late builder
rejection. The corrections retain the static-sprite control and partial-run behavior.
The seventh review's shared-pseudo-default candidate was reproduced in both a
geometry-rejected normal flow and a geometry-accepted fixed layout before repair.
The primary separately found the absolute-clipping and delivered-iframe layout
cases. An initial document-parsing wait alone did not fix zero iframe dimensions;
establishing parent layout fixed the delivered path. Final assertions run without
diagnostic instrumentation and check both immediate and delayed state.

The import UI now supplies an explicit pending-save retry. Note exports are
opinion-list snapshots, not deletion commands: failed deletions stay pending
for retry and get a specific message, and imports do not delete local opinions
absent from the file. The retry/deletion path is exercised. This clarified limit
does not weaken preservation of pending additions or edits.

Final validation includes nineteen standard-library tests under the default
Python and the browser suite's interpreter, the complete Chromium/Playwright
1.64.1 suite, package/frontmatter validation, JavaScript/Python syntax, local
links/reference anchors, installed-source resolution and exact file fingerprints.
Initial new-test setup needed to wait for asynchronous file handling and dialog
opening before the next import or other-tab action. An interim parser helper
collided with its base class's `offset` attribute; the contract suite caught it
and the helper was renamed before the final frozen candidate. These interventions
are not counted as successful first runs or suppressed product failures.

#### Closeout evidence and provenance

Record revision 8 reconciles the complete creation/refinement sequence before
the user-authorized repository commit and push. It corrects historical package
locators and fills the record history without replacing earlier PASS or FAIL
results. Documentation review does not change the implemented runtime behavior
or upgrade the evidence to a fresh-agent workflow test. The subject's Git
revision is null because this evidence identifies the pre-commit working-tree
package by its content fingerprint; Git records the subsequent publication.

The original example-size discussion has no retained measurement establishing
a fixed 33 MB package cost; generated
output, source snapshots and optional runtime dependencies must be measured
separately rather than carrying that number into the package contract.

Two independent read-only documentation reviews applied `docs-structuring` and
`docs-shaping` to the resolved package, record and catalog owners, with the same
session context and bounded source references. Both identified three necessary
corrections: expose the record's required content roles, restore the original
consumer trial's scope beside its partial recovery, and distinguish hash
manifests from source archives. Those corrections preserve the historical trial
order, results and qualifications. Both reviewers independently verified the
consumer counts from the retained manifests and found no further necessary
correction in their delta reviews. They executed no package code or tests and
provided no acceptance or publication approval.

Closeout reran the nineteen standard-library tests under the default Python and
the browser suite's interpreter, the complete Playwright 1.64.1/Chromium suite,
package/frontmatter checks, JavaScript/Python syntax and whitespace checks.
Record metadata matched the improvement-record schema; fifty-six local Markdown
targets/anchors and both repository catalog links resolved. Exact manifest and
installed-source checks confirmed that only the two package references changed
after the final code review; all runtime files, the entry contract and UI metadata
remain identical to the revision-6 baseline. These checks passed. The package
validator's two optional neighboring-skill review notices were reconciled with
their availability-qualified handoff wording. Reference-editor inspection
transcripts and raw execution logs for every historical run are not retained in
this repository; closeout did not replay all those earlier operations.

### Historical audit before package revision 6: correspondence and recovery import

On 2026-11-08, one additional audit round checked the unchanged package identified
by `790cd45ab9008260cc229485bb68a6446532bdb3ae349a924734e55e2b92db0b`.
Record revision 6 added evidence while leaving the revision-5 implementation unchanged.
The full existing suite passed again: fifteen standard-library tests, Chromium
usability/reliability checks, package/frontmatter validators, JavaScript/Python
syntax and whitespace checks. Installed-source resolution, package fingerprints,
metadata, twenty-eight local Markdown targets and reference anchors also passed.

A fresh, bounded read-only challenger inspected the eighteen package files and
synthetic tests without prior audit conclusions. It proposed two cases outside
the existing suite. The primary reproduced both; the expanded audit result is
**FAIL**, with **partial** evidence coverage and **resource-execution** maturity.
Passing existing tests is counterevidence to a broad regression claim, not a
pass for these newly exercised requirements. Neither defect's introduction by
the earlier repair was established, and this was not a fresh-agent app workflow.

1. **Ambiguous source elements can produce a false counterpart.**
   In [catalog.js](../../../skills/ui-atlas/assets/catalog.js), semantic fallback
   checks uniqueness only among target elements. The Chromium witness starts
   with distinct buttons `#a` and `#b`, both labelled `Remove item`. A state
   retaining both correctly keeps `#a` selected. After `#a` is removed, comparison
   selects the surviving `#b` and reports `같은 요소 · 확대 수준 유지`. The repeated
   source meaning does not establish that this already-distinct control is the
   missing element's counterpart. Selection and ensuing feedback can therefore
   move to the wrong control. Existing missing-element tests remove every
   semantic match and do not cover this combination. The witness initially read
   a hidden inspector property using rendered text; using its DOM text corrected
   the test observation without changing the package.
2. **Import skips an exported pending update when its ID is already stored.**
   In [notes.js](../../../skills/ui-atlas/assets/notes.js), import accepts only
   previously unseen IDs. The primary ran the actual class in a Node VM with
   storage-write fault injection: save a note as `open`, fail its change to
   `reviewed`, and export the in-memory version. The exported value is `reviewed`.
   A new manager after storage recovery reads the older `open` record; importing
   the export returns success but leaves that old status. The file retains the
   pending decision, but normal import does not restore it or expose a conflict.
   Within-tab retry and import of new IDs still pass the existing controls.
   This contradicts the documented export-before-closing recovery path for
   pending same-ID updates; the witness is a storage-owner execution, not a
   browser persistence-portability claim.

Both issues were medium-impact functional omissions. At the end of that audit,
correction remained open under the existing skill owner. That request authorized
one additional verification round, so no package, consumer app or retained
consumer output was changed. Readiness was waiting for correction work rather
than more identical reruns. No execution budget was assigned. The authorized
repair above subsequently closed these findings.

The correction criteria required preserving these two failing cases as
regressions. Correspondence had to reject the duplicate-source substitution while
retaining exact-selector, named-region and unambiguous semantic controls.
Recovery import had to restore or explicitly resolve differing same-ID values,
without silently overwriting newer local work from an older export. Closure required
both distinguishing cases and the existing suite to pass, with clear
conflict/recovery behavior and matching documentation. The earlier repair
results below remain valid for their stated scope; those older checks alone did
not close the newly discovered findings. Public evidence is limited to portable code and synthetic observations.

### Package revision 5: failure recovery and comparison integrity

Revision 5 applies the five defects confirmed in the final revision-4 audit and
one related comparison omission found during independent static challenge.
The frozen baseline is identified by the [v4 manifest](regression/package-manifest-v4.json):
`ce32e4c8a4d371110fb5386616093af81ddd4d902deaefc26e423db9bb466565`.
The [v5 manifest](regression/package-manifest-v5.json) identifies that corrected
18-file package. The `ui-atlas` name, `.artifacts/ui-atlas/` default, local ignore
policy, note schema and app/source ownership boundaries remain unchanged.
No product source or retained consumer output was changed in this refinement.

Observed on 2026-11-08. Result: **PASS** for the executed static and resource
checks below. Evidence Coverage: **partial**. Highest evidence level:
**resource-execution**, including comparable synthetic failure/recovery reruns.
These are authored resource tests, also executed by a named bounded verifier;
they are not an independent agent producing an atlas in an unfamiliar repository.

| Confirmed baseline failure | Owner and correction | Executed recovery/control |
| --- | --- | --- |
| A failed note save remained exportable only until a later storage read/event or unrelated change discarded it. | `notes.js` overlays pending per-note writes/deletions on stored values, retries them on later operations, and clears only successful entries. `viewer.js` includes pending saves in its unsaved-work guard. | Quota, read and deletion fault injection preserves local edits alongside external notes. Deleting an old note frees quota and retains the new note; failed deletions do not reappear after storage events. The real form exports a failed save, then persists it on retry and clears the guard. |
| A truncated old manifest raised a JSON decoding error and blocked the next capture before opening a browser. | `atlas.py` atomically publishes complete JSON; both `capture.py` manifest writes use it. `workspace.py` isolates malformed run metadata and lists unreadable runs separately without changing their bytes. | Interrupted serialization preserves the previous manifest and cleans staging. Malformed JSON/status shapes coexist with a readable run. The default-path capture CLI proceeds beside a corrupt old run and records its expected terminal journey failure, preserving the old manifest/canvas. |
| A viewport-fixed button under an unrelated overflow wrapper was painted but absent from visible inventory, text and selection. | Shared `geometry.js` follows the browser's containing parent for fixed HTML elements and retains native top-layer boundaries. | Native hit testing, observed text, materialized inventory and mouse/ID selection agree for the visible overlay and descendants. Absolute-position and transform/filter/contain/will-change/content-visibility controls remain clipped, as does overflow inside a fixed element. Existing nested-modal checks pass. |
| At 390px, next-state comparison changed 150% zoom to 29% while claiming to retain it. | `viewer.js` skips narrow-layout auto-fit during comparison and carries the last inspected rectangle through missing states. | 1440px and 390px checks retain 150% zoom and screen position across a moved counterpart, a missing state and return. Ordinary selection fit and existing desktop comparison remain covered. |
| Rebuilding old observed DOM after current source changes showed global drift but left its note out of the recheck filter and grouped-request warning. | `viewer.js` qualifies notes using current freshness separately from recorded observation identity. References distinguish portable saved identities from destination-viewer source checks. | Changed and unavailable sources produce distinct warnings in note details, review filters, pins and grouped requests. Restoring original bytes clears only that source warning; older identity and missing-frame warnings remain. Original frame identities stay unchanged across all three rebuilds. |

The primary reproduced all five original failure shapes against frozen v4 using
the same installed Chromium/Playwright 1.64.1 and synthetic inputs. Baseline
execution imported v4 scripts/assets; a plain JSON test adapter only created
synthetic input manifests because v4 lacks the new atomic helper. It did not
replace production capture, catalog, storage, geometry or navigation behavior.
The baseline source-drift witness returned zero recheck notes out of one, and
the narrow comparison witness measured 29% after requesting 150%.

The independent read-only challenger found a missing control in the initial
repair: both comparison states used identical geometry. A genuinely moved target
followed by a missing state and return reproduced a 180px horizontal/90px vertical
anchor shift at 150% zoom. Retaining the last inspected rectangle corrected it;
the strengthened wide/narrow witness passes. A static follow-up examined that
delta and the clarified JSON/freshness boundary. Reviewer evidence informed the
primary's decision; it was not execution or completion approval.

Final checks include fifteen standard-library tests, the full Chromium suite,
package/frontmatter validators, JavaScript/Python syntax, local Markdown targets,
reference TOCs, package fingerprints and whitespace checks. The added browser
form-recovery test initially returned a native function from its test evaluation,
causing an illegal-invocation exception; the test now returns no function, and
the final suite completes. No production exception was suppressed to pass it.
The workspace reference now has a contents list and documents unreadable-run
isolation, atomic publication and pending-note recovery.

This run adds no app-wide coverage claim and does not rerun private consumer
sheets. Broad CSS painting/occlusion, every top-layer clipping combination,
native host/device behavior, real external services, additional browser engines
and fresh-agent workflow execution remain outside the demonstrated scope.
Failed saves are recoverable only while the tab remains open or through an
explicit export; local-file browser storage is not a portable backup.


### Revision 4: consumer workspace and usability corrections

Revision 4 applies an authorized refinement after a broader app run exposed
seven bounded usability/materialization failures. Its baseline is revision 3,
identified by the [preserved manifest](regression/package-manifest-v3.json).
The reusable package now defines a consumer-repository artifact convention at
`.artifacts/ui-atlas/`, independently of harness governance or any particular
app. Explicit user destinations and established repo owners take precedence.
No product source or historical app observation was changed to implement it.

The broader consumer trial used a source snapshot from 2026-11-07 at 17:55 KST,
with shipped-app surfaces distinguished from additional development-web surfaces
across twenty sheets. It attempted 256 capture checkpoints: 241 rendered and
fifteen failed, at 1440×1000 and 390×844. The retained manifests also contain two
`not-applicable` and two `unverified` coverage-only entries, for 260 total entries.
Six files changed in the working checkout during the audit; those concurrent
changes were excluded from the preserved rendering source. These are generalized
private-run observations, not the public synthetic fixture's state count or a
claim that every app page, feature toggle or reachable state was covered.

`scripts/workspace.py` owns initialization, distinct run directories and a small
derived catalog. The skill/package owner remains separate from consumer recipes,
synthetic fixtures, generated DOM and feedback. The workspace is ignored locally;
`docs/` is reserved for deliberately maintained explanations/decisions, and shared
synthetic recipes can be promoted to an app-owned test/story location. Old runs
are retained without automatic pruning; task-owned runtime scratch is cleaned.
The [workspace contract](../../../skills/ui-atlas/references/artifact-workspace.md)
specifies the paths, overrides, relocation, browser-note export and cleanup rules.

Result: **PASS** for the static and resource checks described below. Evidence
Coverage: **partial**. Highest evidence level: **resource-execution**, including
an author-run comparable rerun of the previously failed materialization cases.
This is not an independent fresh-agent execution on an unfamiliar repository.

| Observed failure or required behavior | Correction and checked result |
| --- | --- |
| A draft silently followed a changed element selection | Drafts are bound to state, evidence identity and element; navigating away/clearing and returning restores the original message/kind. Saved notes retain the correct selectors. Unsubmitted drafts remain tab-local, not portable exports. |
| Offscreen/overflow-hidden elements appeared searchable and fit to blank canvas | Observer, inventory and bridge share clipping logic. Full source rectangles remain available for geometry checks; visible rectangles govern inspection. Hidden-target search exclusion and direct bridge clipping passed. Legacy inventories get viewport rejection plus live bridge checks, not retroactive complete visibility evidence. |
| Fit-all stopped at 6% and left frames offscreen | Fit permits the scale required by content. Both twenty-row and single-row arrangements of 100 repeated synthetic DOM frames fit; the percentage remains nonzero/readable. These are layout stress fixtures, not discovered app states. |
| The 390px inspector covered the working canvas | A separate bottom inspector leaves a full-width canvas over 250px high in the 390×844 witness. Selection, payload access and adding feedback passed. |
| Partial quotes lost their qualification when saved/exported | Saved notes, inspector, opinion list, JSON and grouped requests retain `clipped`; a fully visible quote remains unmarked. |
| Matches after the first 200 were inaccessible | Paged search reaches item 420; Enter selects the first result on the active result page. Frame mounting remains intact. |
| Fixed materialized heights broke child-margin collapse | Computed auto height is preserved for eligible block containers while other resolved heights stabilize normal/native line boxes. The 3px guard remains unchanged; synthetic normal-flow, flex, grid/table and existing modal/control checks pass. |
| A run needs a predictable owner, safe retention and relocation | Default/custom init, repeat init preservation, ignore behavior, refusal to adopt a nonowned directory, retained failed/latest/history/pending entries and original-hash relocation checks pass. The capture CLI without `--out` creates the repo default path and reports a terminal failure there. Catalog source-check labels do not turn drift into a current-source claim. |

The author ran thirteen standard-library contract tests and the expanded browser
suite with Playwright 1.64.1 and local Chromium. Existing seven-state capture,
source/preview geometry, source/fixture drift, inert network isolation, replay,
hover/focus, disabled controls, frame/section movement, cross-state comparison,
label collision and multi-tab feedback checks remain passing. No original screen
images are introduced as frames. Tests own and clean their synthetic server,
browser and temporary outputs.

In the bounded app rerun, all fourteen earlier geometry failures across three
sheets and wide/narrow viewports materialized. Their independent HTML views had
maximum measured rectangle delta 0.047px, zero page errors and zero HTTP requests.
The rerun used the preserved source and synthetic fixtures, not a changing live
checkout. Private inputs/results remain with the user's selected artifact owner;
none are copied into this public package or regression fixtures. This verifies
those materialization failures, not every app page or transition. An earlier
interaction/recipe target failure remains outside these corrections, and native
host behavior, real external services and full mobile-device behavior remain
unverified.

#### Independent static challenge

A named read-only review challenger compared frozen baseline/candidate source
trees and synthetic test sources. It executed nothing and supplied no completion
approval. Its three independent candidates were accepted by the primary:

1. Newly inserted pagination buttons intercepted the search Enter shortcut.
   Enter now targets a result; first/later-page browser witnesses pass.
2. Generic overflow clipping crossed a native top-layer boundary. The shared
   helper now stops at the dialog/popover root. A modal nested inside a small
   clipping wrapper retains visible inventory, text, search and mouse/ID selection.
3. The opinion list omitted the partial-quote qualification already present in
   the inspector and exports. It now displays the qualifier beside the quote;
   the review-row assertion passes.

The primary separately added capture-time freshness to the new run manifest and
catalog, and validated visible-element bounds/status consistency. These were
not independent challenger findings. The public manifest was generated after
correction; the reviewer's frozen test manifest identified historical revision 3,
not its candidate. Final resource checks are author verification of the corrected
package, not a second independent semantic review or fresh workflow forward-test.

### Revision 3: section and review navigation

Revision 3 refines the existing DOM viewer after an observed navigation review.
At overview zoom, fixed-size section and frame labels could collide; section
headings did not follow moved frames. Search filtered frames, state navigation
discarded element selection, and stored feedback lacked a spatial return path.
The author changed the reusable viewer and aligned its recipe descriptions,
feedback fields, skill contract and resource checks. Product rendering remains
owned by the app; reference-editor content was not imported.

`catalog.js` owns section membership, readable names, element hierarchy, search
and conservative cross-state matching. `sections.js` derives bounds from frame
positions and owns description cards and title density/collision suppression.
The existing camera and per-note storage owners remain in place. A section drag
updates its member-frame positions; it does not introduce a second persisted
layout. Search preserves mounted DOM observations. Selection request IDs and
view revisions prevent stale asynchronous selections or deferred fits from
overriding a newer selection.

Optional observed journey descriptions carry purpose, action, result and
exceptions; existing conditions and ordered checkpoints retain their roles.
Unprovided explanations remain explicitly undescribed. Notes retain the v1
schema, with optional observation/proposal kind and open/reviewed status; older
notes retain their IDs and evidence. Review status never clears evidence drift
or asserts product-edit approval. The inspection bridge changed, so previous
feedback identities appropriately require reconsideration.

Observed on 2026-11-07. Result: **PASS** for executed static and resource checks.
Evidence Coverage: **partial**; highest level: **resource-execution**. These are
author-run browser and contract checks, not independent fresh-agent execution or
a comparable agent rerun. No general workflow-reliability claim follows.

| Must-pass criterion | Executed evidence | Boundary |
| --- | --- | --- |
| Readable spatial grouping | No visible section/frame title intersections at ten tested zoom levels from 6% to 400%; section dragging moved all member frames by the same delta; individual frame persistence still passed. | Deliberately overlapping user layouts may suppress labels; full names remain available through navigation and hover. |
| Explain observed states | Optional plain-text description validation/embedding, description inspector and ordered checkpoint list passed. Description-card and panel visibility controls passed. | Authored explanations require source evidence; they do not invent intended behavior or unobserved exceptions. |
| Retain comparison context | Unique counterpart selection preserved zoom and screen position; a hidden modal counterpart left selection empty, showed the limit and recovered when returning. A changed positional-path item was rejected. | Matching is conservative; uncertainty is shown rather than treated as correspondence. Frozen navigation is not actual replay. |
| Find and revisit elements | Search selected matching text without remounting frames; named-region tree and collapse/expand passed; opinion location links, pins, review status and status filters passed. | Broad visibility and complex occlusion retain the renderer limits below. |
| Preserve earlier contracts | Nine contract tests and the complete synthetic browser suite passed, including source geometry, modal/SVG/disabled selection, pan/zoom, source drift, inert previews, replay, cross-tab notes, legacy imports, provenance and terminal failures. | Same installed Chromium and synthetic fixture; browser and native-host generalization remain unverified. |
| Package integrity | Package validator, JavaScript/Python syntax, metadata, relative resource links and private-path/reference exclusions passed. Installed source remains the approved symlink to the canonical package. | Static checks do not establish fresh-session instruction uptake or agent behavior. |

Validation exposed an overly wide section-title hit area that intercepted empty
sheet drags. Limiting it to its displayed text corrected the behavior. Browser
assertions were also updated for the new opinion-list location and to await
deferred fit/visibility paint before measuring it; these were test timing and
locator changes, not removed behavior checks. Minimum-zoom section spacing was
increased so title readability does not depend solely on hiding colliding text.

The [revision-3 manifest](regression/package-manifest-v3.json) identifies the
package checked at that stage. The [revision-2 manifest](regression/package-manifest-v2.json)
records the exact file hashes identifying the prior DOM viewer. The source was uncommitted at that validation.
Public evidence contains portable resources, synthetic checks and bounded
outcomes only; private observations and reference-project content remain outside
the repository. Existing coverage and rendering limitations below still apply.

### Historical revision 2: selectable DOM canvas

Revision 2 follows an explicit change in the requested interaction model. The
revision-1 image board was the baseline, not evidence that image-only frames
could meet the new requirement. The requested outcome is a neutral, compact
spatial canvas with mouse pan/zoom, movable frames and selectable actual UI
nodes. Product rendering and state recipes remain authoritative; the viewer
must not become a second editable product or execute product side effects.

The primary refined the owning package and retained the existing state recipe,
source/fixture identity, coverage distinctions, replay and feedback contracts.
`snapshot.js` materializes actual HTML/CSS/SVG; `frame.js` restores display state
and supplies DOM inspection; `canvas.js` owns camera/gestures; `notes.js` owns
per-note persistence. The runner verifies source/preview geometry, and the
builder packages sandboxed inert frames. The viewer now puts detailed scope,
limitations and provenance behind an information panel and shows properties,
payload and notes on selection. Existing note IDs and the v1 notes schema remain
compatible; changed evidence receives a recheck marker.

Observed on 2026-11-07. Result: **PASS** for the executed resource and static
checks. Evidence Coverage: **partial**; highest level: **resource-execution**.
These are author-run checks against synthetic resources, not an independent
fresh-agent forward-test or comparable agent rerun. The earlier reviewer did
not review or execute this revision. No workflow-reliability or exhaustive-state
claim follows. The package was uncommitted at that validation; its fingerprint and
per-file hashes are in the [revision-2 manifest](regression/package-manifest-v2.json).
Fingerprint construction is the same as revision 1 below.

| Must-pass criterion | Executed evidence | Boundary |
| --- | --- | --- |
| Actual selectable DOM | Eight contract tests passed, including active-document and screen-image rejection, exact element inventory, ownership, source/support drift, incomplete states, required arrays and region bounds. | Supported HTML/SVG; raster asset pixels, CSS pseudo-elements and native internals do not become separate DOM nodes. |
| Preserve observed layout | Seven synthetic states rendered without generated screen PNGs; every visible element was measured in the generated iframe against its source rectangle. Native modal restoration passed. | 3 CSS pixel tolerance, with warnings above 1 pixel; geometry is not pixel-equivalence or animation evidence. |
| Sheet interaction | Browser checks passed for pan, pointer-centered wheel zoom, persisted frame movement, HTML/SVG picking, disabled controls and parent selection. | One installed Chromium browser and fixed fixture viewports; broader input-device/browser compatibility remains unverified. |
| State conditions and real replay | Held route history remains distinct before/after response; payload inspection, bounded actual replay and zero backend POSTs passed. | Forward rules are recorded, not every forwarded response body; mocks do not establish real service success. |
| Observation-only preview | Offline canvas made no HTTP requests; original app actions remain inert under the trusted bridge and sandbox. | The upstream fixture server still requires its own isolation. |
| Preserve feedback and gaps | Cross-tab add/delete, export/import, legacy stale-note import, search, narrow-layout provenance, clipped text, stacked-dialog observation and terminal journey failure passed. | Local-file storage portability and complex visibility remain bounded. |
| Package consistency | Package validator, creator frontmatter validator, syntax, metadata, relative links and resource checks passed. | Static acceptance is separate from behavioral evidence. |

The DOM implementation initially exposed resolved logical/physical CSS conflicts
and native dialog positioning differences. Physical-property serialization and
restoration from measured top-layer coordinates corrected the observed cases.
Waiting for animation frames left offscreen iframes unready; readiness now follows
font/state restoration and layout directly. These fixes are covered by the
geometry, modal and complete iframe-readiness witnesses. Pointer assertions were
corrected to use physical mouse coordinates under transformed iframes and account
for integer mouse positions and serialized transform precision; the zoom invariant
remains tied to the pointer's world position.

A static package check initially interpreted a JavaScript replacement token as a
skill reference. An equivalent replacement callback removed the ambiguous token;
the package check then passed. No repository-wide validator was weakened. The
regression suite is executable from its [owner](regression/README.md), which keeps
synthetic inputs separate from private application observations.

Remaining gaps include fresh-agent execution, unfamiliar frameworks, closed
shadow roots, nested frames, canvas/media/native host surfaces, transformed
native dialogs, popovers without a dedicated witness, complex clipping and wider
browser/storage behavior. Unsupported surfaces require an app-owned preview or
an explicit gap, never a screenshot substitute. The static canvas cannot monitor
source changes; rerun the source check and state recipe when resuming.

Public fitness of this revision was reviewed by the primary: portable code,
synthetic fixtures and bounded outcomes only. No private app content, machine
paths or reference-project content is part of the reusable package or record.
Local changes do not imply publication or human case acceptance.

### Historical revision 1 validation

The following evidence describes the earlier image-based board and its own
contract. It does not validate the revision-2 DOM renderer or new canvas gestures.

Observed on 2026-11-07. The primary authored and executed the resources. Browser
checks used Playwright 1.64.1 and an installed Chromium browser; standard-library
checks also passed on Python 3.9.6. The package was uncommitted, so its source
revision is null. The metadata fingerprint is SHA-256 of compact, sorted-key
UTF-8 JSON mapping package-relative paths to their file SHA-256 hashes, without
a trailing newline. The [v1 file manifest](regression/package-manifest-v1.json)
identifies those bytes; evidence files themselves are outside that fingerprint.

Result: **PASS** for executed resource and static checks. Evidence Coverage:
**partial**. This is resource-execution evidence, not a fresh skill forward-test
or comparable agent rerun. The independent role was a bounded read-only static
reviewer; it was not assigned production execution. The primary's app operation
cannot establish that a fresh agent will discover appropriate states and follow
the workflow on an unfamiliar app. That gap does not block the first usable
tool and bounded observation artifact, but does block broad workflow-reliability
or exhaustive-coverage claims.

| Check | Observed result | Limit |
| --- | --- | --- |
| Package and metadata | Repository package checks, creator validation, local resource links, UI metadata and script syntax passed. Optional design-skill references were reviewed as availability-qualified handoffs. | Static checks do not exercise the workflow. |
| Seven contract tests | Standalone safe embedding, source/fixture/support-file drift, image ownership and dimensions, incomplete states, missing inspection arrays and region bounds passed. | Declared dependencies only; no exhaustive dependency discovery. |
| Synthetic browser capture | Seven existing fixture states captured; one explicit unknown remained unknown. Held requests and bounded replay worked, with zero backend POSTs. | Browser presentation under synthetic responses, not real service success. |
| Inspection and feedback | Region/copy selection, filters, export/import, stale-note notice, independent notes from two tabs, deletion propagation and narrow-screen provenance passed. | Local-file storage behavior outside the tested browser is unverified; exports remain the portable backup. |
| Visibility and failure witnesses | Overflow-clipped regions/text were excluded; partial text was marked; top sibling modal text was included; a failure after the last capture returned code 2 and remained visible in the board. | DOM extraction remains heuristic for complex clipping/occlusion and unsupported rendering surfaces. |

The [regression owner](regression/README.md) provides commands and synthetic
inputs. Tests own and clean their loopback server, browser and temporary outputs.
The published fixtures contain no private app content or machine paths.

#### Independent challenge and corrections

A named read-only review challenger received a frozen package and regression
snapshot, not private app data or earlier conclusions. It checked the supplied
hashes and traced validation, capture, viewer, replay and feedback paths. It
executed no code and supplied no completion approval. Its six static candidates
were adjudicated by the primary:

1. Viewport-only clipping could expose text hidden by scroll/overflow panels.
   Ancestor clipping and a stricter hit check were added; hidden-region/text and
   partially visible text witnesses passed in the browser.
2. Missing `regions` or `texts` could pass validation and crash the viewer.
   Required arrays and text-to-region membership are now validated; omission
   witnesses are rejected by the builder.
3. Traversing only the first modal omitted a later sibling dialog's text.
   Observation now traverses the body and uses visibility/hit checks; the stacked
   sibling-dialog witness retains the top dialog's copy.
4. A failed action after the final checkpoint could vanish from the result.
   Journey failures now remain in the manifest, board and exit status; the
   terminal-failure witness retains its earlier valid capture and reports failure.
5. Whole-collection localStorage writes could lose another tab's feedback.
   Per-note storage and storage-event updates preserve separate additions; the
   two-tab addition/deletion witness passed.
6. Narrow layouts hid capture time, source-check time and global limits.
   The provenance disclosure remains available; its 390px witness passed.

The primary separately found that response fixture files could change without
altering recipe identity. Automatic response-file hashes and explicit
`support_files` now participate in checks and feedback identity. Contract tests
show that changed fixture bytes and a missing launcher are distinguished.
These corrections were verified through resources; the static reviewer did not
re-review the revised candidate or independently reproduce those checks.

An earlier replay cleanup emitted cancellation errors while closing held routes.
Explicit pending-route cancellation and context route removal corrected the
observed case; bounded replay subsequently completed with empty stderr. The
first creator-check attempt lacked PyYAML in the system interpreter; it passed
in an isolated cached validation environment without changing an app environment.

#### Revision 1 outcome and reuse

The initial package and synthetic regression suite are implemented. Public
fitness was reviewed by the primary: the record describes portable resources,
synthetic witnesses and bounded review evidence, without private source paths,
original captures, app associations or user content. This is a local repository
change; writing the record is not publication or human case acceptance.

Reuse the actual renderer and control its inputs. Keep unsupported states and
observation failures explicit. Review source and recipe identity before using
old feedback; a static HTML artifact cannot watch later filesystem changes.
Keep screenshot playback separate from actual replay and real end-to-end tests.

Remaining evidence gaps include independent fresh-agent execution, unfamiliar
frameworks, native hosts, shadow DOM/iframes/canvas text extraction, complex
transforms and wider browser/storage compatibility. A claim extending into
those areas requires its own bounded execution. No broader skill-reliability
or test-completeness claim is made.

## Work And Acceptance

The record-revision-9 pan/workspace changes are complete against their executed
synthetic/resource criteria. The user authorized repository commit and push after
the independent documentation reviews, necessary repairs and required checks;
only session-owned reusable changes are eligible for that publication. Current
private consumer state belongs to its private owner. Broader evidence limits
remain as stated above.

At the earlier record-revision-8 closeout, the reusable-package repair was closed
against its failure/control criteria and executed checks. This state does not close the consumer's separate recipe
question or the broader evidence needs below. The user subsequently authorized
repository commit and push after the two documentation reviews, necessary
corrections, required checks and preservation of unrelated work; that authority
does not publish the private consumer bundle or authorize product changes.

At that earlier closeout, private consumer outputs remained preserved at the
user's selected owner and had not been regenerated with that final package. The
fourteen materialization failures described under revision 4 had a bounded
successful rerun; the separate narrow-viewport interaction/recipe failure still
needed its target and intended behavior reconciled before being called a product
defect or a corrected state. Its next check belonged to that consumer's recipe
and source owner, not this reusable package. These are historical observations,
not a claim about the consumer's current state. The first fourteen-state recollection did not retain a full
package fingerprint for its intermediate candidate; a later retained snapshot
and synthetic checks identify the final revision-4 tool. That limits exact
whole-package replay of the earlier recollection without invalidating its
reported source/geometry observations.

Fresh-agent execution on an unfamiliar repository, native host and real-device
behavior, real service effects and wider browser/rendering coverage remain
unverified. They are follow-up evidence needs when making those broader claims,
not completed checks. The final synthetic/resource criteria are the basis for
closing the reusable-package repair.

## Outcome And Reuse

The pan/workspace changes passed the bounded checks above, including the
regressions for retained feedback. Reuse the metadata-driven selector and keep
transient inspection state distinct from saved opinions. Publication is authorized
after final checks; this record does not itself prove a successful push.

In the earlier repair phase, the two previously open findings and all additional
accepted candidates were closed for those criteria. No known actionable defect
remained from that final review; broader environment gaps remain the documented limits. That repair
phase changed no private app or retained consumer artifact and did not commit
or publish the work.

## History

- 2026-11-09, revision 10: added bounded consumer evidence for injected error
  provenance, omitted connected-source states and explicit Atlas refresh.
  Retained package identities, earlier resource checks, independent states and
  native/model/guidance-effect limits; no shared skill change is implied.
- 2026-11-08, revision 9: recorded direct workspace entry, in-view sheet selection
  and catalog, retained draft/pending-write ownership and the hand/Space pan repair.
  Twenty contract tests and the complete synthetic browser suite passed. Preserved
  the earlier closeout manifest, updated the current package identity, and applied
  the two independent documentation reviews without broad restructuring. Evidence
  remains partial resource execution; private consumer state is not published.
- 2026-11-08, revision 8: reconciled the selected observation model, general
  artifact ownership, optional automation and storage distinctions; corrected
  historical package links, manifest provenance and the record's content roles.
  Restored the consumer baseline counts and retained app-run gaps separately
  from completed resource repairs. Both independent documentation delta reviews
  found no further necessary correction; closeout checks passed for the
  authorized repository publication.
- 2026-11-08, revision 7: recorded the repair loop against package revision 5,
  eight independent static challenges, nineteen contract checks and the expanded
  browser regressions. The final inspected candidate had no additional material
  finding; coverage remains partial resource-execution evidence.
- 2026-11-08, revision 6: added the unchanged-package audit that reproduced
  ambiguous correspondence and skipped same-ID recovery imports, leaving both
  findings open rather than treating the passing earlier suite as sufficient.
- 2026-11-08, revision 5: repaired pending-note recovery, corrupt-run handling,
  fixed-overlay clipping, narrow comparison context and note freshness, with
  failure/control reruns and an independently challenged comparison-anchor fix.
- 2026-11-07, revision 4: established the consumer workspace and lifecycle,
  corrected seven observed usability/materialization defects, and incorporated
  three independently challenged regressions/omissions with bounded witnesses.
- 2026-11-07, revision 3: added movable sections, scale-aware labels, observed
  descriptions, element-preserving state comparison, search-to-element navigation,
  readable hierarchy, spatial feedback and explicit review status/view controls.
- 2026-11-07, revision 2: replaced image frames with selectable DOM states and a
  compact pan-and-zoom canvas; preserved recipes, feedback and explicit gaps.
  Added geometry, interaction, isolation and migration witnesses.
- 2026-11-07, revision 1: created the observation-layer skill, portable runner,
  offline viewer, synthetic regression suite and this bounded validation record.
  The repository catalog points to this single component-owned record.
