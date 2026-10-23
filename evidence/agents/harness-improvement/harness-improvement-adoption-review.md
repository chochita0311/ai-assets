---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-harness-improvement-adoption-review",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {
      "kind": "harness",
      "key": "agents/policies/harness/harness-improvement.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "615c015ff7e3c3f07c899d2631dc84832427c799ea19681c618be1e4a510a65c"
    },
    {
      "kind": "harness",
      "key": "agents/policies/harness/improvement-record-contract.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "db98376d8187126edd8b3908714ab64e27645095b445e82a67fc066d77e9411c"
    },
    {
      "kind": "harness",
      "key": "agents/operations/harness-improvement.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "3a5af75778f0472493087a41351ddf80a4fecef02c6d5df0f2e9c5e21a306d71"
    },
    {
      "kind": "harness",
      "key": "agents/templates/run.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "148dba7cb5193677b866e6bf1987cb9c86edf9525d442358acee50ae7cdb54bb"
    },
    {
      "kind": "harness",
      "key": "agents/templates/evaluation.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "0aa8e6a3ec04e69eef38dba3b08dcb368aee26d176287ca655540562bf327d15"
    },
    {
      "kind": "harness",
      "key": "agents/README.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "ba76cbc8eebb24e5cef94f219c41edbfb7676232803466bcc13ffc09007c61ac"
    },
    {
      "kind": "skill",
      "key": "skills/refine-skill/SKILL.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "6dd4d9cc3f69846e15d318663c56cf61ecbb3acd9b0406d21c2e57b9e3a6a98c"
    },
    {
      "kind": "skill",
      "key": "skills/refine-skill/references/method.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "ab294706aaf485db3d4b716fb2bfb0043e482f8ae997107ac035ad1a2eb79a13"
    },
    {
      "kind": "skill",
      "key": "skills/refine-skill/references/checklist.md",
      "source_revision": "933f565c26387bed939d1803c978d1106bd68e84",
      "content_sha256": "d2bd5e125b82d16e79122c1498cc7d70a8eb679c7d17199b6c8552ac4a708e09"
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
      "generalized-private-observation"
    ],
    "maturity": "static-validation",
    "execution": "run",
    "coverage": "partial"
  },
  "adoption": {
    "public_fitness": "approved",
    "case_status": "draft",
    "rule_status": "not-proposed"
  },
  "relations": {
    "related": [
      "ir-refine-skill-discovery-validation",
      "ir-refine-skill-comparable-reruns"
    ],
    "supersedes": []
  }
}
---

# Harness improvement adoption review

## Context And Applicability

**Result: PASS for the reviewed documentation, ownership, preservation and
publication checks. Evidence Coverage: partial for repeated operational use and
improvement effects.** One template-trigger conflict was corrected. The review
found no remaining blocker within its checked scope; it did not establish that
future agents reliably collect or reuse experience.

This is the public account of the final adoption review completed on
2026-10-23. The reviewed source and delivered correction are in
[commit 933f565](https://github.com/chochita0311/ai-assets/commit/933f565c26387bed939d1803c978d1106bd68e84).
The metadata fingerprints identify the delivered bytes of the primary policy,
operation, entry/template and standalone-skill subjects. The commit diff owns
the complete 36-path delivery; the subject list is not its complete file list.
The initial review candidate was uncommitted, based on the preceding commit;
its changed contents were not attributed to that preceding commit.

The improvement question is whether stage experience, comparison and public
feedback have coherent ownership and usable entry paths while preserving the
standalone skill contract. The primary owner is the Harness Improvement
procedure. Run/evaluation templates, its package overview and the refine-skill
boundary are related subjects. The observing reviewers are not component owners.

Use this account when reviewing a lifecycle-rule change across policy,
operation, entrance and output templates, or assessing this adoption baseline.
Recheck changed sources and applicability before reuse. It provides no task
assignment, runtime-installation authority or new normative rule. Other skills,
unrelated domain rules and future source versions are outside its conclusions.

## Evidence And Evaluation

### Review Scope And Provenance

Three bounded reviewers covered documentation structure, composition/meaning
preservation and disclosure. The primary agent reconciled their findings and
made the correction. Docs-structuring used `incremental`; docs-shaping used
`reshape` with a minimal local correction. A new hierarchy or broad rewrite
was not justified. These were source-reading reviews, not three independent
model task trials. Exact requested/observed model settings are not available
in this public account; reviewer roles do not establish different model bindings.

All 35 present candidate files (33 Markdown and two JSON), plus the deleted
follow-up source, were read completely. Whole-repository discovery, the
117-document link scan and transitive owner checks had their stated structural
or mechanical scopes; unrelated skill/domain/runtime bodies were not given a
full semantic audit. At entry, 83 source fingerprints matched the preceding
audited snapshot. Only the three correction passages below changed afterward.

Original reviewer outputs and check receipts remain with the originating
review's private evidence owner. This record preserves their generalized
observations, conditions and limits without private paths, identifiers,
associations or original traces. Public readers can inspect the committed
sources and rerun applicable checks; the private review sequence and reported
historical checks are not independently reproducible from this record alone.
This export did not rerun the historical checks or add an independent event.

### Confirmed Finding And Correction

The earlier bounded audit reported no additional defect. The later template
review found that the owning policy was correct while downstream wording was
still broader. This narrows the earlier conclusion rather than erasing it.
No erroneous runtime execution was observed.

| Surface | Reviewed candidate wording | Delivered wording |
|---|---|---|
| Run template | Experiment reference when an investigation exists | Only when the comparison's first authorized trial has actually started and the audience may access the reference |
| Evaluation template | An actual harness investigation calls for an experiment reference | A related comparison's first authorized trial must have actually started; keep the reference audience-safe |
| Package overview | Experiment record for an actual investigation | Private comparison record at a resolved owner, created only once the first authorized trial actually starts |

The [policy](../../../agents/policies/harness/harness-improvement.md#binding-and-continuity)
and [operation](../../../agents/operations/harness-improvement.md#procedure)
keep observation-only investigation and an unstarted proposal at the existing
task/stage owner. The delivered [run](../../../agents/templates/run.md#optional-harness-experience),
[evaluation](../../../agents/templates/evaluation.md#evidence) and
[overview](../../../agents/README.md#related-shared-docs) now agree with them.
These relative links locate current owners; use the pinned commit and metadata
for the reviewed historical bytes.

This was a low-severity, local predicate correction. No section moved and no
unique requirement was compressed. The rest of each affected file was unchanged
from the review-entry snapshot. The following source/output conditions were
checked by reading, not by executing a new workflow:

- Observation-only work and a prepared comparison without a started trial do
  not require an experiment record.
- A started but interrupted or incomplete comparison still qualifies; success
  or completed execution is not required.
- The private owner and audience-safe reference/omission conditions remain.
  Unused or unsafe public links may be omitted without preventing authorized
  private recording.
- Per-edit effects stay with their evidence owner. Evaluation Result/Coverage
  still assess the run's declared criteria; ordinary evaluation leaves change
  effect `not assessed`. None of these references authorizes a comparison.

The textual inconsistency is resolved. Per-edit behavioral improvement is
**not assessed**: there was no controlled task rerun, passing/failed comparison,
causal attribution or measured efficiency result for these three edits.

### Ownership And Meaning Preserved

| Reviewed relationship | Finding and limit |
|---|---|
| Entrance and overview | Entrances route; README explains use. Detailed ownership remains below the entrance layer. |
| Governance and execution | Policies own lifecycle/exchange rules, operations own sequence, schema/templates own shape and scaffolds, and adapters own runtime installation. Existing task owners retain execution and acceptance. |
| Evidence and adopted rules | Component records own generalized knowledge/work by improvement subject. One catalog discovers them without independent work/rule authority. UI/UX criteria remain with their existing policy owners. |
| Follow-up migration | All ten original task compounds and the complete historical comparison baseline were preserved, including conditions, controls, approvals/budgets, figures and limits. Ten tasks stayed open/unassessed; the eleventh record was an unrun synthetic reference. |
| Standalone skill | Refine-skill uses an existing authorized follow-up owner or the session. Selected/configured harness coordination owns common-schema mapping, storage and exchange. |
| Adoption and feedback | Optional selection, the complete eight-file core, private binding, ignored local outputs, selected public records, source/rendered provenance and reviewed feedback remain distinct. Installation, successful writes, observed use, comparison, rule adoption, publication and consumer refresh are separate events. |

The former unresolved-only follow-up list was replaced by component records
that retain resolved history. This intentional lifecycle change did not close
any pending task or turn its historical data into a verified improvement.

### Checks Reported For The Reviewed Snapshot

These counts describe the source delivered in commit `933f565`, before this
public review record was added. They are not counts of the latest collection.

| Check | Observed result and scope |
|---|---|
| Skill package validator | PASS: 11 packages; six optional external references retained explicit availability conditions |
| Generated shared instructions | Current under `render_global_agent_instructions.py --check` |
| Existing configured tests | PASS: 22 tests under `python3 -m unittest discover -s scripts -p 'test_*.py'` |
| Markdown targets | 117 files; 621 concrete local references resolved; 24 missing instantiation targets were intentional placeholders already in the prior source. External URLs were not fetched. |
| Record metadata/body/catalog | 11 records passed duplicate-key, current-schema-keyword, required-section/order, identity, relation and catalog checks. The stdlib checker was not full JSON Schema engine certification. |
| Diff and preservation | Diff hygiene passed after correction; complete local before/after units retained the linked conditions. |
| Disclosure | Full-text review found no actual sensitive/private material in the 35-file candidate. This is scoped disclosure review, not a guarantee for future edits or other content. |
| Commit and push | Exactly the reviewed 36 paths were committed; committed bytes matched the reviewed candidate. Normal push and subsequent remote read agreed on `933f565`; the source tree was clean at completion. |

The three final prose edits changed no link targets, schema, skill code or
marked generated-policy region; unrelated tests were not repeated solely for
them. Metadata parsing and successful tests do not establish semantic truth,
private-data fitness or runtime improvement on their own.

### Remaining Evidence Limits

This review's new evidence level is static validation. Earlier original-project
comparison and consumer installation observations retain their original
snapshots and limits. The earlier video review covered nine sampled frames,
without a full transcript or independently verified benchmark result. Those
results were not borrowed as this package's performance evidence.

The earlier consumer installation trial was not refreshed for these final
text corrections. Its observed old state therefore does not prove installation
of the delivered correction or an accepted committed-source refresh. General
ordinary-stage collection, cross-session recovery, relevant retrieval/reuse,
real public export/import feedback, and improvement benefit/recording cost
remain unverified. No pending maintenance task was executed by this review.

## Work And Acceptance

This is a reference-only review account, so its work basis, state and readiness
are `not-applicable`. The bounded source correction is already completed in the
pinned commit; this export creates no duplicate pending correction or active
performer/task. Case acceptance remains draft and is separate from disclosure
approval or the already observed source publication.

Existing [discovery validation](../../skills/refine-skill/refine-skill-discovery-validation.md)
and [comparable-rerun validation](../../skills/refine-skill/refine-skill-comparable-reruns.md)
retain their own requirements and open states. Their runtime/discovery/repeated
comparison conditions are not satisfied by this report. Later checks need their
original task authority, scope, inputs, controls and budget. No new schedule,
execution permission or closure criterion is introduced here.

Revisit this account if the lifecycle condition, templates, adoption mapping or
skill boundary changes, or an actual run supplies contrary evidence. Preserve
the old observation and update or supersede the relevant conclusion; do not
count this public projection or its imported copies as independent support.
A no-change decision remains valid when the current sources already agree.

## Outcome And Reuse

The supported lesson is narrow: in this adoption, a correct owning policy
coexisted with stale downstream experiment-reference triggers, and checking
those entry/template passages found the mismatch. Trace the relevant condition
to its consumers when the same review situation applies. This is evidence for
that bounded review observation, not general proof of self-improvement efficacy
or a newly adopted rule. Confidence is high in the inspectable text alignment;
operational reliability and causal effects remain unestablished.

The package's structure and standalone-skill boundary passed the declared
review, so no broader restructuring was applied. The complete result is retained
here under the Harness Improvement subject and discoverable through the
[common catalog](../../README.md). The public account is self-contained and has
no dependency on a temporary report path. Private originals remain at their
existing evidence owner under its retention rules.

Public fitness was reviewed by the primary coordinating author before this
record entered the source: useful conditions, counterevidence, observation
limits and approval distinctions are retained; private paths/IDs/hashes,
consumer identity, original traces and revealing associations are excluded.
The hashes in metadata identify public committed assets only. This disclosure
decision does not validate the unrun checks or grant human case acceptance.

The earlier source commit and push are observed events. Publication of this
record, future consumer refresh and observed runtime activation are separate;
this record supplies no new installation or activation evidence.

## History

- Revision 1, 2026-10-23: generalized the completed adoption/publication review
  into a component-owned, reference-only record. Retained the earlier
  no-new-defect assessment and the later contradictory template finding,
  correction, checks and unresolved operational limits. Matched the existing
  collection; no earlier record owned this review question. Added one catalog
  entry. Export adds accessibility and retention, not a new execution event,
  independent support, task completion or normative instruction.
