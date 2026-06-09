# Post Deploy Monitoring Plan

## Goal

선택형 concise answer mode가 원격 반영된 뒤 운영 API/Web 상태와 사용자-facing 동작을 짧게 모니터링하고 다음 개선 후보를 정한다.

## Scope

- 서버 API/Web health 재확인
- 필요 시 `standard`/`concise` 대표 질의 1회씩 추가 확인
- GitHub Actions success 상태 재확인
- 다음 개선 후보 정리

## Out Of Scope

- 새 기능 구현
- 기본 프롬프트 변경
- 기본 모델 변경
- full eval 재실행

## Assumptions

- 선택형 concise answer mode는 서버에 배포됐고 기본 `standard` full eval은 통과했다.
- GitHub Actions `CI`는 push 후 성공했다.

## Pre-flight checks

- `git status --short --branch`
- `gh run list --branch main --limit 1`
- 서버 `/health`, Streamlit health 확인

## Steps

1. 로컬/원격 동기화 상태를 확인한다.
2. 서버 API/Web health를 확인한다.
3. 필요한 경우 concise mode 대표 질의를 추가 smoke한다.
4. 다음 개선 후보를 정한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- API `/health`
- Streamlit `_stcore/health`
- 필요 시 `/query` standard/concise smoke

## Skipped/Not Run

- full eval은 선택형 concise mode 구현 직후 이미 실행했으므로 재실행하지 않는다.

## Open Work

- 없음

## Completion

- 로컬 `main`은 `origin/main`과 동기화되어 있고 작업트리는 깨끗하다.
- GitHub Actions 최신 `CI` run은 `completed/success` 상태다.
- 운영 API `/health`는 `status=ok`, `model=gemma3:12b`를 반환했다.
- 운영 Streamlit `_stcore/health`는 `ok`를 반환했다.
- 운영 API `/query` smoke에서 `standard`와 `concise` answer mode 모두 status 200, source 5개 반환을 확인했다.
- 다음 개선 후보는 concise mode 사용 로그/trace를 더 모은 뒤, 필요 시 concise 전용 경량 평가셋을 추가하는 것이다.

## Validation Result

- Pre-flight checks: 통과
  - `git status --short --branch`: `## main...origin/main`
  - `gh run list --branch main --limit 1`: `CI`, `completed/success`, run `27179833410`
- Automated tests: 통과
  - `bash scripts/validate-docs.sh`: `template docs validation passed`
- Manual/Runtime QA: 통과
  - `curl -fsS http://10.10.220.5:8000/health`: `{"status":"ok","model":"gemma3:12b"}`
  - `curl -fsS http://10.10.220.5:8501/_stcore/health`: `ok`
  - `/query` `answer_mode=standard`: status 200, source 5개
  - `/query` `answer_mode=concise`: status 200, source 5개
- Skipped/Not Run: 계획대로 full eval은 재실행하지 않았다. 선택형 concise mode 구현 직후 standard full eval이 이미 통과했고, 이번 작업은 배포 후 smoke 모니터링 범위다.
