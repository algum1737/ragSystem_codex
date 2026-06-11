# 2026-06-11 Concise Post-Fix Monitoring Result

## Summary

`concise-06` 안정화 변경 이후 운영 API/Web 상태와 최근 concise trace를 확인했다.

결론:

- 운영 API/Web은 정상이다.
- 최근 운영 trace에는 `answer_mode=concise` API 표본이 7건 있다.
- post-fix 이후 표본은 작업 중 smoke 중심이라 실제 사용자 표본은 아직 부족하다.
- 표본 부족을 보완하기 위해 `concise-06` 운영 API smoke를 1회 실행했고, 사전/사후 예외 보존과 무관 bullet 제거를 확인했다.
- 추가 prompt 변경이나 eval case 추가는 이번 모니터링 범위에서 진행하지 않는다.

## Server Health

확인 결과:

```text
ragsystem-api: active
ragsystem-web: active
API /health: {"status":"ok","model":"gemma3:12b"}
Streamlit _stcore/health: ok
```

## Trace Review

Trace file:

```text
/opt/ragSystem_codex/logs/rag_traces.jsonl
```

집계:

```text
total_records=54
api.query=31
eval.case=23
api.answer_mode.standard=3
api.answer_mode.concise=7
api.answer_mode.none=22
```

최근 `answer_mode=concise` 3건:

| timestamp UTC | answer length | source count | total latency ms | note |
| --- | ---: | ---: | ---: | --- |
| 2026-06-11T01:05:04Z | 386 | 5 | 24668.10 | post-fix 작업 중 smoke, 이전 prompt에서 무관 bullet 확인 |
| 2026-06-11T01:18:56Z | 302 | 5 | 24041.51 | post-fix 작업 중 final API smoke |
| 2026-06-11T04:11:08Z | 376 | 5 | 14664.74 | 이번 monitoring API smoke |

실제 사용자 표본은 아직 부족하다. 따라서 이번 판단은 운영 smoke 중심이다.

## API Smoke

질문:

```text
유료서비스 약관에서 서비스 제공 중단 또는 서비스 변경 시 회원에게 어떻게 통지하는가?
```

요청:

```json
{
  "doc_type": "유료서비스",
  "answer_mode": "concise"
}
```

결과:

```text
answer_length=376
source_count=5
has_post_exception=true
irrelevant_terms=[]
```

확인한 기준:

- 사전/사후 예외 표현 포함
- `사용기간`, `청약철회`, `환불` 재발 없음
- source count 5 유지
- 답변 길이 700자 이하

답변에는 네이버 유료서비스의 통지/보상 문장이 함께 포함됐지만, 별도 무관 bullet은 아니고 서비스 제공 불가 시 통지 문맥 안에 함께 나온 표현이다. 이번 범위에서는 blocking issue로 보지 않는다.

## Decision

post-fix monitoring은 통과로 본다.

다만 실제 사용자 concise 표본이 부족하므로 다음 후속 작업은 운영 trace가 더 쌓인 뒤 실제 사용자 표본 중심으로 다시 확인하는 것이다.
