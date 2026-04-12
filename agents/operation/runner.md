# Runner

## Purpose
- Define how a human or harness starts and continues one execution run using prompts.
- Keep execution startup and continuation consistent without requiring repo-local automation scripts.

## Ownership
- This document owns invocation.
- Use it when you need the operator-facing entry pattern for one approved feature run.
- It does not own the overall sequence model.
- It does not own the Orchestrator role contract itself.
- In a consuming repo, use `docs/agents/flow/workflow.md` for the sequence model.
- In a consuming repo, use `docs/agents/role/orchestrator.md` for loop-control responsibilities and routing logic.

## When To Use
- A feature document has already been approved.
- You want to begin or continue the execution loop from that approved boundary.
- You want reusable invocation prompts that work even when no local script or special runtime wrapper exists.

## Core Rule
- Start execution from the approved feature and parent PRD, not from the original request.
- Treat this document as the operator-facing execution entry guide.
- Do not generate ad hoc startup flows per run unless the project explicitly needs them.
- Treat one run as an automated unit.
- Do not assume the human owner will interrupt a normal active run.
- If the result should go back to spec or planning, report that at run completion so the human owner can make the next routing decision.

## Required Inputs
- one approved feature document
- its parent PRD
- relevant golden sources
- relevant project policies and contracts
- current implementation context

## Run Artifact
- Record one active run document under `docs/plans/run/`.
- Use one run identifier such as `run-YYYYMMDD-01` for each active execution pass.
- If the same run loops or is corrected materially, record attempts inside the run document rather than implying one uninterrupted straight-line pass.
- Put that run identifier into:
  - the run document
  - the spec document
  - evaluator reports
  - fix logs
  - heuristic backlog entries

## Default Invocation Order
1. Orchestrator
2. Spec Agent
3. Builder
4. Design Evaluator when the feature is visually sensitive
5. Functional Evaluator
6. UX Heuristic Evaluator when the feature is user-facing
7. Fix Agent
8. Re-run the needed evaluators

## Invocation Rules
- Fresh execution should start with `Orchestrator`, not directly with `Builder`, evaluators, or `Fix Agent`.
- Invoke one role at a time.
- Always include:
  - run ID
  - active feature path
  - active PRD path
  - active spec path once it exists
- Keep the role prompt anchored to approved docs.
- Do not restate the original request as the primary source once the feature is approved.
- If a role reports `spec gap` or `planning gap`, record it as a result for the run report unless a technical blocker prevents further continuation.
- After post-run human review sends work upward and that layer is corrected, start a new run from the corrected layer rather than continuing as if the earlier attempt remained valid.
- After the run exists, prefer continuing from the run document plus active spec and latest reports instead of re-invoking only from the feature path.
- Direct role invocation without `Orchestrator` is an exception path for tightly controlled continuation work, not the default operating pattern.

## Default Closing Sequence
- When all related runs for the active feature or PRD increment are complete, do not jump straight to acceptance.
- First summarize any reusable `design` or `interaction` evaluation candidates discovered during the run set.
- Ask the human owner whether each candidate should be added or discarded.
- After that decision, report that the related runs are complete and ask for:
  - PRD or feature acceptance when relevant
  - run acceptance
  - final close or follow-up direction

## Prompt Frame
Use this frame for every execution-role prompt in a consuming repo:

```text
Run ID:
- run-YYYYMMDD-##

Active feature:
- docs/plans/feature/feat-####-slug.md

Parent PRD:
- docs/plans/prd/prd-####-slug.md

Active spec:
- docs/plans/spec/spec-####-slug.md

Task:
- perform only this role
- do not redefine scope
- classify blockers as implementation bug, spec gap, or planning gap
```

## Role Prompts

### Orchestrator
```text
Run the execution loop for the approved feature below.

Run ID:
- run-YYYYMMDD-##

Active feature:
- docs/plans/feature/feat-####-slug.md

Parent PRD:
- docs/plans/prd/prd-####-slug.md

Task:
1. Confirm feature type.
2. Confirm the evaluator set.
3. Confirm the next role to run.
4. Classify any immediate blocker as implementation bug, spec gap, or planning gap.
5. Do not redefine scope.
```

### Spec Agent
```text
Read and execute as Spec Agent.

Run ID:
- run-YYYYMMDD-##

Inputs:
- docs/plans/feature/feat-####-slug.md
- docs/plans/prd/prd-####-slug.md
- relevant golden sources
- relevant implementation files
- relevant policy docs

Task:
Write the executable spec for this approved feature.
Do not expand scope.
Write to:
- docs/plans/spec/spec-####-slug.md
```

### Builder
```text
Read and execute as Builder.

Run ID:
- run-YYYYMMDD-##

Inputs:
- docs/plans/feature/feat-####-slug.md
- docs/plans/spec/spec-####-slug.md

Task:
Implement exactly the active spec.
Do not broaden scope.
Report changed files and blocker classification if needed.
```

### Design Evaluator
```text
Read and execute as Design Evaluator.

Run ID:
- run-YYYYMMDD-##

Inputs:
- docs/plans/feature/feat-####-slug.md
- docs/plans/spec/spec-####-slug.md
- relevant golden sources
- relevant design policies
- current implementation

Task:
Evaluate only the approved visual scope.
Write findings to:
- docs/plans/evaluation/eval-####-design-slug.md
```

### Functional Evaluator
```text
Read and execute as Functional Evaluator.

Run ID:
- run-YYYYMMDD-##

Inputs:
- docs/plans/feature/feat-####-slug.md
- docs/plans/spec/spec-####-slug.md
- relevant architecture and contract docs
- current implementation

Task:
Check behavior, state handling, and regression surfaces.
Write findings to:
- docs/plans/evaluation/eval-####-functional-slug.md
```

### UX Heuristic Evaluator
```text
Read and execute as UX Heuristic Evaluator.

Run ID:
- run-YYYYMMDD-##

Inputs:
- docs/plans/feature/feat-####-slug.md
- docs/plans/spec/spec-####-slug.md
- current implementation

Task:
Check clarity and friction within the approved scope.
Use browser automation or runtime inspection tools when available.
Record non-blocking suggestions separately from blocking failures.
Write to:
- docs/plans/evaluation/eval-####-ux-slug.md
- docs/plans/heuristic/heur-####-slug.md when suggestions should accumulate
```

### Fix Agent
```text
Read and execute as Fix Agent.

Run ID:
- run-YYYYMMDD-##

Inputs:
- docs/plans/feature/feat-####-slug.md
- docs/plans/spec/spec-####-slug.md
- relevant evaluator reports
- current implementation

Task:
Fix only reported defects.
Do not absorb new scope.
Write fix notes to:
- docs/plans/fix/fix-####-slug.md
```

## Invocation Examples
- Use short operator examples that point at the approved artifact directly.
- Prefer the feature document as the primary run target.
- Treat these examples as run-start or run-continuation triggers, not as replacements for the underlying role prompts.
- After the run starts, continue from the active feature, active spec, and latest execution artifacts.
- Common forms:
  - `run docs/plans/feature/feat-####-slug.md`
  - `continue docs/plans/feature/feat-####-slug.md`
  - `run docs/plans/feature/feat-####-slug.md as product loop`
  - `continue docs/plans/feature/feat-####-slug.md from fix`

### Fresh Run
```text
run docs/plans/feature/feat-0001-example-feature.md

Run ID:
- run-YYYYMMDD-01

Active feature:
- docs/plans/feature/feat-0001-example-feature.md

Parent PRD:
- docs/plans/prd/prd-0001-example-increment.md

Task:
- start the execution loop from the approved feature
- run only the Orchestrator role first
- confirm the evaluator set
- do not redefine scope
```

### Continue Existing Run
```text
continue docs/plans/feature/feat-0001-example-feature.md from fix

Run ID:
- run-YYYYMMDD-01

Active feature:
- docs/plans/feature/feat-0001-example-feature.md

Parent PRD:
- docs/plans/prd/prd-0001-example-increment.md

Active spec:
- docs/plans/spec/spec-0001-example-feature.md

Latest reports:
- docs/plans/evaluation/eval-0001-design-example-feature.md
- docs/plans/evaluation/eval-0001-functional-example-feature.md

Task:
- continue the same run as Fix Agent
- fix only reported defects
- keep the same approved feature boundary
```

### Continue From Run Record
```text
continue docs/plans/run/run-YYYYMMDD-01-example-feature.md

Run ID:
- run-YYYYMMDD-01

Task:
- resume from the active run record
- use the latest spec and latest evaluator or fix artifacts already linked there
- run Orchestrator first if the next role is not already explicit
```

## Environment Rule
- If optional skills or MCP tools are available and relevant, roles should use them.
- If they are not available, the roles must still remain operable through their base contract.

## Continuation Rule
- Continue the loop from the latest approved feature, active spec, and latest evaluator or fix artifacts.
- Do not restart from the raw request unless the work has been explicitly returned to planning.
