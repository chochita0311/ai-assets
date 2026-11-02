# Refactor Plan Checklist

Use this as the final yes-or-no validation after applying [method.md](method.md).

## Scope And Structure

- Is the work classified as structural, behavioral, or semantic?
- Is behavior-preserving work separated from intentional change?
- Are the baseline, scope, non-goals, and invariants explicit?
- Does every phase have one purpose, bounded targets, validation, and an exit gate?
- Does the plan preserve existing repository conventions and historical rationale?

## Contract And Risk

- Are interface, schema, persistence, side-effect, transaction, concurrency, and generated-artifact risks addressed where relevant?
- Are intentional deltas named rather than hidden inside cleanup language?
- Are wiring, startup, runtime, and regression checks included when required?
- Are unresolved facts marked provisional?

## Parity And Merge Claims

- If parity is claimed, are baseline and candidate frozen separately, both sides' state/guidance identities recorded, and the requested moving reference rechecked at close?
- Were affected old-to-new paths and logic units compared?
- Were query, write, output, side-effect, and failure semantics covered where relevant?
- Do path witnesses include relevant terminal consumers, lifecycle/recovery paths, actual types, predicates, and dependency branches?
- Was independent review need assessed proportionally, with actual discovery/dispute exposure and any required independence gap recorded?
- Were candidates adjudicated with counterevidence and valid fixtures, keeping claim status separate from action?
- After repairs or changed inputs, were affected witnesses renewed using both whole-scope and repair-delta comparisons?
- Were actual hard limits, their sources, and their action/resource/task scopes distinguished from revisable planning allowances, with justified revisions and integration, verification, and cleanup capacity recorded?
- Were cumulative usage, spent attempts, unresolved objections, commitments, remaining capacity, and stop/resume conditions preserved across changed inputs and sessions without treating a planning checkpoint as a forced task stop or exhaustion as acceptance?
- Did each further pass have material information or decision value, with worker return boundaries kept separate from overall acceptance and any real hard-stop partial result?
- Is parity `Unknown` or `Provisional` whenever required audit coverage is incomplete?
- Does a merge decision use [../templates/merge-check.md](../templates/merge-check.md) rather than an ad hoc report?
- Is the reviewed working tree limited to the intended merge scope?

## Artifact Roles

- Does the active plan own future work rather than execution history?
- Do logs own completed work, blockers, runtime evidence, and handoffs?
- Is the dedicated merge-check used only when parity or merge safety is the active decision?

## Final Question

- Could another reviewer judge the planned boundary and every safety claim without relying on conversation-only context?
