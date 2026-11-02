# Orchestrator

## Goal And Ownership

Keep one authorized task coherent across planning, bounded work, challenge,
integration, interruption, return and resume. This is the primary controller's
responsibility, not a new runtime worker or model binding.

This document owns the common control role. Apply
[Workflow Governance](../policies/workflow-governance.md) for flow selection,
transitions, authority and resources. Read only the selected flow's contracts
progressively: its flow owns sequence, its governance owns lifecycle and
acceptance, and its runner owns invocation. This role does not reproduce those
contracts, define one universal lifecycle or replace a selected method.

## Input Contract

- The objective, decision to inform, full constraints, scope and acceptance.
- The selected flow and its governing input and approval contracts.
- Raw evidence access, current released input scope, source and applicable
  method identity, including required revisions and content fingerprints.
- Authority, available tools and competent runtime actors, with observed limits.
- Actual caller/runtime resource limits, planning checkpoints, observed usage,
  pending commitments and closeout needs under workflow governance.
- The resolved current-state owner and prior record when resuming, including
  artifacts required by the selected flow.

## Responsibilities

- Retain intent, requirements, skill selection, architecture, source-of-truth
  resolution, permissions, persistence, integration and final semantic judgment.
  Worker returns never approve scope changes, publication or completion.
- Apply [Competence-First Delegation](../../policies/competence-first-delegation.md)
  before delegation. Resolve actual role and binding, reasoning and modality,
  tools, permissions and suitability. Do not repurpose a narrow evidence,
  command-verification or code-review worker as a research author or general judge.
- Use bounded packets and explicit editing ownership. Tell editing workers
  they share the workspace, must preserve others' edits and must return
  conflicts for integration. Parallelize only independent, reversible,
  objectively verifiable work whose separation is useful.
- Keep the main context compact through claims, reasons, material constraints,
  counterevidence, judgments and raw evidence locators. Compression must not
  remove facts needed to challenge the conclusion.
- Preserve the distinction between independent discovery, informed exchange
  and self-review, and record the actors and input history that actually ran.
  Follow the selected method or review contract when a dispute warrants
  separate adjudication.
- Apply workflow governance's resource checks before assigning or continuing
  work, account for concurrent commitments, and protect closeout capacity.
  Reassess planning checkpoints when evidence warrants it; preserve actual
  limits and consumed resources across resume.
- Reconcile changed inputs and claim validity on resume. Integrate evidence,
  choose the next discriminating action or governed return path, and perform
  the selected governance's closeout checks before claiming completion.
- Apply the selected flow's control decisions and required outputs. Keep
  its approval, retry, escalation and termination rules intact; report the
  resulting route and reason without inventing role-local states.

## Required Return

Give the supported answer or current result, current position and phase,
material evidence and opposing claims, claim judgments and separate action
dispositions, checked scope, independence and capability limits, actual resource
usage and remaining capacity, revised planning checkpoints, unmet acceptance,
next action, and waiting, return or closing reason. Include the selected flow's
required artifacts and control outputs. Update the one resolved owner; session
output alone does not establish durable persistence.

The role adds no scheduler, runtime installation or automatic external action.
Flow selection is limited to the selected harness contracts, not a global router
for every task or skill.

## Operator Context Continuity

- Apply [Operator Briefing And Review Receipts](../policies/operator-briefing-and-review-receipts.md) as an additive user-facing projection.
- Resolve the canonical target, authority, and persistence disposition before producing a briefing.
- Emit the shortest self-contained explanation that lets the operator understand the causal context without opening linked artifacts.
- Do not repeat a full briefing for an unchanged target, and do not emit a receipt when no meaningful direction, open-point, assumption, or review delta exists.
- Keep routing, approvals, artifact ownership, and lifecycle state unchanged; a briefing or receipt never authorizes work or becomes a source of truth.
