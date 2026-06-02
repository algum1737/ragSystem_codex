# Gemma3 Top-K 3 Full Eval Plan

## Goal

`gemma3:12b + top_k=3` 조합이 latency 개선과 품질 기준선을 동시에 만족하는지 full eval로 검증한다.

## Scope

- 서버에서 `gemma3:12b`, `top_k=3` full eval 실행
- 전체 지표를 기존 `gemma4:26b`, `gemma3:12b top_k=5` 결과와 비교
- trace latency sample 확인
- 운영 전환 가능 여부 판단

## Out Of Scope

- 운영 기본 모델 즉시 변경
- API 설정 코드 변경
- 프롬프트 변경
- GPU/driver 변경

## Assumptions

- `tc-07`, `tc-11` 2케이스 smoke에서 `top_k=3`은 모두 회복됐다.
- full eval에서 source recall 또는 다른 케이스가 회귀할 수 있으므로 전체 검증이 필요하다.

## Pre-flight checks

- 서버 API 모델이 원래 `gemma4:26b`로 복구되어 있는지 확인
- 서버 `gemma3:12b` availability 확인
- `eval/results/eval_20260602_131307.json` 기준선 확인

## Steps

1. 서버에서 `RAGEvaluator(top_k=3, llm_model="gemma3:12b")` full eval을 실행한다.
2. 결과 리포트를 로컬 저장소로 가져온다.
3. `accuracy_mean`, `faithfulness_mean`, `source_recall@k_mean`, `not_found_success_rate`를 비교한다.
4. 운영 전환 가능 여부와 필요한 후속 변경을 결정한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- eval report 확인
- trace latency sample 확인

## Skipped/Not Run

- 아직 full eval 전이다.

## Open Work

- `gemma3:12b + top_k=3` full eval 실행.
