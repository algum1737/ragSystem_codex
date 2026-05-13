# Partial Answer Policy Plan

## Goal

`not_found_rate=0.2`를 줄이기 위해, 질문 일부에만 근거가 있을 때 전체 no-answer로 끝나지 않도록 부분 답변 정책을 설계하고 검증한다.

## Scope

- 최신 리포트 `eval/results/eval_20260513_155642.json`의 `tc-01`, `tc-04` 분석
- no-answer와 partial-answer 기준 정의
- `retriever/engine.py` 프롬프트 개선 후보 선정
- full eval 재실행 기준 정의

## Assumptions

- `tc-01`은 환불 정책 근거가 약해 no-answer가 타당할 가능성이 있다.
- `tc-04`는 정기 결제 취소/해지 근거가 일부 있으므로 partial-answer 후보로 본다.
- 구현 변경은 사용자 승인 후 진행한다.

## Steps

1. `tc-01`, `tc-04`의 최종 검색 청크와 답변을 비교한다.
2. no-answer, partial-answer, full-answer 판정 기준을 정한다.
3. 프롬프트가 문서에 있는 부분만 답하고 없는 부분은 분리해서 밝히도록 개선한다.
4. `.venv/bin/python eval/pipeline.py --all`로 재평가한다.

## Risks

- 부분 답변 정책이 과도하면 근거가 약한 내용까지 답하려 할 수 있다.
- faithfulness가 떨어지면 accuracy 상승보다 위험하다.

## Validation

- `.venv/bin/python -m py_compile retriever/engine.py`가 통과해야 한다.
- `bash scripts/validate-docs.sh`가 통과해야 한다.
- full eval에서 `faithfulness_mean`이 하락하지 않아야 한다.
- `not_found_rate` 또는 `tc-04` answer quality가 개선되어야 한다.

## Open Work

- 구현 변경 승인
- partial-answer 프롬프트 설계
- full eval 재실행
