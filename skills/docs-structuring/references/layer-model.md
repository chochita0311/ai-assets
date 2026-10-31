# Layer Model

Use this model to assign documentation responsibility.

## Entrance Layer
- Purpose: help the reader enter the repo correctly.
- Typical file: `AGENTS.md`
- Should contain: scope, codebase map, source-of-truth pointers, top-level rules.
- Should not contain: deep implementation detail, design specs, repeated setup commands, catch-all notes.

## Overview Layer
- Purpose: explain what the repository is and how to use it.
- Typical file: `README.md`
- Should contain: concise overview, local usage, navigation to deeper docs.
- Should not contain: detailed project policy or duplicated architecture guidance.

## Project Layer
- Purpose: hold durable project-specific detail.
- Typical files: policy, architecture, development, roadmap, package guide, or other role-specific docs
- Should contain: one owned responsibility per file.
- Should not contain: broad mixed-purpose summaries that overlap several layers at once.

## Specialized Layer
- Purpose: hold deeper domain-specific material.
- Examples: design docs, refactor plans, operations notes, package-specific guidance, domain references.
- Move information here when it becomes too detailed or too local for upper layers.
- Package-specific guidance can live near the owning package or subsystem when that placement improves clarity.

## Content Roles And Reader Needs

Assign a scope layer above and a content role below to affected passages. A shared project or feature topic does not make their responsibilities identical.

| Content role | Owns |
| --- | --- |
| Knowledge and guidance | Established facts, current contracts, concepts, procedures, applicable conditions, exceptions, and the rationale needed to interpret them |
| Active work | Goals, proposals, sequencing, current status, unresolved questions, dependencies, and next actions |
| Execution and evidence | What happened, when, against which inputs and environment, with what results, decisions, verification limits, and historical context |

Each role can have an authoritative owner. A log can be canonical evidence without owning the current rule. A dated snapshot is not competing current guidance when its scope is explicit; research explanations and ADRs may need historical rationale or negative findings.

Check placement separately from truth or traceability:

- Ask whether removing or relocating a detail would prevent the intended reader from completing this document's task, then whether the exact value must be available at this point in the reading path.
- Keep explanation and user guides focused on usable facts, concepts, and steps. Internal commit lists, run IDs, raw hashes, temporary paths, and pass receipts belong in their evidence owner when the reader does not need them to understand or act. Traceability alone does not justify their inclusion, even in an appendix.
- Keep exact supported versions, public identifier formats, commands, fixed inputs, and content fingerprints where compatibility, execution, or reproduction requires them. Explain what each value identifies and where it is used; a version and a content fingerprint serve different purposes and do not replace one another.
- In execution or verification records, retain the identifiers and qualifications needed to distinguish inputs, environments, actions, results, and their limits. Do not remove dates, commits, versions, or hashes merely because they look technical; do not require every possible identifier when it serves no recordkeeping purpose.

## Directory Rule
- Prefer adapting to the repository's existing clear structure over imposing a new one.
- If no good structure exists, create the smallest clear hierarchy that separates ownership cleanly.
- Choose folders and filenames based on ownership clarity, navigability, and maintainability.

## Ownership Rule
- Generalizable guidance moves upward.
- Package-specific or tightly local guidance moves downward.
- If two docs contain the same instruction, choose one owner and make the other doc point to it.
