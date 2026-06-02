# Gemma3 Quality Gap Review Plan

## Goal

`gemma3:12b` 전환 실험에서 하락한 `tc-07`, `tc-11` 품질 gap을 분석하고 기준선 회복 가능성을 판단한다.

## Scope

- `tc-07` answer accuracy 하락 원인 분석
- `tc-11` faithfulness 하락 원인 분석
- 프롬프트 보정, 평가셋 보정, 모델 유지 중 후보 정리
- 필요한 경우 좁은 수정 후보 제안

## Out Of Scope

- 운영 기본 모델 즉시 변경
- 대규모 프롬프트 리라이트
- GPU/driver 변경
- Langfuse 연동

## Assumptions

- `gemma3:12b`는 latency 측면에서 운영 후보가 될 수 있다.
- 운영 전환은 기존 기준선 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0` 회복 여부를 보고 판단한다.

## Pre-flight checks

- `eval/results/eval_20260602_131307.json` 확인
- `eval/test_cases.json`의 `tc-07`, `tc-11` expected fields 확인
- 관련 retrieved sources 확인

## Steps

1. `tc-07`, `tc-11` 답변과 근거 문서를 비교한다.
2. 하락이 실제 품질 문제인지 평가셋/judge 문제인지 분류한다.
3. 최소 수정 후보와 검증 계약을 정리한다.
4. 운영 모델 변경 여부의 다음 판단 기준을 제시한다.

## Automated tests

- `bash scripts/validate-docs.sh`

## Manual/Runtime QA

- 해당 케이스 답변과 retrieved source 샘플 비교

## Skipped/Not Run

- full eval은 실행하지 않았다. `top_k=3` 후보가 정해졌으므로 별도 plan에서 수행한다.

## Open Work

- 없음. 다음 작업은 `gemma3:12b + top_k=3` full eval이다.

## Progress

- `eval/results/eval_20260602_131307.json`에서 `tc-07`, `tc-11` 답변과 지표 확인.
- `eval/test_cases.json`의 expected keywords와 relevant sources 확인.
- 서버에서 같은 RAG retrieval 경로로 `tc-07`, `tc-11` retrieved chunks 확인.
- 프롬프트 후보 3종을 2케이스 대상으로 임시 monkeypatch 검증.
- `top_k=3` 후보를 2케이스 대상으로 검증.
- 결과 문서 작성: `docs/references/2026-06-02-gemma3-quality-gap-review.md`

## Validation Result

- 통과: `tc-07` gap 분류
  - 실제 답변은 근거 충실
  - 하락은 `면책` fixed keyword 표현 불일치
- 통과: `tc-11` gap 분류
  - 실제 answer grounding 문제
  - 불필요한 미확인 섹션과 source 혼합 확인
- 실패/보류: 전역 프롬프트 후보
  - 일부 후보가 `tc-11`을 회복했지만 `tc-07` faithfulness 회귀 발생
- 통과: `top_k=3` 후보 2케이스 smoke
  - `tc-07`: accuracy `1.0`, faithfulness `1.0`
  - `tc-11`: accuracy `1.0`, faithfulness `1.0`

## Completion

- `gemma3:12b` 품질 gap 원인을 분류했다.
- 즉시 프롬프트 변경은 보류했다.
- 다음 실험 후보를 `gemma3:12b + top_k=3` full eval로 정했다.
