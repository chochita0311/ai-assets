---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "hc-skill-trigger-example",
  "revision": 4,
  "audience": "public",
  "subjects": [{"kind": "skill", "key": "example/document-link-audit", "source_revision": null, "content_sha256": null}],
  "work": {"basis": "not-applicable", "state": "not-applicable", "readiness": "not-applicable"},
  "knowledge": {"state": "candidate"},
  "evidence": {"kinds": ["illustrative-synthetic"], "maturity": "none", "execution": "not-run", "coverage": "unavailable"},
  "adoption": {"public_fitness": "approved", "case_status": "draft", "rule_status": "not-proposed"},
  "relations": {"related": [], "supersedes": []}
}
---

# Skill Trigger Example

## Context And Applicability

Task/component: selecting a fictional document-link audit skill from its
discovery description. This is an illustrative synthetic reference, not run;
there is no observed discovery or task outcome.

An intended request may not be selected because its wording is absent from a
skill's discovery description. Consider this hypothesis only after checking
whether the failure occurred at discovery. It does not explain a correctly
loaded skill that failed during execution, or a tool failure after selection.

The existing skill's purpose and authorized actions remain the scope boundary.
Keep the baseline if the candidate broadens that boundary or no defect is
supported. This example is not a request to edit any installed skill.

### Problem, Intervention And Public Inputs

The fictional skill audits broken relative Markdown links in a repository.
Baseline description: “Find broken Markdown links when asked for a link audit.”
Candidate description: “Audit broken relative Markdown links in a repository,
including requests to check documentation links. Exclude prose rewriting.”

The hypothesis is that naming an ordinary intended request may improve
discovery while preserving scope. These descriptions and tasks were invented
for explanation. There is no original private incident behind this example.

| Synthetic request | Expected scope decision, not an observed result |
|---|---|
| “Use the link audit skill on these Markdown files.” | Select; explicit authorized audit |
| “Check whether the documentation links still resolve.” | Select; implicit intended request |
| “Rewrite this paragraph to sound friendlier.” | Do not select; prose rewriting is outside this skill |

Only the description changes in this hypothetical comparison. Before actual
execution, fix the skill revision, producer inputs, model/tools, inherited
instructions, task artifacts and checks. Necessary link fixtures belong in
producer inputs; the evaluation answer key does not. A fresh session still
needs a check for inherited candidate instructions.

## Evidence And Evaluation

- Public execution and original outputs: `not run`; no model or runtime selected
  either description here.
- Per-edit effect: `not assessed` because no comparison was executed.
- Positive controls: explicit and implicit requests above are proposed checks.
- Negative/no-change control: prose rewriting above is proposed, not passed.
- Authorized-success regression: a candidate that requires extra confirmation
  for an already authorized local audit would regress that success path.
- Counterexample: if the baseline already selects both intended requests,
  changing wording may have no observed effect. Keep that result in selection.
- A single better selection cannot establish stable discovery, task completion,
  efficiency or transfer to other skills. Reading this case is not a rerun.

The fictional asset has no real source revision or fingerprint. No requested
or observed runtime/model identity is inferred from this illustration. Static
illustration and publication review are not empirical evidence maturity.

## Work And Acceptance

No maintenance task is assigned by this reference. Before any authorized
comparison, use the conditions and explicit/implicit/negative controls above.
Human case acceptance remains pending; neither import nor reading supplies it.

## Outcome And Reuse

The illustrative hypothesis is to adjust the actual discovery owner only when
evidence supports a discovery defect, then compare explicit, implicit and
negative requests while retaining the baseline. Confidence in a behavioral
benefit is unestablished; no durable empirical lesson is claimed.

The owning skill package controls its description and domain method. The
[Harness Improvement policy](../../../agents/policies/harness/harness-improvement.md)
owns the comparison and public-case boundary. Revisit after actual evidence,
changed skill scope, model/tool changes or contrary outcomes.

Publication fitness review: author reviewed this as synthetic, self-contained
material with no private-source links or claims of observed improvement.
Human case acceptance remains pending. Disposition: hold as an illustrative
reference candidate. Normative change to the fictional skill: none. External
publication, consumer installation and runtime activation: not established.

## History

- Revision 1, 2026-10-21: normalized the legacy case-record contract v1 into
  Improvement Record v1. Retained public ID `hc-skill-trigger-example`, all
  example inputs, scope conditions, controls, counterexamples and limitations.
- Corrected the legacy effect label `confounded because there is no execution
  evidence` to `not assessed`: without an executed comparison no change effect
  was assessed. This corrects classification and claims no new experiment.
- Revision 2, 2026-10-21: this record is the sole source of the example;
  removed the redundant source pointer after updating discovery. No execution
  or new empirical support was added.
- Revision 3, 2026-10-23: moved to component-owned skill evidence with the
  same record ID, task conditions and assessment states. Updated discovery and
  applicable links; no execution, closure or new empirical support was added.
- Revision 4, 2026-10-23: moved into the repository-level evidence layer,
  retaining the same subject ownership, record ID, conditions and assessment
  states. This location change adds no execution, closure or empirical support.
