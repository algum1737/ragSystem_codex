# 2026-05-15 Faithfulness Eval Stability

## Summary

최신 유효 리포트 `eval/results/eval_20260514_180006.json`에서 `tc-10`만 `faithfulness=0.0`으로 떨어진 원인을 분석했다. 결론은 답변의 근거 부족보다 faithfulness judge에 전달되는 context 구성 문제다.

## Baseline

- 리포트: `eval/results/eval_20260514_180006.json`
- `tc-10`
  - `answer_accuracy=1.0`
  - `faithfulness=0.0`
  - `not_found=false`
- 검색 지표:
  - `rag_normalized_source_precision@k=1.0`
  - `source_recall@k=1.0`
  - `rag_chunk_precision@k=1.0`

## Answer

`tc-10` 답변은 아래 세 가지를 포함한다.

- Daum 게시물의 저작권/지적재산권은 저작자가 계속 보유한다.
- 네이버 서비스를 통해 타인의 콘텐츠를 이용한다고 해서 이용자가 해당 콘텐츠의 지식재산권을 보유하게 되는 것은 아니다.
- 네이버의 콘텐츠 저작권 및 지적재산권 귀속에 대한 구체적 내용은 문서에 명시되어 있지 않다.

첫 두 문장은 retrieved context 1, 2와 직접 일치한다. 세 번째 문장은 부정형 요약이라 judge가 엄격하게 보면 불안정할 수 있지만, 단건 재현에서는 context 1, 2만 제공할 때 `YES`로 판정됐다.

## Context Check

faithfulness 함수는 `context_texts[:3]`만 judge에 넘긴다.

| Context | Source | Relevance |
| --- | --- | --- |
| 1 | `다음 이용약관.txt` | Daum 게시물 저작권/지적재산권 보유 근거와 직접 일치 |
| 2 | `네이버 이용약관.txt` | 타인 콘텐츠 이용 시 지식재산권을 보유하지 않는다는 근거와 직접 일치 |
| 3 | `다음 이용약관.txt` | 이용 제한/해지 조항으로 `tc-10` 답변 근거와 무관 |

## Judge Reproduction

동일 답변과 동일 검색 결과로 faithfulness judge를 단건 실행했다.

| Judge context | Result |
| --- | --- |
| `context_texts[:2]` | `YES` |
| `context_texts[:3]` | `NO` |
| `context_texts[:5]` | `NO` |

## Interpretation

- `tc-10` 답변의 핵심 내용은 상위 2개 context에 근거한다.
- 현재 judge 입력 방식은 항상 앞 3개 context를 붙이며, 세 번째 context가 질문/답변과 무관해도 그대로 포함된다.
- 무관 context가 추가되면 judge가 "답변 전체가 참고 문서에만 근거하는지"를 과도하게 엄격하게 해석하거나, 부정형 문장을 근거 부족으로 처리해 `NO`를 반환한다.
- 따라서 이번 문제는 검색 recall이나 답변 생성보다 **faithfulness 평가 context selection** 문제로 분류하는 것이 타당하다.

## Recommendation

다음 구현 후보는 faithfulness judge에 전달하는 context를 답변/질문과 더 잘 맞게 고르는 것이다.

우선순위:

1. Faithfulness 전용 context selection 추가
   - 현재 `context_texts[:3]` 대신 질문/답변과 lexical overlap이 높은 context를 우선 사용한다.
   - 최소 구현은 `question + answer` 기준 token overlap으로 top 2 또는 top 3 context를 선택하는 방식이다.
2. Faithfulness prompt 보정
   - "답변의 각 핵심 주장에 참고 문서 근거가 있으면 YES, 무관한 참고 문서가 함께 있어도 NO로 판단하지 말라"는 지시를 추가한다.
3. 답변 생성 프롬프트 보정은 후순위
   - 이전 answer format prompt 실험에서 생성 지표 회귀가 확인됐으므로 우선순위가 낮다.

## Decision

다음 active plan은 faithfulness 전용 context selection의 최소 구현 실험이 적합하다. full eval 전에는 `tc-10` 단건 judge가 `context[:2]=YES`, `context[:3]=NO`로 재현되는지 확인하고, 구현 후 `tc-10`이 `YES`로 안정화되는지 확인한다.
