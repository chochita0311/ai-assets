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

- If parity is claimed, is the immutable compare baseline recorded?
- Were affected old-to-new paths and logic units compared?
- Were query, write, output, side-effect, and failure semantics covered where relevant?
- Is parity `Unknown` or `Provisional` whenever required audit coverage is incomplete?
- Does a merge decision use [../templates/merge-check.md](../templates/merge-check.md) rather than an ad hoc report?
- Is the reviewed working tree limited to the intended merge scope?

## Artifact Roles

- Does the active plan own future work rather than execution history?
- Do logs own completed work, blockers, runtime evidence, and handoffs?
- Is the dedicated merge-check used only when parity or merge safety is the active decision?

## Final Question

- Could another reviewer judge the planned boundary and every safety claim without relying on conversation-only context?
