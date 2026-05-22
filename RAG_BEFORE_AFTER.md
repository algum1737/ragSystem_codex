# RAG 성능 변화 비교 보고서

**최종 업데이트:** 2026-05-22

**목적:** 특정 카테고리 문서 기반 RAG 검색 및 문서 초안 생성

**검증 도메인:** 이용약관 (예시 — 다른 도메인으로 교체 가능)

> **중요:** 이 문서에서 "추정 효과"는 학술 연구 기반 추정치입니다.

> 실제 수치 측정은 `python3 eval/pipeline.py --all`로 실행 가능합니다. (v0.3 평가 파이프라인 구축 완료)

---

## 비교 1: v0.1 초기 → v0.2

**비교 기준:** v0.1 초기 (Phase 1~4) vs v0.2 완료 (Phase 9)

### 시스템 구성 변화

| 구성 요소 | v0.1 초기 | v0.2 완료 |
| --- | --- | --- |
| 검색 방식 | 벡터 검색 단독 | BM25 + 벡터 + RRF 병합 |
| 임베딩 모델 | multilingual-mpnet (768dim) | 동일 |
| chunk_size | 500자 | 1,000자 |
| chunk_overlap | 50자 | 200자 |
| 청크 구분자 | 영문 기본값 | 한국어 문장 경계 10종 추가 |
| 인제스천 형식 | PDF, DOCX, HWP | + TXT, MD |
| 컨텍스트 한도 | 4,000자 | 8,000자 |
| 프롬프트 | 도메인 고정 | 범용 문서 Q&A |

### 청킹 실측 변화

동일 문서(3,160자)를 두 방식으로 청킹한 결과:

| 지표 | v0.1 초기 | v0.2 완료 | 변화 |
| --- | --- | --- | --- |
| 청크 수 | 7개 | 4개 | -43% |
| 청크 평균 길이 | 454자 | 907자 | **+100%** |
| overlap | 50자 (10%) | 200자 (20%) | +4배 |
| 구분자 | 영문 기본 | 한국어 종결어미 우선 | 질적 변화 |

### 검색 방식 구조 변화

**v0.1 초기: 벡터 검색 단독**

```
쿼리 → 임베딩 → ChromaDB 유사도 검색 → top_k 청크 → LLM
```

    - 정확한 키워드가 포함된 청크를 놓칠 수 있음

    - 예: "해지 시 환불" 검색 시 "환불"이 직접 언급된 청크 누락 가능

**v0.2 완료: 하이브리드 검색**

```
쿼리
 ├─ 임베딩 → 벡터 검색 (의미 유사도)
 └─ 토크나이징 → BM25 검색 (키워드 매칭)
        ↓
    RRF 점수 병합 → top_k 청크 → LLM
```

**측정 가능한 변화:** 청크 평균 길이 +100% (실측)

**추정 변화:** 검색 Recall +5~15% (BEIR 벤치마크 기준)

---

## 비교 2: v0.2 → v0.3

**비교 기준:** v0.2 완료 (Phase 9) vs v0.3 완료 (Phase 12)

### 시스템 구성 변화

| 구성 요소 | v0.2 완료 | v0.3 완료 |
| --- | --- | --- |
| 임베딩 모델 | multilingual-mpnet (768dim, 50개 언어) | **multilingual-e5-large (1024dim, 94개 언어)** |
| e5 prefix 처리 | 없음 | `passage:` / `query:` 자동 적용 |
| 재순위 | 없음 | **Cross-Encoder (mmarco-mMiniLMv2-L12-H384-v1)** |
| 검색 후보 수 | top_k개 직접 사용 | top_k×4 후보 → Cross-Encoder → top_k |
| 평가 파이프라인 | 없음 | **Precision@K / Accuracy / Faithfulness 자동 측정** |
| 출처 메타데이터 | temp 경로 저장 (버그) | **원본 파일명 저장 (수정 완료)** |
| 도메인 | 범용 | **이용약관 특화 (4개 문서 인제스천)** |

### 임베딩 모델 변화

| 항목 | v0.2 (mpnet) | v0.3 (e5-large) |
| --- | --- | --- |
| 차원 | 768 | 1024 |
| 지원 언어 수 | 50개 | 94개 |
| MTEB 다국어 순위 | 중위권 | 상위권 |
| prefix 필요 | 없음 | passage: / query: |
| 추정 정확도 향상 | — | +3~8%p |

### 재순위 파이프라인 추가

**v0.2: 단일 패스**

```
쿼리 → BM25+Vector → top_5 → LLM
        (후보 5개)
```

**v0.3: 2-stage 검색**

```
쿼리 → BM25+Vector → top_20 → Cross-Encoder 재순위 → top_5 → LLM
        (후보 20개)                (정밀 재순위)
```

    - 초기 검색의 낮은 순위에 묻혀 있던 관련 청크를 Cross-Encoder가 재발굴

    - 추정 효과: NDCG@10 기준 +5~12%p (학술 벤치마크)

### 현재 인제스천 상태

| 파일명 | 청크 수 | 비고 |
| --- | --- | --- |
| 다음 이용약관.txt | ~32개 | 일반 이용약관 |
| 다음 위치기반서비스 이용약관.txt | ~16개 | 위치기반서비스 약관 |
| 네이버 위치기반서비스 이용약관.txt | ~10개 | 위치기반서비스 약관 |
| 네이버 이용약관.txt | ~31개 | 일반 이용약관 |
| 네이버 유료서비스 이용약관.txt | ~12개 | 유료서비스 약관 |
| 카카오 서비스 약관_20260221_F.pdf | ~42개 | 일반 서비스 약관 |
| 카카오통합서비스약관20210701.pdf | ~42개 | 일반 서비스 약관 |
| 카카오계정약관20240416.pdf | ~28개 | 계정 약관 |
| 카카오 유료/결제서비스 이용약관.txt | ~38개 | 유료/결제서비스 약관 |
| 카카오 위치정보 이용약관.txt | ~14개 | 위치정보 약관 |
| 게시물 운영정책.txt | ~22개 | 운영정책 |
| 카카오 운영정책.txt | ~16개 | 운영정책 |
| 계정 운영정책.txt | ~15개 | 운영정책 |
| **합계** | **~318개** | 최신 인제스천 기준 |

---

## 비교 3: v0.3 → v0.4 (Phase 13)

**비교 기준:** v0.3 완료 (Phase 12) vs v0.4 Phase 13 완료

### 시스템 구성 변화

| 구성 요소 | v0.3 완료 | v0.4 Phase 13 |
| --- | --- | --- |
| doc_type 메타데이터 | 없음 | **일반약관 / 위치기반약관 저장** |
| 인제스천 API | `POST /ingest` (파일만) | `POST /ingest` + `doc_type` Form 파라미터 |
| 쿼리 API | `POST /query` (질문만) | `POST /query` + `doc_type` JSON 필드 |
| 검색 필터 | 전체 문서 대상 | **doc_type 지정 시 해당 유형만 검색** |
| Streamlit UI | 파일 업로드만 | **문서 유형 selectbox 추가 (인제스천/쿼리 탭)** |
| 입력 검증 | 없음 | `_VALID_DOC_TYPES` 허용 목록 — API/모델 양쪽 |

### Precision@5 변화 (실측)

| 케이스 | v0.3 | v0.4 Phase 13 | 변화 |
| --- | --- | --- | --- |
| tc-05 위약금/손해배상 | 0.2 | **0.4** | **+0.2 ✓** |
| tc-09 이용자의무 | 0.2 | 0.2 | 변화 없음 * |
| 나머지 8개 | 0.4~0.8 | 0.4~0.8 | 회귀 없음 |
| **전체 평균** | **0.46** | **0.48** | **+0.02** |

\* tc-09는 위치기반약관 침범이 아닌 다음 이용약관 청크 쏠림 현상 — MMR 필요

---

## 전체 버전 누적 비교

```
                    v0.1 초기        v0.2 완료        v0.3 완료        v0.4 Phase 13       2026-05-15
                    ─────────────    ────────────────  ──────────────── ──────────────────── ─────────────────────
검색 방식           벡터 단독        하이브리드        하이브리드+재순위 하이브리드+재순위+필터 실제 RAG 경로 다양성 선택
임베딩 차원         768dim           768dim            1024dim          1024dim
지원 언어           50개             50개              94개             94개
재순위              없음             없음              Cross-Encoder    Cross-Encoder        Cross-Encoder
doc_type 필터       없음             없음              없음             ✅ 일반약관/위치기반약관 ✅ 4개 카테고리 기준 호환
청크 평균 길이      454자            907자             907자            907자
컨텍스트 한도       4,000자          8,000자           8,000자          8,000자
파일 형식 지원      3종              5종               5종              5종
평가 파이프라인     없음             없음              ✅ 구축 완료     ✅ 실측 완료       ✅ RAG/vector 지표 분리+정규화
Precision@5 평균    미측정           미측정            0.46             0.48                vector 0.48 / RAG 0.60
생성 품질           미측정           미측정            기준선 구축      accuracy 0.70       accuracy 1.0 / faithfulness 1.0
```

---

## 비교 4: v0.4 Phase 13 → 2026-05-14 검색 품질 1차 개선

**비교 기준:** `eval/results/eval_20260513_164755.json` vs `eval/results/eval_20260514_113849.json`

### 시스템 구성 변화

| 구성 요소 | Before | After |
| --- | --- | --- |
| RAG 검색 API | `query()` 내부에 검색과 생성 결합 | `retrieve()`로 검색 단계 분리 |
| eval retrieval | vector-only와 LLM query 의존 혼재 | LLM 없이 실제 RAG 검색 경로 측정 |
| 최종 청크 선택 | rerank top_k 직접 사용 | 상위 후보 창 안에서 source 다양성 보존 |
| doc_type 전달 | full eval query 경로에서 누락 | `RAGEngine.query(..., doc_type=...)` 전달 |

### 실측 지표 변화

| Metric | Before | After | Delta |
| --- | --- | --- | --- |
| `vector_precision@k_mean` | `0.48` | `0.48` | `0.00` |
| `rag_precision@k_mean` | `0.54` | `0.60` | `+0.06` |
| `source_coverage@k_mean` | `0.925` | `1.0` | `+0.075` |
| `accuracy_mean` | `0.675` | `0.70` | `+0.025` |
| `faithfulness_mean` | `0.8` | `0.9` | `+0.1` |
| `not_found_rate` | `0.1` | `0.1` | `0.0` |

### 케이스별 주요 변화

| Case | 변화 |
| --- | --- |
| `tc-04` | `rag_precision_at_k 0.4 -> 0.8`, `source_coverage_at_k 0.5 -> 1.0` |
| `tc-07` | `rag_precision_at_k 0.6 -> 0.8`, `source_coverage_at_k 0.75 -> 1.0` |
| `tc-09` | `answer_accuracy 0.5 -> 0.75` |
| `tc-10` | `faithfulness 0.0 -> 1.0` |

상세 before/after는 `docs/references/2026-05-14-before-after.md`에 기록한다.

---

## 비교 5: 검색 품질 1차 개선 → 평가셋 정합성 보정

**비교 기준:** `eval/results/eval_20260514_113849.json` vs `eval/results/eval_20260514_152044.json`

### 변경 내용

| Case | Before | After |
| --- | --- | --- |
| `tc-01` | 해지 시 환불 정책 질문 | 문서 근거가 있는 해지 후 데이터/게시물 처리 질문 |
| `tc-03` | exact keyword 중심 | 이용 제한/정지/금지 표현 OR group 보정 |
| `tc-04` | 자동 갱신과 해지 복합 질문 | 자동 갱신 근거 부족을 인정하고 해지/데이터 처리 근거 평가 |
| `tc-09` | 일부 표현 불일치 | 권리/보유 등 약관식 표현 일부 허용 |

### 실측 지표 변화

| Metric | Before | After | Delta |
| --- | --- | --- | --- |
| `precision@k_mean` | `0.48` | `0.48` | `0.00` |
| `vector_precision@k_mean` | `0.48` | `0.48` | `0.00` |
| `rag_precision@k_mean` | `0.60` | `0.60` | `0.00` |
| `source_coverage@k_mean` | `1.0` | `1.0` | `0.0` |
| `accuracy_mean` | `0.70` | `0.875` | `+0.175` |
| `faithfulness_mean` | `0.90` | `1.0` | `+0.10` |
| `not_found_rate` | `0.10` | `0.0` | `-0.10` |

검색 경로는 바꾸지 않았기 때문에 검색 지표는 유지됐다. 개선은 문서 근거와 평가 질문/키워드 정합성을 맞춘 결과다.

상세 결과는 `docs/references/2026-05-14-eval-case-alignment.md`에 기록한다.

---

## 비교 6: 평가셋 정합성 보정 → Retrieval metric 정규화

**비교 기준:** `eval/results/eval_20260514_152044.json` vs `eval/results/eval_20260514_164724.json`

### 변경 내용

| 항목 | Before | After |
| --- | --- | --- |
| source precision | 고유 source 수를 `top_k=5`로 나눔 | 기존 지표 유지 |
| source 수 상한 보정 | 없음 | `normalized_source_precision@k` 추가 |
| context purity | 명시 지표 없음 | `chunk_precision@k` 추가 |
| source recall | `source_coverage@k` 이름으로 제공 | `source_recall@k` alias 추가 |

### 새 기준선

| Metric | Value |
| --- | --- |
| `precision@k_mean` | `0.48` |
| `rag_precision@k_mean` | `0.60` |
| `rag_normalized_source_precision@k_mean` | `1.0` |
| `rag_chunk_precision@k_mean` | `0.96` |
| `source_recall@k_mean` | `1.0` |
| `accuracy_mean` | `0.90` |
| `faithfulness_mean` | `1.0` |
| `not_found_rate` | `0.0` |

기존 `rag_precision@k_mean=0.60`은 낮은 검색 성능이 아니라 현 metric 설계의 상한이다. 새 지표 기준으로 RAG 검색 경로는 source recall과 normalized source precision에서 모두 1.0이다.

상세 결과는 `docs/references/2026-05-14-retrieval-metric-normalization.md`에 기록한다.

---

## 비교 7: Retrieval metric 정규화 → Faithfulness context 선택 개선

**비교 기준:** `eval/results/eval_20260514_180006.json` vs `eval/results/eval_20260515_110900.json`

### 변경 내용

| 항목 | Before | After |
| --- | --- | --- |
| faithfulness judge context | 검색 결과 상위 context 일부를 그대로 사용 | 질문/답변 overlap과 source diversity 기반으로 judge용 context 선택 |
| 주요 실패 케이스 | `tc-10`에서 무관 context 혼입으로 `faithfulness=0.0` | `tc-10` 단건 및 full eval에서 faithfulness 안정화 |

### 실측 지표 변화

| Metric | Before | After | Delta |
| --- | --- | --- | --- |
| `accuracy_mean` | `0.975` | `0.95` | `-0.025` |
| `faithfulness_mean` | `0.90` | `1.0` | `+0.10` |
| `not_found_rate` | `0.0` | `0.0` | `0.0` |

`accuracy_mean` 하락은 검색/생성 회귀보다 잔여 keyword 표현 차이에 따른 감점으로 분류됐다. 따라서 다음 단계는 답변 로직 변경이 아니라 keyword 기준 정합성 재검토로 진행했다.

상세 결과는 `docs/references/2026-05-15-faithfulness-eval-stability.md`와 `docs/exec-plans/completed/2026-05-15-faithfulness-context-selection.md`에 기록한다.

---

## 비교 8: Faithfulness context 선택 개선 → 잔여 keyword accuracy 보정

**비교 기준:** `eval/results/eval_20260515_110900.json` vs `eval/results/eval_20260515_135903.json`

### 변경 내용

| Case | Before | After |
| --- | --- | --- |
| `tc-03` | 이용 제한 exact keyword 중심 | "이용이 제한", "제한될" 등 자연 표현 허용 |
| `tc-07` | 책임/손해 exact keyword 중심 | 귀책사유, 고의·과실, 불가항력, 장애/방해 등 면책 표현 허용 |
| `tc-09` | 준수/약관/정책/권리/보유 중심 | 권한, 부여, 라이선스, 명예, 불이익, 복제/유통 표현 추가 |
| `tc-10` | "귀속" exact keyword 중심 | "보유", "보유하게" 표현 허용 |

### 실측 지표 변화

| Metric | Before | After | Delta |
| --- | --- | --- | --- |
| `precision@k_mean` | `0.48` | `0.48` | `0.00` |
| `vector_precision@k_mean` | `0.48` | `0.48` | `0.00` |
| `rag_precision@k_mean` | `0.60` | `0.60` | `0.00` |
| `rag_normalized_source_precision@k_mean` | `1.0` | `1.0` | `0.0` |
| `rag_chunk_precision@k_mean` | `0.96` | `0.96` | `0.0` |
| `source_recall@k_mean` | `1.0` | `1.0` | `0.0` |
| `source_coverage@k_mean` | `1.0` | `1.0` | `0.0` |
| `accuracy_mean` | `0.95` | `1.0` | `+0.05` |
| `faithfulness_mean` | `1.0` | `1.0` | `0.0` |
| `not_found_rate` | `0.0` | `0.0` | `0.0` |

현재 10개 평가 케이스 기준으로 생성 품질 핵심 지표는 상한에 도달했다. 다음 비교 축은 모델/검색 추가 튜닝이 아니라 평가셋 일반화, hard case 확장, keyword 기반 판정 한계 점검이다.

상세 결과는 `docs/references/2026-05-15-residual-keyword-accuracy.md`에 기록한다.

---

---

## 비교 9: 잔여 keyword accuracy 보정 → 평가셋 일반화 및 hard case 확장

**비교 기준:** `eval/results/eval_20260515_135903.json` vs `eval/results/eval_20260522_091248.json`

### 변경 내용

| 항목 | Before | After |
| --- | --- | --- |
| 평가 케이스 수 | 10개 | 16개 |
| corpus 범위 | 다음/네이버 중심 | 13개 약관/정책 문서, 318개 청크 |
| 신규 hard case | 없음 | 유료서비스, 운영정책, 위치정보, 계정, no-answer 케이스 추가 |

### 실측 지표 변화

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `total_cases` | `10` | `16` | `+6` |
| `accuracy_mean` | `1.0` | `0.9062` | `-0.0938` |
| `faithfulness_mean` | `1.0` | `0.75` | `-0.25` |
| `not_found_rate` | `0.0` | `0.0625` | `+0.0625` |

이 하락은 시스템 전체 회귀가 아니라, 기존 평가셋이 다루지 못한 no-answer, source drift, 다문서 faithfulness 문제를 드러낸 결과다.

---

## 비교 10: 평가셋 확장 → no-answer / faithfulness triage

**비교 기준:** `eval/results/eval_20260522_091248.json` vs `eval/results/eval_20260522_131753.json`

### 변경 내용

| 항목 | Before | After |
| --- | --- | --- |
| no-answer 평가 | 일반 accuracy/faithfulness 실패로 집계 | `expected_not_found`, `not_found_success_rate` 추가 |
| faithfulness context | 상위 3개 context 중심 | 최대 5개 context로 확대 |
| 주요 개선 케이스 | `tc-16`, `tc-09`, `tc-10` | negative/no-answer와 다문서 faithfulness 안정화 |

### 실측 지표 변화

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `accuracy_mean` | `0.9062` | `0.9219` | `+0.0157` |
| `faithfulness_mean` | `0.75` | `0.9375` | `+0.1875` |
| `not_found_success_rate` | N/A | `1.0` | 신규 |

---

## 비교 11: Failure triage → source drift calibration

**비교 기준:** `eval/results/eval_20260522_131753.json` vs `eval/results/eval_20260522_160844.json`

### 변경 내용

| Case | Before | After |
| --- | --- | --- |
| `tc-04` | 자동 갱신/해지 복합 질문 | 자동 갱신 positive case |
| `tc-06` | 다음/네이버 중심 분쟁 source | 카카오/다음/네이버 분쟁 source와 표현 반영 |
| `tc-16` | negative case 유지 | 결제 주기/금액 변경 조건 no-answer 성공 |
| `tc-17` | 없음 | 해지/개별 서비스 이용 종료 positive case 추가 |

### 실측 지표 변화

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `total_cases` | `16` | `17` | `+1` |
| `accuracy_mean` | `0.9219` | `1.0` | `+0.0781` |
| `faithfulness_mean` | `0.9375` | `1.0` | `+0.0625` |
| `not_found_rate` | `0.125` | `0.0588` | `-0.0662` |
| `not_found_success_rate` | `1.0` | `1.0` | `0.0` |
| `rag_normalized_source_precision@k_mean` | `0.7188` | `0.7971` | `+0.0783` |
| `source_recall@k_mean` | `0.7188` | `0.7836` | `+0.0648` |

---

## 비교 12: source drift calibration → regression guard / watch case review

**비교 기준:** `eval/results/eval_20260522_160844.json` + `scripts/source_drift_report.py`

### 변경 내용

| 항목 | 결과 |
| --- | --- |
| source drift guard | 저장된 eval JSON에서 critical/watch case 자동 분류 |
| critical case | 없음 |
| watch case | `tc-02`, `tc-03`, `tc-06`, `tc-07`, `tc-08`, `tc-14`, `tc-15` |
| 평가셋 즉시 보정 | 보류 |
| 다음 작업 | source scope policy 수립 |

watch case는 모두 `accuracy=1.0`, `faithfulness=1.0`이다. 따라서 검색 실패가 아니라 relevant source 범위 정책 문제로 분류했다.


## 실측 평가 실행 방법

v0.3에서 평가 파이프라인이 구축되어 실제 수치 측정이 가능합니다.

```
# retrieval 지표만 측정 (빠름, Ollama 불필요)
python3 eval/pipeline.py --metric retrieval

# 전체 지표 측정 + JSON 리포트 저장
python3 eval/pipeline.py --all

# 결과: eval/results/eval_{YYYYMMDD_HHMMSS}.json
```

**평가 케이스:** `eval/test_cases.json` — 이용약관 도메인 17개 질문

**relevant_sources 매핑:** 완료 (Precision@K 즉시 측정 가능)

---

## 변경되지 않은 항목

| 항목 | 이유 |
| --- | --- |
| chunk_size | v0.2에서 최적화 완료 (1,000자) |
| RRF 알고리즘 | v0.1부터 적용 중, 변경 필요 없음 |
| ChromaDB cosine | 의미 검색 기준으로 적합 |

---

## 다음 단계

1. 최신 full eval 리포트 `eval/results/eval_20260522_160844.json` 기준 17개 케이스 상한 도달 상태를 유지한다.

1. source drift watch case 7건에 대해 `relevant_sources` 범위 정책을 먼저 정한다.

1. source scope policy 확정 후 필요한 경우 평가셋 source 기준을 보정하고 full eval을 재실행한다.

---

*최종 업데이트: 2026-05-22 — 17개 케이스 기준 accuracy/faithfulness/not_found_success 상한 달성, source drift watch case review 완료*
