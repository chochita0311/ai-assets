---
name: docs-shaping
description: Reshape document content into a clearer, more coherent, and more navigable form while preserving meaning. Apply minimal, non-destructive restructuring only when necessary. Default to reshaping existing structure.
---

# Docs Shaping

Use this skill to reshape document content without casually changing what the document means.

This is a content-level restructuring skill. It improves composition, flow, hierarchy, and navigability while preserving substance.
This skill also covers shaping a raw source set into a first coherent artifact when the input is not yet a document.
This skill can also be applied to a skill document set to improve coherence across `SKILL.md`, method, checklist, and examples without redesigning the overall skill system.

If another skill such as `docs-structuring` is available, prefer that direction when the real problem is document ownership, repo layering, entrance-doc drift, or cross-document duplication.

## Purpose

Reshape document content into a clearer, more coherent, and more navigable composition while preserving all meaningful content, constraints, and intent.

This skill improves structure only when necessary. It prioritizes stability over perfection.

## Modes

This skill operates in two implicit modes based on input state.

### `reshape` (default)

Use when the input is already a document or document set with recognizable structure.

Goal:
- improve clarity, flow, and section boundaries without changing meaning

### `intake`

Use when the input is a raw or fragmented source set rather than a coherent document.

Examples:
- golden source notes
- idea fragments
- screenshots
- webpage excerpts
- copied references
- rough planning notes

Goal:
- consolidate scattered source material into one coherent structured document
- leave behind one clearly identified primary shaped artifact by default

## Mode Selection

- Default to `reshape`.
- Use `intake` only when the input is clearly not yet a coherent document.
- Choose the mode based on input state, not desired operations such as split or merge.

## When To Use

Use this skill when the user wants to:
- reorganize one Markdown document so it reads more clearly
- consolidate several overlapping Markdown docs into one coherent document
- split an overloaded doc into a small cleaner set with explicit rationale
- preserve current content while redesigning the outline, order, or section boundaries
- strengthen a policy, planning, logging, guide, or design note so it reads as one deliberate artifact instead of an accumulated draft
- make a document feel more seamless and impeccable without destructive rewriting

Do not use this skill for:
- repository-wide doc ownership or docs-tree cleanup
- lightweight wording or typo edits with no composition impact
- inventing new policy, decisions, or strategy without source basis
- aggressive restructuring when the current document is already clear and stable
- downstream authoring such as PRDs, execution plans, repo/docs structure proposals, or implementation specs unless the user explicitly asks for a separate next step

## Core Outcomes

Produce a document or document set with these properties:
- the meaning, constraints, and intent are preserved
- the structure is clearer and easier to scan
- repeated ideas are consolidated into one canonical place
- rules, caveats, and exceptions stay attached to the guidance they qualify
- the result feels intentionally designed rather than historically accumulated
- stable sections remain untouched unless change is necessary
- changed versus unchanged areas are explicit when reshaping a document set
- `intake` mode leaves behind one clear primary shaped artifact by default

## Workflow Summary

1. Read for purpose, audience, genre, constraints, and hidden structure.
2. Decide whether restructuring is actually necessary.
3. Diagnose the composition failures that justify intervention.
4. Apply the minimum effective reshaping.
5. Validate that substance, force words, and exceptions were preserved.
6. Check the result with the checklist.

## Rules

- Restructuring is applied only when it meaningfully improves clarity. Otherwise, preserve the existing structure.
- If no meaningful improvement can be made, return the document unchanged.
- Prefer the minimum effective restructuring.
- Do not rewrite already-stable sections for aesthetic neatness.
- Do not introduce artificial structure where the existing structure is sufficient.
- Do not silently drop meaningful content.
- Do not merge near-duplicate content until you verify that no distinct constraint is being lost.
- Preserve force words such as `must`, `should`, `only`, `never`, and `unless`.
- Keep examples, caveats, and exceptions near the rule or concept they qualify.
- Prefer one strong canonical explanation over repeated paraphrases.
- Make section titles reveal purpose, not just topic fragments.
- Do not reshape in a way that conflicts with established document conventions unless necessary.
- When reshaping a related document set, prefer compatible heading patterns unless local divergence clearly improves clarity.
- When writing to a comparison copy or staging path, preserve source-relative terminology unless the user asks for standalone relocation.
- When intake relies on screenshots, PDFs, or mixed-media sources, preserve traceability and report extraction-confidence when fidelity may be affected.
- In `intake` mode, produce one clearly identified primary shaped artifact by default.
- Retain the primary shaped artifact by default when derived views are created.
- Additional `intake` outputs are optional derived views, not required defaults.
- Derived views should normally be proposed or user-confirmed rather than emitted by default.
- If multiple `intake` outputs are emitted, each file must declare its role in one line near the top.
- Do not expand from `intake` into downstream planning or specification documents unless the user explicitly asks for that next step.
- When refinement improves substance but leaves the document bloated, fragmented, or uneven, this skill may be used to stabilize the composition.
- When reshaping reveals cross-document ownership confusion, call out that boundary explicitly and consider `docs-structuring` if that skill is available.

## References

Read [references/method.md](references/method.md) for the full procedure, scoring model, risk signals, and handoff logic.
Read [references/checklist.md](references/checklist.md) before finalizing a reshaping pass.
Read [references/example-output.md](references/example-output.md) when you need the reporting shape for a full pass.

## Output Format

Unless the user asks for a lighter response, structure the working result around:
- operating mode used (`reshape` or `intake`)
- necessity justification
- intervention level when a full pass is being reported
- changed files versus unchanged stable files when the input is a document set
- primary shaped artifact when the mode is `intake`
- derived views, if any, when the mode is `intake`
- optional suggested derived views when they would help but were not emitted
- composition diagnosis
- composition score before and after when a full pass is useful
- resulting outline
- major `before -> after` moves
- preserved versus consolidated content
- unchanged stable areas
- evidence artifacts and extraction-quality confidence for PDF or mixed-media intake when relevant
- confidence summary
- unresolved or low-confidence items

## Output Standard

When doing a document-shaping pass, aim to leave behind:
- a document that reads more smoothly without losing substance
- a structure whose hierarchy matches the actual content
- fewer repeated explanations
- clearer section boundaries
- stronger reader orientation
- a result that feels seamless and deliberate
- no unnecessary churn in already-working areas
