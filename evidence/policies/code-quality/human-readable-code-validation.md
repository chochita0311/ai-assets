---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-code-quality-human-readability",
  "revision": 1,
  "audience": "public",
  "subjects": [
    {
      "kind": "resource",
      "key": "policies/baseline/code-quality.md",
      "source_revision": null,
      "content_sha256": "12bc91345fd9a01b28cdc761dc8da7e74542537852e6f06b52a1bdcbacebcfd0"
    },
    {
      "kind": "resource",
      "key": "agents/instructions/standard.md",
      "source_revision": null,
      "content_sha256": "ed8791f5b1e4bab592dfa105faf4b6d0114d6394e4ce762c4a65d321ce1d1163"
    }
  ],
  "work": {
    "basis": "evidence-gap",
    "state": "open",
    "readiness": "waiting"
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
    "case_status": "not-requested",
    "rule_status": "implemented"
  },
  "relations": {
    "related": [],
    "supersedes": []
  }
}
---

# Human-readable code guidance and validation limits

## Context And Applicability

Can a language-neutral code-quality baseline reduce the effort required to
understand behavior, locate a change, and correct an agent's structural choices,
without favoring either unnecessary abstraction or excessive consolidation?
The current rule owner is [Code Quality](../../../policies/baseline/code-quality.md).
This record owns the evidence, adoption rationale, and remaining evaluation
question; it does not duplicate the runtime rules or assign a new project task.

The initiating concern was repeated manual correction of code whose classes,
helpers, packages, and execution machinery made responsibilities harder to
follow. The investigation considered four explanations: missing operational
criteria; inadequate application of existing rules or interpretation of the
requested outcome; necessary complexity mistaken for overengineering; and
incorrect instruction delivery. A causal relationship between a messy codebase
and increased overengineering remains a hypothesis, not a measured result.

The baseline already required project conformity, actual-version official
sources, reading/change-cost judgments, justified single-use boundaries,
meaningful validation and error handling, scoped edits, and honest checks.
The refinement makes human reading and responsibility ownership more explicit.
It applies proportionally when responsibilities, state, or dependency boundaries
change; it does not prescribe one folder tree, class count, function length,
language, retrieval service, or architecture diagram. Existing project contracts,
compatibility, lifecycle, concurrency, transaction, and performance requirements
remain constraints on simplification.

Ownership decisions are:

| Surface | Responsibility and decision |
|---|---|
| Code Quality policy | Own the self-contained common rules, including conditional ownership and structural-completion judgments. |
| [Generated instructions](../../../agents/instructions/standard.md) and [delivery guide](../../../agents/instructions/README.md) | Distribute the marked policy without maintaining another rule source. Generation does not install runtime copies. |
| [Codex adapter](../../../agents/adapters/codex/README.md#baseline-installation) | Retain the existing installation and equality-check procedure; no new hook, background evaluator, or worker binding was needed. |
| [Refactor Plan](../../../skills/refactor-plan/SKILL.md) and consuming projects | Keep phased refactoring and parity judgments in the existing skill; keep concrete public/internal boundaries and allowed dependencies in project guidance and checks. |

A possible separate design skill was discussed, not created. Reconsider it only
if a distinct detailed procedure repeatedly earns its cost beyond the baseline
and existing refactoring method. Description-based skill selection is not a
guaranteed interception mechanism, so required guidance must not depend on a
skill being selected. Reading official API documentation also does not validate
where a project's responsibilities belong. Language-specific examples from Go,
Python, and Spring informed the discussion without becoming universal rules;
Context7 remains an optional means of retrieving official material.

## Evidence And Evaluation

### Historical discovery and third-party evidence

The initial investigation screened approximately 1,900 local log files, selected
main-session material by relevant terms, and inspected representative surrounding
conversations, selected source/history, and official documentation. This was
sampled discovery, not a census of code tasks or a performance experiment.
The existing code-quality rules were present in the inputs of five selected
historical sessions. That weakens missing delivery as a complete explanation;
instruction presence does not establish compliance.

The following are generalized historical observations, not claims that the
current projects still contain the same defects:

| Situation | Observation and qualification |
|---|---|
| Custom scheduling and startup/stop scaffolding | A correction asked whether an existing framework facility could own the job. Delegation to a framework still requires preserving startup, shutdown, threading, and error semantics. |
| Verbose persistence and recovery logic | Feedback and the contemporaneous diagnosis separated mixed responsibilities from necessary connection identity, primary-key, atomicity, and indeterminate-result protections. Current implementation redundancy was not independently established. |
| Feature-oriented package refactoring | Early infrastructure/model work was explicitly proposed and authorized. Later feedback showed that finishing that increment did not fulfill the broader packaging expectation; it was not established to be unauthorized narrowing. |
| Names obscuring execution roles | Repeated generic names concealed distinct input, decision, and execution responsibilities. Hot-path behavior, shared constraints, and independent parallel work still had to be preserved. |
| Flush/check/write orchestration | Moving orchestration alone did not settle reuse and readability concerns. A deadline or shutdown flag can change during I/O, so an earlier check cannot automatically replace a later completion guard. |

The investigation used [Research SADR](../../../skills/research-sadr/SKILL.md).
Two initial research workers explored without the author's synthesis, followed
by separate evidence collection and informed challenge. Further fresh discovery
and candidate-blind probe design preceded the comparison below. These were
independent reasoning contexts over related material, not independent empirical
replications. Historical conversations and author diagnoses do not establish
all claimed defects in present source.

[Ponytail at the inspected revision](https://github.com/DietrichGebert/ponytail/tree/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846)
provided short instructions, injection/mode hooks, and regex-based code-name maps.
Those assist model judgment; they do not automatically prove call-graph coverage,
cohesion, or package boundaries. Reuse and small-diff advice must still permit
repairing misplaced legacy ownership and preserving justified one-use seams.

The author's [2026-10-07 benchmark report](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/benchmarks/results/2026-10-07-agentic.md)
reported 53% fewer source lines across 39 tasks in Claude Code with Opus 5.5,
default effort, and five runs per task and arm. Only 18 had executable hidden
checks; the other 21 used a model completeness judgment. Mutation detection
where tests existed was 77% for the baseline and 69% for Ponytail 5; across all
cells it was 46% and 66%, respectively, alongside increased test production.
These different denominators cannot establish that each generated test improved.
Candidate-pool selection in the inspected benchmark source used comparative
outcomes, limiting its use as untouched evaluation data. Raw benchmark runs
were unavailable and were not rerun; these figures remain author-reported.
They do not establish long-term readability or general cross-language benefit.

### Frozen synthetic decision comparison

Before observing answers, the task prompts and a 30-criterion rubric were fixed.
The rubric designer had not seen the candidate. Six tasks were designed first;
a seventh mutable-state control was added from source-based challenge before
any trial result. These are development probes, not an untouched real-code set.

| Probe | Contract or distinguishing control | Criteria |
|---|---|---:|
| Retry-message fallback | Change null only; preserve empty strings, spacing, and public calls without speculative infrastructure. | 4 |
| Browser/operations dependency separation | Remove the administration SDK from the browser's reachable graph while preserving one startup connection, per-call audit effects, errors, and the remaining phases. | 5 |
| Offline estimates with one production provider | Permit a present test/effect seam; retain one-argument callers, validation order, timeout/null mapping, and other errors. | 4 |
| Export versus shared normalization | Preserve case for export without changing login normalization or nullable-input behavior. | 4 |
| Event-plugin lifecycle | Reject eager subscription when registration/startup order matters; retain failed-startup and shutdown behavior. | 4 |
| Pinned retry configuration | Select supplied version-matched official evidence despite a Context7 coverage miss; preserve the version and total-attempt semantics. | 4 |
| Completion after an awaited write | Retain a live-state recheck, exact deadline boundary, allowed residual payload, on-time completion, and observable failures. | 5 |

Two fresh, no-history `research_worker` invocations, observed in local runtime
metadata as `gpt-6.1-sol` with `max` reasoning, each solved all seven tasks once.
One received the explicit baseline and the other a candidate refinement. Both
also inherited the existing baseline through runtime instructions and used the
research role and the same response scaffold. Supplied pseudocode contracts and
retrieval records were fictional closed-world inputs. No production code,
network fallback, or behavior tests were executed by these trial workers.

The rubric author evaluated condition-blinded answer artifacts, and the primary
read both outputs and adjudicated the results. Both conditions met all 30
criteria across all seven tasks; no advantage or regression was observed.
The primary also checked 85 cited excerpts against their answer locations.
This is a ceiling/null result for decision artifacts, not causal evidence,
policy equivalence, human-readability measurement, or reduced correction cost.
One worker per condition, shared inherited guidance, explicit task cues, and
common synthetic origins limit independence and transfer to real coding.

The exploratory draft was revised before the comparison: a prohibition on
per-step components became a prohibition on splitting solely by execution order;
ownership wording was clarified to permit invariants across justified boundaries;
and mutable-state revalidation remained conditional. The later adopted wording
further emphasized the human reader and meaningful names. That final revision
was not rerun in the synthetic comparison and inherits no measured superiority.

### Source and delivery checks

The starting repository revision was
`9e0523a1c71d89501493b71f6ba3602d6698b2f0`. The subject fingerprints identify the
refined repository policy and generated bundle. Their source revisions are null
because these exact versions were uncommitted when recorded; they are not
attributed to the starting commit. This is not an installed-runtime manifest.

Before the edit, the inspected effective global code-quality rules matched the
source, the observed aliases resolved to one owner, and no override was found
at the inspected locations. The refined policy was not installed during this
work. No claim is made about another machine, a future session, or actual rule
compliance.

The renderer freshness check and its seven existing tests passed after the
policy edit, as did whitespace/diff checks. The other generated policy regions
were unchanged. A frozen semantic review found no material regression in prior
duties or balanced boundary choices. A later full-document `docs-shaping` review
left both documents unchanged; the generated bundle also received a separate
whole-content review. Those are static wording/composition checks, not coding
outcome experiments.

At repository closeout, two new review contexts independently applied
`docs-structuring` and `docs-shaping` to the policy, bundle, evidence record,
catalog, session reports, and relevant ownership contracts. Neither identified
a concrete revision need. They shared historical evidence and made independent
judgments; they did not replay the reported executions. The renderer freshness
check and seven tests passed again. Record metadata, required sections, subject
fingerprints, unique record identity, catalog placement, and relative links were
checked separately; those checks do not establish empirical effectiveness.

Original private sessions remain the evidence owner. Task-owned probe packets,
answer files, rubric, and review snapshots were removed after their verification
ended. This generalized record preserves observations and limits, not the full
replay corpus. Public readers cannot independently reproduce the private trial
from this narrative; no new synthetic example inherits its results.

## Work And Acceptance

Policy implementation and its document review are complete. The improvement
question remains **open / waiting** for representative real-code evaluation;
there is no active follow-up run, selected task set, or automatic work assignment.

At a later authorized evaluation, compare untouched representative tasks from
the same starting code, requirements, versions, and model/settings. Preserve
behavior and required boundaries first, then assess structural completion,
human effort to locate the modification, correction content and count, change
impact, and total work cost. Include simple tasks that need no split, tasks that
require separation, and lifecycle/concurrency/error boundaries that must remain.
Use replication and explicit cost/acceptance criteria appropriate to the selected
tasks; a new run needs its own authority, evidence access, and resource allowance.
No such production comparison or allowance is established by this record.

Keep the effectiveness claim unresolved until those observations discriminate
between the baseline and refinement. Revisit or narrow rules if they increase
ceremony, fragmentation, hidden coupling, or lost contracts. Reconsider a
separate skill only when recurring detailed work and benefit justify its cost.
Runtime installation is a separate authorized merge through the existing adapter,
followed by content-equality and fresh-session checks; it is not completed here.

## Outcome And Reuse

The initial research and null pilot did not justify a new skill, adapter, or
immediate broad policy expansion. After those limits were reported, the user
explicitly requested policy supplementation centered on human-readable code.
That request authorized the repository refinement. The adoption basis is the
requested guidance and preserved contracts, not a claim that the pilot proved
better code. Normative source implementation and unproven effectiveness are
therefore recorded separately.

The implemented change strengthens reader-oriented simplicity, conditional
responsibility/ownership analysis, meaningful naming, mutable-state safeguards,
provider-neutral official-source retrieval, and structural completion alongside
behavioral verification. Existing project authority, scope, compatibility,
performance, valid single-use abstractions, and proportional verification remain.
No new skill, adapter behavior, renderer logic, executable tests, production code,
or runtime installation was introduced.

Public-fitness review by the primary retained the problem structure, contrary
results, conditions, adoption authority, and evidence limits while excluding
private paths, identities, raw traces, source associations, and operational
secrets. This is a reviewed generalized account, not independent public replay
or formal case acceptance. No private record store was configured; the exchange
receipt remains session-only rather than creating a separate ledger. Commit,
push, and consumer activation must be verified separately from this record.

## History

- 2026-11-04, revision 1: consolidated the investigation, candidate challenge,
  null synthetic comparison, later user-authorized policy refinement, static
  checks, and unchanged document-shaping review under the code-quality evidence
  owner. Two independent closeout documentation reviews found no necessary
  restructuring or meaning repair. Kept real-code effectiveness and runtime
  installation unresolved; no standalone session log or new skill/adapter was
  created.
