# Harness Experiment

Use with the installed
[operation](../operations/harness-improvement.md) and
[policy](../policies/harness/harness-improvement.md) for a bounded comparison
once its first authorized trial actually starts. Before execution, prepare the
Comparison Contract below at the existing private task/stage evidence owner;
retain that contract and its original timing in this record when execution
starts. Observation-only work or a proposal cancelled before any trial starts
stays at its existing evidence owner. Include interrupted/incomplete comparisons
with their actual execution limits. Remove inapplicable rows with reasons; use
`unknown — reason` for unavailable facts. Do not create an empty record for every run.

## Identity And Ownership

- Experiment ID:
- Record contract version: `1`
- Record status: `draft / reviewable / closed / superseded`
- Created / updated:
- Private record owner and storage authorization:
- Related feature / run / attempt or session:
- Related ordinary stage and Improvement Records, when they exist:
- Component and change owner:
- Comparison scope and separately authorized follow-on work, if any:

## Problem And Hypothesis

- Expected behavior and governing task criteria:
- Observed behavior and original evidence:
- Cause: `skill/resource / model/execution / tool/environment / input/evidence / surrounding workflow / mixed / uncertain`
- Why that cause and owner; alternative explanations:
- Existing task route: `fix / spec-review / planning-review / continue`; reason:
- Falsifiable hypothesis and authorized change:
- Success checks and falsification checks:
- Applicable conditions and exclusions:
- Related private/public Improvement Records consulted, eligibility/exclusions and why
  their current conditions fit, fail to fit or remain uncertain:

## Comparison Contract — Before Execution

- Baseline and no-change option:
- Candidate IDs, exact versions/snapshots and diff locations:
- Cases: failure, passing, authorized success, no-change, regression, transfer;
  explain relevant inclusions and exclusions:
- Per-case input snapshots and expected checks:
- Producer evidence per check; evaluator-only evidence and admission limits:
- Producer isolation: inherited guidance, cache, prior output, answer key and
  author knowledge; `independent / author check / unknown` with evidence:
- Environment/model differences and expected attribution limits:
- Maximum trials / elapsed time / cost; available measurement:
- Allowed side effects and isolation or substitution:
- Stop conditions:

## Trial Record — Repeat For Each Version, Case And Attempt

- Trial ID / case / baseline or candidate / attempt:
- Logical role/stage and actual performer/runtime, with unknowns and limits:
- Related run/session and execution profile:
- Start / end / actual completion state:
- Input snapshot and supplied task evidence:

### Component Identity And Application

Repeat for each relevant component; do not collapse the identities of siblings.

- Logical source / component path:
- Full source revision, or `unknown`; base revision for a dirty candidate:
- Component content fingerprint / dirty or local diff:
- Accepted import baseline source revision / mapping version:
- Baseline source SHA-256 / baseline rendered SHA-256:
- Actual installed fingerprint:
- Actual supplied-content identity and observation limit:

| Claim | Actual state | Support: observed / declared / unknown | Event or evidence locator | Observation boundary |
|---|---|---|---|---|
| Installed | | | | |
| Provided to this trial | | | | |
| Used at a relevant step | `used / not_used / unknown` | | | |

### Execution Conditions And Original Evidence

- Requested model/settings:
- Observed model/settings and supporting event, or unknown:
- Runtime / tool versions and relevant configuration:
- Inherited global instructions / cached content / isolation differences:
- First output locator:
- Relevant action/read/invocation events, errors and resulting artifacts:
- Interventions, retries and completion evidence:
- Actual elapsed time / task calls / tool calls / retries / user interventions:
- Actual monetary cost and recording effort, or unknown with reason:

## Comparison And Evaluation

| Check / case | Baseline evidence and result | Candidate evidence and result | Counterexample or difference in conditions |
|---|---|---|---|
| | | | |

| Component | Candidate IDs | Edit | Observed difference | Original evidence locator | Effect | Attribution limits |
|---|---|---|---|---|---|---|
| | | | | | `helped / hurt / no observed effect / confounded` | |

- Result: `PASS / PASS WITH SUGGESTIONS / FAIL` for named checked criteria:
- Evidence Coverage: `complete / partial / unavailable` against declared scope:
- Highest evidence maturity: `static validation / resource execution / observed stage execution / fresh forward-test / comparable rerun`; qualify independence/comparability:
- Unverified claim / owning requirement / acceptance impact and reason:
- Preserved passing, authorized-success and no-change controls:
- Stability or transfer claim supported, or not established:

## Disposition And Experience

- Disposition: `keep baseline / apply locally / propose common promotion / hold / discard`
- Selection reason, including baseline and useful edits in rejected candidates:
- Actual stop reason and total measured overhead; unknown measurements:
- Lesson established: `yes / no`; reason:
- Cue and eligibility/exclusion conditions:
- Lesson: component, proposed method and rationale:
- Evidence and counterevidence:
- Confidence and evidence-based reason:
- Tested conditions, limits and revisit triggers:
- Supersedes / contradicted by / scope correction, if any:
- Related [Improvement Record](harness-improvement-record.md) and private index
  update, when reusable knowledge/work is retained; the experiment keeps the
  original comparison, while the common record owns evolving knowledge/work:

## Promotion And Lifecycle

- Public case ID and public candidate location, if created:
- Publication fitness review / case acceptance:
- Common rule owner / promotion decision and authority:
- Actual source change and revision or uncommitted snapshot:
- External publication status:
- Consumer refresh status and accepted manifest, if any:
- Observed runtime activation, separate from installed-file equality:
- Retention owner / cleanup condition / transferred evidence:

Keep the private-to-public link here. Do not copy this record, its private
identifiers, traces or hashes into a public case.
