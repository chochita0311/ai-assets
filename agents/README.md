# Agent Package

## Purpose
- Keep reusable agent docs for iterative harness work in one shared source package.
- Separate role contracts from flow and operation docs so multiple workflow variants can compose from the same role set.
- Keep these docs general-purpose and portable across frontend, backend, and fullstack repos unless a file is explicitly marked domain-specific.

## Roles Package
### Planning Roles
- [agents/roles/prd-normalizer.md](roles/prd-normalizer.md): normalize chaotic product inputs into a bounded PRD package
- [agents/roles/feature-planner.md](roles/feature-planner.md): decompose a normalized PRD into loop-sized product and foundation features

### Execution Roles
- [agents/roles/orchestrator.md](roles/orchestrator.md): control one bounded execution loop, select the execution profile, and route failures to the right layer
- [agents/roles/spec-agent.md](roles/spec-agent.md): translate one approved feature into an implementation-facing spec
- [agents/roles/builder.md](roles/builder.md): implement one approved spec without expanding scope
- [agents/roles/contract-evaluator.md](roles/contract-evaluator.md): evaluate APIs, schemas, generated artifacts, source-of-truth ownership, and integration boundaries
- [agents/roles/design-evaluator.md](roles/design-evaluator.md): evaluate visual and design-surface correctness against sources and spec
- [agents/roles/functional-evaluator.md](roles/functional-evaluator.md): evaluate runtime behavior, state handling, workflows, and regressions
- [agents/roles/ux-heuristic-evaluator.md](roles/ux-heuristic-evaluator.md): evaluate interaction clarity and friction without inventing new scope
- [agents/roles/fix-agent.md](roles/fix-agent.md): apply targeted corrections from approved evaluator findings

## Flows Package
- [agents/flows/workflow.md](flows/workflow.md): define the baton flow, stop points, and role composition options

## Operations Package
- [agents/operations/runner.md](operations/runner.md): define how a human or harness starts and continues one run using prompts
- [agents/ADOPTION-GUIDE.md](ADOPTION-GUIDE.md): explain how to export this shared package into a consuming repo and align it as local docs

## Profiles Package
- [agents/profiles/README.md](profiles/README.md): explain reusable execution profiles
- [agents/profiles/frontend-product.md](profiles/frontend-product.md): user-facing screen, route, component, and interaction work
- [agents/profiles/backend-product.md](profiles/backend-product.md): service, API, job, command, persistence, and message behavior work
- [agents/profiles/fullstack-product.md](profiles/fullstack-product.md): coordinated multi-surface product work
- [agents/profiles/foundation-contract.md](profiles/foundation-contract.md): contract, invariant, ownership, identity, and generated-output foundation work
- [agents/profiles/infra-devtool.md](profiles/infra-devtool.md): infrastructure, tooling, scripts, CI, and local workflow work
- [agents/profiles/docs-content.md](profiles/docs-content.md): documentation, content, policy, guide, and information-architecture work

## Runtime Adapters Package
- [agents/adapters/codex/README.md](adapters/codex/README.md): install competence-first delegation, named worker bindings, and an optional operator-context recognition hook into a personal Codex runtime
- Keep portable delegation policy outside adapters; adapters own only platform-specific fragments, concrete model bindings, and installation guidance.

## Related Shared Docs
- [agents/policies/harness/competence-first-delegation.md](policies/harness/competence-first-delegation.md): platform-neutral admission, capability, fallback, context-transfer, and final-ownership rules for delegated work
- [agents/policies/harness/prd-feature-management.md](policies/harness/prd-feature-management.md): planning-governance rule for PRDs, features, approval, and traceability
- [agents/policies/harness/execution-loop-governance.md](policies/harness/execution-loop-governance.md): execution-loop rules, fail classification, routing, and artifact ownership
- [agents/policies/harness/execution-profiles.md](policies/harness/execution-profiles.md): profile selection, surface-lane, and evaluator routing rules
- [agents/policies/harness/traceability-and-link-hygiene.md](policies/harness/traceability-and-link-hygiene.md): portable path, link, and source-of-truth reference rules
- [agents/policies/harness/operator-briefing-and-review-receipts.md](policies/harness/operator-briefing-and-review-receipts.md): low-noise operator context, lifecycle triggers, repetition limits, and non-interference rules
- [agents/policies/review/design-evaluation.md](policies/review/design-evaluation.md): reusable visual evaluation assets
- [agents/policies/review/interaction-evaluation.md](policies/review/interaction-evaluation.md): reusable interaction-quality evaluation assets
- [agents/templates/prd.md](templates/prd.md): reusable PRD template
- [agents/templates/feature.md](templates/feature.md): reusable feature template
- [agents/templates/spec.md](templates/spec.md): reusable spec template
- [agents/templates/run.md](templates/run.md): reusable run template
- [agents/templates/evaluation.md](templates/evaluation.md): reusable evaluation template
- [agents/templates/fix-log.md](templates/fix-log.md): reusable fix-log template
- [agents/templates/heuristic-backlog.md](templates/heuristic-backlog.md): reusable heuristic backlog template
- [agents/templates/operator-briefing.md](templates/operator-briefing.md): non-persistent response scaffolds for operator briefings, alerts, and receipts

## Operator Context Continuity

Long-running imported harnesses can provide automatic, low-noise user context through [Operator Briefing And Review Receipts](policies/harness/operator-briefing-and-review-receipts.md). The policy adds explanatory Work Briefings and Review Receipts at relevant target and lifecycle boundaries without adding a source of truth, workflow stage, status, or approval gate.

Use [Operator Briefing Template](templates/operator-briefing.md) as a non-persistent output scaffold. Repository-local adoption owns the detailed policy and template; the Codex adapter carries only a small recognition hook and remains silent when the current repo does not expose the policy.

## Consumer Repo Placement
- This package is a shared source set, not a consumer repo by itself.
- In a consuming repo, place:
  - role docs under `docs/agents/roles/`
  - flow docs under `docs/agents/flows/`
  - operation docs under `docs/agents/operations/`
  - profile docs under `docs/agents/profiles/`
  - non-persistent agent response scaffolds under `docs/agents/templates/`
  - PRD and execution templates under `docs/plans/`
  - governance and review assets under `docs/policies/`
- Keep the rules for those artifacts in the consuming repo's policy layer instead of repeating them in folder README files.

## Workflow Variation
- Treat `agents/flows/workflow.md` as a strong default example, not the only valid orchestration shape.
- A consuming repo may use smaller or larger workflows from the same role set depending on product scope, stack shape, and approval needs.
- When the workflow expands, keep the role contracts stable and add profiles, lanes, or flow docs through composition rather than rewriting every role.

## Invocation
- Initialize one execution pass from the approved feature document and the runner guide.
- Treat the runner guide as the ordered prompt source for the current execution pass instead of generating runtime scaffolding files automatically.

## Packaging Rule
- Treat `agents/` as the shared home for stable roles, flows, operations, profiles, policies, and templates.
- Keep repo-specific operating rules in the consuming repo's `AGENTS.md` or `docs/policies/`; do not hide them inside reusable role definitions.
