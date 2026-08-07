# Context Freshness Indicators

## Contents

- [Purpose](#purpose)
- [Universal Indicator Principles](#universal-indicator-principles)
- [Strong Freshness Signals](#strong-freshness-signals)
- [Weak Or Misleading Signals](#weak-or-misleading-signals)
- [Cross-Domain Indicator Families](#cross-domain-indicator-families)
  - [Source Code And Version Control](#source-code-and-version-control)
  - [Delivery And Runtime](#delivery-and-runtime)
  - [Pipelines And Data Flow](#pipelines-and-data-flow)
  - [Work Tracking And Delivery Plans](#work-tracking-and-delivery-plans)
  - [Temporal Language, Phase, And Scope](#temporal-language-phase-and-scope)
  - [Incidents And Operational Learning](#incidents-and-operational-learning)
  - [Decisions, Policies, And Standards](#decisions-policies-and-standards)
  - [Data, Research, And Investigations](#data-research-and-investigations)
  - [Runbooks And Operational Procedures](#runbooks-and-operational-procedures)
  - [Learning And Reference Material](#learning-and-reference-material)
  - [Personal And Project Notes](#personal-and-project-notes)
- [Minimal Metadata](#minimal-metadata)
- [High-Stakes Domains](#high-stakes-domains)
- [Reference Models](#reference-models)

## Purpose

Provide general indicators for freshness judgments without imposing one source hierarchy or fixed expiration period on every domain.

Select only the sections relevant to the current target. Treat these as evidence prompts, not automatic deletion rules.

## Universal Indicator Principles

### Freshness Is Claim-Relative

A claim is fresh when it remains valid for its stated scope and time, not when its file was recently edited.

An old historical observation may remain perfectly valid as history. A newly written current-state claim may already be stale if reality changed after it was written.

### Authority Is Domain-Relative

No source wins every question.

- code can prove implementation presence
- a deployment system or runtime can prove what is running or observed
- a work tracker can prove its own workflow state
- a policy owner can prove the effective rule
- a dated study can prove what its source set showed at that time

Record the authority relationship per claim instead of ranking entire systems universally.

### Lifecycle Is Not Binary

Information need not be either current or deleted.

Use current, active, reusable, historical, superseded, and unresolved roles to preserve useful material while keeping current surfaces clear.

### Disposal Requires More Than Freshness

Staleness can justify correction or reclassification. It does not by itself prove that information lacks future value or can be safely removed.

## Strong Freshness Signals

Use combinations of these signals:

- a stronger source directly contradicts a present-tense claim
- an observable state transition occurred, such as merge, deployment, closure, rollback, schema change, or policy replacement
- the claim names a version, branch, owner, date, resource, or dependency that changed
- a successor explicitly supersedes the prior decision, document, or configuration
- an active item now has verified completion evidence
- a current-state document conflicts with another owner for the same claim
- a previously current snapshot now falls outside its stated or implied observation window
- a command, runbook step, or operational assumption fails under the currently supported environment
- the context calls something canonical that no longer owns the decision or fact

## Weak Or Misleading Signals

Do not use these alone:

- old creation or modification time
- no recent links or edits
- a task or incident is complete
- a branch is inactive or merged
- a newer document exists
- two passages look similar
- a file name contains `old`, `todo`, `draft`, `backup`, or a date
- repository search finds no direct reference
- the current agent does not understand why the material exists
- external evidence is inaccessible or was not checked
- a relative deadline or planning window has passed
- a file or package is untracked, uncommitted, or not yet distributed

Completion often changes lifecycle role rather than preservation value. Apparent duplication may hide a distinct constraint, rationale, audience, or evidence trail.

## Cross-Domain Indicator Families

### Source Code And Version Control

Check when claims depend on implementation state:

- current branch and tracked remote
- merge-base and ancestor relationships
- current and historical commit identifiers
- merged versus merely rebased or cherry-picked work
- removed, renamed, or replaced symbols and configuration keys
- dependency, language, or API version applicability
- generated versus hand-owned artifacts

Interpretation guards:

- merge does not prove deployment
- rebase changes current identifiers without invalidating historical evidence
- absence from the default branch does not prove a plan or experiment lacks value
- old code examples may remain useful when clearly version-scoped
- untracked or uncommitted state describes a local work lifecycle; it does not prove staleness, rejection, or lack of future value
- installed-copy drift matters only after canonical-source and distribution authority are known

### Delivery And Runtime

Check when claims depend on deployed or observed behavior:

- deployed release or artifact identity
- environment-specific configuration and feature flags
- startup, health, monitoring, and user-observed behavior
- rollback state and known recovery path
- observation time and environment
- whether evidence reflects one instance or the complete system

Interpretation guards:

- committed or merged code is not production evidence
- one successful observation may not establish continuous health
- user confirmation is valuable operational evidence within its stated scope but does not settle unrelated tracker or compliance states

### Pipelines And Data Flow

When current-state claims describe a pipeline, separate the roles and states that may have different evidence:

- trigger or event origin
- scheduler
- orchestrator
- executor
- progress, state, or completion store
- status and observability surface
- configured destination
- deployed path
- populated or ingested data
- actual consumer use

Interpretation guards:

- one platform or service does not necessarily own every pipeline role
- resource existence or configuration does not prove deployment, population, ingestion, or actual use
- storage, identifier, permission, or dependency drift should trigger a bounded check of the directly affected destructive, reprocessing, rollback, or recovery procedure

### Work Tracking And Delivery Plans

Check when claims depend on workflow state:

- issue and pull request state
- accepted scope and completion criteria
- current owner, reviewer, blocker, due date, and next action
- implementation completion versus formal closure
- optional evidence collection versus a true blocker

Interpretation guards:

- an open ticket can describe already-deployed work
- a closed ticket can leave operational follow-up active
- a plan documents intent and sequencing, not proof of execution

### Temporal Language, Phase, And Scope

Check when current usefulness depends on wording such as `current`, `planned`, `under development`, `launched`, `complete`, `later`, or a relative time window:

- the date, event, or scope that anchors the wording
- whether a later phase transition changed only the label or the underlying action
- whether narrow completion evidence is being used to close a broader task, owner responsibility, or checklist item
- whether a list or index claims current completeness while an owning source explicitly routes to an omitted successor or addition
- whether apparently conflicting phase labels can both be true for different environments, rollout stages, or ongoing development scopes

Interpretation guards:

- an expired relative-time heading can become stale while its child actions remain active or unverified
- a launch does not automatically contradict continued development; compare the claimed scope before choosing `stale` or `conflict`
- narrow completion evidence must not settle a broader claim without scope coverage
- an omitted link is a strong navigation-drift signal only when the surface claims completeness or an authoritative owner explicitly requires that route

### Incidents And Operational Learning

Separate:

- current impact and mitigation
- unresolved preventive actions
- root cause and contributing factors
- timeline and raw evidence
- rollback and diagnostic guidance
- reusable lessons

Interpretation guards:

- resolution makes current impact stale, not the postmortem disposable
- completed action items should leave the active surface but may remain in the historical record
- incident evidence can retain future diagnostic value long after closure

### Decisions, Policies, And Standards

Check:

- decision or policy status
- effective and superseded dates
- named owner or authority
- successor and dependency links
- applicability by product, jurisdiction, version, or environment
- whether current external standards were rechecked when needed

Interpretation guards:

- preserve the original context and rationale of superseded decisions
- do not rewrite an accepted historical decision to reflect later knowledge
- a newer policy does not automatically erase audit or interpretation value in the prior version

### Data, Research, And Investigations

Check:

- observation or extraction date
- source dataset, schema, query, and methodology
- coverage and exclusions
- reproducibility inputs
- whether the output is a snapshot, trend, or present-state assertion
- later schema, source, or population changes

Interpretation guards:

- age does not invalidate a correctly scoped snapshot
- a snapshot becomes misleading when presented as current without its date or source scope
- preserve methodology and evidence needed to reproduce or reinterpret the finding

### Runbooks And Operational Procedures

Check:

- supported system and version
- prerequisites, permissions, and environment
- command or procedure verification
- rollback and failure handling
- current owner and escalation path
- external service, endpoint, credential mechanism, or UI changes

Interpretation guards:

- preserve durable principles even when exact commands change
- a successful past run is evidence for its environment and date, not universal proof
- do not remove rollback or failure guidance merely because the happy path changed

### Learning And Reference Material

Check:

- whether the concept remains valid
- version-specific examples and terminology
- links to current canonical references
- whether the material explains rationale not present elsewhere
- whether onboarding or troubleshooting still benefits from it

Interpretation guards:

- learning value is independent from task completion
- stale examples may need annotation or refresh while the explanation remains reusable

### Personal And Project Notes

Check:

- whether the note records intent, observation, hypothesis, or confirmed fact
- date and source of the observation
- whether later context resolved the uncertainty
- whether the note was ever promoted into a canonical owner

Interpretation guards:

- do not promote a note to truth merely because it is detailed
- do not delete a note merely because it is non-canonical
- preserve unresolved reasoning when it may explain later decisions

## Minimal Metadata

Add metadata only where it prevents future misreading. Useful fields include:

- status or lifecycle role
- `as-of` date or observation window
- valid scope or environment
- source or evidence pointer
- owner
- successor or superseded-by pointer
- last verified date for operational procedures
- confidence or explicit `not checked` note

Do not add every field to every document. Prefer a small marker near the claim it qualifies over a heavy universal header.

## High-Stakes Domains

For legal, regulatory, medical, financial, security, privacy, records-retention, and destructive data decisions:

- verify current authoritative sources by default
- keep evidence scope and date explicit
- preserve conflicts rather than resolving them by convenience
- require domain owner or user approval for consequential actions
- never convert a freshness heuristic into automatic disposal authority

## Reference Models

These sources are design analogies, not universal policies for every context:

- [AWS Architectural Decision Record process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html): accepted decisions retain history and move to a superseded state when a successor is approved.
- [Google SRE Postmortem Culture](https://sre.google/sre-book/postmortem-culture/): incident records preserve learning while follow-up actions remain concrete and trackable.
- [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/): current metadata is tied to explicit ownership and maintained from designated sources.
- [U.S. National Archives General Records Schedule FAQ](https://www.archives.gov/records-mgmt/grs/faqs-about-grs): age-only bucket destruction can remove records still in active use, so disposition requires an applicable authority and scope.

The shared lesson is to separate current state, lifecycle, ownership, historical value, and disposal authority rather than collapsing them into one freshness score.
