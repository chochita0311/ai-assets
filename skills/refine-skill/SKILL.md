---
name: refine-skill
description: Use when an existing skill already has real output evidence and you need to tighten its contract through direct comparison, file-role cleanup, and rerun-aware refinement.
---

# Refine Skill

Use this skill to tighten an existing skill after real runs have exposed weaknesses.

## Definition
- Refinement means making the skill more reliable for its intended purpose by clarifying boundaries, reducing duplication, tightening instructions, and preserving important core content.
- Refinement does not mean deleting essential skill content just to make the package shorter.

## Use This Skill When
- A skill already exists and has real output evidence from a realistic task
- The skill looks organized, but the outputs still drift, duplicate, or blur file roles
- You can point to concrete evidence such as prior outputs, a realistic transcript, or the current package itself when refining the skill against itself
- You want to strengthen the skill itself rather than preserve every by-product
- You need a sharper contract before spending time on wording polish

## Do Not Use This Skill When
- The skill does not exist yet
- There are no real outputs to review
- The only evidence is hypothetical concern rather than an observed run, artifact, or transcript
- The task is only to rename files or polish wording without validating output behavior
- The problem is implementation of the target skill’s domain work rather than the skill contract itself

## Invocation Examples
- `Use $refine-skill to evaluate this skill from its recent outputs, compare v1 and v2, and tighten the skill contract.`
- `Use $refine-skill to review the current skill outputs, identify contract failures, and refine the templates and file-role separation.`
- `Use $refine-skill to rerun and compare this skill across multiple passes until the outputs stabilize.`

## Workflow
1. Read [references/method.md](references/method.md) for the full refinement procedure.
2. Confirm and state the `v1` baseline evidence before changing anything.
3. Compare the baseline against the current pass and isolate concrete contract failures.
4. Fix only the owning file:
   - `SKILL.md` for trigger, scope, package boundaries, and response expectations
   - [references/method.md](references/method.md) for procedure, decision logic, and failure diagnosis
   - [references/checklist.md](references/checklist.md) for the final yes-or-no validation pass
5. Treat the current pass as rerun evidence only when it rechecks the same target skill on a comparable input; otherwise record the validation gap explicitly.
6. Finish with [references/checklist.md](references/checklist.md).

## Output Handling
- Keep temporary comparison outputs under `docs/tmp/` only when needed.
- Use versioned outputs only as evidence for comparison.
- Do not create permanent by-product documents unless the user asked for them.
- Remove `docs/tmp/` after the refinement loop is complete.
- The goal is to keep the strengthened skill, not a pile of by-products.

## Output Expectations
- The refinement result should center on the strengthened skill package itself, not on permanent analysis artifacts.
- The final response should identify the `v1` baseline evidence, the contract failures found, which file owned each fix, and whether rerun evidence exists, is still missing, or is provided by the current pass itself.
- If rerun evidence is missing, say so explicitly instead of implying the skill is fully proven.

## Package Layout
- `references/`
  - `method.md` for the full refinement procedure and evaluation logic
  - `checklist.md` for the quick execution and validation sheet

## Core Rule
- Judge a skill by its repeated output behavior, not by how polished the skill files look in isolation.
- Tighten contracts before polishing wording.
- Refine for the skill's purpose.
- Compare runs directly.
- Prefer clean separation, lower duplication, and more dependable reruns over longer explanations.
- Do not claim refinement is complete without saying what evidence was actually compared.
