# FEAT-0000: Title

## Metadata
- ID: `feat-0000`
- Status: `draft`
- Type: `product` | `foundation`
- Surface: `frontend` | `backend` | `fullstack` | `data` | `infra` | `docs` | `mixed`
- Execution Profile:
- Required Evaluators:
- Parent PRD: `[prd-0000-title](../prd/prd-0000-title.md)`
- Created: `YYYY-MM-DD`
- Updated: `YYYY-MM-DD`

## Goal
- Product feature:
  - state the one user-visible outcome this feature is responsible for
- Foundation feature:
  - state the contract, invariant, or ambiguity this feature resolves for downstream work

## Acceptance Contract
- State the guarantees that must hold after this feature is complete.

### Product Feature Guidance
- Define the user-visible result that must hold.
- Example:
  - when user switches display mode, the active surface changes and the selected mode remains clear

### Foundation Feature Guidance
- Define the system-level contract that must hold.
- Example:
  - media source ownership is fixed
  - value shape is fixed and documented
  - fallback behavior is deterministic
  - downstream features do not need to guess

## Scope Boundary
- In:
- Out:

## Surface Lanes
- Use only when the feature spans multiple surfaces.
- Lane:
  - path roots:
  - dependencies:
  - expected evidence:
  - evaluator ownership:

## Contract Surfaces
- APIs, schemas, messages, generated outputs, routes, commands, config, source-of-truth ownership, or integration boundaries that must remain stable.

## Required Evaluators
- `contract` when contract surfaces, generated outputs, source-of-truth ownership, or integration boundaries matter.
- `design` when visible presentation changes.
- `functional` when runtime behavior changes.
- `ux-heuristic` when interaction clarity or friction should be inspected.

## User-Visible Outcome
- Required for `product` features.
- Optional for `foundation` features if the primary outcome is system-level rather than directly user-visible.

## Entry And Exit
- Entry point:
- Exit or transition behavior:

## State Expectations
- Default:
- Loading:
- Empty:
- Error:
- Success:

## Dependencies
- Required prerequisite features or system conditions.

## Likely Affected Surfaces
- Files, screens, modules, or system surfaces likely to change.

## Pass Or Fail Checks
- Checks must map directly to the Acceptance Contract.
- Checks must be testable without interpretation.

### Foundation Feature Guidance
- No unresolved ownership questions remain.
- No unresolved value-shape questions remain.
- Downstream spec can proceed without guessing.

### Contract Guidance
- Contract surfaces are explicitly defined.
- Producer and consumer expectations are clear.
- Generated artifacts are marked as derived output unless the project policy says otherwise.

## Regression Surfaces
- Existing flows or features that must remain intact.

## Harness Trace
- Active spec doc: `[spec-0000-title](../spec/spec-0000-title.md)`
- Active run: `[run-YYYYMMDD-01](../run/run-YYYYMMDD-01-title.md)`
- Execution profile:
- Latest evaluator report: `[eval-0000-title](../evaluation/eval-0000-title.md)`
- Latest fix note: `[fix-0000-title](../fix/fix-0000-title.md)`

## Continuity Notes
- `YYYY-MM-DD`: initial draft
