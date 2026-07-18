# 한국어 PR 예시

다음 예시는 구조와 문체를 보정하기 위한 가상 사례다. 실제 PR의 사실이나 검증 결과로 복사하지 않는다.

## 목차

- Backend/API
- Frontend/Web
- CI/CD/Jenkins
- Infrastructure/IaC
- Database/Migration
- Library/Dependency
- Mixed/Security and Operations

## Backend/API

근거: 선택 배송지가 없는 주문을 조회하면 `500`이 발생하며, 수정 후 단위 테스트와 API 통합 테스트가 통과했다.

```markdown
Title: 선택 배송지가 없는 주문의 조회 오류 수정

## Summary

선택 배송지가 없는 주문을 조회할 때 발생하던 `500` 응답을 수정했습니다. 배송지 유무와 관계없이 주문 상세를 반환하도록 응답 변환 로직을 보완했습니다.

## Changes

- 선택 배송지에 대한 null-safe 매핑 추가
- 배송지 없는 주문 응답 테스트 추가
- 잘못된 주문 ID의 기존 오류 응답 유지

## Validation

- `./gradlew test`
- API 통합 테스트에서 배송지 없는 주문의 `200` 응답 확인

## Impact

- 배송지 없는 주문을 조회하는 API 소비자의 오류 응답 제거
```

## Frontend/Web

근거: 검색 결과 화면에 빈 상태와 키보드 포커스 스타일을 추가했으며, 컴포넌트 테스트와 Chrome 수동 검증을 수행했다.

```markdown
Title: 검색 결과의 빈 상태와 키보드 탐색 개선

## Summary

검색 결과가 없을 때 사용자가 다음 행동을 이해할 수 있도록 빈 상태를 추가했습니다. 키보드 사용자가 결과 카드의 현재 포커스를 식별할 수 있도록 포커스 스타일도 개선했습니다.

## Changes

- 결과가 없을 때 안내 메시지와 필터 초기화 동작 표시
- 결과 카드에 `:focus-visible` 스타일 적용
- 빈 상태와 키보드 탐색 컴포넌트 테스트 추가

## Validation

- `npm test -- SearchResults`
- Chrome에서 키보드 탐색과 필터 초기화 동작 확인

## Impact

- 검색 결과가 없는 사용자의 복구 경로 제공
- 키보드 탐색 시 포커스 가시성 개선

## Screenshots

- 검색 결과 빈 상태 이미지 첨부
- 결과 카드 키보드 포커스 이미지 첨부
```

## CI/CD/Jenkins

근거: `Jenkinsfile`과 배포 shell script가 변경되었으며, pull request 빌드에서는 배포 단계를 건너뛰고 release branch에서만 실행되도록 했다. `shellcheck`와 Jenkins Replay 검증이 통과했지만 공식 배포 및 롤백 절차는 제공되지 않았다.

```markdown
Title: 릴리스 브랜치로 운영 배포 단계 제한

## Summary

운영 배포 단계가 릴리스 브랜치에서만 실행되도록 Jenkins 조건을 강화했습니다. Pull request와 일반 브랜치 빌드가 운영 배포 스크립트에 진입하지 않도록 실행 경로를 분리했습니다.

## Changes

- 운영 배포 stage에 릴리스 브랜치 조건 추가
- 배포 shell script의 필수 인자 검증 추가
- 조건 불충족 시 배포 stage를 건너뛰도록 로그 보완

## Validation

- `shellcheck scripts/deploy.sh`
- Jenkins Replay에서 pull request 빌드의 배포 stage 생략 확인
- Jenkins Replay에서 릴리스 브랜치의 배포 stage 진입 확인

## Impact

- 운영 배포 trigger 범위를 릴리스 브랜치로 제한

## Deployment and Rollback

- 권장 배포: shared pipeline 반영 후 다음 릴리스 빌드에서 조건 동작 확인
- 권장 롤백: 문제가 발생하면 이전 pipeline revision 복원
```

## Infrastructure/IaC

근거: Terraform으로 애플리케이션 서브넷의 NAT gateway를 변경하며, formatting, validation, staging plan이 통과했다. 운영 apply와 공식 롤백 절차 확인은 수행하지 않았다.

```markdown
Title: 애플리케이션 서브넷의 NAT gateway 구성 분리

## Summary

애플리케이션 서브넷의 외부 통신을 전용 NAT gateway로 분리했습니다. 공유 gateway 장애의 영향 범위를 줄이고 환경별 네트워크 구성을 독립적으로 관리하기 위한 변경입니다.

## Changes

- 애플리케이션 전용 NAT gateway와 route 추가
- 기존 공유 route 참조 제거
- gateway 상태와 오류율 모니터링 항목 추가

## Validation

- `terraform fmt -check`
- `terraform validate`
- staging `terraform plan`에서 리소스 추가와 route 교체 확인
- 운영 apply 미실행

## Impact

- 애플리케이션 서브넷의 outbound route 변경
- NAT gateway 리소스 추가에 따른 비용 증가

## Deployment and Rollback

- 권장 배포: gateway 생성 후 route를 전환하고 outbound 연결 확인
- 권장 롤백: 기존 공유 gateway route 복원 후 신규 gateway 제거
```

## Database/Migration

근거: 주문 테이블에 nullable 컬럼을 먼저 추가하고 애플리케이션 배포 후 backfill하도록 설계했다. migration test와 staging backfill을 완료했다.

```markdown
Title: 주문 처리 채널 컬럼과 단계적 backfill 추가

## Summary

주문 생성 경로를 식별할 수 있도록 `order_channel` 컬럼을 추가했습니다. 기존 데이터와 배포 중인 애플리케이션의 호환성을 유지하도록 nullable 컬럼 추가, 애플리케이션 배포, backfill 순서로 적용합니다.

## Changes

- `orders.order_channel` nullable 컬럼 추가
- 신규 주문의 처리 채널 저장
- 기존 주문을 위한 batch backfill 추가

## Validation

- migration test 통과
- staging에서 100,000건 backfill과 건수 일치 확인

## Impact

- 주문 저장량과 batch 처리 시간의 소폭 증가

## Migration

- 1단계: nullable 컬럼 추가
- 2단계: 신규 값을 기록하는 애플리케이션 배포
- 3단계: 기존 데이터 backfill
- 4단계: 누락 값 확인 후 제약 조건 검토

## Deployment and Rollback

- 확인된 배포 절차: schema, application, backfill 순서로 적용
- 권장 롤백: 애플리케이션의 신규 컬럼 사용 중단 후 backfill 작업 중지
```

## Library/Dependency

근거: HTTP client의 retry API를 새 설정 객체로 이동하고 기존 overload는 deprecated 처리했다. 지원 런타임 전체에서 테스트했다.

```markdown
Title: HTTP client retry 설정 API 통합

## Summary

분산된 retry 인자를 `RetryPolicy` 설정 객체로 통합했습니다. 기존 overload는 호환성을 위해 유지하면서 신규 소비자가 일관된 retry 설정을 사용하도록 API를 정리했습니다.

## Changes

- `RetryPolicy` 공개 설정 객체 추가
- 기존 retry overload를 deprecated 처리
- 기존 인자를 `RetryPolicy`로 변환하는 호환 계층 추가
- 소비자 예제와 API 문서 갱신

## Validation

- `./gradlew test`
- 지원 JDK 버전의 compatibility matrix 통과

## Impact

- 기존 소비자 코드의 동작 유지
- 신규 API 사용 시 retry 설정 방식 변경

## Migration

- 기존 overload는 다음 major release까지 유지
- 신규 코드는 `RetryPolicy` 사용 권장
```

## Mixed/Security and Operations

근거: 대규모 web application PR이 LDAP 인증을 SSO로 전환하고, 구조화된 파일 logging과 Kubernetes mount를 추가하며, 취약한 browser dependency를 교체한다. SSO 수동 검증은 최종 landing까지 확인했지만 logging runtime과 UI regression 검증 근거는 없다. 이전 application artifact와 manifest로 rollback할 수 있으며 관련 보안 이슈와 paired PR이 제공되었다.

```markdown
Title: SSO 전환과 운영 logging 및 browser dependency 보안 개선

## Summary

SAFE 요구사항에 대응하기 위해 기존 LDAP 인증을 SSO로 전환하고 운영 logging 경로를 구조화했습니다. 취약한 browser dependency를 교체하고 관련 출력 처리를 보완해 인증과 web 보안 변경을 함께 적용합니다.

## Changes

### Authentication

- 미인증 요청을 SSO 인증 흐름으로 전환
- callback 응답으로 application session 생성
- logout 이후 SSO 재인증 경로 적용

### Logging and Platform

- application logging을 구조화된 file output으로 전환
- request context를 MDC에 주입
- pod별 log 경로를 위한 manifest와 runtime option 추가

### Dependency Security

- 취약한 jQuery 및 jQuery UI 버전 교체
- 변경된 browser dependency에 맞춰 JSP 출력 처리 보완

## Validation

- Authentication — 수동: callback 처리, session 생성, 최종 application landing 확인
- Logging and Platform — 미확인: pod file 생성과 rotation 결과
- Dependency Security — 미확인: UI regression과 DAST 재검사 결과

## Impact

- 사용자 인증 진입점과 session 생성 흐름 변경
- 운영 log 형식과 pod별 저장 경로 변경
- 공통 browser dependency 변경에 따른 기존 화면 영향 가능성

## Deployment and Rollback

- 권장 배포: manifest와 application artifact를 함께 배포한 후 SSO callback과 pod log 생성을 순서대로 확인
- 확인된 롤백 절차: 이전 application artifact와 manifest 복원

## Review Guide

1. 인증 interceptor와 callback session 처리 검토
2. logging configuration과 request context 주입 검토
3. manifest의 volume 및 runtime option 검토
4. hand-written JSP 변경 검토 후 vendored/minified dependency 확인

## Related Issues

- SAFE-0000
- Paired PR: `example/service#100`
```
