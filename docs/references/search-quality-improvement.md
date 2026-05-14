# Search Quality Improvement

분석 기준:

- 이전 기준선: `eval/results/eval_20260513_164755.json`
- 개선 후 리포트: `eval/results/eval_20260514_113849.json`

## Result

- `vector_precision@k_mean`: `0.48 -> 0.48`
- `rag_precision@k_mean`: `0.54 -> 0.60`
- `source_coverage@k_mean`: `0.925 -> 1.0`
- `accuracy_mean`: `0.675 -> 0.70`
- `faithfulness_mean`: `0.8 -> 0.9`
- `not_found_rate`: `0.1 -> 0.1`

`precision@k_mean`은 vector-only 호환 지표이므로 그대로 `0.48`이다. 이번 개선의 대상은 실제 RAG 검색 경로의 최종 source 지표인 `rag_precision@k_mean`이다.

## Change

- `RAGEngine.query()` 내부 검색 단계를 `RAGEngine.retrieve()`로 분리했다.
- eval retrieval 지표가 LLM 생성 호출 없이도 실제 RAG 검색 경로를 측정하도록 바꿨다.
- Cross-Encoder rerank 이후 최종 청크 선택에서 source 다양성을 보존한다.
- source 다양성은 전체 후보가 아니라 상위 후보 창 안에서만 적용한다.
  - `tc-04`, `tc-07`처럼 상위 후보 안에 누락 source가 있는 케이스를 보강한다.
  - `tc-10`처럼 낮은 순위의 off-topic source가 끼어드는 부작용을 줄인다.
- eval full 경로에서 `doc_type` 필터를 `RAGEngine.query()`에 전달하도록 보정했다.

## Case Notes

- `tc-04`: `rag_precision_at_k 0.4 -> 0.8`, `source_coverage_at_k 0.5 -> 1.0`
- `tc-07`: `rag_precision_at_k 0.6 -> 0.8`, `source_coverage_at_k 0.75 -> 1.0`
- `tc-10`: 관련 일반 약관 source만 유지하면서 `source_coverage_at_k=1.0`을 유지했다.

## Validation Notes

Ollama 상태를 권한 상승 경로에서 재확인했고 `gemma3:12b`가 사용 가능함을 확인했다. full eval을 재실행해 검색 지표와 생성 지표를 모두 산출했다.
