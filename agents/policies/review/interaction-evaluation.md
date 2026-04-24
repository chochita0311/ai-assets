# Interaction Evaluation

## Purpose
- Keep reusable interaction-quality evaluation rules for state changes, transitions, and browse or read continuity.
- Preserve durable checks for interaction stability without mixing them into project-governance docs.
- Support consistent evaluation across functional and UX review work.

## Ownership
- This document owns reusable interaction-evaluation checks and cautions.
- In a consuming repo, use `docs/agents/roles/functional-evaluator.md` for the functional evaluation role contract.
- In a consuming repo, use `docs/agents/roles/ux-heuristic-evaluator.md` for the UX heuristic evaluation role contract.
- In a consuming repo, use `docs/policies/harness/execution-loop-governance.md` for fail routing and loop handling.

## Use
- Apply these rules when evaluating visible state changes, navigation continuity, or browse and read flows.
- Add new entries when the same class of interaction failure proves reusable beyond one feature.
- Promote an entry elsewhere only when it becomes broader product law rather than an evaluation asset.

## Reusable Evaluation Notes

### Transition Stability And Continuity

#### Interaction Stability
- Click-driven view changes should swap to the next state only when the destination content is ready enough to avoid visible flicker, flash, or placeholder-only intermediate states.
- Do not expose internal source paths, loading scaffolds, or temporary copy during normal screen transitions if the user can avoid seeing them.
- Prefer atomic content swaps, cached data reuse, and background prefetching over clearing the current screen first and then rebuilding it.
- Verify important browse and read flows by clicking through them in a browser and checking for brief visual flashes, unstable sticky regions, or loading-state leaks.

#### Navigation Continuity
- A user should not lose orientation during normal browse or read transitions.
- Local view changes should preserve the surrounding shell and navigation anchors unless the approved feature explicitly changes them.
- Returning from a detail surface or changing a browse mode should not feel like a reset unless the feature explicitly requires one.

#### State Exposure Discipline
- Intermediate system states should stay as invisible as reasonably possible during normal interaction.
- Temporary copy, debug-facing labels, or source-oriented state descriptions should not leak into the user-visible surface.
- If loading or recovery states are required, they should appear intentional and bounded rather than as raw implementation leakage.

### Binding And State Ownership

#### Interaction Binding Preservation
- UI updates must not silently destroy active interaction bindings on controls that should continue working after a rerender.
- If a surface rebuild replaces buttons, links, or controls with new nodes or components, the system must preserve or rebind the intended interactions as part of the same change.
- Re-rendering markup without restoring event behavior is a blocking defect, not an acceptable implementation detail.
- Pagination, mode toggles, navigation controls, and repeated actions should be explicitly rechecked after any interactive-surface replacement strategy.

#### Scope Transition Reset Rule
- When a scope change redefines the result set, explicit reset is usually safer than carrying forward the previous search or filter state.
- If global filtering and scoped search would conflict, the interaction should clear one state before entering the other instead of leaving both implicitly active.
- Evaluators should check whether query, tag, category, collection, or similar browse states are reset or preserved intentionally rather than by accident.

### Menus, Disclosures, And Affordances

#### Immediate Dropdown Dismissal
- Hover-driven dropdowns should close immediately after the user makes a selection.
- Leaving the dropdown open after selection slows recognition of the newly loaded destination state.
- Evaluators should verify both the selected result and the menu-dismiss behavior, not just the navigation target.

#### Compact Control Menu Placement
- Compact controls such as page-size or sort menus should open in a way that preserves nearby content readability rather than covering the primary browse surface unnecessarily.
- The expanded menu should feel attached to its trigger through aligned width, boundary, and placement instead of appearing as a detached floating box.
- Evaluators should test both the closed and expanded states and verify that the chosen direction, spacing, and attachment do not create avoidable overlap with cards or other active content.

#### Click-Affordance Match
- Pointer, hover, and focus affordances should appear only on the part of a surface that is actually interactive.
- If only a title, summary, or other sub-area opens a destination, the surrounding card body must not advertise clickability through pointer cursor or full-surface hover treatment.
- Evaluators should compare real click targets with visible affordances and flag any surface that still feels clickable after the interactive area has been narrowed.

#### Disclosure Direction Consistency
- A compact disclosure control should not visually imply one expansion direction while actually opening in another.
- If a menu opens downward, its cue should remain stable or reinforce downward attachment rather than flipping into an upward state on open.
- Evaluators should check both closed and expanded states and confirm that the visual cue, placement, and expanded panel all tell the same directional story.

### Repeated Controls And First-State Isolation

#### Repeated Footer Action Anchoring
- Repeated footer actions such as pagination buttons or page-size changes should preserve practical click reach after each state change.
- If the result length changes after the action, the interaction should keep the footer control area anchored closely enough that the user can continue acting without re-chasing the control.
- Evaluators should test short-final-page transitions, larger page-size transitions, and repeated previous or next actions near the bottom of the viewport.

#### First-State Interaction Isolation
- If a landing, modal, overlay, or other first-entry surface is meant to be the active state, downstream interactive surfaces must not remain keyboard-focusable, pointer-active, or screen-reader-visible during that phase.
- Visual overlay alone is not sufficient evidence of isolation; evaluators should explicitly check `inert`, focus order, `aria-hidden`, or equivalent interaction-blocking behavior on deferred surfaces.
- A feature may still pass if downstream content remains visually mounted for continuity, but only after evaluators confirm that the inactive layer cannot steal interaction before the handoff.

## Classification Guidance
- Usually classify as `implementation bug` when the spec already requires stable transitions, continuity, or no-leak behavior.
- Usually classify as `spec gap` when the spec failed to define how view changes, loading behavior, or navigation continuity should work.
- Classify as `planning gap` when the interaction failure reveals a missing mode, missing flow definition, or wrong approved feature boundary.
