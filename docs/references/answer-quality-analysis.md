# Answer Quality Analysis

분석 기준 리포트: `eval/results/eval_20260513_134658.json`

## Current Metrics

- `vector_precision@k_mean`: `0.48`
- `rag_precision@k_mean`: `0.54`
- `source_coverage@k_mean`: `0.925`
- `accuracy_mean`: `0.625`
- `faithfulness_mean`: `0.8`
- `not_found_rate`: `0.2`

## Interpretation

검색 coverage는 높다. 따라서 다음 병목은 검색 누락보다 답변/평가 정합성이다.

다만 `accuracy_mean`은 `expected_keywords`의 단순 문자열 포함 여부로 계산된다. 의미상 맞는 답변도 기대 키워드의 정확한 문자열이 없으면 낮게 나온다.

## Low-Score Cases

| Case | Accuracy | Faithfulness | Not Found | Classification |
| --- | ---: | ---: | --- | --- |
| `tc-01` | 0.0 | 0.0 | true | 문서 근거 부족 가능성이 높음. 해지 근거는 있으나 환불 정책 근거가 약함 |
| `tc-04` | 0.25 | 0.0 | true | 혼합 케이스. 정기 결제 취소 근거는 DB에 있으나 자동 갱신 근거는 약하고 최종 답변은 no-answer |
| `tc-08` | 0.5 | 1.0 | false | 답변은 근거 기반. `중단`/`통보` 대신 `중지`/`통지`/`공지` 표현을 사용해 keyword accuracy가 낮음 |
| `tc-09` | 0.5 | 1.0 | false | 답변은 근거 기반. `금지`/`준수` 같은 평가 키워드가 답변 표현과 정확히 맞지 않음 |

## Evidence Notes

- `tc-01`: Chroma DB에는 서비스 해지와 탈퇴 관련 청크가 있으나 환불 정책을 직접 설명하는 청크는 확인되지 않았다.
- `tc-04`: Chroma DB에 매월 정기 결제와 취소 요청 관련 청크가 있다. 다만 질문의 `자동 갱신`과 `구독` 표현은 문서 표현과 다르고, 최종 답변은 no-answer로 끝났다.
- `tc-08`: 답변은 공지, 통지, 고지 절차를 설명한다. 평가 키워드 `통보`와 표현 불일치가 있다.
- `tc-09`: 답변은 이용자의 주요 금지 행위를 나열한다. 평가 키워드 `금지`, `준수`가 그대로 나오지 않아 점수가 낮다.

## Failure Modes

1. 평가셋 근거 불일치
   - `tc-01`은 현재 인제스천 문서 기준으로 환불 정책을 묻기 어렵다.

2. 복합 질문
   - `tc-04`는 자동 갱신과 해지 방법을 동시에 묻는다.
   - 문서에는 정기 결제 취소와 이용계약 해지가 흩어져 있어 한 답변에 묶기 어렵다.

3. keyword exact-match 한계
   - `고지`, `통지`, `통보`, `공지`처럼 의미상 가까운 표현이 별도 문자열로 평가된다.
   - `금지 행위`를 나열해도 `금지`라는 단어가 없으면 점수가 낮다.

4. no-answer 판정 기준
   - `tc-04`처럼 일부 근거가 있어도 질문 전체를 만족하지 못하면 no-answer로 처리될 수 있다.
   - 부분 답변 정책이 필요하다.

## Recommended First Experiment

첫 구현 실험은 평가셋/accuracy 판정 보정이다.

구체 작업:
- `eval/test_cases.json`에 키워드 동의어 또는 대체 표현을 표현할 수 있는 구조를 추가한다.
- `answer_accuracy()`가 단일 문자열 목록뿐 아니라 OR 그룹을 평가하도록 확장한다.
- `tc-08`, `tc-09`처럼 의미상 맞는 답변이 낮게 평가되는 케이스를 먼저 보정한다.
- `tc-01`, `tc-04`는 no-answer 또는 부분 답변 평가 케이스로 재분류할지 결정한다.

성공 기준:
- 답변이 실제로 나아졌다고 보기 어려운 케이스를 프롬프트로 억지 보정하지 않는다.
- faithfulness 1.0인 케이스의 keyword mismatch가 줄어든다.
- full eval 후 `accuracy_mean`이 개선되더라도, 변경 이유가 평가 기준 정렬임을 리포트에 명확히 남긴다.

다음 구현 후보:
- 평가셋 보정 후에도 no-answer가 남는 `tc-04`에 대해 partial-answer 프롬프트를 실험한다.
