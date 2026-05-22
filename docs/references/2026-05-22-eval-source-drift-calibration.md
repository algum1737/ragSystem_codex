# 2026-05-22 Eval Source Drift Calibration

## Summary

확장 corpus 기준으로 남은 `tc-04`, `tc-06` 실패를 평가셋 정의 문제와 keyword calibration 문제로 분리해 정리했다.

주요 변경:

- `tc-04`의 자동 갱신/해지 복합 질문을 자동 갱신 positive case로 좁혔다.
- 해지/개별 서비스 이용 종료 확인은 `tc-17`로 분리했다.
- `tc-06`의 분쟁 해결 keyword를 확장 corpus의 실제 표현인 협의, 소송, 법원, 제소까지 인정하도록 보정했다.
- `tc-06`의 relevant source에 카카오 통합서비스, 카카오계정, 카카오 유료/결제서비스 약관을 반영했다.

최종 리포트는 `eval/results/eval_20260522_160844.json`이다.

## Before vs After

| Metric | Before `eval_20260522_131753` | After `eval_20260522_160844` |
| --- | ---: | ---: |
| `total_cases` | `16` | `17` |
| `accuracy_mean` | `0.9219` | `1.0` |
| `faithfulness_mean` | `0.9375` | `1.0` |
| `not_found_rate` | `0.125` | `0.0588` |
| `not_found_success_rate` | `1.0` | `1.0` |
| `rag_normalized_source_precision@k_mean` | `0.7188` | `0.7971` |
| `rag_chunk_precision@k_mean` | `0.5` | `0.5882` |
| `source_recall@k_mean` | `0.7188` | `0.7836` |

## Case-Level Outcome

| Case | Change | Result |
| --- | --- | --- |
| `tc-04` | 자동 갱신 조건 positive case로 재정의 | `accuracy=1.0`, `faithfulness=1.0`, `rag_normalized_source_precision=1.0` |
| `tc-06` | 분쟁 해결 keyword와 relevant source를 확장 corpus 기준으로 보정 | `accuracy=1.0`, `faithfulness=1.0` |
| `tc-16` | 유료서비스 자동 갱신의 결제 주기/금액 변경 negative case 유지 | `not_found_success=true` |
| `tc-17` | 서비스 이용계약 해지/개별 서비스 이용 종료 positive case 추가 | `accuracy=1.0`, `faithfulness=1.0` |

## Notes

- `tc-04`는 최초에는 no-answer 후보로 봤지만, full eval 결과 최신 유료서비스 문서에서 정기결제형 서비스의 무료 체험 만료, 등록 결제 수단, 정기 결제 고지, 이용 중단 근거가 확인됐다. 따라서 expected no-answer가 아니라 positive case가 맞다.
- 이 판단은 중간 리포트 `eval/results/eval_20260522_155633.json`에서 `tc-04`가 근거 기반 답변을 생성했으나 expected no-answer로 잘못 평가된 것을 확인한 뒤 반영했다.
- `tc-16`은 "결제 주기와 금액 변경 조건"처럼 더 구체적인 정보를 묻기 때문에 expected no-answer 케이스로 유지한다.
- `tc-06`은 기존 다음/네이버 중심 source만으로는 확장 corpus의 카카오 분쟁 조항을 낮게 평가했다. 현재 corpus 기준에서는 카카오/다음/네이버의 협의, 민사소송, 관할법원, 제소 표현을 함께 인정하는 것이 더 정확하다.

## Recommended Next Work

평가셋은 다시 모든 생성 지표가 1.0에 도달했다. 다음 작업은 평가 케이스 수를 더 늘리기 전에 신규 문서 추가 시 source drift를 자동으로 발견하는 리포트나 regression guard를 검토하는 것이다.
