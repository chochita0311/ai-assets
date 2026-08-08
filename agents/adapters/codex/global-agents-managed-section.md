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

<!-- ai-assets:operator-context-continuity:start -->

## Operator Context Continuity

- The user does not need to invoke a briefing command. Detect orientation requests, new or resumed canonical targets, handoffs, planning returns, material direction changes, partial-evidence review, and meaningful completion boundaries from normal conversation.
- When the current repo exposes the detailed operator-briefing policy, load it only after such a trigger. If no resolvable policy exists, do not synthesize a substitute or create continuity artifacts; keep the normal response unchanged.
- On target activation or resumption, provide at most one self-contained Work Briefing for the unchanged work episode only when prior context materially affects understanding or execution. Explain the objective, causal history, current boundary, next action, and human review need without requiring the user to open links.
- Do not repeat unchanged briefing content on same-target follow-ups. Emit a Direction Alert only for a material conflict or change.
- Emit a Review Receipt only when direction, assumptions, open points, evidence scope, human review, blocking, handoff, or another durable continuity concern materially changed.
- Use plain-language names before IDs, define material internal terms, and treat links as audit evidence rather than a substitute for explanation.
- Briefings and receipts are projections only. They must not create state, alter routing or approvals, duplicate canonical facts, or create permanent artifacts solely for presentation.
- If no relevant context or meaningful delta exists, remain silent and continue the normal response.

<!-- ai-assets:operator-context-continuity:end -->
