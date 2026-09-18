# Method

Use this file for the full document-structuring procedure.

## Contents

- [Purpose](#purpose)
- [Review Scope And Evidence Reuse](#review-scope-and-evidence-reuse)
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

## Review Scope And Evidence Reuse

### Select the starting scope
- Resolve the target from the active request and conversation, including named knowledge bases outside the working repository. The current directory is not automatically the documentation owner.
- For document-set maintenance, first orient to the set as a whole using its entrances, ownership map, and available structural history. Growth, accumulated notes, uncertain coverage, or the task's cross-document purpose can justify a whole-target review from the outset; a known contradiction is not a prerequisite.
- For routine end-of-task reconciliation, derive changed facts, decisions, statuses, and files from available task evidence. Use a diff when useful, but support non-Git targets and changes that have not yet reached a document. Do not require the user to prepare a scope packet.
- When evidence supports a bounded impact, start with affected owners, their entrance or overview pointers, and searches for references to changed claims. This focused path is an option, not a required stage before broader review. Use inventories and searches to guide reading, not to exclude content needed to understand the whole.
- When no trustworthy change baseline exists, discover the target's active owners and check for drift more broadly. Do not assume that unmentioned documents are stable.
- An explicit whole-target audit requires whole-target coverage of the requested properties. Exhaustive semantic review requires reading the relevant content, not sampling and calling it complete. Respect exclusions and existing authorization boundaries.

### Expand according to evidence
- Read enough surrounding content and authoritative sources to establish ownership, unique constraints, and whether a status is current or historical. A matching line or changed hunk alone may be insufficient.
- Expand when ownership is unclear, claims conflict, links are stale, a shared rule affects other consumers, or initial evidence cannot support the requested conclusion. These are examples, not an exhaustive permission list: broad exploration may be needed to discover problems not yet known. Follow affected references transitively as needed; do not stop at an arbitrary one-hop boundary.
- Do not require a new user prompt or add an approval gate merely to widen review within the selected target. Existing access permissions and edit approval boundaries still apply.
- Use existing mechanical checks for properties they can establish, such as link targets or generated indexes. Distinguish those results from semantic review; samples cannot establish correctness of all unexamined content.
- Ground factual or status corrections in authoritative task evidence. Preserve historical context and unresolved disagreements; recency or file modification time alone does not establish truth. If broader fact reconciliation is the main task, make that boundary explicit instead of treating structural review as proof that every fact is current.

### Reuse preparation, preserve judgment
- Reuse already-read, unchanged instructions and source content, inventories, source locators, and check results within the same task. Recheck their target, revision or content, and coverage when freshness is uncertain; do not invent a persistent cache or audit ledger.
- Before an authorized delegation, derive a compact handoff from the current work: resolved target, requested coverage, changed facts with source locators, and reusable checks. Prefer this to forwarding full session history; do not ask the user to assemble it or create another agent merely to prepare it.
- When paired or delegated reviews are already authorized, share neutral discovery evidence and changed-fact context when available. Each reviewer still checks the decisive source passages and applies its own lens; another reviewer's conclusion is a lead, not verification. Keep explicitly requested independent discovery independent.
- On a follow-up, recheck the changed findings, affected passages, and dependent references against the last reviewed state. Restart broader discovery when that baseline is stale or new evidence expands the impact, not merely because the skill was invoked again.

### Finish at the evidence boundary
- Stop when requested coverage is met, material findings are resolved or explicitly withheld/unresolved under the existing gates, and affected links and ownership have been checked. An unchanged result is valid.
- If coverage cannot be completed, report the specific gap; do not silently narrow the task or describe unreviewed material as verified or stable. Keep evidence notes in the session unless an existing owner or user request requires an artifact.

## Working Sequence

### 1. Audit the active docs
- Apply the scope procedure above; use the relevant entrance docs and owners as starting points, not an automatic whole-repository body read.
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
- Assign each doc in the review scope one primary role where possible:
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
  - target, scope basis, and coverage (content-reviewed, mechanically checked, or only inventoried)
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
- Expand the role map and change categories only when useful; a bounded or unchanged pass does not need the full report template or a catalog of untouched files.

## Finish Pass
- Check the result with [checklist.md](checklist.md).
- Confirm that necessary fixes improved maintainability, or explain why the reviewed structure was left unchanged.
- If no comparable rerun exists yet, treat the refinement as improved but not fully rerun-validated.
