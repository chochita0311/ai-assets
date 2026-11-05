# Clean Code Regression Cases

This evaluator resource owns a small, runnable set of synthetic cases for the
[validation record](../validation.md). It is outside the runtime skill package.
The cases were newly authored for replay; they are not the exact temporary
fixtures from earlier trials and do not reproduce every historical check.

## What each file does

- `inputs/TASKS.md` supplies ordinary candidate requests and supported contracts.
- `inputs/pricing.py` supplies an implementation task with duplicated policy,
  forwarding, runtime registration, and a transaction boundary.
- `inputs/publish.py` supplies a read-only review task with a state change across
  an await, deadline equality, failure precedence, and cancellation.
- `check.py` checks externally visible behavior on trusted copies. It does not
  judge readability, authority compliance, structural completion, or selection.

## Run the behavioral checks

Use Python 3.9 or newer with no third-party dependencies, from the repository
root. The checker imports and executes the selected code; use trusted local
fixtures or reviewed candidate output.

```sh
python3 -B evidence/skills/clean-code/regression/check.py
python3 -B evidence/skills/clean-code/regression/check.py --self-test
python3 -B evidence/skills/clean-code/regression/check.py --candidate /path/to/disposable-copy
```

The default command checks the supplied inputs. Pricing intentionally still
has its structural problem; passing behavior checks does not finish that task.
`--self-test` requires the original and two valid cleanup variants (including
module-registry renderer lookup) to pass, then checks six bad edits fail:
deleting the runtime renderer, moving calculation/rendering inside the
transaction, fetching fields before quantity validation, removing the later
state check, changing deadline equality, and omitting awaited release. A seventh
control confirms termination when async finalization blocks. Temporary copies
are owned by the parent and removed automatically, including on failure.

Candidate copies contain both Python modules, with only authorized edits.
The five test methods cover totals, single-pass inputs, validation order,
selected raw error identities, dynamic renderer selection, connection identity,
transaction suppression and exit failures, state/deadline combinations, write
and mark failures, release precedence, and cancellation. Async checks use event
gates, a scheduling yield, and two-second cooperative timeouts. The parent
terminates a check process after 15 seconds if cancellation cannot finish;
the blocked-finalization self-test uses a three-second process bound instead.
These checks do not simulate real network, scheduler, or production timing.
Preserve failures as failures;
do not loosen an oracle merely to accept a candidate.

## Evaluate an agent result

1. Create a fresh disposable workspace containing only `inputs/` contents.
   Give the candidate its tasks and the declared baseline instructions plus the
   selected skill condition. Keep this README, checker, prior results, and
   other candidates outside its accessible evidence. If the host cannot enforce
   that separation, disclose the limit and inspect actual accesses; a new chat
   alone does not establish isolation.
2. Freeze the model/role, instructions, skill files and catalog, source files,
   request, tools and permissions. Record revisions or content hashes and
   actual reads/edits. For a comparison, use separate fresh contexts, identical
   tasks and tools, and record changes in cache/context conditions.
3. Run the checker against the resulting copy. Independently inspect the
   requested outcomes below; do not substitute test counts or line reduction.
4. Keep output, adjudicated findings, corrections, time and total effort at the
   authorized evidence owner. Remove disposable workspaces after evaluation
   and any active diagnosis. Do not feed evaluator findings into an untouched
   trial or describe a corrected rerun as a fresh holdout.

| Task | Separate acceptance judgment |
|---|---|
| Pricing cleanup | Trace preview and checkout to one owner of the full quote rule. Locate where a shipping-policy change would be made. Confirm forwarding no longer adds navigation, runtime renderer lookup remains functional, and transaction ownership stays with checkout. Keep independently changing normalization policies separate. Accept different clear implementations; do not require the self-test's helper name or layout. |
| Publisher review | Report whether any specific reading or change obstacle exists. A justified unchanged result is valid. Treat the two checks as observations at different times; do not call their textual similarity redundancy. Preserve the exact deadline and cleanup/error conditions when describing a proposed change. Verify that the read-only task made no edits. |

These checks are intentionally bounded. They do not cover generated-source
ownership, real integrations, every Python protocol, other languages, human
comprehension, or long sessions. They do not establish an advantage over the
existing Code Quality baseline. Extend only for a concrete unresolved question;
do not turn each language edge into a universal skill instruction.

## Probe selection separately

Use ordinary requests without a skill name in a fresh host context, and inspect
actual resource reads. The expectations below are evaluator criteria, not a
keyword matcher or proof that a host follows descriptions. Supply suitable raw
code/plan artifacts when running a task; otherwise report metadata judgment
only. A plan request can coexist with a separate implementation task, so judge
the actual request rather than demanding exclusive routing in every context.

| Ordinary request | Expected boundary |
|---|---|
| Remove the needless forwarding in this function while preserving behavior. | `clean-code` is relevant; implementation alone does not require `refactor-plan`. |
| Review whether these two checks around an await are redundant; suggestions only. | `clean-code` is relevant; keep the task read-only. |
| Change only this timeout constant from 10 to 15. | Neither skill is needed solely for this mechanical edit. |
| Prepare a phased refactor plan with invariants and validation gates. | `refactor-plan` is relevant; implementation is not implied. |
| Decide whether this refactor preserves parity and is safe to merge. | `refactor-plan` is relevant for the requested checkpoint; preserve its evidence gates. |

Record selection and non-selection separately from task quality. Repeated
observations across contexts are needed for a reliability claim. The description
clarification and this corpus alone do not demonstrate improved host routing.
