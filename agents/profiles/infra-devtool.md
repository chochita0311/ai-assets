# Infra Devtool Profile

## Purpose
- Guide infrastructure, tooling, scripts, CI, local workflow, and operational developer-surface work.
- Keep command behavior, environment assumptions, and failure modes explicit.

## Default Role Sequence
1. Orchestrator
2. Spec Agent
3. Builder
4. Contract Evaluator when command, config, artifact, or environment contracts change
5. Functional Evaluator
6. Fix Agent when implementation defects are confirmed

## Required Inputs
- approved feature and parent PRD
- current developer guide, CI policy, command list, scripts, or runtime configuration
- active spec with supported commands, inputs, outputs, and failure behavior

## Required Evidence
- command output or deterministic local check
- config, artifact, or environment-contract evidence when applicable
- failure-mode evidence when the feature changes error handling or operational behavior

## Default Evaluators
- `functional` for command behavior and regression checks
- `contract` when scripts, generated artifacts, config values, CI outputs, or environment assumptions change

## Split Triggers
- The work combines command behavior with unrelated policy or architecture changes.
- Environment assumptions are unclear or vary by consuming repo.
- Generated artifacts or config ownership needs a foundation feature before tool behavior can be changed safely.
