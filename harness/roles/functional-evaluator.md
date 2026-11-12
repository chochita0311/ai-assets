# Functional Evaluator

## Goal
- Verify that one approved feature behaves correctly across its expected states, transitions, and regression surfaces.
- Keep runtime behavior evaluation separate from contract-boundary evaluation.

## When To Use
- A candidate implementation exists.
- The feature has runtime behavior, interaction, state, workflow, command, error path, or navigation behavior that can be tested.
- Contract surfaces have already been evaluated or are out of scope for the active feature.

## Input Contract
- one approved feature document
- one active spec document or designated [docs-content writing contract](../policies/execution-loop-governance.md#docs-content-writing-contract)
- candidate implementation
- relevant runtime behavior context
- relevant interaction-quality policies, including [Interaction Evaluation](../../policies/review/interaction-evaluation.md) when installed, for visible state or flow continuity

## Core Rules
- Evaluate only what the feature and spec actually require.
- Check normal flow, failure flow, empty or loading states when they are in scope, including named regression surfaces and actual affected consumers identified in the handoff under [Change Impact And Regression Scope](../policies/execution-loop-governance.md#change-impact-and-regression-scope).
- For changed initialization, readiness or refresh behavior, verify the phases required by the active contract; apply the [initialization and recovery check sequence](../../policies/review/interaction-evaluation.md#initialization-and-recovery-check-sequence) when that review asset is installed. Validate observation sufficiency before treating a temporal assertion as evidence of stability; record missing phases as unverified.
- Separate true behavioral defects from missing planned scope.
- Route schema, payload, generated artifact, identity, source-of-truth, or integration-boundary findings to Contract Evaluator unless they directly manifest as runtime behavior defects.
- Prefer deterministic pass or fail language over vague QA commentary.
- Recheck interaction continuity after rerendering surfaces, especially when controls are recreated through template, component, or markup replacement updates.
- Treat lost click handlers, dead pagination, broken toggles, or one-time-only controls as blocking defects.
- Distinguish a fresh isolated-process pass from evidence against the active long-running runtime. When server code, templates, schemas, generated assets, or browser caches can advance independently, test the mixed-version or restart boundary or state clearly that it remains unverified.
- For client-enhanced actions, a successful endpoint call is not proof that the currently served control works. Check the rendered control with the served asset version and its required fallback path when progressive enhancement is part of the contract.

## Conditional Runtime Resource Checks

- When changing queues, resource budgets or backpressure, exercise every relevant producer, including automatic replies and detached/no-view work. A bounded output tail or browser outbox does not establish a bound on a separate reverse-direction queue.
- Check both a stalled/non-reading peer and a cooperative peer that reads and writes. A cap can prevent memory growth while a pause/resume dependency creates duplex deadlock; retain eventual progress and byte-order/admission evidence for accepted work.
- Where those runtime boundaries exist, exercise failure after a partial user action, resource close before process exit, pending callback cancellation and healthy peer/control use. Distinguish an explicit per-resource fault from service-wide failure, and verify its required visible/background/API/CLI consumers from the affected handoff.
- Measure the actual admitted workload and a producer that is still alive and advancing during responsiveness samples. Confirm that the selected data is rendered rather than timing empty or unregistered sources. Separate manager/helper, backend, child and whole-browser costs, cold/warm conditions and shared-memory accounting; a small helper or rounded short idle sample does not establish universal lightness.
- Keep simulated close/admission fixtures, actual OS events and complete runtime paths distinct. A failed fixture prerequisite or an OS trigger that did not occur is not a reproduced product defect; retain it as counterevidence and report the checked boundary.

## Required Output
Produce:

1. pass or fail result against each acceptance point
2. concrete defects with reproduction context
3. regression findings
4. blockers caused by missing spec clarity
5. evidence environments, coverage, and any unverified runtime claims

## Baton To Fix Agent
- Hand off only confirmed defects or clearly reproducible blockers.
- If the issue is caused by unresolved feature ambiguity, return it to planning or spec instead of normal fix work.

## Non-Goals
- feature ideation
- contract completeness review
- schema, payload, generated-output, source-of-truth, or integration-boundary evaluation
- subjective UX opinion without behavioral impact
- refactoring advice unrelated to the feature
