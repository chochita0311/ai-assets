---
name: init-design
description: Use when starting or resetting product design from a first screen artifact and you need to turn it into a stable design constitution with compatibility checks and reusable rules. Use for web, mobile, or mixed products when a visual starting point exists but should not become the system by itself.
---

# Init Design

Use this skill to turn a first screen artifact into a stable design starting point.

## Use This Skill When
- A project has a first screen, mockup, or AI-generated entry page but no stable design rules yet
- The visual direction exists, but compatibility, expandability, and maintainability are still unclear
- You need to convert a screen into:
  - design DNA
  - primitive tokens
  - semantic tokens
  - layout rules
  - core component rules
  - a design constitution
  - design document governance
- A project has drifted and needs its design baseline rebuilt from the current artifact

## Do Not Use This Skill When
- There is no visual entry artifact yet
- The task is only to polish a single existing component
- The task is implementation-only and the design constitution already exists
- The task is a full visual redesign without a stable starting artifact to evaluate

## Invocation Examples
- `Use $init-design to analyze this project from the current first screen artifact and produce a design constitution.`
- `Use $init-design to review this initial screen and turn it into stable tokens, layout rules, and a design constitution.`
- `Use $init-design to reset the design baseline for this app using the current main screen and the existing product constraints.`
- `Use $init-design to analyze this project from index.html and DESIGN.md and make a constitution.`

## Workflow
1. Read `references/method.md` for the full workflow.
2. Identify the starting artifact type:
   - `single-screen artifact`
   - `screen-plus-context`
3. Resolve source priority before writing:
   - current screen artifact or committed base screen
   - existing creative-source document such as `DESIGN.md`
   - repository constraints and docs
   - explicit user notes or clarifications
   - only then inference
4. Identify whether a creative-source document already exists, such as `DESIGN.md`, and treat it as source material rather than as durable law.
5. Evaluate the artifact as design input, not as the final system.
6. Check compatibility against:
   - product goals
   - entities
   - roles
   - states
   - device priority
7. Write or update the constitution with `templates/design-constitution.md`.
8. Write or update design document governance with `templates/design-document-governance.md`.
9. Use `references/checklist.md` as the final quick validation pass.

## Package Layout
- `references/`
  - workflow and explanatory material to read while thinking
- `templates/`
  - reusable output scaffolds to copy or adapt for constitutions and governance docs
- `agents/openai.yaml`
  - optional UI metadata

## Output Location
- Write project outputs under split policy/plan folders by default:
  - `./docs/policies/design/design-constitution.md`
  - `./docs/policies/design/design-document-governance.md`
- Only use another folder if the project already has an established convention.

## Core Rule
- Start from a screen artifact, but never let that artifact become the system by itself.
- Always convert the artifact into explicit rules before expanding screens.
- Always validate design against compatibility, expandability, and maintainability constraints.
- Treat the constitution as the stable rule document.
- Keep screen families in the constitution only when they are durable product structure.
- Treat this skill as drafting-agent/evaluator friendly: a second agent should be able to judge pass/fail from the output files without reconstructing the whole design process.

## Constitution Scope
- `design-constitution.md` answers:
  - what is locked
  - how the product should feel
  - which tokens, semantics, layouts, and component rules are durable
  - which screen families are fundamental to the product structure
- `design-constitution.md` must not include:
  - immediate next actions
  - implementation sequencing
  - file-by-file work items
  - temporary uncertainty that does not change durable rules
  - transitional wording such as `for now`, `until later`, or `currently unless changed`

## Governance Scope
- `design-document-governance.md` answers:
  - how `DESIGN.md`, the constitution, and any future design plan relate
  - which document owns which kind of change
  - how durable design rules are promoted or updated
- `design-document-governance.md` should stay general enough to work whether a design plan exists yet or only becomes necessary later.
- When a creative-source file such as `DESIGN.md` already exists, the governance doc should name it concretely instead of leaving the source abstract.

## Pass/Fail Expectation
- A run passes only when:
  - the constitution reads like durable law rather than implementation notes or next-step planning
  - the governance doc names the actual creative source when one exists
  - the output is strong enough that another agent could build several more screens without inventing a new visual language
- A run fails when:
  - the constitution mixes durable rules with temporary tasks or sequencing
  - the governance doc leaves source ownership ambiguous
  - the output depends on unstated assumptions that an evaluator cannot verify from the files
