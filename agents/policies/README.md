# Shared Agent Policies

This directory owns platform-neutral policies used by the agent package and
local AI runtimes. Each policy has one durable owner; runtime installation and
concrete model, tool, and permission bindings belong to adapters.

| Layer | Responsibility |
|---|---|
| `baseline/` | Session-wide defaults: [response clarity and meaning preservation](baseline/response-clarity.md) for answers and authored prose, and [code quality](baseline/code-quality.md) for code work |
| `harness/` | Workflow governance, delegation, execution, continuity, and traceability |
| `review/` | Domain-specific design and interaction evaluation criteria |

These folders classify policy responsibility, not instruction precedence. The
baseline policies work without a harness or skill invocation when installed in
the runtime's instruction chain. Harness and review contracts retain their own
scope, triggers, and evidence boundaries.

Marked runtime sections in the owning policies are the editable sources for the
[generated shared instruction bundle](../instructions/standard.md).
The [shared instruction guide](../instructions/README.md#generated-shared-instructions)
owns source mapping, generation, and freshness checks. Policy files retain
rule ownership when adapters install the generated bundle.

The [adoption guide](../ADOPTION-GUIDE.md) separately owns harness export into
consuming repositories. Its harness and review mappings do not implicitly
install the session-wide baselines or any personal runtime files.
