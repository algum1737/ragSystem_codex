# 2026-05-14 Next Quality Iteration Analysis

## Basis

- Active plan: `docs/exec-plans/active/2026-05-14-next-quality-iteration.md`
- Latest report: `eval/results/eval_20260514_113849.json`
- Current summary:
  - `vector_precision@k_mean=0.48`
  - `rag_precision@k_mean=0.60`
  - `source_coverage@k_mean=1.0`
  - `accuracy_mean=0.70`
  - `faithfulness_mean=0.90`
  - `not_found_rate=0.10`

## Interpretation

검색 경로의 1차 목표는 달성했다. `source_coverage@k_mean=1.0`이므로 현재 병목은 관련 source를 못 찾는 문제가 아니라, 질문/평가 키워드/답변 형식의 정합성 문제에 가깝다.

다음 실험은 청킹이나 검색 가중치보다 평가셋 정합성 보정이 우선이다. 검색 구조를 더 조정하면 이미 충분한 coverage가 있는 케이스에서 off-topic source가 늘어날 위험이 있다.

## Low-Score Case Review

| Case | Current Scores | Classification | Notes |
| --- | --- | --- | --- |
| `tc-01` | `accuracy=0.0`, `faithfulness=0.0`, `not_found=true` | 문서 근거 부족 / 평가 질문 불일치 | 검색 결과에는 해지 근거가 있으나 환불 정책, 환불 기간 근거가 부족하다. 현재 평가 키워드 `환불`, `정책`, `기간`은 문서 근거와 맞지 않는다. |
| `tc-03` | `accuracy=0.5`, `faithfulness=1.0` | 평가 키워드 표현 불일치 | 답변은 이용 제한/정지 조건을 근거 기반으로 설명한다. 다만 `이용제한`, `금지`, `위반` 같은 기대 키워드와 실제 답변 표현이 부분적으로 다르다. |
| `tc-04` | `accuracy=0.25`, `faithfulness=1.0` | 복합 질문 / 문서 근거 일부 부족 | 해지 방법은 확인되지만 자동 갱신 조건은 직접 근거가 약하다. 현재 질문은 자동 갱신과 해지를 동시에 묻고 있어 부분 답변 평가 구조가 더 적합하다. |
| `tc-09` | `accuracy=0.75`, `faithfulness=1.0` | 경미한 평가 키워드 보정 후보 | 답변은 이용자의 금지 행위와 의무를 잘 설명한다. 남은 감점은 `준수` 등 키워드 표현 차이일 가능성이 높다. |

## Recommended Next Experiment

다음 구현 후보는 **평가셋 정합성 보정**이다.

구체 작업:

- `tc-01`을 no-answer 또는 partial-answer 평가 케이스로 재분류한다.
  - 현재 문서에는 해지 근거는 있으나 환불 정책 근거가 부족하다.
  - 질문을 "해지 시 데이터 및 게시물 처리는 어떻게 되는가?"처럼 문서 근거에 맞게 바꾸는 방안도 가능하다.
- `tc-03` expected keywords를 OR group으로 보정한다.
  - 예: `["이용제한", "이용 제한", "서비스 이용 제한"]`
  - 예: `["정지", "중지", "영구 정지"]`
  - 예: `["금지", "법령 위반", "권리침해", "운영정책"]`
- `tc-04`를 복합 질문 평가로 분리하거나, 자동 갱신 근거 부족을 명시적으로 인정하는 partial-answer 기준을 추가한다.
  - 자동 갱신 관련 키워드는 현재 문서 근거 기준에서 낮은 우선순위다.
  - 해지/동의 철회/서비스 종료 표현을 OR group으로 반영한다.
- `tc-09`는 남은 감점만 보정한다.
  - 답변 품질은 충분하므로 대규모 검색 튜닝 대상이 아니다.

## Expected Impact

보수적 예상:

- `accuracy_mean`: `0.70 -> 0.775~0.825`
- `faithfulness_mean`: `0.90` 유지
- `not_found_rate`: `0.10` 유지 또는 no-answer 평가 기준 정렬
- 검색 지표: 유지

## Risks

- 평가셋을 과도하게 보정하면 실제 답변 품질 개선이 아니라 점수만 올라갈 수 있다.
- 따라서 보정 이유를 케이스별로 문서화하고, faithfulness가 낮은 케이스는 프롬프트나 검색 튜닝으로 억지 보정하지 않는다.

## Decision

다음 active implementation plan 후보:

- `Eval Case Alignment Plan`
- 목표: 최신 full eval의 낮은 accuracy 케이스를 문서 근거 기준에 맞게 재분류하고 expected keyword OR group을 보정한다.
