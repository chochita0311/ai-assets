# Refactor Planning Method

Use this file for detailed refactor planning, parity analysis, validation design, and merge-scope reasoning.

## Contents

- [Purpose](#purpose)
- [Planning and Organization Rules](#0-planning-and-organization-rules)
- [Define Invariants Up Front](#1-define-invariants-up-front)
- [Classify Diff Scope](#2-classify-diff-scope)
- [Define Phase Semantics Explicitly](#3-define-phase-semantics-explicitly)
- [Review for Behavior Parity](#4-review-for-behavior-parity)
- [Validation Gates](#5-validation-gates)
- [Refactoring Anti-Patterns](#6-refactoring-anti-patterns)
- [Clean Tree and Merge Scope Gate](#7-clean-tree-and-merge-scope-gate)
- [Artifact Selection And Logging](#artifact-selection-and-logging)
- [Output Resource Routing](#output-resource-routing)

## Purpose

- This document owns the detailed procedure and decision logic for `refactor-plan`.
- Use it to classify the work, define invariants, design safe phases, and determine what evidence is required before parity or merge claims.
- Use [checklist.md](checklist.md) only as the final short validation pass.

## 0) Planning and Organization Rules

- Start by deciding whether the work is:
  - a behavior-preserving structural refactor
  - a behavior-affecting fix or redesign
  - an intentional semantic cleanup
- Keep those categories separate in the plan and in review language.
- Choose a plan structure that fits the repository:
  - extend an existing track when scope and risk model remain the same
  - create a new track when goals, risk, or baseline change materially
- Create a new plan when:
  - the goal changes from structural parity to semantic redesign
  - the dominant risk moves to another layer
  - the previous track is complete and the next work needs a new boundary
  - appending would make the existing track ambiguous
- Extend the current plan when:
  - the work is the next batch in the same initiative
  - the baseline, goals, and risk model still apply
  - the file remains readable after the new step or handoff
- Keep each step coherent:
  - one dominant purpose
  - one clear validation story
  - one understandable merge decision
- Prefer boundaries based on blast radius, dependency order, runtime criticality, contract surface, or validation strategy.
- Avoid steps that are only miscellaneous-cleanup buckets.
- Leave handoff notes when work moves to another track.
- Record non-goals so unrelated cleanup does not silently enter the diff.

## 1) Define Invariants Up Front

- Functional invariants:
  - inputs and outputs for key flows
  - required side effects
  - data semantics such as defaults, enum meanings, and state transitions
- Non-functional invariants:
  - transaction scope and rollback expectations
  - performance, locking, latency, and throughput expectations
- Intentional changes:
  - identify any planned breaks from existing invariants
  - mark each as intentional or unintentional

## 2) Classify Diff Scope

- Compare the planned changes and classify each touched area:
  - `Behavioral`: logic, rules, persistence behavior, side effects
  - `Structural`: move, rename, extract, split, inline, reformat
  - `Interface`: signatures, payloads, public contracts, integration boundaries
- Focus review effort on `Behavioral` and `Interface` areas first.
- Call out intentional deltas explicitly, especially:
  - exception type or message changes
  - null-handling strictness changes
  - retry, skip, timeout, concurrency, or transaction changes
  - logging or monitoring changes that affect operations

## 3) Define Phase Semantics Explicitly

- If a refactor uses phases, levels, or batches, define what each one means inside the active plan.
- Do not assume the same level count or severity model carries across different refactor tracks.
- Keep reusable review and validation guidance in the checklist; keep ticket-specific phase definitions in the active plan.
- Good phase definitions usually separate by one or more of:
  - blast radius
  - dependency ordering
  - runtime criticality
  - validation method
  - ownership boundary
- Avoid phase definitions that are only chronological and say nothing about risk or review strategy.

## 4) Review for Behavior Parity

### 4.1 Trace Critical Paths End to End

- Trace each important operation across its full path.
- Compare old and new call order and identify:
  - removed steps
  - reordered steps
  - newly introduced branches

### 4.2 Check Persistence and Write Equivalence

For every changed write path, verify:
- target selection parity:
  - keys, predicates, filters, and null handling
- write parity:
  - fields written, defaults applied, timestamps, actor or source fields
- schema alignment:
  - primary key, unique key, foreign key, and required-constraint assumptions

### 4.3 Check Semantic Rule Drift

- Validate rule changes explicitly:
  - validation conditions
  - default mapping behavior
  - null and blank handling
  - formatting, truncation, normalization, or fallback behavior
- Mark each drift as:
  - intentional and approved
  - unintentional and must fix

### 4.4 Check Transaction and Failure Model

- Compare atomicity model:
  - all-or-nothing versus partial or chunked completion
- Define acceptable failure behavior:
  - rollback, retry, compensation, or partial commit
- Verify idempotency and retry safety where relevant.

### 4.5 Check Side-Effect Parity

- Confirm parity for side effects such as:
  - events or messages
  - audit and history writes
  - cache invalidation
  - notifications
  - security or authorization behavior

### 4.6 Check Data Contracts

- Document the required post-condition rules for affected data.
- Confirm the refactor still produces data consistent with those rules.
- Record any intentional normalization or contract tightening.

### 4.7 Strict Baseline Audit Gate (Required for parity claims)

- Baseline target is explicit:
  - branch, commit, or release compare target is pinned
  - resolved immutable reference (commit SHA) is recorded when available
- Old-to-new source mapping is complete for affected flow:
  - entrypoint
  - orchestration/service path
  - repository/query path
  - payload builder/output writer path
- Query semantics are compared explicitly for each affected query at logic-unit level:
  - join types and join predicates
  - where predicates
  - group/order/limit
  - null/default/filter/status conditions
- Write semantics are compared explicitly for each affected write path:
  - target selection and predicates
  - inserted/updated fields and defaults
  - timestamp/actor/source behavior
- Output semantics are compared explicitly:
  - field-by-field mapping
  - fallback/default behavior
  - dedupe and ordering behavior
- Side-effect semantics are compared explicitly:
  - events/messages
  - audit/history writes
  - cache invalidation
  - notifications
  - security/authorization behavior
- Failure-mode semantics are compared explicitly:
  - exception model
  - retry/rollback/compensation behavior
  - transaction boundary and partial-failure behavior
- If any path was not audited:
  - parity conclusion must be `Unknown` or `Provisional`
  - do not conclude `Preserved`

## 5) Validation Gates

- Build gate:
  - compilation or equivalent static validation succeeds
- Targeted tests:
  - tests cover changed paths and critical contracts
- Wiring and startup checks:
  - run a startup, context-load, registration, or plugin-load smoke check if modules, packages, registrations, or runtime wiring move
- Runtime smoke:
  - run at least one representative runtime path when refactoring touches operationally significant flows
- Full-suite checkpoint:
  - before declaring a phase complete, run the full test suite once on the committed state when practical

## 6) Refactoring Anti-Patterns

Treat these as warning signs that the plan is weak or the change is violating refactoring discipline:

- "Refactor" steps that intentionally change behavior without documenting the delta
- phases with no explicit exit gate
- steps defined only by folder names rather than risk or purpose
- mixing persistence rewrites, contract changes, and broad renames in one batch without justification
- using broad formatting or style churn to mask behavioral edits
- replacing one large opaque module with several new opaque modules without improving ownership or testability
- declaring parity without checking side effects, contracts, and failure behavior
- deleting historical tracking context instead of closing or handing off the track

## 7) Clean Tree and Merge Scope Gate

- Before final parity judgment, confirm no unintended local changes remain.
- Review the exact merge scope against the chosen baseline.
- Do not mix:
  - unfinished later-phase refactors
  - debug-only changes
  - test-only helpers that are not part of the tracked plan
  - unrelated formatting churn

## Artifact Selection And Logging

Choose one artifact role for each output:

- `active plan`: future scope, invariants, planned steps, validation gates, and exit goals
- `refactor log`: completed work, confirmed blockers, runtime evidence, wrap-up, and handoff events
- `merge-check log`: a parity or merge-safety decision against an explicit baseline

Use the active plan as the continuing owner of future work. Write or update it under the repository's established planning convention, defaulting to `./docs/plans/refactoring/` only when no local owner exists.

Use a refactor log when tracked execution changes code or records a meaningful event and no equivalent durable record already owns it.

- Prefer one log per step, batch, blocker, runtime-smoke, wrap-up, or handoff event.
- Keep logs factual and scoped: attempted work, changes, evidence, residual risk, and next action.
- Use a sortable filename such as `YYYY-MM-DD_refactor-xxxx_<event-slug>.md` when the repository has no stronger convention.
- Default to `./docs/plans/refactoring/logs/` only when the repository has no established log location.
- Do not combine unrelated events merely because they occurred on the same day.

Adapt the general log by event:

- `step` or `batch`: record exact scope, compatibility adjustments, and validation
- `blocker`: record the first confirmed blocker, failure evidence, and whether work returned to a stable baseline
- `runtime smoke`: replace change narration with environment, assumptions, checks, observed results, and unverified scope
- `wrap-up` or `handoff`: summarize closure, accepted deltas, deferred work, and the destination track

Use the dedicated merge-check artifact instead of the general log whenever the active question is whether a step, batch, or track is parity-safe, merge-safe, or blocked by missing proof. Do not list `merge check` as a general log type.

For every log:

- prefer scoped facts over narrative
- state reverts, skipped validation, and narrow evidence limits explicitly
- keep the title aligned with the event rather than the whole initiative

## Output Resource Routing

- Use [../templates/plan.md](../templates/plan.md) for the active refactor plan.
- Use [../templates/log.md](../templates/log.md) for step, blocker, runtime-smoke, and wrap-up logs.
- Use [../templates/merge-check.md](../templates/merge-check.md) for exact parity and merge-decision evidence.
- Do not duplicate those output forms inside this method.
