# 2026-06-01 Residual Tuning Case Review

## Purpose

`eval/results/eval_20260529_173928.json` 기준 잔여 케이스인 `tc-04` faithfulness 실패와 `tc-17` source recall 저하를 검토하고, 추가 튜닝 방향을 결정한다.

## Baseline Report

- 리포트: `eval/results/eval_20260529_173928.json`
- 평가 기준 모델: `gemma3:12b`
- `top_k`: 5
- `accuracy_mean=1.0`
- `faithfulness_mean=0.9565`
- `not_found_success_rate=1.0`
- `rag_normalized_source_precision@k_mean=0.9891`
- `source_recall@k_mean=0.9891`

Source drift guard 기준으로 `tc-04` faithfulness 0.0은 critical case다.

## tc-04 Review

- 질문: `자동 갱신 조건은 문서에서 어떻게 정해져 있는가?`
- 관련 문서: 카카오 유료/결제서비스 이용약관, 네이버 유료서비스 이용약관
- 검색 상태: `rag_normalized_source_precision_at_k=1.0`, `source_recall_at_k=1.0`
- 답변 상태: `answer_accuracy=1.0`, `faithfulness=0.0`

검색은 정상이다. 실패 원인은 검색 누락이 아니라 생성 답변 또는 faithfulness judge 입력/판정 안정성 쪽이다.

관찰된 답변은 전반적으로 관련 문서 근거를 사용하지만, 기존 결과에는 제공된 컨텍스트 범위를 벗어난 번호 표기 예시가 섞였다. 이 때문에 judge가 unsupported citation으로 판단했을 가능성이 있다.

## Rejected Prompt Experiment

출처 번호를 참고 문서 범위 안에서만 쓰도록 `retriever/engine.py` 프롬프트를 보강하는 실험을 서버에서 수행했다.

단건 `tc-04` 질의에서는 존재하지 않는 번호 표기가 사라졌지만, full eval에서는 다른 케이스가 흔들렸다.

- 실험 리포트: `eval/results/eval_20260601_085420.json` (커밋하지 않음)
- `accuracy_mean=0.9783`
- `faithfulness_mean=0.9565`
- `not_found_success_rate=1.0`
- 새 critical case: `tc-05`, `tc-07`, `tc-11`

결론: 전역 프롬프트 변경은 채택하지 않는다. 단건 개선보다 전체 평가 회귀가 크다.

## tc-17 Review

- 질문: `서비스 이용계약 해지 또는 개별 서비스 이용 종료는 문서에서 어떻게 설명되는가?`
- 현재 relevant sources:
  - 카카오통합서비스약관20210701.pdf
  - 카카오계정약관20240416.pdf
  - 다음 이용약관.txt
  - 네이버 이용약관.txt
- RAG retrieved sources는 카카오통합서비스, 다음, 네이버 이용약관을 포함하지만 카카오계정약관 대신 유료서비스 약관을 포함했다.
- 결과: `rag_normalized_source_precision_at_k=0.75`, `source_recall_at_k=0.75`
- 답변 상태: `answer_accuracy=1.0`, `faithfulness=1.0`

답변 품질은 통과한다. 낮은 source recall은 질문 범위보다 relevant source가 넓게 잡힌 평가셋 source scope 문제일 가능성이 높다.

## Decision

- `tc-04`: 전역 프롬프트 변경은 보류한다. 다음 단계에서 faithfulness judge 입력과 답변 citation 표현을 좁게 진단한다.
- `tc-17`: 검색 튜닝보다 relevant source 범위 재검토가 우선이다.
- 대규모 검색 파라미터 변경은 현재 단계에서 하지 않는다.

## Next Work

다음 active plan에서 `tc-04` faithfulness diagnostic과 `tc-17` source scope calibration을 함께 진행한다.
