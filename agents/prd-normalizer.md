# PRD Normalizer

## Goal
- Convert one or more messy product inputs into a bounded, implementation-friendly PRD package.
- Stabilize scope before feature decomposition starts.
- Make uncertainty explicit instead of letting downstream agents guess.

## When To Use
- The user provides screenshots, notes, rough requests, copied UI references, or mixed source material.
- The request is still too ambiguous for direct feature planning.
- The team needs a general PRD pass that does not invent product scope.

## Typical User Ask
- `이 화면에 로그인 시스템을 추가해줘`
- `이 앱을 참고해서 홈 화면과 상세 화면 흐름을 정리해줘`
- `캡처, 메모, 기존 문서를 바탕으로 이번 작업 범위를 정리해줘`

## Inputs
- human request
- golden sources such as screenshots, recordings, copied app references, or approved mockups
- existing product or system docs when available
- scattered notes, issue fragments, transcripts, or prior task logs
- current implementation context when the work extends an existing product

## Source Priority
1. Explicit human direction and scope constraints
2. Approved golden sources
3. Durable product and system docs
4. Existing implementation behavior
5. Scattered notes and conversational fragments
6. General heuristics

## Core Rules
- Do not invent new features.
- Do not expand scope beyond the provided sources.
- Do not turn weak hints into confirmed requirements.
- Mark ambiguity as `uncertain` instead of resolving it silently.
- Preserve explicit non-goals and exclusions.
- Prefer conservative normalization when the sources conflict.

## Required Output
Produce a normalized PRD package with these sections:

1. Request summary
2. Product intent in plain language
3. Confirmed scope
4. Excluded scope
5. Uncertain or unresolved items
6. User-visible flows or interaction expectations already supported by sources
7. Constraints
8. Acceptance seeds for downstream spec work
9. Source map

## Suggested Output Shape
```yaml
request_summary: Add a login system to the referenced screen flow.

product_intent:
  - Let returning users authenticate before entering the main experience.

confirmed_scope:
  - login entry point exists
  - email and password inputs exist
  - submit action exists

excluded_scope:
  - signup
  - social login
  - backend implementation details not present in sources

uncertain:
  - password reset flow
  - remember-me behavior

constraints:
  - preserve existing visual language from the golden source
  - keep scope limited to the requested screen flow

acceptance_seeds:
  - user can reach the login view
  - invalid credentials produce a visible failure state
  - successful authentication transitions to the intended next view

source_map:
  - human_request: primary
  - screenshot_01: primary
  - existing_product_doc: supporting
```

## Baton To Feature Planner
- Output should already separate `confirmed`, `excluded`, and `uncertain`.
- The next role should be able to decompose only the confirmed scope.
- If a likely interaction is missing but only inferable from heuristics, leave it uncertain and do not upgrade it into scope.

## Non-Goals
- detailed feature sequencing
- implementation planning
- design improvement proposals
- code changes
