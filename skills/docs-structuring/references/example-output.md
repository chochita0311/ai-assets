# Example Output

Use this as a shape reference for a full `docs-structuring` pass.

This is an example of the reporting format, not a mandatory literal template.

For a bounded or unchanged pass, use a compact result instead (see the closing examples).

## Operating Mode Used
- `incremental`

## Review Coverage
- Reviewed the five documents below and checked affected ownership pointers; this is not a semantic audit of every other repository document.

## Doc-Role Map
| File | Role | Owner Level | Current Problems | Planned Action |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | entrance | entrance | duplicates setup summary from `README.md` | tighten and keep as contributor entrance |
| `CLAUDE.md` | entrance | entrance | duplicates `AGENTS.md` too closely | align as parallel AI entrance file |
| `README.md` | overview | overview | duplicates setup and project summary from deeper docs | keep user-facing overview and own setup |
| `docs/handbook.md` | mixed-purpose | mixed | mixes policy, architecture, setup, roadmap, and package-local guidance | move setup and package-local guidance to existing owners; retain project sections and propose an optional file split |
| `packages/payments/README.md` | specialized reference | package | already owns local package flags clearly | keep in place and link from overview docs if needed |

## Ownership Changes
- `README.md` becomes the owner of local run instructions.
- `AGENTS.md` and `CLAUDE.md` become entrance-layer files only.
- `docs/handbook.md` stops being the owner of setup and package-local guidance; it retains policy, architecture, and roadmap in its existing sections.
- `packages/payments/README.md` remains the owner of payments-specific flags.

## Before -> After Structure Summary
- Before:
  - duplicated setup instructions across entrance docs, overview doc, and handbook
  - one mixed-purpose handbook file owned too many responsibilities
  - package-local guidance was duplicated in both central docs and package docs
- After:
  - entrance files route to owned docs
  - `README.md` owns overview and setup
  - `docs/handbook.md` still owns policy, architecture, and roadmap in its existing sections
  - package-local guidance stays near the package owner

## Moved Content Summary
- local run steps moved from `AGENTS.md`, `CLAUDE.md`, and `docs/handbook.md` into `README.md`
- payments environment flag guidance removed from `docs/handbook.md` and left in `packages/payments/README.md`
- policy, architecture, and roadmap content retained in `docs/handbook.md`; none was moved into separate files

## Removed Duplication Summary
- removed repeated repository description from `AGENTS.md`, `CLAUDE.md`, and `README.md`
- removed repeated local run command from four files down to one owner
- removed repeated payments package flag notes from central and local docs

## Cross-Link Additions
- `AGENTS.md` -> `README.md` for overview and setup
- `CLAUDE.md` -> `README.md` and `AGENTS.md`
- `README.md` -> the policy, architecture, and roadmap sections of `docs/handbook.md`
- central project docs -> `packages/payments/README.md` only when package-local context is needed

## Suggested-Only Restructures
- consider splitting `docs/handbook.md` into separate policy, architecture, and roadmap docs if the repository keeps growing; this split was not applied and requires approval
- consider adding a docs index if more specialized doc areas appear later

## Decision Confidence Summary
- `high`
  - keep setup owned by `README.md`
  - keep package-local flags owned by `packages/payments/README.md`
  - align `AGENTS.md` and `CLAUDE.md` as entrance-layer docs
- `medium`
  - split `docs/handbook.md` into several docs if growth continues
- `low`
  - whether a separate docs index is needed immediately

## Unresolved Or Low-Confidence Items
- whether the repository needs a separate roadmap file yet
- whether `CLAUDE.md` should remain distinct in tone or mirror `AGENTS.md` more closely

## Compact Scope Examples

- End-of-task update in a non-Git knowledge base: "Incremental review followed the completed migration's status owner and references. Updated the active summary and its stale plan pointer; preserved the dated incident account. Other workstreams were not substantively reviewed. No unresolved ownership issues in the reviewed set."
- Follow-up after those edits: "Rechecked the changed status passages and affected pointers against the prior review. No new drift or ownership conflicts; no further changes. This was a follow-up, not a fresh whole-target audit."
- Whole-set upkeep after growth: a request to keep the expanded documentation coherent can start with all active owners and their relationships, even without the words "full audit" or a previously identified defect. The task itself justifies broad discovery.
- Explicit full audit: inventory the entire selected target, review each requested ownership relationship, and report any unexamined areas as gaps. A small or unchanged patch does not reduce the requested review coverage.
