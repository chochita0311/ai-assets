# Agent Roles

## Purpose
- Keep reusable role definitions for iterative harness work in one editable package.
- Draft and refine the role contracts here before promoting them into shared assets.
- Keep these role docs general-purpose unless a file is explicitly marked repo-local.

## Current Roles
- `agents/prd-normalizer.md`: normalize chaotic product inputs into a bounded PRD package
- `agents/feature-planner.md`: decompose a normalized PRD into loop-sized product and foundation features
- `agents/workflow.md`: define the baton flow and approval points between roles

## Related Shared Docs
- `docs/policies/prd-feature-management.md`: shared planning-governance rules for PRDs and features
- `agents/templates/prd.md`: reusable PRD template
- `agents/templates/feature.md`: reusable feature template

## Planning Artifact Placement
- In a consumer repo, store bounded PRD instances under `docs/plans/prd/`.
- In a consumer repo, store loop-sized feature instances under `docs/plans/feature/`.
- Keep the rules for those artifacts in `docs/policies/prd-feature-management.md` instead of repeating them in folder README files.

## Workflow Variation
- Treat `agents/workflow.md` as a reusable default example, not the only valid orchestration shape.
- Consumer repos may assemble smaller or larger workflows from the same role set depending on product scope, stack shape, and approval needs.
- When the workflow expands, keep the role contracts stable and add variation through sequencing rather than rewriting every role.

## Packaging Rule
- Treat `agents/` as the shared home for stable general-purpose role definitions.
- Promote or refine role drafts here once they are no longer repo-specific.
- Keep repo-specific operating rules in project repos instead of hiding them inside reusable role definitions.
