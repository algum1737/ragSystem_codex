# Performance Tuning Baseline Plan

## Goal

성능 튜닝을 시작하기 전에 같은 평가 기준 모델, 같은 평가셋, 같은 top_k 조건으로 기준선을 고정하고 1차 튜닝 후보를 결정한다.

## Scope

- 평가 기준 모델 `gemma3:12b`로 full eval 기준선 실행
- 최신 리포트의 retrieval, accuracy, faithfulness, no-answer 지표 확인
- 1차 튜닝 후보 결정
- negative/no-answer 탐지 보정이 1차 병목이면 좁게 구현
- 결과를 handoff와 참조 문서에 기록

## Out Of Scope

- 운영 기본 모델 변경
- GPU 드라이버 또는 서버 런타임 변경
- 여러 튜닝 변경을 동시에 적용

## Assumptions

- 운영 기본 모델은 `gemma4:26b`로 유지한다.
- 튜닝 비교 기준 모델은 `gemma3:12b`다.
- 성능 비교는 동일 평가셋과 동일 `top_k=5` 기준으로만 판단한다.

## Pre-flight checks

- `git status --short --branch` 확인
- active plan 존재 확인
- Ollama와 `gemma3:12b` 사용 가능 여부 확인
- Chroma collection count 확인

## Steps

1. 기준선 full eval을 실행한다.
2. 결과 리포트의 summary와 실패 케이스를 확인한다.
3. 검색 지표와 생성 지표 중 먼저 튜닝할 병목을 결정한다.
4. 기준선상 1차 병목이 no-answer 탐지라면 평가 탐지식을 보강한다.
5. 동일 조건 full eval을 재실행해 안정화 기준 충족 여부를 확인한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py`
- `.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5`

## Manual/Runtime QA

- 기준선 리포트에서 `summary.llm_model=gemma3:12b`, `summary.top_k=5` 확인
- 주요 지표와 실패 케이스를 사람이 검토한다.

## Skipped/Not Run

- 로컬 Ollama는 기동되어 있지 않아 full eval은 Ubuntu 서버에서 실행했다.

## Completion

- 서버 기준 `gemma3:12b`, `top_k=5`, Chroma count 318 조건으로 튜닝 전 full eval을 실행했다.
- 기준선 리포트 `eval/results/eval_20260529_172801.json`을 저장했다.
- 1차 병목을 검색 파라미터가 아니라 no-answer 탐지 보정으로 결정했다.
- `eval/pipeline.py`의 no-answer 탐지식을 좁게 보강했다.
- 보정 후 full eval 리포트 `eval/results/eval_20260529_173928.json`을 저장했다.
- 결과 문서 `docs/references/2026-05-29-performance-tuning-baseline-result.md`를 추가했다.
- 다음 active plan으로 `docs/exec-plans/active/2026-05-29-residual-tuning-case-review.md`를 생성했다.

## Validation Result

- 통과: `git status --short --branch`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py`
- 통과: no-answer 탐지식 단위 확인
- 통과: 서버 full eval before `eval/results/eval_20260529_172801.json`
  - `accuracy_mean=0.9565`, `faithfulness_mean=0.913`, `not_found_success_rate=0.0`
- 통과: 서버 full eval after `eval/results/eval_20260529_173928.json`
  - `accuracy_mean=1.0`, `faithfulness_mean=0.9565`, `not_found_success_rate=1.0`
- 실패: `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260529_173928.json --fail-on-critical`
  - `tc-04` faithfulness 0.0이 critical case로 분류되어 다음 active plan에서 리뷰한다.

## Open Work

- 없음.
