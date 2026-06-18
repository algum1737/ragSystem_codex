# 2026-06-18 TC04 Faithfulness Triage Result

## Summary

`tc-04` faithfulness failure를 systematic-debugging 방식으로 재현하고 분류했다.

결론:

- `tc-04`는 retrieval/source failure가 아니다.
- `answer_accuracy=1.0`, `source_recall_at_k=1.0`, `rag_normalized_source_precision_at_k=1.0`이다.
- 실패 원인은 `확인된 내용`과 `문서에서 확인되지 않는 내용`이 섞인 partial answer 구조가 binary faithfulness judge를 흔드는 것이다.
- positive-only 답변은 안정적으로 faithful이다.
- negative-only 답변은 안정적으로 unfaithful로 판정된다.
- 실제 답변은 positive 근거와 negative no-confirm 문장이 섞여 `YES/NO`가 반복 판정에서 흔들린다.

## Inputs

- Full eval report: `eval/results/eval_20260618_132509.json`
- Single-case server report: `/opt/ragSystem_codex/eval/results/eval_tc04_check_20260618_132648.json`
- Test case: `eval/test_cases.json` `tc-04`
- Faithfulness judge: `eval/pipeline.py`

## Baseline Failure

최신 full eval:

| Metric | Value |
| --- | ---: |
| `answer_accuracy` | 1.0 |
| `faithfulness` | 0.0 |
| `source_recall_at_k` | 1.0 |
| `rag_normalized_source_precision_at_k` | 1.0 |

단일 재실행:

| Metric | Value |
| --- | ---: |
| `answer_accuracy` | 1.0 |
| `faithfulness` | 0.0 |
| `source_recall_at_k` | 1.0 |
| `rag_normalized_source_precision_at_k` | 1.0 |

## Retrieved Context

RAG context에는 다음 근거가 포함됐다.

- 네이버 유료서비스 사용기간은 별도 표시가 없으면 구매일로부터 1년
- 사용기간 경과 후 이용권 소멸 및 보유목록 삭제
- 카카오 정기결제형 서비스의 무료체험기간 만료 전 회원 의사 확인
- 무료체험 만료 후 등록 결제수단으로 정기결제 진행
- 무료체험 시작 전 고지
- 정기결제 후 결제 내용 고지
- 회원의 명시적 동의가 있는 경우 고지 생략 가능
- 결제수단 유효기간 만료 등으로 결제 실패 시 이용 중단 및 지속 시 계약 해지 가능

따라서 source coverage 자체는 충분하다.

## Answer Pattern

실패 답변은 두 종류의 문장을 섞는다.

Positive grounded content:

- 네이버 사용기간과 만료 후 소멸
- 카카오 무료체험 후 정기결제
- 결제수단, 고지, 동의 시 고지 생략
- 결제 실패 시 이용 중단 및 계약 해지

Negative no-confirm content:

- 네이버 자동 갱신 조건의 구체적인 내용은 확인되지 않음
- 카카오 자동 갱신 조건에 대한 다른 내용은 확인되지 않음

이 negative sentence는 질문의 "자동 갱신" 표현과 카카오 문서의 "정기결제" 표현 사이를 모델이 조심스럽게 분리하려다 생긴 partial answer다.

## Judge Variant Test

서버에서 `RAGEvaluator.faithfulness()`를 같은 `tc-04` context로 반복 실행했다.

| Variant | Result |
| --- | --- |
| full eval answer | `[1.0, 0.0, 0.0]` |
| single-case answer | `[0.0, 1.0, 0.0]` |
| positive-only answer | `[1.0, 1.0, 1.0, 1.0, 1.0]` |
| negative-only answer | `[0.0, 0.0, 0.0, 0.0, 0.0]` |

해석:

- 확인된 positive 근거만 쓰면 judge는 안정적으로 `YES`를 낸다.
- 확인되지 않는다는 negative assertion만 쓰면 judge는 안정적으로 `NO`를 낸다.
- 실제 답변처럼 둘을 섞으면 judge 결과가 흔들린다.

## Classification

Primary classification:

- `answer wording`

Secondary classification:

- `faithfulness judge`

근거:

- 검색과 source scope는 정상이다.
- 답변의 positive content는 faithful이다.
- 답변의 negative no-confirm section이 judge instability를 유발한다.
- judge prompt는 "참고 문서에만 근거하는지"를 binary로 묻기 때문에, absence claim이 섞인 partial answer를 안정적으로 평가하지 못한다.

## Decision

이번 triage에서는 code, prompt, eval rule을 변경하지 않는다.

다음 후속 후보는 둘 중 하나다.

1. Standard answer prompt wording 보강
   - 명시적 하위 항목이 아닌 경우 `문서에서 확인되지 않는 내용` 섹션을 남발하지 않게 한다.
   - 확인되는 정기결제/만료/고지/중단 조건을 중심으로 답하게 한다.
2. Faithfulness judge 개선
   - partial answer의 "확인된 내용"과 "확인되지 않는 내용"을 분리 평가한다.
   - absence claim을 포함한 답변은 별도 rule로 다룬다.

권장 우선순위:

- 먼저 `tc-04` answer wording focused fix를 검토한다.

이유:

- positive-only answer가 안정적으로 faithful이다.
- judge 자체를 바꾸면 전체 평가 의미가 넓게 바뀐다.
- prompt wording은 `tc-04` 같은 partial answer 과잉을 줄이는 데 직접적이다.

## Next Work

후속 active plan 후보:

- `2026-06-18-tc04-answer-wording-fix.md`

검증 계약:

- `tc-04` focused smoke
- full eval
- source drift report
- `tc-07`, `tc-15` 보정 유지 확인
- latency trace 확인
