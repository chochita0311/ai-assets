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

#### Active Runtime And Mixed-Version Evidence

- A fresh isolated process does not by itself prove that an already running application survives an update when server code, templates, schemas, generated assets, or browser caches can refresh independently.
- Evaluators should check the active runtime before and after the intended restart or migration boundary, or record that mixed-version compatibility is unsupported and requires a bounded restart.
- If independently refreshed layers can temporarily disagree on required fields, markup, or state, that transition should fail safely instead of turning an otherwise valid route into an unhandled error.

#### Client Asset Freshness And Executable Fallback

- When a visible action depends on client code, evaluators should confirm that the rendered page loads the matching asset version and that the control is actually bound after navigation, rerendering, restart, and a warm-cache revisit.
- Endpoint success alone is insufficient evidence for a click-driven action because stale assets can leave new markup visible but inert.
- When progressive enhancement is part of the approved contract, the underlying form or link should remain a safe executable path and preserve the relevant user scope.

#### Scope Transition State Contract

- When a scope change redefines the result set, define preservation or reset per state owner instead of treating the whole page as one state. Query, filter, selection, disclosure, pane geometry, outer page scroll, and nested result or tree scroll may need different outcomes.
- If global filtering and scoped search would conflict, the interaction should clear one state before entering the other instead of leaving both implicitly active.
- A destination scope should normally start its own result-local, tree-local, or preview-local state at an intentional anchor. Carrying hidden local scroll depth, disclosure, selection, or layout state from an unrelated scope is usually a continuity failure.
- Preserving the outer document position can still be intentional when it keeps the scope control or current task anchor stable; it is not automatically equivalent to inheriting the destination's local result state. Full-page versus partial navigation is an implementation detail and does not decide this contract by itself.
- Evaluators should exercise the transition after scrolling, across multiple scope choices, with shorter and longer destinations, and through back, forward, refresh, and direct entry as applicable. Verify each scroll container and state owner separately.

#### Equivalent Scope Consistency

- A problem reported for one tab, root, category, collection, or similar scope option should be traced to the shared control and state owner before it is treated as data-specific.
- When the behavior is shared, evaluators should sample multiple equivalent options and include selected, unselected, empty, or unavailable states that materially change disclosure or orientation.
- A fix should not hard-code the reported example when the approved behavior belongs to the whole scope family; evidence should state the family-wide rule and the representative cases used to verify it.

#### In-Place Analytical Switch Continuity

- Not every query-backed control changes the user's task scope. Switching metric units, aggregation, or composition inside the same analytical surface should usually preserve the surrounding document position and stable control anchors.
- Evaluators should distinguish a new result destination that has a meaningful beginning from an in-place re-expression of the same selected data. The former may reset to an intentional anchor; the latter should not make the page jump merely because the URL or server-rendered region changed.
- Test analytical switches after scrolling, with back and forward navigation, and across partial or full rendering paths. Verify page scroll, local scrollers, focus, selected state, and sticky regions rather than checking only the final values.

#### Action And Status Scope Parity

- A scoped action and the status or source summary placed beside it should describe the same operating boundary, or make their difference explicit.
- Adjacent counts, labels, or source entries should not imply that an action will affect data that it intentionally excludes.
- Implementation annotations such as storage paths or internal identifiers should stay off ordinary product surfaces unless they are required for the approved user task.

#### Navigation Context Restoration

- Direct entry into a detail route should restore enough surrounding navigation context for the user to understand where the item belongs.
- If the same detail item reached from a list expands or highlights a category, collection, or parent group, a direct URL entry should produce the same orientation state.
- Evaluators should compare list-driven entry and direct-link entry for active navigation state, expanded groups, and visible parent labels.

#### Hierarchical Browse-To-Preview Continuity

- When selecting an item changes only a preview or detail region, stable navigation regions such as source rails, trees, and grouped lists should preserve their user-facing state unless the approved interaction intentionally resets their scope.
- Whether those regions remain mounted or are rebuilt, preview changes should preserve or deliberately restore user-owned disclosure, navigation scroll, focus, interaction bindings, and current-item visibility inside any required expanded ancestors.
- URL and history state, preview identity, visible selection, programmatic current or selected state, and bounded feedback should advance as one coherent update rather than settling independently.
- Back and forward navigation should restore the same orientation contract as click-driven entry, including the active item, necessary ancestors, and an intentional focus destination.
- Rapid consecutive selections should cancel or ignore superseded work so stale responses cannot overwrite the latest choice. Normal destination links should remain available as a no-script or failed-enhancement fallback when the product supports progressive enhancement.
- Evaluators should test deep selection, repeated sibling selection, preserved scroll and disclosure, back and forward restoration, rapid input, and failed-update fallback instead of validating only the final preview content.

#### Contextual Selection Focus And Scroll

- When a nested selection reveals or replaces a meaningful content region, focus and scroll should move to the most specific newly selected destination that establishes context, not to a generic page heading or shared ancestor.
- The destination should remain visible below sticky shell regions and use the nearest reachable document position when the exact offset cannot be attained near a scroll boundary.
- Click-driven selection, back or forward restoration, and initial direct entry should have explicit, separately tested focus and scroll behavior rather than sharing one unconditional jump routine.

#### Breakpoint Control-State Compatibility

- If a responsive breakpoint hides or removes a mode switch, toggle, or similar state-changing control, the interface must also normalize into a state that remains supported without that control.
- A hidden control must not leave the user stranded in a now-invisible or no-longer-supported mode merely because URL state, previous viewport state, or persisted runtime state still points there.
- Evaluators should resize into and out of the affected breakpoint and also test direct-link entry with stateful query parameters to confirm that the visible controls and active runtime mode still match.

#### Component Interaction Ownership Boundary

- Component-level interaction code should own local affordances, visible state, and emitted intents; route delays, shell classes, global storage, and cross-surface animation timing should belong to an explicit shell or navigation coordinator.
- If a component accumulates route-specific timers, body classes, storage markers, and unrelated surface checks, evaluators should flag the ownership drift even when the visible behavior currently passes.
- A component may expose a small controller or event surface for orchestration, but evaluators should confirm that the component can still be understood as the owner of its own interaction contract rather than the owner of the page transition.

### Execution Confirmation And Action Ownership

#### Preflight And Execution Separation

- A preview or preflight for a remote, costly, destructive, or multi-target action should establish the exact known scope, selected targets, expected operation count or limit, and user-visible consequence without performing the action it is meant to confirm.
- Readiness failures such as a missing connection, capability, executor, permission, or runtime dependency should gate execution rather than erase the preview. Preserve the user's inputs and target selection, explain the recovery path, and keep safe local navigation or organization work available.
- Defaults should be inspectable and overridable before submission. Page load, ordinary browse, search, setup, or preview must not silently become execution merely because the required dependency is available.
- Evaluators should test preview with execution ready and unavailable, positive target data, zero targets, limit boundaries, partial failure, selected-only retry, and no-script fallback where progressive enhancement is part of the contract.

#### Effective Execution Input Confirmation

- When a product offers pre-execution confirmation for a command, job, or mutation, show the effective base request, user-supplied additions, executable invocation, and relevant input-channel boundaries such as arguments, standard input, environment, or files at the level needed for an informed decision.
- Distinguish base input from optional additions and make append, replace, or override semantics explicit; changes made in the form should update the confirmation coherently.
- The confirmation should derive from the same execution source as the real action rather than from a separately maintained approximation, while masking credentials or other values the user should not need to inspect.
- Evaluators should compare the visible confirmation with captured execution input for the normal path and each in-scope optional-input path.

#### First-Use Prerequisite Recovery

- When the primary task requires a registered connection, account, tenant, workspace, or similar prerequisite, the first-use path should offer an in-context way to reuse or create it instead of ending at an instruction-only dead end.
- Derive safe local facts from the user's input before requesting configuration, but do not infer a trust boundary, credential source, or access provider from a resource locator alone. Reuse may be automatic only when the match is unambiguous; multiple matches require an explicit choice.
- When prerequisite choices are dependent, establish the target scope before the connection, provider, or executor. Filter downstream choices to compatible options, and clear or reject an incompatible downstream selection when the target changes.
- Prerequisite creation should be atomic with the initiating local action. Validation failure must retain correctable input and leave no partial identity, while an intentionally unbound or local-only result must state that it is not yet ready for remote execution.
- Evaluators should test zero, one, and multiple prerequisite matches, target changes after downstream selection, optional later binding, invalid input, late failure rollback, direct entry, and the server-executable path when JavaScript is unavailable.

#### Single Execution-Path Ownership

- One user task at one lifecycle stage should normally have one primary initiation action.
- A marker, preparation, or alternate run control that produces the same practical outcome should be consolidated or removed unless its distinct side effects and lifecycle are clear to the user.
- Evaluators should confirm that action labels, progress, errors, cancellation or retry, and resulting history all belong to the same visible execution path.

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

#### Technical Canvas Input Ownership

- Gesture shortcuts for a diagram or technical canvas should supplement visible controls rather than replace them. Users need a deterministic way to inspect the current scale, reach supported bounds, reset to a known baseline, and fit the canvas when that behavior is offered.
- Ordinary wheel or trackpad scrolling should remain owned by the page or bounded viewport unless the approved modifier or pinch gesture is active. Zoom should preserve the pointer or viewport neighborhood closely enough that users do not lose the content they were inspecting.
- Rerendered or replaced canvases need one current interaction binding and an explicit reset-or-preserve rule. Render failure and no-script states must retain the approved textual or navigational fallback instead of leaving inert controls.
- Evaluators should test plain scrolling, modifier gestures, visible buttons, keyboard focus, bounds, reset, fit, repeated replacement, narrow layouts, and unavailable rendering separately.

#### In-Place Utility Action Continuity

- An auxiliary action inside a repeated record or detail heading should update only the state it owns and must not activate the surrounding destination link or unrelated row action.
- Successful in-place mutation should preserve the current query, filter, page, outer and nested scroll positions, and a meaningful focus target. Replacing state must not resize the control box, shift sibling metadata, or reorder the record unless ordering is an explicit consequence.
- Failure should preserve or restore the prior visible state and place bounded feedback beside the owning action without replacing the primary task.
- Evaluators should test rows with and without optional child controls, list and detail entry points, parent-link isolation, idle/hover/focus/pressed presentation, mutation failure, and the exact scroll and focus positions before and after activation.

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
