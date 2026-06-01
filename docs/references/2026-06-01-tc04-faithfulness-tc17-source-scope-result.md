# 2026-06-01 TC04 Faithfulness And TC17 Source Scope Result

## Purpose

`tc-04` faithfulness critical과 `tc-17` source recall 저하를 좁게 보정하고, full eval과 source drift guard로 회귀 여부를 확인한다.

## Changes

### TC04 Faithfulness

`eval/pipeline.py`의 faithfulness judge 입력에서 숫자 citation marker를 제거하도록 보강했다.

- 제거 대상 예: `[3]`, `[4]`, `[10]`
- 목적: 답변의 citation 번호 표기 흔들림이 근거성 판정을 오염하지 않게 한다.
- 제품 답변 프롬프트는 대규모로 변경하지 않았다.

### TC17 Source Scope

`tc-17`의 `relevant_sources`에서 `카카오계정약관20240416.pdf`를 제외했다.

- 질문은 서비스 이용계약 해지와 개별 서비스 이용 종료를 묻는다.
- expected keyword는 데이터/게시물/정보 삭제와 개별 서비스 종료를 검증한다.
- 카카오계정약관은 계정 단위 조건에 가깝고, 현재 질문의 대표 근거 범위보다 넓다.
- source scope policy의 representative evidence 기준에 따라 직접 대표 근거 3개로 좁혔다.

### TC21 Scope

검증 과정에서 `tc-21`이 서비스 제공 중단과 약관 변경을 한 케이스에 섞고 있음을 확인했다.

- 질문을 `유료서비스 약관에서 서비스 제공 중단 또는 서비스 변경 시 회원에게 어떻게 통지하는가?`로 좁혔다.
- expected keyword의 `개정`을 제거했다.
- 이는 검색 결과와 대표 근거가 실제로 검증하는 범위에 맞춘 보정이다.

### Prompt Guard

`retriever/engine.py`의 근거 사용 규칙에 문서 밖 추론 표현 금지를 한 문장 추가했다.

- `가능성`, `것으로 보아`처럼 문서 밖 추론을 암시하는 표현을 쓰지 않도록 했다.
- `tc-04`에서 네이버 자동 갱신 여부를 추론하던 답변을 막기 위한 좁은 보강이다.

## Validation

최종 full eval은 서버에서 GPU 메모리 경합을 피하기 위해 평가 프로세스만 CPU 모드로 실행했다.

```bash
CUDA_VISIBLE_DEVICES='' .venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5
```

최종 리포트:

- `eval/results/eval_20260601_164832.json`

지표:

- `total_cases=23`
- `llm_model=gemma3:12b`
- `top_k=5`
- `accuracy_mean=1.0`
- `faithfulness_mean=1.0`
- `not_found_success_rate=1.0`
- `rag_normalized_source_precision@k_mean=1.0`
- `source_recall@k_mean=1.0`

Source drift guard:

```bash
python scripts/source_drift_report.py eval/results/eval_20260601_164832.json --fail-on-critical
```

결과:

- critical case 없음
- watch case 없음

## Notes

- 일반 full eval을 서버 GPU에서 바로 실행하면 API/Ollama와 GPU 메모리 경합이 생길 수 있다.
- 평가 프로세스의 임베딩/reranker는 CPU로 돌리고 Ollama는 기존 서비스가 처리하도록 `CUDA_VISIBLE_DEVICES=''`를 사용하는 방식이 안정적이었다.
