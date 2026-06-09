# Concise Mode Trace Review Plan

## Goal

선택형 `concise` answer mode의 실제 사용 trace를 모아 빠른 요약 모드가 별도 경량 평가셋이나 추가 UX 보강이 필요한지 판단한다.

## Scope

- 운영 trace에서 `answer_mode=concise` 사용 사례 확인
- `standard` 대비 응답 길이, latency, source 반환 상태 비교 후보 정리
- concise 전용 경량 평가셋 필요 여부 판단

## Out Of Scope

- 새 기능 구현
- 프롬프트 변경
- full eval 재실행
- 자동 라우팅 도입

## Assumptions

- 선택형 concise mode는 운영 서버에 배포되어 있고 기본값은 `standard`다.
- trace metadata에는 `answer_mode`가 기록된다.
- 현재 단계에서는 실제 사용 로그가 충분하지 않을 수 있다.

## Pre-flight checks

- `git status --short --branch`
- active plan 존재 확인
- 운영 API `/health` 확인

## Steps

1. 운영 trace에서 `answer_mode`별 최근 query 이벤트를 확인한다.
2. concise mode 사례가 충분하면 latency, answer length, source count를 표본 비교한다.
3. 사례가 부족하면 추가 smoke 또는 관찰 기간 연장을 기록한다.
4. concise 전용 경량 평가셋 추가 여부를 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 운영 API `/health`
- 필요 시 `/query` `answer_mode=concise` smoke

## Skipped/Not Run

- full eval은 이 계획의 범위가 아니다. 품질 회귀가 의심될 때 별도 계획으로 실행한다.

## Open Work

- 없음

## Completion

- 운영 API `/health`에서 `status=ok`, `model=gemma3:12b`를 확인했다.
- 운영 trace `/opt/ragSystem_codex/logs/rag_traces.jsonl`에서 `api.query` 성공 이벤트 29건을 집계했다.
- `answer_mode`가 기록된 표본은 `standard` 3건, `concise` 4건이었다.
- 같은 `question_hash` 기준 `standard`/`concise` paired sample 3쌍을 확인했다.
- paired sample 기준 `concise` 평균은 total 5650.12ms, LLM 5536.59ms, answer length 307.33자, source count 5개였다.
- paired sample 기준 `standard` 평균은 total 16088.69ms, LLM 12737.12ms, answer length 496.33자, source count 5개였다.
- 결과 문서는 `docs/references/2026-06-09-concise-mode-trace-review.md`에 기록했다.
- 다음 active plan은 `docs/exec-plans/active/2026-06-09-concise-lightweight-eval-set.md`다.

## Validation Result

- Pre-flight checks: 통과
  - `git status --short --branch`: `## main...origin/main`
  - active plan 존재 확인
  - `curl -fsS http://10.10.220.5:8000/health`: `{"status":"ok","model":"gemma3:12b"}`
- Automated tests: 통과
  - `bash scripts/validate-docs.sh`: `template docs validation passed`
- Manual/Runtime QA: 통과
  - 운영 trace 집계 완료
  - 같은 질문 해시 기준 paired sample 3쌍 확인
- Skipped/Not Run: 추가 `/query` smoke는 실행하지 않았다. 최근 post deploy smoke와 운영 trace 표본이 있어 추가 질의를 만들지 않았다.
