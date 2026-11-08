---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-result-preserving-performance",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {
      "kind": "resource",
      "key": "policies/baseline/code-quality.md",
      "source_revision": "410ee4a06ee606deafe05876fb5edcbf9a6eafc2",
      "content_sha256": "12bc91345fd9a01b28cdc761dc8da7e74542537852e6f06b52a1bdcbacebcfd0"
    },
    {
      "kind": "skill",
      "key": "skills/clean-code/SKILL.md",
      "source_revision": "410ee4a06ee606deafe05876fb5edcbf9a6eafc2",
      "content_sha256": "b5c023740080e604bf80bff7e0e6963e03b22ce31d101d88b6044394be528a53"
    }
  ],
  "work": {
    "basis": "not-applicable",
    "state": "not-applicable",
    "readiness": "not-applicable"
  },
  "knowledge": {
    "state": "candidate"
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
    "rule_status": "not-proposed"
  },
  "relations": {
    "related": [
      "ir-change-impact-preservation",
      "ir-code-quality-human-readability"
    ],
    "supersedes": []
  }
}
---

# Result-preserving performance investigation

## Context And Applicability

How can a local data application remove repeated database, filesystem and index
work while retaining the same admitted results and lifecycle behavior? The
primary owner is [Code Quality](../../../policies/baseline/code-quality.md);
[Clean Code](../../../skills/clean-code/SKILL.md) supplies a related bounded
inspection method. This record retains evidence, not another normative policy,
a benchmark suite or a new optimization task.

Use these observations when a measured path repeats independent aggregation,
owner lookups, fallback reads, directory descent or reusable index preparation.
An intentional full-candidate ranking, inexpensive current path or shared
registry is not inherently defective. Preserve eligibility, ordering, exact
arithmetic, read snapshots, observation times, immutable facts, resumption and
failure/cancellation semantics before choosing a cache or moving a filter.

The projection preserves the computation and distinguishing boundaries while
removing private corpus contents, project identities, row totals and local
latencies. Synthetic fixture sizes below were executed in the original private
product checks; they are not newly executed public reproductions. Original
receipts remain private and cannot be inspected through this record. Subject
fingerprints identify the shared files inspected for this export, not the exact
historical installed/provided instructions. Those identities and complete model
settings are unknown. No causal skill or guidance effect is established.

## Evidence And Evaluation

Selected execution receipts, implementation and regression controls were
reviewed on 2026-11-08. Product results came from same-author source, synthetic
browser/package checks and paired read-only local comparisons. This export
does not replay the product or disclose a personal database.

### Locate the expensive computation before changing it

| Observed path | Work removed | Preserved result and distinguishing boundary |
| --- | --- | --- |
| Small paginated list with a costly source summary | Joining an owner's independent file and session children expanded intermediate rows roughly as file count times session count. Independent child aggregates retained the same summary without that multiplication. | Preserve eligible-session counts, file-error counts, document-root admission and zero/null semantics. A small page query or unchanged number of SQL calls did not explain the whole server-render cost; DISTINCT counts could conceal the expanded intermediate work. |
| Keyword results with per-result owner reads | One-to-one owner metadata joined into the candidate query instead of being read again for each result. | Exact registered-root identity and private-runtime exclusions still ran before the result limit. Earlier rejected hits could not displace later admitted hits; snippet, score, order and evidence URLs matched. FTS internal trace statements were counted separately from application SELECTs. |
| Chart timestamp fallback | Only records with both metadata times missing or invalid entered event-time batches of at most 500 IDs. A 300-record synthetic comparison used 301 versus 2 SELECTs with all fields equal; a 1,200-record regression exercised multiple batches. | Valid metadata remained authoritative. Python parsing and UTC extrema preserved offset/invalid-time behavior; SQL lexical MIN/MAX would not be equivalent. Only identity/time fields were read, without event bodies. The current valid-metadata fast path was already one query. |
| One external-item detail loading a full inventory | Stable-ID restriction ran before joined body loading and projection, while the full-inventory path stayed available. | Complete nonempty detail dictionaries matched, including classifications, evidence and memberships. Missing and out-of-range integer IDs retained the prior no-result behavior instead of introducing a binding overflow. Comparing two empty results would not establish detail parity. |
| Usage aggregation dominated by row processing | Disjoint indexed null/earlier/ordinary/later raw-time ranges avoided a broad exceptional-time scan and general per-row merge. The ordinary cursor opened first to retain its prior snapshot; concatenation retained raw-time/ID order. Fetches of at most 512 rows, final cursor closure, one-time column-position resolution and local bucket-date reuse reduced processing. | Preserve exact Decimal addition and its input order, parsed UTC/local-time boundaries, invalid/untimed limitations, source/project/maintenance scope, synthetic/replay exclusions and frozen attribution. No floating SQL SUM or persisted cache replaced those contracts. Four targeted reads improved the measured path despite replacing two broader reads. |

Usage controls included null, empty, whitespace and invalid timestamps, week and
basic ISO forms, large offsets, timezone boundaries, empty scopes and exact
cost cancellation beyond floating or SQL-integer precision. Complete returned
models matched in paired fixed-snapshot/fixed-time comparisons; repeated runs
were repetitions, not extra independent scenarios. Simpler compound-query and
dictionary-row alternatives did not improve every measured path and were not
retained. These observations support profiling the actual computation rather
than treating fewer SQL calls as the optimization objective. Local timings are
environment-specific and establish no universal latency promise.

### Reuse work only within its valid lifetime

| Observed path | Reported synthetic comparison or correction | Preserved lifecycle and limit |
| --- | --- | --- |
| Excluded filesystem trees | Pruning before descent reduced directory reads from 204 to 1 for 100 excluded subdirectories and 10 retained Markdown files, with the same sorted paths. | Preserve case-sensitive file eligibility, file symlinks, no directory-symlink descent, registered-root eligibility, error/cancellation and stale-record behavior. Filtering only after recursive discovery had paid the traversal cost already. |
| File-change metadata | One snapshot taken after source admission and lifecycle writes replaced repeated path metadata reads for 32 unchanged files. | Keep fresh filesystem stats and no-reparse behavior; Session/Event/Usage payloads stayed unchanged. Per-record reference/evidence freshness queries remained, so synchronization was not made constant-query overall. |
| New-record attribution | Thirty records in one store call reused one workspace lookup rather than thirty. | Cache only the lookup within that call: each record retained its own observation time, a later call observed changed Git metadata, and existing facts/prices remained frozen. Caching the whole attribution result would incorrectly freeze time or stale metadata. |
| Resumable vector preparation | Loading existing staged hashes and batching prior-vector reads by at most 256 keys reduced SELECTs from 354 to 15 for 177 fragments with encoder batch 16. Parent, fragment, vector-blob and term rows matched; 177 were reused and zero encoded. | A resumed stage was not assumed empty. Do not eagerly load every vector blob; preserve occurrence order, batch flushes, validation, force/cancel behavior and atomic publication. This reuse fixture establishes no model-inference speedup. |
| Compatibility backfill | Adding WHERE updated_at IS NULL stopped already-populated rows being UPDATE targets while retaining the created-time repair value. | The statement may still scan, and initialization also ran on public scan entry, not only process startup. This is not evidence that all startup work disappeared. |

The same audit also identified same-root document-body preparation. Opening a
folder-backed document bulk-loaded identities and bodies, including unlinked
documents; ordinary links did not recursively fetch every connected note.
Existing embeds had depth/cycle bounds. Lazy body loading remained a candidate,
not a delivered optimization. Other explicitly parked development features
remained unchanged. A census of SQL-bearing call sites, including writes and
DDL, was not a count of SELECTs or complete runtime coverage.

The historical code-quality baseline and scoped inspection method were relevant,
but a passing product comparison does not prove their causal contribution.
Public execution and a controlled guidance comparison were **not run**; guidance
effect is **not assessed**. Evidence maturity is the original observed stage,
with partial coverage and no independent implementation review.

## Work And Acceptance

This reference assigns no common work, executor or runtime budget. The user
authorized source export and documentation validation. Public-fitness review
must preserve the problem structure and limits without private dependencies;
record/schema/link checks establish only those documentation properties.

For a future authorized optimization, freeze the applicable input snapshot and
clock, compare complete admitted outputs and relevant failure/no-change paths,
and measure the actual bottleneck. Keep query count, intermediate cardinality,
database time, server rendering, browser interaction and packaged delivery as
different measurements. A result-preserving local change does not close a
required native or recipient check. This record neither schedules missing tests
nor authorizes collecting personal sources.

## Outcome And Reuse

The candidate lesson is to remove repeated work at its actual owner while
preserving the lifetime and semantics of the reused result. Confidence is
bounded by paired full-output checks and discriminating synthetic controls;
current fast paths, rejected alternatives and unimplemented candidates constrain
reuse. Existing Code Quality already requires behavior, lifecycle, performance
and proportionate verification, so no new baseline rule or skill edit is
justified by this export. The related impact record owns migration and
source/user-state preservation, without counting shared events as replication.

Knowledge remains candidate, case acceptance draft, normative rule not proposed
and work not applicable. Primary semantic/disclosure review approves this public
projection; it is not independent review or public reproduction. Revisit when
changed data distributions, plans, timestamps, admission rules, cache lifetimes
or contrary evidence invalidate a reported boundary. Source integration does
not establish commit/push, consumer refresh, installation, native replacement or
observed future use; private exchange associations remain at the task owner.

## History

- 2026-11-08 — Revision 1. Matched the actual public collection and created one
  reference for result-preserving repeated-work reduction. Retained contrary
  alternatives, cache/snapshot contracts, unimplemented scope and delivery limits.
  Generalization and source checks add no new product execution or effect claim.
