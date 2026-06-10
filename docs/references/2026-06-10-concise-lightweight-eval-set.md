# 2026-06-10 Concise Lightweight Eval Set

## Summary

선택형 `concise` answer mode의 품질을 빠르게 확인하기 위한 경량 평가셋 후보와 판정 기준을 정의했다.

결론:

- 경량셋은 6개 케이스로 시작한다.
- 목적은 full eval 대체가 아니라 `concise` 전용 회귀 감지다.
- 판정은 단순 keyword보다 `required_points`, `forbidden_claims`, `source_count`, `answer_length`, `latency`를 함께 본다.
- 코드 반영은 별도 구현 작업으로 분리한다.

## Why A Separate Concise Eval Set

`standard` full eval은 기존 품질 기준선을 검증한다. `concise`는 짧은 답변을 목표로 하므로 같은 keyword coverage를 그대로 적용하면 빠른 요약의 의도와 충돌할 수 있다.

다만 `concise`가 짧아지는 과정에서 다음 회귀가 생기면 안 된다.

- 필수 조건 또는 예외사항 누락
- 문서에서 확인되지 않는 내용을 확정적으로 표현
- no-answer 케이스에서 임의 답변 생성
- source count는 유지되지만 답변이 특정 source에만 과도하게 의존

따라서 `concise` 전용 경량셋은 “짧지만 놓치면 안 되는 포인트”를 중심으로 둔다.

## Candidate Cases

| id | source case | doc_type | question | purpose |
| --- | --- | --- | --- | --- |
| `concise-01` | `tc-22` | 운영정책 | 운영정책에서 계정 이용이 제한되거나 해지될 수 있는 조건은 무엇인가? | trace에 paired sample이 있고 운영정책 제재 요약 품질을 확인 |
| `concise-02` | `tc-18` | 위치기반서비스 | 위치기반서비스 약관에서 개인위치정보는 어떤 목적으로 이용되는가? | trace에 paired sample이 있고 concise 이점이 제한적인 케이스 확인 |
| `concise-03` | `tc-13` | 위치기반서비스 | 위치정보 이용 동의 철회와 개인위치정보 보유 기간은 어떻게 처리되는가? | 보유/파기/예외를 짧은 답변에서 누락하지 않는지 확인 |
| `concise-04` | `tc-11` | 유료서비스 | 유료서비스 결제 후 청약철회 또는 환불이 제한되는 조건은 무엇인가? | 이전 concise prompt 회귀가 있었던 환불/제한 조건 확인 |
| `concise-05` | `tc-16` | 유료서비스 | 유료서비스 자동 갱신의 결제 주기와 금액 변경 조건은 문서에서 어떻게 정해져 있는가? | no-answer 계약 확인 |
| `concise-06` | `tc-21` | 유료서비스 | 유료서비스 약관에서 서비스 제공 중단 또는 서비스 변경 시 회원에게 어떻게 통지하는가? | 이전 concise prompt 회귀가 있었던 통지 수단/예외 확인 |

## Required Points

### `concise-01`

Question:

`운영정책에서 계정 이용이 제한되거나 해지될 수 있는 조건은 무엇인가?`

Required points:

- 계정 이용 제한, 정지, 해지, 삭제 중 둘 이상을 언급한다.
- 운영정책 또는 약관 위반을 원인으로 언급한다.
- 비정상 이용, 도용, 부정 이용, 권리침해, 불법, 스팸 중 하나 이상을 예시로 든다.
- 답변은 운영정책 범위로 제한한다.

Forbidden claims:

- 모든 위반이 즉시 영구 해지된다고 단정한다.
- 일반 서비스 약관 또는 위치기반서비스 내용만 근거로 답한다.

### `concise-02`

Question:

`위치기반서비스 약관에서 개인위치정보는 어떤 목적으로 이용되는가?`

Required points:

- 개인위치정보 또는 위치정보를 언급한다.
- 위치기반서비스 제공 목적을 언급한다.
- 검색, 콘텐츠, 광고, 생활편의 중 둘 이상을 예시로 든다.
- 수집, 이용, 제공 중 하나 이상의 처리 행위를 언급한다.

Forbidden claims:

- 개인위치정보를 모든 서비스에서 장기 보관한다고 단정한다.
- 위치정보 이용 목적을 개인정보 일반 처리 목적만으로 대체한다.

### `concise-03`

Question:

`위치정보 이용 동의 철회와 개인위치정보 보유 기간은 어떻게 처리되는가?`

Required points:

- 동의 철회 또는 일부 철회를 언급한다.
- 목적 달성 시 지체 없이 파기한다는 점을 언급한다.
- 게시물 또는 콘텐츠와 함께 저장되는 경우 해당 보관기간 동안 보관될 수 있음을 언급한다.
- 법령 또는 정당한 사유에 따른 보유 예외를 언급한다.

Forbidden claims:

- 개인위치정보 보유 기간을 일괄적으로 6개월이라고 답한다.
- 동의 철회 시 모든 기록이 예외 없이 즉시 삭제된다고 단정한다.

### `concise-04`

Question:

`유료서비스 결제 후 청약철회 또는 환불이 제한되는 조건은 무엇인가?`

Required points:

- 청약철회 또는 환불 제한을 언급한다.
- 결제, 대금, 이용요금 중 하나 이상을 언급한다.
- 이미 이용했거나 제공이 시작된 경우처럼 제한 조건을 설명한다.
- 제한 또는 불가 조건과 취소/환불 가능 조건을 혼동하지 않는다.

Forbidden claims:

- 모든 유료서비스 결제는 언제나 전액 환불된다고 답한다.
- 운영정책 제재 조건을 환불 제한 조건으로 섞어 답한다.

### `concise-05`

Question:

`유료서비스 자동 갱신의 결제 주기와 금액 변경 조건은 문서에서 어떻게 정해져 있는가?`

Required points:

- 문서에서 직접 확인되지 않거나 명시적 근거가 부족하다고 답한다.
- 자동 갱신, 결제 주기, 금액 또는 요금을 질문 범위로 언급한다.
- 확인 가능한 관련 내용이 있다면 제한적으로만 말한다.
- 근거 없는 세부 주기나 금액을 만들지 않는다.

Forbidden claims:

- 구체적인 결제 주기, 금액 변경 기준, 통지 시점을 근거 없이 확정한다.
- no-answer 케이스인데 정상 answer case처럼 장황하게 설명한다.

### `concise-06`

Question:

`유료서비스 약관에서 서비스 제공 중단 또는 서비스 변경 시 회원에게 어떻게 통지하는가?`

Required points:

- 유료서비스의 중단 또는 변경을 언급한다.
- 통지, 공지, 고지 중 하나 이상을 언급한다.
- 전자우편, 카카오톡, 서비스 게시판, 팝업, 제6조에서 정한 방법 중 둘 이상을 언급한다.
- 사전 통지가 원칙이나 부득이한 경우 사후 통지가 가능하다는 예외를 구분한다.

Forbidden claims:

- 어떤 경우에도 사전 통지가 필요 없다고 답한다.
- 유료서비스가 아닌 위치기반서비스 고지 방식만 근거로 답한다.

## Pass Criteria

각 케이스는 아래 기준을 모두 만족해야 통과로 본다.

- `required_points` 충족률 0.75 이상
- `forbidden_claims` 0건
- `source_count` 3개 이상
- `answer_length` 700자 이하
- `latency_ms.total`은 warmed 상태 기준 12000ms 이하를 권장 기준으로 기록하되, 초기 cold load 표본은 별도 표시한다.

`concise-05` no-answer 케이스는 추가로 아래를 만족해야 한다.

- 문서 미확인 또는 직접 근거 부족을 명시한다.
- 결제 주기나 금액 변경 조건을 임의로 생성하지 않는다.

## Implementation Recommendation

다음 구현 작업에서는 별도 JSON 파일을 추가하는 방식을 권장한다.

- 후보 경로: `eval/concise_test_cases.json`
- 필드:
  - `id`
  - `source_case_id`
  - `question`
  - `doc_type`
  - `required_points`
  - `forbidden_claims`
  - `expected_not_found`
  - `max_answer_length`
  - `min_source_count`

하네스는 첫 단계에서 LLM judge 없이 deterministic check로 시작한다. 이후 필요한 경우 faithfulness judge 또는 required-point judge를 추가한다.

## Decision

경량 평가셋은 필요하다. 다만 이번 작업은 문서 정의까지만 완료하고, eval harness 코드 반영은 별도 사용자 승인 후 진행한다.

다음 active plan은 concise lightweight eval harness 구현 계획으로 둔다.
