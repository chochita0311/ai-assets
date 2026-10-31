# Example Output

Use this as a shape reference for a full `docs-shaping` pass.

This is an example of the reporting format, not a mandatory literal template.

## Contents

- [Full-pass reporting example](#operating-mode-used)
- [Intake example notes](#intake-example-notes)
- [Content role examples](#content-role-examples)

For bounded work, a compact result is sufficient: "Reviewed the revised runbook procedure and its prerequisites, warnings, and linked exceptions. Separated a diagnostic example from a destructive command because the shared block invited accidental execution. Preserved both commands and their conditions; no broader outline change. Other runbooks were not reviewed."

For an unchanged follow-up: "Rechecked the edited procedure and qualifying warnings against the prior review. No remaining composition problem or meaning loss in this scope; no further changes." A whole-set request still requires whole-set review, even when only one file changes.

A request to check whether an expanded guide set still reads as a coherent whole can begin with whole-set exploration. It need not wait for a local defect or the words "full audit"; any resulting major rewrite still follows the existing approval boundary.

## Operating Mode Used
- `reshape`

## Review Coverage
- Read the four listed documents for composition and preservation; no claim is made about other documents.

## Necessity Justification
- `policy.md` spreads required logging rules, implementation notes, examples, and exceptions across six sections.
- The current order forces implementers to reconstruct which statements are requirements and which are supporting detail.

## Changed Files Versus Unchanged Stable Files
- Changed:
  - `policy.md`: required rules and supporting material are mixed across the document-wide reading path
- Unchanged:
  - `logging-reference.md`: stable implementation reference with no ownership overlap
  - `alerts.md`: already stable and narrowly scoped
  - `glossary.md`: reference-only structure already fit its purpose

## Intervention Level
- high-risk `major`

## Major Authorization Basis
- The active request explicitly authorized a document-wide major rewrite of `policy.md`.

## Pre-Edit Preservation Inventory
- all required logging rules and force words
- implementation examples and operational terminology
- exception cases and the caveats they qualify
- distinctions between policy requirements and supporting implementation notes

## Composition Diagnosis
- policy and implementation details are mixed together
- repeated logging rules appear in several sections
- examples contain hidden constraints
- the current opening does not orient the reader to the document's purpose

## Resulting Outline
1. Overview
2. Core Logging Principles
3. Required Logging Rules
4. Implementation Notes
5. Examples
6. Exceptions And Edge Cases

## Before -> After Movement Summary
- moved: scattered logging rules -> `Required Logging Rules`
- merged: repeated rationale paragraphs -> `Core Logging Principles`
- elevated: hidden constraints from examples -> `Required Logging Rules`
- separated: implementation detail from policy text
- moved without rewriting: exception examples -> `Exceptions And Edge Cases`

## Unchanged Stable Sections
- left `logging-reference.md`, `alerts.md`, and `glossary.md` unchanged
- kept stable implementation detail in its existing owner instead of duplicating it into `policy.md`

## Preservation Notes
- preserved all original constraints and examples
- preserved `must` versus `should` distinctions
- preserved the exception examples verbatim while moving them into the owned section
- consolidated repeated explanations without collapsing distinct exceptions

## Confidence Summary
- `high` for the consolidation and section reordering
- `medium` for whether implementation notes should remain in the same file long term

## Unresolved Or Low-Confidence Items
- whether the implementation notes should eventually move to a separate reference doc if the file grows again

## Intake Example Notes
- In `intake` mode, include:
  - the primary shaped artifact
  - any derived views, labeled explicitly
  - optional suggested derived views when they would help but were not emitted
  - source types processed
  - evidence artifacts and extraction-quality confidence for PDF or mixed-media intake when relevant
  - chosen target document genre
  - grouped versus deferred fragments
  - unresolved or low-confidence source material
- Do not emit PRDs, execution plans, repo/docs structure proposals, or implementation specs by default from `intake`.

## Content Role Examples

These synthetic cases apply when this skill runs alone as well as when a separate ownership review is available.

| Input | Expected disposition |
| --- | --- |
| A guide paragraph combines “Retries require version 2.4 or later” with a dated run ID, build hash, and one-off pass receipt; the selected set includes the existing verification record. | Keep the compatibility condition in the explanation. Preserve the run-specific values, result, environment, and limits in the verified record and link it when useful. Merely renaming the paragraph “Implementation notes” does not resolve the mixture. |
| A reproduction step uses an exact source revision and distinct source/input hashes; an API reference specifies an identifier's required format. | Keep the exact values and format where the reader must execute or compare them, with labels explaining their subjects. Do not simplify them away for a cleaner-looking page. |
| A single selected working note has a confirmed constraint, a future proposal, and a failed dated experiment. | Keep the constraint binding, the proposal tentative, and the experiment historical with its conditions. Use clear local sections when adequate; do not force a new file or turn the experiment into a general rule. |
| Intake combines source fragments for a guide with task notes and an existing evidence record. | Produce the primary guide while preserving the other material in appropriate existing sources or owners. Do not copy the whole work history into the guide, reinterpret the record as a required derived view, or create a new plan/log by default. |
| Only an explanation guide is selected and a proposed relocation has no suitable authorized destination. | Keep the original material accessible and report the unresolved placement and scope boundary. The single-file selection does not authorize turning the guide into a working log; do not silently omit material or claim that an appendix alone fixes the ownership problem. |
| A follow-up finds no remaining composition defect, changed evidence, or new execution. | Return an unchanged result in the response; do not add a review appendix or repeat the prior closeout in the artifact. |
