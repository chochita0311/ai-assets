# Skill Quality Guide

## Purpose
- Define what makes a good skill in this repo.
- Keep skill quality standards reusable across domains, not tied to one project.
- Support both direct human use and future harness-style automation.

## What A Good Skill Is
- A good skill is not just a smart prompt.
- A good skill is a reusable contract that:
  - triggers for the right kind of problem
  - produces the right output shape
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

### 3. Clean File-Role Separation
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

### 4. Durable vs Temporary Separation
- Durable guidance should live in the skill package or owned docs.
- Temporary comparison artifacts, experiments, or rerun evidence should stay temporary unless the user explicitly asks to keep them.
- Skills should not create by-product docs by default.

### 5. Evaluator-Friendly Outputs
- Another agent or future pass should be able to judge the output from the files themselves.
- Outputs should not depend on hidden explanation from the original drafting run.
- If pass/fail cannot be judged without guessing, the skill contract is too soft.

### 6. Source Priority And Reconciliation
- If the skill consumes several input sources, it should define source priority or reconciliation rules.
- Higher-priority sources should not be silently overridden by lower-priority ones.
- Contradictions should be resolved explicitly rather than blended together invisibly.

### 7. Reusable Generalization
- Prefer rules that generalize across repos and domains.
- Concrete examples are useful, but they should support the rule rather than replace it.
- A skill should not become overfit to one repo unless it is intentionally repo-local.

### 8. Harness-Ready Expansion
- Good skills should be usable:
  - by one agent end-to-end
  - by a drafting agent plus an evaluator
  - inside a rerun or harness loop later
- This does not mean every skill must always run in multiple parts.
- It means the contract should be strong enough that role separation is possible when needed.

## Common Failure Patterns
- `SKILL.md` reteaches the full method instead of staying at contract level.
- `references/checklist.md` becomes a second method document.
- Outputs mix durable rules with temporary tactics.
- File names or output paths drift from what the skill promises.
- The skill creates weak by-product docs that no one owns later.
- Evaluation depends on verbal explanation rather than self-contained artifacts.
- Multi-source input is used without source-priority rules.

## Review Questions
- Can I summarize the skill's trigger in one short sentence?
- Does each file in the package have one clear job?
- Would a second agent know how to evaluate the output?
- Would the same skill still make sense on another repo of the same class?
- Are temporary outputs clearly temporary?
- Does the skill reduce drift rather than adding more prose?

## Good Direction For Harness Engineering
- Prefer pass/fail validation criteria over soft “looks good” guidance when possible.
- Prefer outputs that are checkable from files rather than from conversation memory.
- Prefer explicit source priority when multiple artifacts or docs are involved.
- Prefer owned docs and stable templates over one-off generated notes.
- Strengthen contracts incrementally from real runs instead of front-loading abstract complexity.

## Practical Summary
- A good skill is reusable.
- A better skill is reusable and checkable.
- The best skills in this repo should be reusable, checkable, and easy to refine from real evidence.
