# Workflow Governance

## Ownership

This policy owns flow selection, transitions between flows, shared authority
boundaries and resource governance. The [Orchestrator](../roles/orchestrator.md)
is the common primary controller. A flow owns its own sequence, its runner owns
invocation, and its governance owns its lifecycle and acceptance rules. These
contracts do not create an additional runtime worker, scheduler, universal
state machine or shared persistent ledger.

## Flow Selection And Loading

Resolve the requested outcome, canonical target, current authority and selected
capabilities before selecting the flow. Use only the contracts needed for that
task; selection does not require loading every sibling flow or role.

| Selected work | Flow and governing boundary | Invocation |
| --- | --- | --- |
| Delivery planning or approved-feature execution, including product, docs-content, foundation and infrastructure work | [Delivery Flow](../flows/delivery.md), [PRD And Feature Management](prd-feature-management.md) and [Execution Loop Governance](execution-loop-governance.md); load planning or execution contracts when their stage is reached | [Delivery Runner](../operations/delivery-runner.md) starts or continues an approved-feature execution run |
| Open investigation with optional capability `research` selected | [Research Flow](../flows/research.md) and [Research Governance](research-governance.md), with the complete pinned local research-sadr method package | [Research Runner](../operations/research-runner.md) starts or resumes the research task |

A narrow factual lookup or small defined correction need not enter the research
flow. Selecting research requires its optional capability and local method
bundle; it does not require a separate controller actor or global skill install.
The research method remains owned solely by research-sadr.

After selection, read the selected flow and governing contracts, then its runner
when invoking or continuing work. Load further roles, profiles, method resources
and evidence progressively as the selected contract requires. In a consuming
repository, use the imported local contracts and the pinned complete method at
`docs/agents/methods/research-sadr/`; an installed same-name skill or external
checkout is not evidence of the pinned package's revision or content identity.

Harness Improvement is selected independently. Selecting research or delivery
does not itself enable experience storage, public-record import, comparisons or
new run identities. Its own capability, persistence and authority
rules govern any use.

## Transitions And Authority

The primary retains intent, requirements, architecture, source-of-truth
resolution, permissions, persistence, integration and final judgment. A worker
return, flow selection, budget revision or research conclusion grants no new
scope, implementation, external publication or operational authority.

When research selects a concrete implementation boundary, return its supported
result, constraints, evidence limits and unresolved decisions to delivery's
planning and approval sequence. Research recommendations do not approve that
boundary. Delivery retains human PRD review and approval, feature-boundary
review and approval, spec or designated writing-contract readiness, evaluation,
escalation and post-run human review. If an approved boundary already exists,
verify its continuing validity; do not infer a new approval from investigation.

Delivery's implementation-bug, spec-gap, planning-gap, technical-block and
[resource-block rules](execution-loop-governance.md#resource-block-exception)
remain owned by execution governance. A spec or planning return is a post-run
human decision followed by correction of the owning layer and a new run; it is
not a silent in-run redirect. Research does not relax those gates. Conversely,
individual hypotheses require no PRD, feature, spec, implementation-run artifact
or permanent research ledger.

For any transition, reconcile the current owner with actual inputs, preserve
prior observations and unresolved acceptance, identify the receiving boundary
and its required authority, and resolve only the dependent work if that authority
or a required durable destination is missing. The receiving flow keeps its own
lifecycle and artifacts; do not flatten distinct flows into a common state
machine or duplicate their state in a new ledger.

## Resource Governance

### Hard Limits And Planning Checkpoints

Before dispatch or continuation, distinguish:

- **Actual hard limits:** user-imposed or environment-enforced deadlines, cost,
  tool-use or attempt ceilings, and any other binding resource cap. Record each
  limit's source, units, scope, current bound, observability and enforcement.
  Do not invent a task deadline or silently turn a caller's hard cap advisory.
- **Planning checkpoints:** the agent's estimates, allocations and reassessment
  points for useful bounded work. Record their rationale and observable units.
  They guide dispatch and reassessment; reaching one is not automatically a
  whole-task stop, failed outcome or reason to ask the user to approve the
  agent's own estimate again.

If a required hard boundary cannot be observed or enforced, disclose that
specific limit and resolve the dependent dispatch or continuation before it
proceeds. Unknown usage or enforcement remains unknown, not zero or guaranteed.
A prose role supplies neither a scheduler nor a hard timeout.

The primary may revise its plan within the existing scope, authority and actual
caps. A critic may challenge an allocation's adequacy. Record the changed
estimate or allocation, new information or expected information gain, rationale,
actual usage, pending commitments and effect on closeout capacity. Preserve
earlier estimates and consumed resources; a session, input, worker or run change
does not reset them. A change to an actual hard limit needs the applicable
authority and a separately recorded addition or replacement, never an implicit
reset. Revising a plan grants no other approval.

### Dispatch, Reserve And Accounting

Reserve task-appropriate capacity for integration, verification, the final
receipt and cleanup. Before every assignment or continuation, account for
observed consumption and outstanding worker commitments, check the remaining
capacity against actual caps, and confirm that the proposed bounded work fits
while preserving that reserve. If only a planning allocation is reached,
reassess and, when justified within existing authority and real caps, revise it
before dispatch. If an actual cap leaves only closeout capacity for its affected
work, stop new assignments against that resource and preserve the reserve. Do not
use a universal reserve percentage, duration, worker count or round quota.

Account for parallel work using the cap's actual metric: elapsed wall time and
additive resource use are different. Include already spent and committed work
across actors. Give each worker a bounded assignment and an explicit stop/return
condition compatible with actual caps and the current plan. A worker reaching
its assignment boundary means it must return; it does not establish that the
whole task has enough evidence or must end. The primary integrates the return
before deciding whether a revised assignment or another direction is warranted.

If an actual hard-limit overrun occurs, preserve actual timing or usage and the
failed bound check separately from any valid findings. Account for pending workers and
artifacts before closeout: collect or stop work as authorized and identify
unresolved activity and its owner.

### Sufficiency And Stopping

Decide sufficiency from the requested judgment, required evidence, material
unresolved concerns, remaining useful information and the selected acceptance
contract. Agreement, finding counts, no new findings, elapsed time and cap
exhaustion do not by themselves establish success or failure. A supported null
finding can answer a bounded question. Reaching a planning checkpoint requires
reassessment, not automatic partial closure.

Further substantive inquiry or review needs new evidence, a discriminating
question or path, changed input or repair, or a concrete unresolved concern;
do not repeat unchanged work endlessly. If an actual hard limit prevents required
work, stop the affected resource or action and continue unrelated feasible work
within existing authority; a query quota does not prohibit analysis of evidence
already held. A whole-task deadline can require overall closeout. When the task
closes before acceptance is met, preserve usable results and report a scoped
partial result, unmet acceptance, stopping reason and next bounded check or
resumption condition. If acceptance was already met, the limit alone does not
turn the result partial. Map the stop to the selected flow's existing lifecycle.
When an actual cap prevents required delivery continuation, use its
[Resource Block Exception](execution-loop-governance.md#resource-block-exception)
for the `blocked` report and verified resumption, with task accounting carried
across the new run.
Resource outcome, evidence coverage and quality verdict remain separate; missing
required independence, strict parity evidence or other acceptance gates cannot
be waived by a revised allocation or a successful narrow check.
