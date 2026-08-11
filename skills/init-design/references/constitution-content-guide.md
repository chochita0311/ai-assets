# Design Constitution Content Guide

Use this file only when a run needs detailed guidance for defining constitution content, tokens, examples, or design terminology.

The procedural workflow remains in [method.md](method.md). Output structure remains owned by the templates.

## Contents

- [Purpose](#purpose)
- [Department Structure](#department-structure)
- [Property Definition Guidance](#how-each-property-should-be-defined)
- [Concrete Token Example](#concrete-token-example)
- [Design Terms](#design-terms-for-backend-minded-builders)

## Purpose

- Own the explanatory model for constitution content.
- Provide optional property-level guidance without making every `init-design` run load it.
- Keep examples and terminology separate from execution order and approval logic.

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
- Use [Concrete Token Example](#concrete-token-example) for the complete raw-token example.

### Semantic Tokens
- Semantic tokens describe role, not raw value.
- They should answer:
  - what this value is used for in the product
- Use [Concrete Token Example](#concrete-token-example) for the complete role-mapping example.

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

## Concrete Token Example

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
