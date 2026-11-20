---
{
  "format": "ai-assets-improvement-record",
  "schema_version": 1,
  "record_id": "ir-codex-review-challenger-validation",
  "revision": 6,
  "audience": "public",
  "subjects": [
    {
      "kind": "runtime",
      "key": "agents/adapters/codex/custom-agents/review_challenger.toml",
      "content_sha256": "0107df39d140e2fe15256c88c4e6b028e8ee4da7d25c276d8fdf0bdfe5f52140",
      "source_revision": "17e414f69d3323df98c2191b217fb4c3241e0350"
    },
    {
      "kind": "runtime",
      "key": "agents/adapters/codex/custom-agents/research_worker.toml",
      "content_sha256": "772de526484aa28abc2292f71456fa2b038f271a05d1a4bbe262c726ccb98fcd",
      "source_revision": "526a681f455230946bfde18a0493fc1bf3f2eeeb"
    },
    {
      "kind": "skill",
      "key": "skills/refactor-plan/SKILL.md",
      "content_sha256": "7ec3b5aacb76566d4a72b38cfaa706cf3eb2a8b4d3f2b456ed2951f575c14d9a",
      "source_revision": null
    },
    {
      "kind": "resource",
      "key": "skills/refactor-plan/references/method.md",
      "content_sha256": "4ac7b84807eeba31d7dd863e51aa30a4c493b05856c1d44915c48b94f417ef93",
      "source_revision": null
    },
    {
      "kind": "harness",
      "key": "agents/policies/harness/execution-loop-governance.md",
      "content_sha256": "f21adfc6f3b1605434de968b147babb334bdf9eb8e846e88b3fad7a7bdadb906",
      "source_revision": null
    }
  ],
  "work": {
    "basis": "evidence-gap",
    "state": "open",
    "readiness": "waiting"
  },
  "knowledge": {
    "state": "candidate"
  },
  "evidence": {
    "kinds": [
      "static-observation",
      "generalized-private-observation"
    ],
    "maturity": "fresh-forward-test",
    "execution": "mixed",
    "coverage": "partial"
  },
  "adoption": {
    "public_fitness": "approved",
    "case_status": "not-requested",
    "rule_status": "not-proposed"
  },
  "relations": {
    "related": [
      "ir-pr-review-semantic-corpus",
      "ir-research-sadr-validation"
    ],
    "supersedes": []
  }
}
---

# Codex review-challenger runtime validation

## Context And Applicability

Validate the optional [Codex review challenger](../../../agents/adapters/codex/README.md#review_challenger)
before relying on its named binding, independence or omission benefit. This
runtime role supplements evidence scouts and exact-command verifiers with
semantic candidate discovery. It is an omission-only support role; the
[portable PR-review skill](../../../skills/gh-review-pr/SKILL.md#run-directly-or-as-a-delegated-reviewer)
can also be executed directly or by a full-task delegated reviewer without it.

In the earlier trials, the role file selected `gpt-6.1-sol` / `max` and four
optional feature reductions. Configuration is not proof of effective model,
competence, cost or context isolation. The
[adapter](../../../agents/adapters/codex/README.md#review_challenger)
owns binding, installation, reasons and tradeoffs. Task contracts own risk
routing and semantic gates: [refactor-plan](../../../skills/refactor-plan/SKILL.md)
for local refactor checkpoints, [execution-loop governance](../../../harness/policies/execution-loop-governance.md#independent-code-challenge)
for approved-feature implementation, and the PR-review skill for its own domain.
The primary remains the decision owner. This record reports evidence; it does
not install a global router, adopt a universal rule or authorize model replacement.
It also holds the shared Codex configuration, installation and named-runtime
evidence for the Sol upgrade. [Research SADR validation](../../skills/research-sadr/research-validation.md)
owns the research method's acceptance question.

## Evidence And Evaluation

### Source-only baseline — 2026-10-31

The source-only audit parsed all four adapter TOMLs, verified required fields
and feature booleans, and passed seven offline audit/renderer tests. The
[manifest fixture](../../../scripts/test_model_binding_audit.py) checked that the
existing discovery glob includes a distinct worker binding without changing the
audit profile's model. It invoked a synthetic Codex executable, not the actual
worker. This is the same seven-test resource check counted in the
[semantic record](../../skills/gh-review-pr/pr-review-semantic-corpus.md), not
another semantic trial or independent evidence of runtime quality.

The first adapter audit returned PASS WITH SUGGESTIONS for explaining optional
restrictions; the explanation was added without changing binding or flag values.
The final independent refine audit returned PASS for static and resource checks,
Evidence Coverage partial, highest evidence resource execution. It found no
reason for further document restructuring. The [official custom-agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agent-file-schema)
supported the declared fields; account access, actual loading and effective
permissions were not observed in that audit. The record refresh at that
checkpoint reused the results of those checks.

At that checkpoint, the TOML hash identified an uncommitted candidate and its
`source_revision` was null. No shared harness routing, repair-loop budget or
escalation service had been added, and no runtime installation, named invocation,
cache activation or routing trial had been performed in that evaluation. The
two generic delegated reviews in the semantic record did not invoke this role
and do not validate its binding or omission benefit. Original results remain in
the originating conversation; that audit's task-owned scratch was removed.

### Bounded local executions — 2026-11-02

The following are generalized observations of actual local synthetic executions,
not illustrative unrun examples or public deployment. Two initial calls invoked
the actual registered `review_challenger` with no inherited conversation on two
frozen local Python standard-library fixture families. Raw first-discovery packets excluded author conclusions
and expected findings.

- In a high-risk dependency/consumer parity case, the fresh reviewer identified
  two regressions and returned bounded execution requests. Separate authorized
  runtime checks supported the reported behavior.
- In a legitimate-zero case, the reviewer distinguished an authorized delta and
  pre-existing behavior from a new regression.
- An ordinary producer using frozen refactor-plan without a harness requested
  the high-risk named challenge. Low-risk work stayed with the primary; general
  code review did not enter the refactor workflow. A controlled no-delegation
  setting retained the required-independence acceptance gap.
- A separate informed adjudicator refuted an invalid comparison using equal-input
  checks, rather than treating the critic's conclusion as a product defect.
- A third named call used no inherited conversation but explicitly received the
  prior return and observations. It was informed repair confirmation, not blind
  discovery. It distinguished the original baseline, moved current branch,
  previous candidate and repair; identified narrowly restored behavior, a carried
  defect and an additional destructive alias boundary. Independent producer
  runtime evidence supported those claims. The alias observation was additional
  evidence, not a retroactively preregistered must-pass criterion.

The exact source-root-equals-store replay was not separately executed. Source
tracing, same-path intake and hard-link replay support only their stated scope.
A directory inventory exposed extra task-local metadata filenames during the
informed follow-up. No contents or live state from those entries supported the
conclusions; this boundary exposure prevents claiming a fully sealed packet.
These synthetic observations are not new findings against a user project.

Named invocation and no-history input delivery were observed. Source manifests,
instruction revisions and content fingerprints were recorded with the private
task evidence. The challenger reported that it did not execute reviewed code;
execution validation was performed separately. The full child action trace,
hidden effective model/provider/permissions, capability reductions and cached
activation were not independently exposed. Earlier source/runtime-copy equality
checks are historical installation input, not proof that all runtime flags were
effective. Requested or configured settings must not be reported as observed.

At the November 2 checkpoint, the TOML matched its verified committed source
byte for byte. The subject metadata records that commit while preserving the
original uncommitted observation in its earlier scope.
The refactor-plan entry, method and harness-policy hashes identify those
snapshots at the same checkpoint. They were uncommitted candidates then,
hence null source revisions; later source edits or publication do not relabel
those historical fingerprints as the current files.
Only original reported observations, source/input identities and reviewer returns
are recorded in the originating task conversation. Diagnostic snapshot files
were removed after their evaluation and recovery purpose ended; no
persistent or reproducible fixture bundle is promised. This public projection
includes no private fixture identities or traces.

Evidence Coverage remains **partial**; the highest level reached is
**fresh-forward-test**. Evidence execution is mixed: the dated offline checks
and local synthetic trials ran; remaining runtime, access and comparison checks
below did not. The final independent refine audit returned **PASS** for frozen-v2
preservation and the observed controlled tasks, with partial coverage of the
broader acceptance envelope. The observations support a bounded candidate
conclusion that the role can contribute
useful candidates under these inputs. Per-edit effect is **not assessed**:
there is no comparable before/after control, quantified cost, general project
rollout or demonstrated stability. Instruction-following routing in these trials
does not establish automatic product-wide activation or universal omission benefit.
Exploratory planning-only behavior and the approved-feature harness code gate
were checked statically, not in separate runtime tasks.

### Retained ordinary refactor task — 2026-11-02

An earlier ordinary refactor skill task detected an error-semantics regression.
Independent reproduction covered 44 differential cases: 28 behaved the same
and 16 differed. The producer output did not include the predeclared rubric's
literal `pending` input, so that specific rubric check remains unmet. The task
and skill did not require that literal, and an equivalent non-ready-state
branch was exercised. The rubric's overly specific condition does not itself
establish a task failure.

This is retained task evidence, not another observed named-runtime trial or a
whole-scope parity result. Full context and tool history were not independently
verified, and no comparable earlier-version control established improvement or
general stability. Keep these 44 comparisons separate from the later repair
measurements below; their relationship does not establish an additional
independent-trial count. The retained report does not replace the deleted raw
task artifacts with a replayable fixture.

### Retained payload and repair observations — 2026-11-02

A later payload audit retained a synthetic dependency/consumer case, actual
named challenger returns, informed objection adjudication, and a moving-current-
branch repair check. The adjudicator supported both original regressions and
calibrated the replacement finding from high to medium while keeping it
blocking under the explicit parity requirement. The partial repair restored
eight earlier label failures, but the fixed baseline passed 36 of 36 differential
checks while the repaired candidate passed 24 of 36; replacement of a small
existing target still failed. Both supplied test suites passed, so their success
did not establish whole-scope parity. Full baseline-to-current and previous-
candidate-to-repair comparisons remained distinct.

The delivery contract and functional results remained FAIL for the synthetic
implementation defect and routed to targeted fix under the existing spec, not
to an invented planning or specification gap. A separate fresh documentation-
only control returned no qualifying finding and required no reviewed-code
execution. An offline feedback audit separately rejected an invalid test
counterargument and distinguished a pre-existing defect; the PR-specific
evidence is retained in [the semantic corpus record](../../skills/gh-review-pr/pr-review-semantic-corpus.md).

These are retained observations from the same development effort, not a new
public fixture suite or another completed runtime-acceptance matrix. The
relationship of every continuation to the earlier trial families has not been
reconstructed from raw logs; do not count this summary as additional independent
trials or duplicate support. The follow-up was informed, and no fresh review of
the complete repaired pair or general project deployment was established. Raw
task-owned audit bundles were deleted after integration; the conversation
retains the reported results and limits. The broader checks below remain open.

### Later application review and informed integration confirmation

A later generalized private application task invoked three registered
`review_challenger` instances on distinct input/rendering, state-continuation and
process/resource questions. The initial packets requested no inherited history,
frozen full-source inventories and bounded read-only inquiry. They withheld
prior review conclusions, but normative requirements exposed some historical
closure claims; one early live-tree lookup was disclosed and its output excluded.
These qualifications limit answer isolation even though supplied manifest hashes
matched. Instruction restrictions and reported read/search/hash conduct were not
an independently enforced OS sandbox or a complete child action trace.

Returned candidates led to primary-owned browser/PTY and process probes. Those
probes supported focus/cursor and authority defects, detached query behavior,
unbounded automatic-reply buffering and identity/setup gaps. Informed rounds then
challenged repair-side duplex progress, read-only focus, interrupted-input
feedback and background fault visibility. The primary made the fixes, selected
acceptance and ran the checks; a worker supplied neither implementation nor
completion approval. Later turns and repeated source hashes do not multiply the
initial independent inquiry count.

A proposed wrong-target-descriptor consequence remained unobserved: the suggested
OS trigger did not produce master closure. Controlled close plus real descriptor
reuse supported the added guard's boundary without proving the proposed OS
failure. A final timezone false-positive was primary-discovered and received
only narrow informed confirmation. The [research record](../../skills/research-sadr/research-validation.md)
describes the same task's method use, not additional independent replication.

The configured role/model/effort was known, while actual provider internals,
cumulative cost, complete hidden context and effective capability reductions
were not exposed. Private scoped checks eventually passed; no public replay,
causal role-benefit comparison or complete runtime-acceptance matrix ran for this
export. Keep the open evidence requirements and historical subject identities
below; a successful private application review does not close them.

### Sol binding migration

GPT-6.2 Sol became available in Codex on 2026-11-17. The November 20 audit
still found 6.1 Sol listed, with no retirement identified. The user then
approved upgrading `review_challenger` and `research_worker` to 6.2 Sol. Both
local Codex homes already defaulted to `gpt-6.2-sol` / `max`, and both catalogs
supported that effort. At that point the named roles explicitly selected
`gpt-6.1-sol` / `max`. All four installed regular files matched their canonical
TOMLs. [Release announcement](https://learn.chatgpt.com/docs/whats-new/gpt-62-astra-sol) ·
[Codex model catalog](https://learn.chatgpt.com/docs/models?surface=cli)

The migration changed the `model` keys of the two role TOMLs to `gpt-6.2-sol`
and retained `max`. After atomic replacement, the four regular files matched
their source bytes and retained their file modes. The current session's tool
registry exposed both updated named bindings. TOML parsing, the model-only
diff check and seven offline model-binding audit tests passed. Focused
exploration, bounded verification and the optional audit profile use separate
Luna bindings. The audit profile was present only in the repository for these
two homes.

The isolated role-matched smoke test required before replacement did not run.
The initial migration also ended before fresh named execution in either
installed home. The user approved retaining the installed settings and running
the named-worker checks during closeout as late verification. The subject
metadata preserves the earlier `review_challenger` source and the
`research_worker` baseline checked before the upgrade. Both are 6.1 Sol
configurations. [Controlled migration procedure](../../../agents/adapters/codex/model-binding-audit.md#controlled-migration-after-an-alert)

#### Late named-worker verification

Codex CLI 0.170.0 opened one fresh, ephemeral app-server session per installed
home. Each session loaded that home's installed role TOMLs in an isolated
configuration under its existing account. The parent used Luna, a read-only
sandbox and no approval prompts. The probe kept the normal user instructions
and connectors out of the test sessions. The named-worker requests called for
fresh context and used only public method files and synthetic fixtures.

Structured child activity reported `gpt-6.2-sol` / `max` at start for
both named roles in both sessions. All four child turns completed, and each
emitted cumulative token usage. The first receipt parser missed the child
activity items. The results were verified directly from the captured start,
completion, action and usage events.

- Both research workers verified the method files and hashed the two input
  extracts. They found that repetition raised the completed-row rate from
  `2/4` to `5/7`, while both extracts still contained `2/4` distinct completed
  tasks. The source of the repeated rows remained unresolved.
- Both review challengers identified the missing-title and null-title path in
  a frozen render change. The baseline returned a placeholder. The candidate
  called `.strip()` on `None` and would raise `AttributeError`. Both reports
  traced the caller and retained a normal string-title control. The code was
  inspected statically.

The parent sandbox and approval settings were visible, and recorded worker
actions stayed within the synthetic task. The probes establish named execution,
bounded fixture behavior and per-child token reporting under those conditions.
Hidden context, full child capability enforcement, connector-only controls,
ordinary-session behavior and billed cost remain open. No comparative result
between 6.1 and 6.2 Sol was measured.

## Work And Acceptance

### Eligibility And Authority

Work remains open, waiting on the unresolved evidence below. No further test
performer is assigned. Before selecting another check, resolve its specific
question, raw immutable artifacts, accessible evidence, action authority and
finite budget. A future runtime target or installation change must be explicitly
authorized. Source changes or this record do not authorize personal installation,
live GitHub writes, schedule activation, commit/push or model replacement.

### Remaining Checks

- Preserve historical source/runtime-copy equality evidence. For any authorized
  installation or update, follow the adapter's [installation and recovery procedure](../../../agents/adapters/codex/README.md#installation-boundary),
  preserve unrelated destination content, capture prior state, and verify
  regular-file copies and exact source equality in every approved runtime home.
- In a fresh session, complete named-runtime proof under the settings in scope.
  Verify actual model and effort, effective instructions and revision, cached
  activation, inherited permissions, all capability reductions and observable
  usage. The earlier 6.1 Sol trials observed named calls and no-history packets.
  The late 6.2 Sol probes observed named execution, model and effort, and token
  usage in isolated sessions. Generic invocation, successful reads, configuration
  equality or worker self-report cannot fill the remaining fields. Retain
  justified-routing and primary-retention results within their tested conditions.
- Confirm behavioral limits with sufficient action evidence: raw-evidence
  discovery without author discussion or expected findings; no edits,
  reviewed-code execution, publication, acceptance decisions or further
  delegation; bounded validation requests and explicit gaps. The current
  separate-validation evidence and challenger self-report do not expose the
  entire child trace.
- Retain the observed cross-file/consumer, legitimate-zero and invalid-comparison
  controls. Additional duplicate/repeated-concern controls, measured omissions,
  false positives and actual cost remain open, as does any comparable
  before/after claim. The primary adjudicates every candidate under its contract.
  Test the exact alias replay separately if a broader claim depends on it;
  do not expand the completed trial's original acceptance criteria afterward.
- Compare a complete local packet with an app/plugin-only evidence need; that
  control has not run. Confirm an authorized completion path or explicit gap.
  Disabled memories do not remove passed conversation, and disabled permission
  requests do not create an independent sandbox.

### Completion

Close only after the required named-runtime and semantic controls have observed
results and adverse outcomes are resolved or deliberately withdrawn with reasons.
Preserve unavailable model, context, permission, capability-access and cost
proof as gaps. Official lifecycle drift or an actual binding mismatch triggers
reviewed replacement evaluation, never silent substitution. Resume only for a
bounded unresolved question with new evidence or changed conditions; this
record starts no further trial by itself.

## Outcome And Reuse

The earlier work completed the source adapter and explanatory documentation.
Its trials observed named local use and bounded semantic controls on the 6.1
Sol binding. They left the configuration in place and included no push,
publication or consumer rollout. The later [binding migration](#sol-binding-migration)
established the source and local installation of 6.2 Sol. The late named checks
observed bounded execution in isolated sessions that loaded each home's
installed role files. Full runtime
acceptance, broader semantic utility and cost remain open. Static compatibility
and partial runtime use do not establish all configured behavior or a stable
improvement.

Keep actual configuration and installation instructions with the adapter, and
risk routing and semantic decisions with the task owners. Reuse this existing
record for the evolving verification question; its candidate conclusion does
not adopt a universal review rule. Original evidence stays in the originating
task conversation. Public reproduction or deployment needs its own evidence.

Revision 5 adds bounded application-use evidence without changing the adapter,
model binding, existing work/readiness or acceptance states. Original per-task
returns, first discoveries and informed dispositions are retained privately;
older deleted-diagnostic statements above remain scoped to their dated cases.
The primary reviewed this projection for necessary meaning and public fitness,
not as independent runtime attestation or proof of the role's general benefit.

## History

- Revision 1, 2026-10-31: retained the reviewed source configuration, bounded
  static/resource results and pending named-runtime/semantic acceptance.
  Public-fitness review found only portable source identities, synthetic
  observations and generalized checks; no private runtime paths, identifiers or
  transcripts were copied. Creation of this record was not a runtime execution,
  installation or approval to replace the model.
- Revision 2, 2026-11-02: added generalized actual named, routing, adjudication and
  informed repair observations; scoped the earlier no-invocation/no-routing
  statements to their original checkpoint and recorded the unchanged committed
  TOML identity. Retained incomplete runtime/access/comparison evidence and open
  work. This updates the same question and record; it is not another independent
  count of the old seven checks, a causal improvement claim or rule adoption.
- Revision 3, 2026-11-02: preservation review restored the explicit fresh-session
  and instruction-revision requirements. No new trial ran and no runtime result
  changed.

- Revision 4, 2026-11-02: reconciled the retained ordinary refactor task and its
  unmet rubric detail, repair, delivery routing and legitimate-zero observations,
  clarified historical subject fingerprints and
  completed scratch cleanup, and preserved runtime/comparison gaps. This
  reconciliation ran no new challenger trial and adds no independent trial count.

- 2026-11-12 — Revision 5. Added frozen application inquiry and informed integration/closure confirmation. Preserved disclosed context exposures, primary-owned execution, unobserved descriptor consequence and provider/cost gaps; no new worker trial or binding change in this export.

- 2026-11-20 — Revision 6. Recorded the approved Sol binding migration and the
  configuration, copy and registration checks. Recorded the missed pre-install
  test and the subsequent user-approved named checks. Kept the 6.1 Sol results
  scoped to their original trials and the 6.2 Sol results scoped to the late
  synthetic probes.
