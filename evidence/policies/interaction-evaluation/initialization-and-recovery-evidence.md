---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-ui-initialization-recovery-evidence",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {
      "kind": "harness",
      "key": "policies/review/interaction-evaluation.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "4902a049a862d80974d5be4e1717e814c125cc116574550c81edb4f3a7aa6e50"
    },
    {
      "kind": "harness",
      "key": "policies/review/design-evaluation.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "c8652b61d4366a615a74ec669e03c8ada8178590bdc030ae2ea6ce77017eed26"
    },
    {
      "kind": "harness",
      "key": "harness/roles/functional-evaluator.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "c7621b65d4a4ebfe7839f8ef155e0b3f07f5d53d3707c41a62699420fe7930c6"
    },
    {
      "kind": "harness",
      "key": "harness/roles/spec-agent.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "bbf62349300a96da7523def9212dd56ebeb9c6d092e9ac9a3328d4db3e6194da"
    },
    {
      "kind": "harness",
      "key": "harness/templates/evaluation.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "bd7994d4da5762fd7f075680f82d9bdb84cc8aa53ce325ae170d1cad14927bf0"
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
      "ir-ui-state-transition-contracts",
      "ir-ui-native-host-evidence",
      "ir-ui-requested-control-rendering",
      "ir-change-impact-preservation"
    ],
    "supersedes": []
  }
}
---

# Initialization, recovery and sufficient UI observations

## Context And Applicability

What evidence establishes that an asynchronously initialized or refreshed surface
stays truthful and usable before, during and after readiness or failure? The owner
is [Interaction Evaluation](../../../policies/review/interaction-evaluation.md#initialization-and-recovery-check-sequence).
[Design Evaluation](../../../policies/review/design-evaluation.md#rendered-state-and-viewport-evidence)
owns visual comparisons; spec and functional roles apply the owned sequence.

Use this record when initialization, action readiness, category changes or
refresh can change presentation and behavior. Existing first-state, intermediate
frame, shared-owner and recovery criteria already apply. The new sequence makes
those checks concrete. This question concerns initial/readiness evidence and
recovery, alongside the existing
[stateful control and committed-intent case](state-transition-contracts.md),
[host-evidence case](native-host-evidence.md) and
[rendered-control case](../design-evaluation/requested-control-rendering.md).

## Evidence And Evaluation

The following are generalized private observations reviewed from retained task
receipts. Original captures and full historical runtime instruction inputs are
not available in this public projection. Reported product checks were executed
in their recorded scope; they were **not rerun as public UI reproductions** here.

| Recorded case | Preserved problem and reported correction | Limit |
| --- | --- | --- |
| Initial settings read | Empty labels and an inserted/removed loading message moved the content before readiness. Initial values and a stable progress location addressed the recorded transition. | Exact geometry, timing, styling and saved-value rules remain product-owned. |
| Read and readiness recovery | A failed registry read became an empty-list message after a category change, while unknown readiness exposed actions. Reported checks followed category changes, retry, failed refresh and recovery. | Unknown is not confirmed empty or ready. Each action has its own prerequisites; actual incorrect work execution was not established. |
| Bootstrap asset failure | The background was correctly isolated, but the controller failed before opening its first active surface. A preparation surface and ordinary scoped reload path preserved isolation and recovery. | Data-request failure and controller-asset failure are separate boundaries. This does not prescribe whole-app no-script support or a universal timeout. |
| Initial and polled lifecycle | A completed job with no output appeared to be preparing; initial and update consumers required the same state meaning. Reported checks also preserved actual output already displayed across a later empty read. | Lifecycle and artifact availability are distinct. Exact retention behavior follows the product contract; verification need not restart a job. |
| Sampling sufficiency | Static inspection found a range-only temporal assertion that could succeed with no observations or one instant. This identified a local oracle gap. | It did not establish that the earlier run had missing samples or that the UI defect recurred. Other observations and guarded paths provided counterevidence. |

The lifecycle event is also used in the
[impact-handoff case](../../harness/execution-loop-governance/change-impact-and-preservation.md);
that cross-reference is not another independent test.

Illustrative checks, **not run as new UI scenarios**:

- Observe the affected phase before initialization or interaction, then compare
  applicable initial, pending, ready, failed and recovered states on entry/revisit.
- Separate unreadable, confirmed empty and unknown readiness fixtures; repeat
  category/scope change, retry and refresh with the approved preservation rules.
- Fail an initialization asset independently of a data request where both paths
  exist; verify an operable approved recovery, isolation and preserved URL scope.
- Pair initial rendering with later polling/category updates carrying the same
  lifecycle meaning. Keep missing output separate from the underlying job state.
- Deliberately omit samples or capture only one phase: those observations must
  not establish cross-phase stability. A single image can still support its
  directly observed static properties.

Subject fingerprints identify the reviewed common-source baseline, not past
loaded instructions. A passing command, two reviewers agreeing or a later product
correction does not establish a causal effect of this check sequence. Guidance
change effect is **not assessed** without a controlled comparison.

## Work And Acceptance

This reference starts no product run or experiment. The authorized common-source
change installs the bounded sequence and its role/evidence pointers. Source
acceptance requires matching ownership, valid links/metadata, preserved scope and
coverage semantics and semantic disclosure review. Local QA implementation and
unverified native/physical-input or additional product states retain their owners.

Apply the sequence only to affected state boundaries. Choose representative
consumers, content and supported environments from the product contract. Treat
unobserved required phases as evidence gaps and assess their acceptance impact;
full test-suite success or endpoint success cannot substitute for the missing UI
observation. Fixing a sampler requires renewed affected evidence before broader
claims. Further execution or guidance-effect comparisons need separate task authority.

## Outcome And Reuse

The supported lesson is to verify both truthful state meaning and the existence
of observations from the phases being claimed. Disposition: promote the bounded
sequence under existing review assets, retaining their already-required checks.
No new skeleton framework, global delay threshold, mandatory viewport cross-product
or replacement workflow is implied.

The primary reviewed this public projection for standalone meaning, necessary
information, sensitive content and revealing associations before source write.
Private source identifiers and exchange links stay private. Case acceptance is
draft, independent of source-rule implementation. This source update establishes
neither consumer installation, observed use nor improved future task outcomes.

## History

- 2026-11-04 — Revision 1. Added the distinct initialization/readiness evidence
  question after reconciling existing state/intent, geometry and native-host
  records. Generalization retains failure and recovery predicates while removing
  identifying values and product-specific measurements. Public examples remain
  unexecuted and the original product evidence retains its scope limits.
