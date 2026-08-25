# Korean Review Examples

Use these examples only for Korean tone and artifact separation. They are synthetic and are not evidence for a real PR.

Use [review-criteria.md](review-criteria.md) for semantic rules and the [review plan schema](github-publishing.md#review-plan-schema) for exact structure and rendering.

## Contents

- [Review with findings](#review-with-findings)
- [Zero findings](#zero-findings)
- [Coverage gap](#coverage-gap)

## Review with findings

```markdown
## Review summary

이 PR은 저장 상태 교체와 재시도 종료 기록을 변경하며, 실패 원자성과 관측성이 주요 위험 표면입니다.

### Review receipt

| Item | Result |
| --- | --- |
| Profile | `balanced` |
| Snapshot | `8f31c2a` |
| Scope | Human-authored 변경 파일 6개를 검토했고 생성된 client 2개는 generator와 schema 기준으로 확인했습니다. |
| Focus | 실패 원자성; 재시도 종료 관측성 |
| Findings | **1 blocking** · **1 non-blocking** · 0 questions · 0 suggestions |
| Coverage gaps | None recorded. |

### Review evidence

- **Boundary / behavior** — Base와 head의 durable replacement 순서 및 예외 복구 동작을 대조했습니다.
- **Integration / consumers** — 재시도 종료 결과가 최종 metric과 alert consumer에 전달되는 경로를 추적했습니다.
- **Tests / validation** — 실패 경로 테스트를 실행하고 생성 client의 source contract를 확인했습니다.

### Review notes

- **Positive** — 생성 client와 source schema가 같은 변경에서 함께 갱신됐습니다.
```

```markdown
issue (blocking, high, data-integrity): 실패한 갱신이 기존 상태를 삭제합니다

새 예외 분기는 저장 성공 여부와 무관하게 기존 record를 먼저 제거해 재시도 시 복구할 값이 남지 않습니다. 새 값의 저장이 완료된 뒤 기존 record를 교체하거나 실패 시 원래 상태를 유지하도록 순서를 바꿔주세요.
```

```markdown
issue (non-blocking, medium, operability): 재시도 종료 원인이 동일한 성공 지표로 기록됩니다

최대 횟수에 도달한 경로도 성공 label을 사용해 운영 지표에서 실패를 구분할 수 없습니다. 종료 원인을 별도 label이나 실패 counter로 기록해 경보가 실제 결과를 반영하게 해주세요.
```

Summary는 finding의 제목이나 수정 방법을 반복하지 않습니다. Thread는 관찰된 동작, 영향, 최소 안전 경로만 담고 Positive note는 finding 수에 포함하지 않습니다.

## Zero findings

```markdown
## Review summary

이 PR은 요청 검증을 영속화보다 앞 단계로 이동하며, malformed input 처리와 write isolation이 주요 위험 표면입니다. 검토 범위에서 balanced 게시 기준을 충족하는 finding은 없었습니다.

### Review receipt

| Item | Result |
| --- | --- |
| Profile | `balanced` |
| Snapshot | `391ad76` |
| Scope | Human-authored 변경 파일 3개와 직접 persistence consumer를 모두 검토했습니다. |
| Focus | 검증 경계; persistence isolation |
| Findings | 0 blocking · 0 non-blocking · 0 questions · 0 suggestions |
| Coverage gaps | None recorded. |

### Review evidence

- **Boundary / behavior** — 변경된 검증 경계의 정상, 빈 값, malformed input을 base와 head에서 대조했습니다.
- **Integration / consumers** — 허용된 값은 durable write까지, 거부된 값은 write에 도달하지 않는 경로까지 추적했습니다.
- **Tests / validation** — 관련 validation 및 persistence-isolation 테스트 12/12개가 통과했습니다. ✅
- **Design / adversarial** — 가장 강한 partial-write 후보를 transaction 동작과 대조했습니다.
```

“문제없음”, “안전함”, “merge 가능”처럼 검토 범위를 넘어서는 결론을 쓰지 않습니다.

## Coverage gap

```markdown
## Review summary

이 PR은 인증 callback 검증과 배포 설정을 함께 변경하며, callback integrity와 rollout compatibility가 주요 위험 표면입니다. 검토 범위에서 focused 게시 기준을 충족하는 finding은 없었습니다.

### Review receipt

| Item | Result |
| --- | --- |
| Profile | `focused` |
| Snapshot | `a91e65b` |
| Scope | 변경 파일 9개 중 7개와 callback consumer를 검토했습니다. |
| Focus | callback validation; deployment compatibility |
| Findings | 0 blocking · 0 non-blocking · 0 questions · 0 suggestions |
| Coverage gaps | 2 recorded; see warning below. |

> [!WARNING]
> **Coverage gaps:**
>
> - Provider가 patch를 생략한 binary 1개는 검토하지 못했습니다.
> - Provider가 생략한 truncated diff 1개는 검토하지 못했습니다.

### Review evidence

- **Boundary / behavior** — Callback state와 redirect validation의 base/head 동작을 대조했습니다.
- **Integration / consumers** — 허용된 callback data가 session-establishment 경계에서 소비되는 위치까지 추적했습니다.
- **Tests / validation** — 배포 설정과 가용한 compatibility check를 확인했고 생략된 artifact는 coverage gap으로 유지했습니다.
```
