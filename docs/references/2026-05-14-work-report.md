# 2026-05-14 Work Report

## Summary

2026-05-14 작업은 운영 하네스 보강과 검색 품질 1차 개선으로 진행했다.

- GitHub Actions 최소 CI를 추가하고 PR checks가 표시되도록 했다.
- RAG 검색 경로를 LLM 생성과 분리해 검색 지표를 안정적으로 측정할 수 있게 했다.
- rerank 이후 최종 청크 선택에서 source 다양성을 보존해 실제 RAG 검색 지표를 개선했다.
- Ollama 상태를 재확인하고 full eval을 재실행해 검색/생성 지표를 모두 갱신했다.
- 완료된 계획은 completed로 이동했고, 다음 품질 반복 계획을 active로 생성했다.

## Completed Work

### GitHub Actions CI

- PR: #15 `GitHub Actions 최소 CI 추가`
- 상태: merged
- 추가 파일: `.github/workflows/ci.yml`
- CI 범위:
  - `bash scripts/validate-docs.sh`
  - `python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- 결과:
  - PR checks 생성 확인
  - `Static checks` 통과
  - 계획 문서: `docs/exec-plans/completed/2026-05-13-github-actions-ci.md`

### Search Quality Improvement

- PR: #16 `RAG 검색 source coverage 개선`
- 상태: merged
- 주요 변경:
  - `RAGEngine.retrieve()` 추가
  - `RAGEngine.query()` 내부 검색 단계를 `retrieve()`로 분리
  - eval retrieval 지표가 LLM 생성 호출 없이 실제 RAG 검색 경로를 측정하도록 변경
  - Cross-Encoder rerank 이후 상위 후보 창 안에서 source 다양성 선택 적용
  - eval full 경로에서 `doc_type` 필터를 `RAGEngine.query()`에 전달
- 결과:
  - `rag_precision@k_mean`: `0.54 -> 0.60`
  - `source_coverage@k_mean`: `0.925 -> 1.0`
  - `accuracy_mean`: `0.675 -> 0.70`
  - `faithfulness_mean`: `0.8 -> 0.9`
  - 계획 문서: `docs/exec-plans/completed/2026-05-14-search-quality-improvement.md`

## Updated Files

- `.github/workflows/ci.yml`
- `retriever/engine.py`
- `eval/pipeline.py`
- `eval/results/eval_20260514_113849.json`
- `docs/references/search-quality-improvement.md`
- `docs/exec-plans/completed/2026-05-13-github-actions-ci.md`
- `docs/exec-plans/completed/2026-05-14-search-quality-improvement.md`
- `docs/exec-plans/active/2026-05-14-next-quality-iteration.md`
- `README.md`
- `docs/index.md`
- `docs/PLANS.md`
- `docs/HANDOFF.md`

## Validation

- 통과: `bash scripts/validate-docs.sh`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- 통과: `.venv/bin/python eval/pipeline.py --metric retrieval`
- 통과: `.venv/bin/python eval/pipeline.py --all`
- 통과: PR #15 GitHub Actions `Static checks`
- 통과: PR #16 GitHub Actions `Static checks`

## Latest Metrics

기준 리포트: `eval/results/eval_20260514_113849.json`

| Metric | Value |
| --- | ---: |
| `vector_precision@k_mean` | `0.48` |
| `rag_precision@k_mean` | `0.60` |
| `source_coverage@k_mean` | `1.0` |
| `accuracy_mean` | `0.70` |
| `faithfulness_mean` | `0.90` |
| `not_found_rate` | `0.10` |

## Remaining Work

- 최신 full eval 리포트의 낮은 점수 케이스를 재분류한다.
- 다음 개선 후보를 하나로 좁힌다.
- 후보군은 청킹, hybrid search 가중치, reranking 적용 범위, 평가셋 확장 순서로 검토한다.
