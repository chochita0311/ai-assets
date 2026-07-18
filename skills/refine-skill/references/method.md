# Refine Skill

## Contents

- [Purpose](#purpose)
- [Core Principle](#core-principle)
- [Acceptable Evidence](#acceptable-evidence)
- [Common Contract Failures](#common-contract-failures)
- [File Ownership During Refinement](#file-ownership-during-refinement)
- [Refinement Cycle](#refinement-cycle)
- [Exit Criterion](#exit-criterion)

## Purpose
- This document owns the full refinement procedure.
- Use it to decide what evidence is valid, how to diagnose failures, which file should be edited, and when the refinement loop can stop.

## Core Principle
- Do not judge a skill by how polished the package looks in isolation.
- Judge it by whether comparable runs produce stable structure, clean file-role separation, and low drift.
- Treat refinement as clarification and contract strengthening for the skill's purpose, not as removal of essential content for the sake of brevity.

## Acceptable Evidence
- Evidence does not need a formal version folder.
- Acceptable `v1` evidence can be:
  - files produced by a prior run
  - multiple saved versions of skill outputs
  - a realistic transcript showing what the skill instructed an agent to do
  - the current skill package itself when the failure is visible in the package structure
- If only one prior realistic run exists, treat that observed behavior as `v1`.
- If you are refining the skill against itself and no older artifacts exist, use the current on-disk package as `v1` and the edited package as `v2`.
- If you are running another refinement pass on the same target skill and comparable input, that new pass can count as rerun evidence for the previous revision.
- Do not block refinement just because earlier evidence was not labeled in advance.

## Common Contract Failures
- duplication across files that should have distinct roles
- unstable file-role separation
- naming drift between the instructions and the outputs
- stable documents collecting temporary or tactical language
- checklist content expanding into method detail
- entry instructions promising deliverables that the package does not actually constrain
- refinement removing core skill content instead of clarifying or relocating it

## File Ownership During Refinement
- Tighten the smallest file that actually owns the failure.
- Use this separation:
  - `SKILL.md` owns trigger rules, applicability, workflow summary, package boundaries, and response expectations
  - `references/method.md` owns the detailed procedure, decision logic, and evaluation model
  - `references/checklist.md` owns the quick execution and final validation pass
- If two files are saying the same thing at the same level of detail, the package is drifting toward duplication.
- Prefer one authoritative file and one shorter operational companion rather than two near-duplicates.

## Refinement Cycle
### 1. Confirm A Baseline
- Identify the best available `v1` evidence.
- Prefer a real prior run, but accept a realistic transcript or the current package when the failure is visible in the package itself.
- State explicitly what counts as `v1` before you change anything.

### 2. Review Outputs As Artifacts
- Evaluate the outputs as working artifacts rather than as promises.
- Check:
  - whether the skill created the right files
  - whether each file kept its intended role
  - whether any file duplicated another file's job
  - whether stable outputs collected temporary language
  - whether naming or paths drifted from the intended convention

### 3. Compare `v1` To The Current Pass
- Do not review the current pass in isolation.
- Name the exact failures that still matter:
  - duplication
  - role overlap
  - naming drift
  - unstable language
  - missing output constraints

### 4. Assign Each Failure To One Owning File
- Use `SKILL.md` when the issue is about trigger, scope, package layout, deliverables, or file-role expectations.
- Use `references/method.md` when the issue is about evaluation logic, step order, or how to diagnose failures.
- Use `references/checklist.md` when the issue is about the final quick validation pass.
- Avoid fixing the same problem in all three places.

### 5. Tighten The Contract
- Prefer sharper boundaries over more prose.
- Preserve important core content that still defines the skill's purpose, scope, decision logic, or expected behavior.
- If content is essential but misplaced, move or rewrite it in the correct owning file instead of deleting it.
- Typical improvements:
  - stronger must-not-include rules
  - shorter and clearer workflow summaries
  - explicit output expectations
  - clearer evidence requirements
  - removal of repeated explanation that belongs elsewhere

### 6. Rerun Or Record The Validation Gap
- Rerun the target skill on a comparable input when possible.
- A later pass counts as rerun evidence only if it revisits the same target skill and the same class of refinement issue closely enough to show whether the same structural failure reappears.
- If a rerun is not available, say that the package is improved but not fully rerun-validated.
- Keep only the comparison evidence needed to support the conclusion.
- Place temporary comparison artifacts under `docs/tmp/` and remove that folder when the loop is complete.

### 7. Stop Only When The Failure Stops Reappearing
- Refinement is complete when another comparable run is unlikely to need the same structural fix again.
- If the next likely issue is only wording polish, the structure is probably stable.

## Exit Criterion
- The refinement loop finishes when the skill’s output behavior is stable.
- Stable means:
  - repeated comparable runs produce the same structure cleanly
  - file roles remain distinct without manual separation work
  - stable outputs stop collecting temporary or tactical content
  - naming, paths, and conventions stop drifting
  - new runs no longer reveal the same structural failure again
- Do not stop just because one version looks better.
- Stop when another comparable run is unlikely to require structural correction and only negligible polish remains.
