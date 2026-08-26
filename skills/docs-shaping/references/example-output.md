# Example Output

Use this as a shape reference for a full `docs-shaping` pass.

This is an example of the reporting format, not a mandatory literal template.

## Operating Mode Used
- `reshape`

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
