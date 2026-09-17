---
name: refine-skill
description: Audit or improve an existing skill using observed runs, outputs, or visible package defects. Use for skill reevaluation, failure diagnosis, and comparison of revisions, including a limited static audit when execution evidence is absent. Do not use for creating a new skill, cosmetic-only editing, or performing the target skill's domain task.
---

# Refine Skill

Improve an existing skill's fitness for its intended purpose through evidence, diagnosis, and comparison. Preserve essential content and behavior that already works.

## Operating Modes

Choose the mode from the user's request and existing authorization:

| Mode | When | Result |
| --- | --- | --- |
| `audit` | Review, evaluate, or diagnose; default when changes are not requested | Evidence-backed findings and recommendations; leave the target package unchanged |
| `refine` | Apply requested or already authorized improvements | The smallest justified package changes and a calibrated validation report |

- Continue authorized work without asking for the same permission again. A review request or skill invocation alone does not authorize package changes, external publication, or the target skill's domain actions.
- Real runs are preferred evidence. A current package can support a static audit or correction of a visible defect without prior outputs; it cannot establish behavioral reliability.
- Keep hypothetical concerns separate from observed failures. A justified no-change result is valid in either mode.

## Workflow

1. Read [references/method.md](references/method.md) for either mode. It owns success criteria, diagnosis, file assignment, and validation decisions.
2. Resolve the canonical package and applicable instructions. State the `v1` baseline, evidence limits, and intended success conditions before changing anything.
3. Compare task outcomes and execution evidence. Distinguish skill defects from model, tool, input, and surrounding workflow problems before selecting a fix.
4. In `audit`, report the findings. In `refine`, edit the actual owning files and align affected resources; follow the target package's anatomy rather than imposing this package's filenames.
5. Validate in proportion to the change, compare eligible runs, and record unresolved gaps. Finish with [references/checklist.md](references/checklist.md).

## Output Expectations

Keep the response proportional to the work. Identify:

- the mode, target, and exact baseline evidence;
- material findings, their evidence and likely cause, and the owner of each correction or reason for no change;
- what was compared, what improved or regressed, and which checks actually ran;
- `Result` (`PASS`, `PASS WITH SUGGESTIONS`, or `FAIL`) for the checks performed, separately from `Evidence Coverage` (`complete`, `partial`, or `unavailable`);
- the highest evidence level reached and any missing rerun, confounding change, or remaining follow-up that limits the conclusion.

Report static acceptance and behavioral validation separately when their conclusions differ. Do not present a revised file, a critique of prior output, or a successful one-off run as proof of stable behavior.

## Evidence Handling

- Keep comparison evidence in the session when sufficient. Do not create permanent analysis documents by default.
- When scratch files are needed, use a bounded task-owned temporary location. Keep private transcripts and runtime data outside public checkouts; a repository-local scratch location must follow the repository's rules.
- Before finishing, remove only exact task-created files or directories whose ownership is known and which no active process uses. Never delete a shared scratch root such as `docs/tmp/` wholesale.
- Preserve uncertain ownership and evidence still needed for active diagnosis or recovery; report retained paths, purpose, and cleanup condition. Durable references must point to an explicit durable owner or original evidence, not disposable scratch paths.

## Invocation Examples

- `Use $refine-skill to audit this skill against these recent runs without changing it.`
- `Apply the reviewed improvements to this skill and compare the results on the same task cases.`
- `Audit this existing skill's package; there are no execution records yet.`
