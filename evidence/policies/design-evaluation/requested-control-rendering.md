---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-ui-requested-control-rendering",
  "revision": 3,
  "audience": "public",
  "subjects": [
    {
      "kind": "harness",
      "key": "agents/policies/review/design-evaluation.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "44c460dc47bd3f088739f8e4883a3df39ea95e665fc110898b5505bf15e93c49"
    },
    {
      "kind": "skill",
      "key": "skills/screen-alignment/references/method.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "fabc999818783a702bc22783ca470604f47650a936b1cbb0eb6be3d0200b1048"
    },
    {
      "kind": "skill",
      "key": "skills/screen-alignment/references/checklist.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "fdc1ba03efa0e12dc1b7bfe66c07c473a8a4cc0474ea4dd8f4f726f032bf2edb"
    }
  ],
  "work": {
    "basis": "not-applicable",
    "state": "not-applicable",
    "readiness": "not-applicable"
  },
  "knowledge": {
    "state": "supported"
  },
  "evidence": {
    "kinds": [
      "static-observation",
      "generalized-private-observation",
      "illustrative-synthetic"
    ],
    "maturity": "observed-stage-execution",
    "execution": "mixed",
    "coverage": "partial"
  },
  "adoption": {
    "public_fitness": "approved",
    "case_status": "draft",
    "rule_status": "implemented"
  },
  "relations": {
    "related": [
      "ir-ui-state-transition-contracts",
      "ir-ui-native-host-evidence",
      "ir-ui-initialization-recovery-evidence"
    ],
    "supersedes": []
  }
}
---

# Requested controls and rendered geometry

## Context And Applicability

This record asks how visual review can verify the relationship the user actually
requested when a nearby implementation passes its own checks. The primary owner
is [Design Evaluation](../../../policies/review/design-evaluation.md);
[screen-alignment](../../../skills/screen-alignment/SKILL.md) owns the standalone
alignment procedure. This account retains the evidence behind the source changes;
it is not a second rule authority.

Apply the lesson to placement, size, overlap, icon alignment, or unexpected scroll
extent within an approved interaction. Explicitly requested control replacement
or broader redesign remains valid under its own acceptance target. Exact control
sizes, icon angles, colors, shadow styles, and menu choices remain product decisions.

The public projection preserves the request-versus-result relationship and the
geometry that exposed the mismatch. It omits private identities, paths, images,
and product-specific dimensions. Metadata identifies the common-source baseline
before this refinement, not the instructions loaded during the historical work;
those historical instruction revisions and producer settings are unknown.

## Evidence And Evaluation

The following are generalized observations from private execution receipts,
reviewed on 2026-10-26. Original captures and probes were not available for this
review. The reviewer read recorded observations and did not reproduce the UI.

| Recorded event | Observation and correction | Limit |
|---|---|---|
| Dropdown placement request | A radio/search replacement did not satisfy the request to retain a dropdown and place its menu below the trigger. The corrected dropdown received rendered placement and interaction checks. | Tests of the replacement were scoped evidence for that replacement, not proof of the requested fix. Later owner preference changes are not automatically earlier defects. |
| Compact icon menu alignment | Equal container widths did not align the painted bounds of differently oriented glyphs. Later checks distinguished the frame from the visible artwork. | This supports inspecting the requested visible edges, not a universal icon shape or pixel width. |
| Blank scroll tail | Positioned, visually hidden accessible text contributed to document overflow. A local containing-block correction removed the recorded excess in a long-content fixture and app check. | The recorded checks did not establish every later-page navigation flow; deleting accessible text was not the repair. |

These are reported stage executions, not publicly reproducible runs. The current
source comparison is static. The rewritten public scenarios and controls below
were **not run** as UI tests, and no candidate-skill forward-test or comparable
rerun was performed. Historical improvements cannot be attributed to this new
common-source change. Repeated descriptions of an event add no independent support.

Illustrative controls for future use, with expected rather than observed outcomes:

- A placement-only request retains its dropdown and is checked while expanded;
  an explicit request to replace it with radio choices permits that replacement.
- Equal outer boxes with misaligned painted edges fail the named visual relation;
  a deliberately larger hit area remains valid when the artwork aligns.
- A long list reaches its real last item without a hidden descendant adding blank
  depth; needed accessible labels and intentional local scrolling remain usable.

### Later Painted-Icon And Compact-Host Evidence

Private receipts reviewed on 2026-11-06 add two rendered geometry observations.
The source review did not rerun their UI scenarios publicly; private captures and
product-specific dimensions remain at their original owner.

| Recorded condition | Observation and reported correction | Limit |
| --- | --- | --- |
| Bundled external SVG symbols | The controls and SVG elements existed and had nonzero geometry while glyphs were outside the visible viewport because nested symbol and outer viewport coordinates disagreed. Correcting that coordinate relationship restored the painted icons. | Element presence and a nonzero bounding box had not proved visible artwork. Locally bundled official vector assets and their license were distinct from an external font dependency; the lesson does not prescribe a particular icon provider. |
| Compact native layout | A narrow-layout rule changed sticky positioning while retaining a host offset already reserved by parent padding. The rail extended beyond the short window and pushed the footer offscreen; the host-specific positioning correction restored the intended frame and last controls. | A wide browser screenshot did not establish compact embedded-host reachability. Visible first controls did not establish the final item or footer. Exact reserved space and breakpoint values remain product-owned. |

The existing [painted-geometry check](../../../policies/review/design-evaluation.md#reference-geometry-uses-internal-insets),
[scroll-frame check](../../../policies/review/design-evaluation.md#bounded-scroll-frame-and-end-inset-integrity)
and [rendered viewport evidence](../../../policies/review/design-evaluation.md#rendered-state-and-viewport-evidence)
already require the relevant distinctions. This revision adds support and an
execution-gap example without duplicating those rules or changing the standalone
alignment skill. Pointer-origin feedback is covered by the related
[initialization record](../interaction-evaluation/initialization-and-recovery-evidence.md),
not counted as an additional geometry experiment. Guidance effect remains
**not assessed**.

Source inspection for revision 3 used `policies/review/design-evaluation.md` at common-source
commit `19e14c8d48fc9ba3106219969f6ca70802479032`
(SHA-256 `d92bae8dc81b1d57507e66c77eb56c40718c31da12976a80c876c9e2d253e3aa`).
Historical subject fingerprints above remain unchanged. This identifies the
compared shared source, not the instructions loaded during product executions.

## Work And Acceptance

This is a reference record, with no separately assigned execution task or budget.
The maintainer authorized integration into the common policies and skill procedure,
followed by documentation review, validation, commit, and push. Source acceptance
requires preserving the controls above, existing scope rules, and package ownership;
it does not require a new product runtime campaign or establish behavioral reliability.

When this guidance next governs affected UI work, compare the actual requested
control and rendered bounds at that product's supported states and viewports.
A broader reliability claim requires an identified instruction revision and an
actual task execution with relevant authorized-success and regression controls.
Unobserved conditions stay unverified; this record does not schedule that work.

## Outcome And Reuse

The source change adds [Requested Control Preservation](../../../policies/review/design-evaluation.md#requested-control-preservation),
extends [Reference Geometry Uses Internal Insets](../../../policies/review/design-evaluation.md#reference-geometry-uses-internal-insets)
and [Bounded Scroll Frame And End-Inset Integrity](../../../policies/review/design-evaluation.md#bounded-scroll-frame-and-end-inset-integrity),
and adds applicable verification steps to the standalone skill. The supported
lesson is that a similar control or equal CSS box is insufficient evidence for a
specific requested interaction or painted relationship. Improvement in future
agent performance remains **not assessed**.

Disposition: promote the bounded checks to their existing source owners. The
primary agent reviewed this public projection for standalone meaning,
necessary evidence, sensitive details, and revealing associations. Public-fitness
approval permits this generalized account; case acceptance remains draft, separately
from the authorized rule implementation. No private trace is published.

Original receipts remain with the originating project's private evidence owner.
Public readers cannot inspect those originals or reconstruct the private runtime
from this account. Revisit if new evidence contradicts a reported observation or
changes the applicable interaction contract. Source publication, consumer refresh,
and observed activation remain separate; this record establishes no installation
or runtime use. Exchange provenance is session-only; no private exchange owner was
configured for this export.

Revision 3 retains the existing rule implementation and draft case status.
It does not establish a new public UI reproduction, guidance-effect result,
consumer installation, commit or push. The new private exchange receipt stays
with the originating task; the earlier session-only receipt remains historical.

## History

- 2026-10-26 — Revision 1. Created a generalized reference record for requested
  controls and rendered geometry. Matching across the public collection found no
  existing record for this question. Added one catalog row; related state and host
  questions retain their own records. This migration is not a new UI execution.
- Revision 2, 2026-11-02: updated current Design Evaluation links after its
  source relocation. Retained historical subject keys, source revisions and
  content fingerprints, observations and assessment states. Navigation
  maintenance adds no execution, empirical support or installation evidence.
- 2026-11-06 — Revision 3. Added external-symbol paint and short native-rail
  evidence. Existing geometry/viewport rules were sufficient; this revision is
  evidence maintenance, with no additional design-policy or skill rule. Retained
  the earlier cases and their original evidence limits.
