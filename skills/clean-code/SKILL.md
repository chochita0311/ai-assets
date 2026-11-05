---
name: clean-code
description: Simplify hard-to-read or overengineered code and clarify responsibility boundaries while preserving required behavior. Use for code cleanup, code diet, readability reviews, or implementation decisions about abstractions, mixed responsibilities, duplicated policy, or needless indirection. Do not use for formatting-only changes, routine edits with no structural decision, or document cleanup.
---

# Clean Code

Reduce the effort needed to understand behavior, identify who owns state and rules, and make the requested change. Remove unnecessary complexity and repair misplaced responsibility within the task. A clearer result may require deletion, consolidation, extraction, or movement; fewer lines or files are not the objective.

## Scope and authority

- Resolve the target and desired outcome from the request and available code. For ordinary implementation, start with the affected flow; for an explicit cleanup or review, cover the named target. Expand reading to related callers, dependencies, tests, configuration, and runtime registrations as needed to establish the change's impact. Review breadth does not grant broader edit authority.
- For generated or vendored code, identify the generator or upstream owner instead of editing an output that will be overwritten.
- In a review or advice task, report findings without changing code. In an authorized implementation or cleanup task, apply necessary in-scope improvements directly, including removing code made unused by the change. Skill selection does not authorize unrelated cleanup, publication, or a migration.
- Follow explicit task and project contracts. An inferred local pattern is evidence, not a requirement to preserve a demonstrated defect. Surface a material conflict with an explicit rule before deviating. Use the actual language and dependency versions and relevant official sources when semantics are uncertain.
- Keep new public API, data format, dependency, or architecture migrations within existing authorization. When resolving the task requires an unapproved expansion, finish unaffected work and present the concrete boundary and proposed change. Do not ask again for already-authorized work or impose approval solely because several files must change.
- Apply this procedure proportionally to the active task. It is not a session-wide mode, a mandatory repository audit, or a reason to produce a design document.

## Diagnose before choosing a transformation

Read the relevant execution paths and identify a concrete obstacle to understanding or modification. For new code, use the actual flow and change the requested implementation must support; a pre-existing defect is not required. Useful evidence includes a policy scattered across callers, state whose owner is unclear, a forwarding chain that hides no useful decision, or several independent jobs that must be understood together to change one. Length, age, naming taste, and a complexity score alone do not establish a defect.

For each material obstacle, connect these facts in working reasoning:

1. **Reader or change task:** what must someone understand or modify, and where does the current code obstruct it?
2. **Cause and scope:** which responsibilities, state, branches, conversions, or dependency hops create that burden? Which affected paths establish the diagnosis?
3. **Necessary intervention:** which change removes the obstacle, and what present requirement justifies any new boundary?
4. **Preservation and check:** what behavior or relationship must survive, and which observation can detect its loss?

Keep this reasoning internal unless a finding, consequential trade-off, or unresolved boundary needs explanation. Do not invent alternatives or bookkeeping for a routine change. A maintainability finding needs a concrete reading or modification difficulty; it need not invent a runtime bug.

For a broad cleanup, examine the target's relevant responsibilities and paths, not only the first obvious issue. A sample can guide discovery but cannot establish whole-target completion. Distinguish examined, inventoried, and unexamined areas. If the target is unclear and available evidence cannot resolve a consequential choice, ask a focused question while continuing independent work.

## Choose the smallest sufficient intervention

Choose among leaving valid code, renaming, deleting, inlining, reusing, consolidating, extracting, and moving. Compare the combined reading and change burden before and after, including navigation and the concepts a caller must understand. Do not choose a smaller diff that leaves the requested ownership problem unresolved, or redesign stable neighbors to make a tree look uniform.

- **Delete or inline** when the code has no required use or hides no useful policy, effect, or lifecycle boundary. Establish usage through the mechanisms the project actually uses; a text search with no callers does not prove absence of exports, reflection, dependency injection, configuration, or plugin registration.
- **Reuse or consolidate** when existing code, a standard facility, or an installed dependency supplies the required semantics. Check whether apparent copies represent the same rule and must change together. Similar syntax alone does not justify coupling independent policies. Preserve meaningful boundary validation and error handling.
- **Extract or move** when a present responsibility, independent change, state lifetime, or external dependency warrants a boundary. Keep related rules and state under clear ownership and preserve shared invariants across boundaries. One implementation or one caller can justify a boundary; execution order alone does not justify a component per step.
- **Keep explicit code** when it makes decisions and effects easier to follow. Avoid replacing a clear sequence with clever expressions, mechanical helper chains, or generic frameworks. Long names and comments that narrate mechanics can obscure intent, but useful API documentation, constraints, reasons, and algorithm explanations must survive.

Read [Decision examples](references/decision-examples.md) when deletion, consolidation, or splitting has competing plausible interpretations, especially around runtime usage, mutable state, and shared resources. The examples are discriminators, not mandatory transformations or language style rules.

## Apply and verify

Identify the requested behavioral changes separately from cleanup. Preserve all other relevant contracts: results, error semantics, evaluation timing and side-effect order, atomicity, concurrency, resource lifetime, compatibility, and required performance. Do not retain a bug that the task explicitly asks to fix under the label of behavior preservation.

Apply coherent, reviewable increments and complete the affected callers, tests, configuration, and documentation. Reuse configured formatting, lint, type, architecture, and behavior checks appropriate to the change. Add or adapt meaningful regression checks where the changed logic or boundary warrants them; avoid tests that merely mirror code shape. When coverage is missing, obtain a focused observation or characterize the relevant behavior before relying on it; narrow unsupported conclusions rather than treating an unrun check as passed.

Check both outcomes:

- **Behavior:** do the available checks and inspected paths support the required contracts, including important failure paths? Tests passing is evidence within their coverage, not a proof of equivalence.
- **Structure:** follow an affected flow and locate a concrete in-scope modification. Is the obstacle gone, is state and rule ownership clear, and is the requested responsibility or package outcome complete? Inspect the rest of a broader target sufficiently to avoid declaring a partial increment complete.

If simplification loses a contract or merely moves the burden elsewhere, revise it or undo the task-owned change. Preserve unrelated or concurrent edits. Stop when the requested result and identified obstacles are addressed and applicable checks are complete, or report the specific remaining boundary or evidence gap. Do not keep searching for aesthetic changes to satisfy a cleanup quota.

A no-change result is valid when the examined target already supports the requested reading and modification tasks. Explain the evidence for keeping it and any coverage limits; do not label unexamined code clean.

## Output and handoff

The result is the requested code change or a read-only assessment. Briefly report the obstacle and its consequence, the intervention or justified no-change result, actual verification and coverage, and unresolved work. Scale detail to the task; no permanent report, scorecard, or log is required by this skill.

Keep language-specific syntax, layout, and tool choices with the consuming project. This package supplies judgment criteria, not a universal class hierarchy, folder tree, function-size limit, or code-reduction target.

When work needs a tracked sequence of substantial refactoring phases or a strict parity/merge decision, use $refactor-plan if available. Otherwise retain the same scope and evidence boundaries using the project's existing planning process. A handoff does not complete unfinished cleanup or authorize a new scope.
