---
name: docs-structuring
description: Reorganize repository documentation into a clear layered structure with explicit ownership, deduplication, and cross-links. Use when docs are scattered, overlap each other, mix responsibilities, need entrance files such as AGENTS.md or CLAUDE.md aligned, or need to be restructured again as the project grows.
---

# Docs Structuring

Use this skill when repository docs need to be arranged, deduplicated, and systemized.

Prioritize documentation that is clean, seamless, readable, and descriptively clear.

## When To Use

Use this skill when the user wants to:
- collect scattered initial docs into a cleaner structure
- clean up `AGENTS.md`
- initialize or restructure `AGENTS.md`
- initialize or restructure `CLAUDE.md`
- reconcile multiple AI entrance docs into a coherent entrance layer
- reorganize `README.md` and project docs
- reduce duplicated instructions across docs
- split ambiguous summary docs into clearer files
- create a layered documentation structure for a repo
- make docs easier for agents and humans to navigate
- re-break down and reorganize the docs after the project has grown

Do not use this skill for:
- editing only one isolated sentence with no structural impact
- content work that does not involve document ownership or organization
- product planning or design-system work unless the task is specifically about document structure

## Core Outcomes

Produce a documentation system with these properties:
- entrance docs such as `AGENTS.md` or `CLAUDE.md` act as maps, not encyclopedias
- `README.md` remains user-facing
- project and domain docs are separated by role and responsibility
- specialized material lives outside entrance docs
- documents link to one another where that improves context discovery
- duplicated content is removed and replaced with pointers
- preexisting useful content is preserved and re-homed rather than discarded casually

## Workflow Summary

1. Audit the active docs and classify each file by role.
2. Identify duplicated facts, mixed-purpose docs, and ambiguous ownership.
3. Choose the owning layer for each durable fact.
4. Reorganize by moving or rewriting content into the owning doc.
5. Add cross-links where they materially improve context discovery.
6. Track the changes explicitly as `before -> after`.
7. Validate the result with the checklist.

## Operating Modes

- Use `incremental` by default when the repository already has a mostly workable documentation tree; focus on stale, overlapping, or misowned material and preserve stable areas.
- Use `restructure` only when ownership is broadly mixed, duplication is widespread, or the entrance and navigation layers are no longer usable.
- Choose the mode from the current documentation state, not from a preference for a cleaner-looking tree.

## Approval Boundary

- Apply clear ownership fixes, obvious deduplication, entrance-doc tightening, useful cross-links, and safe re-homing directly.
- Suggest optional file splits, new folder hierarchies, and navigation-changing reorganizations first, then wait for approval.
- Leave already stable documents and package-local guidance unchanged unless a concrete ownership or navigation problem justifies intervention.

## Rules

- Keep `AGENTS.md` short, stable, and operational.
- Apply the same entrance-map rule to `CLAUDE.md` or other AI entry docs when they exist.
- Keep `README.md` focused on user-facing overview and usage.
- Keep detailed maintenance guidance in deeper docs rather than in the entrance map.
- Prefer kebab-case for Markdown files under `docs/` unless an existing convention should be preserved.
- Use filenames that reveal purpose immediately.
- Keep every file clean, concise, and organically integrated into the doc tree.
- When changing one doc, check nearby docs and linked docs for stale context.
- If guidance already exists in the correct owner doc, link to it instead of copying it.
- Prefer document structures that clarify ownership and navigation instead of copying folder patterns mechanically.
- When a repository uses a durable-rule versus active-plan split, prefer `docs/policies/` for owned rules and `docs/plans/` for sequencing, refactoring, and roadmap material.
- Do not remove preexisting file content just to make the tree look cleaner; preserve and reorganize it unless the user explicitly wants content removed.
- When a proposed split, new file, or larger restructure is optional rather than clearly required, suggest it first and wait for approval before applying it.
- Prefer incremental cleanup when the existing structure is already mostly stable; do not reprocess stable areas without a reason.

## References

Read [references/method.md](references/method.md) for the full procedure, decision logic, and approval boundaries.
Read [references/layer-model.md](references/layer-model.md) when you need a concise model for assigning document ownership.
Read [references/checklist.md](references/checklist.md) before finalizing a documentation reorganization.
Read [references/example-output.md](references/example-output.md) when you need the reporting shape for a full pass.

## Output Format

Unless the user asks for a lighter response, structure the working result around:
- operating mode used (`incremental` or `restructure`)
- doc-role map
- ownership changes
- `before -> after` structure summary
- moved content summary
- removed duplication summary
- cross-link additions
- suggested-only restructures
- decision confidence summary
- unresolved or low-confidence items

## Output Standard

When doing a document-structuring pass, aim to leave behind:
- one clear entrance doc or one coherent entrance layer if multiple AI entry files must coexist
- one user-facing overview doc
- one owned home for each durable class of detail
- fewer repeated instructions
- clear cross-links where context discovery benefits from them
- a cleaner doc tree than the one you started with
- a structure that can be revisited and reorganized again as the project evolves
