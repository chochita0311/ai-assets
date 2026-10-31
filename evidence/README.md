# Improvement Evidence

This repository-level layer holds public, generalized improvement records for
shared AI assets. Records retain reusable knowledge, improvement questions,
evidence limits and work history. A planned check or synthetic example is not
an observed success. Runtime assets and adopted instructions remain with their
owners under `agents/` and `skills/`; private originals remain private.

## Ownership And Placement

| Improvement subject | Record location |
|---|---|
| Harness role, flow, operation, policy, profile, template, adapter or review asset | `evidence/agents/<component>/<record>.md` |
| Skill, skill resource or shared skill-maintenance concern | `evidence/skills/<component>/<record>.md` |

The component identifies the improvement subject and responsible owner, not the
performer who observed it. A named shared concern can own a multi-subject
question, with every subject retained in the record. Create directories only
for actual records; the placement patterns do not declare records for every
role or skill. UI/UX evaluation criteria retain their existing policy sections.

Use the shared [record and exchange contract](../agents/policies/harness/improvement-record-contract.md#public-record-placement),
[metadata schema](../agents/schemas/improvement-record.schema.json) and
[template](../agents/templates/harness-improvement-record.md). The two subject
domains use one format, lifecycle and ID space. This catalog is their only
public discovery list and owns no independent work state or rule authority.

## Select Records

Filter by subjects and cues, then read applicability, readiness, evidence,
exclusions, counterevidence and independent work/knowledge/adoption states.
Finding a record neither assigns work nor adopts a rule. Query all relevant
domains when matching IDs or questions; an absent row does not prove that a
record is missing from the actual collection.

Current records span harness and skill subjects.

| Record | Subjects | Title |
|---|---|---|
| [ir-harness-improvement-adoption-review](agents/harness-improvement/harness-improvement-adoption-review.md) | Harness Improvement, run/evaluation templates, `skills/refine-skill` | Harness improvement adoption review |
| [ir-ui-requested-control-rendering](agents/design-evaluation/requested-control-rendering.md) | Design Evaluation, `skills/screen-alignment` | Requested controls and rendered geometry |
| [ir-ui-state-transition-contracts](agents/interaction-evaluation/state-transition-contracts.md) | Interaction Evaluation, Design Evaluation, `skills/screen-alignment` | Stateful controls and committed intent |
| [ir-ui-native-host-evidence](agents/interaction-evaluation/native-host-evidence.md) | Interaction Evaluation, `skills/screen-alignment` | Native host and end-to-end evidence |
| [ir-skill-distribution-contract](skills/skill-distribution/skill-distribution-contract.md) | `skills` | Skill distribution and removal contract |
| [ir-skill-benchmark-prerequisites](skills/skill-benchmark/skill-benchmark-prerequisites.md) | `skills` | Shared skill benchmark prerequisites |
| [ir-refine-skill-discovery-validation](skills/refine-skill/refine-skill-discovery-validation.md) | `skills/refine-skill` | Refine-skill discovery and static-audit validation |
| [ir-refine-skill-comparable-reruns](skills/refine-skill/refine-skill-comparable-reruns.md) | `skills/refine-skill` | Refine-skill comparable reruns and stability |
| [ir-documentation-adaptive-review](skills/documentation/documentation-adaptive-review.md) | `skills/docs-structuring`, `skills/docs-shaping` | Documentation skill adaptive-review follow-up |
| [ir-documentation-content-role-validation](skills/documentation/documentation-content-role-validation.md) | `skills/docs-structuring`, `skills/docs-shaping` | Documentation content-role validation |
| [ir-context-freshness-independent-maintenance](skills/maintain-context-freshness/context-freshness-independent-maintenance.md) | `skills/maintain-context-freshness` | Independent context maintenance validation |
| [ir-context-freshness-disposal-validation](skills/maintain-context-freshness/context-freshness-disposal-validation.md) | `skills/maintain-context-freshness` | Context archive and deletion validation |
| [ir-context-freshness-claude-discovery](skills/maintain-context-freshness/context-freshness-claude-discovery.md) | `skills/maintain-context-freshness` | Context skill discovery in Claude |
| [ir-pr-review-semantic-corpus](skills/gh-review-pr/pr-review-semantic-corpus.md) | `skills/gh-review-pr` | PR review semantic corpus and comparisons |
| [ir-pr-review-live-validation](skills/gh-review-pr/pr-review-live-validation.md) | `skills/gh-review-pr` | PR review controlled live validation |
| [ir-codex-review-challenger-validation](agents/codex/review-challenger-validation.md) | `agents/adapters/codex/custom-agents/review_challenger.toml` | Codex review-challenger runtime validation |
| [hc-skill-trigger-example](skills/skill-discovery/skill-trigger-example.md) | fictional skill | Synthetic skill discovery reference |

## Maintain And Exchange

Use [Maintain Improvement Records](../agents/operations/harness-improvement.md#maintain-improvement-records)
for the owning record's question, evidence, work and outcome, then update its
catalog row. Retain resolved records for knowledge and history. Resolve
scattered notes into the matching record and remove absorbed documents within
authorized scope, without a separate follow-up list or compatibility copies.

Use the same operation's [export](../agents/operations/harness-improvement.md#export-common-experience)
and [import](../agents/operations/harness-improvement.md#import-improvement-records)
procedures. Private originals and private-to-public associations remain private;
public writes require semantic disclosure review. Mapping v8 imports only
selected records and their rows from this catalog, retaining source/rendered
provenance. Omit the catalog when no records are selected; a skill record does
not install its skill. Unselected relationships remain IDs with evidence limits.
Local results return as reviewed feedback to a later source revision; source
updates do not establish installation or actual use.
