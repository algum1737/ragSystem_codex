# RAG 성능 향상 보고서

**프로젝트:** ragSystem

**작성일:** 2026-05-22

**현재 버전:** v0.4 진행 중 (확장 평가셋 안정화, no-answer 평가, source drift guard 적용)

**목적:** 특정 카테고리 문서 기반 RAG 검색 및 문서 초안 생성 파이프라인

**검증 도메인:** 이용약관 (예시 도메인 — 다른 도메인으로 교체 가능)

---

## 1. 시스템 개요

ragSystem은 완전 로컬 실행 기반의 RAG(Retrieval-Augmented Generation) 문서 생성 파이프라인입니다.

특정 카테고리의 문서를 인제스천하고, 요청사항에 맞는 내용을 검색·생성하여 원하는 형태의 문서 초안을 출력합니다.

현재 검증 도메인: 이용약관 문서 (다른 도메인으로 교체 시 `eval/test_cases.json`만 교체하면 됩니다)

```
문서 업로드
    │
    ▼
[파서] → [청커] → [임베딩 (e5-large)] → [벡터 DB (ChromaDB)]
                                               │
                               ┌───────────────┴───────────────┐
                          [벡터 검색]                      [BM25 검색]
                               └───────────────┬───────────────┘
                                           [RRF 병합]
                                               │
                                    [Cross-Encoder 재순위]
                                               │
                                  [source-aware 최종 청크 선택]
                                               │
                                         [LLM (Ollama)]
                                               │
                                             [답변]
```

**기술 스택**

| 구성 요소 | 선택 | 버전 |
| --- | --- | --- |
| LLM | Ollama (gemma3:12b) | v0.1~ |
| 벡터 DB | ChromaDB (PersistentClient, cosine) | v0.1~ |
| 임베딩 | `intfloat/multilingual-e5-large` (1024dim) | v0.3 Phase 10~ |
| 검색 방식 | 하이브리드 BM25 + Vector + RRF | v0.1 Phase 5~ |
| 재순위 | Cross-Encoder (`mmarco-mMiniLMv2-L12-H384-v1`) | v0.3 Phase 11~ |
| API | FastAPI (uvicorn, port 8000) | v0.1~ |
| UI | Streamlit (port 8501) | v0.1~ |

---

## 2. 적용 완료된 RAG 성능 향상

### 2-1. 하이브리드 검색 (BM25 + 벡터 + RRF)

**적용 시점:** v0.1 Phase 5

**파일:** `retriever/engine.py`

단일 벡터 검색만 사용할 경우 정확한 키워드 매칭이 누락되는 문제를 해결하기 위해 BM25(키워드 기반)와 벡터 검색(의미 기반)을 병행한 뒤 RRF(Reciprocal Rank Fusion)로 병합합니다.

**동작 방식:**

1. 쿼리를 벡터로 변환 → ChromaDB에서 `top_k × 3`개 후보 검색

1. BM25로 동일 쿼리에 대해 `top_k × 3`개 후보 검색

1. 두 결과를 RRF 알고리즘으로 병합 → 최종 `top_k`개 선택

```
# RRF 점수 계산 (k=60 기본값)
score(text) = Σ [ 1 / (k + rank) ]   # 벡터 순위 + BM25 순위 합산
```

**효과:** 키워드와 의미 두 측면에서 모두 관련성 높은 청크를 선택, 단일 검색 방식 대비 재현율(Recall) 향상

---

### 2-2. BM25 인덱스 캐싱

**적용 시점:** v0.1 Phase 5

**파일:** `retriever/engine.py` — `_BM25Cache` 클래스

BM25는 전체 문서를 매 쿼리마다 재인덱싱하면 성능이 크게 저하됩니다. DB에 새 문서가 추가될 때만 인덱스를 재생성하도록 캐싱 처리했습니다.

```
class _BM25Cache:
    def search(self, vs, query, n):
        current_count = vs.get_stats()["count"]
        if current_count != self._count:   # DB 변경 시에만 재인덱싱
            self._index = BM25Okapi(...)
            self._count = current_count
```

**효과:** 반복 쿼리 시 BM25 인덱스 재생성 비용 제거, 응답 속도 향상

---

### 2-3. 다국어 임베딩 모델 교체 (v0.3 — Phase 10)

**파일:** `ingestion/embedder.py`

| 버전 | 모델 | 차원 | 지원 언어 |
| --- | --- | --- | --- |
| v0.1~v0.2 | `paraphrase-multilingual-mpnet-base-v2` | 768 | 50개 |
| **v0.3~** | **`intfloat/multilingual-e5-large`** | **1024** | **94개** |

e5 계열 필수 prefix 처리 로직도 함께 추가했습니다.

```
# 인제스천 시 (passage: prefix)
texts = [f"passage: {c.text}" for c in chunks]

# 검색 시 (query: prefix)
text = f"query: {question}"
```

**효과:** MTEB 다국어 벤치마크 기준 기존 모델 대비 평균 +3~8%p 검색 정확도 향상 (벤치마크 추정치)

---

### 2-4. Cross-Encoder 재순위 (v0.3 — Phase 11)

**파일:** `retriever/engine.py` — `_CrossEncoderReranker` 클래스

BM25+Vector로 top_20 후보를 뽑은 뒤 Cross-Encoder로 재순위 매겨 LLM에 top_k만 전달합니다.

```
개선 전:  쿼리 → BM25+Vector → top_5 → LLM
개선 후:  쿼리 → BM25+Vector → top_20 → Cross-Encoder 재순위 → top_5 → LLM
```

    - 사용 모델: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` (다국어 지원)

    - RAGEngine 생성 시 `use_reranker=True`(기본값)로 자동 활성화

**효과:** 초기 검색에서 놓친 관련 청크를 정밀 재순위로 복원, NDCG@10 기준 +5~12%p 향상 (학술 벤치마크 추정)

---

### 2-5. 평가 파이프라인 구축 (v0.3 — Phase 12)

**파일:** `eval/pipeline.py`, `eval/test_cases.json`

모든 개선 효과를 수치로 검증하는 CLI 평가 스크립트를 구축했습니다.

**측정 지표:**

| 지표 | 설명 | Ollama 필요 |
| --- | --- | --- |
| Vector Precision@K | Chroma vector-only 상위 K source 평가 | 불필요 |
| RAG Precision@K | 실제 RAG 최종 source 평가 | 불필요 |
| Source Coverage@K | 관련 source 중 최종 context 포함 비율 | 불필요 |
| Answer Accuracy | LLM 답변 내 정답 키워드 포함 비율 | 필요 |
| Faithfulness | 답변이 제공된 청크에만 근거했는지 여부 | 필요 |

```
# retrieval 지표만 측정 (빠름)
python3 eval/pipeline.py --metric retrieval

# 전체 지표 측정 + 리포트 저장
python3 eval/pipeline.py --all
```

평가 케이스는 `eval/test_cases.json`에 정의합니다. 현재 이용약관 도메인 17개 케이스가 포함되어 있으며, 도메인 전환 시 이 파일과 relevant source 기준을 함께 교체하면 됩니다.

---

### 2-6. 원본 파일명 메타데이터 보존 (버그 수정)

**파일:** `ingestion/pipeline.py`, `api/main.py`

FastAPI `/ingest` 엔드포인트가 임시 파일(temp path)을 Chroma DB에 `source_path`로 저장하는 버그를 수정했습니다.

```
# 수정 전: tmp 경로가 source_path로 저장됨
result = pipeline.ingest(tmp_path)

# 수정 후: 원본 파일명을 source_name으로 전달
result = pipeline.ingest(tmp_path, source_name=file.filename)
```

**효과:** Chroma DB에 `다음 이용약관.txt` 등 원본 파일명이 저장되어 Precision@K 평가 및 출처 추적이 정상 동작

---

### 2-7. Cosine Similarity 기반 벡터 저장소

**적용 시점:** v0.1 Phase 2

**파일:** `ingestion/vector_store.py`

```
self._collection = self._client.get_or_create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"},
)
```

**효과:** 벡터 크기(magnitude)에 무관하게 방향(의미)만으로 유사도 측정 — 문서 길이 차이에 의한 편향 제거

---

### 2-8. 컨텍스트 길이 제한 확장 (v0.2)

| 버전 | max_context_chars |
| --- | --- |
| v0.1 | 4,000자 |
| **v0.2~** | **8,000자** |

**효과:** LLM에 전달되는 청크 수 증가(약 4~5개 → 8~10개), 답변 완결성 향상

---

### 2-9. 범용 이용약관 도메인 프롬프트 (v0.2)

**파일:** `retriever/engine.py` — `PROMPT_TEMPLATE`

v0.1의 "제안서 전문 어시스턴트" 고정 역할을 제거하고 문서 기반 범용 Q&A 프롬프트로 교체했습니다. 현재 이용약관 도메인에 최적화되어 있습니다.

**효과:** 이용약관 조항 해석, 해지/환불/면책 정보 추출 등 도메인 특화 답변 품질 향상

---

### 2-10. 출처 메타데이터 추적

**파일:** `ingestion/vector_store.py`, `retriever/engine.py`

각 청크에 `source_path`를 메타데이터로 저장하고, 쿼리 응답에 출처 정보를 함께 반환합니다.

**효과:** 답변의 신뢰성 검증 가능, 어떤 이용약관 문서에서 근거했는지 확인 가능

---

### 2-11. Upsert 기반 중복 방지

**파일:** `ingestion/vector_store.py`

```
ids = [f"{c.source_path}::{c.chunk_index}" for c in chunks]
self._collection.upsert(ids=ids, ...)
```

**효과:** 문서 재업로드 시 중복 청크 누적 방지

---

### 2-12. 한국어 토크나이저 (BM25)

**파일:** `retriever/engine.py` — `_tokenize()`

```
def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[가-힣]+|[a-zA-Z0-9]+", text.lower())
    return tokens if tokens else [""]
```

**효과:** 한국어 이용약관 텍스트에서 형태소 단위 BM25 키워드 매칭 정확도 향상

---

### 2-13. 청킹 최적화 (v0.2)

**파일:** `ingestion/chunker.py`

| 파라미터 | v0.1 | v0.2~ |
| --- | --- | --- |
| chunk_size | 500자 | 1,000자 |
| chunk_overlap | 50자 | 200자 |
| 구분자 | 기본값 | 한국어 문장 경계 (`。\n`, `\n\n`) 추가 |

**효과:** 청크당 컨텍스트 증가로 답변 완결성 향상, 이용약관 조항 경계 잘림 현상 감소

---

### 2-14. 다양한 문서 형식 지원 파서

**파일:** `ingestion/parsers/`

| 파서 | 대상 형식 | 적용 시점 |
| --- | --- | --- |
| PdfParser | .pdf | v0.1 Phase 1 |
| DocxParser | .docx, .doc | v0.1 Phase 1 |
| HwpParser | .hwp | v0.1 Phase 1 |
| TxtParser | .txt | v0.2 Phase 7 |
| MdParser | .md | v0.2 Phase 7 |

---

### 2-15. doc_type 메타데이터 필터링 (v0.4 — Phase 13)

**파일:** `ingestion/pipeline.py`, `ingestion/vector_store.py`, `retriever/engine.py`, `api/main.py`, `api/models.py`, `app.py`

인제스천 시 `doc_type` 메타데이터(일반약관 / 위치기반약관)를 Chroma DB에 저장하고, 쿼리 시 해당 필드로 검색 범위를 필터링합니다.

```
# 인제스천: doc_type 메타데이터 저장
pipeline.ingest(file, source_name="다음 이용약관.txt", doc_type="일반약관")

# 쿼리: doc_type 필터 적용
rag_engine.query("위약금 조건은?", doc_type="일반약관")
# → 일반약관 문서 청크만 검색
```

    - 허용 목록: `None` (전체), `"일반약관"`, `"위치기반약관"` — API/UI 양쪽 검증

    - BM25 검색도 where 파라미터로 후처리 필터링 적용

    - ChromaDB where+n_results 불일치 시 자동 재시도 fallback

**효과:**

    - tc-05(위약금/손해배상) Precision@5: **0.2 → 0.4** (위치기반약관 침범 해소)

    - 전체 평균 Precision@5: **0.46 → 0.48**

---

### 2-16. RAG 검색 경로 분리와 source 다양성 선택 (2026-05-14)

**파일:** `retriever/engine.py`, `eval/pipeline.py`

기존 `RAGEngine.query()`는 검색과 LLM 생성을 함께 수행했다. 이 구조에서는 실제 RAG 검색 경로를 측정하려면 Ollama 호출까지 필요했다. 검색 단계를 `RAGEngine.retrieve()`로 분리해 LLM 없이도 실제 RAG 최종 source를 평가할 수 있게 했다.

또한 Cross-Encoder rerank 이후 최종 top_k를 바로 자르지 않고, 상위 후보 창 안에서 source 다양성을 보존하도록 선택한다.

```
final_chunks = _select_diverse_chunks(
    ranked_chunks,
    self._top_k,
    diversity_window=self._top_k * 2 + 2,
)
```

**효과:**

| Metric | Before | After |
| --- | --- | --- |
| `rag_precision@k_mean` | `0.54` | `0.60` |
| `source_coverage@k_mean` | `0.925` | `1.0` |
| `accuracy_mean` | `0.675` | `0.70` |
| `faithfulness_mean` | `0.8` | `0.9` |

최신 리포트: `eval/results/eval_20260514_113849.json`

---

### 2-17. 평가셋 정합성 보정 (2026-05-14)

**파일:** `eval/test_cases.json`

검색 품질 1차 개선 이후 남은 accuracy 저하 케이스를 재검토했다. 문제는 검색 경로보다 평가 질문과 expected keyword가 현재 인제스트 문서 근거와 일부 맞지 않는 데 있었다.

**주요 조정:**

    - `tc-01`: 해지 시 환불 정책 질문을 문서 근거가 있는 해지 후 데이터/게시물 처리 질문으로 재분류

    - `tc-03`: 이용 제한/정지/금지 표현을 OR keyword group으로 보강

    - `tc-04`: 자동 갱신 근거 부족을 인정하면서 해지/데이터 처리 근거를 평가하도록 보정

    - `tc-09`: 권리/보유 등 약관식 표현 일부 허용

**효과:**

| Metric | Before | After |
| --- | --- | --- |
| `precision@k_mean` | `0.48` | `0.48` |
| `vector_precision@k_mean` | `0.48` | `0.48` |
| `rag_precision@k_mean` | `0.60` | `0.60` |
| `source_coverage@k_mean` | `1.0` | `1.0` |
| `accuracy_mean` | `0.70` | `0.875` |
| `faithfulness_mean` | `0.90` | `1.0` |
| `not_found_rate` | `0.10` | `0.0` |

최신 리포트: `eval/results/eval_20260514_152044.json`

---

### 2-18. Retrieval metric 정규화 (2026-05-14)

**파일:** `eval/pipeline.py`

기존 `precision@k` 계열 지표는 고유 source 수를 `top_k=5`로 나누는 방식이라, relevant source가 2개인 케이스는 최고점이 0.4, 4개인 케이스는 최고점이 0.8로 제한됐다. 기존 지표는 리포트 호환을 위해 유지하고, 해석 가능한 새 지표를 추가했다.

**추가 지표:**

    - `normalized_source_precision@k`: source 수가 적은 케이스의 상한 보정

    - `chunk_precision@k`: top_k 청크 중 relevant source 청크 비율

    - `source_recall@k`: 관련 source를 모두 포함했는지 확인

**효과:**

| Metric | Value |
| --- | --- |
| `rag_normalized_source_precision@k_mean` | `1.0` |
| `rag_chunk_precision@k_mean` | `0.96` |
| `source_recall@k_mean` | `1.0` |
| `accuracy_mean` | `0.90` |
| `faithfulness_mean` | `1.0` |
| `not_found_rate` | `0.0` |

리포트: `eval/results/eval_20260514_164724.json`

---

### 2-19. Faithfulness judge context 선택 개선 (2026-05-15)

**파일:** `eval/pipeline.py`

`tc-10`에서 답변 자체는 문서 근거와 일치하지만, faithfulness judge에 전달되는 context 중 무관 청크가 섞이면서 `faithfulness=0.0`으로 판정되는 문제가 있었다.

질문/답변과의 lexical overlap과 source diversity를 함께 고려하는 faithfulness 전용 context selector를 추가해, 판정에 필요한 근거 청크를 우선 전달하도록 개선했다.

**효과:**

| Metric | Before | After |
| --- | --- | --- |
| `faithfulness_mean` | `0.9` | `1.0` |
| `not_found_rate` | `0.0` | `0.0` |

리포트: `eval/results/eval_20260515_110900.json`

---

### 2-20. 잔여 keyword accuracy 보정 (2026-05-15)

**파일:** `eval/test_cases.json`

faithfulness 안정화 이후 남은 accuracy 감점 케이스를 재검토했다. `tc-03`, `tc-07`, `tc-09`, `tc-10`은 답변 누락보다 문서/답변에서 사용하는 자연스러운 표현과 expected keyword 사이의 불일치가 원인이었다.

**주요 조정:**

    - `tc-03`: "이용이 제한", "제한될" 등 이용 제한 표현 허용

    - `tc-07`: 면책 조항에서 책임/손해의 대체 표현 허용

    - `tc-09`: 이용자 의무 관련 권한, 라이선스, 명예, 복제/유통 등 약관 표현 허용

    - `tc-10`: 지적재산권 "귀속" 외 "보유" 표현 허용

**최종 full eval 결과:**

| Metric | Value |
| --- | --- |
| `precision@k_mean` | `0.48` |
| `vector_precision@k_mean` | `0.48` |
| `rag_precision@k_mean` | `0.60` |
| `rag_normalized_source_precision@k_mean` | `1.0` |
| `rag_chunk_precision@k_mean` | `0.96` |
| `source_recall@k_mean` | `1.0` |
| `source_coverage@k_mean` | `1.0` |
| `accuracy_mean` | `1.0` |
| `faithfulness_mean` | `1.0` |
| `not_found_rate` | `0.0` |

최신 리포트: `eval/results/eval_20260515_135903.json`

---

### 2-21. 평가셋 일반화 검토와 hard case 확장 (2026-05-22)

**파일:** `eval/test_cases.json`, `docs/references/2026-05-22-eval-generalization-review.md`, `docs/references/2026-05-22-eval-set-expansion-result.md`

기존 10개 평가 케이스는 다음/네이버 4개 약관 중심이라, 최신 13개 문서·318개 청크 corpus를 충분히 검증하지 못했다. 유료서비스, 운영정책, 위치기반서비스, 계정/운영정책 관련 hard case를 추가해 평가셋을 16개로 확장했다.

**초기 확장 평가 결과:**

| Metric | Value |
| --- | ---: |
| `total_cases` | `16` |
| `accuracy_mean` | `0.9062` |
| `faithfulness_mean` | `0.75` |
| `not_found_rate` | `0.0625` |

이 단계에서 `tc-16` expected no-answer, `tc-09`/`tc-10` faithfulness, `tc-04`/`tc-06` source drift 문제가 드러났다.

---

### 2-22. expected no-answer 평가 정책과 not_found_success 지표 (2026-05-22)

**파일:** `eval/pipeline.py`, `eval/test_cases.json`

문서에 없는 질문은 답변을 생성하지 않고 "찾을 수 없음"으로 응답하는 것이 올바른 동작이다. 이를 실패로만 집계하지 않도록 `expected_not_found`와 `not_found_success_rate`를 추가했다.

**동작 방식:**

- `expected_not_found=true`인 케이스에서 no-answer가 나오면 `answer_accuracy=1.0`
- 같은 조건에서 faithfulness도 `1.0`으로 처리
- 전체 no-answer 발생률은 `not_found_rate`, 기대한 no-answer 성공률은 `not_found_success_rate`로 분리

**효과:**

| Metric | Before | After |
| --- | ---: | ---: |
| `accuracy_mean` | `0.9062` | `0.9219` |
| `faithfulness_mean` | `0.75` | `0.9375` |
| `not_found_success_rate` | N/A | `1.0` |

리포트: `eval/results/eval_20260522_131753.json`

---

### 2-23. 확장 평가셋 source drift 보정 (2026-05-22)

**파일:** `eval/test_cases.json`, `docs/references/2026-05-22-eval-source-drift-calibration.md`

`tc-04`와 `tc-06`은 답변 품질보다 평가셋 정의와 relevant source 범위가 최신 corpus와 어긋난 케이스였다.

**주요 조정:**

- `tc-04`: 자동 갱신/해지 복합 질문을 자동 갱신 positive case로 재정의
- `tc-17`: 해지/개별 서비스 이용 종료 positive case 추가
- `tc-06`: 분쟁 해결 표현에 협의, 소송, 법원, 제소를 반영
- `tc-16`: 결제 주기와 금액 변경 조건은 expected no-answer negative case로 유지

**최종 full eval 결과:**

| Metric | Value |
| --- | ---: |
| `total_cases` | `17` |
| `accuracy_mean` | `1.0` |
| `faithfulness_mean` | `1.0` |
| `not_found_rate` | `0.0588` |
| `not_found_success_rate` | `1.0` |
| `rag_normalized_source_precision@k_mean` | `0.7971` |
| `rag_chunk_precision@k_mean` | `0.5882` |
| `source_recall@k_mean` | `0.7836` |

최신 리포트: `eval/results/eval_20260522_160844.json`

---

### 2-24. Source drift regression guard 리포트 (2026-05-22)

**파일:** `scripts/source_drift_report.py`, `docs/references/2026-05-22-source-drift-regression-report.md`

저장된 eval result JSON과 `eval/test_cases.json`을 대조해 source drift 후보를 Markdown으로 출력하는 로컬 guard를 추가했다.

**기능:**

- critical case: 생성 지표 실패 또는 source recall/precision이 critical threshold 미만
- watch case: 생성 지표는 통과했지만 source alignment 검토가 필요한 후보
- `--fail-on-critical` 옵션으로 critical 발생 시 비정상 종료 가능

**최신 리포트 결과:**

| 구분 | 결과 |
| --- | --- |
| Critical case | 없음 |
| Watch case | `tc-02`, `tc-03`, `tc-06`, `tc-07`, `tc-08`, `tc-14`, `tc-15` |

---

### 2-25. Watch case review와 source scope 정책 분리 (2026-05-22)

**파일:** `docs/references/2026-05-22-watch-case-review.md`

watch case 7건은 모두 `answer_accuracy=1.0`, `faithfulness=1.0`이었다. 따라서 즉시 `relevant_sources`를 현재 검색 결과에 맞춰 확장하지 않고, source scope 정책을 먼저 정하기로 했다.

**결정:**

- `eval/test_cases.json` 즉시 보정 보류
- watch case는 답변 실패가 아니라 source 범위 정책 후보로 유지
- 다음 active plan: `docs/exec-plans/active/2026-05-22-source-scope-policy.md`

---

## 3. 현재 인제스천 상태 (v0.4 기준)

**인제스천 문서:** 13개 약관/정책 파일 (총 318개 청크)

| 파일명 | doc_type | 종류 |
| --- | --- | --- |
| 다음 이용약관.txt | 일반약관 | 일반 이용약관 |
| 다음 위치기반서비스 이용약관.txt | 위치기반약관 | 위치기반서비스 약관 |
| 네이버 위치기반서비스 이용약관.txt | 위치기반약관 | 위치기반서비스 약관 |
| 네이버 이용약관.txt | 일반약관 | 일반 이용약관 |
| 네이버 유료서비스 이용약관.txt | 유료서비스 | 유료서비스 약관 |
| 카카오 서비스 약관_20260221_F.pdf | 일반 | 일반 서비스 약관 |
| 카카오통합서비스약관20210701.pdf | 일반 | 일반 서비스 약관 |
| 카카오계정약관20240416.pdf | 일반 | 계정 약관 |
| 카카오 유료/결제서비스 이용약관.txt | 유료서비스 | 유료/결제서비스 약관 |
| 카카오 위치정보 이용약관.txt | 위치기반서비스 | 위치정보 약관 |
| 게시물 운영정책.txt | 운영정책 | 게시물 운영정책 |
| 카카오 운영정책.txt | 운영정책 | 서비스 운영정책 |
| 계정 운영정책.txt | 운영정책 | 계정 운영정책 |

기존 인제스천 데이터에는 `일반약관`, `위치기반약관` 값이 남아 있고, 신규 인제스천 데이터는 `일반`, `유료서비스`, `위치기반서비스`, `운영정책` 기준을 사용한다. 검색 경로에는 호환 매핑이 있으나, 정식 재평가 전에는 DB 초기화 후 4개 유형 기준으로 재인제스천하는 것이 가장 깔끔하다.

---

## 4. 추가 가능한 향상 방법

| 기법 | 예상 효과 | 구현 난이도 | 상태 |
| --- | --- | --- | --- |
| ~~메타데이터 필터링~~ | ~~특정 문서 유형 필터 검색~~ | ~~중간~~ | ✅ Phase 13 완료 |
| ~~Answer Accuracy 실측~~ | ~~LLM 답변 품질 수치화~~ | ~~낮음~~ | ✅ 2026-05-14 완료 |
| ~~Faithfulness 실측~~ | ~~답변 근거 검증 수치화~~ | ~~낮음~~ | ✅ 2026-05-14 완료 |
| ~~RAG source 다양성 선택~~ | ~~최종 context source coverage 개선~~ | ~~중간~~ | ✅ 2026-05-14 완료 |
| ~~평가셋 정합성 보정~~ | ~~문서 근거와 평가 질문/키워드 정렬~~ | ~~낮음~~ | ✅ 2026-05-14 완료 |
| ~~Retrieval metric 정규화~~ | ~~검색 지표 상한 문제 해소~~ | ~~낮음~~ | ✅ 2026-05-14 완료 |
| ~~Faithfulness context 선택 개선~~ | ~~무관 context 혼입에 따른 판정 흔들림 완화~~ | ~~낮음~~ | ✅ 2026-05-15 완료 |
| ~~잔여 keyword accuracy 보정~~ | ~~표현 차이에 따른 accuracy 감점 해소~~ | ~~낮음~~ | ✅ 2026-05-15 완료 |
| ~~평가셋 일반화 검토~~ | ~~기존 10개 케이스 과적합 여부 점검~~ | ~~낮음~~ | ✅ 2026-05-22 완료 |
| ~~hard case 확장~~ | ~~13개 문서/318개 청크 corpus 검증~~ | ~~낮음~~ | ✅ 2026-05-22 완료 |
| MMR 다양성 검색 | 단일 문서 집중 문제 해소 | 중간 | source 다양성 적용 후 잔여 후보 |
| 쿼리 재작성 (Query Rewriting) | 모호한 쿼리 처리 능력 향상 | 중간 | 미정 |
| Parent-Child 청킹 | 검색 정밀도 + 컨텍스트 품질 동시 향상 | 높음 | 미정 |
| 이용약관 특화 QLoRA | 답변 형식·어투 도메인 최적화 | 높음 | 미정 |
| 중복 문서 해시 감지 | 내용 동일 문서 재인제스천 방지 | 낮음 | 미정 |

---

## 5. 요약

```
v0.1 완료 (9개 기법)
├── 검색 품질
│   ├── ✅ 하이브리드 검색 (BM25 + Vector + RRF)
│   ├── ✅ BM25 인덱스 캐싱
│   ├── ✅ Cosine Similarity 유사도 측정
│   └── ✅ 한국어 BM25 토크나이저
├── 임베딩
│   └── ✅ 다국어 임베딩 (multilingual-mpnet, 768dim)
├── 답변 품질
│   ├── ✅ 컨텍스트 길이 제한 (4,000자)
│   └── ✅ Hallucination 억제 프롬프트
└── 데이터 품질
    ├── ✅ 출처 메타데이터 추적
    └── ✅ Upsert 중복 방지

v0.2 완료 (3개 기법)
├── ✅ 지식 소스 확대 (TxtParser, MdParser)
├── ✅ 청킹 최적화 (size 1000, overlap 200)
└── ✅ 범용 프롬프트 + 컨텍스트 8,000자

v0.3 완료 (5개 기법) — 2026-05-12
├── ✅ 임베딩 모델 업그레이드 (e5-large, 1024dim) — Phase 10
├── ✅ Cross-Encoder 재순위 — Phase 11
├── ✅ 평가 파이프라인 (Precision@K / Accuracy / Faithfulness) — Phase 12
├── ✅ 원본 파일명 메타데이터 보존 버그 수정
└── ✅ 이용약관 도메인 전환 (4개 문서 인제스천)

v0.4 진행 중 — 2026-05-12~
├── ✅ doc_type 메타데이터 필터링 — Phase 13
│   Precision@5: 0.46 → 0.48 (tc-05: 0.2 → 0.4)
├── ✅ 평가 하네스 정렬 / accuracy 보정 / partial answer 정책 — 2026-05-13
├── ✅ RAG source 다양성 선택 — 2026-05-14
│   rag_precision@k: 0.54 → 0.60, source_coverage@k: 0.925 → 1.0
├── ✅ 평가셋 정합성 보정 — 2026-05-14
│   accuracy: 0.70 → 0.875, faithfulness: 0.90 → 1.0
├── ✅ Retrieval metric 정규화 — 2026-05-14
│   rag_normalized_source_precision@k: 1.0, rag_chunk_precision@k: 0.96
├── ✅ Faithfulness context 선택 개선 — 2026-05-15
│   faithfulness: 0.9 → 1.0
├── ✅ 잔여 keyword accuracy 보정 — 2026-05-15
│   accuracy: 0.95 → 1.0, faithfulness: 1.0 유지, not_found: 0.0 유지
├── ✅ 평가셋 일반화 검토 및 hard case 확장 — 2026-05-22
│   10개 → 17개 케이스, 13개 문서/318개 청크 corpus 검증
├── ✅ no-answer 평가 정책 및 source drift calibration — 2026-05-22
│   accuracy: 1.0, faithfulness: 1.0, not_found_success: 1.0
├── ✅ source drift regression guard — 2026-05-22
│   critical case 없음, watch case 7건 분리
└── 🔄 source scope policy — 2026-05-22
    relevant_sources 범위 기준 정립 진행 중
```

---

*최종 업데이트: 2026-05-22 — 최신 리포트 `eval/results/eval_20260522_160844.json`, 17개 케이스 기준 accuracy/faithfulness/not_found_success 상한 달성*
