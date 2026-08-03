# Competence-First Delegation

## Purpose
- Define when delegated work improves throughput without lowering the competence applied to the task.
- Keep model selection subordinate to task requirements, verification quality, and final ownership.
- Provide a platform-neutral policy that runtime adapters can translate into concrete agent configuration.

## Ownership
- This document owns delegation admission, competence floors, fallback behavior, context-transfer limits, and final-review ownership.
- Runtime adapters own platform-specific configuration, named custom-agent bindings, and installable entrance-policy fragments.
- Concrete model identifiers belong only in runtime binding files, not in this policy.
- Role contracts and workflow policies may narrow this policy for their domain but must not silently weaken its competence floor.

## Core Invariant
Delegation must not be used merely to consume quota, increase agent count, or move work away from the primary agent. Delegate only when the designated worker is demonstrably suitable for the bounded task and the result can be integrated without weakening semantic quality.

When suitability is uncertain, keep the task with the primary agent.

## Terms
- `primary agent`: the root agent that owns requirements, decisions, integration, and final review for the active task.
- `designated worker`: a named custom agent with a narrow role and an explicit runtime model binding.
- `competence floor`: the minimum reasoning, context, modality, tool access, and judgment capability required by a task.
- `delegation packet`: the bounded goal, inputs, constraints, verification, output contract, and stop conditions passed to a worker.
- `opportunistic delegation`: delegation selected automatically because it is expected to save time or isolate noisy context.
- `explicit delegation`: delegation to a worker or model requested directly by the user.

## Competence Floor
Determine the competence floor from the task rather than from a fixed hierarchy of model names. Consider:

- ambiguity and requirement interpretation
- architectural or cross-domain judgment
- amount and locality of required context
- required text, image, audio, or other modality
- tool and sandbox requirements
- security, privacy, compatibility, migration, and operational risk
- whether an objective judge such as a test, type check, diff, or reproducible query exists
- observed reliability for the task class when evidence is available

Latency, cost, or available quota may influence selection only after the competence floor is satisfied.

## Primary-Agent Ownership
The primary agent retains responsibility for:

- interpreting user intent and acceptance criteria
- selecting and sequencing applicable skills
- resolving source-of-truth ownership and conflicting sources
- architecture, public contracts, security, authorization, persistence, migration, concurrency, and compatibility decisions
- deciding whether durable context or artifacts should be created or updated
- integrating worker evidence into the active task
- final semantic review and completion claims

Worker output is evidence or a bounded implementation result. It is never an implicit merge, persistence, or completion approval.

## Delegation Admission Gate
Auto-delegate only when every applicable condition is satisfied:

1. The task is independent enough to complete without continuous coordination with the primary agent.
2. The goal, scope, allowed actions, and output shape can be stated precisely.
3. The worker does not need to make an unrecorded product, architecture, source-of-truth, security, or persistence decision.
4. The result is objectively verifiable through evidence such as file and symbol references, a diff, an exact command, a test, or a reproducible procedure.
5. Failure is reversible and cannot materially damage the active task.
6. Delegation saves meaningful time or isolates enough noisy context to justify its coordination overhead.
7. The named worker's configured capability and permissions meet the task's competence floor.

If any required condition fails, the primary agent performs the work directly.

## Granularity Rule
Do not auto-delegate a single immediate operation when invoking and reintegrating a worker costs more than doing the operation directly. Examples normally retained by the primary agent include:

- one short file read
- one targeted search
- one `git diff --stat`
- one immediately needed test command
- one small observation required for the primary agent's next decision

Prefer delegation for a bounded packet of related, noisy operations such as multi-directory evidence gathering, broad branch-risk inspection, several test shards with failure clustering, or repeated usage tracing.

## Delegation Packet Contract
Every delegated task should provide the smallest sufficient contract:

```text
Goal:
Input artifacts:
Allowed scope and actions:
Forbidden decisions:
Done when:
Verification:
Return format:
Stop conditions:
```

Do not pass full conversational history by default. Pass only the artifacts and decisions needed for the worker's role. If the full conversation is genuinely required for correctness, keep the task with the primary agent.

When the runtime exposes history-fork controls, invoke a differently bound named worker with no inherited history or the smallest bounded recent-turn window that contains its task contract. Do not combine a full-history fork with a custom worker or model binding; full-history inheritance may retain the primary model or invalidate the requested binding.

## Worker Selection And Binding
- Select a stable role first, then invoke the named worker bound to that role.
- Preserve the named worker's binding by using a compatible history-fork mode rather than inheriting the full primary thread.
- Do not use a generic subagent when an exact worker binding or capability guarantee is required.
- Do not infer that a similarly described worker is an equivalent substitute.
- Keep concrete model bindings in platform adapter configuration so model generations can change without rewriting this policy.
- Treat the runtime binding file as the source of truth for the model assigned to each named worker.
- Do not mirror concrete model names into entrance-policy documents. Resolve the active model from the named worker's runtime binding when selection or availability must be verified.

## Availability And Fallback

### Opportunistic Delegation
If the designated worker is unavailable, the primary agent performs the task directly. Do not substitute an unspecified or unapproved worker merely to preserve delegation.

### Explicit Delegation
If the user explicitly requests a particular worker or model and it is unavailable, report:

```text
REQUESTED_WORKER_UNAVAILABLE
requested_agent: <name>
requested_model: <model-or-unknown>
action_taken: no substitution
```

Do not silently replace the request.

### Approved Substitution
A substitute may be used only when an explicit runtime binding or fallback policy confirms that it meets the task's competence floor and the substitution does not violate the user's model request. Cost, speed, or availability alone is not sufficient evidence of equivalence.

## Skill-Aware Sequencing
- The primary agent selects and reads applicable skills before delegating skill-governed work.
- The primary agent retains any target resolution, authority classification, approval gate, source reconciliation, or persistence decision required by the skill.
- A designated worker may receive a bounded evidence or verification task only after those upstream decisions are fixed.
- Worker completion does not bypass a skill's required review or approval boundary.

## Verification And Completion
- A read-only worker must cite concrete files, symbols, commands, or other reproducible evidence.
- A verification worker must run only the authorized checks and distinguish primary failures from cascading failures.
- The primary agent judges whether the returned evidence is sufficient and whether any uncertainty changes task risk.
- Important implementation, architecture, security, compatibility, or persistence outcomes require final review at or above the task's competence floor.
- A worker's statement that no issue was found is not by itself a completion or merge gate.

## Binding Lifecycle

When changing the model behind a named worker:

1. Change the concrete model identifier in the runtime binding file.
2. Validate the binding file's syntax and confirm that installed runtime targets still resolve to it.
3. Install or sync the adapter only to an approved runtime target when its link or file mapping changed.
4. Start a fresh runtime session when configuration or instruction caching may apply.
5. Explicitly invoke the named worker and verify its actual model and permissions before treating the new binding as active.

An official deprecation, retirement, availability change, or new model generation is a binding-review trigger, not authorization for automatic substitution. Keep the current binding until a candidate has been checked against the role's competence floor and verified in the actual runtime.

The role name and this policy should remain stable unless the role contract or competence boundary itself changes.

## Non-Goals
- maximizing delegated token consumption
- defining a permanent ranking of model families
- routing every terminal command through a worker
- allowing workers to make unowned high-level decisions
- making an optional worker a hard dependency for the primary task
