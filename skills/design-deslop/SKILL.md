---
name: design-deslop
description: Improve existing screens that feel AI-generated, generic, or template-driven through an interactive HTML before/after review with per-change acceptance, rejection, and feedback. Use for comparing UI improvements before adoption, preserving intentional character, or applying previously reviewed selections. Not for AI-authorship detection, routine UI fixes, greenfield brand design, product-wide rebranding, or a comprehensive accessibility audit.
---

# Design De-slop

Make an existing screen belong more clearly to its product and users. Connect
each proposed change to a visible problem and a useful comparison; a familiar
font, card, gradient, or animation is not by itself a defect. Preserve room for
creative alternatives and for keeping the original.

## Scope and authority

- **Always deliver an HTML review:** keep the before view on the left and the
  proposed or actually applied result on the right, visible simultaneously.
  Offer whole-screen context and focused before/after inspection of changed
  components at a readable scale. Prefer actual inspectable DOM with preserved
  HTML/CSS and element identities, so the user can point to an element in browser
  DevTools. Include an explicit whole-screen comparison of the exact selected
  combination, item-level choices and feedback plus
  an overall note, including when there are no changes to select. Chat prose or
  separate screenshots supplement this artifact; they do not replace it. A no-change result still
  shows the retained screen and explains the judgment.
- **Preview new choices before adoption:** keep the working product unchanged
  while developing alternatives. Requests to improve, continue or repeatedly
  "ship" do not select unseen design changes. Creative exploration can be broad;
  adoption remains tied to what the user actually reviewed and chose.
- **Apply reviewed selections:** carry out an expressly selected variant or
  exact displayed combination without asking for the same permission again.
  A checkmark is a draft preference until the user submits the selection for
  application. An autosave or a receipt merely found on disk is not approval.
  The review controls never write project files or imply that they already did.
- Follow current user instructions and applicable project rules. Separate
  binding product truth, supported behavior, frozen regions and explicit design
  commitments from incidental implementation habits. Read actual content and
  rendered screens alongside design documents; filenames, stale plans, and a
  missing design document do not establish visual authority.
- Preserve real content, data meaning, routes, controls and accessibility unless
  their change is explicitly in scope. A visual proposal must not invent a
  testimonial, statistic, metadata field, action or working interaction.
- Identify conflicts with binding design rules. A rule-changing alternative may
  be proposed with its impact and required owner-document changes made explicit;
  do not silently veto creative exploration or rewrite the rules. Carry out an
  expressly authorized rule change within its agreed scope.
- A change to shared tokens or components can affect unselected screens. Make
  that reach part of the choice, or contain the change within the selected area.

## Establish a comparison

1. Resolve the screen or region and its visitor's job: reading, completing a
   task, discovering work, or deciding to act. Read nearby implementation,
   current design rules, real content, states and relevant sibling surfaces.
   Ask only about a missing fact that could materially change the decision.
2. Inspect the rendered baseline at relevant sizes and states. Record the route,
   viewport, content, theme, scroll/selection and motion conditions needed to
   reproduce the comparison. Do not diagnose a loading frame or missing font as
   the final design. Identify meaningful changed components and measure their
   bounds or DOM selectors in each rendered view when focused inspection is possible. Name any
   rendering or access limitation.
3. Retain a lightweight source identity for the affected files and shared
   dependencies: a revision plus working changes, or file fingerprints when
   needed. Keep the initial baseline and last accepted state distinct from
   unaccepted drafts. Record intentional features worth preserving and the
   visual dimensions still open to exploration.

For diagnosis, read [Contextual patterns](references/patterns.md). Use its
conditions and counterexamples to form hypotheses, not a checklist of required
defects. Finish the product-specific assessment before considering an optional
detector; warnings neither prove authorship nor determine quality.

## Develop and show alternatives

Use [Proposal scaffold](templates/proposal.md) to prepare the decision content.
Read [HTML review contract](references/html-review.md) to build the required
artifact with the bundled viewer and [review helper](scripts/review.py), or an
equivalent implementation that preserves the same interaction and evidence
contract. The helper needs only Python's standard library; browser capture uses
the project's available tools.

- Separate the observation from the interpretation. State why it matters here,
  including its relationship to content, hierarchy, identity or the visitor's
  task. Distinguish an established functional problem from a taste hypothesis.
- Give each independently selectable change a stable ID and each alternative a
  distinct label. Explain the proposed change, expected benefit, tradeoff,
  preserved elements, affected files/regions and a comparison question that can
  discriminate improvement from novelty. Repeated text can serve different
  orientation, grouping and filtering roles; do not erase a role to simplify it.
- Explore genuinely different compositions where useful, rather than cosmetic
  variations that all share the same weakness. A small region may support a bold
  visual change. Offer a more adventurous direction when the request or problem
  warrants it, without imposing a candidate quota, a mandatory new aesthetic, or
  a predetermined amount of restraint.
- Study real references when they can answer an unresolved design question.
  Identify the particular principle worth transferring and its fit here; do not
  replace the product with a reference's branding, content or features. Use
  available tools without requiring an external service, installation or upload.
- Build previews in an isolated copy or other reversible preview environment.
  Preserve existing user changes and the product workspace before selection;
  do not switch the user's working tree between experimental candidates.
- Show the original and alternatives under matching comparison conditions,
  including enough surrounding screen to judge the changed region. Prefer
  actual rendered DOM previews with element selectors the user can cite. Use the
  bundled [DOM snapshot resource](assets/snapshot.js) when preserving a rendered
  page as portable HTML/CSS; read its procedure and limitations in the HTML
  contract. Do not require screenshots alongside complete DOM previews. Use
  labeled captures only when DOM cannot be preserved or when separate visual
  evidence is useful for verification. Distinguish a frozen DOM snapshot from
  a running application; do not imply captured controls still execute product
  behavior. Label sketches, static concepts and untested states
  accurately. For motion or interaction changes, include a replay or sequence
  and relevant reduced-motion behavior, not only a favorable still image.
- If rendering is unavailable, deliver the useful diagnosis and explicitly
  labeled concepts in the HTML, with visible missing-render states. State what
  visual evidence is missing; do not call the before/after verified or allow a
  concept or missing capture to masquerade as an application-ready comparison.
- Show the artifacts, not just their paths or promises to make them later. Keep
  the unchanged original as a real option. Mark alternative choices, compatible
  combinations, prerequisites and conflicts before asking for selection. Include
  shared-style impact and any requested design-rule departure. Return a working
  HTML link and an inline view of the actual comparison when the client supports it.

Let the user move between a component and the whole screen without losing choices
or notes. In DOM mode, navigate to the actual corresponding elements and retain
the captured viewport dimensions; do not enlarge the frame height and silently
change viewport-dependent layout. In capture mode, use corresponding measured
regions at a shared scale. Keep the whole composition available to reveal surrounding effects. A
missing region needs a visible explanation and a whole-screen return, not an
invented crop. For combined selections, use that combination's measured regions.
Component focus is inspection, not a new adoption boundary: keep inseparable
changes bundled and name every affected component in that bundle’s adoption scope.

Offer a direct integrated whole-screen view of the user's exact selected set.
Use its actual combined document, not fragments assembled from individual options;
show a missing combination honestly. Let element references carry the before/after
side, view, preview and selector into feedback. DevTools edits are exploratory:
they do not update the proposal or source files. Restore the recorded preview
before application, or turn the requested edits into a new reviewed proposal.

Keep the comparison surface quiet: one entry to the selected combination, one
place to choose each proposal, and one handoff action. Put rationale, comparison
questions, benefits, tradeoffs, preserved meaning, scope and checks in expandable
details beside the change. Use accessible names and tooltips for compact controls;
do not repeat their meaning across toolbars, sidebars and status prose. Show
explanations when a limitation or conflict affects the current decision.
Support full acceptance, partial/revision requests, rejection, defer, undo and
free-text feedback. Treat preference as the user's judgment;
do not replace it with an automated aesthetic score. Keep active preview,
selected changes, displayed combination and applied source as distinct states.
Never pretend that switching a screenshot has recomposed the selected design.

In compare mode, stop after the concrete proposals and a concise selection
request. The user can adopt, retain, reject, defer or revise individual items.
Do not require the user to approve a vague direction before doing the already
authorized investigation and preview work.

Explain the handoff once: choose a proposal, optionally point to an element and
write what to take or preserve, then copy the request into the conversation.
The viewer's primary export is readable request text; JSON is an optional
structured copy. A partial choice requests a new proposal for that scope, not
the whole original proposal or automatic CSS extraction. Keep the user's accepted
preferences and reasons while building the next preview. When an element spans
shared styles or inseparable behavior, show that reach; clarify only a material
scope ambiguity. Partial choices are excluded from the accepted combination
until a revised, independently selectable result is reviewed. Do not turn free
text such as “just the spacing” into full adoption because a checkmark was also
present: reconcile the user's narrower intent before application.

For another round, carry forward the user's reasons and retained choices, keep
the original and last accepted state available, and give changed proposals a new
review identity. Prior approval does not transfer to a changed selected design
or impact; source drift needs reconciliation before carrying an unchanged choice
forward.
Continue by making another draft when requested; stop exploring when the user
stops, accepts the current result, or keeps the original. Do not force another
iteration or silently apply a sequence of drafts.

## Apply a selection

1. Resolve selected IDs and variants against the displayed comparison. Apply
   prerequisite bundles only if that scope was included in the selection; do not
   infer permission for an incompatible combination or an extra improvement.
2. Check current source in the selected area and affected dependencies against
   its baseline. If relevant source changed, reconcile it and refresh the
   affected proposal. Preserve concurrent work. Continue an already authorized
   change when its meaning and impact remain the same; obtain a new decision
   only when the earlier selection no longer describes the result.
3. Match the exact selected set to a real rendered result. If a combination is
   missing, build it in isolation and return an updated HTML review before
   application. Resolve dependencies and incompatible variants; do not silently
   add required changes, pick a conflicting winner, or stitch screenshots into
   supposed integration evidence.
4. Implement only the authorized changes using the project's existing stack and
   facilities. Do not introduce a new framework, plugin, generated asset service
   or design system merely to make the screen feel different. Update existing
   owner documents when the selected change alters a durable rule or behavior.
5. Compare the actual integrated result with the original and last accepted
   state at the relevant sizes and states. Check content and behavior
   preservation, keyboard/focus access, responsive layout and reduced motion
   where affected, plus applicable project checks. A good screenshot or passing
   lint alone does not establish usable behavior or better design. Return the
   HTML in applied mode with actual result DOM or necessary fallback evidence; its controls must not imply
   that rejecting a proposal now undoes already-applied source.

For a submitted JSON decision receipt, use the helper's `check` command against
the exact HTML and current source root before editing. Feedback-only exports
request exploration, not application. A stale artifact, changed source or
unrendered composition needs reconciliation and a refreshed review. A plain
language selection is also valid when it identifies the same reviewed result;
do not require JSON as a separate approval ceremony.

Repair regressions caused by the selected work within its authorized scope.
Report unrelated pre-existing problems separately rather than expanding into a
general audit. If the desired benefit does not survive integration, explain the
result and retain or restore only task-owned changes as appropriate; never roll
back another actor's work.

## Finish and retain only what is needed

Report the selected or retained outcome, the evidence for each comparison
question, checks actually run, and remaining visual or behavioral limits.
Distinguish a proposed benefit from one observed in a rendered comparison, and
both from human preference or measured user success. No detector count or
composite aesthetic score substitutes for this explanation.

Finish when the selected problem is addressed and the relevant checks pass, when
the original is the better-supported choice, or when a material choice needs the
user. Never force a change or another round solely to demonstrate improvement.
A no-change result still needs inspection proportional to the requested scope.

The HTML is a requested deliverable, not disposable work merely because the turn
ends. Prefer a self-contained local file outside the product checkout, or the
project's established private artifact owner. Keep the review, source snapshots
and selected preview material while selection or application is pending; state
their location, purpose and cleanup condition. Preserve an explicit durable owner
for later reuse before removing temporary copies. Once that purpose ends, remove
task-owned scratch and stop preview processes, preserving anything with uncertain
ownership or active use. Do not publish or add private screen contents to a public
repository, or create an additional permanent report, merely to deliver the HTML.

## Adjacent work

These are optional boundaries, not a required skill chain:

- If available, use `$init-design` when the requested deliverable is a durable
  design constitution for a new or deliberately reset design direction.
- If available, use `$design-plan` for coordinated, phased reconciliation across
  multiple screens rather than an isolated surface comparison.
- If available, use `$screen-alignment` for matching a known target or extending
  an existing system when interchangeable design is not the problem being solved.

Without those skills, use the project's existing process. Broader rebranding,
new product functionality and comprehensive audits require their own scope;
discovering them does not authorize their implementation.
