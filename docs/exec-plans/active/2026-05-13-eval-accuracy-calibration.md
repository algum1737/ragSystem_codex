# Eval Accuracy Calibration Plan

## Goal

키워드 exact-match에 치우친 accuracy 평가를 보정해, 의미상 맞는 답변이 낮게 평가되는 문제를 줄인다.

## Scope

- 약관 카테고리 기준 정리
- `eval/test_cases.json`의 expected keyword 구조 검토
- 동의어/대체 표현을 표현하는 평가 구조 설계
- `eval/pipeline.py`의 `answer_accuracy()` 확장
- full eval 재실행과 기준선 비교

## Assumptions

- 현재 `accuracy_mean=0.625`에는 실제 답변 품질 문제와 평가 기준 불일치가 섞여 있다.
- 약관 카테고리는 `일반`, `유료서비스`, `위치기반서비스`, `운영정책` 4개로 나눈다.
- `tc-08`, `tc-09`는 우선 평가 기준 보정 대상이다.
- `tc-01`, `tc-04`는 no-answer 또는 partial-answer 케이스로 별도 판단이 필요하다.
- 구현 변경은 사용자 승인 후 진행한다.

## Steps

1. 기존 `expected_keywords`와 호환되는 확장 구조를 설계한다.
2. `doc_type` 카테고리를 `일반`, `유료서비스`, `위치기반서비스`, `운영정책` 기준으로 정리한다.
3. `answer_accuracy()`가 문자열 키워드와 OR keyword group을 모두 처리하게 한다.
4. `tc-08`, `tc-09`의 대체 표현을 평가셋에 반영한다.
5. `tc-01`, `tc-04`의 평가 목적을 no-answer/partial-answer 관점에서 정리한다.
6. `.venv/bin/python eval/pipeline.py --all`로 새 리포트를 생성한다.

## Risks

- 평가셋 보정이 실제 품질 개선처럼 오해될 수 있다.
- 동의어를 과도하게 추가하면 평가가 느슨해질 수 있다.

## Validation

- `.venv/bin/python -m py_compile eval/pipeline.py`가 통과해야 한다.
- `bash scripts/validate-docs.sh`가 통과해야 한다.
- `.venv/bin/python eval/pipeline.py --all`이 통과해야 한다.
- 새 리포트에서 accuracy 변화 원인을 문서화해야 한다.

## Open Work

- 구현 변경 승인
- 약관 카테고리 4종 기준 반영
- accuracy 평가 구조 확장
- 평가셋 보정
- full eval 재실행
