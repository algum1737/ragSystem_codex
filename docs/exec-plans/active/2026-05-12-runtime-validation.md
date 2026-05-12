# Runtime Validation Plan

## Goal

현재 저장소에서 Python 실행 환경을 복구하고, API, Streamlit, 평가 파이프라인이 최소 수준에서 동작하는지 smoke test로 확인한다.

## Scope

- Python 가상환경 `.venv` 생성
- `requirements.txt` 의존성 설치
- FastAPI 기동과 `/health` 확인
- Streamlit 앱 기동 확인
- `eval/pipeline.py` 실행 가능 여부 확인
- 로컬 런타임 경계(Ollama, Chroma, 샘플 데이터) 의존성 분리

## Assumptions

- 로컬 머신에 Python 3.14 실행 환경이 있다.
- Ollama는 별도 설치 및 기동 상태일 수 있으나 아직 검증 전이다.
- Chroma 데이터베이스는 현재 저장소에 없으므로 일부 검증은 빈 상태 기준일 수 있다.

## Steps

1. `.venv` 생성과 활성화 절차 확인
2. `pip install -r requirements.txt` 실행
3. FastAPI 서버 기동과 `/health` 응답 확인
4. Streamlit 앱 기동 여부 확인
5. `eval/pipeline.py --metric retrieval` 실행 가능 여부 확인
6. 실패 시 원인을 환경, 모델, 데이터, 코드로 분류해 기록

## Risks

- Python 3.14와 일부 패키지의 호환성 이슈가 있을 수 있다.
- Ollama 모델 미설치 또는 미기동 상태면 API와 eval 검증이 제한될 수 있다.
- `chroma_db/`가 비어 있으므로 검색 품질 수치는 바로 재현되지 않을 수 있다.

## Validation

- `.venv` 생성과 의존성 설치가 완료되어야 한다.
- `uvicorn api.main:app --port 8000`이 기동되어야 한다.
- `curl http://localhost:8000/health`가 유효한 응답을 반환해야 한다.
- `streamlit run app.py`가 시작되어야 한다.
- `python eval/pipeline.py --metric retrieval` 실행 결과 또는 실패 원인이 문서화되어야 한다.

## Open Work

- FastAPI 서버 실제 기동과 `/health` 확인
- Streamlit 앱 실제 기동 확인
- `eval/pipeline.py` 실행 확인
- `sentence_transformers` / `torch` 포함 경로의 초기 로딩 시간을 smoke test에서 관찰

## Progress

- `.venv` 생성 완료
- `requirements.txt` 설치 완료
- `.venv/bin/pip check` 통과
- `fastapi`, `streamlit`, `chromadb` import 확인 완료
- FastAPI smoke test 1차 실행 완료
- `EmbeddingEngine` lazy initialization 적용 완료
- FastAPI `/health` smoke test 성공
- Streamlit smoke test 성공
- eval retrieval smoke test 실행 완료
- `multilingual-e5-large` 로컬 캐시 준비 완료
- `/stats` endpoint 복구 완료
- retrieval eval 성공
- full eval 실행 완료

## Verification Notes

- Python 버전: `3.14.4`
- 패키지 의존성 충돌: 없음
- 무거운 ML 패키지 import는 첫 초기화 비용이 있어 환경 복구 단계에서는 경량 import까지만 확인했고, 전체 경로 검증은 다음 smoke test 단계로 넘긴다.
- `uvicorn api.main:app --port 8000` 실행 시 앱 시작 단계에서 `EmbeddingEngine`이 `intfloat/multilingual-e5-large`를 로드하려고 하며, 로컬 캐시가 없는 상태에서 `huggingface.co` 접근이 필요했다.
- 현재 환경은 외부 네트워크 없이 실행 중이므로 모델 다운로드 단계에서 반복 재시도가 발생했고, `/health` 응답 확인까지 도달하지 못했다.
- 결론: FastAPI 기동 실패의 1차 원인은 코드 예외가 아니라 "로컬 모델 캐시 부재 + 오프라인 환경"이다.
- `ingestion/embedder.py`를 수정해 임베딩 모델 로드를 요청 시점으로 미뤘다.
- 수정 후 FastAPI startup은 오프라인에서도 완료됐고 `GET /health`가 `200 OK`와 `{"status":"ok","model":"gemma3:12b"}`를 반환했다.
- 현재는 검색, 인제스천, 평가처럼 실제 임베딩이 필요한 경로에서만 모델 캐시 필요 여부를 확인한다.
- `streamlit run app.py --server.headless true --server.port 8501` 실행 후 `HEAD /` 요청이 `200 OK`를 반환했다.
- `python eval/pipeline.py --metric retrieval` 실행 결과, 코드 예외 없이 `Chroma DB가 비어 있습니다. 먼저 문서를 인제스천하세요.` 메시지로 조기 종료했다.
- 결론: eval의 현재 blocker는 모델 캐시가 아니라 "평가 대상 데이터 부재"다.
- `SentenceTransformer('intfloat/multilingual-e5-large')`를 실행해 캐시를 생성했다.
- `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` 환경에서 `local_files_only=True`로 다시 로드했을 때 `dim 1024`를 확인했다.
- `ingestion/embedder.py`에서 `SentenceTransformer` import 시점을 지연시켜 오프라인 플래그가 실제 로딩 경로에 반영되도록 수정했다.
- `ingestion/vector_store.py`에서 stale collection handle을 감지하면 컬렉션을 다시 잡도록 수정했다.
- 수정 후 `GET /stats`가 `{"collection_name":"ragSystem","count":89}`를 반환했다.
- `python eval/pipeline.py --metric retrieval` 결과 `precision@k_mean: 0.48`로 정상 완료됐다.
- `python eval/pipeline.py --all` 결과도 `precision@k_mean: 0.48`로 완료됐고 리포트는 `eval/results/eval_20260512_175957.json`에 저장됐다.
- 다만 `accuracy_mean`과 `faithfulness_mean`은 `None`이었다. 원인은 `Ollama 연결 실패: http://localhost:11434`로, 로컬 LLM 서버가 실행 중이지 않았다.
- Cross-Encoder도 로컬 캐시가 없어 오프라인 환경에서 로드되지 않았고, 폴백 경로로 평가가 진행됐다.
- 권한 상승으로 `python eval/pipeline.py --all`을 다시 실행했을 때 전체 지표가 정상 산출됐다.
- 최신 전체 평가 리포트: `eval/results/eval_20260512_182410.json`
- 최신 전체 평가 수치:
  - `precision@k_mean: 0.48`
  - `accuracy_mean: 0.575`
  - `faithfulness_mean: 0.7`
- 결론: 현재 남은 품질 이슈는 런타임 장애가 아니라 검색/모델 품질 자체다.

## Next Actions

- 필요하면 Cross-Encoder 모델도 로컬 캐시에 준비해 reranking 경로를 완전 오프라인으로 맞춘다.
