# Research Runner

## Ownership And Use

This optional operation owns the entry and continuation prompts for a research
task. [Research Flow](../flows/research.md) owns sequence,
[Orchestrator](../roles/orchestrator.md) owns control, and
[Research Governance](../policies/research-governance.md) owns research lifecycle,
state and acceptance. Apply [Workflow Governance](../policies/workflow-governance.md)
for shared selection, transition, authority and resource controls. Invoke this
operation for a selected research task with its complete local method bundle.

## Start

1. Resolve the requested question and its decision, constraints, acceptance and
   allowed actions. Reuse an authorized task or research owner, otherwise keep
   state in the session or task-owned scratch. Resolve a required durable
   handoff destination before dependent persistence; do not invent one.
2. Load `docs/agents/methods/research-sadr/SKILL.md` directly in a consumer
   ([source method](../../skills/research-sadr/SKILL.md)). Check the pinned
   package and instruction revisions and fingerprints against the actual
   files. Missing or drifted method files require reconciliation; an installed
   same-name skill is not a verified substitute.
3. Give the primary the frame below. Before dispatch, it resolves actor
   suitability, actual resource caps and their scopes, planning checkpoints,
   closeout reserve and any hard-limit enforcement gap under shared governance. Use the
   [state scaffold](../templates/research-state.md) only when useful.
4. Follow the flow and return the actual scope, result, evidence limits and
   next action. No special script or automatic skill discovery is assumed.

```text
Start the selected research task using the local Research Flow and Orchestrator.
Question and decision to inform:
Constraints, allowed actions and acceptance:
Raw evidence and current released input scope:
Source, method and instruction revisions AND fingerprints:
Available actors/tools and known limits:
Actual hard limits: source, units, scope, observability and enforcement:
Planning checkpoints/allocations and rationale; required closeout reserve:
Observed usage, pending commitments and remaining capacity:
Current-state owner: existing authorized record, or session/task-owned scratch
Requested output and durable handoff destination, if already resolved:

Resolve capability and closeout capacity before dispatch. Reassess planning
checkpoints within existing authority and actual caps; record information gain
and rationale for revisions. Use the pinned local method directly; retain raw
evidence access and actual actor/history records.
```

## Resume

Read the current owner and reconcile its claims with the actual current inputs,
method and instructions. Preserve prior facts, initial independent returns,
later informed judgments, actions and consumed resources. Record changed releases
and invalidate only affected evidence; make the current input scope explicit.
For a waiting task, confirm whether its external condition has occurred. For a
closed task, record the reopening reason and applicable authority. Preserve the
original limits and usage: actual limit changes need their applicable authority;
planning revisions need recorded rationale under shared resource governance.

```text
Resume the existing research task from its current-state owner:
Changed raw inputs, claims, constraints or permissions:
Current released scope and its revisions/fingerprints:
Actual limits and previous usage, pending commitments and remaining capacity:
Current planning checkpoints and closeout reserve:
External condition resolved or reason to reopen:
Authorized changes to actual limits; justified planning revisions:

Reconcile earlier evidence and judgments before choosing the next action.
Preserve history and acceptance gaps. Check remaining capacity against actual
caps, commitments and closeout needs before continuing or assigning a worker.
A worker return or planning checkpoint calls for reassessment, not automatic closure.
```

## Return And Close

Apply governance's waiting and closeout rules. Report the accepted evidence
scope and task outcome separately from unverified acceptance, failed checks,
actual hard-limit overruns and runtime limits. A requested durable handoff must
identify its actual destination; otherwise say the state remains session-only.

If the next action exceeds this task's scope or authority, preserve usable results
and return the decision through [shared transition governance](../policies/workflow-governance.md#transitions-and-authority).
