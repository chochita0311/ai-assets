# Improvement Evidence

This repository-level layer holds public, generalized improvement records for
shared AI assets. Records retain reusable knowledge, improvement questions,
evidence limits and work history. A planned check or synthetic example is not
an observed success. Runtime assets, harness contracts, shared policies, and
skill instructions remain with their owners under `agents/`, `harness/`,
`policies/`, and `skills/`; private originals remain private.

## Ownership And Placement

| Current responsible asset owner | Record location |
|---|---|
| Portable harness role, flow, operation, workflow policy, profile or template | `evidence/harness/<component>/<record>.md` |
| Runtime adapter, shared instruction or prompt preset | `evidence/agents/<component>/<record>.md` |
| Common baseline, delegation or review policy | `evidence/policies/<component>/<record>.md` |
| Skill, skill resource or shared skill-maintenance concern | `evidence/skills/<component>/<record>.md` |

The domain and component identify the current responsible owner of the
improvement question. Placement does not identify its performer, originating
workflow or cause of an observed result; historical `subjects.kind` and
`subjects.key` do not select its folder. Keep one record per question. A
multi-subject question belongs to its primary responsible owner or a named
shared concern, with every subject retained in the record. Resolve unclear
ownership before placing a new record.

Create directories only for actual records, without mirroring whole source
trees; the placement patterns do not declare records for every role or skill.
UI/UX evaluation criteria retain their existing policy sections.

Use the shared [record and exchange contract](../harness/policies/improvement-record-contract.md#public-record-placement),
[metadata schema](../harness/schemas/improvement-record.schema.json) and
[template](../harness/templates/harness-improvement-record.md). The four owner
domains use one format, lifecycle and ID space. This catalog is their only
public discovery list and owns no independent work state or rule authority.

## Select Records

Filter by subjects and cues, then read applicability, readiness, evidence,
exclusions, counterevidence and independent work/knowledge/adoption states.
Finding a record neither assigns work nor adopts a rule. Query all relevant
domains when matching IDs or questions; an absent row does not prove that a
record is missing from the actual collection.

Current records have responsible owners in harness, agents, policies and skills.

| Record | Subjects | Title |
|---|---|---|
| [ir-code-quality-human-readability](policies/code-quality/human-readable-code-validation.md) | Code Quality, generated shared instructions | Human-readable code guidance and validation limits |
| [ir-clean-code-validation](skills/clean-code/validation.md) | `skills/clean-code`, `skills/refactor-plan` | Clean Code author checks, replayable cases, discovery boundaries, and effectiveness limits |
| [ir-design-deslop-validation](skills/design-deslop/validation.md) | `skills/design-deslop` | Inspectable DOM and component/whole-screen HTML review, partial choices, agent handoff, and preservation cases |
| [ir-harness-improvement-adoption-review](harness/harness-improvement/harness-improvement-adoption-review.md) | Harness Improvement, run/evaluation templates, `skills/refine-skill` | Harness improvement adoption review |
| [ir-ui-requested-control-rendering](policies/design-evaluation/requested-control-rendering.md) | Design Evaluation, `skills/screen-alignment`, painted glyphs and compact hosts | Requested controls and rendered geometry |
| [ir-change-impact-preservation](harness/execution-loop-governance/change-impact-and-preservation.md) | Delivery governance, Orchestrator, Builder and evaluator handoffs, capability and artifact closure | Actual impact paths and preservation handoffs |
| [ir-ui-initialization-recovery-evidence](policies/interaction-evaluation/initialization-and-recovery-evidence.md) | Interaction/Design Evaluation, initialization, style readiness and recovery | Initialization, recovery and sufficient UI observations |
| [ir-ui-state-transition-contracts](policies/interaction-evaluation/state-transition-contracts.md) | Interaction Evaluation, Design Evaluation, `skills/screen-alignment`, history and input ownership | Stateful controls and committed intent |
| [ir-ui-native-host-evidence](policies/interaction-evaluation/native-host-evidence.md) | Interaction Evaluation, `skills/screen-alignment`, delivery and probe conditions | Native host and end-to-end evidence |
| [ir-skill-distribution-contract](skills/skill-distribution/skill-distribution-contract.md) | `skills` | Skill distribution and removal contract |
| [ir-skill-benchmark-prerequisites](skills/skill-benchmark/skill-benchmark-prerequisites.md) | `skills` | Shared skill benchmark prerequisites |
| [ir-refine-skill-discovery-validation](skills/refine-skill/refine-skill-discovery-validation.md) | `skills/refine-skill` | Refine-skill discovery and static-audit validation |
| [ir-refine-skill-comparable-reruns](skills/refine-skill/refine-skill-comparable-reruns.md) | `skills/refine-skill` | Refine-skill comparable reruns and stability |
| [ir-documentation-adaptive-review](skills/documentation/documentation-adaptive-review.md) | `skills/docs-structuring`, `skills/docs-shaping` | Documentation skill adaptive-review follow-up |
| [ir-documentation-content-role-validation](skills/documentation/documentation-content-role-validation.md) | `skills/docs-structuring`, `skills/docs-shaping` | Documentation content-role validation |
| [ir-context-freshness-independent-maintenance](skills/maintain-context-freshness/context-freshness-independent-maintenance.md) | `skills/maintain-context-freshness` | Independent context maintenance validation |
| [ir-context-freshness-disposal-validation](skills/maintain-context-freshness/context-freshness-disposal-validation.md) | `skills/maintain-context-freshness` | Context archive and deletion validation |
| [ir-pr-review-semantic-corpus](skills/gh-review-pr/pr-review-semantic-corpus.md) | `skills/gh-review-pr` | PR review semantic corpus and comparisons |
| [ir-pr-review-live-validation](skills/gh-review-pr/pr-review-live-validation.md) | `skills/gh-review-pr` | PR review controlled live validation |
| [ir-codex-review-challenger-validation](agents/codex/review-challenger-validation.md) | `agents/adapters/codex/custom-agents/review_challenger.toml`, `skills/refactor-plan`, `agents/policies/harness/execution-loop-governance.md` | Codex review-challenger runtime validation |
| [ir-research-sadr-validation](skills/research-sadr/research-validation.md) | `skills/research-sadr`, research flow and governance, optional `research_worker` | Standalone and harness research validation |
| [ir-harness-mapping-v10-validation](harness/adoption/harness-mapping-v10-validation.md) | Harness adoption and record contracts, workflow governance | Mapping v10 preservation and consumer-validation limits |
| [ir-pr-description-concurrency-validation](skills/pr-descriptor/publication-concurrency-validation.md) | `skills/pr-descriptor` and its publication helper/tests | Pre-draft capture and publication concurrency validation |
| [hc-skill-trigger-example](skills/skill-discovery/skill-trigger-example.md) | fictional skill | Synthetic skill discovery reference |

## Maintain And Exchange

Use [Maintain Improvement Records](../harness/operations/harness-improvement.md#maintain-improvement-records)
for the owning record's question, evidence, work and outcome, then update its
catalog row. Retain resolved records for knowledge and history. Resolve
scattered notes into the matching record and remove absorbed documents within
authorized scope, without a separate follow-up list or compatibility copies.

Use the same operation's [export](../harness/operations/harness-improvement.md#export-common-experience)
and [import](../harness/operations/harness-improvement.md#import-improvement-records)
procedures. Private originals and private-to-public associations remain private;
public writes require semantic disclosure review. For authorized import/refresh
administration, use the **SOURCE-ONLY**
[adoption contract and current mapping](../harness/ADOPTION-GUIDE.md#export-mapping)
in the actual selected shared-source snapshot. This administrative reference is
not an ordinary runtime dependency or an additional selected payload file.
Import only selected records and their rows from this catalog, retaining
source/rendered provenance. Omit the catalog when no records are selected; a
skill record does not install its skill. Unselected relationships remain IDs
with evidence limits. Local results return as reviewed feedback to a later source
revision; source updates do not establish installation or actual use.
