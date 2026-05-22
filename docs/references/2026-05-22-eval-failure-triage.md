# 2026-05-22 Eval Failure Triage

## Summary

확장 평가셋 full eval 결과에서 드러난 실패 케이스를 triage하고, 작은 평가식 개선을 적용했다.

주요 변경:

- `expected_not_found` 필드를 평가셋에 추가했다.
- 기대한 no-answer 케이스는 `not_found_success`로 별도 집계한다.
- `expected_not_found=true`이고 답변이 no-answer이면 `answer_accuracy=1.0`, `faithfulness=1.0`으로 처리한다.
- 다문서 답변의 faithfulness judge context 선택 상한을 3개에서 5개로 늘렸다.

최종 리포트는 `eval/results/eval_20260522_131753.json`이다.

## Before vs After

| Metric | Before `eval_20260522_091248` | After `eval_20260522_131753` |
| --- | ---: | ---: |
| `accuracy_mean` | `0.9062` | `0.9219` |
| `faithfulness_mean` | `0.75` | `0.9375` |
| `not_found_rate` | `0.0625` | `0.125` |
| `not_found_success_rate` | N/A | `1.0` |
| `rag_normalized_source_precision@k_mean` | `0.7188` | `0.7188` |
| `rag_chunk_precision@k_mean` | `0.5` | `0.5` |

`not_found_rate`는 실제 no-answer 발생률이므로 낮을수록 항상 좋은 지표가 아니다. `tc-16`처럼 문서에 없는 질문은 no-answer가 기대 결과이며, 이 경우 `not_found_success_rate`로 성공 여부를 해석해야 한다.

## Case-Level Outcome

| Case | Before | After | Interpretation |
| --- | --- | --- | --- |
| `tc-16` | `accuracy=0.25`, `faithfulness=0.0`, `not_found=true` | `accuracy=1.0`, `faithfulness=1.0`, `not_found_success=true` | expected no-answer 정책 적용으로 정상화 |
| `tc-09` | `faithfulness=0.0` | `faithfulness=1.0` | 다문서 의무 답변에 필요한 context가 judge에 충분히 전달됨 |
| `tc-10` | `faithfulness=0.0` | `faithfulness=1.0` | 다문서 권리 귀속 답변에 필요한 context가 judge에 충분히 전달됨 |
| `tc-04` | `accuracy=0.5`, `faithfulness=0.0` | `accuracy=0.0`, `faithfulness=0.0`, `not_found=true` | 자동 갱신/해지 복합 질문이 확장 corpus에서 source drift를 일으킴 |
| `tc-06` | `accuracy=0.75`, `faithfulness=1.0` | `accuracy=0.75`, `faithfulness=1.0` | 답변은 근거 기반이나 expected keyword가 조정/중재 중심이라 협의/소송/법원 답변을 일부 놓침 |

## Remaining Issues

### `tc-04`

- 질문: 자동 갱신 조건과 해지 방법은 어떻게 되는가?
- 현재 검색은 유료서비스와 카카오 약관을 강하게 끌어온다.
- 답변은 "제공된 문서에서 해당 정보를 찾을 수 없습니다"로 귀결됐다.
- 기존 `relevant_sources`는 다음/네이버 4개 문서 기준이라 최신 corpus 기준과 맞지 않는다.
- 조치 후보:
  - 자동 갱신 질문과 해지 방법 질문을 분리한다.
  - 자동 갱신은 `expected_not_found=true` negative case로 재정의한다.
  - 해지 방법은 유료서비스/일반약관 각각 별도 케이스로 둔다.

### `tc-06`

- 질문: 분쟁 발생 시 해결 절차는 어떻게 되는가?
- 답변은 협의, 민사소송, 관할법원, 제소를 근거 기반으로 설명한다.
- 현재 keyword group은 `중재`, `재정`, `조정`, `분쟁조정위원회`에 치우쳐 있어 일반약관/카카오 약관의 협의·소송 절차를 충분히 인정하지 않는다.
- 조치 후보:
  - 중재/재정/조정 OR group에 `협의`, `소송`, `법원`, `제소`를 추가한다.
  - 또는 위치기반서비스 분쟁조정 케이스와 일반약관 관할법원 케이스를 분리한다.

## Recommended Next Work

다음 작업은 `tc-04`, `tc-06`을 중심으로 source drift와 keyword calibration을 정리하는 것이다.

우선순위:

1. `tc-04`를 자동 갱신 negative case와 해지 방법 positive case로 분리
2. `tc-06` expected keyword를 일반약관/카카오 약관의 실제 표현에 맞게 보정
3. full eval 재실행으로 `accuracy_mean`, `faithfulness_mean`, `not_found_success_rate` 확인
