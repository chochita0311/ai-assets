---
name: design-plan
description: Create or update scoped design-change plans for existing products, including UI, UX, brand experience, consistency, and phased rollout. Use when a request or ongoing work needs design decisions, shared-impact analysis, sequencing, or validation gates, even for one complex screen. Not for isolated polish, implementation with settled design decisions and no planning need, constitution-only work, greenfield product definition, or general code refactoring.
---

# Design Plan

Turn a bounded design problem into evidence-backed decisions and a usable change
plan: what to preserve, what to change, where the change reaches, how to sequence
it, and how to check the result. A list of screen-editing tasks alone is not enough.

Use this method when explicitly requested or when the current task needs design
planning. It works independently and inside an existing harness. The skill owns
design-planning methods; the project's workflow retains task selection, scope
approval, execution routing, lifecycle state, and completion authority.

## Select The Work

- Plan changes across screens, components, patterns, or user flows when their
  relationships, alternatives, shared impact, or rollout need coordination.
- Include a single complex screen when its states or interactions need a real
  planning decision. Screen count alone is not an eligibility test.
- Reconcile implementation drift with existing rules, or plan an explicitly
  requested design evolution while separating preserved behavior from intended
  changes. Cover visual, interaction, information-hierarchy, brand-experience
  consistency, or the relevant combination.
- Revisit an existing plan when new evidence, a changed requirement, a completed
  batch, a blocker, or evaluation findings affect its decisions or next work.
- Skip a separate design-planning pass for an isolated polish task or a settled
  target that can be implemented directly. Explaining or evaluating this skill
  does not itself request a product plan.

Keep neighboring work distinct. When available, `init-design` can establish or
deliberately revise durable design rules, `design-deslop` can provide selectable
visual alternatives, and `screen-alignment` can implement against an existing
system or target. General code-refactor planning belongs to `refactor-plan` when
available. These are optional methods, not a required chain. New-product
definition and a new visual identity need their own scope.

## Resolve Scope And Sources

1. Resolve the actual product, requested outcome, allowed actions, and existing
   planning owner before writing. Read applicable project guidance, relevant
   requirements or PRD/feature boundaries, design policies, active plans, and
   current implementation. Do not infer the output project from the skill's
   repository or an imported harness directory.
2. Distinguish a planning-only request from a broader task that already includes
   implementation or evaluation. Preserve existing authorization and the
   project's required review gates; invoking a skill adds no new approval gate.
3. Use this source priority unless the project defines a stricter owner:
   - explicit user direction and scope constraints for this task;
   - approved product requirements and durable design policies or constitution;
   - accepted decisions in the active plan;
   - rendered screens, source artifacts, and implementation as current-state evidence;
   - cautious inference.
4. Identify whether a source describes the target product or an external
   reference, and keep its authority separate from observation quality. A
   reference's controls, content, layouts, and states are not target invariants
   unless target evidence or an approved requirement establishes them. Track a
   reference-inspired choice as a proposal until adoption is authorized. When
   authorized, record the intended change and its approval status. When target
   evidence is absent, keep its current state unknown.
   Current implementation is not automatically a new product rule, and drift
   does not override the constitution. Record authorized exceptions explicitly.
   Keep material scope or durable-rule conflicts open
   until their owner resolves them, while progressing unaffected work.
5. A PRD or constitution is not mandatory for every plan. Use the available
   request, established constraints, and inspectable artifacts; identify missing
   criteria and provisional decisions. Ask only when a missing answer materially
   changes the dependent scope, design decision, or acceptance condition. Do not
   require another skill or a new policy document merely to begin useful planning.

## Diagnose And Decide

1. Inspect enough of the current experience to support the requested decision:
   relevant screens, real content, components, states, flows, and device sizes.
   Reuse sound existing findings. Do not turn every planning task into a full
   product audit. Prefer rendered evidence for visual claims; when it is absent,
   state the limitation and keep affected conclusions provisional.
2. Record a reproducible baseline: source location and available revision or
   snapshot identity, observed viewport/state/content, and material access limits.
   A static capture shows appearance under those conditions, not verified focus
   movement, validation, navigation, persistence, or other unobserved behavior.
3. Connect each material finding to its evidence and affected user task. Separate
   direct observation, interpretation, reported requirements, and proposed change.
   Distinguish a defect or inconsistency from an intentional variation, an
   unsupported state, and a preference hypothesis. Similar components need not
   have identical behavior when their jobs differ.
4. Define the desired state and the design decision that reaches it. State what
   stays, what intentionally changes, and why. Compare alternatives when they
   could materially change the outcome; record relevant tradeoffs and why a
   choice is preferred. Retaining the current design can be the right decision.
   Do not invent data, controls, workflows, or confirmed requirements to complete
   the plan. Keep unaccepted choices identifiable as proposals.
5. Trace the impact through shared components, tokens, content models, and
   related surfaces. Name affected areas outside the requested change, preserve
   their constraints, and either contain the change or make the additional reach
   an explicit scope decision. Do not silently rewrite durable design law.

## Build Or Update The Plan

- Reuse the existing owner and its format. In a harness, contribute design
  evidence, proposed changes, and acceptance criteria to the designated planning
  artifact without creating a parallel PRD, feature boundary, or lifecycle ledger.
  Keep product scope in its requirement owner, execution decomposition in its
  feature/plan owner, and actual evaluation results in their evaluation owner.
- For a standalone plan with no stronger convention, use
  `docs/plans/design/` in the resolved product and
  [templates/plan.md](templates/plan.md). Prefer a descriptive name such as
  `design-change-plan.md` or `design-consistency-plan.md`. Honor a requested
  session-only answer; do not create a file merely because the skill was selected.
- Extend the same active track when its scope and baseline still apply. If a
  changed goal or baseline needs a separate track, explain the boundary and
  leave a handoff rather than silently replacing the old plan.
- Include purpose and plan type, baseline, scope and non-goals, invariants,
  findings and design decisions, bounded work, validation gates, risks or open
  questions, an exit goal, and a handoff when needed. Refer to owned rules;
  do not repeat the full constitution or locked token tables.
- Group work by a coherent screen family, pattern, flow/state, or drift category.
  For each batch include **Goal**, **Why this grouping**, **Guardrails**,
  **Targets**, **Validation**, and **Exit gate**. Connect batches to the design
  decisions, identify material prerequisites and shared impact, and explain
  priority through user impact, risk, or dependency rather than chronology alone.
- Keep intended changes separate from preserved requirements. Include only
  findings and decisions that affect the scoped outcome, preservation, acceptance,
  or sequencing; avoid unbounded redesign ideas and unrelated summaries.
- When updating, reconcile reported progress with actual evidence. Preserve
  accepted choices, completed-work evidence, earlier rationale, and deferred
  items with their reasons. Record changed assumptions and which conclusions
  need rechecking. Keep status, remaining work, blockers, and next action in the
  existing owner's convention; plan authorship does not mark execution passed.

## Define Checks And Report Evidence

- Specify the situation, surface/state/viewport when relevant, expected result,
  and evidence needed for each material acceptance check. Prefer side-by-side
  comparisons, targeted runtime smoke checks, and design-rule alignment checks.
  Include shared-surface regressions and meaningful intentional variations.
- Distinguish planned checks from checks actually performed. A complete plan is
  not evidence that an implementation meets it. A screenshot or source-only
  review cannot establish unobserved interaction or accessibility behavior.
- Validate the plan itself: supported findings, explicit preservation and
  intentional deltas, reasoned grouping/dependencies, concrete checks, unresolved
  decisions with their impact, correct artifact ownership, and a usable next step.
  If the evidence supports no change, record that decision without inventing work.

## Finish And Continue Within Authority

- For planning-only work, finish with the requested plan or update, the important
  decisions and their reasons, checks actually performed, evidence gaps, and the
  next scoped action or decision. Do not imply implementation completion.
- When the original task already authorizes implementation or evaluation,
  hand the plan back to that work and continue under its existing gates. Do not
  stop or request the same permission again solely because this skill ran.
- Keep active cleanup and rollout in the plan. Propose promotion of stable rules
  to the project's policy owner (`docs/policies/design/` by default); apply a
  constitution change only within explicit authorization, including authorization
  already present in the current task.
- Keep the workflow's approval and progress records authoritative. This method
  neither starts background monitoring nor grants authority to publish or merge.
- Keep task-owned captures and other working evidence temporary unless a durable
  owner is requested or already established. Preserve evidence needed for an
  active handoff, then remove inactive task scratch; durable plans must not rely
  on deleted temporary files.

## Invocation Examples

- `Use $design-plan to plan the changes to these existing screens, preserving our product constraints and identifying shared-component impact.`
- `Our list, detail, and settings flows handle errors differently. Work out what should stay different and plan the changes and checks.`
- `This one screen has several editing states. Establish the design decisions and a staged plan before changing it.`
- `Update the design section of the existing approved feature using these new findings; keep its scope and approval state.`
