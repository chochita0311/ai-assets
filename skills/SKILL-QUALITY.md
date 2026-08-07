# Skill Quality Guide

## Purpose
- Define what makes a good skill in this repo.
- Keep skill quality standards reusable across domains, not tied to one project.
- Support both direct human use and future harness-style automation.
- Keep skill contracts strong enough that real runs do not drift into adjacent work by habit.
- Act as the standing reference when a skill is added, updated, or refined in this repository.

## Scope And Ownership
- This guide owns the repository-wide acceptance bar for reusable skill packages under `skills/`.
- Treat active target-platform rules for package anatomy, frontmatter, metadata, and baseline validation as compatibility requirements without copying version-specific mechanics into this guide.
- Keep package-local domain procedure in the package that uses it; do not move it into this guide merely because it is important.
- Keep temporary findings, run evidence, and unresolved follow-up work outside this guide; only accepted reusable quality rules belong here.

## How To Use This Guide
- Read this before adding a new skill package under `skills/`.
- Read this before materially changing an existing `SKILL.md`, metadata, references, scripts, assets, or templates.
- Use this as the first review lens when deciding whether a proposed skill change should strengthen a contract, split responsibilities, or stay out of scope.

## What A Good Skill Is
- A good skill is not just a smart prompt.
- A good skill is a reusable contract that:
  - triggers for the right kind of problem
  - produces the right output shape
  - makes authority, scope, and stopping points explicit
  - keeps file roles distinct
  - can be evaluated without guesswork

## Core Quality Criteria

### 1. Clear Discovery And Trigger Boundary
- YAML frontmatter must follow the active platform contract and include the required `name` and `description` fields.
- The frontmatter `description` is the primary discovery and trigger surface. It should say what the skill does and when it should be used in language that matches realistic user asks.
- The body may define execution-time scope and guardrails after a valid trigger, but trigger inclusions and exclusions must not live only in the body. The body cannot rescue a vague or over-broad `description` because it is loaded only after triggering.
- Validate triggering against realistic positive and negative examples; those examples do not need to remain in the skill body unless they materially help execution.
- The skill should not trigger on every vaguely related task.

### 2. Strong Output Contract
- The skill should define what it creates or updates.
- Output location should be explicit when the repository convention is predictable.
- Stable outputs and temporary outputs should not be mixed casually.
- If multiple outputs are possible, the primary artifact versus derived views should be explicit.

### 3. Clear Operating Modes And Calibrated Control
- If a skill supports materially different operating modes, the modes should be explicit and easy to choose.
- Modes should be based on input state or task type, not on arbitrary naming churn.
- If one mode is the normal case, the default should be stated clearly.
- Match instruction freedom to task fragility and variability: use heuristics when several approaches are valid, parameterized patterns when a preferred approach allows variation, and deterministic scripts or exact sequences when errors are costly or ordering is critical.

### 4. Clear Authority And Source Priority
- If the skill consumes multiple inputs, it should define which source wins when they disagree.
- Authority order should be easy to restate from the package without opening several files.
- If the skill allows inference, it should be clear when inference is allowed and when it is too risky.

### 5. Clean Package Anatomy And File Roles
- `SKILL.md` is required and owns the lean entry contract, core workflow, output expectations, package boundaries, and routing instructions for bundled resources.
- Write procedural instructions in imperative, action-oriented form so another agent can execute them directly.
- `agents/` is optional and owns product- or harness-facing metadata such as `agents/openai.yaml`, not agent procedure. When metadata exists, keep it aligned with the current `SKILL.md` and validate it against the active platform constraints.
- `references/` is optional and owns detailed domain knowledge, procedure, decision logic, examples, and validation material that should load only when needed.
- `scripts/` is optional and owns executable, deterministic operations that are safer or more efficient to reuse than rewrite.
- `assets/` is optional and owns source material intended for produced outputs rather than instructions that should be loaded into context.
- `templates/` is an optional repository convention for output scaffolds; templates must not become a second home for method explanation.
- Trace each optional resource to a repeated, failure-prone, or context-heavy step in at least one concrete usage scenario.
- Remove generated placeholders and unused resource directories before accepting the package.
- Do not add auxiliary package documents such as a README, installation guide, quick reference, or changelog unless they have a distinct execution purpose and durable owner.
- Use `references/method.md` and `references/checklist.md` only when those roles fit the skill. Do not force every package into that pair when clearer domain-specific references are appropriate.

### 6. Progressive Disclosure
- Assume the executing agent already has general competence. Include only non-obvious procedural, domain, or tool-specific guidance that earns its context cost, and prefer concise examples over broad explanation.
- Keep `SKILL.md` focused on essential execution guidance and split detailed material as the file approaches 500 lines.
- Link required references directly from `SKILL.md` and state when each one should be read; do not require agents to discover important material through deep reference chains.
- Give reference files longer than 100 lines a concise table of contents so their scope is visible before the full file is read.
- For very large references, provide section names or search patterns in `SKILL.md` so the needed subset can be found without loading the whole file.
- Keep one authoritative home for each rule or explanation instead of duplicating it between `SKILL.md`, references, templates, and examples.
- Load examples, variants, and deep domain material conditionally rather than making every run pay their context cost.

### 7. Durable vs Temporary Separation
- Durable guidance should live in the skill package or owned docs.
- Temporary comparison artifacts, experiments, or rerun evidence should stay temporary unless the user explicitly asks to keep them.
- Skills should not create by-product docs by default.

### 8. Evaluator-Friendly Outputs
- Another agent or future pass should be able to judge the output from the files themselves.
- Outputs should not depend on hidden explanation from the original drafting run.
- If pass/fail cannot be judged without guessing, the skill contract is too soft.

### 9. Intervention And Approval Boundaries
- A good skill should make it clear whether it acts immediately, asks first, or stops for approval at specific boundaries.
- Optional or high-churn restructures should be suggested before they are applied when user approval matters.
- The skill should define when to leave stable material unchanged instead of optimizing it anyway.
- Validation does not expand task authority. Propose a forward-test before running it when it may take substantial time, require new approval, or affect a live system.

### 10. Reusable Generalization
- Prefer rules that generalize across repos and domains.
- Concrete examples are useful, but they should support the rule rather than replace it.
- A skill should not become overfit to one repo unless it is intentionally repo-local.

### 11. Output Lifecycle And Handoff
- A good skill should define where its job ends.
- If the output often leads to a downstream artifact, that next step should be named without being silently folded into the current skill.
- Handoffs to adjacent skills should be explicit when boundary confusion is likely.
- References to adjacent skills should stay optional and boundary-oriented rather than reading like hard dependencies unless the integration is truly mandatory.

### 12. Harness-Ready Expansion
- Good skills should be usable:
  - by one agent end-to-end
  - by a drafting agent plus an evaluator
  - inside a rerun or harness loop later
- This does not mean every skill must always run in multiple parts.
- It means the contract should be strong enough that role separation is possible when needed.

### 13. Validation And Evidence Maturity
- Keep `Result` separate from `Evidence Coverage`:
  - `Result`: `PASS`, `PASS WITH SUGGESTIONS`, or `FAIL` for the checks actually performed
  - `Evidence Coverage`: `complete`, `partial`, or `unavailable` for the required environments, scenarios, and reruns actually observed
- Use the following evidence ladder and report the highest level actually reached:
  1. static validation: frontmatter, package naming, links, referenced files, and metadata when present
  2. resource execution: relevant scripts, templates, parsers, or other deterministic resources exercised with representative inputs
  3. fresh forward-test: a fresh agent performs a realistic task from the skill and raw task artifacts without receiving the intended answer, suspected failure, or proposed fix
  4. comparable rerun: the revised skill is rerun on the same task class and contract failure closely enough to show whether that failure reappears
- Static validation is required for changed packages but does not prove output behavior.
- A forward-test is not comparable rerun evidence unless it rechecks the same target skill and class of failure after the revision.
- Frame forward-tests as ordinary user tasks rather than requests to review or simulate the skill.
- Give a fresh evaluator only the minimum task-local context and raw artifacts needed for the task. Isolate or clean prior outputs between passes so later runs cannot discover earlier conclusions.
- Substantial contract revisions and fragile workflows should normally reach a fresh forward-test; when they do not, report the reason and the resulting behavioral evidence gap.
- Not every change requires every level, but the final report must name missing evidence and whether the gap blocks the claimed quality result.
- Do not claim refinement stability from file polish or one successful pass. When real output evidence exists, compare the failure directly and require a comparable rerun before claiming that the revised behavior is stable.

### 14. Canonical Source And Distribution Lifecycle
- Name the canonical package before editing or syncing. For repository-owned packages, `skills/<skill-name>/` becomes the canonical source after an approved import.
- Edit the canonical source first, or import an explicitly chosen installed source into it before making further repository-owned changes.
- When the skill changes, inspect nearby metadata, references, templates, and executable resources for stale contracts.
- Run the applicable static validation and resource checks before distribution.
- Sync only to user-approved targets such as Codex or Claude installation directories.
- Compare intended source and target files after syncing, while accounting explicitly for target-specific metadata or compatibility differences.
- Do not maintain an installed copy as a silent parallel source once the repository package is canonical.
- Record that already-running sessions may retain cached skill instructions; use a new session when validating whether the installed revision is active.

## When To Update This Guide
- Update this guide when a real skill run reveals a reusable contract gap that affects more than one skill.
- Update this guide when several skills independently converge on the same new boundary, output rule, or evaluation rule.
- Do not update this guide just to mirror one package's local wording.
- If a finding applies only to one skill, keep it in that skill package rather than adding it here.

## What This Guide Should Not Become
- not a catalog of every current skill package
- not a repository-wide instruction file or entrance document
- not a temporary run log
- not a place to restate package-local method details
- not a backlog for unresolved or package-specific follow-up work

## Maintenance Bias
- Prefer strengthening existing criteria over adding parallel categories that say nearly the same thing.
- Prefer adding one reusable rule after repeated evidence instead of front-loading speculative governance.
- When a new criterion is added, make sure it can be checked from skill files or realistic outputs rather than conversation memory alone.
- Keep this guide as one document unless growth creates a concrete navigation or ownership problem; do not split it only for symmetry with skill packages.
- Keep unresolved improvement work out of this guide until evidence supports an accepted reusable criterion.

## Common Failure Patterns
- The body contains detailed `When To Use` guidance, but the frontmatter `description` is too vague to trigger the skill correctly.
- `SKILL.md` reteaches general knowledge or the full method instead of preserving context for non-obvious execution guidance.
- Instruction freedom does not match operational risk: contextual work is over-constrained, or a fragile sequence is left to open-ended prose.
- `SKILL.md`, references, templates, or examples repeat the same rule at the same level of detail.
- `references/checklist.md` becomes a second method document.
- Important references are reachable only through another reference instead of being routed directly from `SKILL.md`.
- A long reference has no navigable contents summary.
- A very large reference has no section or search routing from `SKILL.md`.
- An optional resource, auxiliary document, placeholder, or empty directory remains without a concrete execution purpose.
- A script or template is shipped without exercising its executable or parseable behavior.
- UI-facing metadata is missing where the target requires it, or remains stale after the entry contract changes.
- Outputs mix durable rules with temporary tactics.
- File names or output paths drift from what the skill promises.
- The skill creates weak by-product docs that no one owns later.
- Evaluation depends on verbal explanation rather than self-contained artifacts.
- A static validation pass is reported as proof that realistic output behavior or rerun stability was verified.
- A forward-test receives the intended answer, suspected bug, or proposed fix and therefore cannot test independent generalization.
- A forward-test is framed as a review exercise or can discover artifacts from an earlier pass.
- Multi-source input is used without source-priority rules.
- The skill silently expands into adjacent work such as planning, specification, or restructuring beyond its stated boundary.
- The skill references another skill as if that other skill were a required dependency rather than an optional better fit for a neighboring problem.
- Several modes exist, but no one can tell which mode is the default or why one mode should be chosen.
- Derived outputs appear, but the package never clarifies whether they replace the primary artifact or sit on top of it.
- High-churn changes are applied automatically even when stable areas could have been left alone.
- Installed copies drift from the canonical package or become undeclared parallel sources.

## Review Gates

Mark every applicable gate `yes` or `no`. Mark a gate `not applicable` only with a short reason.

### Discovery And Contract
- Does frontmatter pass the active platform validator, with the folder name and required metadata aligned?
- Does `description` state both what the skill does and when realistic users should invoke it?
- Are trigger inclusions and exclusions present in `description` rather than only in the body, with operating modes, authority order, approval boundaries, output roles, and stopping points explicit where needed?
- Is instruction freedom calibrated to task variability, ordering risk, and failure cost?
- If `agents/openai.yaml` exists, does it still match `SKILL.md` and the active UI metadata constraints?

### Package And Progressive Disclosure
- Does every file have one clear job, with optional resources traceable to concrete repeated, failure-prone, or context-heavy execution needs?
- Were generated placeholders, unused resource directories, and purposeless auxiliary documents removed?
- Does the package spend context only on non-obvious guidance and concise execution-relevant examples?
- Does `SKILL.md` link required references directly and state when to read them?
- Are long references navigable, very large references searchable from `SKILL.md`, and detailed examples or variants loaded only when needed?
- Are rules owned once instead of repeated across the package?
- Are durable outputs, temporary evidence, and derived artifacts kept distinct?

### Validation And Evidence
- Did the changed package pass static validation, including link and referenced-file checks?
- Were changed executable or parseable resources exercised with representative inputs?
- Does the report separate `Result` from `Evidence Coverage` and name every material gap?
- If behavioral reliability or refinement stability is claimed, is there a fresh forward-test or comparable rerun that actually supports that claim and was framed as an ordinary user task with isolated evidence?
- Did substantial contract revisions and fragile workflows receive a fresh forward-test, or does the report state why not and identify the behavioral evidence gap?
- Would a second agent be able to judge the output without conversation-only context?

### Lifecycle And Portability
- Is the canonical source explicit, and were adjacent metadata, references, templates, and resources reviewed for drift?
- Were only approved installation targets updated and compared with the canonical source afterward?
- Are target-specific differences and running-session cache limits stated instead of hidden?
- Would the same skill still make sense in another repository of the intended class?

## Practical Summary
- A good skill is reusable.
- A better skill is reusable and checkable.
- The best skills in this repo should be reusable, checkable, bounded, portable, and easy to refine from real evidence without overstating its coverage.
