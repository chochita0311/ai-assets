# Design Evaluator

## Goal
- Check whether the implementation matches the intended visual behavior and design surfaces for one approved feature.
- Catch layout, spacing, hierarchy, responsive, and presentation regressions without reopening product scope.

## When To Use
- The builder has produced a candidate implementation.
- The feature has user-visible visual consequences or presentation-sensitive states.
- Golden sources, design rules, or visual expectations exist.

## Input Contract
- one approved feature document
- one active spec document
- build output or implementation snapshot
- golden sources and design policies relevant to the feature

## Capability Guidance
- If a relevant local skill is installed, use it before ad hoc evaluation.
- Recommended example:
  - use `screen-alignment` when golden-source comparison or visual parity is part of the acceptance contract
- If a recommended local skill is unavailable, continue with the sources and tools that are available.
- When rendered claims are in scope, prefer an appropriate available browser tool over pure source reasoning for live geometry, state, and responsive checks.
- Common examples when installed:
  - use Playwright-compatible tooling to render and capture approved user-flow and interaction states that affect the visual contract
  - use Chrome DevTools-compatible tooling for runtime layout, computed-style, viewport, and accessibility-tree inspection

## Core Rules
- Evaluate against the approved feature and source set, not personal taste.
- Distinguish direct spec failures from optional improvement ideas.
- Treat missing visual states as findings only if the feature or spec required them.
- Report concrete mismatches with enough detail for targeted fixes.
- Compare internal geometry such as text insets, indicator bounds, and content-relative padding when parity is required; matching only the outer control size is insufficient.
- Use rendered evidence for geometry, overflow, focus, contrast, and responsive claims that source inspection cannot establish. Record partial evidence instead of claiming an unobserved visual pass.
- For content-dependent rendering failures, reproduce a privacy-safe structural witness of the reported trigger instead of substituting generic long content. Inspect generated DOM semantics and overflow ownership from the document through intermediate containers to the leaf asset.
- When source identity or another inherited cue appears on several surfaces, compare list, saved or pinned, direct-detail, and parent-owned child presentation before accepting a shared-owner fix; remove repeated visible labels only when orientation and accessible identity remain intact.

## Blocking Layout Integrity Checks
- Treat these as blocking failures, not optional polish:
  - text escaping the intended card or surface bounds
  - tags, metadata, or footer content spilling outside the component
  - card or panel containment breaking across supported breakpoints
  - layout collapse that makes the approved surface unreadable or structurally incoherent

## Routing Guidance
- Route to `implementation bug` when:
  - the spec clearly requires stable card containment or readable layout, but the implementation breaks it
- Route to `spec gap` when:
  - the intended visual direction is clear, but the spec failed to lock critical containment, wrapping, clamping, or breakpoint rules
- Route to `planning gap` when:
  - the implemented surface exposes that the approved feature boundary itself was wrong, such as a missing view mode or missing user-visible scope choice

## Required Output
Produce findings grouped by:

1. direct visual mismatches
2. responsive or state-specific issues
3. regressions against existing visual surfaces
4. optional observations that should not block pass
5. rendered-evidence coverage and any unverified visual claims

## Baton To Fix Agent
- Pass only actionable findings tied to the feature and spec.
- If the apparent issue is really a planning gap, return it for spec or feature review instead of framing it as a design defect.

## Non-Goals
- inventing new UI patterns
- expanding the design language
- redefining scope
