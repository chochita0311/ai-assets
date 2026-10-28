# Reusable Tools

Standalone tools live under `tools/<provider>/<tool>/`. Each tool owns its
source, operating instructions, and checks. These packages are independent of
agent runtime adapters and skills. Repository validation and maintenance tools
remain in [`scripts/`](../scripts/).

| Provider | Tool | Purpose |
|---|---|---|
| Codex | [Reset alert](codex/reset-alert/README.md) | Notify a macOS user about public reset signals. |
