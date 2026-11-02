# Foundation Contract Profile

## Purpose
- Guide features that establish a reusable contract, invariant, ownership boundary, fallback rule, identity model, or generated-output shape.
- Keep foundation work separate from downstream product behavior.

## Default Role Sequence
1. Orchestrator
2. Spec Agent
3. Builder or contract updater
4. Contract Evaluator
5. Functional Evaluator only when runtime behavior also changes
6. Fix Agent when implementation defects are confirmed

## Required Inputs
- approved foundation feature and parent PRD
- current policy, architecture, schema, generated artifact, or implementation context
- active spec that states the contract outcome and downstream readiness condition

## Required Evidence
- contract completeness evidence
- source-of-truth ownership evidence
- generated-output or artifact evidence when applicable
- stale-assumption check across likely consumers

## Default Evaluators
- `contract` by default
- `functional` only when behavior changes beyond contract establishment

## Split Triggers
- The work includes both a new foundation contract and downstream product behavior.
- Contract ownership is still unclear.
- The proposed foundation change affects multiple consumers that need separate staged validation.
