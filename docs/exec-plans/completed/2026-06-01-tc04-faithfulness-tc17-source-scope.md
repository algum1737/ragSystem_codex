# TC04 Faithfulness And TC17 Source Scope Plan

## Goal

잔여 critical/watch 후보인 `tc-04` faithfulness 실패와 `tc-17` source scope 불일치를 좁게 보정한다.

## Scope

- `tc-04` faithfulness judge 입력 context와 답변 citation 표현 진단
- `tc-04`에 대한 좁은 보정 후보 선정
- `tc-17` relevant source 범위 재검토
- 필요 시 평가셋 source scope 또는 평가 하네스 보정
- 보정 후 full eval과 source drift guard 실행

## Out Of Scope

- 운영 모델 변경
- 전역 프롬프트 대규모 변경
- 검색 파라미터 전체 튜닝
- GPU/서버 런타임 변경

## Assumptions

- `eval/results/eval_20260529_173928.json`이 현재 채택 기준 리포트다.
- 2026-06-01 전역 출처 프롬프트 실험은 full eval 회귀가 있어 채택하지 않는다.
- `tc-17`은 답변 품질 문제가 아니라 source scope 문제일 가능성이 높다.

## Pre-flight checks

- `git status --short --branch` 확인
- `eval/results/eval_20260529_173928.json` 확인
- `docs/references/2026-06-01-residual-tuning-case-review.md` 확인

## Steps

1. `tc-04` faithfulness judge prompt와 selected contexts를 재현한다.
2. `tc-04` 보정 후보를 전역 회귀가 적은 방식으로 좁힌다.
3. `tc-17` relevant source 범위를 source scope policy 기준으로 재검토한다.
4. 필요한 최소 변경만 적용한다.
5. full eval과 source drift guard로 회귀 여부를 확인한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py`
- `.venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5`
- `.venv/bin/python scripts/source_drift_report.py <latest-report> --fail-on-critical`

## Manual/Runtime QA

- `tc-04`, `tc-17` 답변과 검색 source를 사람이 검토한다.

## Skipped/Not Run

- GPU 모드 full eval 재실행은 서버 GPU 메모리 경합으로 실패했다. 최종 검증은 `CUDA_VISIBLE_DEVICES=''`로 평가 프로세스만 CPU 모드로 실행했다.

## Completion

- `tc-04` faithfulness judge 입력에서 숫자 citation marker를 제거하도록 보강했다.
- `tc-17` relevant source를 representative evidence 기준에 맞춰 3개 문서로 좁혔다.
- 검증 과정에서 `tc-21` 질문이 서비스 변경과 약관 개정을 섞고 있어 서비스 제공 중단/서비스 변경 범위로 좁혔다.
- `retriever/engine.py`에 문서 밖 추론 표현 금지 규칙을 한 문장 추가했다.
- 최종 리포트 `eval/results/eval_20260601_164832.json`을 저장했다.
- 결과 문서 `docs/references/2026-06-01-tc04-faithfulness-tc17-source-scope-result.md`를 추가했다.
- 다음 active plan으로 `docs/exec-plans/active/2026-06-01-observability-langfuse-review.md`를 생성했다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py`
- 통과: `CUDA_VISIBLE_DEVICES='' .venv/bin/python eval/pipeline.py --all --model gemma3:12b --top-k 5`
  - `accuracy_mean=1.0`
  - `faithfulness_mean=1.0`
  - `not_found_success_rate=1.0`
  - `rag_normalized_source_precision=1.0`
  - `source_recall=1.0`
- 통과: `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260601_164832.json --fail-on-critical`
  - critical case 없음
  - watch case 없음

## Open Work

- 없음.
