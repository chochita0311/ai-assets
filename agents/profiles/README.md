# Execution Profiles

## Purpose
- Define reusable loop presets that assemble stable roles for common project shapes.
- Keep framework, language, and surface differences out of the role contracts.
- Let consuming repos choose the smallest profile that fits the approved feature.

## Ownership
- This directory owns profile descriptions.
- Use the harness `execution-profiles.md` policy for the rules that govern profile selection, surface lanes, and evaluator routing.
- Use the Orchestrator role contract for the role responsible for selecting and applying a profile during a run.

## Profile Set
- `frontend-product.md`: user-facing screen, component, route, interaction, or presentation work.
- `backend-product.md`: service, API, job, command, persistence, message, or server-side behavior work.
- `fullstack-product.md`: product work spanning two or more coupled surfaces.
- `foundation-contract.md`: contract, invariant, ownership, schema, identity, or generated-output foundation work.
- `infra-devtool.md`: infrastructure, tooling, scripts, CI, local workflow, or operational developer-surface work.
- `docs-content.md`: documentation, content, policy, guide, or information-architecture work.

## Use Rule
- Profiles are presets, not new role systems.
- Roles remain stable across profiles.
- A feature may use one profile by default, or a multi-surface profile with explicit lanes when one loop must coordinate multiple surfaces.
