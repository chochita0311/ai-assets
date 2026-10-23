# Private Harness Experience Store

Use the [setup operation](../operations/harness-improvement.md#configure-local-experience)
and [private-store policy](../policies/harness/harness-improvement.md#activation-and-private-store).
This is a blank portable scaffold. Complete it at the consumer's local
`docs/evidence/STORE.md` by default, or reuse an existing configured equivalent.
Establish the policy's local exclusions before private writes. Keep the filled
store out of shared source, managed import targets and the import manifest.

## Binding

- Record contract version: `1`
- Private store ID:
- Consumer/project identity:
- Environment and audience boundary:
- Authorized local root and authorization: `docs/evidence/` by default, or configured equivalent:
- Effective Git/publication exclusions, tracked/staged conflict check and owner separation:
- Discovery: standard `docs/evidence/STORE.md` entrance pointer, or existing private instruction/context surface:
- Binding state: `ready / unresolved / unavailable`, with reason:
- Common source checkout for authorized export, if resolved; otherwise `unresolved`:
- Recording/retrieval budget or applicable task budget:
- Retention owner and conditions for archiving, moving or deleting evidence:

`ready` requires a resolved, authorized and accessible owner, the applicable
local exclusions and a discovery path for later sessions. An ignored consumer
path is valid under the policy; exclusion alone does not resolve ownership or
untrack files. Do not carry a machine's private binding into another environment
automatically.

## Record Owners

Map these roles to existing owners, or use these paths relative to the local
`docs/evidence/` root. Create records only as needed, not empty placeholder histories.

| Record | Default relative location | Actual owner/location |
|---|---|---|
| Stage observations | `stages/<stage-id>.md` | |
| Bounded comparisons | `experiments/<experiment-id>.md` | |
| Original task inputs/outputs and snapshots needed later | Their existing authorized owner | |
| Reusable knowledge, improvement questions/work and exchange identity | `improvements/<record-id>.md`, or mapped equivalent common records | |
| Actual execution tasks/runs/evaluations | Their existing task owner; linked from improvement records | |
| Private import/export receipt | Existing improvement/task record, or this store when no receipt owner already exists | |

Use [Improvement Record v1](../policies/harness/improvement-record-contract.md)
for reusable asset-level work and experience. Original observations/tasks remain
at their owners. Selected shared references at `agents/`, `skills/` and `README.md`
under this layer retain import ownership; local records do not overwrite them.
Missing or conflicting local ownership leaves session-only observations until
setup is resolved. Refresh preserves this store and its local records.

## Current Target Pointers

Use existing audience-safe task references when they suffice. Otherwise keep a
compact pointer here so resuming a target finds the same stage instead of
creating a duplicate. Historical events remain in their stage records.
With a ready binding, save or reuse the stage at entry, then save the needed
pointer before performing the role. At the closing boundary, save the stage
first, then refresh its pointer with the saved state independently of Improvement
Record creation. Recover a missing pointer from identifiable saved stage evidence;
report ambiguous matches or partial writes instead of resetting or duplicating
records.

| Target | Latest stage/attempt and locator | State / next role |
|---|---|---|

## Improvement Index

| Record ID and locator | Stage/subjects | Cue and eligibility/exclusions | Knowledge/evidence limits | Public record ID and private receipt |
|---|---|---|---|---|

The common record owns knowledge, work/readiness, evidence and adoption state;
this index projects discovery fields from it. Retrieve by subject, cue and
scope, then inspect the actual record, contrary evidence and supersession.
An empty index is valid. Save the record before updating its row and repair
partial writes from the saved record. Do not maintain a parallel lesson list
or asset-specific backlog. Product-only tasks retain their planning owner.

## Exchange Receipt

Reuse the receipt's existing private owner and link it above. If this store is
its resolved owner, record each selected public ID/revision with:

- Request mode: commonization / case-only / review-only, selected project,
  categories/time range, evidence coverage and unavailable history:
- Import purpose: reference or explicitly selected work-candidate:
- Shared source commit, repository-relative source record path and SHA-256;
  imported source revision is distinct from the affected subject's source
  revision/fingerprint:
- Actual installed path and rendered baseline/hash or its manifest entry:
- Local applicability/exclusions, decision and reason; unknown/missing evidence:
- Actual local task/run/evaluation and observed use, or none:
- New local evidence/counterevidence and event identity, or none:
- Export disposition: local / propose promotion / hold / discard and reason;
  authorized common-edit scope and resolved canonical source destination:
- Private-to-public association; structure retained, conditions changed and
  disclosure/meaning review, reviewer and authority; keep identifying notes here:
- Reference/evidence-only versus work-state or normative change, reuse value,
  public-fitness decision and local/hold reason when applicable:
- Export public ID and new revision/source hash, expected prior revision/hash,
  actual committed source or uncommitted candidate, or not exported:
- Case acceptance and normative adoption with scope/authority;
  source change, external publication, consumer refresh and observed activation
  as separate facts; partial writes and next trigger:

Keep local decisions and private-to-public associations here, never in a public
record or import manifest. A source record's work state is not local task state.
No private receipt means no claim that persistent reuse/feedback tracking exists.

## Maintenance

- Last update and responsible actor:
- Unresolved binding, index or evidence gaps:
- Reconciliation or supersession notes:

Reread current records before writing and preserve concurrent work. Do not
reset an unknown index or count a resumed/copy event as new experience.
