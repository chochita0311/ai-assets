# Refine Skill

## Contents

- [Resolve The Target And Authority](#resolve-the-target-and-authority)
- [Establish The Baseline](#establish-the-baseline)
- [Define Success For The Target Skill](#define-success-for-the-target-skill)
- [Diagnose Before Choosing A Fix](#diagnose-before-choosing-a-fix)
- [Refine The Actual Owner](#refine-the-actual-owner)
- [Validate And Compare](#validate-and-compare)
- [Stop And Report](#stop-and-report)

## Resolve The Target And Authority

- Identify the existing target skill, its intended job, the requested mode, and the authorized change scope. Use prior authorization that still applies; do not introduce another approval step for routine in-scope corrections.
- Resolve the canonical package before editing. Distinguish repository source, installed copies, symlinks, and instructions already loaded in a running session. If the source is unresolved, continue diagnosis but resolve the ownership before choosing an edit target.
- Derive intended behavior from the user's request and applicable higher-priority instructions, then the target's compatible contract. Use observed runs to establish what happened. Treat previous evaluations and external best practices as supporting evidence, not authority to redefine the user's goal.
- Keep surrounding workflow rules with their owner. Publication, transport selection, and repository-wide policy do not automatically belong in a skill that produces content.

## Establish The Baseline

- Name the package revision or snapshot and the best available `v1` task evidence before edits. A formal version folder is unnecessary; one prior realistic run is a usable starting point.
- Collect the smallest evidence set that explains the failure and includes relevant successful or contradictory cases. Prefer original outputs, tool results, and user corrections over a prior agent's summary alone.
- When reviewing sessions, distinguish a skill name in a catalog or inherited conversation from actual loading and execution. Do not count parent and child copies of the same event as independent runs.
- Record the task input, expected behavior, observed result, evidence location, and known execution conditions. Mark unavailable details instead of reconstructing them from assumptions.

| Available evidence | Supported conclusion | Limit |
| --- | --- | --- |
| Current package or package diff | A visible static defect or a static correction | No claim about actual task performance |
| Realistic task output and execution trace | Observed success or failure under those conditions | One run does not establish stability or its cause |
| Fresh, answer-isolated producer execution with the intended revision loaded | Forward-test of that task | A different task or materially different environment may not support a before/after claim |
| Comparable execution after a revision | Whether the observed failure recurs and controls still pass | Generalization remains bounded by the cases and conditions tested |

For self-refinement, the current package may be `v1` and the edited package `v2` for static comparison. A behavioral test still requires an actual audit or refinement task performed with the skill. Missing execution evidence limits the conclusion; it does not forbid a useful static audit or an authorized correction of a visible defect.

## Define Success For The Target Skill

Choose a small set of observable must-pass checks before changing the contract. Start with the target skill's purpose. Apply the relevant dimensions below and briefly justify exclusions; do not turn them into a universal numerical score.

| Dimension | Question to make observable |
| --- | --- |
| Task outcome | Did the requested job complete correctly and usefully, including authorized actions? |
| Discovery | Does the description select realistic intended requests and reject nearby out-of-scope requests? |
| Evidence quality | Are factual claims, omissions, uncertainty, and conclusions supported by the available inputs? |
| Authority and process | Does execution respect the requested scope without unauthorized action or unnecessary refusal and reconfirmation? |
| Preservation and structure | Are successful behavior, meaning, examples, and constraints preserved, with appropriate output and file roles? |
| Efficiency | Does the task finish with proportionate exploration, intervention, time, and context use? |

Tie each check to an expected result and observable evidence. For example, a review skill should recover a supported defect while rejecting an unsupported one; a reshaping skill should preserve meaning while completing justified edits. Correct filenames or a stable outline cannot establish either outcome.

Include controls that could disprove the proposed improvement. A restriction must preserve the corresponding authorized success path; a detection improvement must not invent findings in a valid zero-result case. When discovery changes, cover explicit, implicit, and negative invocation cases.

## Diagnose Before Choosing A Fix

For each material mismatch, connect expected behavior, observed behavior, evidence, likely cause, and owner. Use the distinctions below to choose the next action rather than assuming every poor output needs more instructions.

| Likely cause | Evidence to seek | Disposition |
| --- | --- | --- |
| Skill contract or resource | Missing or conflicting guidance, misleading examples, inaccessible required references, incorrect bundled behavior | Correct the owning instruction or resource and validate affected consumers |
| Model or execution | Intended revision was loaded, but a clear rule was skipped or results vary under comparable conditions | Record the execution gap; test a specific guidance or execution hypothesis before adding rules |
| Tool or environment | Dependency, API, permission, configuration, or runtime failure | Fix only an in-scope skill-owned resource; otherwise identify the external owner or validation gap |
| Input or evidence | Stale snapshot, unavailable material, contradictory inputs, or unsupported inference | Correct the evidence basis or narrow the conclusion; do not invent facts or constraints |
| Surrounding workflow | Behavior came from user instructions, harness policy, or an adjacent task | Keep that rule with its owner and report the handoff rather than silently expanding the skill |

Causes can be mixed. State uncertainty and choose a bounded check that distinguishes plausible causes. An explicit rule does not prove the skill is adequate, and one model failure does not prove the rule is defective. Leave the package unchanged when evidence does not justify a correction.

## Refine The Actual Owner

In `audit`, return the diagnosis and proposed owner without editing the target. In `refine`, apply authorized corrections:

- Put discovery, scope, mode selection, essential workflow, and response expectations in the target's `SKILL.md`.
- Put detailed decisions in the reference that actually owns them, using its existing domain-specific filename.
- Fix misleading examples or templates where the output pattern is defined. Fix bundled implementation defects in the script and its relevant tests. Align existing metadata when the entry contract changes.
- Keep each rule authoritative in one place; update coupled consumers without repeating the full rule everywhere. Do not require the target to have this skill's `method.md` and `checklist.md` layout.
- Preserve core purpose, essential content, and working behavior. Clarify or relocate misplaced content rather than deleting it merely to shorten the package. Leave stable areas alone.

Prefer a narrow correction supported by the evidence. Do not convert one local preference or incident into a universal requirement, or turn refinement into general rewriting of the target's domain artifacts.

## Validate And Compare

### Static And Resource Checks

Run applicable package validation, frontmatter and naming checks, relative links and referenced files, metadata alignment, and named dependency checks. Exercise changed scripts, parsers, and templates with representative inputs when applicable. These checks establish package or resource correctness, not agent behavior.

Check installation differences only for relevant targets. Sync only within existing authorization, compare the intended source and target, and account for cached instructions in running sessions when selecting behavioral evidence.

### Behavioral Comparison

Select a bounded case set and a proportionate stopping point before launching tests. Use the observed failure, relevant successful controls, and a materially different case when broader reliability is claimed. Reuse safe local fixtures where possible; validation does not authorize live publication or other domain side effects.

For a comparable run:

1. Identify the old and new skill revisions, task input or snapshot, success checks, and relevant tools, model, and execution settings. Keep conditions comparable; record differences and limit attribution when they could explain the result.
2. Execute the target skill as an ordinary user task with raw task artifacts. Give the producer necessary task evidence, but withhold the evaluation answer key, proposed fix, and prior authoring conclusions. Historical outputs remain valid inputs when auditing them is the task itself.
3. Use a fresh producer context when available and permitted, especially for substantial or fragile changes. Isolate prior generated outputs so the producer cannot copy them. A separate evaluator can assess outputs but does not turn an author-guided run into an independent forward-test. If only the author can perform the task, label it an author check.
4. Capture the actual output and relevant actions, errors, interventions, and completion evidence. Compare must-pass checks directly against `v1`, including any regression in successful behavior. Record time or tool usage when efficiency is at issue; do not infer unmeasured savings.
5. Treat a later pass as comparable rerun evidence only when it executes the revised target on the same task class and tests the same failure. Re-reading files, changing instructions, or reviewing an existing output is not a behavioral rerun of that target. For `refine-skill` itself, the executed task must produce an audit or refinement result.

Do not make multiple agents or a large benchmark mandatory. Scale repeated runs to risk and observed variance. Where controls, versions, or context isolation are unavailable, report the limitation instead of presenting an assisted result as a controlled improvement.

## Stop And Report

- Finish an audit when its declared checks and evidence review are complete, even if the conclusion recommends changes or no change.
- Finish an authorized refinement when the bounded corrections and applicable checks are complete. If behavior has not been rerun, say that the package changed but behavioral improvement remains unverified.
- Claim stability only for the observed scope: comparable runs no longer show the original failure, relevant successful and authorized-action controls still pass, and material intervention or environment differences are accounted for. One better-looking version or one successful run is insufficient.
- Stop expanding the loop when only optional polish remains. If failures persist, the agreed test boundary is reached, or additional evidence is unavailable, report unresolved failures and the next discriminating check; do not keep adding rules or declare stability to close the task.

Report `Result` for the criteria actually checked and `Evidence Coverage` against the declared required scenarios and environments. A material failed check is `FAIL`; nonblocking improvements can be `PASS WITH SUGGESTIONS`. A static `PASS` with partial behavioral coverage must not read as overall behavioral acceptance. Name the highest evidence level reached: static validation, resource execution, fresh forward-test, or comparable rerun, qualifying independence and comparability where needed.

Use the entry contract's evidence handling rules to close scratch work. Refer to original evidence or an existing durable follow-up owner when one exists; do not make later work depend on temporary paths or create a permanent report just to demonstrate that refinement occurred.
