# RAG 품질 개선 로드맵

**최종 업데이트:** 2026-05-14  
**현재 버전:** v0.4 진행 중 (검색 품질 1차 개선 완료)  
**목적:** 특정 카테고리 문서 기반 RAG 검색 및 문서 초안 생성 파이프라인  
**검증 도메인:** 이용약관 (예시 — 다른 도메인으로 교체 가능)

---

## ragSystem 모델 구조

```
질문 입력
    │
    ▼
┌─────────────────────────────┐
│  임베딩 모델                 │  ← 검색 품질 결정
│  multilingual-e5-large      │     문서/질문을 벡터로 변환
│  (1024dim, 94개 언어)        │     query: / passage: prefix 처리
│  (ingestion/embedder.py)    │
└─────────────────────────────┘
    │  관련 청크 후보 (top_k×3)
    ▼
┌─────────────────────────────┐
│  하이브리드 검색              │  BM25 + Vector + RRF
│  + doc_type 필터             │  (retriever/engine.py)
└─────────────────────────────┘
    │  후보 top_20
    ▼
┌─────────────────────────────┐
│  Cross-Encoder 재순위        │  mmarco-mMiniLMv2-L12-H384-v1
│  (retriever/engine.py)      │
└─────────────────────────────┘
    │  상위 후보 창 내 source 다양성 보존
    ▼
┌─────────────────────────────┐
│  최종 청크 선택              │  retrieve()로 LLM 생성과 분리
│  source-aware top_5         │  RAG 검색 지표 안정 측정
└─────────────────────────────┘
    │  top_5
    ▼
┌─────────────────────────────┐
│  LLM                        │  ← 답변 품질 결정
│  Ollama (gemma3:12b)        │     청크 + 질문 → 최종 답변 생성
│  (retriever/llm.py)         │
└─────────────────────────────┘
    │
    ▼
  최종 답변
```

---

## 개선 항목 현황

### ✅ 완료 항목

| 개선 방법 | 완료 버전 | 효과 |
|-----------|-----------|------|
| 하이브리드 검색 (BM25 + Vector + RRF) | v0.1 Phase 5 | 키워드+의미 양쪽 재현율 향상 |
| 다국어 임베딩 교체 (e5-large, 1024dim) | v0.3 Phase 10 | 한국어 검색 품질 +3~8%p 추정 |
| Cross-Encoder 재순위 | v0.3 Phase 11 | NDCG@10 +5~12%p 추정 |
| 청킹 최적화 (size 1000, overlap 200) | v0.2 Phase 8 | 청크 맥락 증가, 조항 경계 잘림 감소 |
| 컨텍스트 한도 확장 (4000→8000자) | v0.2 Phase 9 | 더 많은 청크 참조, 답변 완결성 향상 |
| 범용 프롬프트 | v0.2 Phase 9 | 이용약관 도메인 답변 품질 향상 |
| 평가 파이프라인 구축 | v0.3 Phase 12 | Precision@K / Accuracy / Faithfulness 측정 가능 |
| doc_type 메타데이터 필터링 | v0.4 Phase 13 | tc-05 Precision@5 0.2→0.4, 전체 0.46→0.48 |
| 평가 하네스 정렬 | 2026-05-13 | vector-only / RAG 검색 지표 분리 |
| Accuracy 평가 보정 | 2026-05-13 | OR keyword group으로 의미상 동등 표현 반영 |
| 부분 답변 정책 | 2026-05-13 | 일부 근거가 있을 때 no-answer 대신 확인/미확인 분리 |
| GitHub Actions 최소 CI | 2026-05-14 | PR checks에서 문서 검증과 Python compile 검증 |
| RAG 검색 source 다양성 선택 | 2026-05-14 | `rag_precision@k_mean` 0.54→0.60, coverage 0.925→1.0 |
| 원본 파일명 메타데이터 보존 (버그 수정) | v0.3 | Precision@K 평가 정상화 |
| TxtParser / MdParser 추가 | v0.2 Phase 7 | .txt, .md 파일 인제스천 가능 |

---

### 🔄 진행 중 (v0.4)

| 개선 방법 | 대상 | 비고 |
|-----------|------|------|
| 다음 품질 병목 재분류 | 낮은 점수 케이스 분석 | active plan: `2026-05-14-next-quality-iteration.md` |
| 다음 구현 실험 후보 선정 | 청킹 / hybrid 가중치 / reranking / 평가셋 | 사용자 승인 후 별도 active plan 승격 |

---

### ⬜ 미착수 (우선순위 순)

| 개선 방법 | 대상 | 임팩트 | 구현 난이도 | 비고 |
|-----------|------|--------|-------------|------|
| MMR 다양성 검색 | 단일문서 집중 완화 | 중간 | 중간 | 1차 source 다양성 선택 적용 후 잔여 후보 |
| 중복 문서 해시 감지 | 노이즈 감소 | 중간 | 낮음 | 파일 해시 기반 스킵 |
| Query Rewriting | 모호한 쿼리 처리 | 중간 | 중간 | LLM 2회 호출 트레이드오프 |
| Parent-Child 청킹 | 검색 정밀도+컨텍스트 | 중간 | 높음 | ChromaDB 저장 구조 변경 필요 |
| 이용약관 특화 QLoRA | 도메인 어투/형식 | 높음 | 높음 | 데이터 수집 선행 필요 |

---

## 실측 기준선 (2026-05-14 검색 품질 1차 개선 완료)

```
최신 리포트: eval/results/eval_20260514_113849.json

vector_precision@k_mean: 0.48
rag_precision@k_mean:    0.60
source_coverage@k_mean:  1.0
accuracy_mean:           0.70
faithfulness_mean:       0.90
not_found_rate:          0.10
```

v0.4 검색 1차 목표: 실제 RAG 경로 기준 `rag_precision@k_mean` **0.60 이상** 달성

---

## 추천 진행 순서 (잔여)

```
현재 (검색 품질 1차 개선 완료)
    │
    ▼
최신 full eval 케이스별 분석
    │  → tc-01, tc-03, tc-04, tc-09 중심 재분류
    ▼
다음 개선 후보 선정
    │  → 청킹 / hybrid search 가중치 / reranking 적용 범위 / 평가셋 확장
    ▼
사용자 승인 후 별도 active plan으로 구현
```

---

*실측값은 `.venv/bin/python eval/pipeline.py --all`로 측정한다. 최신 before/after는 `docs/references/2026-05-14-before-after.md`를 기준으로 한다.*
