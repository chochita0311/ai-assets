---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-ui-native-host-evidence",
  "revision": 3,
  "audience": "public",
  "subjects": [
    {
      "kind": "harness",
      "key": "agents/policies/review/interaction-evaluation.md",
      "source_revision": "942bcb5bf493d781005060fd5ab1d8b0df925dee",
      "content_sha256": "9798d234258ffe44e20308ca9c2f3a2e51c755e998c5e2624f2da187616071c1"
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
      "ir-ui-requested-control-rendering",
      "ir-ui-state-transition-contracts",
      "ir-ui-initialization-recovery-evidence"
    ],
    "supersedes": []
  }
}
---

# Native host and end-to-end evidence

## Context And Applicability

This record asks what evidence establishes that a rendered action works across
an application's browser, embedded view, backend, and operating-system boundary.
The primary owner is [Interaction Evaluation](../../../policies/review/interaction-evaluation.md#native-host-and-end-to-end-action-evidence);
[screen-alignment](../../../skills/screen-alignment/references/method.md#step-10-browser-level-verification)
uses the same distinction when collecting rendered evidence. A generic web-only
product does not acquire a native-host test requirement from this example.

Use the lesson when packaging, startup, served assets, native actions, or
host-specific input are part of the affected contract. Distinguish source files,
bundled client assets, a frozen backend, and the running native shell, including
layers deliberately reused unchanged. Do not require every browser engine for
every product or treat useful partial probes as worthless.

The projection omits private app identities, runtime paths, authentication values,
and raw traces. It retains the checked segments and their limits. Metadata
identifies pre-change shared-source bytes, not the historical installed or loaded
instruction set, which was not established by the available receipts.

## Evidence And Evaluation

Private receipts reviewed on 2026-10-26 support the following reported events.
The review did not independently rerun their tests or retain their raw captures.

| Recorded event | Supported observation | Unverified or separate boundary |
|---|---|---|
| First packaged launch | Process/window checks passed while the owner received an authentication error and unreadable response text. The original frozen backend reproduced the failure; after repair, embedded-view checks covered fresh and previous-launch state, and the owner confirmed the normal app screen. | Corrected startup on that observed machine did not establish recipient-machine or full distribution acceptance. |
| Native chooser | API and bridge tests checked request handling, cancellation, errors, and duplicate invocation. Helper probes showed a native panel and cancellation; a confirmation attempt without a valid selection did not prove success. | The actual app button through valid native selection to updated draft remained unverified. Helper/API results could not close that gap. |
| Input probe | Operating-system events injected into an isolated embedded view reproduced a pointer-focus difference that ordinary browser checks did not show; the corrected sequence checked pointer and keyboard states. | Trusted events in the probe were not physical mouse input in the packaged app. This event supports an evidence-boundary lesson, not a second independent instance of the state-control correction. |
| Updated delivery layers | Different fixes refreshed client assets or rebuilt the backend while reusing the unchanged native shell; recorded checks named source/package parity and observed runtime responses. | Success in a fresh isolated target did not establish every already-running, concurrent-start, or mixed-version case. |

The historical stages were reported as **run**; public reproduction and a forward-test
of the revised guidance were **not run**. The new source comparison is static.
Reported scoped passes remain valid within their stated conditions, while broader
native acceptance gaps remain separate. An execution record being marked complete
does not change a partial or failed acceptance result into a full pass.

Illustrative future controls, not newly executed:

- Check the first meaningful page and required routes, including retained launch
  state when relevant; process startup or health success alone leaves UI usability
  unverified.
- Follow the actual Browse action through a valid selection and resulting draft;
  cancel preserves prior input when promised. Report mocked, helper, and full-host
  observations separately.
- Name host, served or bundled revision, and input source. Use a partial probe to
  support its observed segment while leaving missing end-to-end evidence open.

### Later Delivered-Path And Probe Evidence

Private receipts reviewed on 2026-11-06 add the following observed distinctions.
Raw captures, private runtime identities and associations remain private. Reported
product executions are not public reruns, and source validation of this revision
does not replace the product observations.

| Recorded condition | Evidence obtained | Boundary retained |
| --- | --- | --- |
| Fixture versus frozen delivery | A fixture that served already-styled content passed help visibility and labels. A private copy of the actual native host, using the original frozen backend through a diagnostic proxy with delayed styles, reproduced cached non-finite metrics and origin-pinned feedback. Later affected probes checked anchor coordinates and final bounds. | The proxy changed timing and appended diagnostic code to a controller asset. Original frozen assets/headers were checked separately; the diagnostic path was not an entirely unmodified app or physical hover. This is the style event in the [initialization record](initialization-and-recovery-evidence.md), not independent support. |
| Host identity after diagnostic packaging | The private app copy required re-signing. File-backed executable sections matched the production host while signature bytes differed; frozen-backend and served-asset identity had their own checks. | Code-section equality did not establish whole-file identity or recipient installation. Browser mocks and isolated engine observations remained separately scoped. |
| Disabled-control hit path | Computed DOM hit testing and pointer events reached a wrapper for disabled navigation controls; approved name/shortcut help remained while the actual hit cursor showed the forbidden state. Browser checks separately verified no activation; an installed-SDK routing check covered avoiding native window drag through that wrapper. | The checked no-action and SDK paths did not prove every physical hit path. Script events and SDK dispatch checks were named separately from operating-system input. |
| Probe interference | Earlier returns included a synthetic child target, lost activation and a focused skip-link covering the intended hit surface. Controlled activation and the normal hit surface produced the later scoped pass while earlier failures were retained. | These were probe-condition corrections, not additional product repairs or evidence of guidance effectiveness. A setup failure must be diagnosed rather than removed or silently counted as a product defect. |

Hidden embedded-view restoration also depended on suspended animation frames and
later queued work. That probe supported its observed functional sequence, not a
foreground physical interaction claim. Direct visual comparison with a named
reference application, real OS IME, recipient-machine behavior and an untested
operating-system build remained unobserved; source portability notes did not
close those gaps.

These events support a bounded diagnostic-condition clarification in the existing
host-evidence policy. The actual source baseline was compared with the accepted
import baseline before editing. No new runtime trials or guidance comparison
were run for this export; effect remains **not assessed**.

Source inspection for revision 3 used `policies/review/interaction-evaluation.md` at common-source
commit `19e14c8d48fc9ba3106219969f6ca70802479032`
(SHA-256 `ea936f4844073807d5a2152419608da0a783c8ab95ef5144c5f6f2f977e862c8`).
Historical subject fingerprints above remain unchanged. This identifies the
compared shared source, not the instructions loaded during product executions.

## Work And Acceptance

No separate runtime task or budget is assigned by this reference record. The
maintainer authorized the bounded source change, documentation checks, commit,
and push. Source acceptance requires truthful distinctions between checked
segments, supported environments, input mechanisms, and broader acceptance.

When a future task requires native acceptance, collect the missing actual-host
and end-to-end path or record the evidence gap under that task's acceptance owner.
Do not close it with a source comparison or substitute probe. A claim that this
new guidance improves agent behavior needs an actual execution with the intended
revision and relevant controls; that comparison remains not assessed here.

## Outcome And Reuse

Disposition: promote a native-host evidence subsection beside existing runtime
and asset-freshness checks, and add a bounded evidence step to the standalone
alignment skill. The supported lesson concerns what each observation establishes;
it is not a claim that all historical passes were invalid or that one probe can
replace the target host.

The primary agent reviewed the public projection for standalone meaning,
necessary detail, and private or revealing associations. Public-fitness approval,
draft case acceptance, and authorized source implementation remain distinct.
Original receipts stay at the originating project's private evidence owner;
public readers cannot inspect the private runtime evidence through this account.

Revisit if new actual-host evidence closes a gap or contradicts a recorded result.
Publication, consumer refresh, and observed activation are separate from the
source changes described here; no installation or future reliability is established.
Exchange provenance is session-only because no private exchange owner was
configured for this export.

Revision 3 implements only a bounded diagnostic-condition clarification at
the existing Interaction Evaluation owner. Existing host, input-mechanism and
layer-identity duties remain in force; no standalone skill change was necessary.
This export is local source maintenance with no commit, push or consumer refresh.
Its private exchange association is retained by the originating task owner;
the earlier session-only exchange statement remains historical.

## History

- 2026-10-26 — Revision 1. Matched the public collection and created one host-evidence
  record with one catalog row. Related state-control evidence is cross-referenced
  as the same event where applicable; this generalization is not a new execution.
- Revision 2, 2026-11-02: updated the current Interaction Evaluation link
  after its source relocation. Retained historical subject keys, source
  revisions and content fingerprints, observations and assessment states.
  Navigation maintenance adds no execution, empirical support or installation
  evidence.
- 2026-11-06 — Revision 3. Added delivered-path timing, diagnostic code/asset
  identity, disabled hit-surface and probe-interference evidence. Preserved
  earlier observations and physical/recipient limits. The source clarification
  does not imply a public reproduction, installation or improved agent outcome.
