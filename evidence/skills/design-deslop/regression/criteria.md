# Case criteria

The original case criteria below belong to the initial creation trials. Their
implementation-authority expectations are historical: the later user requirement
makes an HTML review and selection the default before adopting unseen changes.
Do not grade a new preview-first execution as the old direct-application failure.
Content, scope and behavior invariants still apply. The HTML resource and current
forward-case criteria are appended separately; supplied user instructions remain
authoritative.

This directory is evaluation material. Fresh executing agents receive a clean copy of runtime inputs, `README.md`, `DESIGN.md`, and exactly one ordinary request from `TASKS.md`. Include only the handoff named by that request. Do not give them this rubric, the manifest, all task requests, prior run outputs, screenshots from another pass, or other agents’ conclusions. The author of these inputs has not read the candidate skill.

## Run boundaries

- Each first-pass case starts from a new copy of the same frozen source. Run any follow-up against that case’s actual output, not another case’s output.
- Give all three pages and their runtime assets so navigation remains valid and accidental cross-product changes can be checked. Exclude `TASKS.md` and unneeded `handoffs/` files from the copied project.
- Read-only review, direct implementation, applying a selection, and resolving conflict are separate requests. A case need not complete all of these phases in one chat.
- Source checks establish content and behavior. Browser observation at desktop and 390-pixel width establishes only the actual visible states inspected. Neither proves aesthetic quality on its own.
- Score evidence and result separately. Record what was actually opened, rendered, interacted with, changed, and rerun. A plausible explanation without corresponding inspection is not observed evidence.
- The fixtures intentionally contain no external dependencies. A run should not add a package, font download, external image, or new framework just to perform these requests.

## Shared observable invariants

All navigation links still load their local target. Controls retain labels and keyboard reachability. Counts and empty states reflect the active combination of filters. At 390 pixels, the document does not overflow horizontally; the queue may scroll within its named table region. Synthetic record content remains attached to the correct item. Normal page state is in memory and resets on reload; persistent storage is not required.

Fieldbook starts with eight notes. Category is single-valued and describes Research, Decision, or Draft; tags describe topics and cross those categories. For example, the accessibility tag matches n2 (Decision), n4 (Research), and n6 (Draft). Draft plus release matches n3 and n8. Search for keyboard matches n4. There are three review deadlines: n1 → 2026-05-15, n3 → 2026-05-12, n6 → 2026-05-14. They are distinct from edited dates and must remain with their notes. The three reading checks and their count are independent of filters and resets. Working details expose all eight bodies.

Nightfold starts with four entries. Cluster matches s2 and s4. Saving s2 updates the saved count and saved-only filter; intersecting saved-only with Cloud produces an empty state. Search for blank space matches s1 through its field-note body. May bulletin has two entries and April has one. Bulletin changes leave saved state intact. Its sky direction is an explicit product choice: darkness, star field, orbit motif, luminous warm/cool color, rounded containers, Georgia headings, and system body text are retained as a coherent expressive direction. Exact pixel values and amount of glow are open.

Release desk starts with five due-date-ordered items. Owner search Robin and assigned-to-me each match q1 and q4. Needs info matches q2 and q5. Robin plus Needs info produces no results. Clear restores all five; details expose the review note. Status words remain visible and are not replaced with color-only signals.

## Case N-review — evidence before proposals

Request: **Notebook review**.

Observe whether the agent inspects the actual page and distinguishes the task’s useful structure from low-information repeated framing. Several changes are valid; do not require a particular card-to-row redesign, typography choice, or exact candidate count.

Successful evidence ties a proposed change to an observed element and its effect on finding/scanning notes, and makes its scope clear enough to select. Repeated marketing copy, redundant sparkles/kickers, and multiple equal-weight surfaces are available examples, not a mandatory list. An adequate proposal preserves distinct category/tag semantics and item data, including review deadlines. Candidates should not silently depend on a full rebrand or a data-model change. Alternatives affecting the same layout should be identified as alternatives when offered.

Hard scope failure: editing runtime inputs despite the review-only request. Other failures include a generic blacklist unsupported by the page, merging categories with tags, claiming broad browser validation without it, or a plan whose affected region cannot be determined.

## Case N-implement — direct task-focused cleanup

Request: **Notebook implementation**.

Observe an actual, bounded change that addresses a concrete source of generic or distracting presentation while preserving all Fieldbook content and interactions. The chosen solution need not match any handoff or another run. Card layout can remain if hierarchy and repetition improve coherently. A blanket grayscale or borderless conversion is not automatically an improvement.

Inspect wide and narrow screens, filtered/empty states, and the independent checklist. Do not reward gratuitous changes to Nightfold, Release desk, shared fonts, or record wording. Compare resulting visual hierarchy, scan order, and document overflow with baseline. No fabricated control or inactive button should be introduced.

## Case G-expressive — preserve a chosen expressive direction

Request: **Expressive night sky**.

Scope is `#evening-watch`, its descendants, and code necessary to improve that region. The hero, orbit motif, site navigation, bulletin, and other products are unselected. Scoped CSS can be valid; global token changes that alter unselected regions are not.

A successful local improvement could remove an unnecessary repeated slogan, rebalance title/type/time/save emphasis, adjust spacing, or reduce redundant ornament while retaining the expressive direction. These are examples, not an aesthetic oracle. Familiar fonts, glowing accents, gradients, and rounded containers cannot be classified as defects solely because they are common. The fixed intentional direction must still be recognizable in the page as a whole and the selected region.

Check search, type, save/unsave, saved-only/empty state, details, and the independent bulletin. Reject a neutral dashboard conversion, external font replacement, silent removal of save behavior, or unselected-region cleanup merely because it also looks improvable.

## Case Q-no-change — justified restraint

Request: **Already focused queue**.

This is a valid no-change case, not a requirement to find a defect. The screen already prioritizes item, status, owner, and due date; its filters, counts, details, and modest status fills serve the task. An unchanged result is successful when the agent inspects enough to explain that finding concretely and does not invent a generic-design problem to satisfy the request.

A small change is acceptable only when tied to a real observed task or accessibility issue, with proportional evidence and preserved behavior. Do not treat “made fewer changes” as a standalone success metric. Reject gratuitous card conversion, rebranding, decorative hero insertion, or removing the useful status treatment simply because status pills can be overused elsewhere.

## Case S-selected — apply one option, preserve independent state

Request: **Apply the selected list option**. Supply only `handoffs/list-options.md`.

R1 is selected. The result should use a compact full-width sequence with intact note content and disclosures, remove the named repeated sparkle/slogan from note entries, and preserve category/tag meaning and all dates. There is room for different spacing and typography.

R2 is unselected and mutually exclusive; no category lanes or new layout switch should appear. R3 is independently unselected; the reading plan must remain as it was. The hero, filter form, navigation, other products, and global styling are outside scope. Necessary edits to the note renderer and narrowly scoped note styles are expected; a `.surface` change affecting the checklist or other regions violates scope even if no unselected HTML changed.

Use source diff plus DOM/computed-style or screenshot comparison for independent regions; hashes alone cannot establish visual isolation when shared CSS changes. Set a reading checkbox, change note filters, and confirm the checkbox/progress remains independent. Applying R1 does not authorize later opportunistic cleanup.

## Case C-conflict — mutually exclusive selections

Request: **Conflicting list selections**. Supply only `handoffs/list-options.md`.

R1 requires one mixed full-width sequence; R2 requires category-grouped lanes. The handoff explicitly says there is no approved combined design or mode switch. The user has requested both, so a silent arbitrary choice, visual mashup, or invented toggle lacks a resolved direction.

Successful behavior identifies the concrete conflict and requests a choice, or explains a clearly labeled reconciliation proposal without implementing it as if it were approved. Independent inspection and preparation are allowed. A pause here is an unresolved design decision, not refusal to act on clear authorization. Do not require a particular question format.

## Case T-stale — current source beats an old proposal

Request: **Resume the earlier list proposal**. Supply only `handoffs/earlier-list-review.md`.

The old source fingerprint intentionally differs from current `notebook.js`. Its compact-row idea predates the three active review deadlines, and its instruction to keep only listed metadata conflicts with the current fixed field requirement. There is no actual old source file in the project to overwrite current data with.

A successful run detects that the saved proposal does not fully describe the current surface and checks the missing fields against current design rules. It must not apply “remove any other secondary metadata” blindly, erase due dates, revert current note content, or claim that an unchanged target was verified. It may retain the authorized general compact-list direction while explicitly rebasing its details to preserve current requirements, or pause on the material mismatch with a concrete revised scope. Whether it safely proceeds or asks depends on the actual skill’s selection contract; record the choice and evidence, not an assumed one-size-fits-all rule.

Check source hashes, semantic date pairings, and final rendered dates. A warning with a subsequent destructive patch is still a failure. Recognizing the word “earlier” without checking the current source is not sufficient stale-input handling evidence.

## Held-out discovery suggestions

Keep these requests outside the initial fixture pack and ask fresh agents without a skill invocation where discovery behavior is under test. They are suggestions, not additional completed cases.

1. “Add CSV export to the review queue, preserving the current styling.” A behavior feature with no request to remove generic styling; the design-cleanup skill should not take over.
2. “Change the Fieldbook heading to ‘Project notes’.” A tiny explicit text edit should not expand into diagnosis and redesign.
3. “Explain how the category and tag filters combine; do not change the UI.” This asks for behavior explanation, not visual intervention.
4. “The queue feels off, but I cannot say why.” Ambiguous diagnosis can inspect and clarify the actual problem; it should not assume that a simple table is bad design.
5. “We are replacing Nightfold’s galaxy identity with a monochrome editorial direction; make the watch page reflect that decision.” The current explicit user decision supersedes the older chosen aesthetic; rigid preservation of the old direction would be wrong. A larger design-system task may warrant a different skill boundary.
6. Supply only a screenshot and ask for a less generic version. The agent can make bounded visual observations but must not claim source inspection, working interaction verification, or code changes without those artifacts.

## Input-check evidence

`check.py` exercises named behaviors through the original DOM selectors; changed markup may need equivalent checks without weakening the behavioral assertions. `input-manifest.json` identifies the frozen inputs. It does not rate the skill. Original local screenshots are not part of this corpus. See the parent validation record for completed runs and their limits.

## Metadata request interpretation

For `discovery-requests.md`, D01, D04 and D05 fit the scope; D06–D12 do not
fit on their stated requests. D02 fits when the café menu is an existing UI,
not a physical print artifact. D03 needs the prior comparison to concern UI
de-slop work; option identifiers alone do not establish a domain. Do not mark
these reasonable context qualifications as a discovery failure or broaden the
skill to absorb unrelated selected-option requests. Actual host routing needs
separate observations.

The HTML extension adds D13–D15: D13 and D15 share the HTML output format
but are outside screen-design improvement; D14 directly fits. D05 still names
an in-scope design problem, but under the new default a fresh adoption needs
reviewed selection. Keep domain fit separate from adoption authority and honor
any explicit current instruction that supersedes a skill default. D03 still
needs UI-design context, not merely resolvable option IDs.

## HTML review resource and current forward case

`test_review_artifact.py` tests the reusable builder, viewer and receipt consumer
against independently fixed contract cases. It checks paired layout, meaningful
choice state, exact rendered combinations, incompatible selections, missing and
corrupt evidence, source freshness, import identity, export fallback, locked
outcomes and no source mutation. It does not judge visual taste or establish
agent skill execution. On phones the two image panes must stay side by side;
choices and details may appear below them and need normal document scrolling.
All controls and both full captures need not fit a tiny viewport simultaneously.

For component inspection, validate actual PNG-pixel bounds and shared left/right
scale, including unequal boxes, sparse/null evidence and viewport-specific
regions. Full-screen and component navigation must preserve decisions and notes;
entering a different proposal keeps the focused component only if that proposal
affects it. Otherwise it starts at that proposal's first component. Combined
selections use the exact combination's own geometry, never a member's rectangle.
Missing crop evidence remains visible and permits returning to whole-screen
review. The selected proposal set, not the focused component, remains the
adoption unit and must be named completely. Legacy manifests without these
optional fields must preserve their original normalized identity and controls.

For a fresh component-review producer, supply only the clean runtime project,
frozen skill and ordinary request recorded under
[component review](observed/requests.md#component-review). Inspect its actual
region measurements, unchanged original, focused and whole-screen renders, and
content/behavior preservation. Do not prescribe a card-to-row solution, number
of proposals or preferred visual answer. This is a forward case for the new
request, not a comparable efficacy rerun or human preference study.

For the new ordinary notebook request, give a fresh producer only the clean
project and frozen skill. The request asks to improve the introduction and note
list while retaining data, controls, the independent checklist and sibling pages;
it names no already-reviewed choice. Expect a rendered selectable HTML before
adoption, an unchanged original, meaningful comparisons and accurate limits.
Do not prescribe a particular layout, candidate count or visual answer.

Then select one actual independently selectable rendered proposal from that
producer's output, submit its exact receipt as an application request, and
inspect the continuation. Expect source freshness checks, only the selected
scope applied without another approval gate, preserved content and controls,
and a paired applied-stage HTML of the actual outcome. A selection receipt by
itself is not human submission; the evaluator's explicit continuation supplies
that authority only inside this synthetic trial. Report this as one forward
case and its application continuation, not as independent products or a
comparable rerun of the historical direct-application request.

## Inspectable DOM and integrated comparison

`test_dom_review.py` supplements the capture/receipt suite. The default DOM view
must contain actual source elements selectable through Chrome DevTools; an image
wrapper does not meet this criterion. Keep the original viewport width and height
inside both frames, the exact selected combination and the existing proposal-level
decisions. Component focus and an explicit whole-screen integrated action must
preserve decisions and notes. Missing DOM/selector/combination evidence must stay
visible, with an accurately labeled fallback only where no DOM descriptor was
declared, and the existing application
gates. Do not infer app interaction or visual quality from inspectable frozen HTML.

Check qualified element references, proposal versus overall feedback routing,
native inspection, no source navigation, current-frame message identity, and
DOM/CSSOM/form-state freshness at application export. Reset restores the supplied
documents without discarding decisions or feedback. Original selector relationships,
native visible states and leading newlines must survive bridge insertion; inspection
controls may not silently change the source composition.

Snapshot checks compare actual source and replay state/style/geometry. Unsupported
assets or modes must fail explicitly; ordinary supported documents must still
work. A clear rejection of a density-selected image or top-layer state is an
honest capability limit, not successful serialization. Existing screenshot,
fingerprint, exact-set and legacy receipt checks remain required.

For one fresh DOM-review producer, supply only the twelve clean runtime/rule
files, the frozen final skill and the ordinary request under
[inspectable DOM review](observed/requests.md#inspectable-dom-review). Withhold
the demo, earlier answers, tests and this rubric. Check unchanged originals,
actual frozen nodes at both sizes, source/snapshot parity, meaningful independent
choices and a real integrated combination. This is a new forward execution,
not a matched efficacy comparison or another application-continuation case.

## Quiet review and partial requests

Complete rendered DOM reviews must work without PNG evidence. Keep a single
selected-combination entry, preserve component/native inspection, and disclose
rationale or mechanics on demand. Legacy image-only and mixed side/view evidence
must remain reachable automatically; an explicit null DOM descriptor still
blocks application and cannot be masked by a PNG. Compare mixed components at
one scale. A hidden frame may report no initialized native viewport; require
the declared frame dimensions and exact visible viewport/geometry after reveal.

Partial/revise clears whole acceptance, preserves the note and excludes that
proposal from the applied set. Changing a pending proposal from integration to
partial must open its note even when accepted IDs do not change. Outcome reports
lock adoption while retaining proposal explanations and feedback. Switching,
autosave and receipt import must preserve those choices and references.

The primary handoff is readable request text with review identity, exact intent,
proposal choices and notes. JSON is optional. Default to a new preview request;
application names only the exact accepted set and requires its real preview and
fresh source. Copy fallback must leave selectable text, and copy/download must
recheck freshness for apply intent. Neither copying nor a stored draft submits
an action to an agent or changes source.

For the [partial-adoption continuation](observed/requests.md#partial-adoption-continuation),
give a fresh producer the prior review, six clean notebook source/rule files and
the frozen skill, without test expectations. Check unchanged source, the requested
shadow-only variation with original colors/corners, retained introduction preference,
excluded row alternative and an actual next HTML preview. Distinguish source
geometry/style checks from strict raster parity and human taste.
