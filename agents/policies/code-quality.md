# Code Quality

## Purpose And Scope

Use this session-wide baseline when writing, changing, reviewing, or refactoring code. Aim for correct, readable changes that fit the project and remain easy to maintain. Explicit task and project requirements govern decisions. Language syntax, formatting rules, and tool settings remain with official sources and consuming projects.

## Decision Rules

- Identify the requested outcome, relevant project rules, contracts, actual versions, and configured quality tools from nearby code and manifest, lock, build, and tool files. Resolve routine choices from evidence; surface consequential unresolved assumptions.
- Follow explicit project rules and required behavior, compatibility, error semantics, and performance. Improve inferred local patterns within scope when concrete evidence shows defects, hidden errors, or needless indirection; age alone is insufficient. Surface and resolve material conflicts with explicit rules before deviating. Keep API, architecture, dependency, and version migrations within authorized scope.
- Judge simplicity by reading and change cost: concepts, state, branches, indirection, and files. Add abstractions, configuration, or dependencies only when a current requirement or meaningful boundary justifies their maintenance cost; single use can be justified. Preserve equally clear, valid approaches; avoid line-count targets and stylistic rewrites.
- Prefer idiomatic code, standard libraries, and established project facilities when semantics and performance fit. Preserve boundary validation, genuine error handling, and meaningful edge cases. Remove defensive branches only when contracts and call paths establish redundancy; do not hide failures to shorten code.
- Keep edits tied to the requested outcome and remove code made unused by the edit. Propose unrelated cleanup separately. Use clear names and comments explaining reasons, constraints, and contracts; retain useful API documentation and complex-algorithm explanations.
- For version-sensitive or uncertain API, syntax, and configuration decisions, verify official documentation against actual project versions. Context7 is an optional retrieval tool; check source ownership, version, and freshness. If it is unavailable or coverage is missing, consult official versioned docs or tagged source and state unresolved gaps. Newer documentation alone does not authorize an upgrade.
- When verification is authorized, reuse relevant configured formatting, lint, type, architecture, and behavior checks in proportion to the change. Evaluate review suggestions against actual requirements. Report actual checks, results, pre-existing failures, and unrun relevant checks. Each result supports only its checked scope; formatting or static-analysis success does not establish correct behavior.

## Ownership And Maintenance

This file owns the platform-neutral policy. The Codex adapter distributes a self-contained `code-quality` block in [global-agents-managed-section.md](../adapters/codex/global-agents-managed-section.md); its [installation guide](../adapters/codex/README.md#baseline-installation) owns merging into global instructions. Ordinary use requires no skill invocation or access to this checkout.

Revise guidance when repeated failures, interference with valid solutions, or relevant version and tool changes expose a gap. Add rules with concrete evidence of benefit; relax rules that cause needless complexity or ceremony. Installation checks establish distribution only. Claims of better code require representative behavioral comparisons with the prior baseline.

## Maintainer References

- [Karpathy Guidelines](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md): task focus, simplicity, scoped changes, and evidence; prescriptions are adapted to project contracts and real boundaries.
- [Google's Code Review Standard](https://google.github.io/eng-practices/review/reviewer/standard.html): technical evidence, explicit style authority, and equally valid design choices.
- [What To Look For In A Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): complexity, current requirements, names, comments, and documentation.
- [Context7 Overview](https://context7.com/docs/overview): documentation retrieval; verify the retrieved source and applicable version.
