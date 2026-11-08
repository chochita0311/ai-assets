---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-change-impact-preservation",
  "revision": 3,
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

### Later Capability And Delivery-Closure Evidence

Private delivery receipts reviewed on 2026-11-06 add the following impact paths.
They report local executions with synthetic data, not public reproductions.
The account preserves caller, ownership and failure relationships while omitting
private app identities, exact build fingerprints, paths and task associations.

| Recorded change | Impact path and reported closure | Limit |
| --- | --- | --- |
| Omit unavailable capabilities from a packaged edition | Hiding navigation alone left imports, startup hooks, route handlers, legacy reader links and visible settings/recovery consumers depending on excluded features. The capability boundary was applied before those dependencies, and surviving consumers used their included owner. Checks also preserved stored excluded records and the other edition's supported behavior. | This was a packaging boundary, not authority to delete retained data or remove the capability from every edition. Existing positive-state suppression and actual-consumer rules already applied. |
| Match help to delivered behavior | Only shipped app guides were localized; a later correction placed one language option at the guide contents owner rather than repeating it per article. Topic/URL/history and the surrounding app language retained their distinct owners. Storage and cleanup copy also had to describe the included handler rather than an excluded feature. | Guide-only language selection did not authorize global application localization or rewriting unrelated repository docs. Correct copy still needed real behavior evidence. |
| Expose storage boundaries truthfully | Measurements distinguished app-owned data/cache, shared model storage and free space on each relevant volume, including partial or unavailable reads. Cleanup wording preserved the difference between disposable app cache and shared files used elsewhere. | Unknown was not zero, shared totals were not app-exclusive usage, and documentation of another operating system's expected paths did not establish execution there. Exact paths, units and deletion authority remain product-owned. |
| Replace an identifiable canonical build | A candidate was checked before replacement of owned app/archive/checksum outputs. Review and failure witnesses exposed interruption after renaming the old output; publication kept a recoverable backup through that boundary and retained it if recovery failed. A separate delivery-location correction restored the established final output owner after verified staging. | Staging was not final delivery. Dirty source required a content fingerprint in addition to its commit; a changing-input candidate was rejected. These checks did not establish public signing, recipient installation or another operating-system build. |

Static review candidates were adjudicated through primary before/after witnesses;
reviewers did not perform runtime validation or approve acceptance. Fixture/oracle
assumptions that disagreed with actual viewport or path behavior were corrected
separately from product defects, with earlier failures retained. This is scoped
support for impact closure, not a comparative assessment of reviewer quality.

The existing governance, positive-state suppression, source/runtime identity and
action/status scope rules already cover these relationships. No further harness
role, flow, template or tool-binding change is justified by this export. No
controlled guidance comparison or new product run was made; preventive effect
remains **not assessed**.

Source inspection for revision 2 used `harness/policies/execution-loop-governance.md` at common-source
commit `19e14c8d48fc9ba3106219969f6ca70802479032`
(SHA-256 `ef7831920f523adbc5d5164dc6a275633fd09522d75d2928040aa0d45b5abb4d`).
Historical subject fingerprints above remain unchanged. This identifies the
compared shared source, not the instructions loaded during product executions.

### Later Schema, Ownership And Workspace Eligibility Evidence

Private product receipts and selected source/tests reviewed on 2026-11-08 add
three preservation paths. They describe observed product work; this export did
not execute a public reproduction or migrate a personal runtime database.

| Change and owner | Reported preservation and distinguishing controls | Limit |
| --- | --- | --- |
| Physical order of a nullable display-title column | Fresh and admitted existing tables put the user override after the source title. A verified backup preceded a validated SQLite rebuild. IDs, parent/child links, events, pins, frozen usage, explicit indexes and existing overrides survived. Unknown columns, triggers or constraints refused the rebuild; checks went beyond column metadata to constraints such as CHECK/collation. A copy failure restored table/data/indexes and FK setting, and repeated startup did not rebuild again. | Column-order requirements are product-specific; this is not a recommendation to rebuild tables for cosmetic changes. A read-only real-database preflight proved only the inspected shape and FK status, not a completed runtime migration. |
| Source title versus user override | Eligible primary-work records accepted bounded single-line overrides; blank input stored SQL NULL and restored the source label. Imported or forced reprocessing preserved the override. Pins and chart labels used it while source-backed search evidence retained its original owner; child records stayed read-only. | A title shown to users and a title used as imported evidence need not have the same write owner. Do not treat user-owned fields as rebuildable ingestion output. Exact validation bounds remain with the product contract. |
| Shared workspace registry versus visible projects | Session working directories and document-owning folders could both populate a shared registry. Finding an ancestor's .git entry did not prove the user had opened a project or that a path mention in session text triggered collection. The visible list was narrowed to paths with eligible primary work in the selected sources, retaining registry rows. Admitted synchronization refreshed known path presence even without reparsing unchanged source files, so a removed then restored folder recovered its status while identity, pins and frozen facts survived. | Shared storage membership, Git ancestry, presentation eligibility and current filesystem presence are different claims. The ancestry rule checked .git existence, not a guaranteed directory type or a complete Git validation. This fix did not authorize registry deletion, filesystem crawling from prose, or history rewriting. |

Existing impact and ownership governance already covers these dependencies; no
new harness role, flow, template or global migration policy is added. Product
checks were same-author and bounded to source/browser/package delivery. The
related [performance case](../../policies/code-quality/result-preserving-performance.md)
owns repeated-work and cache-lifetime observations from the same work episode;
cross-reference is not independent evidence. Guidance effect is **not assessed**.

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

Revision 2 updates evidence under the existing owner and leaves implemented
governance unchanged. It creates no pending work for product corrections already
completed. Recipient, physical-input, signing and untested-platform gaps remain
with the product acceptance owner; they are not new common-source assignments.
This local export performs no commit, push, installation or consumer refresh.

Revision 3 adds evidence under the existing governance owner. Previously
completed product corrections are not new pending common work. Work/readiness,
historical fingerprints and adoption states are unchanged; no commit, push,
installation, consumer refresh or native product replacement is performed.

## History

- 2026-11-04 — Revision 1. Added this distinct handoff question after checking the
  current evidence catalog, Code Quality and existing state/native/geometry cases.
  Private identifiers, paths, source artifacts and exchange associations remain
  private. Generalization preserves the consumer relationship and counterevidence;
  it does not present changed public examples as reproduced private outcomes.
- 2026-11-06 — Revision 2. Added capability-dependency closure, guide-only
  language/storage truthfulness and interruption-safe canonical publication
  observations. Retained existing governance because it already covers actual
  consumers and preserved contracts; added no universal platform or build policy.
- 2026-11-08 — Revision 3. Added backed-up admitted migration, imported/user-title ownership and registry/display/presence evidence. Retained existing governance and runtime-migration limits.
