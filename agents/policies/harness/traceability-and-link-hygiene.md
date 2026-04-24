# Traceability And Link Hygiene

## Purpose
- Keep generated planning and execution docs portable across machines, repos, and adopters.
- Prevent local filesystem paths and stale artifact references from becoming canonical truth.
- Make traceability useful without making consuming repos depend on the author's workstation.

## Ownership
- This document owns portable reference rules for shared harness artifacts.
- The PRD and feature management policy owns PRD and feature traceability rules.
- The execution-loop governance policy owns run, evaluator, fix, and attempt traceability rules.

## Link Rules
- Use repo-relative paths inside consuming repos whenever the target lives in the same repo.
- Use stable document IDs such as `prd-0001`, `feat-0001`, `spec-0001`, and `run-YYYYMMDD-01` alongside paths.
- Avoid absolute local paths such as `/Users/...` in generated planning, spec, run, evaluation, and fix artifacts.
- Use external URLs only when the source is genuinely outside the repo.
- If a local absolute path is unavoidable during investigation, mark it as temporary evidence and replace it before the artifact becomes durable.

## Artifact Reference Rules
- Feature, spec, run, evaluation, and fix artifacts should reference each other by ID and repo-relative path.
- Historical artifacts may keep old references when rewriting them would obscure useful history, but new templates must use portable paths.
- If a file is renamed because its semantic boundary changed, update active references in the same pass.
- Do not leave active docs pointing to stale folder names after package layout changes.

## Source-Of-Truth Rules
- Distinguish source material from generated artifacts.
- Do not reinterpret a source-of-truth request as a generated-output-only change.
- When a request could target source content, source metadata, generated artifacts, or runtime-derived state, clarify the target before approval.
- When a run changes a source-of-truth contract, generated-data contract, identity model, or route contract, check for stale assumptions in runtime code, generators, tests, scripts, and adjacent docs.
- Use `execution-loop-governance.md` for the detailed rules about recording those checks in run artifacts.

## Validation Checklist
- No new durable artifact contains `/Users/` or another machine-local root.
- Active cross-links resolve from the consuming repo root.
- Contract-changing runs record stale-assumption checks.
- Templates use placeholder paths that can be safely adapted during export.
