# gemmna4 프로젝트 분석 및 ragSystem 비교 리포트

작성일: 2026-04-27

---

## 1. gemmna4 프로젝트 개요

### 목적

RFP(제안요청서) DOCX를 입력하면 기존에 인덱싱된 과거 RFP+제안서 쌍을 RAG로 검색하고, Gemma 4(Ollama)가 7개 섹션을 자동 생성한 뒤 HTML 및 PPTX 형식으로 출력하는 완전 로컬 AI 파이프라인이다.

ragSystem과 목적이 동일하지만 구현 깊이가 크게 다르다. gemmna4는 단순한 Q&A RAG가 아니라 "제안서 문서 완성"에 특화된 구조를 가지고 있다.

### 기술 스택

| 레이어 | 기술 | 비고 |
|--------|------|------|
| LLM | Ollama + Gemma 4 (e4b/26b) | 컨텍스트 32K~128K 가변 |
| 임베딩 | nomic-embed-text (Ollama) | Ollama API 통해 호출 |
| 벡터 DB | ChromaDB | 2개 컬렉션: rfp, proposal |
| BM25 | rank-bm25 | 하이브리드 검색 |
| 재랭킹 | sentence-transformers CrossEncoder | mmarco-mMiniLMv2 (한국어 지원) |
| 파싱 | python-docx (RFP), python-pptx (제안서) | RFP-제안서 쌍 구조 |
| 생성 | python-pptx + Jinja2 HTML | 이중 출력 |
| API | FastAPI (비동기) | 8개 REST 엔드포인트 |
| DB | SQLAlchemy + aiosqlite | 메타데이터·작업 상태 영속 |
| 로깅 | structlog | 구조화 JSON 로그 |
| 설정 | pydantic-settings + .env | 타입 안전 환경변수 |

---

## 2. 아키텍처

### 전체 데이터 흐름

```
[인제스천]
RFP DOCX + 제안서 PPTX 쌍 업로드
    → DocxParser (RFP 텍스트 추출)
    → PptxParser (제안서 슬라이드 텍스트 추출)
    → PairMapper (RFP-제안서 pair_id 매핑)
    → ChunkSplitter (섹션 인식 청킹)
    → EmbeddingManager (nomic-embed-text via Ollama)
    → VectorStoreManager (ChromaDB, 2개 컬렉션)
    → SQLAlchemy DB (pair 메타데이터 저장)

[생성]
새 RFP DOCX 업로드
    → RFP 파싱 → raw_text 추출
    → GenerationOrchestrator.generate_proposal()
        ├─ [1단계] RFP 구조화 분석: LLM → RFPAnalysis JSON
        │    (project_summary, requirements, constraints, keywords, industry, budget, deadline)
        ├─ [2단계] wave 분리: 섹션 의존도 그래프 → 토폴로지 정렬
        │    Wave 1: cover, problem_analysis, team (의존 없음)
        │    Wave 2: executive_summary (cover 의존), solution (problem_analysis 의존)
        │    Wave 3: implementation_plan (solution 의존)
        │    Wave 4: cost (implementation_plan 의존)
        └─ [3단계] 각 wave asyncio.gather() 병렬 실행
              각 섹션: 한국어 키워드 쿼리 + RFP 키워드 → Retriever → 프롬프트 조립 → LLM 생성
    → PptxGenerator (python-pptx, 템플릿 슬라이드 자동 채우기)
    → HtmlRenderer (Jinja2, proposal_html_generator)
```

### 핵심 컴포넌트

#### Retriever — 3단계 하이브리드 검색

```
쿼리 텍스트
    → [Vector] nomic-embed-text 임베딩 → ChromaDB cosine 검색 (top_k × 4 over-fetch)
    → [BM25]   _tokenize(한/영 정규식) → BM25Okapi.get_scores() (캐시된 전체 인덱스)
    → [RRF]    Reciprocal Rank Fusion (k=60) 앙상블 → 상위 top_k × 2 선별
    → [Rerank] Cross-Encoder (mmarco-mMiniLMv2) predict() → 최종 top_k 반환
               (Cross-Encoder 미설치 시 MMR 폴백)
```

BM25는 컬렉션 크기 변화 감지 시 자동 재인덱싱되며, Cross-Encoder는 지연 로드되어 미설치 환경에서도 폴백으로 동작한다.

#### GenerationOrchestrator — 섹션별 특화 생성

섹션마다 별도 파라미터가 정의되어 있다:

| 섹션 | temperature | max_tokens | 의존 섹션 |
|------|-------------|------------|---------|
| cover | 0.1 | 1500 | 없음 |
| executive_summary | 0.2 | 2500 | cover |
| problem_analysis | 0.15 | 3500 | 없음 |
| solution | 0.35 | 6144 | problem_analysis |
| implementation_plan | 0.2 | 5000 | solution |
| team | 0.1 | 2000 | 없음 |
| cost | 0.1 | 3000 | implementation_plan |

생성 실패 시 에러 텍스트 대신 RFPAnalysis 기반 최소 대체 문구를 삽입(fallback)하며, 재시도는 2회까지 지수 백오프로 수행된다.

#### 데이터 모델 — RFP-제안서 쌍 구조

ragSystem과 가장 큰 구조적 차이: gemmna4는 단독 문서 인덱싱이 아니라 `(RFP, 제안서)` 쌍을 pair_id로 묶어 관리한다. Chroma 컬렉션도 rfp_chunks / proposal_chunks 2개로 분리되어 있어 RFP 요구사항 컨텍스트와 과거 제안서 작성 패턴을 독립적으로 검색할 수 있다.

### API 구조

```
POST /api/v1/ingest           RFP+제안서 쌍 업로드 → 비동기 인덱싱
POST /api/v1/generate         새 RFP로 제안서 생성 시작 → task_id 반환
GET  /api/v1/status/{task_id} 생성 작업 진행률 조회 (polling)
GET  /api/v1/documents        생성된 문서 목록
GET  /api/v1/documents/{id}/download/{html|pptx} 결과 다운로드
GET  /api/v1/admin/health     Ollama 연결 포함 헬스체크
GET  /api/v1/admin/stats      통계
DELETE /api/v1/admin/pairs/{id}
```

생성은 비동기 작업(task_id)으로 시작하고 클라이언트가 폴링하는 구조다. 진행률(0~100%)과 현재 섹션명을 실시간으로 반환한다.

---

## 3. 완성도 평가

| 영역 | 상태 | 비고 |
|------|------|------|
| 인제스천 파이프라인 | ✓ 완성 | RFP+PPTX 쌍, 비동기 |
| 하이브리드 RAG | ✓ 완성 | BM25+Vector+Cross-Encoder |
| RFP 구조화 분석 | ✓ 완성 | JSON extraction, 섹션별 활용 |
| 섹션 병렬 생성 | ✓ 완성 | wave 의존도 그래프 |
| PPTX 생성 | ✓ 완성 | python-pptx 템플릿 기반 |
| HTML 생성 | ✓ 완성 | Jinja2 + image_to_css |
| Web UI (API+라우터) | ✓ 완성 | FastAPI routers |
| 메타데이터 DB | ✓ 완성 | SQLAlchemy + aiosqlite |
| 구조화 로깅 | ✓ 완성 | structlog |
| Fine-tuning | △ scaffold | dataset_builder, finetune_service 뼈대만 존재 |
| 테스트 코드 | △ 미흡 | scripts/에 임시 스크립트만 |
| 에러 복구 UI | △ 미흡 | API는 완성, 프론트 표시 불완전 |

전체 완성도: **~85%**

---

## 4. ragSystem과의 비교

### 공통점

- 완전 로컬 실행 (Ollama + ChromaDB)
- 한국어 문서 처리 대상
- FastAPI HTTP 서버
- python-pptx 기반 PPT 생성
- RFP → 제안서 초안 자동화라는 동일한 최종 목표

### 차이점 요약

| 항목 | ragSystem (현재) | gemmna4 |
|------|-----------------|---------|
| **RAG 방식** | Vector 단일 검색 | BM25 + Vector + Cross-Encoder (3단 하이브리드) |
| **RFP 전처리** | 없음 (raw 텍스트 그대로) | 구조화 JSON 분석 (RFPAnalysis) |
| **생성 단위** | 단일 쿼리 응답 | 7개 섹션 의존도 wave 병렬 생성 |
| **섹션 파라미터** | 없음 | 섹션별 temperature/max_tokens 분리 |
| **생성 실패 처리** | 에러 전파 | fallback 텍스트 삽입 + 재시도 |
| **데이터 모델** | 단일 문서 인덱싱 | RFP-제안서 쌍(pair_id) 구조 |
| **벡터 컬렉션** | 1개 (ragSystem) | 2개 (rfp_chunks, proposal_chunks) |
| **임베딩 모델** | sentence-transformers (로컬 파일) | nomic-embed-text (Ollama API) |
| **출력 형식** | PPTX 예정 (Phase 6) | HTML + PPTX 이중 출력 |
| **작업 처리** | 동기 요청-응답 | 비동기 task_id + 폴링 |
| **메타데이터 저장** | ChromaDB 메타데이터만 | SQLAlchemy 별도 DB |
| **설정 관리** | 하드코딩 + 일부 환경변수 | pydantic-settings + .env |
| **로깅** | 기본 logging | structlog 구조화 JSON 로그 |
| **지원 입력 파서** | PDF, DOCX, HWP | DOCX(RFP), PPTX(제안서) |
| **Web UI** | Phase 5 (미구현) | 완성 |

---

## 5. ragSystem에 접목해야 할 점

우선순위 순서로 정리했다.

### 5-1. 하이브리드 RAG: BM25 + Vector + RRF (최우선)

**현재:** `VectorStore.similarity_search()` — 벡터 유사도만 사용  
**gemmna4:** Vector 검색 + BM25 검색 → Reciprocal Rank Fusion → Cross-Encoder Rerank

한국어 문서에서 키워드 기반 검색(BM25)과 의미 기반 검색(Vector)은 상호 보완적이다. "WBS", "사업비 3억원" 같은 구체적 키워드는 BM25가 더 잘 잡고, "비용 계획 수립" 같은 의미 확장은 Vector가 더 잘 잡는다.

적용 방법:
- `retriever/engine.py`에 BM25 레이어 추가 (`rank-bm25` 패키지)
- 컬렉션 크기 변화 감지 시 BM25 인덱스 재빌드 (gemmna4의 `_BM25Cache` 패턴)
- RRF 앙상블 후 Cross-Encoder rerank 선택 적용 (sentence-transformers 추가 설치 필요)

### 5-2. RFP 구조화 분석 (Phase 6 필수)

**현재:** RFP 텍스트를 청크 단위로 인덱싱하고 쿼리에 그대로 사용  
**gemmna4:** RFP 전체를 LLM에 넣어 `{project_summary, requirements, keywords, industry, budget, deadline}` JSON 추출 후 모든 섹션 생성에 주입

Phase 6 PPT 생성 시 이 패턴 없이는 섹션들이 RFP 맥락을 공유하지 못한다. 섹션 간 일관성이 깨진다. 생성 시작 시 RFPAnalysis를 먼저 추출하고 각 섹션 프롬프트에 포함하는 것이 필수다.

### 5-3. 섹션 의존도 기반 wave 생성 (Phase 6 필수)

**현재:** 섹션 생성 전략 미정 (Phase 6)  
**gemmna4:** `_SECTION_DEPS` 딕셔너리로 의존도 정의 → `_build_generation_waves()` 토폴로지 정렬 → `asyncio.gather()` wave 단위 병렬 실행

표지가 완성된 뒤 경영진 요약이 생성되고, 문제 분석이 끝난 뒤 솔루션이 생성되는 순서는 내용 일관성에 직접 영향을 미친다. 동시에 의존성 없는 섹션들은 병렬로 생성해서 속도를 높인다. Phase 6 설계 시 그대로 참조할 수 있다.

### 5-4. 섹션별 temperature / max_tokens 분리 (Phase 6)

**현재:** 단일 LLM 파라미터  
**gemmna4:** 섹션마다 다른 temperature (표지·비용 0.1, 솔루션 0.35)와 max_tokens (솔루션 6144, 비용 3000)

창의적 내용(솔루션, 기술 방안)은 temperature를 높이고, 형식이 정형화된 내용(표지, 비용)은 낮추는 것이 품질에 영향을 준다. 적용 비용이 낮다.

### 5-5. 생성 실패 fallback + 재시도 (Phase 6)

**현재:** 에러 전파 시 전체 생성 실패  
**gemmna4:** 섹션별 2회 재시도(지수 백오프) + 최종 실패 시 RFPAnalysis 기반 최소 대체 텍스트 삽입

PPT 생성처럼 7개 섹션 중 하나가 실패해도 나머지 6개는 결과를 내야 한다. fallback 패턴은 사용성에 직접 영향을 미친다.

### 5-6. 비동기 생성 작업 (Phase 5 Web UI)

**현재:** POST /query 는 동기 응답 (LLM 응답까지 HTTP 연결 유지)  
**gemmna4:** `task_id` 반환 → 클라이언트가 `/status/{task_id}` 폴링

LLM으로 7개 섹션을 생성하면 수 분이 걸린다. 이 시간 동안 HTTP 연결을 유지하면 타임아웃과 UX 문제가 발생한다. Phase 5 Web UI 설계 시 task_id + 폴링 패턴을 고려해야 한다.

### 5-7. pydantic-settings 기반 설정 관리 (낮은 우선순위)

**현재:** `_DB_PATH = "./chroma_db"` 하드코딩, 일부 환경변수 직접 접근  
**gemmna4:** `Settings(BaseSettings)` — `.env` 파일 자동 로드, 타입 검증, 디렉토리 자동 생성

v0.1에서 큰 문제는 아니지만 배포 환경이 달라질 때 관리 비용이 올라간다.

### 5-8. structlog 구조화 로깅 (낮은 우선순위)

운영 환경 전환 시 `logging.getLogger()` 텍스트 로그보다 structlog JSON 로그가 검색·필터링에 유리하다. Deferred Issue "요청 로깅/correlation ID 없음"과 함께 처리할 수 있다.

---

## 6. ragSystem이 gemmna4보다 나은 점

gemmna4가 앞선 부분이 많지만, ragSystem에서 더 잘 처리한 부분도 있다.

| 항목 | ragSystem 장점 |
|------|---------------|
| **HWP 지원** | pyhwp + LibreOffice fallback으로 한국 문서 형식 지원. gemmna4는 DOCX/PPTX만 처리 |
| **업로드 크기 제한** | MAX_UPLOAD_BYTES=50MB + 413 응답 (audit 적용). gemmna4는 동일 보호 없음 확인 필요 |
| **temp file 안전 처리** | `tmp_path=None` + 단일 try/finally 패턴. gemmna4는 검토 필요 |
| **인제스천 입력 유연성** | PDF, DOCX, HWP 혼합 디렉토리 지원. gemmna4는 쌍 구조 필수 |

---

## 7. 요약

gemmna4는 같은 문제를 더 정교하게 풀고 있는 참조 구현체다. RAG 검색 품질(하이브리드), 생성 품질(RFP 구조화 + wave 의존도), 운영 품질(비동기 task, structlog) 세 축에서 ragSystem보다 앞서 있다.

**ragSystem Phase 6 PPT 생성 설계 시 즉시 참고해야 할 것:**
1. RFPAnalysis JSON extraction 패턴 (생성 첫 단계)
2. `_SECTION_DEPS` + `_build_generation_waves()` + `asyncio.gather()` 패턴
3. 섹션별 temperature/max_tokens 테이블
4. fallback 텍스트 삽입 패턴

**ragSystem Phase 5 Web UI 설계 시 참고해야 할 것:**
- task_id + 폴링 구조 (LLM 생성은 동기 HTTP로 처리하면 안 됨)

**Phase 2/3 검색 품질 개선 시:**
- BM25 + Vector + RRF 하이브리드 검색 (rank-bm25 패키지 추가)
- Cross-Encoder rerank (선택, sentence-transformers 추가)

---

*gemmna4 분석 기준: 2026-04-27*
*대상 경로: /Users/hun/workspace/gemmna4/*
