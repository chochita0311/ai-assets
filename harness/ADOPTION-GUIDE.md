# Harness Adoption Guide

## Purpose
- Explain how to adopt this shared harness package into a consuming repo.
- Keep the export pattern repeatable without turning the package into repo-specific automation.
- Record enough per-repo import state to distinguish later upstream changes from intentional local changes.
- Keep personal Codex runtime installation separate; use [runtime adapter](../agents/adapters/codex/README.md) for global Codex policy and custom-agent bindings.

## When To Use This Guide
- A consuming repo does not yet have the harness package.
- A consuming repo has an older local copy and needs a controlled sync from the selected sources in `../ai-assets/`.
- The operator wants the resulting repo to look like a normal local agent system, not like a mounted external dependency.

## Adoption Mode Resolution

The per-repo import baseline is defined in [Harness Import Manifest](#harness-import-manifest). Resolve the mode before writing:

- No manifest and no installed local harness: use `Fresh Export`.
- No manifest but local harness files already exist: use `Existing Installation Bootstrap`.
- Valid manifest exists: use `Refresh Or Resync` from the recorded baseline.
- Invalid manifest exists: use `Manifest Recovery`; preserve it and stop before harness-content writes.
- A missing or invalid manifest is never proof that existing local files are safe to overwrite.

### Manifest Recovery

When an installed manifest fails schema, path, uniqueness, hash, or provenance validation, preserve it unchanged as evidence and do not use any of its values as a refresh baseline. Build and validate a separate recovery candidate from supported source, target, and Git evidence, using the evidence steps from `Existing Installation Bootstrap` when needed. Resume controlled refresh only after the recovered baseline candidate is valid and every unexplained difference is classified; replace the installed manifest only as the final successful step.

### Existing Installation Bootstrap

When a repo already has imported harness files but no manifest:

1. Inspect the consuming repo's entrance docs, current harness layout, Git history, and repo-local ownership rules.
2. Resolve the intended repository surfaces and optional capability exclusions.
3. Identify the previous harness-only import or refresh commit and its `ai-assets` revision when possible.
4. Render the candidate shared source into the consuming layout before comparing it with current targets.
5. Classify exact or historically supported shared matches as `managed`.
6. Classify confirmed intentional specializations as `local`.
7. Treat unexplained differences as conflicts. Do not overwrite them or manufacture baseline hashes.
8. Complete the controlled merge and finalization checks.
9. Create the manifest only after every tracked entry has a supported source, target, ownership, and baseline.

Bootstrap existing installations lazily on their next refresh. Do not require an immediate repository-wide migration solely to add manifests.

## Shared Source Package
- Source locators use `../ai-assets/` as the repository root. The harness package lives in `../ai-assets/harness/`.
- Harness governance lives in `../ai-assets/harness/policies/`; shared competence and review policies live under `../ai-assets/policies/`.
- Shared execution profiles live in `../ai-assets/harness/profiles/`.
- Shared templates live in `../ai-assets/harness/templates/`.
- The optional research method source lives in `../ai-assets/skills/research-sadr/`;
  its complete pinned package is selected with capability `research`.
- Public improvement records live in the repository-level `../ai-assets/evidence/`
  layer, selected by record ID under the current owner domains defined by
  [Public Record Placement](policies/improvement-record-contract.md#public-record-placement).
- The generalized import-manifest example lives at `../ai-assets/harness/harness-import-manifest.example.json`.
- Runtime adapters, shared instruction bundles and prompt presets remain under `../ai-assets/agents/`; they are not imported by this guide.

## Target Shape In A Consuming Repo
After export, the consuming repo should normally own the selected targets
below. Create only locations required by the resolved selection:

- `docs/agents/`
  - `harness-import-manifest.json`
  - `roles/`
  - `flows/`
  - `operations/`
  - `profiles/`
  - `templates/`
    - non-persistent agent response scaffolds such as `operator-briefing.md`
  - `methods/research-sadr/` when `research` is selected
    - complete pinned method package, loaded directly from its `SKILL.md`
- `docs/plans/` when delivery planning or execution artifacts are selected
  - `prd/`
  - `feature/`
  - `spec/`
  - `run/`
  - `evaluation/`
  - `fix/`
  - `heuristic/`
- `docs/policies/harness/`
  - shared workflow routing, planning, execution, profile, traceability, operator-continuity and research governance as required by the selected flows and capabilities
- `docs/evidence/`
  - local experience outputs and separately owned selected public references when Harness Improvement is enabled
- `docs/policies/design/` and `docs/policies/experience/`
  - review assets when the consuming repo wants durable visual and interaction evaluation rules

When Harness Improvement is selected, its blank record templates live under
`docs/agents/templates/`, its metadata schema under `docs/agents/schemas/`, and
explicitly selected public records under
`docs/evidence/<domain>/<component>/`, preserving the source's `harness`,
`agents`, `policies` or `skills` domain from
[Public Record Placement](policies/improvement-record-contract.md#public-record-placement).
Completed bindings,
stage records, indexes, improvement records, receipts and experiments are
consumer-owned outputs in the same `docs/evidence/` layer: `STORE.md`, `stages/`,
`improvements/` and `experiments/`, or an existing configured equivalent. These
local paths are ignored and excluded from the import manifest. Follow the
[local layout policy](policies/harness-improvement.md#consumer-evidence-layout)
for ownership, exclusions and discovery; shared refresh must preserve them.

## Export Mapping
Resolve optional capability selection before expanding any wildcard. Mapping
v10 uses repository-relative source locators and preserves the existing consumer
roots. Use this resolved source-to-consumer map for the selected file set:

- `harness/roles/*.md`
  -> `docs/agents/roles/*.md`
- `harness/flows/*.md`
  -> `docs/agents/flows/*.md`
- `harness/operations/*.md`
  -> `docs/agents/operations/*.md`
- `harness/profiles/*.md`
  -> `docs/agents/profiles/*.md`
- `harness/templates/prd.md`
  -> `docs/plans/prd/template-prd.md`
- `harness/templates/feature.md`
  -> `docs/plans/feature/template-feature.md`
- `harness/templates/spec.md`
  -> `docs/plans/spec/template-spec.md`
- `harness/templates/run.md`
  -> `docs/plans/run/template-run.md`
- `harness/templates/evaluation.md`
  -> `docs/plans/evaluation/template-evaluation.md`
- `harness/templates/fix-log.md`
  -> `docs/plans/fix/template-fix-log.md`
- `harness/templates/heuristic-backlog.md`
  -> `docs/plans/heuristic/template-heuristic-backlog.md`
- `harness/templates/operator-briefing.md`
  -> `docs/agents/templates/operator-briefing.md`
- `harness/policies/*.md`
  -> `docs/policies/harness/*.md`
- `policies/competence-first-delegation.md`
  -> `docs/policies/harness/competence-first-delegation.md`
- `policies/review/design-evaluation.md`
  -> `docs/policies/design/design-evaluation.md`
- `policies/review/interaction-evaluation.md`
  -> `docs/policies/experience/interaction-evaluation.md`

The current delivery files are `harness/flows/delivery.md` and
`harness/operations/delivery-runner.md`; their consumer filenames are
`docs/agents/flows/delivery.md` and `docs/agents/operations/delivery-runner.md`.
Existing `workflow.md` and `runner.md` targets follow the
[v10 migration procedure](#upgrading-existing-mappings-to-v10), rather than being
silently duplicated or deleted.

Whenever shared roles or flows are exported, include all five common dependencies:

| Source | Consumer target |
|---|---|
| `harness/roles/orchestrator.md` | `docs/agents/roles/orchestrator.md` |
| `harness/policies/workflow-governance.md` | `docs/policies/harness/workflow-governance.md` |
| `policies/competence-first-delegation.md` | `docs/policies/harness/competence-first-delegation.md` |
| `harness/policies/operator-briefing-and-review-receipts.md` | `docs/policies/harness/operator-briefing-and-review-receipts.md` |
| `harness/templates/operator-briefing.md` | `docs/agents/templates/operator-briefing.md` |

The common orchestrator and workflow governance own flow selection, transitions,
permissions and shared resource decisions. They remain required whether research
is selected or omitted; installing them does not select any optional flow or
Harness Improvement. Each selected flow retains its own lifecycle and acceptance
contract. Load only selected flow contracts and render conditional references to
omitted flows as meaningful plain text; a shared dependency never creates a
wildcard opt-in or a requirement to install a sibling flow.

The `policies/baseline/` sources and runtime `agents/` packages are outside
this export. Marked runtime sections inside exported policies remain
policy text; exporting them does not merge any global instruction file. Shared
bundle generation and runtime installation are separate from harness adoption.

Do not export `harness-import-manifest.example.json` as a managed shared file. Use it to initialize the consuming repo's own `docs/agents/harness-import-manifest.json` only after the fresh export and its finalization checks succeed.

`harness/ADOPTION-GUIDE.md` is a source-only import/refresh administration
contract, not an additional selected payload file. Its administrative references
follow the narrow [v10 rendering rule](#current-mapping-v10) below.

### Optional Research

Select capability `research` explicitly before expanding role, flow, operation,
policy or template selections. Mapping v10 includes this four-file core and the
complete method bundle; sources below are relative to the repository root:

| Source | Consumer target |
|---|---|
| `harness/flows/research.md` | `docs/agents/flows/research.md` |
| `harness/operations/research-runner.md` | `docs/agents/operations/research-runner.md` |
| `harness/policies/research-governance.md` | `docs/policies/harness/research-governance.md` |
| `harness/templates/research-state.md` | `docs/agents/templates/research-state.md` |
| `skills/research-sadr/**` | `docs/agents/methods/research-sadr/**` |

Resolve and enumerate every actual method package file at the selected source
revision, including `SKILL.md`, references and metadata. Preserve its internal
structure, bytes and relative links unchanged; exclude scratch, caches and
unrelated placeholders. Track every file separately in the manifest with its
source revision and source/rendered hashes. Preserve any declared method/package
version metadata verbatim; do not substitute an installed same-name version.
Each byte-preserved method file has equal `source_sha256` and
`rendered_sha256` at its accepted baseline. The method source remains owned by
`skills/research-sadr/`; this managed copy is not a second method contract.
Include all five common dependencies above, including the common orchestrator
and workflow governance. Research-controller responsibilities are retained there
and in research governance; v10 does not install `research-orchestrator.md`.
An existing copy is a retirement candidate subject to the
[v10 migration procedure](#upgrading-existing-mappings-to-v10). Verify the entire
method bundle and its local links.

The complete bundle is the required project-local method installation. The flow
directly loads `docs/agents/methods/research-sadr/SKILL.md`; native skill discovery
is separate and no `.agents/skills` entry is required. Adoption
does not install a personal runtime skill, activate automatic discovery, add a
model binding or establish that an installed same-name skill is the pinned
revision. Never substitute a globally discovered same-name skill for this pinned
method. No external `ai-assets` checkout is needed for ordinary research.
State uses one existing authorized owner or session/task-owned scratch; installing
the scaffold creates no durable research record or directory.

When research is not selected, omit all four core files and the method bundle,
record `research` in `selection.excluded_capabilities`, and render conditional
peer references as meaningful plain text. Preserve the common controller and
shared routing dependencies and any selected delivery flow. On refresh, preserve
resolved selection unless a change is authorized.
Absence of `research` from an older manifest's exclusions, including mapping v8,
is not opt-in: inspect its tracked files and actual installation evidence.
Uninstalled research stays disabled; partial installations retain bootstrap,
ownership and conflict handling. A coincidentally named local file is never
permission to overwrite it. Omitted previously tracked files still follow the
retirement rules.

Research and Harness Improvement are independent selections. Selecting research
does not select the eight-file improvement core, public records or experience
storage, and does not invent implementation run IDs. Selecting Harness
Improvement does not select research. Preserve both capabilities' existing
authority and local ownership boundaries.

### Optional Harness Improvement

Select capability `harness-improvement` explicitly before expanding the policy
or operation wildcards. Mapping v10 preserves the complete eight-file core:

| Source relative to the repository root | Consumer target |
|---|---|
| `harness/policies/harness-improvement.md` | `docs/policies/harness/harness-improvement.md` |
| `harness/policies/improvement-record-contract.md` | `docs/policies/harness/improvement-record-contract.md` |
| `harness/operations/harness-improvement.md` | `docs/agents/operations/harness-improvement.md` |
| `harness/schemas/improvement-record.schema.json` | `docs/agents/schemas/improvement-record.schema.json` |
| `harness/templates/harness-local-store.md` | `docs/agents/templates/harness-local-store.md` |
| `harness/templates/harness-stage-record.md` | `docs/agents/templates/harness-stage-record.md` |
| `harness/templates/harness-experiment.md` | `docs/agents/templates/harness-experiment.md` |
| `harness/templates/harness-improvement-record.md` | `docs/agents/templates/harness-improvement-record.md` |

When not selected, exclude all eight and all public-record selections; record
`harness-improvement` in `selection.excluded_capabilities`. Preserve capability
selection on refresh unless a change is authorized. Absence of that exclusion
in an older manifest is not opt-in: resolve from prior tracked files and actual
installation evidence, leaving an uninstalled capability disabled. Bootstrap
and unresolved partial installs retain their ownership/conflict procedure.

Public records are a separate explicit selection within this capability:

- Select record IDs and purpose: reference (default) or explicitly selected
  work-candidate. Admission follows the record contract: supported format,
  public fitness, identity/revision/source hash and local ownership checks.
  Importing a candidate assigns no task and adopts no rule.
- Resolve each ID uniquely across the public evidence layer, following the
  [placement contract](policies/improvement-record-contract.md#public-record-placement).
  The following sources are relative to the ai-assets repository root:

  | Selected source | Consumer target |
  |---|---|
  | `evidence/harness/<component>/<record>.md` | `docs/evidence/harness/<component>/<record>.md` |
  | `evidence/agents/<component>/<record>.md` | `docs/evidence/agents/<component>/<record>.md` |
  | `evidence/policies/<component>/<record>.md` | `docs/evidence/policies/<component>/<record>.md` |
  | `evidence/skills/<component>/<record>.md` | `docs/evidence/skills/<component>/<record>.md` |
  | `evidence/README.md` | `docs/evidence/README.md` |

  Enumerate only the actual selected records; these domain rows do not select
  every record or install its subject assets.
- Render the common catalog only when at least one record is selected. Include
  its owner/use guidance and exactly the selected rows across owner domains;
  adapt ownership/path prose to the installed layout. Track the catalog's source
  and rendered hashes separately. The catalog owns no independent work state.
  A selected skill record does not select the skill package or its runtime installation.
- Preserve record selection from the manifest's exact files. Keep purpose,
  applicability, local task/evaluation and feedback in the private receipt,
  not as global source task state. If a prior receipt is unavailable, do not
  infer work-candidate permission; use reference-only handling until resolved.
- Related unselected record IDs stay plain text with evidence-availability
  limits. Render links to omitted records/assets as logical references rather
  than expanding selection or leaving broken navigation. Subjects' source
  revision/fingerprint values are provenance and must not be rewritten.
- When an older selection uses a removed source path, read its accepted source
  snapshot and actual local contents, recover its declared record ID when one
  exists, and match the unique current record across all four owner domains.
  Old `evidence/agents/` source locators and `docs/evidence/agents/` consumer
  locators remain valid historical baselines until accepted refresh; do not
  relabel them as current source paths before comparing their original bytes
  and provenance. Missing/ambiguous identity or
  unsupported content requires reconciliation before rendering. No source alias
  or compatibility file is installed. Under the authorized refresh, remove
  superseded managed targets only after their content and inbound references
  are resolved and retirement is explicitly covered; preserve local ownership
  and unexplained drift under the existing conflict rules.
- When earlier installations have separate domain catalogs, derive the common
  catalog from the record IDs actually selected. Those catalogs are projections,
  not record identities or authority to import additional records. Reconcile
  their local content and links before retiring old managed catalog targets
  under the same review and ownership rules.

Mapping v10 retains the repository-level evidence layout introduced by v8,
locating each common record by its current responsible owner domain and
component. Original stage/comparison evidence stays separate. Manifest source
paths are repository-relative, using
`source.package_root: "."`, so assets and evidence have unambiguous locators
without parent-directory traversal. This root does not select any additional
files. Record schema 1 and import manifest schema 1 are independent of the
export-mapping version. Earlier installed baselines retain their actual mapping
version until a successful refresh.
Installing the capability or a record does not execute a backlog, authorize
private-history rewrites or install a runtime. Existing runs remain valid.

### Local Experience Activation

Selecting this capability opts into ordinary stage retrieval and reflection
once private persistence is configured. During adoption:

1. Install the complete core and expose the conditional entrance hook below.
   Use that hook for the current task and any selected flow/runner hooks. For
   delivery, those hooks cover planning and execution; research and
   improvement-only work use their actual task stages. No new role or full
   experiment is required for each task.
2. Use the operation's configuration procedure to reuse an existing owner or
   set up the default `docs/evidence/STORE.md` for this consumer/environment.
   Authorized adoption includes this setup when existing rules permit it;
   no separate destination choice is needed. Establish local exclusions and
   resolve tracked/staged, ownership or access conflicts before private writes.
   Initialize or map the blank scaffold at the local owner, not in the template
   folder. Local outputs never enter the shared-file manifest. Entrance docs may
   name the standard relative locator; actual private binding contents and
   identifying or external locators remain local.
3. Report capability installation and binding readiness separately. If storage
   cannot yet be resolved, installation may finish with persistence unresolved;
   the agent uses session-only observation and reports the gap. Do not claim
   that local history is accumulating.
4. On refresh, preserve existing local records, exclusions and discovery bindings;
   do not replace the evidence directory or migrate a configured external store
   merely to adopt the default. Do not
   enable capture for an older installation merely by inferring selection from
   missing exclusion metadata. A new machine/environment resolves its own
   binding using the default layout or its configured owner; common import does
   not synchronize original experience.

At subsequent stages, the agent uses the configured store without requiring a
separate improvement request. This is execution of the imported instructions,
not an installed background process or proof of actual hook execution.
Import brings in selected common assets and public records. Private bindings,
original project history and experience indexes never accompany that import.
Configure private improvement-record and receipt ownership alongside original
evidence. Selected public work candidates are source snapshots; local execution
links to the consumer's normal task owners. Do not copy the whole source work
list or synchronize its task state into the consumer.

## Exported Link Rewriting

### Current Mapping v10

The shared source tree and the consuming-repo tree intentionally use different
roots. Resolve the selected file set and its exact source-to-consumer mapping
before rendering. For each navigable relative link outside the method bundle:

1. Resolve the link against its actual source file in the selected source
   snapshot, separating the file target from its section anchor.
2. For a target present in the resolved mapping, use that exact entry, including
   explicit shared dependencies, planning-template destinations, review-policy destinations and
   selected records/catalog. Compute the relative path from the rendered file to
   the mapped target and preserve the anchor. Do not apply old substring rewrites
   to v10 paths or assume every policy originates below `harness/`.
3. For a reference explicitly marked source-only for authorized import/refresh
   administration, require the target to be the existing file exactly at
   `harness/ADOPTION-GUIDE.md` in the selected source snapshot and any supplied
   anchor to resolve in that file before rendering meaningful plain text naming
   the Harness Adoption Guide, its current export mapping and its
   import/refresh-only use. Retain the
   instruction to resolve that contract in the actual selected shared-source
   snapshot when that administration occurs. An installed manifest's historical
   baseline mapping is not the current source mapping. Do not add the guide to
   the payload, invent an external checkout locator, or require it for ordinary
   work. This exception applies only to that administrative reference; it cannot
   omit a required method, governance or flow dependency.
4. If a conditional target is omitted, retain the useful section name, selection
   condition and evidence limit as labeled plain text. Do not expand selection to
   repair a link. A missing required dependency or ambiguous mapping blocks the
   dependent export until resolved.
5. Reconcile operational path references in prose, code examples and entrance
   hooks with the same map. Preserve logical subject keys, historical source paths,
   revisions and fingerprints in evidence metadata; rendering alone does not
   increment a source record's revision.
6. Validate actual navigable links and anchors within the rendered consuming
   tree. Do not leave normal operation dependent on `../ai-assets/` or another
   external checkout.

For example, the current orchestrator's link to
`../policies/workflow-governance.md` resolves to
`harness/policies/workflow-governance.md`, then becomes
`../../policies/harness/workflow-governance.md` from its consumer target.
A link to `policies/competence-first-delegation.md` uses its separate shared-policy
mapping. A research-governance link to the pinned method resolves to
`docs/agents/methods/research-sadr/SKILL.md`. Do not transform any bytes or internal
links inside that complete method package. Optional design/interaction peers,
research, Harness Improvement, records and catalogs retain their selection
conditions when rendered as unlinked references.

### Historical Mappings v1–v9

The following transforms describe earlier accepted source layouts and remain
available to reproduce those baselines. Apply the entry's actual historical
mapping to its recorded source snapshot; do not reinterpret these paths as
current v10 source paths or relabel the result as v10. Use the current exact map
above only for a new candidate and accepted managed refresh.

In mappings v1–v3, rewrite these source-relative links during export instead of
copying them unchanged:

- In exported role, profile, flow, operation, and planning-template docs, rewrite source links under `../policies/harness/` to `../../policies/harness/`, preserving filenames and section anchors. This includes operator-briefing links, `execution-loop-governance.md#docs-content-writing-contract`, and the Fix Log's execution-return link.
- In exported roles and evaluation templates, rewrite `../policies/review/design-evaluation.md` to `../../policies/design/design-evaluation.md` and `../policies/review/interaction-evaluation.md` to `../../policies/experience/interaction-evaluation.md`. If an optional review asset is omitted, render its conditional reference as plain text instead of leaving a broken link.
- In the exported Design Evaluation policy, rewrite sibling `interaction-evaluation.md` links to `../experience/interaction-evaluation.md`, preserving section anchors. If the optional Interaction Evaluation policy is omitted, retain the section name as conditional plain text instead; for example, `Technical Canvas Input Ownership, when installed, owns gesture and control behavior.` Do not require the omitted peer to complete the export.
- In the exported operator policy, rewrite `../../templates/operator-briefing.md` to `../../agents/templates/operator-briefing.md`.
- Do not leave exported documents dependent on `../ai-assets/` or another external source path.

Mapping version `2` adds the review-to-review link transform and optional-peer handling above to version `1`.

Mapping version `3` also applies the harness-policy link transform to planning templates, including the Fix Log exported under `docs/plans/fix/`.

Mapping versions `4` and `5` introduced the optional capability and common
record metadata. Mapping version `6` consolidated the eight-file core and common
knowledge/work records, removing separate lesson/case formats and source aliases.
Mapping version `7` introduced component-owned evidence roots, per-root catalog
selection and repository-relative manifest source locators. Mapping version `8`
moves those records to `evidence/<domain>/<component>/` and selects one common
catalog. Mapping version `9` adds independently selected research and its pinned
method bundle, with the link transforms below. Preserve earlier versions as actual baseline provenance, not as
parallel active layouts.

Apply these transforms on top of versions 1–3:

- Apply the harness-policy transform to all four record/store templates and the
  improvement operation; their operation/template links otherwise remain valid.
- In the record contract under `docs/policies/harness/`, rewrite
  `../../schemas/`, `../../templates/` and `../../operations/` to
  `../../agents/schemas/`, `../../agents/templates/` and `../../agents/operations/`.
  Map its common catalog link to the installed catalog; render an omitted
  catalog as a labeled logical reference. Sibling policy links stay unchanged.
- In run/evaluation templates under `docs/plans/`, rewrite
  `../operations/harness-improvement.md` to
  `../../agents/operations/harness-improvement.md`.
- For each selected record or the common catalog, resolve a relative link against
  its actual source file, locate the target in the selected source-to-consumer
  mapping, then compute the relative link from the rendered file. Preserve
  section anchors. This applies to same-domain and cross-domain record/catalog
  links, harness policies, schemas, templates and operations; do not assume
  every record originates under `agents/` or has the old nesting depth.
  Render unselected targets as labeled logical references with evidence limits.
  Do not rewrite logical subject keys or historical source revisions/fingerprints
  in JSON metadata. Rendering alone does not increment source record revision.
- When the capability is absent, render its conditional references in roles,
  workflow, runner, run/evaluation templates as plain text, including anchors.
  Do not leave links to an omitted operation or contract.
- For selected records, retain unselected public IDs/relationships and omitted
  asset links as labeled logical references with evidence limits. Validate all
  actual navigable links within the consuming tree after rendering.

Mapping v9 additionally applies these research transforms:

- Map the five v9 research sources (flow, research-specific role, operation,
  governance and state template under the former `agents/` layout) and full
  method bundle to their corresponding v9 consumer targets. For each relative
  link in those five harness files or conditional peer
  links, resolve the source target, find it in the selected source-to-consumer
  map and compute the relative consumer link, preserving anchors.
- In research role, flow, operation and state-template files, harness-policy
  links use the existing `../policies/harness/` to `../../policies/harness/`
  transform. Peer links among `roles/`, `flows/`, `operations/` and `templates/`
  keep their relative layout under `docs/agents/`.
- In research governance, rewrite `../../roles/`, `../../flows/`,
  `../../operations/` and `../../templates/` to `../../agents/roles/`,
  `../../agents/flows/`, `../../agents/operations/` and
  `../../agents/templates/`. Sibling governance links stay unchanged.
- In research role, flow and operation files, rewrite
  `../../skills/research-sadr/` to `../methods/research-sadr/`. In research
  governance, rewrite `../../../skills/research-sadr/` to
  `../../agents/methods/research-sadr/`. Do not transform bytes or internal
  links inside the method bundle itself.
- When research is absent, render the workflow, runner and orchestrator's
  conditional research links as labeled plain text, retaining the selection
  condition. Do not expand selection to satisfy a peer link or leave an
  external-checkout path as a substitute.

## Local Ownership Rules
- The consuming repo should own the final installed copy.
- The consuming repo should own `docs/agents/harness-import-manifest.json` as operational import state.
- After export, local docs should read as if they belong to that repo directly.
- Do not leave the consuming repo depending on `../ai-assets/...` paths for normal operation.
- Treat the manifest as a refresh baseline, not as a source of harness policy or product truth.

## What Must Stay Local
Do not overwrite repo-local material that is not part of the shared harness package:

- architecture rules
- content contracts
- product-specific design constitutions
- project-specific developer guides
- existing run artifacts
- product PRDs and feature plans

## Harness Import Manifest

### Role And Location

- The shared example is [harness-import-manifest.example.json](harness-import-manifest.example.json).
- A consuming repo stores its actual manifest at `docs/agents/harness-import-manifest.json`.
- The example is a schema-shaped illustration. Do not copy placeholder hashes or treat its one sample file as a complete installation.
- The actual manifest must enumerate every selected harness-origin file, research method package file and selected public improvement record/catalog that the consuming repo tracks. One file entry owns one exact source-to-target mapping and its last accepted baseline provenance and hashes.
- Do not include the manifest itself in `files`; it is the repo-owned index of the other tracked artifacts.
- Do not list unrelated repo-local architecture, product, planning, or run artifacts.
- Do not record an absolute local source path. Resolve the current `ai-assets` checkout explicitly for the active session and record only the logical repository, package root, and full Git revision.

### Required Fields

- `schema_version`: manifest contract version. Start with `1`.
- `source.repository`: logical source repository name, normally `ai-assets`.
- `source.package_root`: root for source locators. Mapping v10 retains `.` (the ai-assets repository root) for selected `harness/` assets, shared `policies/` dependencies, `skills/research-sadr/` method files and records under `evidence/`; this does not authorize importing other repository contents.
- `source.revision`: full Git commit SHA for the latest accepted upstream snapshot used by the import or refresh operation. Import from a committed shared-source state.
- `selection.repository_surfaces`: consuming-repo capability surfaces used to choose the exported set.
- `selection.excluded_capabilities`: intentionally omitted optional capabilities such as `design`, `ux`, `research`, or `harness-improvement`.
- `mapping.version`: latest export-mapping and link-rewrite contract version used by the import or refresh operation. The initial version was `1`; the current version is `10`. Increment it when those semantics change materially.
- `files`: the resolved tracked file list for the consuming repo.

Each `files` entry must record:

- `source`: path relative to `source.package_root`; with mapping v10 use repository-relative paths such as `harness/roles/orchestrator.md`, `policies/competence-first-delegation.md`, `skills/research-sadr/SKILL.md` or `evidence/skills/<component>/<record>.md`
- `target`: path relative to the consuming-repo root
- `ownership`: `managed` for a shared file eligible for controlled refresh, or `local` for a harness-origin file intentionally detached for repo-local ownership
- `baseline_source_revision`: full Git commit SHA containing the source content identified by `source_sha256`
- `baseline_mapping_version`: mapping and link-rewrite contract version used to produce `rendered_sha256`
- `source_sha256`: SHA-256 of the source file at the entry's accepted baseline
- `rendered_sha256`: SHA-256 of the installed content after target-layout and link-rewrite transforms at that baseline

Keep `files` deterministically sorted by `target`, reject duplicate source or target mappings, and record hashes as lowercase 64-character hexadecimal values.

Source and target locators must remain relative within their resolved roots;
reject absolute paths and traversal outside those roots. Do not encode evidence
outside a narrower package root through a parent-directory path.

When refreshing an older valid manifest, first resolve every source locator
against its recorded package root. In the candidate v10 manifest, re-encode that
same effective source path relative to `.` (for example, `agents` plus
`roles/orchestrator.md` becomes `agents/roles/orchestrator.md`). This is a locator
conversion, not a new baseline: preserve each entry's actual baseline source
revision, mapping version, source hash, rendered hash, target and ownership.
Compare the same original source and installed bytes before considering an
update. Match a relocated public record by its stable ID across all four owner
domains in the actual collection; missing or ambiguous identity stops the
dependent update. Historical `evidence/agents/` source locators and
`docs/evidence/agents/` target locators remain valid accepted baselines, including
when their current record belongs to
`harness/` or `policies/`. After an accepted managed refresh, use
the new source/target mapping and advance its baseline together. A `local`
entry keeps its original effective source locator and detachment baseline,
even when that path no longer exists in the latest source revision.

The same preservation applies to every v1–v9-to-v10 refresh, including v8 or
v9 entries whose locators already use `.`. A new top-level mapping version does
not rewrite historical per-entry mapping versions, source revisions, source
hashes or rendered hashes. Advance them together only after the corresponding
managed refresh is actually accepted. Manifest schema version remains `1`; it
is independent of the export-mapping version.

For a `managed` entry, compare the current target hash with `rendered_sha256` before refresh. A mismatch is a local modification and must not be overwritten automatically. After accepting a managed refresh, advance its baseline provenance and hashes together to the accepted source and rendered result.

For a `local` entry, preserve the target unconditionally and keep its per-entry baseline provenance and hashes together as the detachment baseline for later review or promotion. The top-level source revision and mapping version may advance for the refresh as a whole, but the local entry's baseline fields must not advance during ordinary refresh. Rebase or reattach it only through an explicit ownership decision.

### Upgrading Existing Mappings To v10

Normalize an older `source.package_root: "agents"` plus its relative `source`
into the same repository-relative locator before matching identities. For
example, `roles/orchestrator.md` becomes `agents/roles/orchestrator.md`, not
`harness/roles/orchestrator.md` at this stage. Preserve the old revision, mapping
version, source/rendered hashes, target and ownership: only the locator's encoding
has changed. Resolve any other recorded root by the same rule; reject traversal
outside it. Do not guess a baseline from the latest source or current target.

Use this compatibility map for the proposed managed refresh after that
normalization. These are identities across layouts, not source aliases to install:

| Effective old source | Current source or replacement | Consumer target handling |
|---|---|---|
| `agents/roles/<name>.md`, except `research-orchestrator.md` | `harness/roles/<name>.md` | Retain `docs/agents/roles/<name>.md` |
| `agents/flows/workflow.md` | `harness/flows/delivery.md` | Rename `docs/agents/flows/workflow.md` to `docs/agents/flows/delivery.md` only through accepted refresh and retirement review |
| `agents/operations/runner.md` | `harness/operations/delivery-runner.md` | Rename `docs/agents/operations/runner.md` to `docs/agents/operations/delivery-runner.md` under the same checks |
| `agents/flows/research.md` | `harness/flows/research.md` | Retain `docs/agents/flows/research.md` |
| `agents/operations/research-runner.md` | `harness/operations/research-runner.md` | Retain `docs/agents/operations/research-runner.md` |
| `agents/operations/harness-improvement.md` | `harness/operations/harness-improvement.md` | Retain `docs/agents/operations/harness-improvement.md` |
| `agents/profiles/<file>` | `harness/profiles/<file>` | Retain the recorded `docs/agents/profiles/<file>` target |
| `agents/templates/<file>` | `harness/templates/<file>` | Retain its exact planning-template or `docs/agents/templates/` target from the export map |
| `agents/schemas/improvement-record.schema.json` | `harness/schemas/improvement-record.schema.json` | Retain `docs/agents/schemas/improvement-record.schema.json` |
| `agents/policies/harness/competence-first-delegation.md` | `policies/competence-first-delegation.md` | Retain `docs/policies/harness/competence-first-delegation.md` |
| Other exported `agents/policies/harness/<file>.md` | `harness/policies/<file>.md` | Retain `docs/policies/harness/<file>.md` |
| `agents/policies/review/design-evaluation.md` | `policies/review/design-evaluation.md` | Retain `docs/policies/design/design-evaluation.md` |
| `agents/policies/review/interaction-evaluation.md` | `policies/review/interaction-evaluation.md` | Retain `docs/policies/experience/interaction-evaluation.md` |
| `agents/roles/research-orchestrator.md` | Responsibilities in `harness/roles/orchestrator.md`, `harness/policies/workflow-governance.md` and `harness/policies/research-governance.md` | Retire `docs/agents/roles/research-orchestrator.md` only after the replacement and retirement checks below |
| `skills/research-sadr/**` | Same source paths | Preserve exact selected method files |
| `evidence/agents/harness-improvement/<record>.md` | The same stable record ID under `evidence/harness/harness-improvement/` | Move its selected `docs/evidence/agents/harness-improvement/` target to `docs/evidence/harness/harness-improvement/` only through accepted refresh and retirement review |
| `evidence/agents/design-evaluation/<record>.md` or `evidence/agents/interaction-evaluation/<record>.md` | The same stable record ID under `evidence/policies/` and its current component | Move its selected `docs/evidence/agents/` target to the same component under `docs/evidence/policies/` under the same checks |
| Other selected `evidence/**` records and the common catalog | Resolve each record by stable ID across all four current owner domains; retain current paths when unchanged | Preserve exact selection and map each actual source domain to the same `docs/evidence/` domain; apply catalog/record retirement rules |

Evidence compatibility rows identify prior locators, not a wildcard selection
or an alternate placement rule. Resolve the unique actual record before rendering
and use its current path under
[Public Record Placement](policies/improvement-record-contract.md#public-record-placement).
A path-only move with the same record ID, revision and raw-source hash is valid;
its record content is unchanged, but its source/target mapping still follows
the refresh, ownership, drift, collision and retirement checks below. It does
not justify a content revision or a new observation. A higher revision is only
an update candidate. No alias tree or parallel record history is installed.

`harness/policies/workflow-governance.md` is a new required common dependency at
`docs/policies/harness/workflow-governance.md`. Its absence from an old manifest
is not permission to overwrite a coincidentally named local file. The common
orchestrator remains required independently of whether research is selected.

Before dependent content, target-rename, hook or manifest writes:

1. Read the accepted old source snapshot and verify its raw bytes against
   `source_sha256`. Reproduce its rendered baseline with the entry's historical
   mapping, verify `rendered_sha256`, and compare the actual old target to that
   rendered hash. A target mismatch is protected local drift, not an automatic
   rename or baseline advance; unsupported source or rendering provenance must
   be reconciled before proceeding.
2. Resolve the proposed new source and target uniquely and inspect any existing
   new target and inbound references. Old and new targets present together,
   duplicate source/target mappings, conflicting owners or an unexplained
   destination are reconciliation conflicts; block dependent writes. Do not
   merge or replace them merely because filenames suggest the same asset or record.
3. Preserve every `local` entry, its original effective source locator,
   detachment baseline and target unconditionally. A source move or retirement
   does not reattach, rename, delete or advance it. Resolve any replacement that
   would overlap its ownership explicitly before the dependent managed update.
4. For a managed delivery rename or selected public-record relocation, render
   the current candidate at the new target, reconcile all inbound references
   and entrance hooks, and explicitly review retirement of the old target. Do not leave both as competing active
   flows/runners or duplicate installed record copies, silently remove the old
   target, or manufacture a compatibility copy. If retirement is not resolved,
   leave the dependent migration pending.
5. For the retired research role, inspect its actual content and verify that
   the common orchestrator, workflow governance and selected research governance
   preserve its applicable controller responsibilities, decisions, inputs,
   outputs, interruption/resume behavior and local adaptations. Ensure these
   replacements are installed and their inbound references reconciled before
   explicitly reviewing removal of a clean `managed` old target. Local-owned or
   drifted roles retain the same protection; a missing new source file alone
   never authorizes deletion. If research is intentionally disabled, reconcile
   its retained responsibilities and capability retirement instead of installing
   research solely to satisfy replacement links. After accepted retirement,
   remove only the retired entry; each replacement has its own exact mapping.
   Do not turn the retired role into a duplicate entry for the common orchestrator
   or overwrite the retained old-baseline evidence with replacement provenance.
6. Only after the accepted managed update and its content/link checks, advance
   that entry's source/target identity, baseline source revision, mapping version
   and both hashes together. Keep untouched or detached entries' actual v1–v9
   baselines. Generate and validate the whole candidate manifest and replace the
   installed manifest only as the final successful operation step.

Research omission remains omission even when an older manifest has no exclusion
key. Resolve tracked and actual installation evidence before selecting its four
current core files and full pinned bundle; partial installation and ambiguity
retain bootstrap/conflict handling. Retiring its former role does not opt into
research, Harness Improvement, public records, storage or a runtime installation.
Preserve independently selected Harness Improvement assets and exact public
record IDs, purposes and private receipt ownership throughout the migration.

### Manifest Lifecycle

- Generate and update the manifest from resolved files; do not hand-edit hashes.
- After content and link checks pass, generate and validate a candidate manifest before replacing the installed manifest.
- Replace the installed manifest only as the final successful refresh step.
- Leave the prior manifest unchanged when export, refresh, conflict resolution, candidate-manifest validation, or another required check fails.
- Keep the manifest in the same harness-only commit as the imported or refreshed shared layer when possible.
- Do not update a recorded hash to match unexplained local drift. Classify the difference first as an accepted upstream result, intentional local ownership, or an unresolved conflict.
- When the shared example's `mapping.version` differs from the installed manifest, treat the mapping or link transforms as changed and re-render the selected file set before comparing target hashes.
- Do not remove a previously tracked target merely because the new selection omits it. Report it as a retirement candidate and remove it only after explicit review.

An uncommitted source may be rendered in a disposable preview for review.
Record its base revision, dirty snapshot and per-file source/rendered hashes in
preview evidence outside the installed manifest. It is not an accepted import
baseline: do not use the current HEAD as provenance for changed content, write
an installed manifest, or report a completed refresh from that preview.

## Operator Prompts
Use prompts like these when asking a local coding agent to install or refresh the package in a repo.

`Fresh Export` and `Refresh Or Resync` have mode-matched prompts below. `Existing Installation Bootstrap` and `Manifest Recovery` follow the procedures above; bootstrap uses `Controlled Merge` for its merge step, but `Controlled Merge` is not an additional manifest-state mode.

### Fresh Export
```text
Export the selected harness system from `../ai-assets/` into this repo using mapping v10.

Install it as a local docs-owned system, not as a runtime dependency.
Map the selected shared package into the applicable locations:
- `docs/agents/`
  - `roles/`
  - `flows/`
  - `operations/`
  - `profiles/`
  - `templates/`
- `docs/agents/methods/research-sadr/` only when research is selected
- `docs/plans/`
- `docs/policies/harness/`
- `docs/policies/design/`
- `docs/policies/experience/`

Keep the exported docs general unless this repo already needs local specialization.
Rewrite source-relative cross-links for the consuming-repo layout.
Resolve optional capabilities before expanding wildcards. Include the complete eight-file Harness Improvement core, including its schema, only when explicitly selected. Select public records separately as references or explicit work candidates; omit the catalog when none are selected. Apply the record contract's admission and private receipt procedure.
Whenever shared roles or flows are selected, include the common orchestrator, workflow governance, competence/continuity policies and operator briefing template independently of research selection. Select research independently. When selected, include its four-file core and every file of the pinned research-sadr method bundle, preserving method bytes and internal links. Load that local SKILL.md directly; claim no runtime discovery or personal installation. When omitted, record the exclusion and render conditional peers as plain text. Use delivery.md and delivery-runner.md for selected delivery.
Update local entrance docs and references so the resulting layout is coherent.
If Harness Improvement is selected, install its conditional stage hook and resolve the private store/discovery binding through the operation; report installation and persistence readiness separately. Never put private bindings, original evidence or receipts in this manifest.
When Harness Improvement is selected, use docs/evidence/STORE.md and its local record paths by default, or reuse an existing configured owner. Establish local exclusions before private writes and preserve any ownership conflicts for resolution. Local evidence is consumer output, separate from imported docs/evidence/harness/, agents/, policies/, skills/ and README.md snapshots. Map only actually selected public records from evidence/<domain>/ to docs/evidence/<domain>/ using the four-domain export map above.
After content and link checks pass, generate and validate a complete candidate from the shared example using the full source revision and every tracked file. Write `docs/agents/harness-import-manifest.json` only as the final successful export step.
```

### Refresh Or Resync
```text
Refresh the local harness system in this repo from the selected sources in `../ai-assets/` using mapping v10.

Read `docs/agents/harness-import-manifest.json` first when it exists.
If the manifest is missing but local harness files already exist, bootstrap the existing installation instead of performing a blind fresh export.
If the manifest exists but fails validation, preserve it unchanged and stop before harness-content writes. Build and validate a separate recovery candidate from supported source, target, and Git evidence; never refresh from invalid values or replace the installed manifest before the final successful step.
Keep repo-specific policy or product docs that are not part of the shared harness package.
Update only the selected shared role, flow, operation, profile, template, harness-policy, method-bundle, schema, public record/catalog and review-asset layers.
Preserve optional capability and public-record selection, resolving relocated harness/shared-policy sources by the v10 compatibility map and replaced record paths by stable ID across the actual harness, agents, policies and skills evidence domains. Normalize older agents-root locators to repository-root dot without changing their effective baselines. Keep old evidence/agents source locators, docs/evidence/agents target locators and their full accepted provenance until controlled refresh succeeds; missing or ambiguous record identity blocks dependent writes. Reconcile record relocations, workflow.md to delivery.md and runner.md to delivery-runner.md; retire old managed targets only after content, inbound-reference and explicit retirement review. Retire the former research-orchestrator only after common-controller replacement coverage, ownership, reference and explicit retirement review. Conflicting destinations block dependent writes. Derive the common catalog from selected records and reconcile superseded catalogs under the existing retirement rules. Do not enable Harness Improvement or research merely because an older manifest lacks its exclusion key; resolve tracked and actual installation evidence, retaining partial-install and conflict handling.
For selected research, verify the complete local method bundle, byte-preserving package copy and rewritten harness links. Preserve every actual per-entry v1–v9 baseline provenance until an accepted managed refresh; local-owned and drifted method files follow the same protection as other managed assets.
Preserve the private experience store, its exclusions and discovery binding when configured; refresh does not migrate history or reauthorize export. Never replace the whole docs/evidence tree or manage local STORE.md, stages/, improvements/ or experiments/ as imported files. Reconcile the conditional stage hook with the existing entrance rules.
If local docs have drifted, reconcile references and ownership cleanly instead of duplicating guidance.
Compare source and rendered hashes before writing, preserve `local` entries, and report unexplained differences as conflicts.
If the current shared mapping version differs from the manifest, re-render the selected file set before comparing targets.
Generate and validate the next manifest only after content and link checks pass. Replace the installed manifest only as the final successful refresh step.
```

### Controlled Merge
```text
Adopt the shared harness system from the selected sources in `../ai-assets/`, but merge it into the current local structure instead of overwriting blindly.

Preserve repo-specific architecture, product policy, and content contracts.
Replace or align only the reusable harness layer:
- role docs
- flow docs
- operation docs
- profile docs
- templates
- harness governance
- the complete pinned research method bundle only when independently selected
- optional improvement schema and explicitly selected public records/catalog
- review assets

Use the import manifest when available to distinguish managed shared files from intentional local ownership. Do not normalize unexplained local differences into a new baseline.
```

## Promotion From Consuming Repos
When a consuming repo improves the agent system:

1. Compare local docs against their selected canonical sources in `../ai-assets/`.
   - When a manifest exists, start from its recorded rendered baseline so upstream evolution is not confused with local delta.
2. Classify each difference as:
   - `promote`: general reusable rule
   - `local`: project-specific rule
   - `discard`: historical note, accidental drift, or obsolete wording
3. Promote only general reusable rules into `ai-assets`.
4. Generalize examples before promotion so they do not depend on one product, framework, language, or local filesystem path.
5. Refresh consuming repos from the canonical package after promotion.

When Harness Improvement is installed, use its private experiment record to
connect compared state, original results, per-edit effects and counterevidence
when an actual comparison exists. Ordinary stage evidence and common Improvement Records connect
applied components, reusable knowledge and work without requiring an experiment.
Use [Export Common Experience](operations/harness-improvement.md#export-common-experience)
to resolve the canonical shared checkout, reconstruct public material, match an
existing case and write to the policy's exact source-owner destination.
Prepare a separate public case only when that work is authorized. Its case
review is independent of adopting a normative change: promote rules into their
existing policy, skill or review-asset owner; normalize reference experience and
reusable pending work into canonical Improvement Records at the current owner's
`evidence/<domain>/<component>/` location under
[Public Record Placement](policies/improvement-record-contract.md#public-record-placement).
Keep private identifiers, traces, paths
and hashes out of the shared source and manifest.

This direction is consumer to common source, independent of whether the
consumer tracks or ignores its local run files. Git ignore is not proof that
those records are suitable for common export. A matching case is updated with
new evidence or counterevidence and its scope preserved; it is not cloned for
every consumer. Case-only export does not adopt a rule. A later project receives
selected cases or changed owned rules through its own authorized import/refresh.

Apply source edits, external publication and consumer refresh only within their
respective authorization. An accepted case or source change does not establish
installation or runtime activation. These distinctions also apply when no
experiment record is used; the optional capability adds no mandatory promotion
artifact.

### Everyday Export Requests

In an established common-asset promotion context, the operator can say
`ai-assets로 export해줘` or simply `export해줘`. The
[request operation](operations/harness-improvement.md#recognize-an-export-request)
resolves the intent; the operator need not repeat a generalization/security
prompt or enumerate harness, skills and UI/UX each time.

Without a category limit, review the current project's available relevant
harness, skill/resource/tool, design/UI and interaction/UX experience. Start
from its index and linked evidence, including unexported items, new support,
counterexamples and changed conditions for earlier cases. Missing history limits
coverage; it does not require a new ledger or authorize unrelated workspace scans.

- `사용 사례를 ai-assets로 export해줘` or `사용 사례만 ai-assets로 export해줘`: export qualified reference cases;
  leave normative adoption out of scope.
- `skill 사용 사례를 export해줘` or `skill 사용 사례만 export해줘`: narrow both category and output to skill cases.
- `UI/UX 관점에서 공통화해줘`: narrow to design/interaction experience and
  supported existing review-asset changes.
- `export할 만한 것만 검토해줘`: review candidates without a shared-source write.

The default commonization request covers bounded changes within the existing
owners and contracts, after reuse/evidence/disclosure review. Complete that
authorized scope without asking for permission per category. Keep unresolved
consequential changes as concrete proposals while completing eligible items.
Reviewed reusable work still unresolved is normalized into the same Improvement
Record format as reference experience. The common record is canonical for both knowledge and work; select by subject
and work state directly from its catalog, without a separate skill list.
The [maintenance operation](operations/harness-improvement.md#maintain-improvement-records)
connects observations, pending work, authorized improvement and results. A case
export updates reference/evidence content and catalog entries, preserving existing work
state/assignments and normative rules.
Only generalized public-appropriate content enters this public repository;
credentials, personal data, confidential facts and revealing context stay private.
When adequate generalization is impossible, retain the item locally or hold it.
No eligible candidate is a valid no-change result.

A product/data export keeps its own task meaning. Resolve genuine ambiguity
before dependent writes. These examples grant no commit/push, cross-project
refresh or runtime activation; preserve each action's existing authority.

## Export And Refresh Finalization Checks
Before finalizing an export or refresh in a consuming repo:

1. Check entrance docs and cross-links.
2. Confirm that all five common dependencies exist when shared roles or flows are installed: `docs/agents/roles/orchestrator.md`, `docs/policies/harness/workflow-governance.md`, `docs/policies/harness/competence-first-delegation.md`, `docs/policies/harness/operator-briefing-and-review-receipts.md` and `docs/agents/templates/operator-briefing.md`, independently of research selection.
3. Confirm that links from the exported orchestrator, shared workflow governance, each selected flow and the operator policy resolve inside the consuming repo. Check delivery filename renames and any retired research role through the v10 migration procedure; conflicting or locally owned targets block dependent writes until resolved.
4. Check that all other local harness policy paths are correct. Verify source-only adoption-guide references under the v10 administration rule: useful contract/current-mapping and import/refresh-only text remains, no runtime link or extra guide payload is introduced, and missing required method/governance/flow dependencies still block export.
5. Check whether review assets belong under local `design/` and `experience/` policy owners; verify that exported role, evaluation-template, and review-policy links resolve to those assets, including section anchors, or become unlinked conditional references when omitted. Confirm that the manifest records the applied mapping version.
6. When delivery is selected, add a short execution gate to the consuming repo's `AGENTS.md` so planning requests stop at PRD or feature review instead of being reinterpreted as implementation approval. Research-only or improvement-only selection preserves its own task/flow authority and does not require delivery artifacts or this delivery gate.
7. Keep repo-specific rules outside the shared role package.
8. Confirm that generated planning docs use repo-relative links instead of local absolute paths.
9. Confirm that the candidate manifest uses full source commit SHAs from committed shared-source states and contains no absolute source or target paths.
10. Confirm that every selected harness-origin file is represented once, mappings are unique and deterministically ordered, every entry has attributable baseline provenance, and every `managed` target matches its recorded `rendered_sha256` after the operation.
11. Confirm that the manifest does not list itself and that repo-local product and planning artifacts are absent.
12. Check capability selection before wildcards, the complete eight-file core, conditional links when absent, and exact record/common catalog selection across the four current owner domains. Check record format/identity/revision/public fitness, repository-relative source locators, preserved effective legacy baselines, source and rendered hashes, and replaced-target/catalog retirement after content/reference reconciliation. Check conditional stage hooks and default or configured store discovery; check local exclusions, tracked/staged conflicts and separation from managed targets before reporting binding/receipt readiness. Preserve local evidence and existing overrides on refresh. Exclude private bindings, indexes, original records, receipts and temporary evidence from the common package and manifest.
13. Check research selection independently: the four-file core, every pinned method package file and governance dependencies are complete when selected; method bytes/internal links match source and all harness links resolve locally. When absent, verify exclusions and meaningful unlinked peers, including older v8/no-exclusion resolution. Preserve drift, local ownership, conflicting targets, historical per-entry baselines and retirement rules. Confirm no automatic storage, run IDs, runtime discovery or installation claim. Treat dirty-source rendering only as a disposable preview with its base, snapshot and per-file hashes outside the installed manifest.
14. Write or replace the installed manifest only after checks 1-13 pass.
15. Commit the imported harness layer and its manifest separately from unrelated product work when possible and authorized.

## Local AGENTS Gate
When a consuming repo uses the selected delivery flow, its local `AGENTS.md` should restate the stop conditions that must be visible at task start:

- PRD requests are planning-only until the human owner approves the boundary.
- `draft` PRDs and unapproved feature proposals must not trigger spec work, code changes, or evaluation.
- If open points can still change scope, acceptance, dependency, or user-visible behavior, stop and ask instead of implementing.
- When a canonical target starts or resumes and prior context materially affects understanding or execution, apply `docs/policies/harness/operator-briefing-and-review-receipts.md`; otherwise preserve the normal response shape.

Whenever shared roles or flows are installed, expose the common controller at
`docs/agents/roles/orchestrator.md` and routing/resource contract at
`docs/policies/harness/workflow-governance.md`. Reconcile this pointer with the
existing entrance rules. It loads only selected flow contracts and retains each
flow's approval and acceptance boundaries; it does not require spawning a runtime
agent or installing a sibling flow.

When research is selected, also reconcile this conditional pointer with the
existing entrance instructions:

```text
For an open research task when capability research is selected, start or resume
through docs/agents/operations/research-runner.md. Load the pinned local method
at docs/agents/methods/research-sadr/SKILL.md directly. Preserve one resolved state
owner, actual input and actor history, resource commitments, actual use and
acceptance gaps under the shared resource contract.
Research conclusions do not authorize implementation; a selected change returns
to the existing planning and approval flow. Narrow factual tasks need no research
flow. This capability does not install runtime agents or configure experience
storage. Keep this pointer conditional if research is later disabled.
```

When Harness Improvement is selected, also reconcile this conditional pointer
with the existing entrance instructions:

```text
When Harness Improvement is selected, follow
docs/agents/operations/harness-improvement.md for ordinary stage entry, observed
component use, and closing reflection. Find the default local store at
docs/evidence/STORE.md or an existing override through this consumer's approved
private context. Follow the configuration procedure for first setup; preserve
existing records and report unresolved conflicts without resetting them. With a
ready binding, retrieve relevant experience and retain knowledge and improvement work in common records as
part of the current task or selected flow without a separate user command.
For delivery, this includes the normal PRD/feature/spec/build/evaluate/fix flow;
research and improvement-only work keep their own stage and artifact contracts.
If the binding is unresolved or unavailable, report the persistence gap and
keep observations session-only. Preserve existing approvals; export common experience only
within its separately applicable source-edit and disclosure authority.
In established ai-assets commonization context, recognize short export requests
through that operation's Recognize An Export Request section. Without a narrower
selection, review available current-project harness, skill/resource and UI/UX
experience. Respect case-only, review-only and category/time limits; generalize
and review public fitness before any common-source write.
Use Improvement Record v1 for reusable experience and unresolved asset-level
work. Import selected public records as references or explicit work candidates;
keep local applicability and execution in the private receipt/task owner. Follow
the operation's maintenance and record import/export procedures, preserving
revisit conditions and action authority. A pending task is not a supported lesson.
```

Keep this pointer conditional when a capability is later disabled. The standard
relative locator is safe navigation; keep actual binding contents, identifying
store IDs and machine-specific or external private locators out of public
`AGENTS.md` and the import manifest.

## Repository-Local Operator Context
Repository adoption owns the detailed operator-context behavior. When shared roles or flows are selected, install the policy and non-persistent response scaffold at the mapped local paths, then expose the conditional pointer above from the consuming repo's entrance layer.

- No additional operator-context command, tracker, map, or historical backfill is required; the import manifest is separate adoption state and does not persist briefing content.
- Existing project artifacts and source-of-truth ownership remain unchanged.
- Adopt the behavior prospectively; do not create permanent briefing logs for earlier conversations.
- The personal Codex adapter is optional and does not install these repo-local assets. Its managed hook only recognizes relevant triggers when the current repo already exposes the detailed policy.

## Non-Goals
- automatic installer scripting
- runtime linking back to `../ai-assets/`
- replacing repo-specific product planning artifacts
