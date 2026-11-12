---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-ui-state-transition-contracts",
  "revision": 8,
  "audience": "public",
  "subjects": [
    {
      "kind": "harness",
      "key": "agents/policies/review/interaction-evaluation.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "9798d234258ffe44e20308ca9c2f3a2e51c755e998c5e2624f2da187616071c1"
    },
    {
      "kind": "harness",
      "key": "agents/policies/review/design-evaluation.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "44c460dc47bd3f088739f8e4883a3df39ea95e665fc110898b5505bf15e93c49"
    },
    {
      "kind": "skill",
      "key": "skills/screen-alignment/references/method.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "fabc999818783a702bc22783ca470604f47650a936b1cbb0eb6be3d0200b1048"
    },
    {
      "kind": "skill",
      "key": "skills/screen-alignment/references/checklist.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "fdc1ba03efa0e12dc1b7bfe66c07c473a8a4cc0474ea4dd8f4f726f032bf2edb"
    }
  ],
  "work": {
    "basis": "not-applicable",
    "state": "not-applicable",
    "readiness": "not-applicable"
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
    "maturity": "observed-stage-execution",
    "execution": "mixed",
    "coverage": "partial"
  },
  "adoption": {
    "public_fitness": "approved",
    "case_status": "draft",
    "rule_status": "implemented"
  },
  "relations": {
    "related": [
      "ir-ui-requested-control-rendering",
      "ir-ui-native-host-evidence",
      "ir-ui-initialization-recovery-evidence"
    ],
    "supersedes": []
  }
}
---

# Stateful controls and committed intent

## Context And Applicability

This record asks how review can distinguish transient presentation from committed
selection, order, and persisted intent during repeated input. The primary owner is
[Interaction Evaluation](../../../policies/review/interaction-evaluation.md).
[Design Evaluation](../../../policies/review/design-evaluation.md#nested-collection-hierarchy-and-ordering)
owns the related displayed-order semantics; [screen-alignment](../../../skills/screen-alignment/SKILL.md)
owns the standalone repeated-control verification procedure. These are connected
checks on state transitions, not a shared requirement for one control design or
storage schema.

Use the lesson for repeated controls, reorderable collections, or remembered
preferences when the affected product promises those behaviors. Keep explicit-save
forms, manual versus derived ordering, and transient canvas manipulation under
their separate contracts. This record does not prescribe autosave, animation,
numeric identifiers, source labels, or configuration formats.

Generalization retains the state transitions and comparison conditions while
omitting private records, labels, paths, and implementation-specific dimensions.
Metadata fingerprints identify the pre-change common-source files. Historical
loaded instructions, models, and full tool settings are unknown; current policy
differences do not establish the cause of earlier failures.

## Evidence And Evaluation

### Query ownership, preference recovery and results-first status (record revision 7)

A generalized private search/settings observation covered a capability-driven
search surface and an editable minimum-relevance preference. The selected engine
followed saved activation and model availability; preparation, query failure and
an empty result were not reasons to silently change retrieval semantics. A
capability change preserved the latest query and deferred navigation while the
settings dialog, a focused query field or input composition still owned work.
Both a page input and the shared header were exercised; after result-page cleanup,
the header became the sole visible query owner there.

The preference checks covered save/default restoration, stale revisions,
failed save/read, retained drafts and retry, and a committed save whose response
was lost but could be confirmed by readback. The numeric cutoff was not presented
as an accuracy probability. Synthetic retrieval confirmed its query-only storage
boundary without rebuilding the index; this did not assess a real embedding
model's semantic quality or establish a universal autosave contract.

The submitted-query screen initially repeated landing instructions, another form,
healthy readiness and preparation coverage before populated results. The approved
correction showed result counts and sources, or an honest empty/error state,
first. Queryless setup guidance remained available. Preparation, partial updates
and failures retained actionable notices. Query failure remained visible even
when aggregate index status reported ready.

Moving the same-query rerun outside the hidden readiness region kept it reachable
after preparation. A rendered check also caught a display rule overriding the
link's hidden attribute; explicit hidden styling corrected it. Native header
submission and evidence-return navigation were checked at wide and narrow widths.
Injected preparation/partial/failure/recovery transitions preserved the query
draft, focus and existing results. Browser scroll anchoring preserved the visible
result position; absolute scroll offsets could change as the notice entered the
document. These are distinct observations from a claim of an unchanged offset.

Product browser checks used synthetic sources, a deterministic encoder and
synthetic model-installation status; some status transitions were injected.
No installed-native rebuild, physical composition test, Atlas recapture for the
later source edits or guidance-effect comparison was part of those checks.
The addition extends reference evidence and the bounded existing review criteria;
it does not change the record's independent work, acceptance or adoption states.


### Earlier control and preference observations

The private receipts were reviewed on 2026-10-26 as recorded evidence. Their
reported UI checks were not independently rerun, and raw temporary captures were
not available. Different events below support different checks; none is counted
again as independent support merely because a related record cites its boundary.

| Recorded event | Observation and correction | Limit |
|---|---|---|
| Repeated color controls | Opening peer menus in sequence and activating the icon versus surrounding button exposed host-specific focus emphasis. A corrected sequence distinguished pointer focus from selected state and checked keyboard focus. | An isolated embedded-view probe with injected operating-system events did not establish physical input in the packaged app. |
| Collection reordering | A handle alone did not communicate movement. Later work added drag preview and destination feedback, commit/cancel handling, keyboard operation, and a reduced-motion branch. | Recorded browser/probe results cover their tested paths, not all physical host input. Feedback style remains a product choice. |
| Preference autosave | Changes saved individual preferences; pending writes, concurrent revisions, close/reopen, and ambiguous failure required serialization or reconciliation with storage. Failed readback left confirmation unavailable. | Explicit-save source editors retained their own draft and Save boundary. Reported application checks did not establish every recipient environment. |
| Displayed path ordering | A list displayed shortened paths but compared a mixture of cached labels and path values, changing pinned order. Sorting was corrected to follow the displayed ordering contract across mixed records. | This is not a requirement to alphabetize manually ordered or chronological lists. Stable identity remains distinct from a mutable label or sort key. |

These historical stages were reported as executed. The shared-source review is
static, and the public examples below were **not run** as new UI scenarios. No
candidate-policy or skill execution comparison was performed, so the effect of
these guidance changes on future task outcomes is **not assessed**.

Illustrative future controls, with expected outcomes:

- Open and dismiss peer controls, then navigate by keyboard: the saved choice
  stays distinct from transient focus, with visible keyboard focus retained.
- Under commit-on-drop, a changed valid drop saves order; cancellation, an
  unchanged drop, or an invalid destination does not write. A separately approved
  transient manipulation returns to its anchor instead.
- Rapid autosave edits and delayed responses preserve the latest accepted intent;
  unknown persistence is reconciled or remains explicitly unknown. An explicit-save
  form still waits for Save and honors Cancel.
- A promised name/path sort matches its displayed meaning across mixed old/new
  data and stable ties. Manual, chronological, and per-group order stay unchanged
  when a label or display format alone changes.

### Later Navigation And Input-Ownership Evidence

Additional private receipts reviewed on 2026-11-06 report executions with
synthetic data. They extend the state-ownership question; the generalized account
was not rerun publicly and does not disclose original captures or runtime state.

| Recorded condition | Observation and reported correction | Limit |
| --- | --- | --- |
| App history over host history | The app retained fewer entries than its embedded host. Unknown or evicted host markers could be appended again and expose out-of-contract traversal; explicit retained-entry boundaries corrected that case. Replacement also needed to replace app identity rather than grow it while native history length stayed unchanged. | Capacity is product-owned. Host history length alone did not establish app traversal availability. Reload, new-branch behavior and direct entry retain their separate contract. |
| Entry versus current-window preference | Restoring a cached document could restore an obsolete sidebar state. Reading the current window-owned preference on revisit preserved its approved lifetime separately from entry-owned scroll and selection. | This did not turn a window preference into a database or cross-device setting. The delayed-render restoration event is described in the [initialization record](initialization-and-recovery-evidence.md), not counted again here. |
| Shell shortcut versus local arrow handler | A focused local splitter consumed modified arrows before a bubbling shell command. Owning only recognized global combinations at the earlier event phase corrected the checked traversal without consuming ordinary local arrows. | Another shared consumer had static protection without its own positive runtime witness. Handler inspection was not that missing witness. |
| Modal and composition ownership | A custom modal used a different inert boundary from a native dialog, allowing shared shortcuts through an incomplete guard. Separately, a hint dismissal handler consumed composing Escape before the input. Guards for the actual modal/inert owner and composition state corrected the corresponding scripted witnesses. | Programmatic event-routing checks did not establish real operating-system IME behavior. Capture priority is not permission to bypass active modal or text input ownership. |
| Disabled action and retained help | The approved disabled state retained its short action name and shortcut help while forbidding activation. Removing only unavailable-state wording did not authorize removing all help. Wrapper hit targets required separate cursor, no-action and native drag checks. | Help visibility, keyboard focusability, accessible identity and execution availability are independent product decisions. The same host hit-path evidence is described in the [native record](native-host-evidence.md), without another independent execution. |
| Focus scroll into an offscreen item | Keyboard navigation scrolled a later menu item into view, but a global scroll dismissal removed its focus-owned hint. Preserving the current keyboard owner while reanchoring corrected the checked path; explicit dismissal and other release paths remained distinct. | A first-item hover pass did not cover a short viewport or later keyboard targets. Pointer, keyboard and supported touch access retain their approved contracts. |

The source additions clarify restoration, shared/local command ownership,
focus-owned scrolling and disabled help within Interaction Evaluation. Existing
anchoring and modal isolation duties already covered parts of these events;
this is not evidence that more rules would have prevented them. No controlled
guidance comparison was run; effect remains **not assessed**.

Source inspection for revision 3 used `policies/review/interaction-evaluation.md` at common-source
commit `19e14c8d48fc9ba3106219969f6ca70802479032`
(SHA-256 `ea936f4844073807d5a2152419608da0a783c8ab95ef5144c5f6f2f977e862c8`).
Historical subject fingerprints above remain unchanged. This identifies the
compared shared source, not the instructions loaded during product executions.

### Later Inline-Title Editing Evidence

Private receipts reviewed on 2026-11-08 report source/browser/package checks of an
inline, user-owned title override. This is additional generalized private
evidence; the scenarios were not rerun publicly. The historical source title and
user override had separate owners; clearing the override restored the source
label rather than deleting imported evidence.

| Checked transition | Observation and reported correction | Limit |
| --- | --- | --- |
| Pointer entry versus keyboard entry | Focusing and selecting the whole title prevented insertion at the clicked location. Capturing the rendered label's DOM caret before hiding it, then mapping its UTF-16 offset into the input, preserved a collapsed pointer caret; the supported range-based engine fallback was also exercised. Keyboard activation intentionally started at the end. | The reported click near the middle of the title and other text/padding points support their checked paths, not every font, truncation or engine. Whole-value selection remains valid when a different product explicitly requests it. |
| Recognizable editable field | Existing outline, surface and elevation roles exposed the field without changing row or heading height. Matching painted padding and interactive bounds prevented a click on the apparent field edge from following the surrounding row link. Independent title, destination and pin targets were checked at narrow and wide widths with long mixed-language/emoji labels. | Foreign reference styling was not copied as a design system. The containing-block event is retained in the [geometry record](../design-evaluation/requested-control-rendering.md), not an additional execution. |
| Save, clear and recover | Browser checks covered save/blur, clearing to source, cancellation, pending exclusion, persisted reload, failure with retained draft and retry, and an executable form without client script. Scope, page, order, scroll, pinned labels and child orientation retained their approved owners. | Scripted composition checks covered event routing; physical OS composition remained unverified. Source/browser/package checks did not rebuild the installed native app. |

The bounded addition to [In-Place Utility Action Continuity](../../../policies/review/interaction-evaluation.md#in-place-utility-action-continuity)
makes text-entry and visible-hit-bound checks explicit. It does not prescribe
autosave, one reference application's styling, or a universal caret position.
Same-author product validation is not independent review or a comparison of
guidance revisions; guidance effect remains **not assessed**.

### Later live-view restoration and deferred-input evidence

Generalized private source, browser and real-stream observations reviewed on
2026-11-12 extend this same ownership question to live editable views. Public
readers cannot inspect the original application or replay these executions here.
The [runtime-resource account](../../harness/runtime-evaluation/bounded-resource-lifetimes.md)
covers the same effort's queue/identity contracts without counting shared events
as independent support.

| Transition | Observation and correction | Boundary retained |
| --- | --- | --- |
| Repeated keyboard tab selection | A delayed editor-focus callback overrode the selector's synchronous focus, causing the next arrow to reach the editor. Keyboard navigation retained selector focus while pointer selection still focused the editor. | Compare after delayed callbacks and across repeated keys; one immediate active-state read was insufficient. |
| Loss and reacquisition of input authority | A native composition helper retained deferred work; a late composition end could send pre-loss text after authority returned. Cancellation retired that work, and a new composition then reached the real stream once. | The browser sequence proves the checked path, not physical keyboard or every input method. Idle observer output also had to retain observation/copy focus instead of repeatedly blurring it. |
| Keyboard paste rejection | A shortcut committed pending composition before the later multiline-paste decision. Deferring that commit to accepted paste preserved pending text on rejection. | On the checked platform, command-paste and the shell's control-key literal-input chord had different roles; no universal keymap is prescribed. |
| New or reused renderer | Text serialization omitted partial parser/control state. A typed, versioned checkpoint preserved supported logical continuation, while browser-local cursor initialization and input authority stayed local. Restored coordinates notified the input-method anchor. | Cell equality and an unopened renderer did not establish a focused cursor or final textarea geometry. This is not a claim of every terminal mode, grapheme or OS candidate-window behavior. |
| Rejected middle input fragment | Per-packet rejection alone allowed later fragments to remain eligible, and ordinary output cleared the error. Closing the affected stream, dropping unsent work and retaining partial-input feedback corrected the checked sequence. | Already accepted bytes could have reached the program; the repair did not make a whole paste atomic or roll back its prefix. |
| Hidden resource failure | The backend exposed an input fault while its background management row still appeared normal. Updating the row's change key, status and detail made recovery visible before reopening the view. | Failure detail stayed with its affected consumer; a healthy service or peer did not resolve that resource's fault. |

These observations support the bounded deferred-input/restored-view, delayed
keyboard-focus and existing status-consumer checks in Interaction Evaluation.
They do not require a particular emulator, persistence layer, font, shortcut,
buffer size or dense error UI. Operating-system input-method evidence is scoped
separately in the [native-host record](native-host-evidence.md); user-agent or DOM
simulation was not promoted to a native-host pass. No public runtime or guidance
comparison was executed; guidance effect remains **not assessed**.

## Work And Acceptance

This reference record assigns no separate task or runtime budget. The maintainer
authorized source integration and documentation validation. Acceptance of that
bounded change requires preserving the product-specific save and ordering
contracts, existing preference lifecycle checks, accessibility, and evidence limits.
A documentation pass cannot close a required product runtime check.

When affected controls are next evaluated, exercise their relevant input and
persistence sequences, including failures and applicable shared consumers. Record
the actual instruction revision, host, and input mechanism before claiming a
behavioral comparison. Broader effect or stability remains unverified until those
executions exist; this record does not automatically authorize or schedule them.

## Outcome And Reuse

The source change extends [Preference Scope And Lifetime](../../../policies/review/interaction-evaluation.md#preference-scope-and-lifetime),
adds [Sequential Control Input And Focus](../../../policies/review/interaction-evaluation.md#sequential-control-input-and-focus)
and [List Reordering Feedback And Commit](../../../policies/review/interaction-evaluation.md#list-reordering-feedback-and-commit),
and strengthens displayed-order checks in the existing Design Evaluation owner.
The standalone alignment method and checklist also check repeated-control sequences
and pointer-to-keyboard handoff. The supported lesson is to check transitions and
confirmed state rather than infer
usable or persisted behavior from a handle, a selected screenshot, or a queued write.

Disposition: promote these bounded checks, retaining the separate product contracts.
The primary agent reviewed this generalized account for meaning, necessary
information, and public fitness, including sensitive associations. Case acceptance
remains draft; rule implementation has separate maintainer authorization. Private
original receipts stay with the originating project's evidence owner and cannot be
verified by public readers through this projection.

Revisit when contrary evidence or a changed commit, save, or sorting contract
invalidates applicability. Source changes do not establish consumer refresh,
installation, activation, or better agent behavior. Exchange provenance for the earlier export was
session-only because no private exchange owner was configured for that export.

Revision 3 adds no new skill, persistence layer or universal keymap. It
implements the bounded checks at the existing shared policy owner; case acceptance
remains draft. Required product or physical-input checks keep their task owners.
The export does not commit, push, refresh consumers or claim observed runtime use
of the revised guidance; private exchange provenance remains at the task owner.

Revision 5 adds bounded inline-edit evaluation notes and reference evidence.
Existing work/readiness, historical subjects and draft case acceptance remain.
This export writes source only: no commit, push, consumer refresh, installed
native replacement or new product task is implied.

Revision 8 adds deferred-input, restored-view and delayed keyboard-focus criteria
at the existing policy owner, preserving all historical subjects and independent
record states. The source change is authorized commonization; it assigns no new
product task or missing-host campaign. Public fitness was reviewed by the primary;
case acceptance remains draft and source export does not establish consumer use.

## History

- 2026-10-26 — Revision 1. Created the state-transition reference after matching
  public subjects and questions. Added its catalog row. Related geometry and host
  evidence remain separately owned; copied descriptions are not new observations.
- Revision 2, 2026-11-02: updated current Design Evaluation and Interaction
  Evaluation links after their source relocation. Retained historical subject
  keys, source revisions and content fingerprints, observations and assessment
  states. Navigation maintenance adds no execution, empirical support or
  installation evidence.
- 2026-11-06 — Revision 3. Added bounded-history, per-window preference,
  shortcut/modal/composition, disabled-help and focus-scroll evidence. Added
  focused evaluation checks at the existing policy owner, retaining historical
  observations, product-owned capacities and the real-IME/physical-input gap.
- 2026-11-06 — Revision 4. Clarified that the session-only exchange statement
  describes the earlier export; the later revision retains its private task-owned
  provenance. This temporal clarification adds no execution, guidance effect,
  work assignment or adoption change.
- 2026-11-08 — Revision 5. Added pointer/keyboard caret, editing recognition, field hit bounds and save/recovery evidence, preserving source ownership and physical-input limits.
- 2026-11-08 — Revision 6. Clarified that the reported pointer click was near
  the middle of the title, avoiding confusion with the middle mouse button.
  The observation, evidence limits and independent record states are unchanged.
- 2026-11-09 — Revision 7. Added query ownership, preference recovery and
  results-first status evidence and bounded checks at the existing review
  owners. Kept earlier observations separately headed, preserving independent
  states, synthetic/native limits and the distinction between visible scroll
  anchoring and unchanged absolute offsets. No guidance effect is established.

- 2026-11-12 — Revision 8. Added live-view ownership, deferred composition, keyboard-paste rejection, receiver-local cursor/anchor and partial-input/background-fault evidence. Preserved platform, non-atomic prefix and native-input limits; implemented bounded existing-owner criteria without changing work or acceptance states.
