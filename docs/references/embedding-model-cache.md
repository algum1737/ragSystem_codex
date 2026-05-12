# Embedding Model Cache Setup

이 문서는 오프라인 환경에서 임베딩 경로를 사용하기 전에 `intfloat/multilingual-e5-large` 모델을 로컬 캐시에 준비하는 절차를 설명한다.

## Why This Is Needed

- FastAPI startup과 Streamlit startup은 이제 모델 없이도 가능하다.
- 하지만 인제스천, 검색, 평가처럼 실제 임베딩이 필요한 경로는 `intfloat/multilingual-e5-large`가 로컬에 있어야 한다.
- 캐시가 없으면 `sentence-transformers`가 Hugging Face에서 모델을 받으려고 시도하고, 오프라인 환경에서는 실패한다.

## Target Model

- Hugging Face model id: `intfloat/multilingual-e5-large`
- 대략적인 최초 다운로드 크기: 약 560MB

## One-Time Online Preparation

인터넷이 가능한 환경에서 아래 절차를 한 번 수행한다.

```bash
cd /Users/hun/workspace/ragSystem_codex
source .venv/bin/activate
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-large')"
```

정상 완료되면 Hugging Face 캐시 아래에 모델 파일이 저장된다.

일반적인 캐시 위치:

- macOS/Linux: `~/.cache/huggingface/`

## Verify The Cache

모델이 이미 내려받아졌는지 확인:

```bash
ls ~/.cache/huggingface/hub | grep multilingual-e5-large
```

또는 실제 로드 확인:

```bash
cd /Users/hun/workspace/ragSystem_codex
source .venv/bin/activate
python -c "from sentence_transformers import SentenceTransformer; m=SentenceTransformer('intfloat/multilingual-e5-large'); print(m.get_sentence_embedding_dimension())"
```

정상이라면 `1024`가 출력된다.

## Reuse In Offline Environments

오프라인 환경에서 같은 사용자 계정으로 실행한다면 캐시가 그대로 재사용된다.

다른 머신으로 옮겨야 하면 최소한 아래를 같이 옮겨야 한다.

- `~/.cache/huggingface/`

복사 후에는 위의 "Verify The Cache" 절차로 다시 확인한다.

## Failure Mode

캐시가 없는 상태에서 임베딩 경로를 호출하면 보통 아래 증상이 보인다.

- `EmbeddingEngine` 로드 실패
- Hugging Face `HEAD` 요청 재시도 로그
- 오프라인 환경에서 이름 해석 실패 또는 연결 실패

## Related Commands

- FastAPI health 확인:
  - `curl http://127.0.0.1:8000/health`
- retrieval 평가:
  - `python eval/pipeline.py --metric retrieval`
- 인제스천:
  - `python ingest.py <file-or-dir>`
