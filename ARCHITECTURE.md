# Architecture

현재 코드베이스는 문서 인제스천, 검색, 생성, 평가, UI/API를 하나의 Python 애플리케이션으로 묶은 로컬 RAG 시스템이다.

## Current State

- 언어와 런타임: Python 3.14
- 인터페이스: CLI, FastAPI, Streamlit
- 검색 스택: Chroma, `multilingual-e5-large`, BM25, RRF, Cross-Encoder
- 생성 스택: Ollama + `gemma3:12b`
- 출력 형식: 현재는 PPTX 템플릿 채우기

## Top-Level Layout

```text
api/          FastAPI 엔드포인트와 요청/응답 모델
eval/         검색/응답 품질 평가 파이프라인
generator/    RFP 분석, 섹션 생성, PPTX 작성
ingestion/    파서, 청킹, 임베딩, 벡터 저장
retriever/    BM25/Vector/RRF/Rerank와 LLM 질의 엔진
docs/         운영 문서, 실행 계획, 제품 명세
scripts/      문서 검증과 handoff 루프 스크립트
```

## Runtime Flow

1. 문서를 `ingestion/parsers/`에서 읽고 정규화한다.
2. `ingestion/chunker.py`가 문서를 청크로 분리한다.
3. `ingestion/embedder.py`가 청크와 질의를 임베딩한다.
4. `ingestion/vector_store.py`가 Chroma에 청크와 메타데이터를 저장한다.
5. `retriever/engine.py`가 벡터 검색, BM25, RRF, Cross-Encoder 재순위를 조합한다.
6. `retriever/llm.py`가 Ollama 모델과 통신한다.
7. `generator/`가 요청 분석과 PPTX 초안 생성을 수행한다.
8. `api/main.py`와 `app.py`가 사용자 인터페이스를 제공한다.

## Architectural Principles

- 문서 처리, 검색, 생성, 인터페이스는 모듈 경계를 유지한다.
- 외부 런타임 경계는 Chroma와 Ollama로 제한한다.
- 검색 품질 개선은 평가 파이프라인과 함께 진행한다.
- 사용자 입력 검증은 API 경계에서 수행한다.
- 운영 규칙과 품질 기준은 코드 밖 문서로 남기고 검증 가능한 항목은 스크립트로 승격한다.

## Known Tensions

- 코드 상 제품 명칭과 문서 상 제품 포지셔닝이 아직 완전히 정리되지 않았다.
- `docs/서버_기동_가이드.md`는 원본 프로젝트 문서이며 현재 하네스 문서와 일부 중복된다.
- 현재는 로컬 실행을 전제로 하므로 배포, 비밀 관리, 멀티유저 운영 설계는 비어 있다.

## Canonical Documents

- 이 파일은 Codex 작업자가 먼저 읽는 아키텍처 기준 문서다.
- `docs/architecture.md`는 Mermaid 기반 상세 다이어그램 문서로 유지한다.
- 아키텍처 설명을 바꿀 때는 이 파일을 먼저 갱신하고, 다이어그램 변경이 필요하면 `docs/architecture.md`를 함께 갱신한다.

## References

- 상세 아키텍처 다이어그램: `docs/architecture.md`
- 서버 기동 가이드: `docs/서버_기동_가이드.md`
