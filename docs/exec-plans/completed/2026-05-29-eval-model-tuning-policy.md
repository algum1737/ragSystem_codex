# Eval Model Tuning Policy Plan

## Goal

운영 모델과 평가 기준 모델을 분리하고, 성능 안정화와 튜닝을 같은 기준선에서 반복할 수 있도록 절차와 리포트 메타데이터를 정리한다.

## Scope

- 평가 기준 모델을 `gemma3:12b`로 명시
- 운영 기본 모델 `gemma4:26b`와 평가 기준 모델의 역할 분리
- eval 리포트 summary에 모델명과 `top_k` 기록
- 튜닝 순서와 안정화 판단 기준 문서화

## Out Of Scope

- full eval 재실행
- 신규 튜닝 실험 수행
- 운영 모델 교체

## Assumptions

- 운영 응답 기본 모델은 `gemma4:26b`다.
- 회귀 비교와 튜닝 기준 모델은 기존 평가 이력을 유지하기 위해 `gemma3:12b`로 고정한다.
- 성능 비교는 같은 모델, 같은 평가셋, 같은 `top_k` 기준으로만 수행한다.

## Pre-flight checks

- `eval/pipeline.py`의 `--model` 기본값 확인
- 최신 eval 리포트와 운영 모델 상태 확인
- 문서 인덱스에 튜닝 정책 문서 추가 여부 확인

## Steps

1. eval 리포트 summary에 `llm_model`과 `top_k`를 기록한다.
2. 운영 모델과 평가 기준 모델 분리 정책을 참조 문서로 작성한다.
3. 문서 인덱스, 계획, handoff를 갱신한다.
4. 문서 검증과 Python compile을 실행한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py`

## Manual/Runtime QA

- full eval은 실행하지 않고, 정책 문서와 리포트 메타데이터 변경을 코드/문서 검증으로 확인한다.

## Skipped/Not Run

- full eval 재실행은 수행하지 않는다. 이번 작업은 튜닝 기준선 절차와 리포트 메타데이터 정리다.

## Completion

- `eval/pipeline.py` 저장 리포트 summary에 `llm_model`과 `top_k`를 기록하도록 보강했다.
- `docs/references/2026-05-29-eval-model-tuning-policy.md`를 추가해 운영 모델과 평가 기준 모델을 분리했다.
- 표준 full eval 명령을 `python eval/pipeline.py --all --model gemma3:12b --top-k 5`로 문서화했다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py`
- 통과: `.venv/bin/python eval/pipeline.py --metric retrieval --model gemma3:12b --top-k 5`
  - `llm_model=gemma3:12b`, `top_k=5` 출력 확인
  - `rag_normalized_source_precision=0.9891`, `source_recall=0.9891`

## Open Work

- 없음.
