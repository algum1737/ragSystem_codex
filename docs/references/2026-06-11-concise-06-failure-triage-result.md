# 2026-06-11 Concise 06 Failure Triage Result

## Summary

`concise-06` 실패는 단일 원인이 아니라 `concise` 생성 안정성과 deterministic 평가 기준의 표현 허용 범위가 함께 드러난 사례다.

결론:

- 검색 자체는 핵심 근거를 반환한다.
- 서버 실패 답변은 실제로 사전/사후 통지 예외를 누락했다.
- 반복 실행에서는 일부 답변이 의미상 예외를 언급하지만, 현재 rule이 `예측 불가능`, `통제할 수 없는`, `약관에 따른 방법`, `미리` 같은 동의 표현을 잡지 못한다.
- 따라서 다음 작업은 평가 rule의 동의 표현 보정과 `concise` prompt의 필수 예외 보존 보강을 함께 검토해야 한다.

## Evidence

기준 실패 report:

```text
/opt/ragSystem_codex/eval/results/concise_eval_20260610_114205.json
```

기준 trace:

```text
/opt/ragSystem_codex/logs/concise_lightweight_eval_20260610_runbook_test2.jsonl
```

실패 요약:

- `total_cases=6`
- `passed_cases=5`
- `pass_rate=0.8333`
- `concise-06 required_points_score=0.5`
- 누락 required points:
  - `notice_methods`
  - `post_notice_exception`

실패 답변은 유료서비스 중단/변경과 통지는 언급했지만, `약관에서 정한 방법` 수준으로만 답했고 사전 통지 원칙과 부득이한 경우 사후 통지 가능성을 말하지 않았다.

## Retrieved Source Review

동일 질문 top-5 검색 청크에는 핵심 근거가 포함됐다.

- 카카오 유료/결제서비스 chunk 15:
  - 제공 중단 시 미리 제6조에서 정한 방법으로 회원에게 통지
  - 예측할 수 없거나 통제할 수 없는 사유로 인한 부득이한 경우 사후 통지 가능
  - 중대한 변경 또는 회원에게 불리한 변경은 제6조에서 정한 방법으로 통지
- 네이버 유료서비스 chunk 5:
  - 사업 전환, 사업 포기, 업체 간 통합 등으로 제공 불가 시 약관에서 정한 방법으로 통지하고 보상

별도 통지 방법 검색에서는 카카오 제6조 청크가 확인됐다.

- 전자우편
- 카카오톡 메시지
- 개별 유료서비스 내 전자쪽지
- 유료/결제서비스 내 팝업
- 유료/결제서비스 내 게시판 및 카카오 내결제 게시/공지

따라서 `concise-06`의 주요 문제는 검색 결과 부재가 아니다. 다만 원 질문 top-5에는 제6조 통지 방법 청크가 항상 직접 포함되지는 않으므로, 구체 수단을 요구하는 rule은 `제6조에서 정한 방법` 같은 간접 표현을 어느 정도 인정해야 한다.

## Repeat Check

서버에서 같은 질문을 `concise` 모드로 3회 반복했다.

결과:

| run | answer length | sources | required score | note |
| --- | ---: | ---: | ---: | --- |
| 1 | 300 | 5 | 0.5 | `예측 불가능한 상황에선 사후 통보`를 말했지만 rule은 `사후`만 매칭 |
| 2 | 276 | 5 | 0.75 | 통지 방법은 통과, 사전/사후 예외는 누락 |
| 3 | 288 | 5 | 0.75 | 통지 방법은 통과, 사전/사후 예외는 누락 |

같은 질문의 `standard` 모드는 카카오 약관의 사전 통지와 부득이한 경우 사후 통지 예외를 안정적으로 언급했다.

## Classification

분류:

- Primary: `concise` prompt 안정성 문제
- Secondary: deterministic rule의 동의 표현 허용 범위 부족
- Not primary: retrieval failure

근거:

- top-5 검색 청크가 사전/사후 예외를 포함한다.
- 표준 모드는 같은 검색 결과에서 예외를 답변한다.
- `concise`는 짧게 합치는 과정에서 예외 문장을 자주 버린다.
- deterministic rule은 의미상 맞는 일부 표현도 놓친다.

## Recommended Next Step

다음 작업은 별도 구현 계획에서 진행한다.

1. `concise-06` rule을 좁게 보정한다.
   - `post_notice_exception`에 `예측 불가능`, `통제할 수 없는`, `미리`, `사후 통보`를 후보로 추가한다.
   - `notice_methods`에 `명시된 방법`, `약관에 따른 방법`을 후보로 추가할지 검토한다.
2. `CONCISE_PROMPT_TEMPLATE`에 예외/조건 질문에서는 예외를 생략하지 말라는 좁은 규칙을 추가하는 후보를 만든다.
3. 서버에서 `concise-06` 반복 smoke와 전체 concise lightweight eval을 재실행한다.
4. 회귀가 없을 때만 반영한다.

## Decision

현재 triage는 완료한다. 즉시 프롬프트나 평가 기준을 바꾸지 않고, 다음 active plan을 `concise-06` 안정화 구현으로 둔다.
