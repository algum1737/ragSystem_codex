# Concise 06 Failure Triage Plan

## Goal

runbook script가 감지한 `concise-06` 실패를 분석해 prompt 문제인지 평가 기준 문제인지 결정한다.

## Scope

- `concise-06` 최근 실패 report와 trace 확인
- 답변 누락 항목과 retrieved source를 비교
- required point 기준이 과한지, concise prompt가 통지 수단/예외를 누락하는지 판단
- 후속 조치 후보 정리

## Out Of Scope

- 프롬프트 즉시 변경
- 운영 기본 answer mode 변경
- full eval 실행
- 자동 라우팅 구현

## Assumptions

- `concise-06`은 유료서비스 중단/변경 통지 케이스다.
- 최근 실패 report는 서버 `/opt/ragSystem_codex/eval/results/concise_eval_20260610_114205.json`이다.
- failure detection script 자체는 정상 동작했다.

## Pre-flight checks

- `git status --short --branch`
- `docs/references/2026-06-10-concise-eval-runbook-script-result.md` 확인
- 서버 failure report 또는 로컬 기록 확인

## Steps

1. `concise-06` 실패 답변과 required point mismatch를 재검토한다.
2. retrieved source에 통지 수단/예외가 충분히 포함됐는지 확인한다.
3. 평가 기준 조정, prompt 보강, 또는 현 상태 유지 중 하나를 결정한다.
4. 필요하면 별도 구현 계획을 만든다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 필요 시 서버 `concise-06` 단일 query 또는 runbook script 재실행

## Skipped/Not Run

- full eval은 실행하지 않는다.

## Open Work

- 완료됨. 상세 결과는 `docs/references/2026-06-11-concise-06-failure-triage-result.md`에 기록했다.

## Completion

- 서버 failure report `/opt/ragSystem_codex/eval/results/concise_eval_20260610_114205.json`을 확인했다.
- 서버 trace `/opt/ragSystem_codex/logs/concise_lightweight_eval_20260610_runbook_test2.jsonl`을 확인했다.
- 동일 질문 top-5 검색 청크를 확인해 사전/사후 통지 예외 근거가 검색 결과에 포함됨을 확인했다.
- 통지 방법 관련 별도 검색으로 카카오 제6조 청크의 전자우편, 카카오톡, 게시판, 팝업 근거가 벡터스토어에 있음을 확인했다.
- 같은 질문의 `standard`/`concise` 답변을 비교했다.
- `concise` 3회 반복 실행으로 답변 안정성 문제와 deterministic rule 표현 허용 범위 문제를 확인했다.
- 다음 active plan을 `docs/exec-plans/active/2026-06-11-concise-06-stability-fix.md`로 둔다.

## Validation Result

- 통과: `git status --short --branch`
- 통과: `docs/references/2026-06-10-concise-eval-runbook-script-result.md` 확인
- 통과: 서버 failure report 확인
- 통과: 서버 trace 확인
- 통과: 서버 동일 질문 retrieve/top-5 청크 확인
- 통과: 서버 `standard`/`concise` 단일 질의 비교
- 통과: 서버 `concise-06` 3회 반복 smoke
- 통과: `bash scripts/validate-docs.sh`
