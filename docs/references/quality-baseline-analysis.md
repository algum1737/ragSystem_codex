# Quality Baseline Analysis

분석 기준 리포트: `eval/results/eval_20260513_100727.json`

## Current Metrics

- 평가 케이스: 10개
- `precision@k_mean`: `0.48`
- `accuracy_mean`: `0.525`
- `faithfulness_mean`: `0.8`
- 로컬 Chroma 상태: 89 chunks
- source 분포:
  - `다음 이용약관.txt`: 32 chunks
  - `네이버 이용약관.txt`: 31 chunks
  - `다음 위치기반서비스 이용약관.txt`: 16 chunks
  - `네이버 위치기반서비스 이용약관.txt`: 10 chunks

## Key Finding

현재 retrieval 평가와 실제 답변 생성 경로가 다르다.

- `eval/pipeline.py`의 `precision@k`는 `VectorStore.similarity_search()`만 사용한다.
- 실제 답변 생성은 `RAGEngine.query()`에서 vector search, BM25, RRF, Cross-Encoder reranking을 조합한다.
- 따라서 현재 `precision@k_mean=0.48`은 실제 RAG 생성 경로의 검색 품질을 직접 대표하지 않는다.

## Case Classification

| Case | Precision | Accuracy | Faithfulness | Classification |
| --- | ---: | ---: | ---: | --- |
| `tc-01` | 0.4 | 0.0 | 0.0 | 관련 source는 일부 검색됐지만 답변이 `찾을 수 없음`으로 실패 |
| `tc-02` | 0.4 | 1.0 | 1.0 | 답변은 성공, source 중복 때문에 precision 낮음 |
| `tc-03` | 0.4 | 0.5 | 1.0 | 답변은 근거 기반이나 기대 키워드 일부 누락 |
| `tc-04` | 0.6 | 0.25 | 0.0 | 문서에 직접 근거가 약한 질문으로 보이며 답변도 `찾을 수 없음` |
| `tc-05` | 0.4 | 0.75 | 1.0 | 답변은 양호, precision은 중복/문서 단위 기준 영향 |
| `tc-06` | 0.6 | 0.25 | 1.0 | 근거는 있으나 기대 키워드 기준과 답변 표현 불일치 |
| `tc-07` | 0.6 | 0.75 | 1.0 | 답변 양호 |
| `tc-08` | 0.8 | 0.5 | 1.0 | 검색 양호, 답변 키워드 일부 누락 |
| `tc-09` | 0.2 | 0.5 | 1.0 | 일반약관 필터 상태에서도 특정 source 편중 |
| `tc-10` | 0.4 | 0.75 | 1.0 | 답변 양호, source 중복 영향 |

## Failure Modes

1. 평가 경로 불일치
   - 실제 RAG는 hybrid + rerank를 쓰지만 retrieval metric은 vector-only다.

2. source 단위 precision 한계
   - 동일 source에서 여러 chunk가 검색되면 정답 source를 포함해도 `precision@5`가 낮게 나온다.
   - 현재 케이스 중 다수는 unique relevant source coverage가 나쁘지 않다.

3. keyword accuracy 한계
   - 답변이 의미상 맞아도 기대 키워드 문자열이 없으면 점수가 낮다.
   - 예: `tc-06`은 분쟁 절차를 설명하지만 `중재`, `관할` 같은 기대 키워드와 표현이 맞지 않아 낮다.

4. 평가 질문/문서 근거 불일치 가능성
   - `tc-01`, `tc-04`는 검색된 source가 있어도 답변이 `찾을 수 없음`으로 끝난다.
   - 실제 인제스천 문서에 환불, 자동갱신, 구독 취소 근거가 약할 가능성이 있다.

## First Improvement Experiment

첫 구현 실험은 검색 파라미터 튜닝이 아니라 평가 하네스 정렬이어야 한다.

목표:
- `eval/pipeline.py`에 실제 `RAGEngine` 검색 후보 경로를 측정하는 retrieval metric을 추가한다.
- vector-only metric은 baseline으로 남기되 이름을 명확히 분리한다.
- source 중복 영향을 줄이기 위해 unique source coverage 지표를 추가한다.

권장 지표:
- `vector_precision@k`: 기존 vector-only precision
- `rag_precision@k`: `RAGEngine`의 최종 source 기준 precision
- `source_coverage@k`: relevant source 중 검색된 unique source 비율
- `not_found_rate`: 답변이 `찾을 수 없음`으로 끝나는 비율

성공 기준:
- 기존 리포트와 비교 가능한 형태로 새 리포트가 저장된다.
- `rag_precision@k`와 `source_coverage@k`가 케이스별로 출력된다.
- 검색 튜닝 전에도 평가 경로 불일치가 해소된다.

재평가 명령:

```bash
.venv/bin/python eval/pipeline.py --all
```

주의:
- 이 실험은 품질을 직접 올리는 작업이 아니라 품질 개선 판단의 계측 오차를 줄이는 작업이다.
- 이후에 청킹, BM25/RRF 가중치, reranker 후보 수, 프롬프트를 순서대로 실험한다.
