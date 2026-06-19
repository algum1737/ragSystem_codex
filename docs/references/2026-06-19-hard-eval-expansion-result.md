# 2026-06-19 Hard Eval Expansion Result

## Summary

모델 품질 개선을 위한 첫 단계로 hard eval 케이스를 9개 추가했다.

결론:

- 평가셋은 `23`개에서 `32`개로 확장됐다.
- retrieval/source 지표는 확장 후에도 정상이다.
- 최종 재채점 기준으로 실제 남은 실패는 `tc-30` 1건이다.
- 실패 원인은 retrieval/rerank가 아니라 answer generation의 multi-source coverage 부족이다.
- 따라서 다음 튜닝 후보는 retrieval/rerank 변경이 아니라 `tc-30` answer coverage focused fix다.

## Changes

파일:

- `eval/test_cases.json`

추가 케이스:

| Case | Focus |
| --- | --- |
| `tc-24` | 위치정보 이용·제공사실 확인자료 보유기간 |
| `tc-25` | 위치정보 동의 철회와 확인자료 파기 |
| `tc-26` | 만 14세 미만 아동 위치정보와 법정대리인 권리 |
| `tc-27` | 게시중단 이의신청 처리 |
| `tc-28` | 비정상 로그인/장기 미사용 계정 보호조치 |
| `tc-29` | 카카오 정기결제일 부재와 무료체험 재가입 |
| `tc-30` | 유료서비스 동일 결제수단 환불 불가 처리 |
| `tc-31` | 미성년자 유료/결제서비스 제한 |
| `tc-32` | Daum 36개월 미로그인 계정 탈퇴 처리 |

`tc-29`는 첫 full eval 뒤 answer가 유효하지만 `날짜가 없을 경우` 표현을 deterministic rule이 놓친 것으로 확인되어 OR group에 `날짜가 없`을 추가했다.

## Local Validation

통과:

```bash
.venv/bin/python -m json.tool eval/test_cases.json > /tmp/test_cases_validated.json
.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py scripts/source_drift_report.py
bash scripts/validate-docs.sh
```

Retrieval-only smoke:

```bash
.venv/bin/python eval/pipeline.py --metric retrieval --model gemma3:12b --top-k 5
```

요약:

| Metric | Value |
| --- | ---: |
| `total_cases` | 32 |
| `rag_normalized_source_precision@k_mean` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_chunk_precision@k_mean` | 0.85 |

## Full Eval

서버 명령:

```bash
cd /opt/ragSystem_codex
RAG_TRACE_ENABLED=true \
RAG_TRACE_PATH=/opt/ragSystem_codex/logs/rag_traces.jsonl \
CUDA_VISIBLE_DEVICES="" \
.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

Reports:

- 서버 original report: `/opt/ragSystem_codex/eval/results/eval_20260619_105835.json`
- 로컬 original report: `eval/results/eval_20260619_105835.json`
- 로컬 recalibrated report: `eval/results/eval_20260619_105835_tc29_recalibrated.json`
- Source drift report: `docs/references/2026-06-19-hard-eval-expansion-source-drift-report.md`

Original metrics:

| Metric | Value |
| --- | ---: |
| `accuracy_mean` | 0.9813 |
| `faithfulness_mean` | 1.0 |
| `not_found_success_rate` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_normalized_source_precision@k_mean` | 1.0 |

Recalibrated metrics:

| Metric | Value |
| --- | ---: |
| `accuracy_mean` | 0.9875 |
| `faithfulness_mean` | 1.0 |
| `not_found_success_rate` | 1.0 |
| `source_recall@k_mean` | 1.0 |
| `rag_normalized_source_precision@k_mean` | 1.0 |

## Failure Classification

### `tc-29`

Initial result:

- `answer_accuracy=0.8`
- `faithfulness=1.0`
- `source_recall_at_k=1.0`

Answer included:

- 정기결제일에 해당하는 날짜가 없는 달은 말일에 결제
- 무료체험기간 이용 후 탈퇴/재가입 시 무료체험기간이 제공되지 않을 수 있음

Classification:

- `eval rule`

Action:

- `expected_keywords`에 `날짜가 없`을 좁게 추가했다.
- 저장 답변 재채점 후 `tc-29`는 통과했다.

### `tc-30`

Recalibrated result:

- `answer_accuracy=0.6`
- `faithfulness=1.0`
- `source_recall_at_k=1.0`
- `rag_normalized_source_precision_at_k=1.0`

Answer pattern:

- 카카오의 동일 방법 환불 불가 처리만 설명했다.
- 계좌 이체, 환불적립금, 환불적립금 운영정책은 포함했다.
- 네이버의 `3영업일`, `수납확인`, 동일 방법 환불 불가 시 사전 고지 근거는 빠졌다.

Classification:

- Primary: `answer generation`
- Secondary: `multi-source coverage`

Not classified as:

- `retrieval`: relevant source recall is `1.0`.
- `faithfulness judge`: answer is grounded and `faithfulness=1.0`.
- `eval rule`: expected keywords represent the omitted 네이버-side condition.

## Decision

- Hard eval 확장은 유지한다.
- 현재 단계에서 retrieval/rerank 튜닝은 보류한다.
- 다음 품질 튜닝은 `tc-30`처럼 여러 관련 문서가 검색된 질문에서 답변이 한 출처만 설명하는 문제를 좁게 다룬다.

## Next Work

1. `tc-30` answer coverage focused plan을 작성한다.
2. 같은 질문의 context와 answer를 비교해 빠진 근거를 정리한다.
3. prompt 보정이 필요한지, eval question을 더 명시적으로 바꿔야 하는지 분류한다.
4. 수정 후보는 focused smoke 후 full eval로만 채택한다.
