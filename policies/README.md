# Shared Policies

This directory owns platform-neutral policies shared by skills, harnesses, and
local AI runtimes. Each policy has one durable owner; runtime installation and
concrete model, tool, and permission bindings belong to
[runtime adapters](../agents/README.md#runtime-adapters-package).

| Layer | Responsibility |
|---|---|
| `baseline/` | Session-wide defaults: [response clarity and meaning preservation](baseline/response-clarity.md) for answers and authored prose, and [code quality](baseline/code-quality.md) for code work |
| [competence-first-delegation.md](competence-first-delegation.md) | Shared admission, capability, fallback, context-transfer, and final-ownership rules for delegated work |
| `review/` | Domain-specific design and interaction evaluation criteria |

Harness-specific selection, workflow execution, continuity, and traceability
belong to [harness/policies/](../harness/policies/), whose contracts are mapped
in the [harness overview](../harness/README.md#related-shared-docs).

These owners classify policy responsibility, not instruction precedence. The
baseline policies work without a harness or skill invocation when installed in
the runtime's instruction chain. Harness and review contracts retain their own
scope, triggers, and evidence boundaries.

Marked runtime sections in the owning policies are the editable sources for the
[generated shared instruction bundle](../agents/instructions/standard.md).
The [shared instruction guide](../agents/instructions/README.md#generated-shared-instructions)
owns source mapping, generation, and freshness checks. Policy files retain
rule ownership when adapters install the generated bundle.

The [adoption guide](../harness/ADOPTION-GUIDE.md) separately owns harness export into
consuming repositories. Its harness and review mappings do not implicitly
install the session-wide baselines or any personal runtime files.

[Research Governance](../harness/policies/research-governance.md) owns the optional research
task lifecycle, research authority, state, evidence acceptance and closeout.
[Workflow Governance](../harness/policies/workflow-governance.md) owns selection,
transitions and resource controls. The separately owned
[research-sadr method](../skills/research-sadr/SKILL.md) supplies inquiry and
validation through a pinned local method bundle at adoption. Research selection
does not select Harness Improvement or install runtime actors.

[Harness Improvement](../harness/policies/harness-improvement.md) owns the optional
configured stage retrieval/reflection, cross-component evidence, comparison,
privacy and private-store lifecycle. The [Improvement Record And Exchange
Contract](../harness/policies/improvement-record-contract.md) owns the common format,
identity, states and import/export admission, including revision feedback.
The [common catalog](../evidence/README.md) discovers component-owned
reusable experience and pending improvements under one contract; records do not adopt rules or
assign local work. Adopted rules stay with their existing policy, skill, or
review-asset owner.
