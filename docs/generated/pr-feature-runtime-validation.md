# PR Draft: feature/runtime-validation

## Title

`feat: complete runtime validation and offline setup`

## Body

### Summary

이 PR은 `ragSystem_codex`의 런타임 복구와 오프라인 실행 준비를 마무리한다.

- `ragSystem` 이식 이후 FastAPI/Streamlit/eval 경로를 실제 실행 기준으로 검증했다.
- 오프라인 환경에서도 FastAPI startup과 `/health`가 가능하도록 임베딩 모델 로딩을 lazy initialization으로 변경했다.
- Chroma reset 이후 stale collection handle 때문에 `/stats`가 깨지던 문제를 수정했다.
- 임베딩 모델 캐시 준비 절차를 문서화하고 실제 `multilingual-e5-large` 캐시를 준비했다.
- retrieval eval과 full eval을 실행해 현재 품질 기준선을 다시 확인했다.

### Changes

- 코드
  - `ingestion/embedder.py`
    - `SentenceTransformer` 로드를 요청 시점으로 지연
    - 오프라인 캐시 우선 로드 경로 추가
  - `ingestion/vector_store.py`
    - stale collection handle 감지 시 collection 재획득

- 문서
  - `docs/exec-plans/active/2026-05-12-runtime-validation.md`
  - `docs/HANDOFF.md`
  - `docs/index.md`
  - `docs/PLANS.md`
  - `docs/서버_기동_가이드.md`
  - `docs/references/embedding-model-cache.md`
  - `docs/references/README.md`

- 결과물
  - `eval/results/eval_20260512_175957.json`
  - `eval/results/eval_20260512_182012.json`
  - `eval/results/eval_20260512_182410.json`

### Validation

- 문서 검증
  - `bash scripts/validate-docs.sh`

- 런타임 검증
  - FastAPI startup 성공
  - `GET /health` -> `200 OK`
  - `GET /stats` -> `{"collection_name":"ragSystem","count":89}`
  - Streamlit startup 성공
  - `HEAD http://127.0.0.1:8501` -> `200 OK`

- 모델/데이터 검증
  - `multilingual-e5-large` 로컬 캐시 준비 완료
  - 오프라인 강제 모드에서 embedding dim `1024` 확인

- 평가 결과
  - retrieval eval: `precision@k_mean = 0.48`
  - full eval: `precision@k_mean = 0.48`
  - full eval: `accuracy_mean = 0.575`
  - full eval: `faithfulness_mean = 0.7`

### Remaining Work

- Cross-Encoder 모델 캐시를 준비하면 reranking도 완전 오프라인으로 맞출 수 있다.
- `docs/architecture.md`와 루트 `ARCHITECTURE.md`의 중복을 장기적으로 정리할 필요가 있다.
