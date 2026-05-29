# Evaluation Model And Tuning Policy

## Purpose

운영 모델과 평가 기준 모델을 분리해 RAG 성능 비교가 모델 변경에 흔들리지 않도록 한다.

## Model Roles

- 운영 기본 모델: `gemma4:26b`
  - FastAPI, Streamlit, CLI 기본 응답 모델이다.
  - Ubuntu 운영 서버에서 `/health` 기준 정상 응답을 확인했다.
- 평가 기준 모델: `gemma3:12b`
  - full eval과 튜닝 비교의 기준선 모델이다.
  - 기존 평가 리포트와 비교 가능성을 유지하기 위해 평가 실행 시 명시적으로 고정한다.

운영 모델과 평가 기준 모델은 다를 수 있다. 성능 비교는 반드시 같은 평가 기준 모델끼리만 수행한다.

## Required Eval Metadata

새 평가 리포트는 최소한 아래 값을 확인해야 한다.

- `summary.llm_model`
- `summary.top_k`
- `summary.total_cases`
- `summary.metrics_evaluated`
- Chroma collection count
- 실행 시점과 리포트 파일명

`eval/pipeline.py`는 저장 리포트의 summary에 `llm_model`과 `top_k`를 기록한다.

## Standard Eval Command

평가 기준 모델을 명시해 실행한다.

```bash
python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

API 서버를 통해 수동 검증할 때도 평가 전 모델을 확인한다.

```bash
curl -X PUT http://localhost:8000/model \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma3:12b"}'

curl http://localhost:8000/health
```

## Tuning Order

한 번에 하나의 변경만 적용하고, 변경 전후 리포트를 같은 모델과 같은 평가셋으로 비교한다.

1. 검색 파라미터
   - `top_k`
   - vector/BM25/RRF 조합
   - source diversity
   - Cross-Encoder reranker 사용 여부
2. 프롬프트
   - 답변 형식
   - 근거 부족 답변 정책
   - 다문서 충돌 처리
   - 출처 언급 방식
3. 평가셋
   - expected keyword OR group
   - relevant source 범위
   - negative/no-answer case
   - hard case 추가
4. 운영 안정성
   - GPU/CPU 메모리
   - timeout
   - 동시 요청
   - systemd 재시작 정책

## Stability Criteria

이용약관 RAG 평가셋 기준 안정화 판단 기준은 아래와 같다.

- `accuracy_mean >= 0.95`
- `faithfulness_mean >= 0.95`
- `not_found_success_rate = 1.0`
- source drift critical case 없음
- watch case 없음 또는 문서화된 예외만 존재
- 같은 평가 기준 모델로 2회 이상 결과 변동이 설명 가능함

## Notes

- `gemma4:26b` 운영 모델의 품질을 평가하려면 별도 리포트를 생성하되, `gemma3:12b` 기준선과 직접 우열 비교하지 않는다.
- 운영 모델 변경은 배포 정책이고, RAG 튜닝 결과 비교는 평가 기준 모델 고정 상태에서 수행한다.
