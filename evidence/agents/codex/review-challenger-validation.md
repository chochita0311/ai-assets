---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-codex-review-challenger-validation",
  "revision": 1,
  "audience": "public",
  "subjects": [{"kind": "runtime", "key": "agents/adapters/codex/custom-agents/review_challenger.toml", "source_revision": null, "content_sha256": "0107df39d140e2fe15256c88c4e6b028e8ee4da7d25c276d8fdf0bdfe5f52140"}],
  "work": {"basis": "evidence-gap", "state": "open", "readiness": "waiting"},
  "knowledge": {"state": "not-assessed"},
  "evidence": {"kinds": ["static-observation", "illustrative-synthetic"], "maturity": "resource-execution", "execution": "mixed", "coverage": "partial"},
  "adoption": {"public_fitness": "approved", "case_status": "not-requested", "rule_status": "not-proposed"},
  "relations": {"related": ["ir-pr-review-semantic-corpus"], "supersedes": []}
}
---

# Codex review-challenger runtime validation

## Context And Applicability

Validate the optional [Codex review challenger](../../../agents/adapters/codex/README.md#review_challenger)
before relying on its named binding, independence or omission benefit. This
runtime role supplements evidence scouts and exact-command verifiers with
semantic candidate discovery. It is an omission-only support role; the
[portable skill](../../../skills/gh-review-pr/SKILL.md#run-directly-or-as-a-delegated-reviewer)
can also be executed directly or by a full-task delegated reviewer without it.

The source selects an initial `gpt-6.1-sol` / `max` binding and four optional
feature reductions. Those choices are not proof of competence, cost or context
isolation. The [adapter](../../../agents/adapters/codex/README.md#review_challenger)
owns their reasons and tradeoffs; the [role file](../../../agents/adapters/codex/custom-agents/review_challenger.toml)
owns exact configuration. Semantic gates remain in the supplied task contract,
and no shared harness routing, repair-loop budget or escalation service was
added. Installation and model replacement retain their existing approval
boundaries.

## Evidence And Evaluation

The 2026-10-31 source-only audit parsed all four adapter TOMLs, verified required
fields and feature booleans, and passed seven offline audit/renderer tests.
The added [manifest fixture](../../../scripts/test_model_binding_audit.py)
checks that the existing discovery glob includes a distinct worker binding
without changing the audit profile's model. It invokes a synthetic Codex
executable, not the actual worker. This is the same seven-test resource check
counted in the semantic record, not another semantic trial or independent
evidence of runtime quality.

The first adapter audit returned PASS WITH SUGGESTIONS for explaining the
optional restrictions; the explanation was added without changing the binding
or flag values. The final independent refine audit returned PASS for static and
resource checks, Evidence Coverage partial, highest evidence resource execution.
It found no reason for further document restructuring. The [official custom-agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agent-file-schema)
supported the declared fields; account access, actual loading and
effective permissions were not observed.

The subject hash identifies the exact uncommitted TOML candidate; its Git
revision was not yet available at evaluation, so `source_revision` is null.
Original audit reports and tool results remain in the originating conversation.
Task-owned audit scratch was removed after verification. No runtime installation,
named invocation, cache activation or routing trial was performed. The two
generic delegated reviews in the [semantic record](../../skills/gh-review-pr/pr-review-semantic-corpus.md)
did not invoke this role and do not validate its binding or omission benefit.

## Work And Acceptance

### Eligibility And Authority

Work is waiting for an explicitly approved installation target and a fresh
runtime in which the exact name can be invoked. No active runtime test or
performer is assigned by this record. Resolve task-specific authority, raw
immutable artifacts, validation limits and a bounded test budget before selection.
Source publication does not authorize personal installation, live GitHub writes,
schedule activation or a model replacement.

### Required Checks

- Follow the adapter's [installation and recovery procedure](../../../agents/adapters/codex/README.md#installation-boundary), preserving unrelated destination content and capturing the prior state. Verify regular-file copies and exact source equality in every approved runtime home.
- In a fresh session, invoke the registered name and verify actual model/effort, instruction revision, no-history inputs, inherited permissions and all capability reductions. Check installed/cached activation, one justified auto-routing case and one case retained by the primary. A generic invocation, successful read or worker self-report is insufficient.
- Confirm its behavioral limits: raw-evidence candidate discovery, no authoring discussion or expected findings, no edits, reviewed-code execution, publication, acceptance decisions or further delegation; return bounded validation requests and material evidence gaps.
- Compare answer-isolated cross-file and terminal-consumer defect cases with legitimate-zero and duplicate controls. Measure omissions recovered, false positives, repeated concerns and actual cost; the primary still adjudicates every candidate under the owning contract.
- Compare a complete local evidence packet with an app/plugin-only evidence need. Confirm an authorized completion path or explicit gap; disabled memories do not remove passed conversation, and disabled permission requests do not create an independent sandbox.

### Completion

Close only after named-runtime and semantic controls have observed results and
any adverse outcome is resolved or explicitly withdrawn with a reason. Preserve
unavailable model, context, permission, capability-access or cost evidence as a
gap. Official lifecycle drift or an actual binding mismatch triggers reviewed
replacement evaluation; it never authorizes silent substitution.

## Outcome And Reuse

The optional source adapter and its explanatory documentation are complete;
runtime acceptance, semantic utility and cost remain open. Static compatibility
is not evidence of a working installed agent. Keep actual configuration and
installation instructions with the adapter and use this record for the evolving
verification question, avoiding another runtime checklist or session log.

## History

- Revision 1, 2026-10-31: retained the reviewed source configuration, bounded
  static/resource results and pending named-runtime/semantic acceptance.
  Public-fitness review found only portable source identities, synthetic
  observations and generalized checks; no private runtime paths, identifiers or
  transcripts were copied. Creation of this record is not a runtime execution,
  installation or approval to replace the model.
