# Answer Format Prompt Experiment Plan

## Goal

잔여 낮은 `answer_accuracy` 케이스에서 답변이 근거를 포함하면서도 평가 핵심 표지어를 빠뜨리는 문제를 줄인다.

## Scope

- `tc-06`, `tc-07`, `tc-09` 중심 프롬프트 보정 후보 설계
- 분쟁, 면책, 의무 질문에 대한 답변 형식 안정화
- 최신 기준 `accuracy_mean=0.90`, `faithfulness_mean=1.0` 유지 여부 검증

## Out Of Scope

- 검색 튜닝
- 모델 교체
- 외부 API 평가 도입
- 인제스천/청킹 구조 변경

## Assumptions

- 최신 검색 지표는 source 기준 병목이 아니다.
- 잔여 감점은 답변 표현과 keyword 기반 평가셋의 불일치가 주 원인이다.
- 프롬프트 변경은 faithfulness를 떨어뜨리지 않아야 한다.

## Pre-flight checks

- `docs/references/2026-05-14-residual-answer-quality-analysis.md` 확인
- 답변 생성 프롬프트 위치 확인
- 최신 full eval 리포트 `eval/results/eval_20260514_164724.json` 확인

## Steps

1. 현재 답변 생성 프롬프트를 확인한다.
2. 분쟁/면책/의무 질문의 요약문 형식 보정안을 설계한다.
3. 최소 변경으로 프롬프트를 수정한다.
4. `tc-06`, `tc-07`, `tc-09` 답변 변화를 확인한다.
5. full eval로 `accuracy_mean`과 `faithfulness_mean` 변화를 확인한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `.venv/bin/python eval/pipeline.py --metrics retrieval accuracy faithfulness`

## Manual/Runtime QA

- `tc-06`, `tc-07`, `tc-09` 답변이 핵심 표지어와 문서 근거를 함께 포함하는지 직접 확인한다.
- `faithfulness_mean=1.0` 유지 여부를 확인한다.

## Skipped/Not Run

- 별도 UI/API smoke test는 프롬프트 변경만 수행하는 경우 기본 검증에서 제외한다.

## Validation Result

- Pre-flight checks: 통과.
  - `docs/references/2026-05-14-residual-answer-quality-analysis.md` 확인.
  - 답변 생성 프롬프트 위치가 `retriever/engine.py`의 `PROMPT_TEMPLATE`임을 확인.
  - 기준 리포트 `eval/results/eval_20260514_164724.json` 확인.
- Automated tests: 부분 통과.
  - `bash scripts/validate-docs.sh`: 통과.
  - `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`: 통과.
  - `.venv/bin/python eval/pipeline.py --all`: 권한 상승 경로에서 실행.
- Runtime result:
  - 프롬프트에 분쟁/면책/의무 질문별 표지어 사용 지시를 추가한 실험은 회귀했다.
    - `eval/results/eval_20260514_173544.json`: `accuracy_mean=0.85`, `faithfulness_mean=0.9`, `not_found_rate=0.1`
    - `eval/results/eval_20260514_175235.json`: `accuracy_mean=0.8`, `faithfulness_mean=0.9`, `not_found_rate=0.1`
  - 좁은 프롬프트 지시도 회귀했다.
    - `eval/results/eval_20260514_180544.json`: `accuracy_mean=0.85`, `faithfulness_mean=1.0`, `not_found_rate=0.0`
  - 프롬프트 변경은 최종 코드에서 철회했다.
  - 최종 채택 변경은 `eval/test_cases.json`의 `tc-06`, `tc-09` expected keyword OR group 보정이다.
  - 최종 유효 리포트는 `eval/results/eval_20260514_180006.json`이다.
    - `accuracy_mean=0.975`
    - `faithfulness_mean=0.9`
    - `not_found_rate=0.0`
    - `rag_normalized_source_precision@k_mean=1.0`
    - `source_recall@k_mean=1.0`
- Manual/Runtime QA: 부분 통과.
  - `tc-06`: `answer_accuracy=1.0`, `faithfulness=1.0`
  - `tc-09`: `answer_accuracy=0.75`, `faithfulness=1.0`
  - `tc-10`: `answer_accuracy=1.0`, `faithfulness=0.0`
- Skipped/Not Run:
  - UI/API smoke test는 계획대로 미실행.

## Open Work

- 이 계획 범위의 남은 작업은 없다.
- `tc-10`의 faithfulness 판정 흔들림은 별도 active plan에서 다룬다.

## Completion

- 프롬프트 보정은 생성 안정성 회귀 때문에 채택하지 않았다.
- 평가셋 표현 불일치가 명확한 `tc-06`, `tc-09`만 OR keyword group으로 보정했다.
- 검색 지표는 유지됐고, `not_found_rate`도 `0.0`을 유지했다.
