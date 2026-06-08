# 2026-06-08 Concise Answer Prompt Experiment Result

## Summary

`gemma3:12b + top_k=5` 운영 조합에서 답변 길이를 줄이는 프롬프트 후보 2종을 서버에서 비교했다.

결론:

- 검색 구간은 warmed 상태에서 약 100ms 수준으로 거의 동일했다.
- latency 차이는 사실상 LLM 생성 구간에서 발생했다.
- `concise_summary`는 평균 total latency를 약 56.2% 줄였지만, 일부 케이스에서 관련성이 낮은 문장 또는 불필요한 "문서에서 확인되지 않습니다" 문장이 섞였다.
- `concise_bullet`은 평균 total latency를 약 45.9% 줄였고, 답변 구조가 더 통제 가능했다.
- 운영 반영 후보는 `concise_bullet` 계열이지만, forced no-answer bullet 규칙은 제거하거나 완화한 뒤 적용해야 한다.

## Environment

- Server: Ubuntu server `10.10.220.5`
- Model: `gemma3:12b`
- Retrieval: `top_k=5`
- Script: `scripts/concise_prompt_experiment.py`
- Final trace: `/opt/ragSystem_codex/logs/concise_prompt_experiment_final_20260608.jsonl`

## Prompt Candidates

### baseline

현재 `retriever/engine.py`의 기본 RAG 프롬프트.

### concise_bullet

- 질문에 직접 답하는 핵심만 3-5개 bullet로 작성
- 각 bullet은 1문장
- 마지막 줄에 근거 문서명 출력
- 긴 배경 설명, 반복, 원문 장문 인용 금지

### concise_summary

- `요약`과 `근거` 두 부분만 작성
- 요약은 최대 4문장
- 근거는 출처 문서명만 나열

## Final Warmed Benchmark

측정 전 warm-up query를 1회 실행해 embedding/LLM 초기화 비용을 제외했다.

| case | prompt | total ms | retrieval ms | LLM ms | answer length |
|---|---:|---:|---:|---:|---:|
| long_general | baseline | 13821.60 | 117.13 | 13704.41 | 1250 |
| long_general | concise_bullet | 7690.55 | 113.23 | 7577.28 | 482 |
| long_general | concise_summary | 6728.85 | 105.36 | 6623.44 | 399 |
| location_purpose | baseline | 12318.26 | 109.06 | 12209.15 | 747 |
| location_purpose | concise_bullet | 5044.76 | 106.54 | 4938.18 | 331 |
| location_purpose | concise_summary | 4021.97 | 107.57 | 3914.34 | 253 |
| operation_limit | baseline | 7534.03 | 105.52 | 7428.47 | 605 |
| operation_limit | concise_bullet | 5476.35 | 96.82 | 5379.48 | 354 |
| operation_limit | concise_summary | 3995.19 | 99.91 | 3895.24 | 255 |

## Average

| prompt | avg total ms | avg retrieval ms | avg LLM ms | avg answer length | total delta |
|---|---:|---:|---:|---:|---:|
| baseline | 11224.63 | 110.57 | 11114.01 | 867.3 | baseline |
| concise_bullet | 6070.55 | 105.53 | 5964.98 | 389.0 | -45.9% |
| concise_summary | 4915.34 | 104.28 | 4811.01 | 302.3 | -56.2% |

## Quality Notes

- `concise_summary` is fastest, but it showed higher answer-risk in smoke review:
  - `long_general`: unrelated cost/ad phrase appeared in the summary.
  - `location_purpose`: "문서에서 확인되지 않는 목적도 존재할 수 있습니다" appears despite the question being answerable from retrieved docs.
  - `operation_limit`: trailing "문서에서 확인되지 않습니다" appears without a clear missing sub-question.
- `concise_bullet` is slower than `concise_summary`, but easier to audit and closer to the current source-grounded answer style.
- The forced rule "문서에서 확인되지 않는 내용은 별도 bullet로 작성" caused unnecessary no-answer text. It should be replaced with "질문에 하위 항목이 있고 일부만 확인되지 않을 때만 미확인 항목을 명시한다."

## Decision

Do not apply either tested prompt exactly as-is.

Recommended next implementation:

1. Start from `concise_bullet`.
2. Keep 3-5 bullet structure and one-sentence bullets.
3. Remove forced no-answer bullet.
4. Require source document names in the final `근거:` line.
5. Run a focused smoke test, then full eval if smoke does not show answer drift.

## Validation Result

- 통과: `.venv/bin/python -m py_compile scripts/concise_prompt_experiment.py retriever/engine.py retriever/llm.py query.py api/main.py app.py`
- 통과: `bash scripts/validate-docs.sh`
- 통과: 서버 final trace 수집 및 구간별 latency 집계
- 미실행: 운영 프롬프트 반영 및 배포. 이번 계획의 Out Of Scope다.
- 미실행: full eval. 후보를 그대로 채택하지 않았으므로 다음 적용 계획에서 실행한다.
