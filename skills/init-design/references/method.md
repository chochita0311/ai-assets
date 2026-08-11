# Init Design

## Contents

- [Purpose](#purpose)
- [What `init-design` Is](#what-init-design-is)
- [What Problem `init-design` Solves](#what-problem-init-design-solves)
- [General Operating Rule](#the-general-operating-rule)
- [When To Run `init-design`](#when-to-run-init-design)
- [Starting Artifact Types](#starting-artifact-types)
- [Expected Output](#expected-output-of-init-design)
- [Source Detection And Priority](#creative-source-detection)
- [Workflow](#workflow-of-init-design)
- [Source-Set Extraction Rules](#source-set-extraction-rules)
- [Screen Expansion Rules](#screen-expansion-rules)
- [Output Rule](#output-rule)
- [Drafting And Evaluation Model](#drafting-agent-and-evaluator-model)
- [Content Guidance](#content-guidance)
- [Constitution vs Plan](#constitution-vs-plan)
- [Writing And Pass/Fail Rules](#writing-rule)
- [Screen Scope Rule](#screen-scope-rule)
- [Non-Goals](#what-init-design-must-not-do)

## Purpose
- This document explains how `init-design` should work as a reusable startup workflow for design.
- It is written for solo builders who may start from:
  - a single AI-generated first screen
  - several related HTML or mock screens
  - a drafted visual entry screen
  - a source set plus product context
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
  - evaluates the current visual source set
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
- The initial source set is a probe.
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

### 2. Multi-Screen Source Set
- Starting artifact:
  - several related HTML pages
  - several frames from the same proposed product
  - several generated screens with overlapping structure
- Main benefit:
  - repeated patterns and system boundaries become easier to detect
- Main risk:
  - contradictions can be averaged together unless one source is named as the anchor

### 3. Screen Plus Context
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
1. current committed visual source set or the explicit base artifact(s) named by the user
2. existing creative-source document such as `DESIGN.md`
3. repository constraints and product/runtime docs
4. explicit user notes or clarifications for the current run
5. cautious inference only where the above sources do not decide the issue

Rules:
- Higher-priority sources should not be silently overridden by lower-priority sources.
- If a lower-priority source reveals a real contradiction, record it and resolve it explicitly instead of blending them together.
- When the source set is `index.html + DESIGN.md`, treat `index.html` as the artifact and `DESIGN.md` as the intent source; the constitution must reconcile them rather than copy either one blindly.
- When the source set contains several screens or HTML files, identify:
  - the anchor source with the strongest structural authority
  - repeated patterns across sources
  - contradictions that should be resolved explicitly instead of blended silently

## Workflow Of `init-design`

### Step 1. Read Project Inputs
- Read:
  - context docs
  - project guidance
  - existing schema docs
  - existing screens
  - token files if they exist

### Step 2. Identify Starting Source-Set Type
- classify:
  - single-screen artifact
  - multi-screen source set
  - screen-plus-context

### Step 3. Build Compatibility View
- identify:
  - entities
  - roles
  - states
  - expected device usage
  - future expansion pressure

### Step 4. Evaluate Initial Source Set
- if one or more visual artifacts exist, extract:
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

## Source-Set Extraction Rules
Use these rules as general extraction guidance. They are heuristic, not parser-level guarantees.

### Visual Tone Extraction
- Extract tone from repeated signals, not one decorative detail.
- Prioritize:
  - dominant backgrounds and surfaces
  - repeated typography hierarchy
  - repeated contrast behavior
  - repeated density and spacing rhythm
- Ignore one-off decorative anomalies unless they recur across the source set.

### Color Extraction
- Identify:
  - dominant page/background color
  - dominant surface color
  - dominant readable text color
  - accent color family from repeated interactive emphasis
- Treat the most repeated non-neutral interactive accent as the likely primary accent.
- Do not treat a single illustration, hero gradient, or one isolated badge as the whole color system.

### Spacing Extraction
- Infer spacing scale from repeated gaps, paddings, and section rhythms.
- Cluster toward a reusable step system instead of copying every literal measurement.
- Prefer identifying families such as compact, standard, and large spacing before declaring many exact values.

### Typography Extraction
- Identify recurring display, headline, body, and caption roles from repeated usage.
- Prefer role detection over copying every literal font size.
- If the source set mixes several text scales, preserve only the scales that recur enough to become durable system roles.

### Component Extraction
- Repeated structures are component candidates.
- Stable interaction surfaces such as buttons, inputs, cards, list rows, nav items, tabs, and drawers should be promoted before one-off compositions.
- If a pattern appears only once and does not look reusable, do not force it into the component layer.

### Shell And Layout Extraction
- Detect recurring shell structure:
  - top bar
  - side navigation
  - bottom navigation
  - content column
  - utility rail
- Treat shell structure as durable only when it recurs or is strongly reinforced by context.

## Screen Expansion Rules
- Infer durable screen families from the source set, not from a fixed template count.
- Strong signals:
  - repeated collections or preview rows suggest browse/list families
  - title + metadata + long body structures suggest detail/read families
  - visible form fields, editors, or input-heavy actions suggest create/edit families
  - persistent global navigation suggests settings, archive, or system-level surfaces later
- When several screens are given, prefer the families supported by repeated structure across them.
- When only one screen is given, infer cautiously and record only families strongly implied by that screen plus context.
- Do not invent speculative screen families just to make the system feel complete.

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

## Content Guidance

Use [constitution-content-guide.md](constitution-content-guide.md) only when a run needs:

- the seven-department model for constitution content
- property-level definition guidance
- primitive or semantic token examples
- terminology support for builders less familiar with design systems

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
- Treat list, detail, and create/edit as common examples, not mandatory slots.
- The selected family set is stable only when shared tokens, layout rules, and components can support it without page-specific visual invention.

## What `init-design` Must Not Do
- It must not create many screens before defining rules
- It must not treat one AI-generated page as final truth
- It must not ignore roles, states, and validation constraints
- It must not recommend visual changes without explaining system impact
- It must not optimize implementation style before design boundaries are clear
- It must not add complex animation systems, rare variants, decorative experiments, or new accent families before the core system is stable
