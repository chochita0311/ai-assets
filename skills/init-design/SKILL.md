---
name: init-design
description: Use when starting or resetting product design from an initial source set and you need to turn it into a stable design constitution with compatibility checks and reusable rules. Use for web, mobile, or mixed products when one or more visual sources exist but should not become the system by themselves.
---

# Init Design

Use this skill to turn an initial source set into a stable design starting point.

## Use This Skill When
- A project has one or more visual sources such as screens, HTML pages, mocks, or AI-generated entry pages but no stable design rules yet
- The visual direction exists, but compatibility, expandability, and maintainability are still unclear
- You need to convert a screen into:
  - design DNA
  - primitive tokens
  - semantic tokens
  - layout rules
  - core component rules
  - a design constitution
  - design document governance
- A project has drifted and needs its design baseline rebuilt from the current source set

## Do Not Use This Skill When
- There is no visual source set yet
- The task is only to polish a single existing component
- The task is implementation-only and the design constitution already exists
- The task is a full visual redesign without a stable starting artifact to evaluate

## Invocation Examples
- `Use $init-design to analyze this project from the current source set and produce a design constitution.`
- `Use $init-design to review these initial screens and turn them into stable tokens, layout rules, and a design constitution.`
- `Use $init-design to reset the design baseline for this app using the current main screen and the existing product constraints.`
- `Use $init-design to analyze these HTML files plus DESIGN.md and derive one design constitution.`

## Reference Routing

- For every run, read [Source Priority](references/method.md#source-priority), [Workflow Of `init-design`](references/method.md#workflow-of-init-design), [Output Rule](references/method.md#output-rule), and [Constitution vs Plan](references/method.md#constitution-vs-plan).
- Read [Starting Artifact Types](references/method.md#starting-artifact-types) when the source-set type is unclear.
- Read [Source-Set Extraction Rules](references/method.md#source-set-extraction-rules) when extracting rules from several artifacts or reconciling source differences.
- Read [Screen Expansion Rules](references/method.md#screen-expansion-rules) only when the constitution needs durable screen-family guidance.
- Read [constitution-content-guide.md](references/constitution-content-guide.md) only when detailed property definitions, token examples, the department model, or design terminology are needed.
- Use [references/checklist.md](references/checklist.md) as the final quick validation pass.

## Workflow
1. Identify the starting source-set type:
   - `single-screen artifact`
   - `multi-screen source set`
   - `screen-plus-context`
2. Resolve source priority before writing:
   - current visual source set or committed base artifact(s)
   - existing creative-source document such as `DESIGN.md`
   - repository constraints and docs
   - explicit user notes or clarifications
   - only then inference
3. Identify whether a creative-source document already exists, such as `DESIGN.md`, and treat it as source material rather than as durable law.
4. Evaluate the artifact as design input, not as the final system.
5. Check compatibility against:
   - product goals
   - entities
   - roles
   - states
   - device priority
6. Write or update the constitution with [templates/design-constitution.md](templates/design-constitution.md).
7. Write or update design document governance with [templates/design-document-governance.md](templates/design-document-governance.md).
8. Complete the routed final validation pass.

## Package Layout
- `references/`
  - `method.md`: procedural workflow and ownership decisions
  - `constitution-content-guide.md`: optional property, token, and terminology guidance
  - `checklist.md`: final binary validation
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
- Start from a visual source set, but never let the source set become the system by itself.
- Always convert the source set into explicit rules before expanding screens.
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
