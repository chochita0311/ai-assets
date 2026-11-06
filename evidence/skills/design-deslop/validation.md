---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-design-deslop-validation",
  "revision": 6,
  "audience": "public",
  "subjects": [
    {
      "kind": "skill",
      "key": "skills/design-deslop",
      "source_revision": null,
      "content_sha256": "1fc8d392907f13ca65620dcca0e0400b6c171513ba7952ca77bf5397d1c9fea4"
    }
  ],
  "work": {
    "basis": "requested-extension",
    "state": "resolved",
    "readiness": "ready"
  },
  "knowledge": {
    "state": "supported"
  },
  "evidence": {
    "kinds": [
      "static-observation",
      "generalized-private-observation",
      "illustrative-synthetic"
    ],
    "maturity": "comparable-rerun",
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

# Design De-slop workflow and validation

## Context And Applicability

The [design-deslop package](../../../skills/design-deslop/SKILL.md) addresses
existing screens whose interchangeable presentation gets in the way of their
content, task or chosen identity. Every result now includes a paired HTML review:
the original on the left and the proposal or actual applied outcome on the right.
Unseen changes stay in previews until selected; a submitted selection authorizes
only its reviewed scope. Item decisions and overall feedback preserve room for
disagreement, another direction, or keeping the original. Whole-screen context
and measured component focus preserve the same proposal-level choices and notes;
inspectable regions do not silently divide inseparable adoption scope. Frozen
HTML/CSS now preserves native elements for DevTools and qualified feedback, with
an exact-selection whole-screen view, partial/revision choices and a readable
agent handoff. Complete DOM reviews no longer need screenshot evidence; legacy
fallback is automatic only where a DOM descriptor was not declared.
It does not detect AI authorship, impose an aesthetic blacklist, create a new
brand, or turn a local design request into a comprehensive product audit.

The requested development included independent case exploration, implementation
and verification. The skill owns runtime instructions and reusable HTML resources; this record
owns their creation and refinement evidence. [Synthetic regression material](regression/README.md) owns
portable inputs, ordinary requests, evaluator criteria and browser checks.
Neighboring design skills remain optional boundaries, not required dependencies.

The candidate preserves product truth and intentional character while allowing
composition changes and explicitly scoped rule departures. Original retention
is a valid choice. Familiar fonts, glow, cards and gradients are contextual
signals, not mandatory defects. The pinned Impeccable source informed the
pattern reference; that reference does not import its entire workflow.

## Evidence And Evaluation

### Initial creation trials: earlier user contract

The following creation results predate the later request for HTML review before
adopting unseen changes. In that earlier task, a generic in-scope implementation
request authorized local design decisions; the observed stop-for-selection was
a failure under that contract. The later user explicitly changed the default.
Neither the earlier failure nor its successful rerun is reclassified retroactively.

### Snapshots and execution conditions

The primary authored the entry, metadata and proposal scaffold. A separate
worker authored the contextual pattern reference. Another worker, without the
candidate skill, designed three synthetic products and their acceptance
criteria. The primary supplied each executing worker an ordinary request, a
clean project, only its relevant handoff and a frozen skill snapshot.

Workers used separate contexts without parent history. Evaluator criteria,
other results and candidate-author rationale were excluded by instruction,
not operating-system isolation. One no-change worker enumerated sibling file
paths while looking for project instructions but reported opening no sibling
contents; this limits a stronger isolation claim. Workers shared the available
runtime and baseline instructions. No model override was requested, and the
actual runtime model/version was not independently exposed. Logical role names
do not establish distinct models or independent human judgment.

Local execution used Python 3.14.6, Playwright 1.64.1 and installed Chrome 156.0.8078.88.
Common browser checks used 1440×1000 and 390×844; case workers checked additional
states and some intermediate widths. Counts of assertions within a fixture are
not independent samples. No external asset service, live-site mutation, global
skill installation or publication was part of the trials.

The initial source package was uncommitted during evaluation, so source revision is
null. The package content fingerprint is SHA-256 of the UTF-8 compact JSON object
mapping relative file paths to their SHA-256 strings, with sorted keys and no
trailing newline. Its aggregate fingerprint was `c9fca7d1214824a341781a2f2c72e20f12fc58e18ef422d6b6ea46a0ef29714f`.
Component fingerprints identify the actual supplied bytes:

| File | Revision 1 final snapshot SHA-256 |
|---|---|
| `SKILL.md` | `cd98f29d275cfe9c4ae8c2ceffe375e34f944a891c4307dddf079b8a1588d911` |
| `agents/openai.yaml` | `8a27cf606680a752e13b24aab1a1225701a9d9ea152fccdb970074a0e14ee53b` |
| `references/patterns.md` | `6fcef9d08707224f1f3ae5b53d10831a1b3029a33e73e5586ad5376ed70448c3` |
| `templates/proposal.md` | `3964d9db3e18c47fb7011a141d19f1b290fae94037c0821809f66869bfce1847` |

The first entry snapshot was
`502ac8ccf6f37ae08d921563623eadd9e3d50da1f4098b52e7b9c6c262602965`.
The second was
`19c042051b4286f2d50c5f5b5fe8c892efa003d267e9cf5b059890ceca4fff1a`;
it changed only discovery wording. The third changed discovery and the
implementation-authorization paragraph. The other three files remained identical.

### Discovery and the observed authorization failure

Twelve metadata-only requests covered comparisons, a selected proposal,
preserving an expressive palette, delegated implementation, a login bug,
authorship detection, a new brand, pixel matching, a full accessibility audit,
an exact spacing edit and prose rewriting. The first fresh classifier made
eleven clear intended classifications but treated delegated implementation as
conditional because the description said only "user-selected" changes.

The description was revised to name explicitly delegated changes. A different
fresh classifier matched the initial twelve expected decisions: five eligible
and seven ineligible. Those expectations assumed the menu was a screen and the
prior comparison concerned UI design. This was metadata interpretation, not
observed host routing.

A fresh execution then exposed a separate entry-contract problem. Asked to
inspect a named expressive region and make a focused improvement, the second
snapshot's worker built a runnable alternative but left the working project
unchanged and requested selection. It cited "Do not apply an unselected design"
and required an exact selected design or separately delegated choice. The
rendered proposal preserved identity and behavior, but stopping short of the
requested implementation was an authorization failure.

The primary revised the contract: a request to implement improvements in a
named scope authorizes necessary local design decisions without another gate;
requests only to review, suggest or compare still authorize previews. Material
conflicts still require a decision. This preserves user choice without making
ordinary implementation depend on special wording. Final discovery wording was
aligned with that distinction.

A fresh worker received the same expressive request and clean inputs with the
third snapshot. It implemented the focused change without another selection
gate, retained the chosen galaxy identity and unselected regions, and passed
the stated browser/preservation checks. This is a comparable rerun of the
observed authorization failure; it does not establish repeated-run stability.

Final metadata interpretation retained three clear positive and seven negative
classifications, while properly qualifying two underspecified requests: a café
menu must be a screen, and a selected option ID needs prior UI de-slop context.
The primary corrected the evaluator expectations to retain those conditions;
no broader trigger or additional package edit was justified. The original
classifications remain reported above. [The twelve requests](regression/discovery-requests.md)
are retained independently of their evaluator criteria.

### Forward executions and primary adjudication

Eight distinct tasks were executed, with a ninth execution repeating the
expressive task after the authorization correction. They are bounded examples,
not eight independent product studies.

| Case / supplied snapshot | Observed result | Limits and retained evidence |
|---|---|---|
| Private note archive comparison / first | Two rendered reading-versus-index directions; original source unchanged; content, search, taxonomy, pagination and detail checks passed at two sizes. A pre-existing mobile navigation problem was a separately selectable proposal. | Generalized private observation only; raw sources and captures are not distributed. No live adoption or preference measurement. |
| Synthetic comparison-only notebook / third | Original unchanged; independent header and filter proposals plus quiet-card versus index-row alternatives, with a combined preview. All six surfaces passed the worker's checks at two sizes. | [Desktop comparison](regression/observed/compare-desktop.png), [record options](regression/observed/compare-options.png), [phone comparison](regression/observed/compare-phone.png). Index rows were explicitly not denser on desktop. |
| Delegated notebook implementation / third | Applied a compact working index without another approval gate; eight records, separate category/tag roles, dates, disclosures and independent checklist retained. | [Observed patch](regression/observed/delegated.patch). First phone title moved from about 946 to 532 px; user scanning speed unmeasured. |
| Expressive local improvement / second, then third | Second stopped at comparison despite requested implementation. Third applied the focused change, retained the galaxy identity, hero, bulletin and siblings, and passed browser checks. | [Rerun patch](regression/observed/expressive.patch). Names moved higher inside cards; one successful comparable rerun, not stability or superiority evidence. |
| Already focused review queue / second | Inspected and retained the plain table; statuses, dates, filters, disclosures and keyboard access served the task. Source unchanged. | Mobile inner table scrolling was permitted; no gratuitous restyling. This is an observed no-change outcome. |
| Selected R1 only / second | Applied compact rows; R2 and R3 remained unselected. All dates, taxonomy, filters and independent checklist retained; shared tokens and siblings unchanged. | [Observed patch](regression/observed/selected.patch). Relevant body rules are unchanged in the third snapshot; this case was not rerun with it. |
| Stale E1 proposal / third | Detected source fingerprint mismatch, reconciled the old field list with current rules, and retained three new review deadlines while applying the authorized compact list. | [Observed patch](regression/observed/stale.patch). Static stale input was exercised; no live concurrent editor race was simulated. |
| Incompatible R1 + R2 / third | Identified mixed rows versus category lanes as mutually exclusive, left source unchanged and requested a concrete choice. | No arbitrary hybrid or new toggle. Baseline renders checked; interactive execution was unnecessary for this unresolved design choice. |

The primary inspected rendered artifacts, scoped source differences and
preservation evidence, and ran the portable behavior checker on implemented
synthetic outputs. Selected-only changes preserved the record data and event
handlers. A shorter list moved the independent reading panel upward on phone
through normal document flow; its appearance and internal geometry were
unchanged. This is distinguished from unauthorized restyling of that panel.

The private-site comparison is a generalized private observation. Original
content, paths, hashes and captures are excluded from this public record. It
does not establish public reproduction or improvement in actual reader success.
The synthetic trials have their own inputs and outcomes; they do not inherit
that private observation's result.

### Test-resource correction and negative controls

Before synthetic case execution, a real fill-then-click sequence found a defect in the
synthetic inputs: redundant input/change listeners rerendered the list on blur,
consuming the first disclosure click. Initial programmatic input-event checks
had missed that sequence. The fixture author reproduced it, removed redundant
filter-form change listeners on all three pages, refreshed the current handoff
hashes, kept the old handoff deliberately stale and reran all three pages at
two widths. All affected synthetic inputs were refreshed before use. This was a fixture
repair, not a skill failure or evidence of improved skill behavior.

The maintained browser checker passed six baseline runs. Four deliberately bad
edits were separately detected: dropping a review deadline, resetting independent
reading state during filtering, restoring the blur-rerender defect, and removing
written status labels. These controls demonstrate those checks' sensitivity,
not comprehensive detection. The checker cannot establish visual quality,
complete semantic accessibility or untouched-region isolation on its own.

The delegated implementation worker also corrected label-matching and
animation-frame reset-wait assumptions in its own checker before the final
passing run. The product's existing reset behavior was retained; these were
test-harness corrections, not additional skill or product fixes.

Independent file reviews of the second and third snapshots found no supported
material contract contradiction or missing resource. The later execution failure
after the second review demonstrates why static review alone was insufficient.
The final review did not receive trial outcomes and supports only its inspected
contract scope.

Repository package validation and platform frontmatter validation passed. The
three optional neighboring-skill references were reviewed as availability-qualified
boundaries. UI metadata, local links, source fingerprints, record metadata and
portable content were checked. All four retained output patches reconstruct the
observed edited files exactly from separate frozen inputs. Four implemented
synthetic outputs passed the primary's browser checks at both sizes. These are
integration/resource checks, not four additional fresh agent trials.

### HTML review extension: new user requirement

The user requested a Git-diff-like HTML with simultaneous before/after panes,
per-change acceptance and rejection, visible evaluation questions and feedback,
and a way to stop or adopt parts of repeated drafts. The prior entry and Markdown
scaffold did not provide that artifact. This was a requested extension and a
change of adoption preference, not evidence that every prior implementation was
wrong. The two HTML reference pages informed explanatory artifacts, side-by-side
variants and exportable decisions; their narrower contribution and links are in
[the HTML contract](../../../skills/design-deslop/references/html-review.md#sources).

The primary set the authority, manifest/receipt contract and implementation
boundaries. Separate no-history workers built the viewer and stdlib helper;
another froze expected resource cases before seeing implementation. The viewer
and helper own separate files. PNG captures are actual isolated product renders;
the helper does not generate designs, capture screens, write product source or
communicate decisions to an agent. Selection exports are requests only when the
user actually submits them. Exact reviewed selections proceed without a second
approval ceremony. New rounds retain reasons and identity but cannot silently
transfer approval to a changed selected design or impact.

A no-history static challenger found two bounded issues. The missing written
feedback in a zero-proposal review was accepted and repaired with an overall
note, including export, import and draft persistence in all stages. The helper's
review-wide source check was retained as a conservative freshness boundary: it
checks every recorded baseline file, even one belonging to an unselected option.
The entry/reference now explicitly reconcile unselected independent drift,
refresh affected evidence and map unchanged submitted scope without another
approval solely for a new artifact fingerprint. No automatic per-proposal file
inference was added. The primary also corrected the content scaffold to give
alternative variants distinct IDs in a shared group, matching the manifest.

Independent resource testing first passed 17 tests. A proposed extra mobile
assertion incorrectly required captures to remain onscreen while the user
scrolled to choices below; it was corrected to test simultaneous visible panes
when returning to the comparison. Image capture waits were strengthened to wait
for decoding. These were test corrections, not implementation failures. After
the overall-note repair, all **18 tests passed: 7 CLI/consumer and 11 actual
Chrome tests**. They cover exact combinations, alternative/dependency/conflict
states, absent/concept/corrupt captures, identity and stale sources, no-change and
locked outcomes, actual export/import, notes, storage/clipboard fallbacks,
keyboard focus, paired scaling/scrolling and no source/network effects. Phones
were emulated at 390×844 and 320×568; desktop was 1440×1000. This checks a browser
resource, not aesthetic preference or agent task behavior.

The revision-2 resource suite used Python 3.11.15, Playwright 1.64.1 and Chrome
156.0.8078.88. Its seven stdlib cases also passed on Python 3.9.6; eleven browser
cases were intentionally skipped in that compatibility run. The builder author
had separately run sixteen initial stdlib cases, not sixteen additional agent
trials. The primary generated and inspected the [standalone synthetic example](regression/observed/review.html),
selected a real combination and checked its exported receipt against the frozen
synthetic source. A first primary probe used an eval-based wait rejected by the
artifact's CSP; locator readiness assertions corrected that probe without
weakening the artifact. This example is author-built, not the fresh producer's
output and not evidence of a preferred design.

### Fresh HTML workflow executions

Two new ordinary tasks were run in fresh no-history producer contexts: a
notebook improvement, followed by its selected application in the same producer,
and a separate review-queue task. Producers received clean copies of the twelve
runtime/rule files, one frozen skill and only their request; they were told not
to inspect evaluator criteria, other outputs or author conclusions. Isolation
was instructional, not filesystem-enforced. The actual runtime model/version
was not independently exposed. The [requests and continuation](regression/observed/requests.md#html-review-and-selected-application)
are retained without task-local paths.

| Task / stage | Observed result and primary evidence | Limit |
|---|---|---|
| Notebook proposal | Returned actual N01 introduction and N02 index previews, plus their exact combination, in a self-contained paired HTML. Included desktop, phone and filtered/disclosure views. Primary verified all twelve original files unchanged and inspected the real artifact. | One producer and synthetic product; a proposed benefit is not human preference. |
| Notebook N02 application continuation | Primary selected only N02 through the actual HTML and submitted its exported application receipt. Producer checked freshness, applied only the three notebook files without another approval gate and returned applied-stage HTML. Primary verified all source files match the reviewed N02 preview, all three actual captures match its reviewed PNG bytes, and the maintained notebook behavior checker passed at both sizes. | N01, reading markup/styles, tokens and siblings retained. No live concurrent-edit race. [Observed patch](regression/observed/html-selected.patch) replays source, not the whole temporary UI session. |
| Review queue retained | A separate producer inspected the already focused table and kept it. It returned paired retained-stage HTML for nine actual states/views with editable overall feedback and locked adoption controls. Source/behavior checks covered dates, written statuses, filters, reset, disclosures, focus and inner table scrolling. Primary inspected the HTML capture and verified all twelve source files unchanged. | The phone table needs its permitted internal horizontal scroll; not all columns fit at once. Five synthetic records and one browser engine. |

The notebook producer used intermediate package
`70365d7057d38b381f2a9381f12e4884b7315cb1292ee5a884d0144f0a023a21`
for both proposal and continuation. The later queue producer used
`0097e43c199b45b45524627c843cf51671f9dbc9c483e86590c10d4d696236f4`,
which adds overall feedback and the source-reconciliation clarification. The
revision-2 final package differs from that queue snapshot only in the proposal scaffold:
distinct variant IDs within one group and an overall-feedback prompt. That last
scaffold correction received static/contract checks, not another fresh producer
execution. Both snapshots and their relationship remain explicit; the notebook
trial is not claimed to exercise a later control it did not load.

### HTML extension discovery and package checks

A fresh metadata-only worker received the unchanged twelve requests plus three
HTML-specific requests. D01, D02, D03, D04 and D14 were classified as fits, D05
as needing adoption context, and the other nine as outside scope. The worker
qualified the existing-screen context for D02/D04 and the prior review for D03.
The primary retains the stronger D03 condition that the prior comparison must
concern UI design; resolvable IDs alone do not establish a domain. D05 names an
in-scope design problem, while its immediate autonomous adoption is a separate
question under the new review default. Explicit current user instructions remain
authoritative. This interpretation is not actual host routing, and does not
justify broadening the skill to code-diff HTML or interactive prose artifacts.

Repository package and platform frontmatter validation passed. Optional adjacent
skills remain availability-qualified boundaries. Local resource links, UI metadata,
JSON record metadata, input/observed-output fingerprints, portable source content
and whitespace were checked. The new selected patch reconstructs the actual
observed files from the original input. These are package/integration checks,
not further fresh trials. At that revision, the standalone example embedded the
then-current viewer and captures without depending on the discarded capture
workspace. The component extension updates that example below.

Revision 2's final uncommitted package fingerprint was `fad1a650c78c4e44bde4223d6064f469b1feba398cd5fad7cbd14d8bd9a3074b`. It is computed by the
same compact sorted JSON file-hash map used above. Revision 2 component bytes:

| File | Revision 2 final SHA-256 |
|---|---|
| `SKILL.md` | `fd4fa484a4f868a7839bf74426cfa47ac71a9fdd9964804ded9eded37e8a7773` |
| `agents/openai.yaml` | `6ee6d084a7ced88e40820be6680b0a3490c67184c1520f1e46668849e16d9066` |
| `assets/review.html` | `496c22fe0ae931637079636f1f922d988e9403b8e7d23d5bf9b075b2bbf0ce66` |
| `references/html-review.md` | `7a02cc952d38571d7229f514f4436729dfd2c9330b450d4aff9775f976792f61` |
| `references/patterns.md` | `6fcef9d08707224f1f3ae5b53d10831a1b3029a33e73e5586ad5376ed70448c3` |
| `scripts/review.py` | `23ad6fbbc632b4e295e21333c7c4e92e5d62ab1105086d22d865af3f9a1ede0c` |
| `templates/proposal.md` | `b735960567bdc1a4530efc663eab362aa08822c9083ddd4c20024b995926a18d` |

### Component inspection and viewer refinement

The next user request identified two gaps: inspect each changed component in
addition to the full composition, and improve the review tool's own generic
appearance. Passing the earlier eighteen resource tests had established the
covered mechanics, not user preference or readable component comparison. The
primary froze revision 2's seven-file package and its actual standalone example
before editing. Separate workers owned helper validation, viewer implementation
and regression checks; the primary owned semantics, documentation, examples and
integration. A later context restart required two recovery workers to continue
from those files, not fresh independent implementation trials.

The extension adds optional component identities and measured regions to the
existing version-1 manifest. It validates finite, correctly scoped rectangles
against each actual PNG's full dimensions. Missing/null regions remain explicit;
full-screen review is still available. Old manifests retain absent fields and
original fingerprint semantics. Each side uses its own rectangle at one shared
scale. Exact selected combinations use their own measured regions, and a focused
component never narrows the complete selected proposal set. Choices, notes,
constraints, receipt schema and source-freshness checks remain owned by their
existing mechanisms.

The viewer worker loaded the skill and contextual patterns, then inspected real
baseline desktop and phone renders before choosing changes. It observed repeated
choice frames, ordinary draft text presented like a warning, and feedback below
long provenance. The candidate retains the system font, useful green decision
accent, conventional labels, simultaneous panes and explicit status text. It
uses separated proposal rows, component/full-screen navigation, and the comparison
question, benefit, tradeoff and feedback before expandable supporting detail.
Normal draft guidance remains at the stage/footer; genuine missing evidence
stays visible. During recovery, a readiness label implying human review was
restored to the actual displayed-and-decoded check, and duplicate ordinary-preview
text was removed. These were author-guided implementation passes, not fresh
answer-isolated skill executions or human aesthetic approval.

The viewer worker rendered twelve actual states at 1440×1000 and 390×844 with no
JavaScript errors or outer horizontal overflow. In the author-built example,
the same N02-A task and data show a note at 100% on desktop versus the previous
whole-page view's 35%. With the phone capture selected on both tools, the
comparison is 46% versus 43%; an earlier baseline observation of 12% instead
showed a desktop-width capture in a phone browser and is not that matched
comparison. The 441-pixel card and 898-pixel row retain their real width
relationship at a shared 57% on desktop. These are layout observations, not
measured comprehension, taste or task-speed gains. A phone viewing the desktop
row remains small at 18% fit; its phone capture and 100% scroll are alternatives.
Component focus hides surrounding composition until toggled, and detailed
provenance now takes an extra disclosure action.

### Component resource checks and semantic challenge

The final resource suite passed **31 of 31 tests: twelve CLI and nineteen actual
browser cases**, preserving all eighteen earlier tests and adding thirteen.
Execution used Python 3.11.15, Playwright 1.64.1 and local Chrome
156.0.8078.88 extended on macOS 26.5.1 arm64. The twelve CLI cases also passed
on system Python 3.9.6; nineteen browser cases were intentionally skipped in
that compatibility run. New cases cover real PNG bounds, malformed/sparse scope,
legacy normalization, unequal crops and shared-scale pixels, focus/decision/note
preservation, combination-specific geometry, missing evidence, and locked stages.

The first complete browser run passed 29 and failed two new assertions. Actual
fractional-edge resampling affected a one-pixel-inset RGB sample; moving the
sample three CSS pixels inside retained the same ±1 RGB tolerance and independent
geometry assertions. The other assertion expected an old focused record after
accepting a different list-only proposal. The established contract enters the
new proposal, so the corrected test first verifies list focus, then explicitly
selects the record and checks the exact combination's independent rectangle and
export. The primary adjudicated both changes; neither required changing correct
runtime selection or crop behavior. The full suite then passed. An earlier
sandboxed Chrome launch failed before browser assertions; authorized local Chrome
execution resolved that environment failure. It is not a product regression.

A separate read-only semantic challenger traced regions, exact-set readiness,
normalization, drafts/imports, locked outcomes and receipt consumption against
the frozen baseline. It found no evidence-backed material defect candidate;
static review alone did not approve the change or establish browser behavior.
The primary additionally loaded the complete pre-extension HTML with the new
helper and checked a matching synthetic legacy receipt against its five baseline
source files. The original fingerprint remained intact. This was read-only
compatibility validation, not human submission or application.

The primary inspected the actual final demos, exported the real N01+N02-A
selection after component/whole-screen navigation, and checked that receipt and
five baseline source files. In the real phone-capture list at 100%, the two
component heights were 2352 and 1411 pixels in 599-pixel viewports; linked
scroll reached their respective ends at 1753 and 812 pixels. The viewer's own
comparison supports three measured areas plus whole-screen context, locked
implemented-tool choices and editable individual/overall feedback at both sizes.
These probes produced no JavaScript errors. Browser tests do not directly cover
every combination of component mode with restored/imported decisions or a mixed
set containing a legacy proposal without component metadata; static tracing
covered those selection paths, and that runtime matrix remains a limit.

### Fresh component-review execution

One fresh no-history producer received the final frozen seven-file package, a
clean copy of the twelve runtime/rule files and the ordinary
[component-review request](regression/observed/requests.md#component-review).
Prior outputs, the example, criteria and author conclusions were excluded by
instruction, not filesystem permissions. It loaded the supplied skill and
returned N01 (introduction), N02 (note list), their exact N01_N02 combination,
and four inspectable components: introduction, list title/total, whole list and
a representative note. N02 explicitly bundles its three affected components.
The introduction proposes a Georgia heading as an open visual choice; the run
did not treat a familiar typeface or the original pastel style as inherently bad.

The producer captured sixteen real images across original, introduction-only,
list-only and combined previews, each at desktop, phone and the corresponding
filtered/open-detail states. It reported checks of all eight records and three
review deadlines, category/tag distinctions, body search, compound filters,
sorting, reset/empty results, keyboard disclosures/focus, independent reading
state, reduced-motion layout, and the review controls/export. No original
project edits or source application occurred. Its test-only selection receipt
was validated read-only and removed; it was never a human submission.

The primary verified all twelve original file hashes unchanged and that preview
changes were limited to the notebook HTML/CSS/renderer: introduction-only changes
two files; list and combination change three. Shared tokens and sibling files
were unchanged. The maintained notebook behavior checker passed at 1440×1000
and 390×844 on the combined preview. The primary loaded the actual self-contained
artifact, inspected its note comparison, and checked real focused geometry at
both sizes against each side's recorded rectangle and shared scale. Whole-screen
navigation preserved the note; these inspected HTML states had no outer horizontal
overflow or JavaScript errors.

The trial review fingerprint was
`90ec9eb3c905175e67fc8492316ecaa45040bf27abb301cdc21e62c6c1f7a505`,
with HTML file SHA-256
`2264827e7498b367895d7c62e4336bcfbb51af10e4f7c02fed1dd2837e7b1d08`.
Its temporary sources and captures were used for the completed evaluation, not
retained as a preferred answer or substituted for the reproducible public demo.
This is one new forward execution, not a matched before/after efficacy rerun,
repeated-run stability result, or another application-continuation trial.
Human preference, task-speed effects, physical mobile and other browser/assistive
technology behavior remain unmeasured. The actual producer model/version was
not independently exposed.

### Component package and artifact identities

The revision 3 component-review package fingerprint was `ce0a0b4294853846d9cb309a744aae9880169765737e3cda2db9421cc566a6cf`. Its seven
files, frozen for the fresh producer, are:

| File | Revision 3 SHA-256 |
|---|---|
| `SKILL.md` | `4455bca26a02e73b8b486334dbf95e6ab10ea410a3e57bea61431cb7c17bd2fd` |
| `agents/openai.yaml` | `d72e4e4ff2b3dfe19cee50e447ebfab0b0be64eca9f759818c54d981a8fcc982` |
| `assets/review.html` | `3f4df82a92f5e0a1417cf7a4826598f9eab18580ab5303c124bf8191d54fecc9` |
| `references/html-review.md` | `409152c4edcd1cdca598c05ca1dfc50c1cdd11d3de354e1c0a2d9263bc61305c` |
| `references/patterns.md` | `6fcef9d08707224f1f3ae5b53d10831a1b3029a33e73e5586ad5376ed70448c3` |
| `scripts/review.py` | `23870884307ab3adbaae38d52b8b35f8b874418a57d47835036b4b24cbb43bdf` |
| `templates/proposal.md` | `12843193648888ef160588a07e926135b365485982d483fb70bc575fc383134c` |

The revision 3 selectable synthetic review embedded real component and
exact-combination captures; its durable path now holds the later DOM revision.
The [tool before/after review](regression/observed/viewer-review.html) still
records that historical component-viewer change; its choices are locked and its
feedback is editable. Neither represents an adopted real-site design or global
skill installation. Both were self-contained with no temporary/server dependency.
The [component screenshot](regression/observed/compare-components.png)
retains the actual revision 3 browser view, not the later DOM interface.

| Revision 3 artifact | HTML file SHA-256 | Embedded review fingerprint |
|---|---|---|
| `review.html` | `6c480267286a85d9d2543266f94acb563c6bf290a6619cc0f040cb272d77e5ad` | `9a4b28f363da258398d410252c110a2ebbfe227306edf41248da65eccb3961f8` |
| `viewer-review.html` | `0a189d8f52a7552af469edb2d4612d42f70060e2890295abf9733b4ef1f5fabc` | `8a5d2c23e8b67e4818e02cb40a787de747f7207f2962c359314e3e4581a0eade` |

The preserved pre-extension demo used file SHA-256
`5ac6d89e84c13e709f9fa555540f33d27551c22520483adc8fc0a5b2fca80b62`
and review fingerprint
`dee926454fa460c48c68415bc929335d21bc8a3ce92e965d7424602a0b6c526c`.
Its actual appearance is embedded in the tool comparison; its task-local original
was used for compatibility checks and then removed.

Repository package validation, platform frontmatter validation, record JSON
schema, local Markdown resource links, metadata and Python syntax/whitespace
checks passed. All fifteen frozen fixture inputs still match their recorded bytes
and fingerprints. Portable retained sources contain no private user paths.
The three optional adjacent skill references remain qualified by availability.
The discovery description did not change, so the earlier fifteen metadata probes
were not repeated or claimed as new host-routing observations. The component
prompt, scaffold and detailed contract were updated together.

### Inspectable DOM and integrated whole-screen extension

The next user request identified a concrete limit of revision 3: the before/after
panes were images, so Chrome DevTools could not select the product's real elements
for a change request. Component review also needed a direct integrated whole-screen
action. This extends the representation and navigation contract; it does not
authorize adopting a new product design. Revision 3's seven-file package and actual
HTML were preserved before editing as the baseline identified above.

The primary fixed the manifest, authority and viewport contract before delegating.
Separate workers owned the snapshot/helper, viewer and independent regression
cases; a read-only challenger examined frozen implementations. The primary owned
the entry, reference, metadata, scaffold, actual demo and final adjudication. No
installation, real-site edit, source application or external publication occurred.

The optional manifest fields embed actual frozen HTML/CSS and component selectors;
their absence preserves legacy normalized identities. PNGs remain capture evidence
and an explicit fallback. Native frames retain both original viewport dimensions,
including on long pages. Component focus navigates to source elements; the direct
integrated action displays the actual exact selected document in whole-screen
mode. Missing combinations never borrow a member's DOM. Element references carry
side, view, preview, selector, short text and known component into proposal or
overall feedback. Selection and receipt authority are unchanged.

The bridge runs without the source application and checks current DOM, CSSOM and
form state before application export. DevTools changes are exploratory, remain
dirty across view changes, and require reset or a newly rendered proposal. Reset
preserves decisions and notes. Highlighting lives outside the source document so
inspection itself does not change source structural selectors. Native context-menu
inspection remains available; the snapshot does not execute product controls.

### Preservation failures found and corrected

An initial 19-method DOM suite and the 31 existing resource methods passed. That
packet did not cover all relevant preservation boundaries. Independent semantic
review and real Chrome probes then identified these defects:

| Observed boundary | Actual witness | Final disposition |
|---|---|---|
| Responsive image density | At device scale 2, a selected 40-pixel image had a 20-pixel intrinsic/rendered size in the source but became 40 pixels after serialization. | Refuse when decoded embedded intrinsic dimensions differ from the current source image; do not invent sizing CSS. Ordinary supported images still serialize. |
| Top-layer state and document mode | An open popover became invisible. A modal's measured width/height happened to match, but the probe did not establish top-layer/backdrop parity. BackCompat became CSS1Compat; the inspected 130-pixel box did not change size. | Reject active popover/modal/fullscreen and unsupported document modes explicitly. Nonmodal open dialogs and HTML5 standards-mode documents remain supported. Do not claim a measured modal or quirks geometry change that the probe did not show. |
| Leading line feeds | Native textarea/pre/listing content lost its first LF. Fixing snapshot serialization alone still failed in the viewer's second parse. | Preserve the parser-consumed LF at both serialization boundaries; compare actual frame content. |
| Structural selectors | Injected script/overlay nodes changed body/html child lists, made `article:last-child` miss, and changed final-child colors, background and a 7-pixel border. | Remove the bridge script on startup and draw highlights in the parent host; selector cardinality and computed styles now match the source. |
| Form property edits | Adding another selected option or setting checkbox `indeterminate` changed native state without changing the first value/index or markup; freshness still reported ready. | Include every option's selected state and checkbox indeterminate state in periodic and immediate export checks. |
| Visibility inheritance | A visible child overriding an ancestor's `visibility:hidden` rendered but was rejected as missing. | Check the target's computed visibility while retaining ancestor display/opacity checks. |

Earlier resource development also caught native link-style loss when `href` was
removed; inert fragment destinations preserve link appearance while the viewer
blocks activation. Phone/re-entry readiness initially measured zero geometry;
waiting for painted layout after assets/fonts load corrected that observed race.
Programmatic fonts without stylesheet font-face representation fail when detected.
Closed shadow roots on ordinary elements remain unobservable to standard page
JavaScript; successful serialization does not prove absence of hidden dependencies.

The evaluator repaired invalid fixture setup and timing assumptions without
relaxing the contract: a missing PNG case first retained an invalid non-null crop;
capture visibility and picker feedback needed their actual decode/message events.
The existing fingerprint assertion now independently includes the bundled bridge
bytes, matching the actual template. A feedback download timed out in intermediate
and final headless runs. The mode-specific diagnosis and retained failure are
reported below; an earlier passing packet is not proof that it disappeared.

Playwright frame locator coordinates did not account for CSS scaling in this
Chrome configuration; physical parent coordinates or 100% scale exercised picking.
Automatic screenshot caret-hiding injects frame CSS and correctly marks the DOM
dirty, so clean review screenshots use `caret="initial", animations="allow"`.
Neither observation justifies weakening actual DOM/style freshness checks.

Repository validation initially misread two JavaScript replacement strings as
named skill references. Equivalent capture-group callbacks removed that static
false positive. A first fresh producer had only read inputs and captured the
baseline when it was canceled for this correction; it produced no design or review
HTML and is not counted as a completed execution. A different no-history producer
received the final validated snapshot and clean inputs for the execution below.

### Final resource and real-demo checks

An initial follow-up packet passed 24 DOM methods and all 31 existing methods
before the equivalent font callback change. On package `c0170336…`, an independent
headless packet passed 23 of 24 DOM methods and all 31 existing methods; the
missing-combination feedback-download case failed. Source hashes stayed fixed.

Five instrumented attempts reproduced that failure before the download handler:
valid JSON and an open dialog, no parent button event, no Blob/anchor call, and no
success status. Root hit testing named the download button, but trusted pointer
events arrived in a background iframe. Scratch-only pointer-event, inertness,
visibility and zoom changes did not fix it and were not adopted. Default headless
Chrome also failed; the same unmodified artifact downloaded successfully in a
visible Chrome window and retained native inspection after close. This establishes
a mode-dependent pointer-delivery discrepancy in this environment, not a proven
browser-engine cause or a source-code correction.

A first full visible-Chrome packet passed that download case but exposed another
initial-layout failure: an ordinary visible intro stayed marked as having no area.
Two animation frames alone had not established final layout. The final bridge
rechecks actual component availability and refocuses when its availability changes,
while preserving permanent-invalid/hidden selector errors and dirty/reset rules.
A real parent-hidden-to-visible regression checks this recovery without mocking
element rectangles or weakening the missing-evidence gate.

The final frozen packet passed **25 DOM-suite methods** (six builder and nineteen
browser methods, using visible Chrome; 35.260 seconds) and **31 existing methods**
(browser cases using headless Chrome; 33.351 seconds). The same missing-
combination and CSSOM cases passed in that visible-browser packet. All four runtime
and two test-file hashes stayed unchanged. The additional availability test uses
real zero-area and restored element geometry, preserving the same frame handles,
source HTML, viewport, notes and decisions without Reset. Its first attempt read
the hide transition too early; awaiting actual native hidden state repaired the
test observation, with the exact zero-area and recovery assertions retained.

The optional `--headed` test mode runs the same assertions. No receipt, missing
combination or pointer assertion was relaxed to obtain a pass. Browser work used
Python 3.11.15, Playwright 1.64.1 and Chrome 156.0.8078.88. The headless pointer
discrepancy is retained as an environment limit; the later availability correction
is not claimed to fix it. Revisit that mode if a consumer requires headless pointer
automation or the browser/runtime changes. No product workaround was adopted.

The final author-built example renders six actual source variants at two sizes.
All 12 serialized documents reproduced their original PNG bytes exactly, including
the measured component geometry and text, in the same headless capture environment.
Cross-mode, font or operating-system raster equality was not asserted. The example
was rebuilt with the final bridge. The primary used Chrome DevTools'
DOM/Runtime protocol to resolve the real `H3` for the first note, checked the
1440×1000 and 390×844 native frame viewports, and inspected simultaneous panes at
both review-window sizes. This is actual DOM evidence, not an image wrapper.

The primary selected N01 plus N02-A and observed C-A's short introduction and
quiet-card list together. Picking its heading produced
`side=after; view=desktop; preview=C-A; component=note` and `#n1 > h3` in overall
feedback. Export retained that reference and exact selection. The helper validated
the test-only receipt against five baseline source files; this was read-only and
not human submission. A native style edit blocked export; reset restored it while
preserving feedback. No page errors or external requests occurred in that flow.
The actual revision 3 HTML and a matching test receipt still validated with its
original fingerprint. The current helper's receipt check also ran under Python 3.9.6.

### Fresh DOM-workflow execution

A different fresh no-history producer received package fingerprint
`c017033674de1823af8a5d38d6d4922c4a8978fcc28ef2aea4e3d49f2998d012`, twelve clean
runtime/rule files and the [ordinary DOM request](regression/observed/requests.md#inspectable-dom-review).
It did not receive the author demo, tests, prior answers or evaluator criteria.
Isolation was instructional rather than operating-system enforced. It reported
reading the entry, pattern and HTML references, proposal scaffold, project README
and DESIGN, the ten runtime files and necessary bundled code. The supplied package
remained byte-identical. No model override was requested; the actual worker
model/version was not independently exposed. This snapshot precedes the final
frame-availability correction described above; its instructions and other eight
package files are unchanged. Final resource checks separately cover that correction.

It produced N01 (a shorter left-aligned introduction preserving every word), N02
(a title-aligned row list preserving decorative wording at reduced emphasis), and
their actual N01-N02 combination. The result distinguishes measured header/list
positions from hypothesized scanning benefits and the loss of card warmth; it
does not claim that desktop rows shorten the whole list. Only each preview's
`notebook.css` changed. All twelve original files, shared tokens, HTML/JS, sibling
pages and project rules remained byte-identical.

The producer checked four source variants at two sizes for eight-note content,
three review deadlines, search/filter intersections, sorting, empty/reset states,
keyboard disclosures/focus and independent reading state. Twelve captures/DOM
snapshots cover desktop, phone and a filtered/open-detail state with reading 1/3.
Measured body-element geometry and appearance properties matched. Eight PNGs
matched exactly; four had raster differences of at most 8/255 per channel. The
producer replaced its failed byte-equality assumption with explicit pixel and
DOM comparisons and disclosed the differences rather than calling all twelve
pixel-identical. Their cause and human perceptibility were not established.

The producer also exercised component focus, actual element references, exact
integrated selection, dirty/reset behavior, phone panes, capture fallback,
feedback export and draft choice reversal. Its checks used locator waits where
CSP blocked string-based waits, physical coordinates for scaled frame clicks,
and caret-preserving screenshots. No candidate skill edits or primary design
coaching occurred during this completed execution. Test-only preferences were
cleared; no application receipt was submitted.

The primary verified the original and preview hashes, inspected the actual paired
HTML, resolved native H3 elements, and observed combined introduction height
298.328125→170.171875 pixels and record width 441→898 pixels at the declared desktop
viewport. The phone frames retained 390×844 with simultaneous panes. The filtered
state preserved two results, open n3 details, search text and the independent
checked reading item. The maintained notebook checker independently passed at
both sizes on the combined live preview. These observations support preservation
and review mechanics, not human preference or task speed.

The trial artifact had file SHA-256
`6166d0cf6f8145c44d62446b64133ef9b1e75e7ab224fcb3ab3d3cd8e09e7817` and review
fingerprint `e5375acff9737f5ed1f6fd47bf985bbae863364281b0d924d8d749cd90bc850d`.
Its temporary output was evaluated separately from the reproducible public demo.
This is one fresh forward execution under the new request, not a matched efficacy
rerun, repeated-run stability result or another application-continuation trial.

### DOM package and artifact identities

The revision 4 DOM package aggregate was `ec486f33a4aa0d2e994ccc56bbdb873a01e879d2519950aa78f445fd3337ad01`, using the same sorted
path-to-SHA-256 calculation as earlier revisions. Its nine files are:

| File | Revision 4 SHA-256 |
|---|---|
| `SKILL.md` | `b282311c98aceb7eeb6ba72bfd9dceac528fe4e3f9246ce6b8158863cc077672` |
| `agents/openai.yaml` | `1398c569fd9ff8e962a8322af3cc4d097450cddbf3f4fe3ca7978e23df3a7780` |
| `assets/dom-preview.js` | `eea4a0eab0e98516d546246e178aefc899d84dee2b24d274e2326e121da4df69` |
| `assets/review.html` | `a4d66fe107de643187fc86120e2c8f1eb53eb5eeb43a4c8a4f13839e4517057e` |
| `assets/snapshot.js` | `b1c556852b759c99def1d00b60f41023412ec2cebd7e784a32610f1f55532377` |
| `references/html-review.md` | `5206e838fb087ef541d321930939d48e729b1186350d8a0f6c30f5dff2104896` |
| `references/patterns.md` | `6fcef9d08707224f1f3ae5b53d10831a1b3029a33e73e5586ad5376ed70448c3` |
| `scripts/review.py` | `8088fb2eb5a37a31dceaa9367cfaf41542d09b6457c0cfb8d4ee8b823c650fd2` |
| `templates/proposal.md` | `820dd93e96494ff2be9d5169c184839741b77edf5655c621a5ee519269711543` |

The revision 4 synthetic review was self-contained. That output was replaced in
revision 5, and the [current artifact](regression/observed/review.html) at the same
path was regenerated for revision 6. The revision 4 file SHA-256 was
`be5cbccc0ee9dbaab9fc6d6f0f868d34b42239d40a76a8b993b5053c106f6d1e`, with embedded
review fingerprint `2cabf4c54644e07fe6e6877c1ad3a880ab7c4678a9ea5fc215d0fc090e0b3396`.
The [component DOM screenshot](regression/observed/compare-dom.png) and
[phone integrated screenshot](regression/observed/compare-dom-phone.png) record
the final revision 4 viewer, before the quieter controls and partial-request
workflow. The separate `viewer-review.html` and component screenshot
identified in revision 3 remain historical pre-DOM evidence, not updated DOM views.

Repository package and platform metadata validation, local Markdown/resource
links, Python syntax/compatibility, whitespace and portable-path checks passed.
The record metadata passes its JSON schema. All fifteen frozen fixture inputs
retain their recorded bytes and SHA-256 values. The three adjacent skill names
remain explicitly optional and availability-qualified; the discovery description
did not change, so no new metadata-routing claim is made. No installed copy or
cached runtime registration was updated or evaluated.


### Quiet viewer, partial choices and conversational handoff

The user's observed review was readable but repeated choice state across its
upper controls, sidebar and footer, and still exposed an unnecessary capture
mode. The requested correction was a quieter review plus a practical way to take
only part of a proposal, exclude it, or request another draft. The baseline was
revision 4 aggregate `ec486f33a4aa0d2e994ccc56bbdb873a01e879d2519950aa78f445fd3337ad01`
and its actual synthetic HTML, not a reconstructed assessment of another tool.

The revised viewer has one selected-combination entry and one agent-handoff
entry. Normal explanatory text moved into change details and optional help;
actual blockers still appear when relevant. The paired surface stays inspectable
DOM, with no source-mode toggle or duplicate selection summary. The current
example needs no PNG evidence. An omitted DOM descriptor can use its actual PNG
automatically per side/view for legacy compatibility; an explicit null descriptor
remains missing evidence. Mixed components use the same scale. No product files
or app behavior are activated by the viewer.

Whole acceptance, partial/revise and exclusion have compact controls with
accessible names. Partial choice clears whole acceptance, preserves the note,
and never enters the accepted combination. The main handoff is a readable request
containing choices, element references, notes and review identity. The user
copies it into the conversation; default intent is another preview. Applying
accepted changes and retaining the original are distinct explicit intents, and
JSON remains optional. Copying or local autosave is not submission. The skill
requires reconciling narrower free-text intent and building a new partial-scope
preview rather than interpreting it as whole adoption or extracting CSS blindly.

Independent static challenge on the intermediate frozen candidate
`9c027aaf0b6329c91424e27fdc5c23d600f268cca6ee2046a0e01b1f14242bc6` found three
concrete omissions: valid mixed DOM/PNG evidence was unreachable without the old
toggle, partial action on the same pending proposal from integration left its
note hidden, and locked outcome reports hid proposal explanations/notes. The
primary accepted and corrected each; browser cases exercise both mixed
orientations, a PNG-only view, explicit-null rejection, the unchanged accepted-set
partial transition, and locked details without changing the outcome.

A former hidden-parent test expected an initialized native iframe viewport even
while its parent was forced to `display:none`. A controlled baseline/current
probe observed zero-area source elements in both; current hidden frames could
report either the declared size or 0×0, then both returned to the exact declared
viewport and ready state when revealed. The revised assertion checks exact
CSS-declared dimensions, only those two hidden native outcomes, and all original
strict visible geometry, source-content, choice and dirty-state recovery checks.
It does not loosen visible viewport preservation or suppress a missing selector.

The final frozen verification packet ran with Python 3.11.15, Playwright 1.64.1
and Chrome 156.0.8078.88. The legacy suite passed 31 methods in 43.852s (including
19 visible-browser methods); the new workflow suite passed 12 stdlib methods in
6.071s. The DOM suite ran 34 methods in 49.392s: **33 passed and one failed**.
Its failure was `test_picker_reference_copy_and_proposal_or_overall_feedback`:
a native heading click after entering the integrated view left the element
reference empty instead of receiving the expected before/baseline reference.
Thus the final packet is **76/77 passed, Result FAIL**, not an all-pass claim.
All seven frozen runtime/test file hashes matched before and after. Native Chrome
needed sandbox escalation for Crashpad startup; this was a launch permission
limit, not an automatic-approval rejection or application failure.

A preceding helper run passed all 77 methods before the final mobile CSS edit.
Three bounded diagnostic attempts then ran the unchanged failed method with click,
control-message and geometry instrumentation; all passed. Each trusted click
reached `h3#page-heading` at native (472,49), inside the visible pane despite the
wide heading block. Picker-enable arrived 63.7–69.4ms earlier and the parent
received the expected picked message. No failure was reproduced, so these are
counterevidence, not a fix. Instrumentation may change timing. The primary did
not change runtime or weaken the picker assertion to obtain a pass.

**Revision 5 verification item — integrated element reference.** The exact frozen
test above owned the reproducer. At that checkpoint its application-versus-
automation cause was unresolved; no runtime correction or repeated-run stability
was claimed. Revisit triggers were a visible blank reference after a real pick,
another uninstrumented failure, or a browser/automation-runtime change. The next
bounded check was a failing native-event trace without interactive pre-click frame
reads, distinguishing lost delivery, stale frame identity and picker state before
selecting a correction. Closure required a confirmed defect correction or an
established tool/assertion cause while retaining native selection evidence. No
further exploratory run was assigned in that bounded UI refinement, and its work
metadata remained open/waiting. The closeout below records the later controlled
defect, correction and remaining attribution limit.


The primary rebuilt the final DOM-only demonstration from real pages at desktop
and phone sizes. All twelve snapshots matched source component geometry, text and
representative computed properties (including typography, backgrounds, borders,
shadows and layout). The first earlier build also passed twelve strict PNG-byte
comparisons. A later strict rebuild differed on the combined card phone raster;
its visual cause and magnitude were not established. That failed raster check is
not relabeled a pass. The generator now performs DOM/style comparison by default
without requiring screenshots; `--verify-raster` retains the strict optional
check. No claim of deterministic raster identity across runs is made. The final
HTML embeds DOM only; older PNG artifacts remain historical evidence.

Primary actual-browser probes also checked paired pane alignment, all toolbar
controls within the viewport and no document overflow at review sizes 1440×1000
and 390×844, with both desktop and phone source views. They confirmed the readable
default handoff and absence of the removed controls. The phone toolbar was put
on an explicit grid and its two pane headings aligned after a real visual check
found a clipped view selector and unequal starting positions.

### Fresh partial-adoption continuation

A no-history producer received the six clean notebook source/rule files, the prior
review as necessary task evidence, the frozen `9c027aaf…42bc6` candidate and the
[ordinary partial-adoption request](regression/observed/requests.md#partial-adoption-continuation).
It received no expected patch, evaluator rubric, other worker outcomes or primary
fix rationale. Isolation was instructional; no independent model-version or host
skill-discovery claim is made. This run preceded the final mixed-evidence,
locked-note and mobile-layout resource repairs; the final resource checks cover
those later changes, not an exact-final-package forward execution.

The producer emitted round 5 with the unchanged N01 preference accepted,
new `N02-A-R5` pending, an actual combined preview and N02-B excluded from the
next candidates with its rejection retained in the review context. Its shadow-only
preview adds only `.note-card { box-shadow: none; }`; all six supplied source
files remained byte-identical. The primary independently checked those hashes,
the actual CSS-only difference, native card text, original gradient/background
and 18px corners, and absent shadow. It opened the resulting HTML and confirmed
N01 accepted, the revised card pending and the excluded row option absent.

The producer reported desktop/phone source/snapshot geometry, styles and content;
search, filters, ordering, reset, keyboard disclosure and independent reading
checks; and viewer choices/feedback/exact-combination behavior. Its output uses a
customized viewer template to carry the unchanged draft choice and expose the
unaccepted combined draft separately. That is an observed authoring adaptation,
not a claim that the stock helper automatically migrates preferences between
artifact fingerprints. The helper accepted its actual HTML identity. Temporary
localhost rendering resolved file-origin CSS access, and clean screenshots used
`caret="initial"` to avoid injecting test styles. All browsers/servers closed.
No project application was submitted, no other-page navigation was available in
the six-file packet, and human preference/task speed were not measured.

The trial HTML file SHA-256 was
`d3bc027effa3a419e14a0e6d5811ab68f1ad0a1fcf8aa7421bd01ee0736ba450`, with embedded
fingerprint `7b9d2663fc61615971436bf65c60d64b8128a0d7355d4690f78309aba3ac4cac`.
Its task-owned output and previews were removed after primary verification; the
portable current example below has a separate durable owner.

### Revision 5 package and artifact identities

Revision 5 package aggregate: `fb36600792f47a017c7fcccbf8b859611cedfea390e1ebea0c3215542e0f15c4`.
The sorted compact path-to-SHA-256 calculation is unchanged.

| File | Revision 5 SHA-256 |
|---|---|
| `SKILL.md` | `1c851c9c3eeb804da6b8e0a4606657672314e924d9435fa84e1fe0d78dc06cad` |
| `agents/openai.yaml` | `61179c59b420691e9e9f8173894166c7eb7b9931373ae71c0e000fd19adbf2fe` |
| `assets/dom-preview.js` | `daf66f1daba343a067f467002e6678ea64ad57ceeea24bdfbe8e56ebe43880c8` |
| `assets/review.html` | `56b0e9bb37909fbb01e3b48302fc52c322ce0a7fd68cf37b19be76e762ec6c03` |
| `assets/snapshot.js` | `b1c556852b759c99def1d00b60f41023412ec2cebd7e784a32610f1f55532377` |
| `references/html-review.md` | `179933be89167456acada0b05512bae68b69d0ae16ec2afe3288fb9f41e7b511` |
| `references/patterns.md` | `6fcef9d08707224f1f3ae5b53d10831a1b3029a33e73e5586ad5376ed70448c3` |
| `scripts/review.py` | `85db60ae265e97f185294d1286031b0c47e6207c9b6eba7c38c59e7d4c2424ea` |
| `templates/proposal.md` | `fc4b94add510a490aa265b54ce0046a25889ca08d6c1aa321a37d8f335aebd38` |

The DOM-only example at this checkpoint had file SHA-256
`5d4b509ce4a5eebb1b957838c82fb1ddb010e8db0de64906de99eed0409c6894` and embedded fingerprint
`3e70560710b8c2c804d905007b0b239864b5611df1365563f80e38eb7b2e60b4`.
It is review round 4; the validation record revision and review round have
separate meanings. No screenshot evidence is embedded. Package, frontmatter,
metadata schema, local links/resources and whitespace checks passed. All fifteen
frozen fixture inputs remained byte-identical. No installation, publication or
actual personal-site edit occurred at this checkpoint. The example was subsequently
regenerated during the closeout below.

### Closeout verification and initialization corrections

The user requested another independent exploration and validation pass, followed
by documentation review, repository closeout and a local skill symlink. The
canonical owner remained `skills/design-deslop`; no personal product was edited.
An independent static reviewer inspected the frozen revision 5 contract, metadata,
scaffold, patterns, viewer, bridge, serializer, helper and relevant regression
assertions. Reading this record exposed earlier finding summaries, so the pass
was not fully blind. It was semantic review, not a fresh producer execution.

The reviewer found that CSS/form baselines were captured only after image, font
and layout waits. CSSOM or input-value edits during those waits produce no DOM
mutation record and could become trusted baseline state. The correction captures
both states synchronously before the first await, after inert source markup and
embedded styles have parsed. Asset/layout readiness remains separate.

For the earlier picker item, five passive-trace attempts of the unchanged method
and one 28-method DOM-browser-order run passed. These did not reproduce or explain
the historical failure. An initial event-listener gate recorded a held control
without reliably preventing delivery; that invalid gate was not admitted as
causal evidence. A later test-local bridge resource controlled delivery inside
the handler before the embedded bridge started. With an already-active picker,
a new frame could report ready while its initial picker state was still false.
The correction passes the controller's current picker state into each new frame
at construction; subsequent control messages remain unchanged.

Two deterministic methods failed against the unchanged runtime with three failed
witnesses: a native baseline-heading click produced no reference while picker
delivery was held; loading-time CSSOM and form-value edits each became ready with
`dirty=false`. The corrected focused packet passed six methods in 8.671s, including
the original native picker method and existing structural, CSSOM and form checks.
A test-only strengthening then released pristine replacement frames and awaited
readiness before checking that the dirty flag still blocked application. This
separates dirty-state blocking from loading-state blocking. The full DOM suite
below exercised those strengthened assertions, reset to the original values and
body, and preservation of the accepted choice and notes.

These controlled resource tests use instrumented bridge copies. They close the
demonstrated initialization defects; they do not establish why the earlier
uninstrumented picker attempt failed, repeated-run stability, or all timings of
a picker toggle during loading. Independent rereading found no additional
material regression in the narrow correction and final assertions. The primary
accepted that scope and retains a real blank reference or another native failure
as a trigger to reopen investigation.

A separate final legacy-suite run initially failed one of 31 methods: crop
geometry was read as zero width. Its helper awaited image decoding and one
animation frame, while the viewer's asynchronous load handler could still be
waiting to unhide the image. A controlled handler gate showed both images fully
decoded at intrinsic width 960 but hidden with zero rendered width when the old
helper returned. Releasing the same handler and waiting for visibility passed
the unchanged scale, dimension and position assertions. The test now awaits the
displayed pair before reading geometry; no production viewer code, numeric
tolerance, pixel check or crop assertion was relaxed.

The final resource results use Python 3.11.15, Playwright 1.64.1 and Chrome
156.0.8078.88. The separately probed system Python 3.9.6 was not the test interpreter.

| Final suite | Methods | Result | Duration |
|---|---:|---|---:|
| Artifact/receipt, including headed legacy browser checks | 31 | PASS | 38.715s |
| DOM builder and headed native-browser checks | 36 | PASS | 44.269s |
| Partial-choice/handoff workflow | 12 | PASS | 5.766s |

Together these are **79/79 passed across three suite runs**, not one atomic test
run. Only the legacy test's display-readiness helper changed between final suite
executions; the DOM and workflow suites do not call it. All nine runtime files
and all three test files were unchanged across the last artifact run. Their final
hashes are recorded below. Native Chrome again required launch sandbox escalation;
no automatic approval rejection occurred.

The regenerated [current example](regression/observed/review.html) passed twelve
source-to-snapshot comparisons of component geometry, text and representative
styles at 1440×1000 and 390×844. It remains DOM-only, with the user-approved quiet
controls and no new screenshot deliverable. Optional strict raster-byte checking
was not run in this closeout; its earlier mismatch remains a separate limit.

The serializer review identified two parity limits within the existing required
caller check: rewriting a link destination can alter `href`-dependent CSS, and
removing a script/template can alter structural selectors. Packaging does not
compare these styles with the original. The HTML contract now names these cases
and preserves the duty to compare source/replay styles and geometry, then use a
verified equivalent preview or labeled capture fallback if they differ. No
universal selector-preservation or automatic parity-detection claim is made.

Two independently tasked documentation reviewers then used `docs-structuring`
and `docs-shaping`. Each read all sixteen in-scope Markdown documents and UI
metadata; executable and binary resources were inventoried rather than retested.
The ownership review retained the existing runtime/evidence/catalog roles with
no necessary restructuring. The composition review moved the complete discovery
qualification paragraph beside its earlier criteria and clarified revision 4
artifact labels. All classification conditions, historical file/fingerprint
identities and pre-DOM qualifications were preserved. No new document owner or
separate session log was created.

### Current package and artifact identities

Revision 6 package aggregate: `1fc8d392907f13ca65620dcca0e0400b6c171513ba7952ca77bf5397d1c9fea4`.
The sorted compact path-to-SHA-256 calculation is unchanged.

| File | Revision 6 SHA-256 |
|---|---|
| `SKILL.md` | `1c851c9c3eeb804da6b8e0a4606657672314e924d9435fa84e1fe0d78dc06cad` |
| `agents/openai.yaml` | `61179c59b420691e9e9f8173894166c7eb7b9931373ae71c0e000fd19adbf2fe` |
| `assets/dom-preview.js` | `935f5d816d5684911364882c809fde1b3519ec2339a59cd52630f89a50a2d50b` |
| `assets/review.html` | `56b0e9bb37909fbb01e3b48302fc52c322ce0a7fd68cf37b19be76e762ec6c03` |
| `assets/snapshot.js` | `b1c556852b759c99def1d00b60f41023412ec2cebd7e784a32610f1f55532377` |
| `references/html-review.md` | `94d5a39c3165b950baba8a27f0eea17f450ffce87e90cf6099eba9d7810e27e3` |
| `references/patterns.md` | `6fcef9d08707224f1f3ae5b53d10831a1b3029a33e73e5586ad5376ed70448c3` |
| `scripts/review.py` | `85db60ae265e97f185294d1286031b0c47e6207c9b6eba7c38c59e7d4c2424ea` |
| `templates/proposal.md` | `fc4b94add510a490aa265b54ce0046a25889ca08d6c1aa321a37d8f335aebd38` |

| Final regression file | SHA-256 |
|---|---|
| `test_review_artifact.py` | `5b6e4cfdb9a4b3bac556984771e2d14d0f6f498e1dc5f505f47f4e3767719a77` |
| `test_dom_review.py` | `5af805da2a447704c99f2f52d547624a8c55cb8dc9027b826973e2c6a8adf660` |
| `test_review_workflow.py` | `a1f5c2ed63d5f43bbb3b62bd56ae1a285da5c64ca7b7e446a02c2aa4e433ebff` |

The current HTML file is 360,522 bytes, SHA-256
`ddf2ad211341370d8b8a91ca3b4102549da14d06041e8c5c858c0295c3476067`, with embedded
fingerprint `13e70f36e2150dd70c9923512ef19a340a5ca7fcdceeb207413308cab8e4a83a`.
Its review identity remains `fieldbook-dom-review-demo`, round 4; the changed
artifact fingerprint distinguishes the rebuilt resource. The validation revision
is a separate identity. No screenshot evidence is embedded.

Final package/frontmatter and metadata checks, record-schema validation, local
links and anchors, Python 3.9 syntax compatibility, JavaScript syntax and whitespace
checks passed. The three adjacent-skill references remain optional and
availability-qualified. All fifteen frozen input files retain their recorded
sizes and hashes; no personal paths or private product content enter the package
or evidence.

## Work And Acceptance

The requested local viewer simplification, DOM-only evidence, partial choices
and conversational handoff are implemented and demonstrated by real browser and
fresh continuation outputs. Static acceptance and the final resource Result are
**PASS**, with **79/79 methods passed** across the three runs above. The controlled
initialization defects are corrected and the required verification item is closed
on that evidence. The revision 5 **76/77 FAIL** remains historical; its exact
uninstrumented picker-failure cause is still unknown. The revision 4 56-method
acceptance and prior headless modal-pointer discrepancy also remain historical,
with no claim that the latter environment limit is fixed. Evidence Coverage is
**partial**. The primary owns semantic acceptance; worker outputs are evidence,
not approvals.

Evidence coverage remains **partial**. The record's comparable-rerun maturity
comes from the historical implementation-authorization correction; the HTML
and component extensions have resource checks and fresh forward executions. The
DOM extension has a fresh workflow execution on the documented preceding bridge
and final resource checks after the narrow availability repair. Revision 4's 56-method
packet combines visible DOM and headless legacy checks; the earlier headless DOM
failure remains reported above. Changed user
requirements prevent treating the new preview-first workflow as that old task's
comparable efficacy rerun. Neither successful executions nor assertion counts
establish repeated-run stability. No skill-versus-no-skill ablation, measured
human preference/task-speed study, physical mobile or other-browser matrix,
live concurrent-editor race, unavailable-browser producer execution, or actual
host skill auto-selection was performed. Still-image reviews do not demonstrate
live motion or all interactive behavior. Frozen DOM preserves inspectable HTML/CSS;
its product controls do not run. Snapshot portability is deliberately bounded by
the documented asset/state limits, and matching captures do not establish identical
raster output across operating systems, fonts or browser modes.

No further experiment is assigned in this refinement. Reopen the relevant case
on a visible blank reference, a new native-click failure, a browser/automation
change, or changed output, selection, freshness or metadata semantics. Publication
and a user-scoped symlink are authorized closeout actions; filesystem installation
and actual fresh-client discovery remain distinct. Host discovery was not tested.

## Outcome And Reuse

The current workflow produces selectable paired HTML with whole-screen context
and native DOM/component inspection before adopting unseen design choices, with
qualified element feedback, partial/revision requests, a readable conversation
handoff and an exact integrated whole-screen view. It then
applies only submitted reviewed scope and returns actual applied evidence. It
preserves expressive alternatives, intentional identity, meaning, controls and
the option to stop. The prior direct-application lesson
remains historical under its earlier authority contract; the current user has
chosen review before adoption. A global rejection of common fonts, gradients,
cards or creativity is not supported by either set of evidence.

Portable inputs, evaluator criteria, resource tests, observed patches and the
self-contained example stay with this record. They are bounded examples, not
visual answers for future producers. Temporary snapshots, browser outputs and
evaluation-only review workspaces are removed after integration; the example
has a durable owner and works without its capture server. Original private site
content and paths are excluded, and the actual site was not edited. Session
messages are observations, not a claim that all raw execution traces are archived.

The primary reviewed public fitness: retained data is fictional and the record
preserves failures, corrections and limits. Human reference-case acceptance was
not requested. The user authorized repository publication and user-scoped symlink
installation as closeout actions. Those steps do not establish actual consumer
activation or runtime skill selection; neither was evaluated here.

## History

- 2026-11-06, revision 1: created the package and independent synthetic cases;
  corrected metadata ambiguity, repaired the fixture's blur/click bug before
  trials, observed and corrected an implementation-authorization failure, and
  recorded fresh executions, comparable rerun, primary checks and remaining
  coverage limits. Kept one record at the skill owner; no prior matching record
  or duplicate observation was added to the catalog.
- 2026-11-06, revision 2: implemented the user-requested paired HTML review and
  explicit selection workflow, reusable viewer/helper and resource tests; added
  overall feedback after independent challenge, clarified stale-snapshot
  reconciliation, and recorded fresh proposal/application and retained-screen
  executions without relabeling the historical authorization evidence.
- 2026-11-06, revision 3: added measured component inspection beside whole-screen
  review, retained proposal-level adoption and legacy artifact identity, refined
  the viewer through subagent baseline inspection, and recorded the 31-case
  resource suite, primary real-demo probes, independent semantic challenge and
  one fresh component-review execution. Preserved earlier results and limits;
  human taste was not inferred from passing mechanics.
- 2026-11-06, revision 4: added inspectable frozen DOM, element references and
  explicit integrated comparison; repaired measured snapshot, structural-selector,
  native-state and availability failures through delegated checks. Recorded the
  final 25 visible-DOM plus 31 headless-legacy tests, twelve real-demo snapshot
  comparisons, fresh workflow execution and its precise revision/raster limits.
  Retained the headless modal-pointer discrepancy and historical artifacts without
  claiming a runtime fix, human preference or cross-browser stability.

- 2026-11-06, revision 5: simplified viewer controls, removed the capture toggle
  and PNG requirement for complete DOM reviews, added partial/revise choices and
  readable agent requests. Corrected three independently found UI/evidence gaps
  and mobile toolbar layout. Recorded the fresh shadow-only continuation, final
  76/77 packet and three instrumented picker passes without relabeling the open
  failure or optional raster mismatch as a fix. Kept the verification item open.
- 2026-11-06, revision 6: independently re-examined the frozen package; corrected
  loading-time freshness baselines and initial picker state with controlled native
  regressions. Repaired a legacy test's display-readiness wait without weakening
  geometry checks; recorded 79 passing methods, twelve regenerated DOM comparisons,
  and the serializer's sanitization limits. Retained historical picker attribution,
  headless and optional raster limits without claiming universal stability or a
  new exact-final-package producer trial. Completed independent structure and
  shaping reviews, retaining the owner structure and applying only the bounded
  criteria-location and historical-label clarifications.
