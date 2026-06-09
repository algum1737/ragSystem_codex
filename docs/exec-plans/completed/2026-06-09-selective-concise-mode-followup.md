# Selective Concise Mode Follow-Up Plan

## Goal

선택형 concise answer mode 구현 변경분을 커밋하고, 필요 시 원격 반영과 후속 확인을 진행한다.

## Scope

- 현재 변경분 검토
- 로컬 검증 재확인
- 커밋 생성
- 필요 시 push 또는 PR 후속 판단
- handoff 갱신

## Out Of Scope

- 추가 기능 구현
- 기본 모델 변경
- 기본 프롬프트 변경
- `top_k` 동작 변경

## Assumptions

- 선택형 concise mode 구현은 서버에 반영됐고 smoke/full eval 검증을 통과했다.
- 현재 운영 기본값은 `standard`다.
- 로컬 `main`은 이미 `origin/main`보다 앞선 커밋이 있다.

## Pre-flight checks

- `git status --short --branch`
- 최신 검증 결과 확인
- `docs/references/2026-06-09-selective-concise-answer-mode-result.md` 확인

## Steps

1. 변경 파일과 diff를 확인한다.
2. compile/docs 검증을 실행한다.
3. 변경분을 커밋한다.
4. 원격 반영 여부를 결정한다.

## Automated tests

- `.venv/bin/python -m py_compile retriever/engine.py api/models.py api/main.py query.py app.py eval/pipeline.py scripts/concise_prompt_experiment.py`
- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 이미 완료된 서버 API/Web health, API smoke, standard full eval 결과를 재확인한다.

## Skipped/Not Run

- 추가 full eval은 코드 변경이 없으면 재실행하지 않는다.

## Open Work

- 없음. 선택형 concise mode 구현 변경분은 커밋 대상으로 정리하고, 원격 반영과 CI 확인은 다음 active plan으로 넘긴다.

## Completion

- 선택형 concise answer mode 구현 변경분을 검토했다.
- 로컬 compile/docs 검증을 재실행했다.
- 서버 API/Web health, API smoke, standard full eval 결과를 handoff와 결과 문서에 반영했다.
- 변경분은 커밋 대상으로 정리한다.
- 원격 push와 GitHub Actions 확인은 `docs/exec-plans/active/2026-06-09-push-and-ci-verification.md`에서 추적한다.

## Validation Result

- 통과: `git status --short --branch`
- 통과: `.venv/bin/python -m py_compile retriever/engine.py api/models.py api/main.py query.py app.py eval/pipeline.py scripts/concise_prompt_experiment.py`
- 통과: `bash scripts/validate-docs.sh`
- 통과: 서버 API/Web health 확인은 `docs/references/2026-06-09-selective-concise-answer-mode-result.md`에 기록된 결과를 재확인했다.
- 통과: 서버 API smoke 및 standard full eval 결과는 `docs/references/2026-06-09-selective-concise-answer-mode-result.md`에 기록된 결과를 재확인했다.
