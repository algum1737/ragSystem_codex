# 2026-06-09 Refined Concise Bullet Prompt Result

## Summary

직전 concise-answer prompt 실험에서 확인된 `concise_bullet` 후보를 다듬어, 불필요한 no-answer 문장과 출처 번호 표기를 줄인 refined 후보를 서버에서 smoke 비교했다.

최종 결론:

- 최종 후보는 `refined_concise_bullet` v4다.
- 평균 total latency는 약 5.1초, 평균 LLM latency는 약 5.0초였다.
- 같은 날 전체 smoke의 baseline 평균 total 11.0초 대비 약 53.5% 빠르다.
- 기존 `concise_bullet`보다 불필요한 "문서에서 확인되지 않습니다" 문장이 줄었다.
- `concise_summary`와 속도는 비슷하지만, bullet 구조라 운영 답변의 감사와 출처 확인이 더 쉽다.
- 그러나 운영 기본 프롬프트 반영 후 full eval에서 `accuracy_mean=0.8804`, `not_found_success_rate=0.0` 회귀가 발생했다.
- 운영 기본 프롬프트 채택은 보류하고 서버/로컬 기본 프롬프트는 기존 버전으로 원복했다.

## Environment

- Server: Ubuntu server `10.10.220.5`
- Model: `gemma3:12b`
- Retrieval: `top_k=5`
- Script: `scripts/concise_prompt_experiment.py`
- Full comparison trace: `/opt/ragSystem_codex/logs/refined_concise_prompt_experiment_v3_20260609.jsonl`
- Final refined-only trace: `/opt/ragSystem_codex/logs/refined_concise_prompt_experiment_v4_20260609.jsonl`
- Full eval trace after temporary apply: `/opt/ragSystem_codex/logs/refined_concise_prompt_eval_20260609.jsonl`
- Full eval report after temporary apply: `/opt/ragSystem_codex/eval/results/eval_20260609_095553.json`

## Final Candidate

`refined_concise_bullet` v4의 핵심 규칙:

- 첫 줄부터 질문에 직접 답하는 3~4개 bullet 작성
- 각 bullet은 1문장
- 같은 의미의 조건이나 서비스별 유사 처리는 하나로 병합
- 질문과 직접 관련 없는 비용, 광고, 일반 안내, 배경 설명 제외
- "문서에서 확인되지 않습니다", "확인되지 않은 항목" 같은 미확인 문장 금지
- 마지막 줄에는 실제 `출처:` 뒤 문서명을 최대 3개까지 작성

## Baseline Comparison

동일 날짜 전체 smoke의 baseline과 refined-only 최종 smoke를 비교했다.

| prompt | avg total ms | avg retrieval ms | avg LLM ms | avg answer length |
|---|---:|---:|---:|---:|
| baseline | 11003.15 | 102.36 | 10900.74 | 908.7 |
| concise_bullet | 7030.42 | 99.87 | 6930.50 | 444.3 |
| concise_summary | 5013.39 | 104.45 | 4908.90 | 296.7 |
| refined_concise_bullet v4 | 5116.24 | 107.28 | 5008.91 | 298.0 |

## Refined v4 Detail

| case | total ms | retrieval ms | LLM ms | answer length |
|---|---:|---:|---:|---:|
| long_general | 6149.63 | 112.47 | 6037.10 | 390 |
| location_purpose | 5239.88 | 102.56 | 5137.27 | 286 |
| operation_limit | 3959.21 | 106.80 | 3852.36 | 218 |

## Quality Notes

- `long_general`: 4 bullet로 데이터 삭제, 스크랩/댓글 잔존, 서비스 내 잔존, 개별 약관 차이를 요약했다.
- `location_purpose`: 3 bullet로 위치기반서비스 제공, 콘텐츠 보관기간, 목적 달성 후 파기를 요약했고 불필요한 미확인 문장이 없다.
- `operation_limit`: 3 bullet로 법령/약관/운영정책 위반, 비정상 로그인/패턴, 이용계약 유지 어려움에 따른 해지를 요약했다.
- 일부 근거 문서명은 조합형으로 짧아질 수 있으므로, 운영 반영 후 API smoke에서 source 표기를 다시 확인해야 한다.

## Full Eval After Temporary Apply

v4 후보를 `retriever/engine.py` 기본 프롬프트에 임시 반영하고 서버 API를 재시작한 뒤 full eval을 실행했다.

결과:

| metric | value |
|---|---:|
| total_cases | 23 |
| rag_normalized_source_precision@k_mean | 1.0 |
| source_recall@k_mean | 1.0 |
| accuracy_mean | 0.8804 |
| faithfulness_mean | 1.0 |
| not_found_success_rate | 0.0 |

판단:

- 검색 지표와 faithfulness는 유지됐지만, answer accuracy와 no-answer 계열 케이스가 회귀했다.
- v4는 smoke 질의에서는 빠르고 간결하지만, 전체 평가셋의 keyword/no-answer 계약을 만족하지 못한다.
- 운영 기본값으로 채택하지 않는다.

## Decision

`refined_concise_bullet` v4는 운영 기본 프롬프트로 채택하지 않는다.

다음 후보 방향:

1. 기본 프롬프트 전체를 바꾸지 말고, API/CLI에 `concise=true` 같은 선택형 모드를 추가하는 방향을 검토한다.
2. no-answer 평가 케이스는 기존 기본 프롬프트를 유지하고, 일반 답변 케이스에만 concise prompt를 적용할 수 있는 라우팅을 검토한다.
3. 운영 기본값 변경 전 full eval을 필수 통과 기준으로 둔다.

## Validation Result

- 통과: `.venv/bin/python -m py_compile scripts/concise_prompt_experiment.py`
- 통과: 서버 smoke 실행
- 통과: v3 full comparison trace 수집
- 통과: v4 refined-only trace 수집
- 통과: 운영 기본 프롬프트 임시 반영 후 API smoke
- 실패: 운영 기본 프롬프트 임시 반영 후 full eval
  - `accuracy_mean=0.8804`
  - `not_found_success_rate=0.0`
- 통과: full eval 실패 후 로컬/서버 기본 프롬프트 원복
