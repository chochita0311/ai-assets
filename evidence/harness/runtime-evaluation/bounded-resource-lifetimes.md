---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-bounded-runtime-resource-validation",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {
      "kind": "harness",
      "key": "harness/roles/contract-evaluator.md",
      "source_revision": "add7f35b084c2bbe463d2fd7914b8921e92dc265",
      "content_sha256": "5a9c04f1469090ea468573adfc2924a60d64f443bbc84226f5d47b6d296a5972"
    },
    {
      "kind": "harness",
      "key": "harness/roles/functional-evaluator.md",
      "source_revision": "add7f35b084c2bbe463d2fd7914b8921e92dc265",
      "content_sha256": "12ba3d29eedfd1012c6a0bf695da02457cf426df6d36013a5d0bffacc733f97d"
    }
  ],
  "work": {
    "basis": "requested-extension",
    "state": "resolved",
    "readiness": "not-applicable"
  },
  "knowledge": {
    "state": "supported"
  },
  "evidence": {
    "kinds": [
      "static-observation",
      "generalized-private-observation"
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
      "ir-result-preserving-performance",
      "ir-codex-review-challenger-validation"
    ],
    "supersedes": []
  }
}
---

# Bounded resource progress and lifetime identity

## Context And Applicability

How can evaluation establish bounded memory and correct ownership without
stalling cooperative work or acting through stale identity? This shared runtime
evaluation question belongs to [Contract Evaluator](../../../harness/roles/contract-evaluator.md)
for producer/consumer, identity and recovery contracts, and
[Functional Evaluator](../../../harness/roles/functional-evaluator.md) for actual
progress, failures and peer/control behavior. Their conditional checks remain
the rule owners; this record retains supporting observations, not another
runtime framework or mandatory benchmark suite.

Apply when approved work changes bidirectional streams, automatic protocol
responses, queues, background resources, process recovery or cached runtime
readiness. A finite output history or a bounded UI outbox does not establish a
bound on a separate reverse-direction queue. Close, exit, lease loss and view
removal can be different lifetime events. Limits, protocols, supported platforms
and termination policy remain product decisions; this record supplies no
universal buffer size, timeout, keymap or architecture requirement.

The account generalizes private source, synthetic runtime and browser/OS probes
while excluding project identifiers, original inputs, paths, hashes, captures and
measurements. Metadata identifies shared owner files inspected before this
export, not all historical loaded instructions. The original private checks ran;
public reproduction and execution of the revised guidance were **not run**.

## Evidence And Evaluation

| Boundary examined | Observation and reported correction | Counterevidence or limit |
| --- | --- | --- |
| Automatic replies without a visible client | A raw program emitted queries but did not read the replies. Ordinary output was bounded while a separate manager-to-program queue grew. A finite equal-byte text/query comparison distinguished that path. A bounded writer and explicit per-resource fault retained management and healthy peers. | Output parsing and client input limits had been real but covered different queues. The finite observation established that cause, not endless-soak or every-program stability. |
| Cooperative duplex progress | An initial cap repair paused output when input backlog rose. A cooperative read/write program then blocked writing, stopped reading, and could not drain the input needed to resume output. Removing that cross-direction pause dependency let all accepted bytes drain. | Raw-mode readiness was confirmed before the paired comparison. Earlier no-ready attempts did not establish accepted-data loss. Repeated bytes/counts established progress; separate mixed-byte tests covered ordering. |
| Packet admission versus user-action interruption | Rejecting one fragment did not by itself stop a later suffix. The affected stream was closed before receiving later fragments; unsent work was dropped with retained partial-input feedback. | Accepted prefix bytes could already have reached the program. This was not an atomic paste or rollback guarantee. UI/authority details are the same events in the [state record](../../policies/interaction-evaluation/state-transition-contracts.md), not independent replications. |
| Resource close versus owner exit | Direct writes using a retained numeric descriptor bypassed the dependency's earlier close gate. Writer ownership was tied to resource close as well as process exit, with a closed-writer admission guard. | Closing stdio in the proposed OS probe did not induce master-close-before-exit. Controlled close with actual numeric descriptor reuse observed no replacement-file writes after the guard; actual wrong-target delivery was not observed. |
| Reused process locator | A stale process locator could name an unrelated live process and block explicit fresh recovery. Positive birth identity distinguished that case while keeping a matching live or unknown identity protected. | The recovery did not adopt/replay old work or prove orphaned programs had ended; no destructive signal to the unrelated process was observed. |
| Display-dependent identity | The same live process's birth string differed with caller timezone, producing a false replacement classification. Canonical UTC time with the C locale and a tagged compatible format removed it; unknown legacy formats stayed protected. | This was a primary-discovered discriminator, not another independent reviewer discovery. Same-process checks across timezones and an actual isolated service checked the correction; wrong-process shutdown was not exercised. |
| Runtime readiness after environment change | The readiness check accepted a cache while only the install-time architecture's helper was executable; source inspection predicted failure after a runtime-architecture change. Setup/explicit start now prepare the supported helpers, and missing helpers invalidate readiness. | Controlled helper and startup checks did not establish execution on every architecture. Marker/import success was necessary evidence, not a complete executable-integrity audit. |
| Detached protocol ownership | A query depended on a visible renderer and timed out while detached. The background owner supplied ordered reports; the view suppressed duplicate replies while retaining mutations, with version compatibility checked before authority. | A partial control sequence crossing a fresh checkpoint was tested separately from complete commands. This supports the specified protocol subset, not every emulator or control sequence. |

Resource observations also checked a nonempty admitted corpus actually appearing
in existing screens, zero/single/multiple resources, hidden views and a producer
still alive and advancing during peer/control samples. An earlier unregistered
source produced an empty search path and was excluded from performance evidence.
Manager, backend, children and whole-browser costs remained separate; whole
browser RSS included shared mappings, warm caches changed later samples, and a
short rounded idle CPU sample was not a zero-cost guarantee. No universal
latency, additive per-pane memory or guidance-effect conclusion followed.

Initial source candidates and later informed repair critiques led to different
primary-owned tests. A simulated close, an OS event, a fixture setup failure and
an observed product failure were retained as different evidence. Public readers
cannot inspect the originals through this account; related research/runtime/UI
records share the effort and do not multiply its independent support.

## Work And Acceptance

The bounded requested common-source work is resolved: conditional resource,
identity, readiness and progress checks were added to the existing Contract and
Functional evaluator owners and statically validated. This is not a pending
product fix or an assignment to run a new benchmark, install an engine or stop
user jobs. Case acceptance remains draft, separate from implemented source
criteria. A future consuming task selects only checks relevant to its approved
contract, authority and environment.

Broader claims would require their own identified runtime and suitable controls:
actual resource close/exit ordering where claimed, concrete architecture execution,
current/failing/unknown identity branches, liveness during measurement and
observed user-facing recovery. This record does not authorize those actions or
silently close untested host, long-duration or intentionally detached-work limits.

## Outcome And Reuse

The supported bounded lesson is to evaluate queue budgets, progress and identity
at their real owners and lifetime boundaries. A local successful helper, bounded
history, empty screen or passed unit suite cannot stand in for a different
producer, receiver or measured path. Pair stalled and cooperative peers, and
pair cancellation with new-work recovery, before claiming that a repair preserves
both bounds and useful behavior. Canonical identity and positive evidence remain
separate from a reusable locator or display string.

The primary reviewed meaning, standalone usefulness, private associations and
public fitness. Original evidence/receipts remain at their private owner. No
independent public reproduction or controlled old/new-guidance comparison was
performed; guidance effect is **not assessed**. Source export does not establish
commit/push, consumer refresh, installation, runtime activation or general
reliability. Revisit when changed queue semantics, identity formats, dependency
close behavior or contrary outcomes invalidate an applicability condition.

## History

- 2026-11-12 — Revision 1. Matched the public collection and created one distinct
  resource-progress/lifetime question. Added bounded existing-owner checks and a
  catalog row. Preserved the unconfirmed OS trigger, controlled close boundary,
  corrected probe prerequisites, primary timezone discovery and partial coverage.
  No new runtime execution or publication was performed by this export.
