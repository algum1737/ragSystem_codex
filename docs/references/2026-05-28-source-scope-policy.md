# 2026-05-28 Source Scope Policy

## Summary

평가셋의 `relevant_sources`는 현재 검색 결과를 따라가는 목록이 아니라, 각 테스트 케이스가 검증하려는 질문 범위를 고정하는 계약으로 둔다.

정책 결론:

- 기본값은 "답변에 충분한 대표 근거 문서" 기준이다.
- "가능한 모든 관련 문서" 기준은 corpus coverage를 측정하는 별도 평가셋이나 별도 케이스에만 사용한다.
- `doc_type`이 지정된 케이스는 해당 카테고리 내부의 직접 근거만 `relevant_sources`에 포함한다.
- `doc_type`이 `null`인 케이스도 무제한 cross-policy 케이스로 보지 않는다. 질문 문구가 요구하는 범위와 expected keyword가 검증하는 답변 범위에 맞춰 대표 근거를 고정한다.
- 새 corpus에서 동등 근거가 발견되면 기존 케이스의 `relevant_sources`를 단순 확장하지 않고, 먼저 케이스 분리 또는 질문 재정의를 검토한다.

따라서 이번 작업에서는 `eval/test_cases.json`을 변경하지 않는다. watch case는 source drift 후보로 유지하고, 다음 평가셋 확장 때 이 정책에 따라 개별 케이스를 분리한다.

## Policy

### Representative Evidence Scope

대부분의 기능 회귀 검증은 대표 근거 기준을 사용한다.

포함 기준:

- 질문의 핵심 답변을 직접 뒷받침하는 문서
- expected keyword가 요구하는 조항을 실제로 포함하는 문서
- `doc_type`이 지정된 경우 해당 카테고리의 문서
- `doc_type`이 없는 경우에도 케이스 작성 당시 의도한 서비스/정책 범위의 문서

제외 기준:

- 비슷한 단어가 있지만 답변 근거가 간접적인 문서
- 현재 retrieval 결과에만 나타난 문서
- 같은 주제의 특수 서비스 약관이지만 기존 질문이 그 특수 범위를 묻지 않는 문서
- 운영정책처럼 제재/집행 근거는 있으나 일반약관 질문의 직접 근거가 아닌 문서

이 기준은 `rag_normalized_source_precision@k`와 `source_recall@k`를 "답변에 필요한 대표 근거를 회수했는가"로 해석하게 한다.

### Exhaustive Corpus Scope

"가능한 모든 관련 문서" 기준은 기본 평가셋에 섞지 않는다.

사용 가능한 경우:

- 신규 corpus가 특정 조항을 빠짐없이 포함하는지 측정하는 coverage 전용 평가
- 같은 질문을 일반약관, 유료서비스, 위치기반서비스, 운영정책 전체에서 비교해야 하는 명시적 cross-policy 케이스
- 인제스천 누락이나 source mapping 누락을 찾는 감사성 평가

이 기준을 쓰는 케이스는 질문에 범위를 명시한다. 예: "일반약관, 유료서비스, 위치기반서비스 약관 전체에서 서비스 중단 고지 예외를 비교하라."

### Case Split Rule

한 질문에 여러 정책군의 동등 근거가 걸리면 기존 케이스를 넓히기보다 먼저 분리한다.

분리 우선 조건:

- 일반약관과 운영정책이 서로 다른 행위를 다루는 경우
- 위치기반서비스나 유료서비스의 특수 조항이 일반 서비스 조항과 다른 예외를 갖는 경우
- 계정 약관과 서비스 약관의 종료/정지 조건이 다른 책임 주체나 절차를 갖는 경우
- source recall을 높이기 위해 `relevant_sources`가 top-k보다 커져 회수율 해석이 흐려지는 경우

확장 허용 조건:

- 새 source가 기존 질문과 같은 카테고리, 같은 답변 범위, 같은 조항 의미를 갖는 직접 근거인 경우
- 질문 문구와 expected keyword가 이미 cross-policy 답변을 요구하는 경우
- 확장 전후에 retrieved source가 아니라 문서 조항 자체로 직접 근거성이 확인된 경우

## Watch Case Decisions

| Case | Decision | Rationale |
| --- | --- | --- |
| `tc-02` | Keep watch | 개인정보 수집/이용 목적은 일반약관, 계정, 위치정보 문서가 섞일 수 있다. 기존 케이스를 확장하기보다 개인정보 일반 목적과 위치정보/계정 목적을 분리해야 한다. |
| `tc-03` | Keep watch | 서비스 제한/정지는 일반약관과 운영정책 모두에 근거가 있다. 운영정책 집행 조건을 별도 케이스로 분리한 뒤 source 범위를 재정의한다. |
| `tc-06` | Keep watch | 분쟁 해결은 현재 대표 근거로 답변과 faithfulness가 통과한다. 카카오 운영정책은 직접 근거성이 약하므로 relevant source로 추가하지 않는다. |
| `tc-07` | Keep watch | 면책 조항은 일반약관, 위치기반서비스, 유료서비스마다 특수성이 있다. 하나의 broad case로 확장하지 않고 카테고리별 케이스 분리를 우선한다. |
| `tc-08` | Keep watch | 서비스 변경/중단 고지는 일반 서비스와 특수 서비스 고지가 섞인다. 일반 고지와 위치/유료 고지 케이스를 분리한다. |
| `tc-14` | Keep watch | 계정 휴면/정지/삭제는 계정 약관과 운영정책이 직접 근거이고, 일반 서비스 약관은 일부 관련되지만 질문 범위를 흐릴 수 있다. 계정 제재와 서비스 이용 제한을 분리한다. |
| `tc-15` | Keep watch | 사전 고지 없는 변경/종료 예외는 cross-policy 성격이 강하다. exhaustive scope로 바꾸려면 질문 문구를 명시적으로 확장하고 별도 케이스로 둔다. |

## Impact

- 현재 latest full eval의 생성 지표는 유지한다.
- `eval/test_cases.json`은 이번 작업에서 변경하지 않는다.
- source drift report의 watch case는 실패가 아니라 정책 기반 재검토 후보로 유지한다.
- 다음 평가셋 확장 작업에서는 broad watch case를 작은 목적별 케이스로 나누고, 각 케이스에 `doc_type` 또는 명시적 cross-policy 범위를 부여한다.

## Next Work

1. `tc-02`, `tc-03`, `tc-07`, `tc-08`, `tc-14`, `tc-15`를 케이스 분리 후보로 둔다.
2. 분리 작업은 별도 active exec plan에서 수행한다.
3. 분리 후 full eval과 source drift report를 다시 실행해 watch case가 실제 regression인지 새 대표 근거인지 판단한다.
