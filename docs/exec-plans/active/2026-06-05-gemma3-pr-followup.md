# Gemma3 PR Follow-Up Plan

## Goal

`feature/gemma3-operating-transition` 브랜치의 운영 전환 변경분을 커밋하고 PR을 생성한 뒤, PR 상태와 남은 후속 작업을 추적한다.

## Scope

- 최종 검증 재실행
- 변경분 커밋
- `gh pr create`로 PR 생성
- PR 생성 결과와 남은 작업 기록
- 후속 리소스 상태 패널/GPU heatmap 변경분 push
- PR CI 상태 재확인

## Out Of Scope

- 추가 모델 튜닝
- token cap 재실험
- PR merge

## Assumptions

- 운영 서버는 `gemma3:12b + top_k=5`, 기본 token cap 없음 상태다.
- token cap 실험은 채택하지 않는다.
- `feature/gemma3-operating-transition` 브랜치에서 PR을 생성한다.

## Pre-flight checks

- `git status --short --branch`
- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py`

## Steps

1. 변경분을 staging한다.
2. 커밋을 생성한다.
3. PR 본문을 한국어로 작성하고 `gh pr create`를 실행한다.
4. PR URL과 검증 결과를 문서와 최종 응답에 남긴다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py`

## Manual/Runtime QA

- 서버 `/health`가 `gemma3:12b`를 반환하는지 확인

## Skipped/Not Run

- full eval 재실행은 하지 않는다. 이미 `gemma3:12b + top_k=5` 기준 full eval과 `top_k=3` 비교 eval을 완료했고, 이번 단계는 변경분 마무리다.

## Open Work

- 리소스 상태 패널/GPU heatmap 변경분을 PR #29 브랜치에 push
- push 후 PR CI 재확인
- 필요 시 리뷰 피드백 반영

## Completion

- 운영 기본 모델 전환 변경분을 커밋했다.
- 커밋 메시지: `운영 기본 모델을 gemma3로 전환`
- PR을 생성했다.
- PR: https://github.com/algum1737/ragSystem_codex/pull/29
- GitHub Actions를 다시 활성화했고 PR #29 `Static checks` 재실행이 통과했다.
- 리소스 상태 패널과 GPU heatmap을 로컬 및 서버에 반영했다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: `.venv/bin/python -m py_compile retriever/llm.py query.py api/main.py app.py`
- 통과: 서버 `/health`
  - `{"status":"ok","model":"gemma3:12b"}`
- 통과: GitHub Actions `Static checks`
  - PR #29 run `26988337943` 재실행 통과
- 통과: 서버 리소스 패널 endpoint
  - `/runtime/resources`, `/runtime/resources/history` 응답 확인
  - RAG 질의 중 GPU 1 utilization `87.0%`, GPU 0/1 VRAM `31.3%`/`81.3%` 샘플 확인
