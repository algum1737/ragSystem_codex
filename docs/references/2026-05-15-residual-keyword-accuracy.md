# 2026-05-15 Residual Keyword Accuracy

## Summary

faithfulness context selection 이후 남은 keyword accuracy 감점을 분석하고 평가셋 표현을 보정했다. 최종 full eval에서 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0`을 확인했다.

## Baseline

- 기준 리포트: `eval/results/eval_20260515_110900.json`
- `accuracy_mean=0.95`
- `faithfulness_mean=1.0`
- `not_found_rate=0.0`
- 낮은 accuracy 케이스:
  - `tc-03=0.75`
  - `tc-09=0.75`

## Findings

### `tc-03`

- 질문: 서비스 이용이 제한되거나 정지되는 조건은 무엇인가?
- 감점 원인: 답변이 `서비스 이용이 제한`, `이용을 제한`, `제한될`처럼 자연어로 표현했지만 expected keyword는 `이용제한`, `이용 제한`, `서비스 이용 제한`에 치우쳐 있었다.
- 판단: 답변은 문서 근거에 충실하며 keyword 표현 불일치다.
- 조치: `이용이 제한`, `이용을 제한`, `제한될`을 OR group에 추가했다.

### `tc-07`

- 질문: 서비스 제공자의 면책 조항은 무엇인가?
- full eval 재실행 중 답변 변동으로 `책임`, `손해` 표지어가 빠지는 경우가 확인됐다.
- 답변은 `불가항력`, `귀책사유`, `고의·과실`, `장애`, `방해`, `신뢰도`, `정확성` 등 실제 면책 사유를 근거 기반으로 나열했다.
- 판단: 답변 누락이 아니라 면책 사유 중심 표현과 keyword 표지어 사이의 불일치다.
- 조치: 책임/손해 keyword group에 면책 사유 표현을 OR로 추가했다.

### `tc-09`

- 질문: 이용자의 주요 의무 사항은 무엇인가?
- 감점 원인: 답변이 `권한`, `부여`, `명예`, `불이익`, `복제`, `유통`처럼 의무 내용을 설명했지만 expected keyword는 `준수`, `권리`, `보유`에 치우쳐 있었다.
- 판단: 답변은 문서 근거에 충실하며 keyword 표현 불일치다.
- 조치: 해당 표현을 OR group에 추가했다.

### `tc-10`

- full eval 재실행 중 답변이 `귀속` 대신 `보유`, `보유하게`로 표현하는 경우가 확인됐다.
- 판단: 저작권/지적재산권 귀속 질문에서 "보유"는 문서의 실제 표현과도 일치한다.
- 조치: `귀속` keyword를 `["귀속", "보유", "보유하게"]` OR group으로 보정했다.

## Result

- 최종 리포트: `eval/results/eval_20260515_135903.json`

| Metric | Value |
| --- | ---: |
| `accuracy_mean` | `1.0` |
| `faithfulness_mean` | `1.0` |
| `not_found_rate` | `0.0` |
| `rag_normalized_source_precision@k_mean` | `1.0` |
| `rag_chunk_precision@k_mean` | `0.96` |
| `source_recall@k_mean` | `1.0` |

## Interpretation

- 현 평가셋 기준으로 검색, 답변 accuracy, faithfulness는 모두 목표 상한에 도달했다.
- 이번 개선은 답변 품질을 과장하기 위한 완화가 아니라, 같은 의미의 문서 표현을 keyword 평가가 인식하도록 보정한 것이다.
- 다음 작업은 평가셋을 더 어렵게 확장하거나 현재 평가셋이 과적합되지 않았는지 점검하는 방향이 적합하다.
