# 2026-05-22 Eval Set Expansion Result

## Summary

평가셋을 기존 10개에서 16개로 확장하고 full eval을 재실행했다. 신규 케이스는 유료서비스, 운영정책, 위치기반서비스, 계정/운영정책, 고지 예외, negative/partial-answer 영역을 포함한다.

최종 리포트는 `eval/results/eval_20260522_091248.json`이다.

## Overall Result

| Metric | Value |
| --- | ---: |
| `total_cases` | `16` |
| `accuracy_mean` | `0.9062` |
| `faithfulness_mean` | `0.75` |
| `not_found_rate` | `0.0625` |
| `rag_normalized_source_precision@k_mean` | `0.7188` |
| `rag_chunk_precision@k_mean` | `0.5` |
| `source_recall@k_mean` | `0.7188` |

확장 전 10개 케이스에서 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0`이었으나, 318개 청크 corpus와 hard case를 반영하자 검색 및 faithfulness 병목이 다시 드러났다.

## Existing vs New Cases

| Group | Cases | Accuracy Mean | Faithfulness Mean | Not Found Rate |
| --- | ---: | ---: | ---: | ---: |
| 기존 10개 | `10` | `0.925` | `0.7` | `0.0` |
| 신규 6개 | `6` | `0.875` | `0.8333` | `0.1667` |

## New Case Result

| Case | Area | Accuracy | Faithfulness | Retrieval Note |
| --- | --- | ---: | ---: | --- |
| `tc-11` | 유료서비스 환불/청약철회 | `1.0` | `1.0` | 유료서비스 source 정확 |
| `tc-12` | 운영정책 게시물 제재 | `1.0` | `1.0` | 운영정책 source 정확 |
| `tc-13` | 위치정보 동의 철회/보유 | `1.0` | `1.0` | 위치기반 source 정확 |
| `tc-14` | 계정 휴면/정지/삭제 | `1.0` | `1.0` | relevant source 일부만 포함 |
| `tc-15` | 서비스 변경/종료 고지 예외 | `1.0` | `1.0` | relevant source 일부만 포함 |
| `tc-16` | 유료서비스 자동 갱신 negative case | `0.25` | `0.0` | retrieval은 정확하나 no-answer 평가 설계 이슈 |

## Failure Classification

| Case | Symptom | Classification | Note |
| --- | --- | --- | --- |
| `tc-04` | `accuracy=0.5`, `faithfulness=0.0`, retrieval 낮음 | 검색 실패 + 평가셋 재정의 필요 | 자동 갱신 질문이 유료서비스 문서를 강하게 끌어오며 기존 relevant source와 불일치 |
| `tc-06` | `accuracy=0.75`, retrieval 낮음 | 검색 실패 + keyword 일부 보정 후보 | 분쟁 해결 질문이 카카오 계정/유료/운영정책으로 확장됨 |
| `tc-09` | `faithfulness=0.0`, retrieval source recall은 1.0 | faithfulness judge/context selection 이슈 | 답변은 다문서 의무를 근거로 설명하나 judge가 NO 반환 |
| `tc-10` | `faithfulness=0.0`, retrieval source recall은 1.0 | faithfulness judge/context selection 이슈 | 답변은 Daum/Kakao/Naver 권리 귀속을 근거 기반으로 설명 |
| `tc-16` | `not_found=true`, `accuracy=0.25`, `faithfulness=0.0` | negative case 평가 설계 이슈 | 답변의 "찾을 수 없습니다"는 의도한 결과이나 현재 accuracy/faithfulness는 실패로 집계 |

## Interpretation

- 확장 평가셋은 의도대로 기존 상한 점수를 깨고 실제 병목을 드러냈다.
- `tc-11`, `tc-12`, `tc-13`은 신규 corpus 검증 케이스로 즉시 사용할 수 있다.
- `tc-14`, `tc-15`는 답변 품질은 좋지만 source recall이 낮아 relevant source 정의 또는 검색 개선 후보로 남는다.
- `tc-16`은 negative/partial-answer 케이스의 채점 정책을 별도로 정의해야 한다. 현재 방식은 no-answer를 `not_found=true`로 잡으면서도 accuracy/faithfulness 평균에는 낮은 점수로 반영한다.

## Recommended Next Work

1. negative case 채점 정책을 개선한다.
   - `not_found=true`가 기대되는 케이스를 명시하는 필드 추가를 검토한다.
   - 기대한 no-answer는 accuracy/faithfulness 실패가 아니라 별도 성공으로 계산한다.
2. faithfulness context selection을 다문서 답변에 맞게 재검토한다.
   - `tc-09`, `tc-10`처럼 답변은 근거 기반이나 judge가 `NO`를 반환하는 케이스를 우선 분석한다.
3. `tc-04`, `tc-06`은 확장 corpus 기준 질문/`relevant_sources`를 재정의한다.
   - 자동 갱신은 유료서비스 문서를 포함한 새 케이스로 분리하는 편이 적합하다.
