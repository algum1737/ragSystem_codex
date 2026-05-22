# RAG 품질 개선 로드맵

**최종 업데이트:** 2026-05-22

**현재 버전:** v0.4 진행 중 (확장 평가셋 안정화 및 source scope 정책 정리 중)

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
┌─────────────────────────────┐
│  평가 하네스                 │  retrieval / accuracy / faithfulness
│  eval/pipeline.py           │  judge용 context 선택과 keyword OR group
└─────────────────────────────┘
    │
    ▼
  최종 답변 및 평가 리포트
```

---

## 개선 항목 현황

### ✅ 완료 항목

| 개선 방법 | 완료 버전 | 효과 |
| --- | --- | --- |
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
| 평가셋 정합성 보정 | 2026-05-14 | `accuracy_mean` 0.70→0.875, `faithfulness_mean` 0.90→1.0 |
| Retrieval metric 정규화 | 2026-05-14 | `rag_normalized_source_precision@k_mean=1.0`, `rag_chunk_precision@k_mean=0.96` |
| Faithfulness context 선택 개선 | 2026-05-15 | `faithfulness_mean=1.0` 안정화 |
| 잔여 keyword accuracy 보정 | 2026-05-15 | `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0` |
| 원본 파일명 메타데이터 보존 (버그 수정) | v0.3 | Precision@K 평가 정상화 |
| TxtParser / MdParser 추가 | v0.2 Phase 7 | .txt, .md 파일 인제스천 가능 |
| 평가셋 일반화 검토 | 2026-05-22 | 기존 10개 케이스의 과적합 가능성과 hard case 확장 필요성 확인 |
| hard case 확장 | 2026-05-22 | 10개→16개→17개 케이스로 확장, 13개 문서/318개 청크 corpus 검증 |
| expected no-answer 평가 정책 | 2026-05-22 | `expected_not_found`, `not_found_success_rate` 추가 |
| Source drift calibration | 2026-05-22 | `tc-04`, `tc-06`, `tc-16`, `tc-17` 정리 후 생성 지표 1.0 회복 |
| Source drift regression guard | 2026-05-22 | critical/watch case 자동 리포트 스크립트 추가 |
| Watch case review | 2026-05-22 | watch case 7건을 source scope 정책 후보로 분리 |

---

### 🔄 진행 중 (v0.4)

| 개선 방법 | 대상 | 비고 |
| --- | --- | --- |
| Source scope policy | `relevant_sources` 범위 기준 | active plan: `2026-05-22-source-scope-policy.md` |
| Watch case 후속 보정 판단 | `tc-02`, `tc-03`, `tc-07`, `tc-08`, `tc-14`, `tc-15` | source scope 정책 확정 후 재검토 |

---

### ⬜ 미착수 (우선순위 순)

| 개선 방법 | 대상 | 임팩트 | 구현 난이도 | 비고 |
| --- | --- | --- | --- | --- |
| MMR 다양성 검색 | 단일문서 집중 완화 | 중간 | 중간 | 1차 source 다양성 선택 적용 후 잔여 후보 |
| 중복 문서 해시 감지 | 노이즈 감소 | 중간 | 낮음 | 파일 해시 기반 스킵 |
| Query Rewriting | 모호한 쿼리 처리 | 중간 | 중간 | LLM 2회 호출 트레이드오프 |
| Parent-Child 청킹 | 검색 정밀도+컨텍스트 | 중간 | 높음 | ChromaDB 저장 구조 변경 필요 |
| 이용약관 특화 QLoRA | 도메인 어투/형식 | 높음 | 높음 | 데이터 수집 선행 필요 |

---

## 실측 기준선 (2026-05-22 full eval)

```
최신 리포트: eval/results/eval_20260522_160844.json

total_cases:             17
precision@k_mean:        0.3529
vector_precision@k_mean: 0.3529
rag_precision@k_mean:    0.4235
rag_normalized_source_precision@k_mean: 0.7971
rag_chunk_precision@k_mean:             0.5882
source_recall@k_mean:                   0.7836
source_coverage@k_mean:  0.7836
accuracy_mean:           1.0
faithfulness_mean:       1.0
not_found_rate:          0.0588
not_found_success_rate:  1.0
```

v0.4 검색 1차 목표: 실제 RAG 경로 기준 `rag_precision@k_mean` **0.60 이상** 달성

v0.4 평가셋 정합성 목표: 문서 근거와 평가 질문/키워드 정렬 완료

v0.4 검색 지표 정규화 목표: 기존 precision 상한 문제 해소와 해석 가능한 source/chunk 지표 추가 완료

v0.4 생성 품질 목표: 현재 17개 평가 케이스 기준 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0` 달성

---

## 추천 진행 순서 (잔여)

```
현재 (17개 평가 케이스 기준 생성 품질 상한 달성)
    │
    ▼
source scope policy 수립
    │  → relevant_sources 범위를 전체 관련 문서 기준으로 볼지 대표 근거 기준으로 볼지 결정
    ▼
watch case 후속 보정 판단
    │  → tc-02, tc-03, tc-07, tc-08, tc-14, tc-15 재검토
    ▼
필요 시 평가셋 source 기준 보정 및 full eval 재실행
```

---

*실측값은 `.venv/bin/python eval/pipeline.py --all`로 측정한다. 최신 결과는 `eval/results/eval_20260522_160844.json`, `docs/references/2026-05-22-eval-source-drift-calibration.md`, `docs/references/2026-05-22-watch-case-review.md`를 기준으로 한다.*
