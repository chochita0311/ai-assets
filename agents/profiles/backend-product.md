# Backend Product Profile

## Purpose
- Guide service, API, command, job, persistence, messaging, and server-side behavior work.
- Keep contract and behavior checks explicit without naming the profile after any language or framework.

## Default Role Sequence
1. Orchestrator
2. Spec Agent
3. Builder
4. Contract Evaluator
5. Functional Evaluator when runtime behavior changes
6. Fix Agent when implementation defects are confirmed

## Required Inputs
- approved feature and parent PRD
- relevant architecture, API, schema, message, command, or persistence contracts
- active spec with in-scope behavior and out-of-scope adjacent behavior
- validation command expectations when the consuming repo defines them

## Required Evidence
- schema, payload, generated artifact, fixture, or contract evidence
- runtime behavior evidence when execution behavior changes
- regression evidence for named consumers, producers, jobs, commands, or integration paths

## Default Evaluators
- `contract` by default
- `functional` when behavior, command output, job execution, state transition, or runtime error handling changes

## Split Triggers
- A schema, payload, persistence, or generated-output contract is not stable enough for product behavior work.
- Producer and consumer changes can be staged independently.
- One feature starts to combine contract migration, runtime behavior, and unrelated cleanup.
