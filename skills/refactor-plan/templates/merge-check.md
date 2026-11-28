# Refactor Merge Check Form

Use this template when recording a merge-safety or parity decision for a defined scope, with or without an active refactor plan.
Select `Preserved` only after completing the [strict baseline audit](../references/method.md#47-strict-baseline-audit-gate-required-for-parity-claims).

## Recommended File Naming

Follow the [log location and naming conventions](../references/method.md#artifact-selection-and-logging). When the repository has no naming convention, the fallback produces names like these:

- `2026-02-24_refactor-0001_level5-7-merge-check.md`
- `2026-02-26_refactor-0003_groupa-merge-check.md`
- `2026-03-18_refactor-0005_final-merge-check.md`

## Canonical Merge Check Template

```md
# [Merge Check Title]

## Merge Assessment

[Give the requested decision for this candidate in the first paragraph. Name any code repair still needed, the next locally answerable question, and the decision awaiting target-environment evidence, where applicable.]

- Safe to merge:
  - `Yes | No | Not yet | Not requested`
- Behavioral parity vs baseline:
  - `Preserved | Intentional deltas present | Known regression | Provisional | Unknown`
  - [If any relevant path is unaudited, select `Unknown` or `Provisional` for overall parity and name any confirmed regression in the opening assessment.]
- Parity confidence basis:
  - `Strict audit complete | Partial audit | Test-only evidence | Runtime-only evidence`
- External contract parity:
  - `Preserved | Intentional deltas present | Known regression | Provisional | Unknown`
- Client-visible change:
  - `No | Yes | Unknown`
- Required fixes before merge, if assessed:
  - `None` or `...`

## Scope

- Related track: `[path/to/existing-plan.md] | None`
- Scope under review:
  - `...`
- Compare baseline:
  - `...`
- Baseline resolved commit SHA (if available):
  - `...`
- Baseline certainty:
  - `Confirmed | Provisional`
- Candidate full commit SHA or immutable bundle/manifest identity:
  - `...`
- Baseline / candidate dependency, configuration, and environment identities:
  - `...`
- Baseline / candidate guidance source, authority, revision, and content fingerprint:
  - `...`
- Observation time, access limits, and evidence locators:
  - `...`
- Requested moving reference rechecked at close, change and reconciliation:
  - `... | Not applicable (fixed reference)`

## Changed Surface

- Added:
  - `...`
- Updated:
  - `...`
- Moved/Renamed:
  - `...`
- Removed:
  - `...`

## Validation Run

- Working tree observation:
  - `Inspected, clean | Inspected, local changes (describe) | Not inspected (reason)`
- Changes outside the intended scope in the frozen candidate (diff or manifest):
  - `None found | Present (list) | Unknown (evidence gap)`
- Build / compile:
  - command: `...`
  - result: `Pass | Fail | Not run`
- Targeted tests:
  - command: `...`
  - result: `Pass | Fail | Not run`
- Full test suite:
  - command: `...`
  - result: `Pass | Fail | Not run`
- Runtime / smoke / manual verification:
  - `...`

## Review Receipt

- Risk and independent-challenge decision:
  - `...`
- Actual hard limits, source/scope/observability, and remaining capacity:
  - `...`
- Current and remaining planning allowance and reassessment point; revised allocation, new information/reason, and outstanding commitments:
  - `...`
- Cumulative observed usage and spent attempts (including stale/interrupted) across inputs/sessions:
  - `...`
- Worker return boundary and remaining overall coverage or acceptance work:
  - `...`
- Review stage and raw packet identity:
  - `Initial discovery | Informed dispute | Repair confirmation | Self-review`
  - `...`
- Reviewer, actual history/instruction exposure, tools/permissions, and unobserved runtime fields:
  - `...`
- Context / method / source-lineage / validation-data independence and limits:
  - `...`
- Initial return and later dispute evidence locators:
  - `...`
- Required independence or execution-validation gaps and acceptance impact:
  - `None | ...`

## Strict Parity Audit Coverage

[Use `Not applicable` only when the reviewed scope contains no such path and give the reason. Mark an unaudited relevant path `No` and record the gap in the path table.]

- Baseline pinned to immutable target (commit SHA):
  - `Yes | No`
- Source mapping complete (old -> new paths):
  - `Yes | No`
- Terminal consumers, lifecycle, generated/historical, helper, and recovery paths covered:
  - `Yes | No | Not applicable with reason`
- Actual types, predicates, boundary combinations, and old/new dependency branches compared:
  - `Yes | No | Not applicable with reason`
- Query semantics audited at logic-unit level:
  - `Yes | No | Not applicable with reason`
- Write semantics audited at logic-unit level:
  - `Yes | No | Not applicable with reason`
- Payload/output mapping audited field-by-field:
  - `Yes | No | Not applicable with reason`
- Side-effect paths audited explicitly:
  - `Yes | No | Not applicable with reason`
- Failure-mode paths audited explicitly:
  - `Yes | No | Not applicable with reason`
- Any unaudited relevant path:
  - `None | ...`

| Material old/new path or logic unit | Contract / branch | Witness and method | Result | Unaudited reason / limit |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |

## Candidate Adjudication

| Candidate | Trigger / reachability | Baseline -> candidate behavior | Causal location / delta / impact | Supporting / counterevidence and fixture validity | Severity / confidence | Category | Claim status | Action / reason / remaining limit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | New regression / Pre-existing defect / Authorized intentional delta / Unproven concern | Supported / Refuted / Unresolved | Fixed / Accepted intentional delta / Retained / Deferred; ... |

- Significant dispute or self-adjudication conflict; informed adjudicator or discriminating validation:
  - `Not needed with reason | ...`

## Changed-Input Reconciliation

- Previous reviewed candidate identity:
  - `... | First review`
- Baseline -> current whole-scope review and previous candidate -> current repair-delta review:
  - `... | Not applicable with reason`
- Changed code, callers/consumers, contracts, dependencies/configuration/environment, guidance, or assumptions; invalidated and renewed witnesses:
  - `None | ...`
- Carried candidate statuses/actions and corrected or retracted earlier claims:
  - `None | ...`

## Parity Proof

- Input contract parity:
  - `...`
- Output contract parity:
  - `...`
- Side-effect parity:
  - `...`
- Failure-mode parity:
  - `...`

## Intentional / Reviewed Deltas

- `None` or `...`

## Residual Risks

- `...`

## Next Action

- `...`
- Stop or return reason, remaining gaps and acceptance impact, next bounded check, and resume condition:
  - `...`
```

## Usage Rules

- Use this template when the main question is “is this scope safe to merge?”
- Do not use this template for every execution event. Use it only when merge safety, parity status, or an explicit go/no-go decision is under review.
- Typical triggers:
  - a planned step or batch is complete and needs a merge decision
  - the user asks whether parity is preserved or whether drift exists
  - tests passed but merge safety is still uncertain because audit coverage is incomplete
  - a branch, PR, or handoff needs an explicit merge judgment before proceeding
- Keep it narrower than a branch diary. Only include the scope under current judgment.
- Treat build and test pass as necessary evidence, not sufficient evidence, for parity.
- If the project's comparison baseline is ambiguous, ask for it when needed; otherwise mark the baseline as provisional and say what assumption was used.
- Internal reordering or code-structure changes are acceptable only if externally observable behavior remains equivalent, unless intentional deltas are explicitly approved.
- If runtime evidence is user-verified or externally observed rather than directly executed, say that explicitly.
- If the full test suite was not run, record that plainly instead of implying broader confidence.
- If the answer is “not yet,” the log should still say what blocks merge and what to do next.
- Apply [the review and claim gates](../references/method.md#4-review-for-behavior-parity) before completing the assessment; this form records their evidence and does not replace the method.
