# Skill Quality Guide

## Purpose
- Define what makes a good skill in this repo.
- Keep skill quality standards reusable across domains, not tied to one project.
- Support both direct human use and future harness-style automation.
- Keep skill contracts strong enough that real runs do not drift into adjacent work by habit.
- Act as the standing reference when a skill is added, updated, or refined in this repository.

## How To Use This Guide
- Read this before adding a new skill package under `skills/`.
- Read this before materially changing an existing `SKILL.md`, `references/`, or `templates/` package shape.
- Use this as the first review lens when deciding whether a proposed skill change should strengthen a contract, split responsibilities, or stay out of scope.
- Update this guide when repeated skill work exposes a missing quality criterion that should apply beyond one package.
- Prefer changing this guide only for reusable standards, not to record one-off preferences from a single skill.

## What A Good Skill Is
- A good skill is not just a smart prompt.
- A good skill is a reusable contract that:
  - triggers for the right kind of problem
  - produces the right output shape
  - makes authority, scope, and stopping points explicit
  - keeps file roles distinct
  - can be evaluated without guesswork

## Core Quality Criteria

### 1. Clear Trigger Boundary
- `SKILL.md` should make it obvious when the skill should be used and when it should not.
- Invocation examples should match realistic user asks.
- The skill should not trigger on every vaguely related task.

### 2. Strong Output Contract
- The skill should define what it creates or updates.
- Output location should be explicit when the repository convention is predictable.
- Stable outputs and temporary outputs should not be mixed casually.
- If multiple outputs are possible, the primary artifact versus derived views should be explicit.

### 3. Clear Operating Modes When Needed
- If a skill supports materially different operating modes, the modes should be explicit and easy to choose.
- Modes should be based on input state or task type, not on arbitrary naming churn.
- If one mode is the normal case, the default should be stated clearly.

### 4. Clear Authority And Source Priority
- If the skill consumes multiple inputs, it should define which source wins when they disagree.
- Authority order should be easy to restate from the package without opening several files.
- If the skill allows inference, it should be clear when inference is allowed and when it is too risky.

### 5. Clean File-Role Separation
- `SKILL.md` owns:
  - trigger scope
  - workflow summary
  - output expectations
  - package boundaries
- `references/method.md` owns:
  - detailed procedure
  - decision logic
  - conflict resolution
  - failure diagnosis
- `references/checklist.md` owns:
  - the shortest possible final validation pass
- `templates/` own output scaffolds, not method explanation.

### 6. Durable vs Temporary Separation
- Durable guidance should live in the skill package or owned docs.
- Temporary comparison artifacts, experiments, or rerun evidence should stay temporary unless the user explicitly asks to keep them.
- Skills should not create by-product docs by default.

### 7. Evaluator-Friendly Outputs
- Another agent or future pass should be able to judge the output from the files themselves.
- Outputs should not depend on hidden explanation from the original drafting run.
- If pass/fail cannot be judged without guessing, the skill contract is too soft.

### 8. Intervention And Approval Boundaries
- A good skill should make it clear whether it acts immediately, asks first, or stops for approval at specific boundaries.
- Optional or high-churn restructures should be suggested before they are applied when user approval matters.
- The skill should define when to leave stable material unchanged instead of optimizing it anyway.

### 9. Reusable Generalization
- Prefer rules that generalize across repos and domains.
- Concrete examples are useful, but they should support the rule rather than replace it.
- A skill should not become overfit to one repo unless it is intentionally repo-local.

### 10. Output Lifecycle And Handoff
- A good skill should define where its job ends.
- If the output often leads to a downstream artifact, that next step should be named without being silently folded into the current skill.
- Handoffs to adjacent skills should be explicit when boundary confusion is likely.
- References to adjacent skills should stay optional and boundary-oriented rather than reading like hard dependencies unless the integration is truly mandatory.

### 11. Harness-Ready Expansion
- Good skills should be usable:
  - by one agent end-to-end
  - by a drafting agent plus an evaluator
  - inside a rerun or harness loop later
- This does not mean every skill must always run in multiple parts.
- It means the contract should be strong enough that role separation is possible when needed.

## When To Update This Guide
- Update this guide when a real skill run reveals a reusable contract gap that affects more than one skill.
- Update this guide when several skills independently converge on the same new boundary, output rule, or evaluation rule.
- Do not update this guide just to mirror one package's local wording.
- If a finding applies only to one skill, prefer recording it in that skill package or in [skill-followups.md](skill-followups.md).

## What This Guide Should Not Become
- not a catalog of every current skill package
- not a second `AGENTS.md`
- not a temporary run log
- not a place to restate package-local method details
- not a replacement for `skill-followups.md`

## Maintenance Bias
- Prefer strengthening existing criteria over adding parallel categories that say nearly the same thing.
- Prefer adding one reusable rule after repeated evidence instead of front-loading speculative governance.
- When a new criterion is added, make sure it can be checked from skill files or realistic outputs rather than conversation memory alone.

## Common Failure Patterns
- `SKILL.md` reteaches the full method instead of staying at contract level.
- `references/checklist.md` becomes a second method document.
- Outputs mix durable rules with temporary tactics.
- File names or output paths drift from what the skill promises.
- The skill creates weak by-product docs that no one owns later.
- Evaluation depends on verbal explanation rather than self-contained artifacts.
- Multi-source input is used without source-priority rules.
- The skill silently expands into adjacent work such as planning, specification, or restructuring beyond its stated boundary.
- The skill references another skill as if that other skill were a required dependency rather than an optional better fit for a neighboring problem.
- Several modes exist, but no one can tell which mode is the default or why one mode should be chosen.
- Derived outputs appear, but the package never clarifies whether they replace the primary artifact or sit on top of it.
- High-churn changes are applied automatically even when stable areas could have been left alone.

## Review Questions
- Can I summarize the skill's trigger in one short sentence?
- Does each file in the package have one clear job?
- Would a second agent know how to evaluate the output?
- Would the same skill still make sense on another repo of the same class?
- Are temporary outputs clearly temporary?
- Does the skill reduce drift rather than adding more prose?
- Does the skill define its stopping point clearly enough that downstream work is not implied?
- If the skill has modes or multiple outputs, are default behavior and artifact roles obvious?

## Good Direction For Harness Engineering
- Prefer pass/fail validation criteria over soft “looks good” guidance when possible.
- Prefer outputs that are checkable from files rather than from conversation memory.
- Prefer explicit source priority when multiple artifacts or docs are involved.
- Prefer explicit default modes and stopping points when a skill can easily sprawl.
- Prefer owned docs and stable templates over one-off generated notes.
- Strengthen contracts incrementally from real runs instead of front-loading abstract complexity.

## Practical Summary
- A good skill is reusable.
- A better skill is reusable and checkable.
- The best skills in this repo should be reusable, checkable, bounded, and easy to refine from real evidence.
