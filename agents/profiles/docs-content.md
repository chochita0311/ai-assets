# Docs Content Profile

## Purpose
- Guide documentation, content, policy, guide, and information-architecture work.
- Keep document ownership, source fidelity, and navigation checks explicit.

## Default Role Sequence
1. Orchestrator
2. Spec Agent when the approved feature requires an implementation-facing writing spec
3. Builder or document updater
4. Contract Evaluator when durable policy, ownership, or source-of-truth rules change
5. Functional Evaluator when links, generated docs, or rendered output must be checked
6. Fix Agent when confirmed defects remain

## Required Inputs
- approved feature and parent PRD
- current docs map, entrance docs, policy docs, and relevant source documents
- active spec or writing contract when needed

## Required Evidence
- source preservation evidence
- ownership and navigation evidence
- link or rendered-output evidence when docs are generated or published
- duplication and stale-reference check for nearby docs

## Default Evaluators
- `contract` when durable rules, ownership, or source-of-truth routing changes
- `functional` when generated docs, links, commands, or published output must be validated

## Split Triggers
- The work mixes durable policy changes with active planning artifacts.
- A docs-tree ownership change is larger than one approved feature.
- Content rewriting starts to change product or technical meaning instead of preserving source intent.
