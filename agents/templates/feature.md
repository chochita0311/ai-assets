# FEAT-0000: Title

## Metadata
- ID: `feat-0000`
- Status: `draft`
- Type: `product` | `foundation`
- Parent PRD: `[prd-0000-title](./prd.md)`
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

## Regression Surfaces
- Existing flows or features that must remain intact.

## Harness Trace
- Active spec doc:
- Latest evaluator report:
- Latest fix note:

## Continuity Notes
- `YYYY-MM-DD`: initial draft
