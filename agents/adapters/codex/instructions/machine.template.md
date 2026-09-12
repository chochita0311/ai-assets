## Local Context Aliases

When the user mentions a shortened local context path, resolve it as follows:

- `context/...` means `{{CONTEXT_ROOT}}/...`.
- `c/...` means `{{CONTEXT_ROOT}}/...`.
- `work/...` means `{{WORK_ROOT}}/...`.
- `ai-assets/...` means `{{AI_ASSETS_ROOT}}/...`.

Examples:

- `context/topic` means `{{CONTEXT_ROOT}}/topic`.
- `c/topic` means `{{CONTEXT_ROOT}}/topic`.
- `work/project` means `{{WORK_ROOT}}/project`.
