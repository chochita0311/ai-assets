# Source Evidence And Rule Promotion

## Contents

- [Intake And Source Roles](#intake-and-source-roles)
- [Inspect Within The Available Evidence](#inspect-within-the-available-evidence)
- [Extract Traceable Tokens](#extract-traceable-tokens)
- [Test Product Fit](#test-product-fit)
- [Promote And Hand Off](#promote-and-hand-off)

## Intake And Source Roles

Use the authority order in [method.md](method.md#source-priority). Keep a compact
source register in the constitution; put temporary capture work in task-owned
scratch. For each source used, record:

- an identifier and original locator: URL or project-relative file/section;
- revision, capture/access date, or another available snapshot identity; mark an
  unavailable identity as unknown rather than inventing one;
- its role: product base, creative intent, external inspiration, discovery lead,
  or derived analysis/export, and the source it derives from when known;
- actual observation scope: page/region, viewport or device, theme and state,
  plus whether evidence came from rendered inspection, source code, a still
  image, a recording, or a third-party description;
- material access or coverage limits that constrain the adopted rules.

A directory, award listing, repository catalog, or video recommendation is a
discovery lead. Follow a selected item to its actual screen, local artifact, or
source capture before treating it as visual evidence. An agency's location,
award count, thumbnail, or technology tags do not establish the design rules of
its work. Do not analyze the directory's own UI as the selected product.

A chosen external screen can seed a new product without a pre-existing app.
Pair it with the product context; state that it is an external seed. Separate
what the reference does from what the new product needs. If only leads or prose
are available, report the missing visual input and complete only supported
preparatory analysis instead of manufacturing an observed baseline.

Treat copied `DESIGN.md` files and structured style exports as derived analyses
unless their provenance establishes otherwise. Exported Markdown, CSS, JSON,
and previews from one analysis are one evidence lineage, not independent votes.
Distinguish an original component from a reconstructed example. Record external
references under their own names; do not overwrite the project's creative
source merely because an external file is also named `DESIGN.md`.

## Inspect Within The Available Evidence

Read the selected artifact with its surrounding screen context. When available,
compare rendered appearance with source styles or computed values. Record the
viewport, state, and inspected region before generalizing a value. A bounded DOM
capture or top-of-page screenshot does not describe an entire product.

Use existing read, browser, or extraction capabilities; a particular provider,
MCP server, or framework is not required. Check what a tool actually returned:
listing metadata, cached analysis, live screenshot, computed-style sample, or a
generated brief. Retain cache age, truncation, and failed capture limits when
they affect a decision. Tool installation and configuration are separate work.

When a source cannot be opened, use an available supplied copy or another
authorized observation path and identify it. Continue supported analysis; do
not describe an inaccessible screen or an unexecuted capture as inspected. If
the missing evidence determines a consequential rule, leave that rule open.

For videos, distinguish the observed frames/time ranges from heard or
transcribed narration. A tool demonstration establishes what is shown, not
that the tool was run in this project. A still cannot establish motion timing,
hover/focus behavior, or responsive transformation. A desktop frame does not
establish mobile behavior. Record those limits rather than silently filling
them with plausible values.

## Extract Traceable Tokens

For material tokens or coherent token groups, retain the source locator,
original value and context, chosen value, and reason for any normalization.
Use a compact table or an adjacent note; no separate evidence database is
required. Distinguish these bases:

| Basis | Meaning |
|---|---|
| Observed | Directly inspected in the supplied code, render, or capture; state which kind |
| Reported | Asserted by an external analysis or export; not independently measured here |
| Inferred | Deduced from repeated evidence; explain the supporting pattern |
| Proposed | Selected to fit this product where the source does not decide it |

These labels describe evidence, not approval. A measured source value may be
unsuitable for the product; a proposed adaptation may become an adopted rule
within the user's authorized baseline task. Keep open proposals out of locked
rules. Do not require separate user approval for every routine token decision.

- Extract repeated values and roles, then normalize only when it improves a
  coherent reusable scale. Preserve intentional exceptions and document the
  original-to-chosen mapping; neither every CSS literal nor a universal grid
  is automatically the right token system.
- Use source styles or measurements for exact values. Treat screenshot-only
  sizes, font identity, colors, and timing as estimates where they cannot be
  established; a neat hex code or numeric scale is not proof of accuracy.
- Keep a typography role's family, weight, size, line height, tracking, and
  usage together when their association is known. Do not zip independent font
  summary lists or infer missing tuple members from their positions.
  For nested text, inspect the text-bearing element and applicable source rules:
  a sampled link, button, or card container can have a different tuple from its
  label or heading. Trace descendant overrides and viewport conditions before
  calling the container's values the displayed text's values. If the available
  sample omits that text, inspect supplied DOM/styles or qualify the tuple as
  unresolved; do not substitute the wrapper measurement. Preserve material
  differences between text roles, or record the original-to-chosen change and
  product reason when deliberately normalizing them.
- Separate UI action/feedback colors from brand marks, illustrations, charts,
  or content imagery. Preserve a source's expressive palette when supported;
  do not promote every decorative color into an action token or impose a
  single-accent/minimal aesthetic on every product.
- Define primitive tokens as raw typed values with units where needed. Use
  neutral scale/value names for new primitives; map semantic names to them by
  product role, theme, state, and component usage. Respect existing naming
  conventions rather than renaming a valid system for style alone.
- Check that semantic aliases resolve to defined primitives, without cycles or
  conflicting definitions. Keep aliases and component rules consistent across
  themes, states, and any requested export formats. Ordinal extraction names
  such as `color-1` do not establish a primary action role.
- Check composed color roles as well as alias resolution. For each material
  text/control variant, trace foreground, background, and host surface through
  its required states, including local inverse surfaces. A page-family hover
  mapping does not automatically apply to every component variant. Check the
  actual pairs against the baseline's stated contrast requirements, compositing
  alpha where needed; merge equivalent pairs to keep the record compact.
  Compare thresholds with unrounded results. Generate displayed ratios directly
  from that calculation, rounding once at the chosen display precision rather
  than rounding intermediate results or re-rounding a shortened value.
  Resolve failing or missing required pairs with a scoped adaptation before
  locking the rule. Proposed states need this check too. Record the pair,
  applicable surface/state or text-size restriction, and actual check result;
  a general contrast requirement is not evidence that the mappings satisfy it.
  Static pair checks do not establish rendered interaction or accessibility
  conformance.
- Reconcile contradictions inside one source as well as between sources. For
  example, a radius table and prose guide can disagree. Consult the strongest
  available evidence or make an explicit product decision within scope; do not
  average incompatible values or present an unresolved claim as established.

## Test Product Fit

Preserve the source-supported visual character through hierarchy, composition,
imagery, density, typography, surfaces, and interaction emphasis, not just a
palette. Explain any intentional departure against the product's jobs, entities,
roles, states, device priorities, and technical constraints.

Check the rules against the supported screen families and required component
states. Include long or missing content, loading/empty/error results, keyboard
focus, narrow layouts, and reduced motion where relevant. Separate observed
source behavior from product-required adaptations; do not invent new fields,
roles, navigation destinations, or workflows to fill a template.

Use the project's accessibility and runtime requirements to check readability,
text/control contrast, focus visibility, touch and zoom behavior, motion, and
font/asset availability. Specify a workable fallback when a reference font or
asset is unavailable; do not silently add a dependency. Record actual checks
and their scope. A token table or aesthetic award alone establishes neither
accessibility nor implementation correctness.

Compare the proposed rules with existing rendered artifacts when possible.
Where rendering is unavailable, perform a source-based walkthrough and state
that limit. A representative specimen may help resolve a design decision when
authorized, but this workflow does not require building multiple screens or a
new preview app before delivering its documents.

## Promote And Hand Off

Adopt a rule when its evidence or explicit design rationale, product fit, and
reusable scope are clear under the active task authority. Keep adopted choices
and their basis in the constitution, including material source limitations.
Keep unresolved alternatives, temporary capture details, and implementation
sequencing in the response or the existing planning owner.

Update governance to name the actual creative source, external evidence, and
any derived token/code outputs. A future change to a reference site or export
does not automatically update locked rules. Explain the deliberate rule change,
update its owner, and synchronize derived artifacts only when in scope.

Finish with the two documents, the checks actually performed, material evidence
gaps, and a scoped handoff. When available, `design-plan` can own substantial
sequencing and `screen-alignment` can own implementation against the adopted
rules. Neither is required to complete this skill's document outputs.
