# Research Governance

## Scope And Owners

This policy owns the lifecycle, research authority boundary, state and
acceptance contract for optional capability `research`. The
[Research Flow](../flows/research.md) owns sequence, the
[Orchestrator](../roles/orchestrator.md) owns primary control, and the
[Research Runner](../operations/research-runner.md) owns invocation.
[Workflow Governance](workflow-governance.md) owns flow selection, transitions,
shared authority and resource controls. The [research-sadr package](../../skills/research-sadr/SKILL.md)
solely owns the research method, including independent inquiry and evidence
validation. Consume its pinned complete local copy directly; harness adoption
does not install a global skill or verify runtime discovery.

Keep one research task coherent across bounded investigation, challenge,
integration, interruption and resume. The common primary retains the control
responsibilities; research adds no controller worker or runtime binding.
Apply shared workflow governance when the result reaches an authority or
transition boundary; its artifact rules also apply to individual hypotheses.

## Research Control Output

Give the supported answer, current question and phase, material evidence and
opposing claims, claim judgments and separate action dispositions, checked
scope, independence and capability limits, actual spent and remaining resources,
planning checkpoints and revisions, unmet acceptance, next action, and waiting
or closing reason. Update the one resolved owner; session output alone does not
establish durable persistence.

## Actors And Delegation

Apply [Competence-First Delegation](../../policies/competence-first-delegation.md) before
assigning work. Logical researcher, critic and adjudicator responsibilities
are not proof of available runtime actors. Automatic delegation requires a
suitable named binding under that policy. Explicit user-authorized delegation
may use a suitable available worker within the user's instructions; it does
not authorize silently replacing a specified worker or model. Do not expand
narrow code-review, evidence-gathering or command-verification roles into general
research authors or judges. This capability adds no runtime bindings.

Use the method's bounded packet and independent-input contract. Keep actual
actor, exposed binding/capability, tools, permissions, instruction revision and
fingerprint, input scope and fingerprints, inherited history, sharing stage,
inspected scope and return location. Mark unexposed fields unknown. Role names
and configuration alone establish neither fresh reasoning nor an operating-system
sandbox. Preserve independent returns before informed exchange.

If a suitable independent actor is unavailable, continue feasible work as
explicit self-review. Keep any acceptance requiring that missing independence
open; do not substitute a differently scoped worker or label self-review fresh.

## State And Persistence

Resolve one current-state owner. Reuse an existing authorized task, research,
planning or run record when appropriate; otherwise use session state and
bounded task-owned scratch. Do not duplicate facts across ledgers or create a
durable folder because this flow exists. An explicit durable handoff with no
resolved required destination needs target resolution before that write.
Session output does not establish persistence.

Keep a compact record with inspectable raw evidence access, preserving:

- Objective, decision, constraints, authority and acceptance conditions.
- Current question, inquiry phase, lifecycle state and current released input
  scope; historical releases and observations remain distinguishable.
- Source, method and applicable instruction revisions **and** content
  fingerprints, evidence locators, access/observation limits and validity after
  changes. Preserve fixed comparisons and unknown provenance as such.
- Hypotheses, support and counterevidence, assumptions, rejected directions and
  reopening conditions; independent discoveries and later informed judgments.
- Material opposing claims and `supported / refuted / unresolved` judgments
  with reasons, separately from revision, retention, intentional acceptance or
  deferral actions. Applying a change does not prove its underlying claim.
- Actual actor/capability/history records, including packet identities, allowed
  and unavailable evidence, tools and returned artifacts. Keep reasoning-context,
  method, source-lineage and validation-data independence distinct under the method.
- Actual resource limits and their sources/scopes, planning checkpoints and
  revisions, observed consumption, pending commitments, remaining capacity and
  closeout reserve; open gaps and their acceptance impact.
- Next discriminating action, waiting condition or closure outcome/reason,
  reopening condition and any subsequently authorized hard-limit addition or
  justified planning revision, preserving the earlier bounds and usage.

The [Research State scaffold](../templates/research-state.md) is optional and
non-persistent by default. It is not a required file or a second owner.

## Lifecycle And Resume

| State | Meaning and transition |
| --- | --- |
| `active` | Authorized research or closeout is in progress within current scope and actual resource limits. |
| `waiting` | A named external condition or caller input is needed; record its owner, effect, next action and resumption trigger. Background polling, elapsed time and successful completion are not waiting conditions. |
| `closed` | Work has ended with a separate outcome: `complete`, `partial`, `returned` for scope/authority, or `cancelled`, and an explicit reason. |

Close complete only when the requested judgment and its acceptance conditions
are met. A supported null finding can satisfy a bounded question. At closure,
missing required evidence or an actual hard limit that prevented completion
yields a partial outcome unless acceptance was already satisfied. Apply shared
resource governance before closure: a planning checkpoint prompts reassessment,
and a resource-specific cap does not stop unrelated feasible work. Agreement,
no new findings or elapsed time is not a quality pass. A rejected hypothesis can
lead to another inquiry or a valid conclusion; it is not by itself task failure.

Resume from the current owner, comparing prior inputs, claims, method and
instructions with current evidence. Update current scope and phase, retain
historical observations, and identify which judgments still hold and which
need rechecking. Keep spent resources and pending commitments; a new session or
worker does not reset them. Reopen a closed task only with a recorded reason and
applicable authority. Keep authorized changes to actual limits and justified
planning revisions separate from the original values under shared resource
governance; partial closure does not become completion through reopening.

## Budget Controls

Apply [shared resource governance](workflow-governance.md#resource-governance)
for actual hard limits, revisable planning checkpoints, dispatch, reserve,
parallel accounting, worker return boundaries, sufficiency and stopping. Keep
these resource facts with the existing research state; this policy introduces
no separate quota or allowance-end rule.

## Closeout And Handoff

Before closing, account for pending workers and artifacts within the allowed
scope: collect or stop work as authorized, and identify any unresolved activity
and its owner. Reconcile the receipt's current inputs, phase, inspected scope,
judgments, actions, gaps and usage with work that actually ran. Report results,
evidence coverage and acceptance limits separately; source checks, imported
bytes, active runtime behavior and observed usefulness are different evidence.

Keep the supported answer understandable without raw logs. Name the reason
for stopping, unmet acceptance, next discriminating observation and conditions
for reopening. Use [operator continuity](operator-briefing-and-review-receipts.md)
when a meaningful delta warrants a briefing or receipt; it adds no ledger.

Remove exact inactive task-owned scratch when its verification or recovery
purpose ends. Preserve active or uncertain-owned artifacts and identify their
owner, purpose and cleanup condition. Durable output must not depend on a
temporary path; resolve and complete any authorized durable handoff first.
