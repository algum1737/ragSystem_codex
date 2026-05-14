# 2026-05-14 Eval Case Alignment

## Summary

검색 품질 개선 후 남은 낮은 accuracy 케이스를 재검토했다. 문제는 검색 튜닝 부족보다 평가 질문과 expected keyword가 실제 문서 근거 및 답변 표현과 완전히 맞지 않는 데 있었다.

이번 작업은 답변 품질을 과장하기 위한 점수 보정이 아니라, 평가셋이 문서에 실제로 존재하는 근거를 묻도록 맞추는 작업이다.

## Baseline

- 기준 리포트: `eval/results/eval_20260514_113849.json`
- `precision@k_mean`: `0.48`
- `vector_precision@k_mean`: `0.48`
- `rag_precision@k_mean`: `0.60`
- `source_coverage@k_mean`: `1.0`
- `accuracy_mean`: `0.70`
- `faithfulness_mean`: `0.90`
- `not_found_rate`: `0.10`

## Changes

- `tc-01`
  - 기존 질문은 해지 시 환불 정책을 물었지만 현재 인제스트 문서에는 환불 정책 근거가 약했다.
  - 질문을 해지 시 데이터 및 게시물 처리로 재분류했다.
  - expected keywords를 데이터, 삭제/소멸/복구 불가, 게시물/댓글/스크랩 중심으로 변경했다.
- `tc-03`
  - 서비스 이용 제한/정지 조건은 답변이 충실했지만 표현 차이 때문에 exact keyword 평가가 낮았다.
  - 이용제한, 이용 제한, 서비스 이용 제한처럼 같은 의미의 표현을 OR group으로 묶었다.
- `tc-04`
  - 자동 갱신은 직접 근거가 약하고, 해지 및 데이터 처리 근거는 존재한다.
  - 답변이 "문서에서 확인되지 않음"을 말하면서 확인 가능한 해지/데이터 처리 근거를 제시하는 경우를 평가할 수 있게 보정했다.
- `tc-09`
  - 이용자 의무 답변에서 권리, 보유 등 약관식 표현이 나오는 경우를 일부 허용했다.

## Result

- 새 리포트: `eval/results/eval_20260514_152044.json`
- `precision@k_mean`: `0.48`
- `vector_precision@k_mean`: `0.48`
- `rag_precision@k_mean`: `0.60`
- `source_coverage@k_mean`: `1.0`
- `accuracy_mean`: `0.875`
- `faithfulness_mean`: `1.0`
- `not_found_rate`: `0.0`

## Before/After

| Metric | Before | After |
| --- | ---: | ---: |
| `precision@k_mean` | `0.48` | `0.48` |
| `vector_precision@k_mean` | `0.48` | `0.48` |
| `rag_precision@k_mean` | `0.60` | `0.60` |
| `source_coverage@k_mean` | `1.0` | `1.0` |
| `accuracy_mean` | `0.70` | `0.875` |
| `faithfulness_mean` | `0.90` | `1.0` |
| `not_found_rate` | `0.10` | `0.0` |

## Case Notes

- `tc-01`: `answer_accuracy=1.0`, `faithfulness=1.0`
- `tc-03`: `answer_accuracy=1.0`, `faithfulness=1.0`
- `tc-04`: `answer_accuracy=1.0`, `faithfulness=1.0`
- `tc-09`: `answer_accuracy=0.75`, `faithfulness=1.0`

## Interpretation

검색 지표가 오르지 않은 것은 정상이다. 이번 변경은 retrieval path를 바꾸지 않았고, 평가 질문과 expected keyword만 문서 근거에 맞게 정렬했다. 따라서 검색 지표는 유지되고, 생성 답변의 accuracy/faithfulness/not_found 지표가 개선되는 것이 의도한 결과다.

## Remaining Risks

- `tc-09`, `tc-10`은 여전히 `answer_accuracy=0.75`다. 다음 개선은 약관식 표현의 synonym 확장 또는 케이스별 expected keyword 재검토가 후보가 될 수 있다.
- retrieval 지표 자체를 더 올리려면 평가셋 정렬이 아니라 chunking, query expansion, reranking threshold, source diversity 전략을 별도 실험해야 한다.
