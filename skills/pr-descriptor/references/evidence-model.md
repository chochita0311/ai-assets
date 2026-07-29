# Evidence Model

Use this reference to decide what can be stated as fact, how validation should be collected, and how operational recommendations must be labeled.

## Contents

- Artifact snapshot and source priority
- Evidence states
- Concern ledger
- Validation acquisition
- Validation alignment
- Manual validation
- Operational provenance
- Sensitive information

## Artifact snapshot and source priority

Freeze the PR subject before classifying claims:

- For an existing PR, use its committed base and head plus the resulting base-to-head diff
- For a local branch draft, use the committed merge base and `HEAD`
- Include working-tree or untracked changes only when the user explicitly asks for an artifact describing the intended future head

Apply source priority in this order:

1. The frozen current-head snapshot for claims about what the PR changes
2. Notes explicitly supplied for the current artifact, including scoped manual validation and motivation
3. Committed repository documentation, CI records, logs, and issue context that can be tied to the snapshot
4. Clearly labeled inference or an explicit unknown state

Earlier session details, local scratch files, discarded approaches, dirty working-tree changes, and untracked helpers are background rather than PR evidence. Do not name them in the artifact or use checks that depend on them as validation. Repository files outside the diff may explain a current-head change, but do not list them as changes.

If ambient context conflicts with the frozen snapshot, the snapshot wins for `Changes`. If a user-provided result applies to a materially different temporary setup, omit it unless the user explicitly asks to preserve that difference.

## Evidence states

Assign each material claim one internal state before drafting:

- `Observed`: directly supported by the frozen snapshot, or by a committed repository file used to interpret that snapshot
- `Provided`: explicitly supplied for the current artifact by the user, an issue, an existing PR, a runbook, or another identified source
- `Verified`: supported by an executed command, CI result, log, screenshot, or observed manual outcome
- `Inferred`: a reasonable consequence, risk, recommendation, or proposed follow-up derived from the evidence
- `Unknown`: not established by the available evidence

Use the state to control wording:

- State `Observed` current-head changes as facts
- Attribute or faithfully preserve `Provided` evidence without pretending it was independently rerun
- State `Verified` evidence with its scope and observed result
- Mark `Inferred` content with language such as `possible`, `recommended`, `proposed`, `expected`, or `requires confirmation`
- State material `Unknown` validation or operational gaps explicitly

Never strengthen a source while paraphrasing it. A routing diagram proves intended topology, not a successful request. A commit message mentioning tests is not equivalent to an observed passing command or CI job.

Negative and exclusive claims require evidence across the relevant scope. Do not state `no impact`, `unchanged`, `not included`, `only`, or an equivalent absolute merely because no contradiction appeared in the inspected subset. Qualify the scope or mark the claim as unverified.

## Concern ledger

Build the ledger around reviewer concerns rather than files:

```text
Concern | Current-head change | Why | Validation | Impact | Transition | Rollout source | Review entry point
```

- Merge closely related files into one concern such as `Authentication`, `Browser Security`, `Logging and Platform`, or `Database Migration`
- Keep materially different failure modes in separate concerns
- Use the same concise concern label and order in `Changes`, `Validation`, and `Review Guide` when present
- Map validation at concern level, not once per file or atomic bullet
- Do not let validation of one concern imply validation of another

## Validation acquisition

Use evidence in this order:

1. Results explicitly supplied for the current artifact and evidence from the frozen PR snapshot
2. Repository CI records, test reports, logs, screenshots, and documented commands already available locally
3. Fast, bounded, read-only local checks that are relevant and already supported by the environment
4. Explicit unverified status

When local repository inspection is authorized:

- Run `git diff --check <base>...<head>` unless the repository context makes it inapplicable
- Run syntax or parse checks for changed shell, JSON, YAML, XML, or similar configuration when the required tool is already installed
- Run focused repository-documented tests only when they are bounded, do not require dependency installation or network access, and are proportionate to the request
- Do not install dependencies, trigger external CI, deploy, mutate environments, or access production merely to improve a PR description unless the user explicitly requests it
- Record the exact command and observed outcome when reproducibility is useful
- If a command is unavailable, incomplete, or fails, report that state without converting it into a pass

Do not discard valid manual evidence explicitly provided for the current artifact merely because it is absent from Git history. Preserve its scope and avoid extending it to unexercised paths. A check that requires uncommitted helper code, temporary local configuration, or another artifact absent from the frozen head is not reproducible PR validation and should be omitted unless the user explicitly asks to preserve that setup difference.

## Validation alignment

For each material concern, include one of:

- a completed command, CI job, or manual check with its result
- a provided result with its actual scope
- `Not run` with the reason when the check was intentionally not applicable or not executed
- `Not verified from the available evidence` for an unknown result

Prefer a stable labeled form:

```markdown
- Authentication — Manual: verified callback handling and final landing in the dev environment
- Logging and Platform — Local: `xmllint --noout ...` passed; runtime file creation not verified
- Dependency Security — Not verified from the available evidence: UI regression and security rescan
```

Translate labels and explanatory text to the selected language while preserving commands and job names. Use the same label style throughout one artifact.

## Manual validation

A manual validation statement must contain:

- the exercised environment or action
- the observable outcome
- any material difference between the tested setup and final head

Treat setup instructions, hosts mappings, routing diagrams, and intended flows as context unless an observed outcome is also supplied. If temporary configuration was reverted, credit only behavior explicitly supplied for the current artifact and disclose the final-head difference.

## Operational provenance

Separate established procedure from useful inference:

- `Confirmed`: supported by explicit user evidence, a repository release document, a runbook, or an existing verified operational procedure
- `Recommended`: a reasonable rollout, verification, or recovery step derived from the diff
- `Unknown`: no supported procedure was found

Never present a `Recommended` or `Unknown` step as an established deployment or rollback procedure.

Use only the applicable labels. For Korean output:

```markdown
- 확인된 배포 절차: <supported procedure>
- 권장 배포: <diff-inferred rollout step>
- 권장 확인: <diff-inferred verification>
- 확인된 롤백 절차: <supported recovery procedure>
- 권장 롤백: <diff-inferred recovery step>
- 미확인: <unsupported or unavailable operational procedure>
```

For English output:

```markdown
- Confirmed deployment: <supported procedure>
- Recommended deployment: <diff-inferred rollout step>
- Recommended check: <diff-inferred verification>
- Confirmed rollback: <supported recovery procedure>
- Recommended rollback: <diff-inferred recovery step>
- Not verified: <unsupported or unavailable operational procedure>
```

Keep rollout recommendations in `Deployment and Rollback`. Put the operational consequence in `Impact` and any code-review action in `Review Guide` instead of repeating the same sentence.

## Sensitive information

- Mention the presence, category, and reviewer-relevant location of a sensitive value without reproducing the value
- Do not expose tokens, passwords, private endpoints, credential payloads, or exploit details merely for completeness
- Distinguish an observed secret-management concern from a claim that a credential is compromised
- Keep security review recommendations proportional to the evidence
