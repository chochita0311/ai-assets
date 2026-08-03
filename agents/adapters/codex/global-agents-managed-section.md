<!-- Managed by the ai-assets Codex adapter. -->
<!-- ai-assets:competence-routing:start -->

## Competence-First Delegation

- The primary agent owns user intent, requirements, skill selection, architecture, source-of-truth resolution, persistence decisions, integration, and final semantic review.
- Auto-delegate only to an explicitly named custom agent whose role, configured model, modality, tools, permissions, and observed suitability meet the task's competence floor.
- Delegate only work that is independent, bounded, reversible, objectively verifiable, and large or noisy enough to justify delegation overhead.
- Keep a single immediate search, file read, diff summary, or test command with the primary agent when its result is needed for the next decision.
- Never use a generic subagent when a named worker or exact capability binding is required.
- Never silently substitute an unavailable worker with an unspecified or unapproved model.
- When verified official model-lifecycle information indicates that a named worker binding may be stale, report the drift without editing or substituting the binding unless the user approves a reviewed replacement.
- If optional delegation is unavailable, the primary agent performs the task directly.
- If the user explicitly requests an unavailable worker or model, report `REQUESTED_WORKER_UNAVAILABLE` and do not substitute it.
- Pass only a bounded delegation packet and the minimum required artifacts. If full conversational context is required for correctness, keep the task with the primary agent.
- Invoke a differently bound named worker with no history or the smallest bounded recent-turn fork. Do not combine a full-history fork with a custom worker binding.
- The primary agent must complete any skill-governed target resolution, authority classification, reconciliation, approval gate, and persistence decision before delegating downstream evidence or verification work.
- Worker output is evidence, not an implicit implementation, persistence, merge, or completion approval.

<!-- ai-assets:competence-routing:end -->
