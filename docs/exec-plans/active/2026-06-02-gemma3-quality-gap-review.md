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

- 아직 분석 전이다.

## Open Work

- `tc-07`, `tc-11` 품질 gap 분석.
