# Init Design Checklist

## Purpose
- Use this as the quick execution sheet for `init-design`.
- This is the short version of the full guide.
- Run through it before expanding screens.

## 1. Identify The Start
- What is the current starting artifact?
  - first screen artifact
  - first screen plus product context
- Which starting point is this?
  - single-screen artifact
  - screen-plus-context
- Is the source priority explicit?
  - screen artifact
  - creative-source doc such as `DESIGN.md`
  - repo constraints/docs
  - user notes

## 2. Confirm Product Reality
- Who are the primary users?
- What are the 3 main repeated tasks?
- Is the product read-heavy, action-heavy, or workflow-heavy?
- Which device matters first?

## 3. Check Compatibility
- What entities already exist?
- What roles already exist?
- What important states already exist?
- What validations or permissions will affect UI?
- What future expansion is already likely?

## 4. Evaluate The First Artifact
- Extract from the first screen:
  - what is the tone?
  - what is the content hierarchy?
  - what components repeat?
  - what is missing?
- Then validate against system constraints:
  - what screen families are implied?
  - what role differences are implied?
  - what UI states are required?

## 5. Lock Design DNA
- Write 5 to 8 tone keywords
- Write 3 to 5 visual principles
- Write 5 to 8 anti-principles

## 6. Lock Primitive Tokens
- Colors
- Typography
- Spacing
- Radius
- Shadows
- States

## 7. Lock Semantic Tokens
- Page background
- Surface hierarchy
- Text hierarchy
- Action hierarchy
- Feedback hierarchy
- Shell sizing
- Reading mode

## 8. Lock Layout Rules
- App shell
- Navigation model
- Breakpoints
- Mobile transformation
- Content width rule

## 9. Lock Core Components
- Button
- Input
- Card
- List row
- Table or grid
- Tabs or chips
- Dialog or drawer
- Empty/loading/error state

## 10. Define Screen Families
- Identify the minimum durable screen families implied by the product
- Typical early families:
  - entry or list
  - detail or read
  - create, edit, or action flow
- Do not force three if the product currently supports fewer
- Do not stop at three if the product clearly needs more
- Put durable families in the constitution

## 11. Check Stability
- Can these screens be built without new colors?
- Can they be built without new radius values?
- Can they be built without page-specific hacks?
- Do backend states map to UI states?

## 12. Define Guardrails
- No raw values outside primitive tokens
- No direct primitive use in components when semantic aliases should exist
- No casual redesign-by-prompt
- No uncontrolled screen expansion before durable screen families are stable

## 13. Output Required
- Constitution contains the durable sections:
  - project context
  - compatibility constraints
  - design DNA
  - primitive tokens
  - semantic tokens
  - layout rules
  - core components
  - screen families
- Governance doc contains:
  - document ownership
  - source hierarchy
  - update rules
  - rule-promotion guidance
  - evaluation rules
  - the actual creative-source file when one already exists

## 14. Pass / Fail Checks
- `Pass` only if the constitution stands on its own as the stable rule document.
- `Pass` only if the governance doc explains which design document to update when a change affects intent, durable law, or future planning.
- `Pass` only if the governance doc names the actual creative-source file when one exists.
- `Pass` only if another agent could build several more screens without inventing new colors, radius families, spacing logic, or tone by guesswork.
- `Fail` if the constitution contains implementation sequencing, next actions, or temporary tactical notes.
- `Fail` if the governance doc leaves document ownership ambiguous.
- `Fail` if the outputs depend on unstated assumptions an evaluator cannot verify from the files.
- Follow-up notes should stay in the response unless they clearly deserve a separate planning workflow.

## 15. Final Question
- If I stop this work for a month, will I know:
  - what the product is
  - how it should feel
  - which values are locked
  - which components already exist
- If not, `init-design` is not finished yet.
