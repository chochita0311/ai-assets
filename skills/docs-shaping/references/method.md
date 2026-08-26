# Method

Use this file for the full document-shaping procedure.

## Contents

- [Purpose](#purpose)
- [Working Sequence](#working-sequence)
- [Handoff Logic](#handoff-logic)
- [Reporting Standard](#reporting-standard)
- [Finish Pass](#finish-pass)

## Purpose
- preserve the substance of one or more documents
- improve internal composition only when needed
- reduce duplication, fragmentation, and flow breaks
- make the result feel seamless and impeccably structured without destructive rewriting

## Working Sequence

### 1. Read for substance first
- Read enough to identify:
  - purpose
  - audience
  - document genre
  - hard constraints
  - decisions and rationales
  - caveats and exceptions
  - repeated ideas
  - mixed scopes
  - buried key guidance
- If several docs are involved, note which one currently behaves like the closest canonical source.
- If the input is a document set, also note:
  - which files clearly need reshaping
  - which files appear already stable
  - whether the set already uses a recognizable heading style or section vocabulary

### 1a. Choose operating mode
- Default to `reshape` when the input is already a document or document set with recognizable structure.
- Use `intake` only when the input is a loose source set rather than a coherent document.
- Choose the mode from input state, not from the desired operations.
- Split, merge, and consolidate are operations inside a mode, not modes by themselves.

### 2. Detect necessity before changing anything
- Before editing, name a concrete reader task that the current composition obstructs or a concrete misreading it is likely to cause.
- Only proceed when one or more of these are true:
  - duplication causes confusion
  - section order makes the document harder to follow
  - policy, examples, reference detail, or planning notes are mixed together
  - important rules are buried in unrelated prose
  - the reader must mentally reorganize the doc while reading
  - refinement or expansion improved substance but degraded composition
  - the input is not yet a coherent document and needs intake shaping
- If the document is already clear and stable, leave it mostly unchanged.
- If no meaningful improvement can be made, return it unchanged.
- A possibly cleaner outline, more explicit route, added links, or relocated warnings are not sufficient by themselves when the document already provides an executable path and the cautions needed to use it.

### 2a. Assign intervention level
- Classify the planned edit before mutation from its complete surface area and semantic effect, not from a preferred label, the number of files changed, or a post-edit diff.
- `minimal`
  - local reordering
  - heading cleanup
  - local consolidation
- `moderate`
  - a bounded cluster of no more than two top-level content sections needs interpretive reordering or regrouping
  - repeated material needs canonicalization
  - the document-wide reading path and claim relationships remain intact
  - purely additive navigation may span more sections or files when it does not move, remove, reinterpret, or reframe existing content
- `major`
  - split or multi-doc consolidation is clearly necessary
  - current structure reflects historical accumulation rather than a usable composition
  - document-wide reordering or broad semantic compression is proposed
  - interpretive moving, rewriting, consolidation, or status labeling would affect three or more top-level content sections, or equivalent conceptual sections when headings are absent
  - one destination section, such as an executive summary, would synthesize or reframe claims drawn from three or more source sections
  - moving largely unchanged text would still replace the document-wide reading path
- Prefer the lowest level that fully describes the planned edit. If the boundary between `moderate` and `major` is uncertain, use `major`.

### 3. Diagnose composition failures
- Look for:
  - duplicated explanations with one concept spread across several sections
  - repeated headings that own overlapping content
  - sections that require future context to make sense
  - examples containing hidden rules
  - rules buried inside examples or notes
  - abrupt jumps between sections
  - appendix-like detail interrupting the main flow
  - headings that do not match the content beneath them
  - stable sections being dragged into churn by nearby edits
  - new structure being imposed where the existing structure is already sufficient
  - related files drifting into incompatible heading or section-label patterns without good reason

### 3a. Detect destructive-risk signals
- Be cautious when:
  - similar paragraphs contain subtle wording differences
  - repeated text may hide distinct constraints
  - policy and brainstorming are mixed together
  - examples encode operational rules
  - `must` and `should` language varies across apparently similar statements
  - planned compression would materially reduce unique examples, caveats, decisions, or explanatory context
  - a broad rewrite could reinterpret factual relationships while improving flow
  - a new heading or summary could strengthen a proposal, inference, or unresolved mapping into a confirmed fact
  - an umbrella label could blur distinct actors, channels, environments, or systems whose equivalence is not established
  - the proposed shape conflicts with established document conventions
- When risk is high, preserve more structure and report uncertainty explicitly.

### 3b. Gate high-risk major interventions
- Complete the intervention classification and preservation inventory before mutating the affected material. Do not use a post-edit `moderate` label to bypass this gate.
- Treat document-wide reordering, broad semantic compression, or interpretive changes across three or more top-level content sections as both `major` and high risk, even when no split or merge is proposed. Count source sections whose claims are synthesized or reframed, not only edited destination sections. Purely additive navigation that leaves existing claims and content in place is not high risk on section count alone.
- Apply a high-risk `major` intervention only when the active user request explicitly authorizes that class and degree of rewriting.
- Do not treat general permission to edit, including “directly apply needed changes,” as authorization for broad semantic rewriting. Major authorization must name or clearly accept broad, major, document-wide, or substantial rewriting, or approve a previously shown major change map.
- When authorization is absent, withhold that intervention before mutating the affected material and provide a concise change map containing:
  - affected sections
  - intended moves, merges, compression, or rewrites
  - unique content and constraints that must be preserved
  - material uncertainty or interpretation risk
- When authorization is present, inventory the same preservation constraints before editing. Authorization permits the intervention but does not permit silent meaning loss.

### 4. Choose the target shape
- Match the structure to the genre instead of forcing one template:
  - policy: purpose -> scope -> rules -> exceptions -> notes
  - guide: goal -> prerequisites -> steps -> variations -> troubleshooting
  - design note: context -> problem -> constraints -> approach -> tradeoffs
  - planning/logging: context -> current state -> decisions -> next steps -> tracking details
  - manuscript-style explanation: thesis -> distinctions -> method -> examples -> limits
- Keep one canonical home per idea when possible.
- Do not introduce artificial structure where the existing structure is already sufficient.
- Do not conflict with established document conventions unless the current conventions are part of the problem.
- When reshaping a related doc set, prefer compatible heading patterns and section vocabulary across files unless local divergence clearly improves readability.

### 5. Apply minimal restructuring
- Allowed operations:
  - reorder sections when flow is broken
  - merge repeated explanation into one canonical section
  - separate mixed-purpose sections
  - elevate hidden rules or caveats
  - move supporting detail downward
  - strengthen section boundaries and headings
  - add short bridging lines when transition gaps cause friction
- Avoid:
  - rewriting stable sections with no clear benefit
  - removing content because it looks messy
  - changing the force or intent of an existing rule
  - broad redesign just because a more elegant outline is imaginable
  - imposing a more formal outline when the current structure is already adequate
  - conflicting with established document conventions without a clear need

### 5a. Preserve before compressing
- By default, compression is allowed only when:
  - repeated material is materially saying the same thing
  - one stronger canonical statement can replace weaker restatements
  - no caveat, exception, or force-word difference is lost
- If in doubt, preserve and annotate rather than compress.
- If the user explicitly authorizes high-risk `major` compression, preserve the meaning of unique material, keep requested tradeoffs explicit, and do not treat authorization as permission to discard examples, caveats, decisions, or constraints silently.

### 5b. Intake shaping
- In `intake` mode:
  - inventory the source set
  - separate canonical content, supporting material, and tentative fragments
  - group related fragments before drafting the target structure
  - preserve uncertainty when the source is incomplete or ambiguous
  - produce one clearly identified primary shaped artifact by default
  - do not force every source fragment into the main narrative
- Some material may remain as notes, appendix, or unresolved items if forcing it into the main flow would reduce clarity.
- Additional outputs may be created as derived views only when:
  - the user asks for them, or
  - the source clearly supports distinct audience-specific views without inventing new strategy
- Prefer proposing derived views or waiting for user confirmation instead of emitting them by default.
- If derived views would be useful but are not emitted, suggest them explicitly as optional next outputs instead of silently expanding the pass.
- Retain the primary shaped artifact by default when derived views are emitted.
- If multiple outputs are emitted:
  - label the primary shaped artifact explicitly
  - label each derived view in one line near the top of the file
  - keep file roles distinct enough to avoid unnecessary overlap
- Do not treat `intake` as permission to continue into downstream authoring such as:
  - PRDs
  - execution plans
  - repo/docs structure proposals
  - implementation specs
- Those are separate next steps, not default `intake` outputs.
- For PDF or mixed-media intake:
  - report any evidence artifacts used for extraction or traceability
  - state extraction-quality confidence explicitly when source quality may affect fidelity

### 5c. Document-set selection report
- If the input is a document set, report:
  - changed files
  - unchanged stable files
  - the reason each changed file needed intervention
  - why unchanged files were left alone
- Prefer this explicit selection report over silently touching only part of a set.

### 5d. Comparison-copy outputs
- When the user asks for a comparison copy, staging path, or side-by-side review output:
  - write to the requested destination without mutating the source package
  - preserve source-relative terminology unless the user asks for a standalone relocated version
  - avoid rewriting internal path language only to match the temporary output location

### 6. Validate preservation
- Confirm:
  - all critical constraints remain
  - all explicit decisions remain
  - all exceptions remain
  - no unique content disappeared
  - force words were preserved
  - confirmed facts, proposals, inferences, and unresolved items did not gain stronger certainty through headings or summaries
  - distinct actors, channels, environments, and systems were not collapsed unless the source established their equivalence
  - unchanged stable sections were left alone on purpose

## Handoff Logic

### Consider `$docs-structuring` when available
- when the real issue is repo-wide doc ownership
- when several files conflict over the durable owner of the same rule
- when entrance docs, overview docs, or docs-map layers have drifted

### Pair well with `$refine-skill` when available
- when substance improved but the composition became bloated, repetitive, fragmented, or uneven
- when refinement exposed internal structure problems but not repo-wide ownership problems

## Reporting Standard
- Report:
  - operating mode
  - necessity justification
  - intervention level
  - withheld high-risk `major` change map when applicable
  - authorization basis and pre-edit preservation inventory when a high-risk `major` intervention was applied
  - changed files versus unchanged stable files when the input is a document set
  - primary shaped artifact when the mode is `intake`
  - derived views, if any, when the mode is `intake`
  - optional suggested derived views when useful but not emitted
  - composition diagnosis
  - resulting outline
  - `before -> after` movement summary
  - unchanged stable sections
  - evidence artifacts and extraction-quality confidence for PDF or mixed-media intake when relevant
  - preservation notes
  - confidence and unresolved risks

## Finish Pass
- Check the result with [checklist.md](checklist.md).
- Prefer a stable, less-churned result over a theoretically prettier one.
