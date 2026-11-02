# Harness Package

## Purpose
- Keep reusable runtime-neutral docs for iterative harness work in one shared source package.
- Separate role contracts from flow and operation docs so multiple workflow variants can compose from the same role set.
- Keep these docs general-purpose and portable across frontend, backend, and fullstack repos unless a file is explicitly marked domain-specific.

## Roles Package

### Shared Primary Role
- [harness/roles/orchestrator.md](roles/orchestrator.md): coordinate the selected workflow; control one bounded delivery execution loop, select its execution profile, and route failures to the right layer; keep a research task coherent across bounded investigation, integration, interruption, and resume

### Planning Roles
- [harness/roles/prd-normalizer.md](roles/prd-normalizer.md): normalize chaotic product inputs into a bounded PRD package
- [harness/roles/feature-planner.md](roles/feature-planner.md): decompose a normalized PRD into loop-sized product and foundation features

### Execution Roles
- [harness/roles/spec-agent.md](roles/spec-agent.md): translate one approved feature into an implementation-facing spec
- [harness/roles/builder.md](roles/builder.md): implement one approved active execution contract without expanding scope
- [harness/roles/contract-evaluator.md](roles/contract-evaluator.md): evaluate APIs, schemas, generated artifacts, source-of-truth ownership, and integration boundaries
- [harness/roles/design-evaluator.md](roles/design-evaluator.md): evaluate visual and design-surface correctness against sources and spec
- [harness/roles/functional-evaluator.md](roles/functional-evaluator.md): evaluate runtime behavior, state handling, workflows, and regressions
- [harness/roles/ux-heuristic-evaluator.md](roles/ux-heuristic-evaluator.md): evaluate interaction clarity and friction without inventing new scope
- [harness/roles/fix-agent.md](roles/fix-agent.md): apply targeted corrections from approved evaluator findings

## Flows Package
- [harness/flows/delivery.md](flows/delivery.md): define the baton flow, stop points, and role composition options
- [harness/flows/research.md](flows/research.md): sequence optional research and its internal return points; [Workflow Governance](policies/workflow-governance.md) owns transitions to existing planning and approval boundaries

## Operations Package
- [harness/operations/delivery-runner.md](operations/delivery-runner.md): define how a human or harness starts and continues one run using prompts
- [harness/operations/research-runner.md](operations/research-runner.md): start and resume an optional research task from its resolved state owner
- [harness/operations/harness-improvement.md](operations/harness-improvement.md): configured stage experience, bounded comparisons and consumer-to-common export
- [harness/ADOPTION-GUIDE.md](ADOPTION-GUIDE.md): explain how to export this shared package into a consuming repo and align it as local docs
- [harness/harness-import-manifest.example.json](harness-import-manifest.example.json): schema-shaped example for initializing a consuming repo's own harness refresh baseline

## Profiles Package
- [harness/profiles/README.md](profiles/README.md): explain reusable execution profiles
- [harness/profiles/frontend-product.md](profiles/frontend-product.md): user-facing screen, route, component, and interaction work
- [harness/profiles/backend-product.md](profiles/backend-product.md): service, API, job, command, persistence, and message behavior work
- [harness/profiles/fullstack-product.md](profiles/fullstack-product.md): coordinated multi-surface product work
- [harness/profiles/foundation-contract.md](profiles/foundation-contract.md): contract, invariant, ownership, identity, and generated-output foundation work
- [harness/profiles/infra-devtool.md](profiles/infra-devtool.md): infrastructure, tooling, scripts, CI, and local workflow work
- [harness/profiles/docs-content.md](profiles/docs-content.md): documentation, content, policy, guide, and information-architecture work

## Related Shared Docs
- [harness/policies/workflow-governance.md](policies/workflow-governance.md): common workflow selection, transitions, authority, resource accounting, and handoff
- [policies/README.md](../policies/README.md): shared baselines, delegation, and evaluation policy owners
- [agents/README.md](../agents/README.md): independently reusable shared instructions, prompt presets, and runtime adapters
- [harness/policies/prd-feature-management.md](policies/prd-feature-management.md): planning-governance rule for PRDs, features, approval, and traceability
- [harness/policies/execution-loop-governance.md](policies/execution-loop-governance.md): execution-loop rules, fail classification, routing, and artifact ownership
- [harness/policies/research-governance.md](policies/research-governance.md): optional research lifecycle, research authority, evidence state, acceptance and closeout; [Workflow Governance](policies/workflow-governance.md) owns selection, transitions and resource controls
- [harness/policies/harness-improvement.md](policies/harness-improvement.md): optional cross-component application evidence, effects, private records and common promotion
- [harness/policies/improvement-record-contract.md](policies/improvement-record-contract.md): common improvement identity, states, import/export admission and revision feedback
- [harness/schemas/improvement-record.schema.json](schemas/improvement-record.schema.json): versioned metadata shape for improvement records
- [harness/policies/execution-profiles.md](policies/execution-profiles.md): profile selection, surface-lane, and evaluator routing rules
- [harness/policies/traceability-and-link-hygiene.md](policies/traceability-and-link-hygiene.md): portable path, link, and source-of-truth reference rules
- [harness/policies/operator-briefing-and-review-receipts.md](policies/operator-briefing-and-review-receipts.md): low-noise operator context, lifecycle triggers, repetition limits, and non-interference rules
- [policies/review/design-evaluation.md](../policies/review/design-evaluation.md): reusable visual evaluation assets
- [policies/review/interaction-evaluation.md](../policies/review/interaction-evaluation.md): reusable interaction-quality evaluation assets
- [harness/templates/prd.md](templates/prd.md): reusable PRD template
- [harness/templates/feature.md](templates/feature.md): reusable feature template
- [harness/templates/spec.md](templates/spec.md): reusable spec template
- [harness/templates/run.md](templates/run.md): reusable run template
- [harness/templates/evaluation.md](templates/evaluation.md): reusable evaluation template
- [harness/templates/fix-log.md](templates/fix-log.md): reusable fix-log template
- [harness/templates/heuristic-backlog.md](templates/heuristic-backlog.md): reusable heuristic backlog template
- [harness/templates/operator-briefing.md](templates/operator-briefing.md): non-persistent response scaffolds for operator briefings, alerts, and receipts
- [harness/templates/research-state.md](templates/research-state.md): optional non-persistent scaffold for one research task's current state
- [harness/templates/harness-local-store.md](templates/harness-local-store.md): private binding, evidence owners, improvement index and exchange receipts
- [harness/templates/harness-stage-record.md](templates/harness-stage-record.md): lightweight stage/attempt application evidence and closing reflection
- [harness/templates/harness-experiment.md](templates/harness-experiment.md): private comparison record at a resolved private owner, created only once the first authorized trial actually starts
- [harness/templates/harness-improvement-record.md](templates/harness-improvement-record.md): common record body and metadata for reusable pending work and experience
- [evidence/README.md](../evidence/README.md): repository-wide improvement record catalog, covering all current asset-owner domains under one contract without adding rule authority

## Optional Research

Select capability `research` through the adoption guide for resumable open
investigation. Its flow, shared primary role, runner, governance and state scaffold
own orchestration; [research-sadr](../skills/research-sadr/SKILL.md) remains the
sole research-method owner. Adoption copies the complete pinned method package
to `docs/agents/methods/research-sadr/` and loads its `SKILL.md` directly. This
does not install a personal skill, prove runtime discovery or add model bindings.

Reuse one authorized task/research owner, or keep state in the session and
task-owned scratch. Preserve evidence, opposing claims, input and instruction
identity, actual actors and history, spent allowance and acceptance gaps across
resume. Research hypotheses need no feature, spec or run artifacts. A selected
implementation boundary returns to existing planning and approval gates.
Research and Harness Improvement are independent capabilities; neither selects
the other, and research alone configures no experience store.

## Optional Harness Improvement

Select `harness-improvement` through the adoption guide when a consumer wants
repeatable experience for incremental harness changes. Configure the consumer's
local `docs/evidence/` store and its discovery binding once during adoption,
or reuse an existing configured owner. Keep its generated local records ignored
and outside the managed import set, beside `docs/agents/` and `docs/plans/`.
The agent then
retrieves relevant experience on each actual stage's entry and records observed
component use and outcomes, reconciling reusable knowledge/work in common records
on exit, including planning-only work. No separate improvement prompt is needed. Missing persistence remains
session-only; template installation alone is not active collection.

Stage records distinguish logical roles from runtime actors and task PRDs,
features and specs from the harness contracts used on them. A real comparison,
when warranted and authorized, adds baseline/candidate results, per-edit effects
and counterexamples. Ordinary completion does not require an experiment.

Keep original evidence with the consumer's private owner. Public improvement
records are generalized, self-contained accounts with explicit evidence limits. Adopted
rules continue to belong to their policy, skill or review-asset owner. Source
changes, publication, consumer refresh and runtime activation are distinct.
Consumers without the capability need no new run fields or migration.

[Improvement Record v1](policies/improvement-record-contract.md) is the
common format for experience and reusable pending work across harness, skills,
resources and UI/UX. Its work, knowledge, evidence and adoption states are
independent. Canonical public records live under their current responsible owner
at `evidence/<domain>/<component>/`, with `harness`,
`agents`, `policies` and `skills` defined by
[Public Record Placement](policies/improvement-record-contract.md#public-record-placement).
The same record owns its knowledge and improvement work; select by subject/cue/state from the
common catalog. Each record appears once, with IDs unique across all four domains.
There are no separate lesson formats, skill work lists or case aliases.
Existing task artifacts still own actual execution and acceptance. Import selected records as references by default,
or explicitly as work candidates; neither assigns work nor adopts a rule.

For common reuse, the operation resolves the actual shared source and exports a
reviewed record to its component-owned evidence location, or an authorized
rule change to its existing policy/skill/review owner. Public identity and
revision connect local applicability decisions, actual work, results and
counterevidence to a later reviewed record update. Other consumers receive
selected records or updated rules through their own controlled refresh and
reassess applicability there. Preserve record history and private/public
separation throughout. Private project and
machine histories are not automatically synchronized. The hooks are instructions
performed by the agent, not a background service or permission to publish.

In that commonization context, `ai-assets로 export해줘` reviews the current
project's available harness, skill/resource/tool and UI/UX experience for
qualified common content. The user need not repeat the privacy/generalization
prompt. [Short export requests](operations/harness-improvement.md#recognize-an-export-request)
also support case-only, review-only and narrower categories. Keep private and
sensitive originals outside the public source; no eligible candidate means no
source change. Export does not itself commit, publish or refresh other projects.

## Operator Context Continuity

Long-running imported harnesses can provide automatic, low-noise user context through [Operator Briefing And Review Receipts](policies/operator-briefing-and-review-receipts.md). The policy adds explanatory Work Briefings and Review Receipts at relevant target and lifecycle boundaries without adding a source of truth, workflow stage, status, or approval gate.

Use [Operator Briefing Template](templates/operator-briefing.md) as a non-persistent output scaffold. Repository-local adoption owns the detailed policy and template; the shared instruction bundle carries only a small recognition hook, installed through a runtime adapter, which remains silent when the current repo does not expose the policy.

## Consumer Repo Placement
- This package is a shared source set, not a consumer repo by itself.
- In a consuming repo, place:
  - role docs under `docs/agents/roles/`
  - the repo-owned harness import manifest at `docs/agents/harness-import-manifest.json` after a successful fresh export, existing-installation bootstrap, or refresh/resync
  - flow docs under `docs/agents/flows/`
  - operation docs under `docs/agents/operations/`
  - profile docs under `docs/agents/profiles/`
  - non-persistent agent response scaffolds under `docs/agents/templates/`
  - the complete pinned research method under `docs/agents/methods/research-sadr/` only when `research` is selected
  - optional blank improvement templates under `docs/agents/templates/` and their metadata schema under `docs/agents/schemas/`
  - generated local experience at `docs/evidence/STORE.md`, `stages/`, `improvements/` and `experiments/` under that layer, ignored and consumer-owned, or at an existing configured equivalent; shared refresh preserves these outputs
  - separately selected public records under `docs/evidence/<domain>/<component>/`, preserving the four-domain source placement above, and only their common catalog's selected rows at `docs/evidence/README.md`, following managed import ownership
  - PRD and execution templates under `docs/plans/`
  - governance and review assets under `docs/policies/`
- Keep the rules for those artifacts in the consuming repo's policy layer instead of repeating them in folder README files.

## Workflow Variation
- Treat `harness/flows/delivery.md` as a strong default example, not the only valid orchestration shape.
- A consuming repo may use smaller or larger workflows from the same role set depending on product scope, stack shape, and approval needs.
- When the workflow expands, keep the role contracts stable and add profiles, lanes, or flow docs through composition rather than rewriting every role.

## Invocation
- Initialize one execution pass from the approved feature document and the runner guide.
- Treat the runner guide as the ordered prompt source for the current execution pass instead of generating runtime scaffolding files automatically.
- For selected research, start or resume through the Research Runner and the one resolved state owner; keep implementation invocation under its existing approval contract.

## Packaging Rule
- Treat `harness/` as the shared home for stable roles, flows, operations, profiles, workflow policies and templates. Shared baselines, delegation and evaluation criteria live under `policies/`; instructions, prompt presets and runtime adapters live under `agents/`. Public improvement records belong to the repository-level `evidence/` layer under their subject domain and component.
- Keep repo-specific operating rules in the consuming repo's `AGENTS.md` or `docs/policies/`; do not hide them inside reusable role definitions.
