# 2026-06-02 Gemma3 Quality Gap Review

## Summary

`gemma3:12b` 전환 실험의 품질 하락은 두 케이스에서 발생했다.

- `tc-07`: answer accuracy `0.75`, faithfulness `1.0`
- `tc-11`: answer accuracy `1.0`, faithfulness `0.0`

리뷰 결과, 전역 프롬프트 변경은 부작용이 있어 바로 적용하지 않는다. 대신 `top_k=3`이 두 케이스를 모두 회복했으므로 다음 실험은 `gemma3:12b + top_k=3` full eval이다.

## `tc-07` Review

질문:

```text
위치기반서비스 약관에서 서비스 제공자의 면책 조항은 무엇인가?
```

기존 `gemma3:12b`, `top_k=5` 답변은 다음/카카오 위치기반서비스 약관의 면책 조항을 충실히 설명했다.

- 천재지변 또는 불가항력
- 제3자의 고의적인 서비스 방해
- 이용자 귀책사유로 인한 장애
- 회사의 고의·과실 없는 사유
- 신뢰도/정확성 보증 부재
- 손해에 대한 책임 부재

하락 원인:

- 답변은 실제 면책 내용을 설명했지만 `면책`이라는 표지어를 직접 쓰지 않아 fixed keyword 하나가 빠졌다.
- 실제 품질 문제보다는 keyword 표현 불일치에 가깝다.

## `tc-11` Review

질문:

```text
유료서비스 결제 후 청약철회 또는 환불이 제한되는 조건은 무엇인가?
```

기존 `gemma3:12b`, `top_k=5` 답변은 다음 문제가 있었다.

- 카카오 항목 아래에 네이버 금지행위 조건이 섞였다.
- 질문하지 않은 `문서에서 확인되지 않는 내용` 섹션을 추가했다.
- 환불수수료/환불적립금 관련 내용은 retrieved context에 있는데 일부를 확인되지 않는 내용으로 처리했다.

판단:

- `tc-11`은 실제 answer grounding 문제다.
- 단순 평가셋 보정으로 처리하면 안 된다.

## Prompt Candidate Results

전역 프롬프트 후보를 임시 monkeypatch로 2케이스만 확인했다.

### Candidate A

핵심 약관 용어를 답변에 유지하고, 질문하지 않은 미확인 섹션을 금지하는 후보.

- `tc-07`: accuracy `1.0`, faithfulness `0.0`
- `tc-11`: accuracy `1.0`, faithfulness `1.0`

결론: `tc-07` faithfulness 회귀가 있어 채택하지 않는다.

### Candidate B

질문하지 않은 미확인 섹션만 금지하는 후보.

- `tc-07`: accuracy `1.0`, faithfulness `0.0`
- `tc-11`: accuracy `1.0`, faithfulness `1.0`

결론: `tc-07` faithfulness 회귀가 있어 채택하지 않는다.

### Candidate C

질문 범위 직접 답변과 미확인 섹션 금지를 더 강하게 지시하는 후보.

- `tc-07`: accuracy `1.0`, faithfulness `0.0`
- `tc-11`: accuracy `1.0`, faithfulness `0.0`

결론: 채택하지 않는다.

## Retrieval Width Candidate

`gemma3:12b`, 기존 prompt, `top_k=3`을 2케이스에서 확인했다.

| Case | accuracy | faithfulness | Note |
| --- | ---: | ---: | --- |
| `tc-07` | 1.0 | 1.0 | 면책 조항 중심 답변 유지 |
| `tc-11` | 1.0 | 1.0 | 불필요한 미확인 섹션 제거, 주요 조건에 집중 |

`tc-11`의 `top_k=3` retrieved sources:

1. 카카오 유료:결제서비스 이용약관
2. 네이버 유료서비스 이용약관
3. 카카오 유료:결제서비스 이용약관

해석:

- `top_k=5`에서는 후반 chunk의 환불적립금/운영정책 조각이 답변을 흐릴 가능성이 있다.
- `top_k=3`은 핵심 청약철회/환불 제한 조건에 집중하게 만들어 두 케이스를 회복했다.

## Decision

- 전역 프롬프트 변경은 보류한다.
- `tc-07` 단독 keyword 보정은 가능하지만, `tc-11` 실제 grounding 문제를 해결하지 못하므로 충분하지 않다.
- 다음 실험은 `gemma3:12b + top_k=3` full eval이다.

## Next Work

`gemma3:12b + top_k=3`으로 full eval을 실행해 전체 기준선이 회복되는지 확인한다. 통과 시 운영 모델 전환과 `top_k` 설정 방식을 별도 변경 계획으로 진행한다.
