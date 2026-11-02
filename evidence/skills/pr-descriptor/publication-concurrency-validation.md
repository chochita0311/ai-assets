---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-pr-description-concurrency-validation",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {"kind": "skill", "key": "skills/pr-descriptor/SKILL.md", "source_revision": null, "content_sha256": "f30beef6635d6e652cb90c76414ec4817d3bbff2416c6380c8cdcbb7eb9adaf4"},
    {"kind": "resource", "key": "skills/pr-descriptor/scripts/pr_description_transaction.py", "source_revision": null, "content_sha256": "b7001a126d65171d8e3f7d606f217cc5654099bba48d6f6fe6a25e48c2c1a308"},
    {"kind": "resource", "key": "skills/pr-descriptor/scripts/test_pr_description_transaction.py", "source_revision": null, "content_sha256": "6564b744fbe707f94ff576b8dc713b522f1291d26868a278455e5367cb60a2e0"}
  ],
  "work": {"basis": "evidence-gap", "state": "open", "readiness": "waiting"},
  "knowledge": {"state": "supported"},
  "evidence": {"kinds": ["static-observation", "generalized-private-observation", "public-execution"], "maturity": "resource-execution", "execution": "run", "coverage": "partial"},
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": ["ir-documentation-content-role-validation"], "supersedes": []}
}
---

# PR-description publication concurrency validation

## Context And Applicability

The improvement question is whether PR-description publication checks the body
and concurrency marker captured **before drafting**, rather than accepting a
new baseline after the candidate already exists. The [PR Descriptor skill](../../../skills/pr-descriptor/SKILL.md#separate-composition-from-publication)
owns the workflow, and its [transaction helper](../../../skills/pr-descriptor/scripts/pr_description_transaction.py)
owns deterministic final checks, one file-based write and post-write
verification. Review/comment publication by other skills is outside this record.

The prior helper read an already-written candidate, fetched the then-current
remote body, created its backup from that fetch, and compared the marker only
across its own subsequent fetches. A concurrent edit between the user's original
capture and helper entry could therefore become the helper's fresh baseline,
allowing a candidate drafted against older text to overwrite that edit. The
problem was the capture boundary, even though later pre-write checks existed.

The corrected workflow resolves the exact PR, captures its body and `updatedAt`
into a separate backup and marker, and then drafts the complete candidate in a
different file. The helper requires that **pre-existing** backup and mandatory
`expected_updated_at` / `--expected-updated-at`; it never creates or overwrites
the backup. It compares both body and marker to that capture on entry and again
immediately before publication, stopping on either mismatch. The old standalone
call interface intentionally fails without the new inputs; callers must
complete capture before drafting and pass the captured values.

## Evidence And Evaluation

### Source And Execution Boundary

The metadata fingerprints identify the assessed skill entry, helper and test
file. `source_revision` remains null because those files were uncommitted when
evaluated; a later commit must not be backdated as their test-time source.
The public [offline test suite](../../../skills/pr-descriptor/scripts/test_pr_description_transaction.py)
uses a fake remote and fake command runner, so it is executable public evidence
without external writes. Completed-run observations and the author-separated
review are reported from the originating private conversation. Its diagnostic
scratch was removed after review, and no surviving raw log or hidden actor trace
is asserted. A separate closeout resource recheck is distinguished below.

The reported author execution on Python 3.14 passed all **14 offline tests** in
0.010 seconds. The subsequent closeout log recorded the same 14 tests passing
in 0.012 seconds; this is a resource recheck, not another independent workflow
trial. These are deterministic resource tests, not a fresh agent task using the
full skill. The public reproduction command is
`python3.14 -B skills/pr-descriptor/scripts/test_pr_description_transaction.py -v`.
The tests cover:

| Control | Observed assertion |
|---|---|
| Matching capture | Exactly one candidate write and exact post-read body; original backup bytes retained, including CRLF and an empty original body. |
| Empty candidate | Zero remote reads/writes without a current-turn clear flag; the explicitly allowed clear publishes an empty body and preserves the backup. |
| Remote update during drafting | Entry mismatch stops on the first fetch with zero writes, preserving the other actor's body and original backup. |
| Wrong marker or backup body | Either entry mismatch stops with zero writes. |
| Marker change at recheck | Two fetches, then zero writes. |
| Body change with the same marker | The body comparison stops at recheck with zero writes. |
| Missing or non-file backup | Refusal before remote access; no backup is created. |
| Missing, empty, whitespace-only or `None` marker | Required API argument or validation rejects it before remote access. |
| CLI marker requirement | Missing or empty `--expected-updated-at` fails before remote access. |
| Missing candidate or shared candidate/backup path | Refusal before remote access, preserving the backup. |
| Candidate mutation detected after validation | Refusal after the first fetch and before publication. |
| Post-write body mismatch | Exactly one write, then verification failure with no retry or restore. |
| Authorization and exact full URL | Missing current-turn publication authorization and a shorthand PR target fail before remote access. |
| `gh` adapter | Full PR URL, target-derived `GH_HOST`, `shell=False` and `--body-file` with the candidate path; no inline body or stdin publication. |

The helper reads UTF-8 files with `newline=""`, retaining exact line endings for
body comparison, and treats the backup as read-only. It validates a non-empty
marker, distinct resolved file paths, actual files and a non-empty candidate
unless clearing is explicitly allowed. It re-reads the candidate before the
last remote check, then verifies the observed published body against the
originally validated candidate text.

An independent named code challenger statically reviewed the frozen skill,
helper and tests and returned no actionable issue in the current delta. It did
not execute the reviewed code. It retained two pre-existing limits: a remote
edit can occur between the last fetch and the write, and the candidate file can
change between its final read and the command's publication read. A later
post-write mismatch can report failure after a write has occurred; it cannot
undo an overwritten concurrent edit. The implementation supplies **no atomic
compare-and-swap guarantee**. No live GitHub or GitHub Enterprise trial, fresh
agent publication workflow or general concurrency guarantee was established.

The original safeguards remain: publication requires explicit authorization in
the current turn and an exact full PR URL; composition alone grants none. The
candidate must be a separate existing file, non-empty unless that turn explicitly
requests clearing; publication is file-only, never stdin, inline body or command
substitution. The captured backup is retained until exact post-publication
verification succeeds. Failures and mismatches do not permit a success claim or
blind follow-up write. Restoration requires evidence that the just-completed
write caused the problem and that no concurrent update occurred; otherwise the
state is reported for direction. The helper itself performs no automatic retry
or restore.

Result is **PASS** for the reported 14 offline resource tests and no actionable
delta from the bounded static challenge; Evidence Coverage is **partial**.
Static source and resource execution support the capture-boundary correction.
They do not demonstrate that an agent always captures before drafting, that a
caller supplied a genuinely prior capture, or that a live provider prevents
races. General workflow improvement and comparative effect are **not assessed**.

## Work And Acceptance

The source defect is corrected and its offline controls passed. Broader
validation remains open, waiting for an explicitly authorized PR target and a
bounded question that needs live or fresh-agent evidence. This record assigns
no performer, authorizes no external write and sets no automatic live trial.
Establish the relevant current-turn publication authority, safe target, current
source identity, expected observations and task-specific resource limits before
selecting such work.

For a selected workflow trial, observe capture before candidate creation and
passing of the unchanged backup and marker. Retain successful publication and
zero-write controls for an edit during drafting, wrong capture, changed body or
marker, missing files, unauthorized publication and unauthorized clearing, plus
post-write mismatch handling. Only an explicitly authorized safe live write can
add live provider evidence; simulated remote behavior cannot be relabeled live.

Any claim that the remaining race windows are closed requires a separately
reviewed mechanism and tests for remote atomicity and candidate immutability.
The current correction does not promise either. A future trial may retain these
limits deliberately rather than change architecture; record its scoped outcome
and leave unsupported guarantees unclaimed. Revisit on helper/caller changes,
provider behavior changes, a contrary observation or a requested broader
guarantee. Do not rerun identical checks without a new evidence need.

## Outcome And Reuse

The supported lesson is that an overwrite guard must compare against the
capture used to draft the candidate. Re-fetching and backing up a newer body
after drafting cannot protect changes that happened during drafting. Requiring
the caller's original backup and marker closes that tested boundary while
preserving the existing publication, verification and recovery rules.

The canonical record is
`evidence/skills/pr-descriptor/publication-concurrency-validation.md`, listed once
in the common catalog. The primary approved public fitness after checking the
problem, controls and limits against source/tests and excluding private paths,
identities, traces and associations. Separate human case acceptance is not
requested. Source correction, record admission, external publication, installed
skill refresh and observed agent use remain separate facts. No external PR
description was written by these offline tests or this record.

## History

- Revision 1, 2026-11-02: recorded the actual after-drafting baseline defect,
  required pre-drafting capture, read-only exact backup, intentionally changed
  caller interface, 14 reported passing offline controls and bounded static
  challenge. Retained both pre-existing race windows and the absence of live
  or fresh-agent workflow evidence. Consolidation adds no new trial or
  publication authority.
