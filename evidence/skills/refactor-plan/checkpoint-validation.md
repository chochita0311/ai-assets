---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-refactor-checkpoint-validation",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {"kind": "skill", "key": "skills/refactor-plan", "source_revision": null, "content_sha256": "521a75478922d1cf6a4a9a848fd10418e81914c4973663f46b0c0b722a80d712"}
  ],
  "work": {"basis": "evidence-gap", "state": "open", "readiness": "waiting"},
  "knowledge": {"state": "candidate"},
  "evidence": {"kinds": ["static-observation", "generalized-private-observation", "illustrative-synthetic"], "maturity": "comparable-rerun", "execution": "run", "coverage": "partial"},
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "implemented"},
  "relations": {"related": ["ir-clean-code-validation"], "supersedes": []}
}
---

# Refactor checkpoint and execution-log validation

## Context And Applicability

Can a refactor checkpoint tell a maintainer what to fix now, which checks can
run locally and which decision needs deployment evidence? Can a later execution
log accurately carry that decision forward? The [skill method](../../../skills/refactor-plan/references/method.md)
owns the review procedure. The [cleanup validation record](../clean-code/validation.md)
owns the related editing and scope-completion comparisons.

## Evidence And Evaluation

### Field evidence

A retrospective of three related service migrations screened 48 candidate
sessions from 1 October through noon on 28 November 2026 (UTC+9). One had
activity displayed within that period but its actual events ended earlier.
The three projects contributed 21, 19 and 7 eligible primary sessions. Three
readers inspected source records and Git evidence by project and a fourth
challenged the interpretation. They examined nine of the 47 sessions closely,
selecting for upgrade work and its immediate structural follow-up.
Eight showed delivery or reading of the refactor-planning instructions and
four of the cleanup instructions. The user explicitly named them in seven and
three of those sessions respectively. These counts overlap and exclude mere
mentions and duplicate child sessions. During implementation, the team
revisited seven originals with Git evidence. A separate check of six originals
confirmed actual resource reads for both skills in each of the three projects.
Those rereads draw from the same archive. The projects also drew on each
other's work, and the full skill revisions loaded historically are unknown.

One reader asked for a local code-contract judgment after receiving outstanding
target-environment checks. In a second case a local reproducer showed that a
driver lost its timeout on reconnect, yet an overall provisional judgment left
the reader asking if the code needed a fix. Elsewhere, enabling the ordinary
test run in CI exposed a shared setting that could route the job to a
live notification destination. A simulated send reproduced the titles and
bodies of seven observed notifications. The exact sending job was never
established. The repair checked the recipient and content at the test double,
restored shared settings and suppressed delivery in the child test process.
Existing strict comparison already found material differences. Both versions
attempted the same progress-recording call. After a database failure, only
the baseline performed the downstream write. Another candidate returned success where
connection release had previously made the query fail. These cases supported
retaining the strict audit and changing how its result is presented.
The archive also supplied positive examples. A file move preserved the ability
to read an existing message, while changing its serialized type name broke it
under the existing configuration. When setup details moved to their owning
document, the warning that local startup could modify stored data stayed next
to the command.
It supplied no corresponding reason to change the research or documentation skills.

### Comparative checks

The initial baseline was `67828fb`. Twelve fresh, read-only assessments used
five synthetic Python, JavaScript and Ruby tasks across the two skills and
successive revisions. A wording review with prior exposure to some scoring
criteria was excluded. Separate executions of the examples checked the
read-only judgments. The next comparison used six same-model pairs across
the skills with an explicitly designated editing role. They compared the prior
working version with its revision. The final comparison against `67828fb`
used one pair per skill and separate reviews of the archive and edited output.
The following results refer to those stages.

| Check | Observation and limit |
|---|---|
| Code repair and deployment evidence | The baseline already detected failed persistence/retry and a wrong notification route. The revision named required repairs in the opening and requested one expected event and zero attempts elsewhere through the ordinary, isolated CI command. In a Ruby control, results and errors matched for all four supported combinations. The reviewer found no further local repair and kept the signed installation check open. |
| Shipped defaults | Both versions caught a fixture that masked the shipped default and distinguished an omitted setting from an explicitly empty one. Only the revision initially scoped the repair to omission. The meaning of empty was unspecified at first. Once its preservation became explicit, both recommendations agreed. |
| Retries and destinations | Both generated checks passed legitimate retries and permitted reordering and caught a duplicate at the intended destination across nine conditions each. In the final rehearsal the candidate passed its default tests and delivered nothing, yet attempted the wrong route once. Both reviewers held the rehearsal. The revision put the default to fix, the local recheck and the installer's remaining confirmation in the opening. The baseline gave the action later. |

The method preserves integrations explicitly authorized at their agreed
destinations. In the isolated cases, both suppressing delivery as required and
blocking an attempt at the wrong route could leave an empty delivery log.
Where routing is part of the contract, the attempted destination distinguishes them.

Three additional rounds used separate editing and reviewing agents and checked
their decisions against execution. The first two shared an initial fixture and
varied the follow-up. Under the default settings the initial candidate
increased receipts from one to two for a single operation. A first repair
removed the duplicate but still wrote one when delivery was disabled, so the
reviewer maintained the hold.
A corrected candidate produced one logical receipt from three
attempts across a retry and a repeated request, and zero attempts and receipts
when disabled.
It passed the local check with signed installation confirmation still pending.
The third round used a separately designed Java 21 queue case. Both candidates
passed the default tests. A waiting consumer holding a previously obtained
view saw reservations and cancellations
in only one candidate. The reviewer accepted that candidate for the checked
scope. These rounds tested the revised behavior without an old-version control.

### Decision transfer between documents

The original event log could pair `Preserved` with test-only evidence and
omit a known regression. Folder reviewers applied the forms to a standalone
parser checkpoint with a confirmed output regression and an unaudited
external path. The decision held the candidate, named the repair, kept
overall parity provisional or unknown and explained why persistence had no
path in scope. The workflow also accommodated a commit-only review and an
intentionally uncommitted bundle, independently recording working-tree access
and out-of-scope changes in the candidate. A separate plan was unnecessary.
Existing batch and handoff records remained usable. Directory and filename
fallbacks worked independently with or without a track identifier.

The first folder walkthrough covered four supplied cases. Two informed rereads
and a final checklist recheck verified three event outcomes. A passing smoke
test could cite a still-valid hold for the same baseline, candidate and scope.
A configuration change or contradicting
observation required linking the old decision and withholding its verdict
pending reassessment. A new candidate without a matching decision retained
only its observed result. The [event form](../../../skills/refactor-plan/templates/log.md),
[checkpoint form](../../../skills/refactor-plan/templates/merge-check.md) and
[checklist](../../../skills/refactor-plan/references/checklist.md) agreed on
those cases. This was document use with supplied facts. No service was deployed.

### Repository checks

The initial investigation passed both package checks and rated the guidance
`PASS WITH SUGGESTIONS`.
After the first skill edits, all 16 packages passed repository validation,
as did nine validator tests, five maintained regression tests and ten self-test
controls. Both local registrations matched and all 35 package links resolved.
The 16-package check also passed after the six paired comparisons, the three
revised-only rounds and the final baseline pairs. The latter two stages each
compared all ten files in the preceding trial snapshot, source and local registrations. The three-round
check also reran the five regression tests.

Before the document repairs, the folder reviews read eight Markdown files
and two UI metadata files and resolved 35 local links, including 15 heading
targets. Six review findings led to changes in seven package documents.
Checks after those repairs resolved 41 package links, including 23 heading
targets, and retained the ten default plan sections, optional handoff and six
required step fields.

Two independent closeout readers compared both packages and their evidence
with the earlier results. The ownership review found that the combined
query/write row could not represent an audited query with no applicable write.
The checkpoint now records these separately, links the strict audit for
`Preserved` and routes artifact selection through one entry section. The
meaning-preservation review distinguished the unscored missing-input case
from the validator task and restored the scope of the corrected test oracle
and the checks run at each stage. The closeout reran the 16-package validator,
both platform frontmatter checks, the nine validator tests and the maintained regression
suite. Its ten positive, negative and termination controls produced their
expected outcomes. All ten installed files matched their final sources. The
43 local link occurrences in the packages included 25 links to headings.
Including the catalog and evidence records, all 96 local link occurrences
resolved, 35 of them to headings. These checks establish package and fixture consistency.
The disposable comparative trials remain historical observations.

## Work And Acceptance

The checkpoint, validation procedure and forms are implemented. The bounded
checkpoint comparisons and document checks passed. Evidence for their effect
is partial. The comparisons support a clearer opening in the
tested cases and a narrower initial repair in one underspecified case. They
do not establish a higher defect-detection rate. The remaining question needs
representative changes, different reviewers and measurement of repair accuracy,
follow-up questions and total effort. It is waiting for suitable cases and
authorization. No further run is assigned.

## Outcome And Reuse

Use the comparison results when the reader must decide whether to repair code,
repeat a local check or obtain target-environment evidence. The final subject
fingerprint identifies the reviewed package before commit, using the
[package manifest convention](../clean-code/validation.md#cleanup-decisions-in-migration-follow-ups).
Earlier results used the versions available at each stage. The source and
local registration matched. This public record preserves generalized archive
observations and local comparisons. The exact disposable trials and private
originals are outside the published material. Production outcomes, long-running
effectiveness and refresh in other consumers remain unverified.

## History

- 2026-11-28, revision 1 recorded the migration evidence, comparative and
  revised-only checks, documentation repairs and their limits.
