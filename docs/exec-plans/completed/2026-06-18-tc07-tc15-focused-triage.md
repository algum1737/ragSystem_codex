# TC07 TC15 Focused Triage Plan

## Goal

`gemma3:12b + top_k=5` 최신 기준선에서 accuracy `0.75`로 남은 `tc-07`, `tc-15`를 분석해 다음 개선 방향을 하나로 좁힌다.

## Scope

- `tc-07`, `tc-15`의 최신 답변, expected keyword group, retrieved sources 비교
- deterministic `answer_accuracy` rule과 실제 답변 품질의 괴리 확인
- 원인을 `answer wording`, `eval rule`, `prompt`, `retrieval/source`, `model/runtime`으로 분류
- 후속 작업 후보 1개 선정

## Out Of Scope

- `eval/test_cases.json` 변경
- `eval/pipeline.py` 변경
- `retriever/engine.py`, prompt template 변경
- full eval 재실행
- 운영 서버 배포

## Assumptions

- 최신 기준선 리포트는 `eval/results/eval_20260618_113500.json`이다.
- 두 케이스 모두 `source_recall_at_k=1.0`, `rag_normalized_source_precision_at_k=1.0`, `faithfulness=1.0`이므로 검색 실패나 hallucination을 1차 원인으로 보지 않는다.
- 실제 답변이 제품 관점에서 충분하면 eval rule 보정 후보로 분류한다.
- 질문의 핵심 표지어를 답변에 유지하는 것이 사용자 품질에도 명확히 이득이면 prompt/answer wording 후보로 분류한다.

## Pre-flight checks

- [x] `git status --short --branch`
- [x] `bash scripts/validate-docs.sh`
- [x] `eval/results/eval_20260618_113500.json` 존재 확인
- [x] `docs/references/2026-06-18-gemma3-quality-baseline-refresh-result.md` 확인

## Steps

1. `eval/test_cases.json`에서 `tc-07`, `tc-15` expected keyword group과 relevant sources를 추출한다.
2. 최신 eval report에서 두 케이스의 answer, accuracy, faithfulness, retrieved sources를 추출한다.
3. `eval/pipeline.py`의 `answer_accuracy` deterministic matching rule을 확인한다.
4. 각 expected keyword group별 match/miss를 표로 정리한다.
5. miss가 실제 품질 결함인지 표현/판정 결함인지 판단한다.
6. 후속 후보를 하나로 좁히고 결과 문서에 기록한다.

## Task Breakdown

- [x] Case extraction
  - 명령:
    ```bash
    jq '.cases[] | select(.id=="tc-07" or .id=="tc-15")' eval/test_cases.json
    jq '.cases[] | select(.id=="tc-07" or .id=="tc-15")' eval/results/eval_20260618_113500.json
    ```
  - 기대 결과:
    - expected groups와 최신 answer를 같은 기준으로 비교 가능
- [x] Rule inspection
  - 명령:
    ```bash
    sed -n '175,195p' eval/pipeline.py
    ```
  - 기대 결과:
    - list group은 OR matching, top-level groups는 평균 점수 산정임을 확인
- [x] Match table
  - 산출물:
    - `docs/references/2026-06-18-tc07-tc15-focused-triage-result.md`
  - 기대 결과:
    - group별 matched/missing 근거가 명시됨
- [x] Decision
  - 기대 결과:
    - 다음 작업을 `eval rule 보정`, `prompt wording 보강`, 또는 `no change` 중 하나로 제한

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py`

## Manual/Runtime QA

- `tc-07`, `tc-15` 답변이 질문에 직접 답하는지 사람이 확인한다.
- missed keyword가 실제 누락인지 동의 표현인지 확인한다.
- source drift report의 missing/unexpected source가 없는지 확인한다.

## Skipped/Not Run

- full eval은 실행하지 않는다. 이 작업은 최신 full eval 결과의 focused triage다.
- 서버 smoke는 실행하지 않는다. 최신 서버 eval report를 기준으로 분석한다.
- 코드/평가셋/prompt 변경은 하지 않는다.

## Open Work

- 후속 후보는 `tc-07`, `tc-15` eval rule calibration이다.
- 구현 변경이므로 사용자 승인 후 별도 plan으로 진행한다.

## Completion

- 완료.
- 결과 문서는 `docs/references/2026-06-18-tc07-tc15-focused-triage-result.md`다.
- `tc-07`, `tc-15` 모두 retrieval/source 문제가 아니라 deterministic keyword rule의 동의 표현 허용 부족으로 분류했다.
- 후속 후보는 `eval/test_cases.json`의 expected keyword OR group을 좁게 보정하는 작업이다.

## Validation Result

- 통과: `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: `eval/results/eval_20260618_113500.json` 확인
- 통과: `eval/test_cases.json`의 `tc-07`, `tc-15` expected keyword 확인
- 통과: `eval/pipeline.py`의 `answer_accuracy` rule 확인
  - list group은 OR matching
  - top-level group 기준 평균 점수 산정
- 통과: keyword match table 작성
  - `tc-07`: `면책` group만 MISS
  - `tc-15`: `예외`/`불가능`/`부득이`/`긴급` group만 MISS
