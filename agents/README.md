# Agent Package

## Purpose
- Keep reusable agent docs for iterative harness work in one shared source package.
- Separate role contracts from flow and operation docs so multiple workflow variants can compose from the same role set.
- Keep these docs general-purpose and portable across frontend, backend, and fullstack repos unless a file is explicitly marked domain-specific.

## Role Package
### Planning Roles
- `agents/role/prd-normalizer.md`: normalize chaotic product inputs into a bounded PRD package
- `agents/role/feature-planner.md`: decompose a normalized PRD into loop-sized product and foundation features

### Execution Roles
- `agents/role/orchestrator.md`: control one bounded execution loop and route failures to the right layer
- `agents/role/spec-agent.md`: translate one approved feature into an implementation-facing spec
- `agents/role/builder.md`: implement one approved spec without expanding scope
- `agents/role/design-evaluator.md`: evaluate visual and design-surface correctness against sources and spec
- `agents/role/functional-evaluator.md`: evaluate behavioral correctness, state handling, and regressions
- `agents/role/ux-heuristic-evaluator.md`: evaluate interaction clarity and friction without inventing new scope
- `agents/role/fix-agent.md`: apply targeted corrections from approved evaluator findings

## Flow Package
- `agents/flow/workflow.md`: define the baton flow, stop points, and role composition options

## Operation Package
- `agents/operation/runner.md`: define how a human or harness starts and continues one run using prompts
- `agents/ADOPTION-GUIDE.md`: explain how to export this shared package into a consuming repo and align it as local docs

## Related Shared Docs
- `agents/policies/harness/prd-feature-management.md`: planning-governance rule for PRDs, features, approval, and traceability
- `agents/policies/harness/execution-loop-governance.md`: execution-loop rules, fail classification, routing, and artifact ownership
- `agents/policies/review/design-evaluation.md`: reusable visual evaluation assets
- `agents/policies/review/interaction-evaluation.md`: reusable interaction-quality evaluation assets
- `agents/templates/prd.md`: reusable PRD template
- `agents/templates/feature.md`: reusable feature template
- `agents/templates/spec.md`: reusable spec template
- `agents/templates/run.md`: reusable run template
- `agents/templates/evaluation.md`: reusable evaluation template
- `agents/templates/fix-log.md`: reusable fix-log template
- `agents/templates/heuristic-backlog.md`: reusable heuristic backlog template

## Consumer Repo Placement
- This package is a shared source set, not a consumer repo by itself.
- In a consuming repo, place:
  - role docs under `docs/agents/role/`
  - flow docs under `docs/agents/flow/`
  - operation docs under `docs/agents/operation/`
  - PRD and execution templates under `docs/plans/`
  - governance and review assets under `docs/policies/`
- Keep the rules for those artifacts in the consuming repo's policy layer instead of repeating them in folder README files.

## Workflow Variation
- Treat `agents/flow/workflow.md` as a strong default example, not the only valid orchestration shape.
- A consuming repo may use smaller or larger workflows from the same role set depending on product scope, stack shape, and approval needs.
- When the workflow expands, keep the role contracts stable and add new flow docs through composition rather than rewriting every role.

## Invocation
- Initialize one execution pass from the approved feature document and the runner guide.
- Treat the runner guide as the ordered prompt source for the current execution pass instead of generating runtime scaffolding files automatically.

## Packaging Rule
- Treat `agents/` as the shared home for stable role, flow, and operation docs.
- Keep repo-specific operating rules in the consuming repo's `AGENTS.md` or `docs/policies/`; do not hide them inside reusable role definitions.
