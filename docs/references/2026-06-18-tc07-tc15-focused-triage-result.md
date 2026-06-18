# 2026-06-18 TC07 TC15 Focused Triage Result

## Summary

`tc-07`, `tc-15`의 최신 `accuracy=0.75`는 retrieval/source 문제나 hallucination 문제가 아니다.

결론:

- 두 케이스 모두 `source_recall_at_k=1.0`, `rag_normalized_source_precision_at_k=1.0`, `faithfulness=1.0`이다.
- 최신 답변은 질문에 필요한 핵심 근거를 포함한다.
- 감점 원인은 deterministic `answer_accuracy`의 keyword group이 의미상 동등한 표현을 충분히 허용하지 않는 것이다.
- 다음 후속 후보는 전역 prompt 변경이 아니라 `eval/test_cases.json`의 `tc-07`, `tc-15` expected keyword OR group을 좁게 보정하는 것이다.

## Inputs

- Eval report: `eval/results/eval_20260618_113500.json`
- Source drift report: `docs/references/2026-06-18-gemma3-quality-baseline-source-drift-report.md`
- Test cases: `eval/test_cases.json`
- Accuracy rule: `eval/pipeline.py`

## Accuracy Rule

`answer_accuracy`는 top-level expected group 수 대비 matched group 수를 계산한다.

- 문자열 group: 해당 문자열이 답변에 포함되면 match
- list group: list 안의 표현 중 하나라도 답변에 포함되면 match
- 최종 점수: `matched / len(expected_keywords)`

따라서 4개 group 중 1개가 누락되면 `0.75`가 된다.

## `tc-07`

질문:

```text
위치기반서비스 약관에서 서비스 제공자의 면책 조항은 무엇인가?
```

최신 결과:

| Metric | Value |
| --- | ---: |
| `answer_accuracy` | 0.75 |
| `faithfulness` | 1.0 |
| `source_recall_at_k` | 1.0 |
| `rag_normalized_source_precision_at_k` | 1.0 |

Keyword match:

| Expected group | Latest answer match | Result |
| --- | --- | --- |
| `면책` | 없음 | MISS |
| `책임`, `귀책사유`, `고의·과실`, `불가항력` | 모두 포함 | PASS |
| `손해`, `장애`, `방해`, `신뢰도`, `정확성` | 모두 포함 | PASS |
| `보증` | 포함 | PASS |

판단:

- 답변은 `손해에 대해 책임을 부담하지 않습니다`, `책임을 부담하지 아니합니다`처럼 면책의 실질 내용을 설명한다.
- `천재지변`, `불가항력`, `제3자의 고의적인 서비스 방해`, `이용자 귀책사유`, `회사 고의·과실 없는 사유`, `신뢰도/정확성 보증 부재`를 포함한다.
- 감점은 `면책`이라는 표지어 직접 매칭 실패다.
- 이는 답변 품질 결함보다 eval rule의 동의 표현 허용 부족에 가깝다.

후속 후보:

- `tc-07` 첫 group을 `["면책", "책임을 부담하지", "책임을 지지", "책임이 없"]`처럼 좁게 확장한다.
- 단순 `책임`은 이미 다른 group에 있으므로 첫 group에는 넣지 않는다.

## `tc-15`

질문:

```text
일반 서비스 약관에서 회사가 서비스를 변경하거나 종료할 때 사전 고지 없이 가능한 예외는 무엇인가?
```

최신 결과:

| Metric | Value |
| --- | ---: |
| `answer_accuracy` | 0.75 |
| `faithfulness` | 1.0 |
| `source_recall_at_k` | 1.0 |
| `rag_normalized_source_precision_at_k` | 1.0 |

Keyword match:

| Expected group | Latest answer match | Result |
| --- | --- | --- |
| `사전`, `미리` | `사전` | PASS |
| `공지`, `통지`, `고지` | `공지`, `통지` | PASS |
| `예외`, `불가능`, `부득이`, `긴급` | 없음 | MISS |
| `변경`, `중단`, `종료` | 모두 포함 | PASS |

판단:

- 답변은 `사전 통지 내지 공지 없이 서비스 중단이 가능합니다`와 `사전 통지 내지 공지를 할 수 없습니다`를 포함한다.
- 예외 조건으로 `정기 또는 임시 점검`, `정전`, `설비 장애`, `이용량 폭주`, `정부 명령/규제`, `정책 변경`, `천재지변`, `국가비상사태`, `예측할 수 없거나 통제할 수 없는 사유`를 설명한다.
- 감점은 예외 의미를 직접 설명했지만 `예외`, `불가능`, `부득이`, `긴급` 중 하나를 그대로 쓰지 않은 데서 발생했다.
- 전역 prompt를 바꿔 모든 답변에 질문 표지어를 반복하게 하면 불필요한 형식 고정이나 다른 케이스 회귀 가능성이 있다.

후속 후보:

- `tc-15` 세 번째 group을 `["예외", "불가능", "부득이", "긴급", "없이", "예측할 수 없", "통제할 수 없"]`처럼 좁게 확장한다.
- `경우`처럼 너무 일반적인 표현은 false positive 위험이 커서 추가하지 않는다.

## Decision

다음 작업은 `eval/test_cases.json`의 expected keyword OR group을 좁게 보정하는 active plan이 적합하다.

추천 범위:

- `tc-07`: 첫 group에 면책 의미의 책임 부정 표현 추가
- `tc-15`: 예외 group에 사전 고지 예외를 의미하는 좁은 표현 추가
- 변경 후 focused score 확인
- full eval 재실행
- source drift report 재생성

## Rejected Options

### Prompt wording 보강

기각한다.

이유:

- 두 답변은 이미 faithful하고 source coverage도 완전하다.
- 전역 prompt에 "질문 핵심 용어를 반드시 반복"을 추가하면 자연스러운 답변보다 평가셋 표지어에 맞춘 출력으로 기울 수 있다.
- 과거 prompt 후보 실험에서 일부 케이스 회귀가 있었으므로, 실제 답변 결함이 아닌 경우 prompt 변경은 우선순위가 낮다.

### Retrieval 또는 model 변경

기각한다.

이유:

- 두 케이스 모두 source recall과 RAG normalized precision이 `1.0`이다.
- faithfulness도 `1.0`이므로 hallucination 또는 source grounding 문제가 아니다.

## Next Work

후속 active plan 후보:

- `2026-06-18-tc07-tc15-eval-rule-calibration.md`

예상 검증:

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py`
- 서버 또는 로컬 full eval: `.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5`
- source drift report 재생성
- 기대 결과:
  - `tc-07=1.0`
  - `tc-15=1.0`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=1.0`
  - `source_recall@k_mean=1.0`
