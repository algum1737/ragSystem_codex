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

- 배포 후 상태 확인
- 다음 개선 후보 정리
