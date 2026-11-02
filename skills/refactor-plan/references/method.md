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
- Keep detailed reusable review and validation guidance in this method, final yes-or-no checks in [checklist.md](checklist.md), and ticket-specific phase definitions in the active plan.
- Good phase definitions usually separate by one or more of:
  - blast radius
  - dependency ordering
  - runtime criticality
  - validation method
  - ownership boundary
- Avoid phase definitions that are only chronological and say nothing about risk or review strategy.

## 4) Review for Behavior Parity

### 4.0 Freeze the Comparison and Review Allowance

- Record the requested baseline reference and resolve the actual current branch, tag, or release to an immutable revision. Recheck a requested moving reference at close; report any change and reconcile affected evidence before using it for a current-reference claim.
- Freeze the candidate separately: use a full commit SHA or an immutable uncommitted bundle with a complete path/content-hash manifest, including additions, removals, and relevant untracked inputs. Do not invent a head SHA or create a commit just for review. Keep a frozen PR review scoped to its commits rather than adding dirty working-tree changes.
- For each side, record dependency, configuration, and environment identities and the applicable guidance's source/provenance, revision, and content fingerprint. Record observation time, access limits, and reproduction locators. Keep unknown or unavailable inputs explicit. Candidate guidance edits do not authorize new exclusions or relaxed gates; resolve authority under the existing task contract.
- Before review, identify actual caller or environment hard deadlines and time, tool-use, cost, or attempt ceilings, with their source, scope, and observability; do not invent a cap. Apply each limit to its constrained action, resource, or whole task: stop before breaching it, while continuing other useful permitted work, including analysis of existing evidence, within remaining limits. Declare completion/stop criteria and a separate finite, risk-appropriate planning allowance and reassessment point, accounting for integration, verification, and cleanup capacity.
- Treat agent-set allowances as revisable checkpoints, not automatic whole-task stops or failed-quality criteria. A critic may challenge their adequacy; the primary may revise the plan within existing scope, authority, and actual limits without another user approval solely to change its own estimate. Record the new information or unresolved concern, expected information gain, rationale, revised allocation, and outstanding commitments; do not silently extend it or impose a universal round count.
- Carry cumulative observed usage, spent attempts, stale or interrupted snapshots, unresolved concerns, outstanding commitments, remaining actual capacity, and the current and remaining planning allowance across changed inputs and resumed sessions. A changed snapshot or revised plan does not reset consumption. Mark unobservable usage or capacity as unknown rather than inventing it.
- Keep the primary responsible for user intent, requirements, skill selection, scope, architecture, source authority, security, permissions, persistence, integration, and final acceptance. A review record does not authorize implementation, external publication, or merge.

### 4.1 Trace Critical Paths End to End

- Trace each important operation from entry through orchestration, query/write, and payload/output to terminal consumers. Include relevant callers, registration/wiring, startup/shutdown, generated code and copied historical artifacts, batch/helpers, and fallback/recovery paths. Changed files and the existing test list alone do not define the full affected flow.
- Compare old and new call order and identify:
  - removed steps
  - reordered steps
  - newly introduced branches
- For every material path, record old/new source locators, the contract or branch compared, a concrete witness, review method, result, and any unaudited reason. Retain distinct paths even when they share a cause.

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
- Compare actual value types, null/blank cases, exact predicates, and distinguishing boundary combinations at logic-unit level. Include applicable storage/state combinations such as memory/disk and fresh/existing targets.
- Inspect the actual old and new dependency implementations and configuration branches reached by the application. An unchanged call name or application body does not establish equivalent library behavior; unavailable dependency evidence leaves the affected conclusion provisional.

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
- Candidate identity and both sides' dependency/configuration/environment and guidance evidence satisfy [4.0](#40-freeze-the-comparison-and-review-allowance).
- Old-to-new source mapping is complete for affected flow:
  - entrypoint
  - orchestration/service path
  - repository/query path
  - payload builder/output writer path
  - terminal consumers and the relevant lifecycle, generated/historical, helper, and recovery paths in [4.1](#41-trace-critical-paths-end-to-end)
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

### 4.8 Obtain an Independent Omission Challenge

- Before a high-risk refactor completion or parity judgment, assess the need for an independent omission challenge without waiting for another user prompt. Triggers include large structural or control-flow changes, framework/dependency migrations, behavior removal, auth/security, data integrity/transactions, concurrency, and multiple consumers. Obtain a fresh challenge when an authorized, competent reviewer is available within actual limits and the current or justifiably revised plan. Keep routine low-risk work proportional and record the risk decision and any required independence gap.
- Honor applicable delegation admission and named-worker requirements. Without a harness or adapter, use any permitted competent execution of this bounded code-review brief. Do not substitute a narrow evidence scout or command runner for semantic review, or silently replace an explicitly requested worker. If no eligible fresh reviewer is available, continue useful primary analysis and report the resulting acceptance limit; self-review cannot satisfy required independence.
- Supply full task constraints, frozen baseline/candidate raw code and diff, surrounding code, contracts, relevant callers/terminal consumers, tests, available validation, and review-instruction provenance, revision, fingerprint, and limits. Distinguish actual resource caps and their sources, the planning allowance, and the assignment's return conditions. Withhold author reasoning, favored conclusions, expected findings, and prior candidate lists from initial discovery. Do not hide necessary facts to manufacture independence.
- Preserve the initial discovery return before sharing arguments for an informed dispute stage. Record actual reviewer/history exposure, instructions, tools and permissions, and unknown runtime fields. Keep author-context, method, source-lineage, and validation-data independence distinct; repeated sources or reused fixtures are not new independent evidence. Role labels or different models alone establish neither independence nor an OS sandbox.
- Keep the challenge non-editing and non-executing: no source/runtime mutation, reviewed-code or build/test execution, dependency installation, GitHub feedback, acceptance decisions, or further delegation. A reviewer, including an available `review_challenger`, returns bounded validation requests to the primary or an authorized capable validator when execution evidence is needed.
- Require the return to identify inspected scope, callers and terminal consumers, candidates, guidance provenance, context-independence limits, coverage/validation gaps, and observed usage and remaining capacity. A candidate is evidence for adjudication, not a decision. The worker returns at its assigned boundary; that return does not settle overall coverage or acceptance, which the primary must reassess.

### 4.9 Adjudicate Candidates Against Evidence

- For each candidate, require a concrete trigger, reachability, baseline and candidate behavior, causal location/delta, impact, supporting and counterevidence, severity, and confidence under the active review contract. Preserve that contract's delta eligibility and causality criteria rather than importing another review system's thresholds.
- Separate new regression, pre-existing defect, authorized intentional delta, and unproven concern. Inspect plausible adjacent occurrences of a supported cause, with separate evidence for each path. Deduplicate repeated claims without losing distinct triggers, causal paths, or impacts; neither agreement nor finding count establishes correctness.
- Keep claim status (`supported`, `refuted`, `unresolved`) separate from action (`fixed`, `accepted intentional delta`, `retained`, `deferred`). Record source locators, observation/state identities, arguments, counterevidence, decision reason, and remaining uncertainty, including rejected or deferred objections.
- Prefer discriminating tests, differential execution, source reproduction, or measurement where permitted. Validate fixture inputs, expected values/oracle, and environment equivalence before treating a differential failure as a regression; an invalid fixture is not a reason to change product behavior.
- For a significant disputed or high-impact claim, or a conflict from adjudicating one's own decision, obtain a separate competent informed adjudicator or objective discriminating validation when needed. Do not assign a judge to every small issue. Preserve unresolved limits if that evidence is unavailable; adjudicator output does not expand authority or replace the primary's final responsibility.

### 4.10 Reconcile Repairs and Stop Within Scope

- After an authorized repair, inspect both baseline -> current candidate across the whole reviewed scope and previously reviewed candidate -> current candidate. Repair confirmation is not automatically fresh omission discovery; label each stage honestly.
- Invalidate affected witnesses when code, callers/terminal consumers, contracts, dependency/configuration/environment, guidance, or assumptions change. Rebuild the affected evidence rather than reusing a stale pass. Preserve prior claim status, actions, and unresolved issues; zero new candidates does not erase them.
- Start substantive follow-up only for new evidence, a question/path, changed input or repair, or a concrete unresolved concern. Before another pass, name the material decision it could change, the new information it could supply, and its estimated cost within actual limits; reassess the planning allowance when needed. Do not repeat the same evidence and method merely to obtain agreement.
- Stop when the declared scope and evidence gates are satisfied. Continue useful, authorized work that can resolve material gaps when a limit blocks only one action or resource. Return an explicitly partial result when evidence, required independence, or material objections cannot be resolved with available means, or when actual limits, scope, or authority prevent further useful authorized work, including at a whole-task deadline. Keep the resource stop, unmet acceptance conditions, and quality verdict distinct. Exhaustion and repeated rereading are not acceptance; no loop must continue until “spotless.”
- Keep claims scoped to audited contracts and observed checks. Report drift immediately and revise prior parity claims; explicitly retract and correct a contradicted safety or preservation statement. Record the next bounded check and resume condition for remaining work without silently expanding the task.

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
- Build, targeted tests, wiring, startup, and runtime checks establish only their checked scope. Record skipped checks and their acceptance impact; a pass does not replace strict coverage, required independence, or unresolved material objections.

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
