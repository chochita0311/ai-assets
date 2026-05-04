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

#### Staged Handoff Timing

- Outgoing surface exit, incoming surface entry, and persistent-shell state changes should be timed as separate parts of one handoff.
- Destination disclosures, dropdowns, or contextual panels should not appear before the destination shell or content is ready enough to own them.
- Evaluators should sample early, middle, and late transition frames and verify computed durations or animation names when timing is part of the fix.

#### Deferred Interaction Reconciliation

- When hover, focus, or disclosure behavior is intentionally deferred during a transition, evaluators should test interactions that happen during the deferred window, not only before and after it.
- A deferred interaction gate should re-read current hover or focus ownership when it opens; otherwise the UI can end in a highlighted-but-not-interactive state.
- Evaluators should verify both paths: pointer leaves during the transition and the state clears, and pointer returns during the transition and the intended interaction becomes available after the destination can own it.

### Binding, Scope, And Responsive State Ownership

#### Interaction Binding Preservation

- UI updates must not silently destroy active interaction bindings on controls that should continue working after a rerender.
- If a surface rebuild replaces buttons, links, or controls with new nodes or components, the system must preserve or rebind the intended interactions as part of the same change.
- Re-rendering markup without restoring event behavior is a blocking defect, not an acceptable implementation detail.
- Pagination, mode toggles, navigation controls, and repeated actions should be explicitly rechecked after any interactive-surface replacement strategy.

#### Scope Transition Reset Rule

- When a scope change redefines the result set, explicit reset is usually safer than carrying forward the previous search or filter state.
- If global filtering and scoped search would conflict, the interaction should clear one state before entering the other instead of leaving both implicitly active.
- Evaluators should check whether query, tag, category, collection, or similar browse states are reset or preserved intentionally rather than by accident.
- If a scope change replaces the visible result set after the user has scrolled, the destination scope should start at an intentional anchor, usually the top of the new result list.
- Carrying the previous scroll depth into a different category, collection, or result scope is usually a continuity failure because it hides the beginning of the newly selected content.

#### Navigation Context Restoration

- Direct entry into a detail route should restore enough surrounding navigation context for the user to understand where the item belongs.
- If the same detail item reached from a list expands or highlights a category, collection, or parent group, a direct URL entry should produce the same orientation state.
- Evaluators should compare list-driven entry and direct-link entry for active navigation state, expanded groups, and visible parent labels.

#### Breakpoint Control-State Compatibility

- If a responsive breakpoint hides or removes a mode switch, toggle, or similar state-changing control, the interface must also normalize into a state that remains supported without that control.
- A hidden control must not leave the user stranded in a now-invisible or no-longer-supported mode merely because URL state, previous viewport state, or persisted runtime state still points there.
- Evaluators should resize into and out of the affected breakpoint and also test direct-link entry with stateful query parameters to confirm that the visible controls and active runtime mode still match.

#### Component Interaction Ownership Boundary

- Component-level interaction code should own local affordances, visible state, and emitted intents; route delays, shell classes, global storage, and cross-surface animation timing should belong to an explicit shell or navigation coordinator.
- If a component accumulates route-specific timers, body classes, storage markers, and unrelated surface checks, evaluators should flag the ownership drift even when the visible behavior currently passes.
- A component may expose a small controller or event surface for orchestration, but evaluators should confirm that the component can still be understood as the owner of its own interaction contract rather than the owner of the page transition.

### Menus, Disclosures, And Affordances

#### Immediate Dropdown Dismissal

- Hover-driven dropdowns should close immediately after the user makes a selection.
- Leaving the dropdown open after selection slows recognition of the newly loaded destination state.
- Evaluators should verify both the selected result and the menu-dismiss behavior, not just the navigation target.

#### Data-Ready Disclosure Gate

- Async dropdowns should not expose placeholder markup, loading copy, or skeletal internal menus merely because hover or focus CSS can open the panel before data is ready.
- Panels should have an explicit readiness gate; if data is pending, keep the disclosure closed unless an intentional, styled loading menu is part of the approved behavior.
- Evaluators should test delayed or failed data fetch paths and confirm that final unavailable states are bounded and intentional.

#### Hover Focus Handoff And Release

- Pointer clicks can leave keyboard focus on a trigger; evaluators should test click-then-mouseleave to confirm highlight and expanded states clear unless keyboard focus intentionally remains.
- Temporary handoff locks used to bridge route transitions should be released once real hover or focus can own the state.
- Same-route navigation clicks should avoid both reload flicker and stale open or highlighted menu states.

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

### Repeated Controls And State Anchoring

#### Repeated Footer Action Anchoring

- Repeated footer actions such as pagination buttons or page-size changes should preserve practical click reach after each state change.
- If the result length changes after the action, the interaction should keep the footer control area anchored closely enough that the user can continue acting without re-chasing the control.
- Evaluators should test short-final-page transitions, larger page-size transitions, and repeated previous or next actions near the bottom of the viewport.

### Reading Surface Link Integrity

#### Reference Link Rendering Integrity

- Reading surfaces that render references, citations, or Markdown links must preserve usable anchors in both the body content and any generated reference panel.
- Auto-linking raw URLs must not corrupt existing Markdown links by creating nested anchors, malformed `href` values, or duplicated visible URL fragments.
- Evaluators should test notes with raw URLs, Markdown links, trailing punctuation, and generated reference sections because link-rendering failures often appear only in mixed content.

### First-State Isolation And Handoff

#### First-State Interaction Isolation

- If a landing, modal, overlay, or other first-entry surface is meant to be the active state, downstream interactive surfaces must not remain keyboard-focusable, pointer-active, or screen-reader-visible during that phase.
- Visual overlay alone is not sufficient evidence of isolation; evaluators should explicitly check `inert`, focus order, `aria-hidden`, or equivalent interaction-blocking behavior on deferred surfaces.
- A feature may still pass if downstream content remains visually mounted for continuity, but only after evaluators confirm that the inactive layer cannot steal interaction before the handoff.

#### First-State Handoff Consistency

- When shell navigation, direct URL entry, or other scope-changing interaction hands off from a first-entry state to a downstream surface, the first-entry state must be dismissed early enough that it cannot visually reappear during the same transition.
- Route interpretation, first-state visibility, and destination rendering should converge as one coherent handoff rather than exposing a frame where the old first state briefly competes with the chosen destination.
- Evaluators should test narrow and wide viewport cases, direct-link entry, and shell-driven navigation to confirm that a hidden landing or overlay does not resurface because dismissal state lags behind routing or render order.

## Classification Guidance

- Usually classify as `implementation bug` when the spec already requires stable transitions, continuity, or no-leak behavior.
- Usually classify as `spec gap` when the spec failed to define how view changes, loading behavior, or navigation continuity should work.
- Classify as `planning gap` when the interaction failure reveals a missing mode, missing flow definition, or wrong approved feature boundary.
