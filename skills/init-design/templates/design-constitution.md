# Design Constitution Template

## Use
- This file is the stable design source of truth.
- Keep durable rules here.
- Do not put immediate next actions, implementation sequencing, or temporary task lists here.
- Do not write transition phrases inside locked rules; if something is unsettled, leave it out of the constitution or handle it in a separate planning workflow.

## Source Basis And Adopted Decisions
- Baseline identity and authorized scope:
- Existing rules retained or deliberately changed:

| Source | Locator and available snapshot identity | Role and derivation | Observed region/device/theme/state and evidence kind | Material limits |
|---|---|---|---|---|
| | | | | |

| Adopted rule or token group | Source locator or product requirement | Basis: observed / reported / inferred / proposed | Adoption rationale and resolved conflicts |
|---|---|---|---|
| | | | |

## 1. Project Context
- Product type:
- Primary users:
- Primary jobs to be done:
- Device priority:
- Technical constraints:
- Starting source-set type:
  - single-screen artifact
  - multi-screen source set
  - screen-plus-context

## 2. Compatibility Constraints
- Data model constraints:
- Role and permission constraints:
- Status/state constraints:
- Form and validation constraints:
- Mobile and responsive constraints:
- Future expansion constraints:

## 3. Design DNA
- Tone keywords:
- Visual principles:
- Anti-principles:
- Source of truth:
- Reference boundaries:

## 4. Primitive Tokens
- Colors:
- Typography:
- Spacing:
- Radius:
- Shadows:
- Motion:
- States:

| Token | Type and chosen value/unit | Original value and source/context | Normalization reason, if changed |
|---|---|---|---|
| | | | |

## 5. Semantic Tokens
- Page background:
- Surface hierarchy:
- Text hierarchy:
- Action hierarchy:
- Feedback hierarchy:
- Shell sizing:
- Reading mode:

| Semantic token | Primitive mapping | Role and component usage | Theme/state scope |
|---|---|---|---|
| | | | |

Material color combinations, including adopted interaction states; equivalent
pairs may share a row. Keep static checks distinct from rendered validation.

| Text/control variant | Foreground, background, and host surface | Theme/state and usage restrictions | Actual check result and evidence limit |
|---|---|---|---|
| | | | |

## 6. Layout Rules
- App shell:
- Navigation model:
- Breakpoints:
- Density rules:
- Content widths:

## 7. Core Components
- Buttons:
- Inputs:
- Cards:
- Lists:
- Tables:
- Tabs or chips:
- Dialogs or drawers:
- Empty, loading, and error states:
- For each applicable component: purpose, anatomy, variants, required states, token mappings, and forbidden deviations.

## 8. Core UI Patterns
- App shell pattern:
- Card and panel pattern:
- Button pattern:
- Navigation pattern:
- List and table pattern:
- Form pattern:
- Filter and chip pattern:

## 9. Mobile Evolution Rules
- What simplifies on mobile:
- What must stay visually consistent:
- Navigation transformation:
- Density rule:
- Content overflow, missing content, and touch/zoom behavior:

## 10. Implementation Rules
- Primitive token rule:
- Semantic token rule:
- Component rule:
- Layout rule:
- Source-of-truth update rule:
- Readability, contrast, keyboard focus, and reduced-motion requirements:
- Font/asset availability and fallback rules:
- Optional derived token/export owner and synchronization rule:

## 11. AI Guardrails
- AI may:
- AI may not:
- Versioning trigger:

## 12. Durable Screen Families
- Screen families:
- Why these families are fundamental:
- Family-specific constraints:

## 13. Guardrails
- Forbidden visual drift:
- Rules for adding new tokens:
- Rules for adding new component variants:
- Rules for versioning:
