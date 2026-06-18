# TC04 Faithfulness Triage Plan

## Goal

`tc-04` 자동 갱신 케이스가 최신 full eval과 단일 재실행에서 `faithfulness=0.0`으로 실패한 원인을 systematic-debugging 방식으로 분류한다.

## Scope

- 최신 full eval answer 확인
- 단일 재실행 answer 확인
- retrieved context 확인
- faithfulness judge prompt와 입력 answer 변형 실험
- 원인을 `answer wording`, `faithfulness judge`, `eval rule`, `prompt`, `retrieval/source` 중 하나로 분류
- 후속 수정 후보 제안

## Out Of Scope

- prompt 변경
- eval rule 변경
- faithfulness scoring 함수 변경
- retrieval, reranker, chunking 변경
- full eval 재실행
- 운영 배포

## Assumptions

- `tc-04`는 이번 `tc-07`, `tc-15` expected keyword calibration 대상이 아니다.
- `tc-04`의 source recall과 RAG normalized precision은 `1.0`이다.
- 단일 재실행에서도 `faithfulness=0.0`이 재현됐으므로 단순 1회 stochastic judge 흔들림만으로 처리하지 않는다.

## Pre-flight checks

- [x] `git status --short --branch`
- [x] `bash scripts/validate-docs.sh`
- [x] 최신 full eval report 확인: `eval/results/eval_20260618_132509.json`
- [x] 단일 재실행 report 확인: `/opt/ragSystem_codex/eval/results/eval_tc04_check_20260618_132648.json`

## Steps

1. `tc-04` 최신 full eval answer와 단일 재실행 answer를 비교한다.
2. RAG retrieved context를 확인해 답변의 각 주장과 매칭한다.
3. faithfulness judge prompt를 재현한다.
4. answer 변형 실험을 수행한다.
   - 원본 답변
   - `문서에서 확인되지 않는 내용` bullet 제거
   - 확인된 positive 근거만 남긴 답변
   - partial no-answer 문장만 남긴 답변
5. 어떤 문장/구조가 `NO`를 유발하는지 분류한다.
6. 결과 문서와 후속 후보를 작성한다.

## Task Breakdown

- [x] Report comparison
  - 명령:
    ```bash
    jq '.cases[] | select(.id=="tc-04")' eval/results/eval_20260618_132509.json
    ```
  - 기대 결과:
    - `answer_accuracy=1.0`
    - `faithfulness=0.0`
    - source metrics `1.0`
- [x] Context inspection
  - 서버에서 `RAGEvaluator._rag_retrieval_query()`로 `tc-04` context 확인
  - 기대 결과:
    - 네이버 사용기간/소멸 근거
    - 카카오 무료체험/정기결제/고지/중단/해지 근거
- [x] Judge variant test
  - 서버에서 `RAGEvaluator.faithfulness()`로 answer variants 판정
  - 기대 결과:
    - failure-triggering phrase 또는 구조 식별
- [x] Result docs
  - 작성 경로:
    - `docs/references/2026-06-18-tc04-faithfulness-triage-result.md`

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py`

## Manual/Runtime QA

- `tc-04` answer와 retrieved context를 사람이 비교한다.
- judge variant 결과가 원인 분류와 일관되는지 확인한다.

## Skipped/Not Run

- full eval은 실행하지 않는다. 이미 `eval/results/eval_20260618_132509.json`에서 실패를 확인했다.
- 코드/평가셋/prompt 변경은 하지 않는다.

## Open Work

- 후속 후보는 `tc-04` answer wording focused fix다.
- 구현 변경이므로 별도 active plan과 사용자 승인으로 진행한다.

## Completion

- 완료.
- 결과 문서는 `docs/references/2026-06-18-tc04-faithfulness-triage-result.md`다.
- 원인은 `확인된 내용`과 `문서에서 확인되지 않는 내용`이 섞인 partial answer 구조로 분류했다.
- primary classification은 `answer wording`, secondary classification은 `faithfulness judge`다.

## Validation Result

- 통과: `git status --short --branch`
  - 시작 시 `main...origin/main`, clean.
- 통과: `bash scripts/validate-docs.sh`
  - `template docs validation passed`
- 통과: full eval report 확인
  - `tc-04 answer_accuracy=1.0`
  - `tc-04 faithfulness=0.0`
  - `tc-04 source_recall_at_k=1.0`
  - `tc-04 rag_normalized_source_precision_at_k=1.0`
- 통과: retrieved context 확인
  - 네이버 사용기간/소멸 근거 포함
  - 카카오 무료체험/정기결제/고지/중단/해지 근거 포함
- 통과: judge variant test
  - full eval answer: `[1.0, 0.0, 0.0]`
  - single-case answer: `[0.0, 1.0, 0.0]`
  - positive-only answer: `[1.0, 1.0, 1.0, 1.0, 1.0]`
  - negative-only answer: `[0.0, 0.0, 0.0, 0.0, 0.0]`
