# Example Output

Use this as a shape reference for a full `docs-shaping` pass.

This is an example of the reporting format, not a mandatory literal template.

## Operating Mode Used
- `reshape`

## Necessity Justification
- `policy.md` and `logging.md` both own logging rules, but the duplicated guidance is split across policy text, examples, and implementation notes.
- The current order forces the reader to reconstruct the intended flow manually.

## Changed Files Versus Unchanged Stable Files
- Changed:
  - `policy.md`: mixed policy and implementation detail
  - `logging.md`: duplicated rules and hidden constraints inside examples
- Unchanged:
  - `alerts.md`: already stable and narrowly scoped
  - `glossary.md`: reference-only structure already fit its purpose

## Intervention Level
- `moderate`

## Composition Diagnosis
- policy and implementation details are mixed together
- repeated logging rules appear in several sections
- examples contain hidden constraints
- the current opening does not orient the reader to the document's purpose

## Composition Score
- Before: `14 / 30`
- After: `25 / 30`

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

## Unchanged Stable Sections
- retained the existing exception examples with only heading and placement changes
- kept the original operational terminology because it already matched the system language

## Preservation Notes
- preserved all original constraints and examples
- preserved `must` versus `should` distinctions
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
