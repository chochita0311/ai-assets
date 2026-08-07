# English Review Examples

Use these examples only to calibrate English tone and artifact separation. They are synthetic and do not establish facts for a real PR.

## Review with findings

```markdown
## Review summary

Reviewed six human-authored files at `8f31c2a`; the review found 1 blocking, 1 non-blocking, and 0 question findings. Two generated client files were covered through their generator and schema.
```

```markdown
issue (blocking, high, data-integrity): Preserve existing state when the replacement fails

The new exception path removes the current record before the replacement is durable, leaving retries with no recoverable value. Store the replacement first or restore the original record on failure so the update remains atomic.
```

```markdown
issue (non-blocking, medium, operability): Distinguish exhausted retries from successful completion

The exhausted path emits the same success label as a completed attempt, so production metrics cannot expose this failure mode. Record a distinct outcome label or failure counter so alerts reflect the terminal result.
```

The summary does not repeat finding titles or fixes. Each thread contains the observed behavior, impact, and smallest safe path.

## Zero findings

```markdown
## Review summary

Reviewed all three human-authored changed files at `391ad76`; the review found 0 blocking, 0 non-blocking, and 0 question findings. No high-confidence finding met the publication threshold within that coverage.
```

Do not expand this into “safe,” “defect-free,” or “ready to merge.”

## Coverage gap

```markdown
## Review summary

Reviewed seven of nine changed files at `a91e65b`; the review found 0 blocking, 0 non-blocking, and 0 question findings. One binary file and one provider-truncated diff remain outside the reviewed coverage.
```
