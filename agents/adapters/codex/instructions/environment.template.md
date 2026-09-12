## Corporate Content Access

When looking up, reading, or searching content hosted on
`{{WIKI_HOST}}` or `{{ISSUE_TRACKER_HOST}}`, you must use the MCP named
`{{ACCESS_MCP_NAME}}`.

## GitHub Enterprise PR Commands

A full PR URL for this environment looks like
`https://{{GITHUB_HOST}}/owner/repo/pull/12`.

For `{{GITHUB_HOST}}` repositories, prepend
`GH_HOST={{GITHUB_HOST}}` to the PR-description publication command:

```sh
GH_HOST={{GITHUB_HOST}} gh pr edit <PR-URL> --body-file <candidate-file>
```

The corporate Wiki and issue-tracker access rule above does not replace the
GitHub PR Description workflow; its authorization, publication, and recovery
rules still apply.
