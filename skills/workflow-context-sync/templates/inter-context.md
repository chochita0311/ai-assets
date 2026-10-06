# Workflow Context

> Artifact role: dedicated canonical workflow context
> Use only when this exact file is the approved context target; do not add it beside a mature document set by default.

## Context Placement

context home:
context namespace:
canonical context target:
working root:
current repo:
related repos:
target kind: dedicated workflow context
requested durability: durable outcome requested
persistence disposition: initialize after approval
creation authority: explicit user request

alias mapping:
- token:
  resolved path:
  mapping source:
  status: confirmed|open

## Workflow Identity

workflow name:
branch purpose:
current goal:

reconciliation review history (historical evidence, not current-session authority):
- review session:
  review date:
  reconciliation scope:
  user review status: pending|confirmed|not-required|skipped
  approval mode: strict|optional|skip
  review basis:
  downstream blockers: none|describe

## Source Inventory

- id:
  type: repo|ticket|doc|runtime|runbook|note|other
  location:
  role: implementation truth|authoritative spec|planned work|operational signal|working note|historical note
  owner/update path:
  freshness: fresh|stale|unknown
  status: active|open

## Source Relationships

- relation:
  from source:
  to source:
  note:

## Source Of Truth Rules

- domain:
  priority:
  rule:

## Reconciliation Notes

- topic:
  source claims:
    - source:
      claim:
  status: aligned|conflict|open
  working assumption:
  follow-up target:

## Confirmed Facts

-

## Open Questions

-

## Drift Watchlist

-

## Working Targets

working targets:

[current-repo]
- path/to/file

[related-repo]
- path/to/file

planned targets:

[current-repo]
- future module/component

## Recent Decisions

-

## Source Sync Status

dated source observations:
- source:
  observation date or evidence window:
  scope:

source deltas vs canonical context:
- source:
  as-of:
  delta:

external recheck needed: yes|no

## Related Context Artifacts

- path:
  role: working note|historical context|duplicate candidate
  disposition: keep|archive candidate|delete candidate|not evaluated
  action: archive|delete|none
  action status: proposed|approved|applied|not applicable
  archive destination: (exact path for an approved or applied archive)
  note:

## Next Handoff Note

next-session baseline:
-
