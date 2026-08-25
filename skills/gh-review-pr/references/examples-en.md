# English Review Examples

Use these examples only to calibrate English tone and artifact separation. They are synthetic and do not establish facts for a real PR.

Use [review-criteria.md](review-criteria.md) for semantic rules and the [review plan schema](github-publishing.md#review-plan-schema) for exact structure and rendering.

## Contents

- [Review with findings](#review-with-findings)
- [Zero findings](#zero-findings)
- [Coverage gap](#coverage-gap)

## Review with findings

```markdown
## Review summary

This PR replaces stored state in one operation and adds terminal retry reporting, with failure atomicity and observability as the principal risk surfaces.

### Review receipt

| Item | Result |
| --- | --- |
| Profile | `balanced` |
| Snapshot | `8f31c2a` |
| Scope | Six human-authored files were reviewed; two generated clients were covered through their generator and schema. |
| Focus | failure atomicity; terminal retry observability |
| Findings | **1 blocking** · **1 non-blocking** · 0 questions · 0 suggestions |
| Coverage gaps | None recorded. |

### Review evidence

- **Boundary / behavior** — Compared the base and head ordering for durable replacement and exception recovery.
- **Integration / consumers** — Traced exhausted retries through the terminal metrics and alerting consumer.
- **Tests / validation** — Ran the focused failure-path tests and inspected the generated client source contract.

### Review notes

- **Positive** — The generated clients and source schema remain aligned in the same change.
```

```markdown
issue (blocking, high, data-integrity): Preserve existing state when the replacement fails

The new exception path removes the current record before the replacement is durable, leaving retries with no recoverable value. Store the replacement first or restore the original record on failure so the update remains atomic.
```

```markdown
issue (non-blocking, medium, operability): Distinguish exhausted retries from successful completion

The exhausted path emits the same success label as a completed attempt, so production metrics cannot expose this failure mode. Record a distinct outcome label or failure counter so alerts reflect the terminal result.
```

The summary does not repeat finding titles or fixes. Each thread contains the observed behavior, impact, and smallest safe path. The positive note is not counted as a finding.

## Zero findings

```markdown
## Review summary

This PR moves request validation ahead of persistence, with malformed-input handling and write isolation as the principal risk surfaces. No finding met the balanced publication threshold within the reviewed coverage.

### Review receipt

| Item | Result |
| --- | --- |
| Profile | `balanced` |
| Snapshot | `391ad76` |
| Scope | All three human-authored changed files and their direct persistence consumer were reviewed. |
| Focus | validation boundaries; persistence isolation |
| Findings | 0 blocking · 0 non-blocking · 0 questions · 0 suggestions |
| Coverage gaps | None recorded. |

### Review evidence

- **Boundary / behavior** — Compared normal, empty, and malformed inputs at the changed validation boundary in base and head.
- **Integration / consumers** — Traced accepted values to the durable write and confirmed rejected values cannot reach it.
- **Tests / validation** — Ran 12/12 focused validation and persistence-isolation tests successfully. ✅
- **Design / adversarial** — Challenged the strongest partial-write candidate against the transaction behavior.
```

Do not expand this into “safe,” “defect-free,” or “ready to merge.”

## Coverage gap

```markdown
## Review summary

This PR changes authentication callback validation and its deployment configuration, with callback integrity and rollout compatibility as the principal risk surfaces. No finding met the focused publication threshold within the reviewed coverage.

### Review receipt

| Item | Result |
| --- | --- |
| Profile | `focused` |
| Snapshot | `a91e65b` |
| Scope | Seven of nine changed files and the callback consumer were reviewed. |
| Focus | callback validation; deployment compatibility |
| Findings | 0 blocking · 0 non-blocking · 0 questions · 0 suggestions |
| Coverage gaps | 2 recorded; see warning below. |

> [!WARNING]
> **Coverage gaps:**
>
> - One binary file was not reviewable.
> - One provider-truncated diff was not reviewable.

### Review evidence

- **Boundary / behavior** — Compared callback state and redirect validation between base and head.
- **Integration / consumers** — Traced accepted callback data to the session-establishment boundary.
- **Tests / validation** — Inspected the deployment configuration and available compatibility checks; the omitted artifacts remain explicit gaps.
```
