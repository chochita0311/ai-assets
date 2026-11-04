---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-change-impact-preservation",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {
      "kind": "harness",
      "key": "harness/policies/execution-loop-governance.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "a58b1fc8f2779054900a36ac1cc549d8f4e271b40791da435385308860b15f0d"
    },
    {
      "kind": "harness",
      "key": "harness/roles/orchestrator.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "31de44d8b28efdb0af0c5a902f9d39bec43e8d16ea980f20b45a6ff3746ef25c"
    },
    {
      "kind": "harness",
      "key": "harness/roles/builder.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "5c21065801a312e14e9d26b7e796f1f74868de076db91324278f29abc13d46bb"
    },
    {
      "kind": "harness",
      "key": "harness/roles/functional-evaluator.md",
      "source_revision": "8e7ee008c067c7a3aae2fff4beb9ea471a63c2c8",
      "content_sha256": "c7621b65d4a4ebfe7839f8ef155e0b3f07f5d53d3707c41a62699420fe7930c6"
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
      "ir-ui-initialization-recovery-evidence"
    ],
    "supersedes": []
  }
}
---

# Actual impact paths and preservation handoffs

## Context And Applicability

How should a delivery handoff preserve existing behavior when the real impact of
a bounded fix extends beyond the surfaces listed initially? The owner is
[Execution Loop Governance](../../../harness/policies/execution-loop-governance.md#change-impact-and-regression-scope),
with [Orchestrator](../../../harness/roles/orchestrator.md),
[Builder](../../../harness/roles/builder.md), spec and evaluator roles applying it.

Use this clarification for actual call, data, storage, rendering or execution
dependencies. Existing Code Quality already requires scoped, necessary changes;
contract regression checks and shared-owner evaluation also cover much of the
principle. The change connects those duties to delivery handoff and closeout,
including fixes that keep the approved contract. File adjacency or a desirable
unrelated cleanup does not establish an affected consumer.

## Evidence And Evaluation

Private product receipts and a static review supplied a bounded example: the
initial page used a preparation placeholder for a completed job with no output,
while the refresh consumer only replaced text when output was nonempty. Changing
the initial page alone could leave an already mounted page with the old meaning.
The reported correction connected the shared state description, initial page,
status response and browser update. That correction already covered its consumers;
this account does not allege a remaining product defect or prove guidance failure.

The same lifecycle example informs the related
[initialization and recovery record](../../policies/interaction-evaluation/initialization-and-recovery-evidence.md).
Its appearance in two records addresses different questions and adds no independent
execution. Earlier product checks were reported as executed; raw temporary
captures are unavailable to this public account and were not rerun here. Public
readers cannot independently verify the private execution through this projection.

Illustrative checks, **not run as new product scenarios**:

- A shared formatter changes: inspect initial and live-update consumers and
  verify both the intended correction and a representative unchanged value.
- A discovery fix changes eligible records: inspect downstream reconciliation
  and preserve identities/accounting required by the owning product contract.
- A contract stays unchanged but a shared implementation changes: identify newly
  discovered consumers instead of treating the original regression list as complete.

Subject fingerprints identify the shared-source baseline reviewed for this
clarification. They do not reconstruct the instructions actually supplied during
historical product work. No controlled guidance comparison or forward task test
has been performed; preventive effect is **not assessed**.

## Work And Acceptance

This reference assigns no task or experiment. The authorized common-source work
adds a bounded clarification in existing governance and role owners. Its source
acceptance checks are role/owner consistency, valid references, proportionate
scope, preservation of existing lane/return semantics and disclosure review.
These checks cannot establish product correctness or better future agent behavior.

At the next authorized relevant delivery, keep the change, shared owner, affected
consumer, preserved contract and checked/unverified evidence in the existing
handoff. Select discriminating normal, failure, positive or no-change controls
in proportion to propagation and risk. Do not require a new form or whole-app
viewport/state/host matrix for a small fix. A broader effectiveness claim needs
a separately authorized comparison with the same task and relevant controls.

## Outcome And Reuse

The supported lesson is the value of tracing a bounded behavioral change through
its real consumers before claiming preservation. The added wording is an
operational clarification of existing principles; the example does not prove
that more instructions prevent regressions.

Disposition: promote the bounded source clarification. The maintainer authorized
source integration; the primary reviewed this generalized account for public
fitness before a publishable write. Case acceptance remains draft and separate
from rule implementation. Publication, consumer refresh and actual runtime use
are separate actions and are not established by this source change.

Honor existing scope and lane authority. Complete necessary dependent changes
within approved contracts; another module alone does not reopen approval.
Unresolved product meaning, ownership, acceptance or lane authority follows
existing spec/planning returns. Retain actual delivery and evidence gaps at their
owning task rather than claiming that a source pass updated active clients.

## History

- 2026-11-04 — Revision 1. Added this distinct handoff question after checking the
  current evidence catalog, Code Quality and existing state/native/geometry cases.
  Private identifiers, paths, source artifacts and exchange associations remain
  private. Generalization preserves the consumer relationship and counterevidence;
  it does not present changed public examples as reproduced private outcomes.
