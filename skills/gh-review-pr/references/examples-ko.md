# Korean Review Examples

Use these examples only for Korean tone and artifact separation. They are synthetic and are not evidence for a real PR.

## Review with findings

```markdown
## Review summary

이 PR은 저장 상태 교체와 재시도 종료 기록을 변경하며, 실패 원자성과 관측성을 중심으로 `8f31c2a` 기준 human-authored 변경 파일 6개를 검토한 결과 blocking 1건, non-blocking 1건, question 0건입니다. 생성된 client 파일 2개는 generator와 schema 기준으로 확인했습니다.
```

```markdown
issue (blocking, high, data-integrity): 실패한 갱신이 기존 상태를 삭제합니다

새 예외 분기는 저장 성공 여부와 무관하게 기존 record를 먼저 제거해 재시도 시 복구할 값이 남지 않습니다. 새 값의 저장이 완료된 뒤 기존 record를 교체하거나 실패 시 원래 상태를 유지하도록 순서를 바꿔주세요.
```

```markdown
issue (non-blocking, medium, operability): 재시도 종료 원인이 동일한 성공 지표로 기록됩니다

최대 횟수에 도달한 경로도 성공 label을 사용해 운영 지표에서 실패를 구분할 수 없습니다. 종료 원인을 별도 label이나 실패 counter로 기록해 경보가 실제 결과를 반영하게 해주세요.
```

Summary는 finding의 제목이나 수정 방법을 반복하지 않습니다. Thread는 관찰된 동작, 영향, 최소 안전 경로만 담습니다.

## Zero findings

```markdown
## Review summary

이 PR은 요청 검증을 영속화보다 앞 단계로 이동하며, 두 경계의 base/head 동작을 대조해 `391ad76` 기준 human-authored 변경 파일 3개를 모두 검토한 결과 blocking 0건, non-blocking 0건, question 0건입니다. 확인한 범위에서 게시 기준을 충족하는 high-confidence finding은 없었습니다.
```

“문제없음”, “안전함”, “merge 가능”처럼 검토 범위를 넘어서는 결론을 쓰지 않습니다.

## Coverage gap

```markdown
## Review summary

이 PR은 인증 callback 검증과 배포 설정을 함께 변경하며, 해당 경로를 중심으로 `a91e65b` 기준 변경 파일 9개 중 7개를 검토한 결과 blocking 0건, non-blocking 0건, question 0건입니다. provider가 patch를 생략한 binary 1개와 truncated diff 1개는 검토 범위에서 제외했습니다.
```
