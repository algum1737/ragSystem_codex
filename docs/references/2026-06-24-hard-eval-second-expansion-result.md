# 2026-06-24 Hard Eval Second Expansion Result

## Summary

32개 hard eval green baseline 이후 hard eval을 2차 확장했다.

결론:

- 평가셋은 `32`개에서 `39`개로 확장됐다.
- 신규 케이스는 `tc-33`~`tc-39` 7개다.
- retrieval/source 지표는 확장 후에도 정상이다.
- full eval 결과 `faithfulness_mean=1.0`, `not_found_success_rate=1.0`이다.
- `answer_accuracy` 기준 critical case는 5건이다.
- 실패 5건 모두 `source_recall_at_k=1.0`, `rag_normalized_source_precision_at_k=1.0`이므로 1차 원인은 검색 누락이 아니다.
- 다음 작업은 prompt/retrieval 변경이 아니라 focused failure triage다.

## Changes

파일:

- `eval/test_cases.json`

추가 케이스:

| Case | Focus |
| --- | --- |
| `tc-33` | 위치정보 제3자 제공 시 제공받는 자/일시/목적 즉시 통지 |
| `tc-34` | 8세 이하 아동 등 보호의무자 동의 효력과 권리 |
| `tc-35` | 카카오 운영정책 계정 생성·이용·탈퇴 제한과 제한 단계 |
| `tc-36` | Daum 권리침해 게시물 게시중단/삭제/임시조치 |
| `tc-37` | 네이버 유료서비스 금지행위 계약해제·해지와 환불 산정 |
| `tc-38` | Daum 무료 서비스 변경 시 보상과 사전/사후 안내 |
| `tc-39` | 유료서비스 월 구독료 연간 인상률 no-answer |

## Local Validation

통과:

```bash
.venv/bin/python -m json.tool eval/test_cases.json > /tmp/test_cases_validated.json
.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py
.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json
bash scripts/validate-docs.sh
```

Retrieval-only smoke:

```bash
.venv/bin/python eval/pipeline.py --metric retrieval --model gemma3:12b --top-k 5
```

요약:

| Metric | Value |
| --- | ---: |
| `total_cases` | 39 |
| `rag_normalized_source_precision@k_mean` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `source_coverage@k_mean` | 1.0 |
| `rag_chunk_precision@k_mean` | 0.8256 |

## Full Eval

서버 명령:

```bash
cd /opt/ragSystem_codex
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
CUDA_VISIBLE_DEVICES= \
.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

Reports:

- 서버 report: `/opt/ragSystem_codex/eval/results/eval_20260624_151136.json`
- 로컬 report: `eval/results/eval_20260624_151136.json`
- Source drift report: `docs/references/2026-06-24-hard-eval-second-expansion-source-drift-report.md`

Metrics:

| Metric | Value |
| --- | ---: |
| `total_cases` | 39 |
| `accuracy_mean` | 0.9711 |
| `faithfulness_mean` | 1.0 |
| `not_found_success_rate` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_normalized_source_precision@k_mean` | 1.0 |
| `rag_chunk_precision@k_mean` | 0.8256 |

## Critical Cases

| Case | Accuracy | Faithfulness | Source Recall | RAG Normalized Precision | Initial Classification |
| --- | ---: | ---: | ---: | ---: | --- |
| `tc-07` | 0.75 | 1.0 | 1.0 | 1.0 | existing eval rule / answer wording candidate |
| `tc-28` | 0.80 | 1.0 | 1.0 | 1.0 | existing answer coverage candidate |
| `tc-29` | 0.80 | 1.0 | 1.0 | 1.0 | existing eval rule candidate |
| `tc-34` | 0.6667 | 1.0 | 1.0 | 1.0 | new question wording / answer coverage candidate |
| `tc-37` | 0.8571 | 1.0 | 1.0 | 1.0 | new eval rule candidate |

## Initial Failure Notes

`tc-07`:

- 답변은 위치기반서비스 면책 사유를 근거 기반으로 나열했다.
- deterministic keyword 중 `보증` 계열 또는 책임/손해 표현 범위가 맞지 않았을 가능성이 있다.

`tc-28`:

- 답변은 비정상 로그인 보호조치를 설명했지만 장기 미사용 계정의 `3개월`, `2년`, `휴면` 처리를 확인되지 않는다고 답했다.
- 관련 source recall은 `1.0`이므로 answer coverage 또는 context prioritization 후보로 본다.

`tc-29`:

- 답변은 결제일이 없는 달을 `정기결제일이 없는 달`로 표현했다.
- expected keyword OR group이 `없는 달` 표현을 놓쳤을 가능성이 있다.

`tc-34`:

- 답변은 보호의무자 동의 효력과 권리를 설명했다.
- expected keyword에는 `생명 또는 신체보호` 목적이 포함되어 있으나 질문은 효력과 권리를 중심으로 묻는다.
- question wording 또는 expected range 조정 후보로 본다.

`tc-37`:

- 답변은 금지행위, 계약해제·해지, 이용 제한, 환불수수료, 3영업일, 수납확인을 모두 설명했다.
- deterministic keyword가 `서비스 이용을 제한` 표현을 `이용제한` group으로 인정하지 않았을 가능성이 있다.

## Decision

- 신규 7개 hard eval 케이스는 유지한다.
- 검색 지표가 정상이므로 retrieval/rerank 변경은 하지 않는다.
- 즉시 prompt나 eval rule을 고치지 않고 focused triage를 먼저 진행한다.
- 다음 active plan은 `docs/exec-plans/active/2026-06-24-hard-eval-second-expansion-failure-triage.md`다.
