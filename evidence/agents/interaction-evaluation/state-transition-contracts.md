---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-ui-state-transition-contracts",
  "revision": 1,
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
      "ir-ui-native-host-evidence"
    ],
    "supersedes": []
  }
}
---

# Stateful controls and committed intent

## Context And Applicability

This record asks how review can distinguish transient presentation from committed
selection, order, and persisted intent during repeated input. The primary owner is
[Interaction Evaluation](../../../agents/policies/review/interaction-evaluation.md).
[Design Evaluation](../../../agents/policies/review/design-evaluation.md#nested-collection-hierarchy-and-ordering)
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

The source change extends [Preference Scope And Lifetime](../../../agents/policies/review/interaction-evaluation.md#preference-scope-and-lifetime),
adds [Sequential Control Input And Focus](../../../agents/policies/review/interaction-evaluation.md#sequential-control-input-and-focus)
and [List Reordering Feedback And Commit](../../../agents/policies/review/interaction-evaluation.md#list-reordering-feedback-and-commit),
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
installation, activation, or better agent behavior. Exchange provenance is
session-only because no private exchange owner was configured for this export.

## History

- 2026-10-26 — Revision 1. Created the state-transition reference after matching
  public subjects and questions. Added its catalog row. Related geometry and host
  evidence remain separately owned; copied descriptions are not new observations.
