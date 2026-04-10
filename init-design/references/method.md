# Init Design

## Purpose
- This document explains how `init-design` should work as a reusable startup workflow for design.
- It is written for solo builders who may start from:
  - a single AI-generated first screen
  - a drafted visual entry screen
  - a first screen plus product context
- The goal is to make design:
  - compatible with backend and frontend evolution
  - maintainable as the project grows
  - consistent across screens
  - restartable after long gaps

## What `init-design` Is
- `init-design` is not a screen generator.
- `init-design` is not a prompt that asks AI to make something pretty.
- `init-design` is a startup design workflow:
  - it reads the current project state
  - evaluates the current visual entry artifact
  - checks compatibility against product and system constraints
  - extracts stable design decisions
  - organizes them into a constitution
  - and writes the governance rules for how design documents relate

## What Problem `init-design` Solves
- Without a stable startup workflow:
  - AI creates different tones from screen to screen
  - the first screen silently becomes the whole system
  - backend realities and UI assumptions drift apart
  - restarting the project feels like starting over
- With a stable startup workflow:
  - design decisions become explicit
  - AI works within constraints
  - frontend and backend remain compatible
  - the next step is always concrete

## The General Operating Rule
- The first screen is a probe.
- The constitution is the system.
- Tokens and semantics are the implementation bridge.
- Components and layouts are the reusable execution layer.

## When To Run `init-design`
- At the beginning of a new project
- After generating a first screen artifact
- When the product direction changes
- When a project has drifted and needs re-baselining

## Starting Artifact Types

### 1. Single Screen Artifact
- Starting artifact:
  - AI-generated first screen
  - a Figma frame
  - a mobile mockup
- Main benefit:
  - tone and hierarchy become visible fast
- Main risk:
  - page styling becomes fake system design

### 2. Screen Plus Context
- Starting artifact:
  - a first screen
  - `DESIGN.md` or another design-intent document
  - product notes
  - schema notes
  - role definitions
  - workflow notes
- Main benefit:
  - design direction can be tested against real product constraints
- Main risk:
  - contradictions stay hidden unless explicitly resolved

## Expected Output Of `init-design`
- `1. Product context summary or delta`
- `2. Starting artifact classification`
- `3. Compatibility constraints`
- `4. Design DNA`
- `5. Primitive token draft`
- `6. Semantic token draft`
- `7. Layout model`
- `8. Core component model`
- `9. Screen-family baseline`
- `10. Risks and unknowns`
- `11. Versioning note`
- `12. Design document governance`

## Creative Source Detection
- If the repo already has a creative-source document such as `DESIGN.md`, treat it as the design-intent source.
- Do not promote that file directly into durable law.
- Reflect the actual source file name in the governance doc when it exists.
- If no creative-source document exists, keep the governance wording general enough to tolerate a future source file.

## Source Priority
Use this priority order unless the repository explicitly defines another source-of-truth rule:
1. current committed screen artifact or the explicit base screen named by the user
2. existing creative-source document such as `DESIGN.md`
3. repository constraints and product/runtime docs
4. explicit user notes or clarifications for the current run
5. cautious inference only where the above sources do not decide the issue

Rules:
- Higher-priority sources should not be silently overridden by lower-priority sources.
- If a lower-priority source reveals a real contradiction, record it and resolve it explicitly instead of blending them together.
- When the source set is `index.html + DESIGN.md`, treat `index.html` as the artifact and `DESIGN.md` as the intent source; the constitution must reconcile them rather than copy either one blindly.

## Output Rule
- `design-constitution.md` is the durable design record.
- `design-document-governance.md` defines how design documents relate and when each one should be updated.
- The constitution should survive multiple screen additions with only occasional updates.
- If a section mainly answers "what is locked?", it belongs in the constitution.
- If a section mainly answers "what now?", keep it in the response or hand it off to a separate planning skill instead of turning `init-design` into a mixed-purpose workflow.
- If a section mainly answers "which document owns this kind of change?", it belongs in the governance doc.

## Drafting Agent And Evaluator Model
- The drafting agent should generate files that stand on their own without extra verbal rescue.
- The evaluator should be able to evaluate those files against the checklist without re-running artifact analysis from scratch.
- If an evaluator would need unstated assumptions to judge the result, the drafting output is too soft.

## Department Structure
- Think of `init-design` as seven departments.
- Each department answers a different kind of design question.

### Department 1. Product Context
- Purpose:
  - define what kind of product this is
- Questions:
  - Who uses it?
  - What do they repeat most?
  - Is it read-heavy, write-heavy, or workflow-heavy?
  - Which device matters first?
- Required properties:
  - product type
  - primary users
  - primary jobs to be done
  - device priority
  - technical constraints
  - starting artifact type

### Department 2. Compatibility Constraints
- Purpose:
  - keep design compatible with real system behavior
- Questions:
  - What entities exist?
  - What statuses exist?
  - What roles exist?
  - Which validation rules will affect the UI?
  - Which states must the UI support later?
- Required properties:
  - data model constraints
  - role and permission constraints
  - status/state constraints
  - form and validation constraints
  - mobile and responsive constraints
  - future expansion constraints

### Department 3. Design DNA
- Purpose:
  - define the product feel
- Questions:
  - What should the interface feel like?
  - What should it never become?
  - What kind of visual pressure is allowed?
- Required properties:
  - tone keywords
  - visual principles
  - anti-principles

### Department 4. Primitive Tokens
- Purpose:
  - define raw design constants
- Questions:
  - What are the allowed colors?
  - What spacing scale is allowed?
  - What radius scale is allowed?
  - What typography scale is allowed?
- Required properties:
  - colors
  - typography
  - spacing
  - radius
  - shadows
  - motion
  - states

### Department 5. Semantic Tokens
- Purpose:
  - map primitive tokens to product meaning
- Questions:
  - Which color is the page background?
  - Which surface is a card?
  - Which text is metadata?
  - Which action is primary?
  - Which shell sizes change by device?
- Required properties:
  - page background
  - surface hierarchy
  - text hierarchy
  - action hierarchy
  - feedback hierarchy
  - shell sizing
  - reading mode

### Department 6. Layout Rules
- Purpose:
  - define how pages are structured
- Questions:
  - Is there a sidebar?
  - Is the product mobile-first or desktop-first?
  - What becomes a bottom nav on mobile?
  - How dense can content become?
- Required properties:
  - app shell
  - navigation model
  - breakpoints
  - density rules
  - content widths

### Department 7. Component Rules
- Purpose:
  - define reusable parts
- Questions:
  - What is a button in this product?
  - What is a list row?
  - What is a card?
  - What are the only allowed variants?
- Required properties:
  - buttons
  - inputs
  - cards
  - lists
  - tables
  - tabs or chips
  - dialogs or drawers
  - empty, loading, and error states

## Constitution vs Plan

### Constitution
- Purpose:
  - define the stable design system for the project
- Should include:
  - product context that materially shapes design
  - compatibility constraints that affect enduring UI rules
  - design DNA
  - primitive tokens
  - semantic tokens
  - layout rules
  - component rules
  - core UI patterns
  - mobile evolution rules
  - implementation guardrails
  - AI guardrails
  - screen families only when they are durable structure
- Should not include:
  - next actions
  - implementation tasks
  - sequencing
  - temporary gaps that do not alter durable rules
  - transitional phrasing inside the rule itself
  - fallback wording that belongs in open decisions

## Writing Rule
- The constitution should read like a clean standard, not like a migration memo.
- When a rule is locked, write it directly.
- When a rule is unsettled, either leave it out of the constitution or note it briefly in the response instead of forcing a planning document.
- Prefer short references such as `see constitution` over re-explaining stable sections in full.

## Pass / Fail Standard
- `Pass` means:
  - the constitution cleanly separates durable law from temporary action
  - the governance doc cleanly separates creative source, durable law, and future planning ownership
  - the outputs make it possible to extend the product without inventing new tone, token families, or screen logic casually
- `Fail` means any of these:
  - tactical next actions or rollout sequencing appear inside the constitution
  - the creative-source file exists but is not named in governance
  - durable rule ownership is ambiguous between source docs
  - an evaluator could not tell whether three more screens could be built without visual drift

## Screen Scope Rule
- Do not force a literal `First 3 Screens` section in every project.
- The durable concept is screen families, not a fixed count.
- Typical early families are:
  - entry or list
  - detail or read
  - create, edit, or action flow
- If the starting input only supports one or two families, record only those.
- If more families are already clearly required, record them.
- Put durable screen families in the constitution.

## How Each Property Should Be Defined

### Product Type
- Define the dominant product category, not every future possibility.
- Good examples:
  - private knowledge management app
  - community board system
  - class reservation workflow
- Bad example:
  - all-in-one learning social booking platform with everything

### Primary Users
- Define actual user groups, not generic visitors.
- Good examples:
  - admin
  - teacher
  - student
  - personal note owner

### Primary Jobs To Be Done
- Write repeated user actions, not aspirations.
- Good examples:
  - browse item lists
  - read detail views
  - add and edit records
  - search and filter content

### Device Priority
- Choose one:
  - mobile-first
  - desktop-first
  - dual-first
- Rule:
  - if the product will mainly live in webview/mobile, do not let a desktop dashboard become the permanent base by accident

### Technical Constraints
- Include constraints that will shape the UI:
  - static hosting
  - SSR/SPA choice
  - auth strategy
  - offline or sync behavior
  - low-complexity MVP

### Data Model Constraints
- Define which entities and relationships matter now.
- Example questions:
  - does an item belong to a collection?
  - can comments exist later?
  - are records soft-deleted?
  - do records have sync status?

### Role And Permission Constraints
- Define who sees what.
- Example:
  - admin can create and manage
  - student can view and interact
  - guest sees only public content

### Status And State Constraints
- List UI-relevant states.
- Examples:
  - draft
  - published
  - archived
  - syncing
  - failed
  - empty
  - loading
  - locked

### Tone Keywords
- Use 5 to 8 words only.
- Example:
  - luxury minimal
  - soft cream workspace
  - deep navy foundation
  - editorial contrast
  - calm structure

### Visual Principles
- Use action-oriented statements.
- Good examples:
  - use whitespace and type hierarchy before decoration
  - keep one strong accent color
  - prefer soft surfaces over loud fills

### Anti-Principles
- Define what should not happen.
- Good examples:
  - no random gradients
  - no neon accents
  - no mixed radius language
  - no hard black shadows

### Primitive Tokens
- Primitive tokens are raw constants.
- They should not know what a card or topbar is.
- Example:
```css
:root {
  --color-primary: #144bb8;
  --color-bg-light: #fdfcf9;
  --color-text-strong: #111827;
  --radius-md: 12px;
  --space-4: 16px;
}
```

### Semantic Tokens
- Semantic tokens describe role, not raw value.
- They should answer:
  - what this value is used for in the product
- Example:
```css
:root {
  --page-bg: var(--color-bg-light);
  --page-heading: var(--color-text-strong);
  --surface-card: var(--color-surface-light);
  --interactive-primary-bg: var(--color-primary);
  --radius-card: var(--radius-md);
  --radius-panel: var(--radius-lg);
}
```

### Layout Rules
- Layout rules decide where structure lives.
- For example:
  - sidebar width
  - topbar height
  - content shell padding
  - mobile drawer behavior
- Example:
```css
:root {
  --sidebar-width: 256px;
  --topbar-height-desktop: 74px;
  --board-drawer-width: min(84vw, 320px);
}
```

### Component Rules
- Component rules should define:
  - purpose
  - allowed variants
  - allowed states
  - forbidden deviations
- Example:
  - primary button uses primary accent, bold label, modest lift
  - ghost button uses soft border and quiet surface

## Concrete Example Using This Repo

### Primitive Token Example
- Example:
```css
:root {
  --color-primary: #144bb8;
  --color-primary-strong: #0f3d97;
  --color-bg-light: #fdfcf9;
  --color-surface-light: #ffffff;
  --color-text-muted: #667085;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --space-1: 4px;
  --space-4: 16px;
  --shadow-card: 0 4px 20px -2px rgba(20, 75, 184, 0.05);
}
```
- General lesson:
  - this layer is raw, reusable, and stack-agnostic

### Semantic Token Example
- Example:
```css
:root {
  --page-bg: var(--color-bg-light);
  --page-heading: var(--color-text-strong);
  --surface-card: var(--color-surface-light);
  --interactive-primary-bg: var(--color-primary);
  --radius-card: var(--radius-md);
  --radius-panel: var(--radius-lg);
}
```
- General lesson:
  - this layer explains product usage, not brand constants

### Why This Matters
- If a project changes from:
  - cream reading app
  - to darker workflow app
- you may be able to change semantic mappings without rewriting every component

## Design Terms For Backend-Minded Builders

### Design Token
- Equivalent mindset:
  - constants
  - config values
- Good analogy:
  - `application.yml` for UI values

### Semantic Token
- Equivalent mindset:
  - service-level alias or named contract
- Example:
  - not every service should know the database column name directly
  - not every component should know the raw token directly

### Radius
- Means corner roundness.
- Example:
  - `12px` means a softly rounded rectangle

### Surface
- Means a visible layer like a card, panel, or sheet.

### Shadow
- Means depth cue.
- In premium interfaces:
  - weaker is often better

### Spacing Scale
- Means approved gaps and paddings.
- Example:
  - `4 / 8 / 12 / 16 / 24 / 32`
- Rule:
  - components should use only approved distances

## Workflow Of `init-design`

### Step 1. Read Project Inputs
- Read:
  - context docs
  - project guidance
  - existing schema docs
  - existing screens
  - token files if they exist

### Step 2. Identify Starting Artifact Type
- classify:
  - single-screen artifact
  - screen-plus-context

### Step 3. Build Compatibility View
- identify:
  - entities
  - roles
  - states
  - expected device usage
  - future expansion pressure

### Step 4. Evaluate Initial Artifact
- if a first screen artifact exists, extract:
  - tone
  - hierarchy
  - navigation assumptions
  - layout density
  - list/detail/edit implications

### Step 5. Convert Artifact Into Constitution
- write:
  - design DNA
  - visual principles
  - anti-principles
  - token draft
  - semantic draft
  - layout rules
  - component rules

### Step 6. Write Outputs To Project Docs
- Default output locations:
  - `./docs/policies/design/design-constitution.md`
  - `./docs/policies/design/design-document-governance.md`
- If the project already uses another established design-doc folder, follow that local convention instead of creating a second parallel location.
- If `DESIGN.md` or another creative-source doc exists, wire that actual file into the governance output instead of leaving the source unnamed.

### Step 7. Add Guardrails
- explicitly define:
  - what may not change casually
  - what requires versioning
  - what AI should not invent

## What `init-design` Must Not Do
- It must not create many screens before defining rules
- It must not treat one AI-generated page as final truth
- It must not ignore roles, states, and validation constraints
- It must not recommend visual changes without explaining system impact
- It must not optimize implementation style before design boundaries are clear

## First 3-Screen Rule
- Every project should stabilize around:
  - entry/list screen
  - detail/read screen
  - create/edit screen
- Reason:
  - if the same design system can support these three, it usually has real reuse potential

## What To Lock Early
- color hierarchy
- typography hierarchy
- spacing categories
- radius scale
- shell structure
- navigation model
- state model
- component naming

## What To Delay
- complex animation systems
- large screen counts
- rare feature variants
- decorative experimentation
- new accent colors

## Suggested `init-design` Output Format
- `Summary`
- `Starting Artifact`
- `Compatibility Constraints`
- `Design DNA`
- `Primitive Tokens`
- `Semantic Tokens`
- `Layout Rules`
- `Core Components`
- `First 3 Screens`
- `Known Risks`
- `Next Actions`

## Quality Checklist
- Can a new screen be built without inventing a new color?
- Can a new screen be built without inventing a new radius?
- Do backend states map to UI states?
- Do roles map to navigation or action differences?
- Can AI be instructed to reuse the system instead of creating new tone?
- If the product changes, is there a place to update the constitution first?

## Simple Success Test
- After a long break, you should be able to reopen the project and answer:
  - what kind of product this is
  - what kind of UI tone it has
  - which values are locked
  - which components already exist
  - what should be built next
- If not, the `init-design` workflow is still incomplete.
