# Method

Use this file for the full document-structuring procedure.

## Contents

- [Purpose](#purpose)
- [Working Sequence](#working-sequence)
- [Entrance-Doc Handling](#entrance-doc-handling)
- [Restructure Boundaries](#restructure-boundaries)
- [Writing Standard](#writing-standard)
- [Change Tracking](#change-tracking)
- [Finish Pass](#finish-pass)

## Purpose
- audit the current documentation set
- classify ownership and layering
- reorganize without discarding useful content
- reduce duplication
- leave a maintainable doc tree behind

## Working Sequence

### 1. Audit the active docs
- Start from the root and the most central entry docs.
- Read enough of the current structure to understand:
  - what the repo is
  - where users start
  - where contributors start
  - where durable detail currently lives
- Respect user exclusions for protected, legacy, or deferred doc areas.

### 1a. Choose operating mode
- Default to `incremental` when the repository already has a mostly workable doc tree.
- Use `restructure` when document ownership is badly mixed, duplication is widespread, or entrance/docs-map layers are broken.
- In `incremental` mode:
  - focus on changed, stale, or overlapping docs first
  - preserve stable ownership unless it is clearly violated
  - avoid broad churn for unaffected areas

### 2. Classify document roles
- Assign each active doc one primary role where possible:
  - entrance
  - overview
  - policy
  - architecture
  - development
  - roadmap
  - specialized reference
  - tracking or logs
- If a file cannot be summarized in one short ownership statement, treat it as mixed-purpose.
- Keep a compact working table during the pass:
  - file
  - role
  - owner level
  - current problems
  - planned action
- Reuse this same shape in the reported doc-role map when the user expects a full output.

### 3. Detect contract failures
- Look for:
  - duplicated setup steps
  - duplicated repository descriptions
  - repeated rules across layers
  - vague catch-all summary docs
  - entrance docs carrying deep implementation detail
  - missing cross-links that make context hard to follow
  - multiple AI entrance docs drifting apart
  - stale docs-map or overview pointers
  - stable docs collecting temporary tactical notes

### 3a. Detect drift explicitly
- Record drift as one or more of:
  - duplicated rule drift
  - entrance drift
  - stale cross-link drift
  - mixed-purpose regrowth
  - misplaced local guidance
- Treat drift detection as a first-class output, not just an internal thought.

### 3b. Assign lightweight severity
- Use a small severity model only for prioritization:
  - `critical`
    - entrance drift
    - ownership conflict between durable docs
  - `high`
    - duplicated durable rules
    - strongly mixed-purpose docs blocking navigation
  - `medium`
    - local duplication
    - stale docs-map pointers
    - misplaced package or subsystem guidance
  - `low`
    - minor naming cleanup
    - non-blocking cross-link gaps
- Use severity to decide what to address first, not to create a heavy scoring system.

### 4. Choose the owning layer
- Move generalizable guidance upward.
- Move package-specific, feature-specific, or tightly local guidance downward.
- Keep one durable owner for each recurring fact or rule.
- Preserve useful preexisting content by relocating or merging it into the right owner.
- When guidance is tightly local to one package, module, or subsystem, prefer placing it near that owner instead of centralizing it artificially.

### 4a. Assign decision confidence
- `high`
  - ownership is clear
  - duplication is obvious
  - change can be applied directly
- `medium`
  - preferred structure is clear enough to apply
  - leave a short note about the judgment
- `low`
  - multiple structures are plausible
  - suggest the change instead of applying it
- Use confidence to decide whether to apply, apply-with-note, or suggest-only.

## Entrance-Doc Handling

### Single entrance doc
- Keep it short and map-like.
- It should point to deeper docs rather than reteach them.

### Multiple AI entrance docs
- When `AGENTS.md`, `CLAUDE.md`, or similar files coexist, align them before editing them independently.
- Keep their ownership model coherent:
  - entrance files route
  - deeper docs own detail
- Do not casually let separate AI entry docs accumulate different versions of the same durable guidance.
- Check whether overview docs or documentation maps should also be updated so the entrance layer is discoverable as a set rather than through one outdated pointer.
- Make entrance governance explicit:
  - entrance docs should not compete for durable rule ownership
  - overview/docs-map files should reflect the entrance layer accurately
  - contributor-facing and model-facing entrance files may differ in tone, but not in ownership boundaries

## Restructure Boundaries

### Apply directly
- removing clear duplication
- rewriting for ownership clarity
- tightening entrance docs
- adding useful cross-links
- re-homing existing useful content

### Suggest first, then wait for approval
- splitting one doc into several new docs when that split is helpful but optional
- introducing a broader new folder hierarchy
- larger reorganizations that materially change navigation patterns

### Do not touch without explicit reason
- stable docs that already have clear ownership
- specialized areas the user marked as deferred
- package-local guidance that is already near its real owner and not causing duplication

## Writing Standard
- Keep each file clean and readable.
- Make each file descriptively clear about why it exists.
- Prefer linked layers over repeated prose.
- Keep filenames and placement aligned with ownership and navigability.
- Prefer the minimum effective restructuring.
- Do not refactor already-readable, stable docs only for aesthetic neatness.

## Change Tracking
- Track the pass explicitly as `before -> after`.
- Record:
  - operating mode used
  - severity summary
  - structure changes
  - ownership changes
  - moved content
  - removed duplication
  - cross-link additions
  - suggested-only restructures
  - decision confidence by change
  - unresolved low-confidence items
- Prefer concise, reviewable summaries over vague statements like "cleaned docs."

## Finish Pass
- Check the result with [checklist.md](checklist.md).
- Confirm that the tree is cleaner and easier to maintain than before.
- If no comparable rerun exists yet, treat the refinement as improved but not fully rerun-validated.
