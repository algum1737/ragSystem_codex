# 2026-05-28 Location Dispute Case Review

## Summary

위치기반서비스 분쟁 해결 절차를 `tc-23` hard case로 추가했다.

신규 케이스:

- `id`: `tc-23`
- 질문: 위치기반서비스 약관에서 위치정보 관련 분쟁 발생 시 해결 절차는 어떻게 되는가?
- `doc_type`: `위치기반서비스`
- 대표 근거:
  - `다음 위치기반서비스 이용약관.txt`
  - `네이버 위치기반서비스 이용약관.txt`
  - `카카오 위치정보 이용약관.txt`

## Rationale

`tc-06`은 일반/계정/유료서비스 약관의 협의와 민사소송 절차를 검증하는 대표 근거 케이스로 정리했다. 반면 위치기반서비스 약관은 위치정보 분쟁에 대해 성실 협의, 방송통신위원회 재정, 개인정보 분쟁조정위원회 조정이라는 별도 절차를 다룬다.

따라서 위치기반서비스 분쟁 절차는 `tc-06`의 `relevant_sources`에 섞지 않고, 질문 범위와 `doc_type`을 명시한 독립 hard case로 검증한다.

## Validation

최종 검증 기준 리포트:

- 기준 리포트: `eval/results/eval_20260528_115250_tc06_rescoped.json`
- `tc-23` 추가 리포트: `eval/results/eval_20260528_115250_location_dispute_added.json`
- source drift report: `docs/references/2026-05-28-location-dispute-case-report.md`

`tc-23` 단건 결과:

| Metric | Value |
| --- | ---: |
| `answer_accuracy` | `1.0` |
| `faithfulness` | `1.0` |
| `rag_normalized_source_precision_at_k` | `1.0` |
| `source_recall_at_k` | `1.0` |

전체 재계산 지표:

| Metric | Value |
| --- | ---: |
| `total_cases` | `23` |
| `accuracy_mean` | `1.0` |
| `faithfulness_mean` | `1.0` |
| `not_found_success_rate` | `1.0` |
| `rag_normalized_source_precision@k_mean` | `0.9891` |
| `source_recall@k_mean` | `0.9891` |

최종 source drift report:

- Critical cases: 없음
- Watch cases: 없음

## Notes

- `eval_20260528_115250_location_dispute_added.json`은 23개 전체를 fresh generation한 리포트가 아니다.
- 기존 22개 케이스는 `eval_20260528_115250_tc06_rescoped.json`의 저장 결과를 유지했고, 신규 `tc-23`만 로컬 Ollama로 생성/faithfulness를 검증해 추가했다.
- 전체 fresh eval은 비용이 크므로, 필요 시 별도 active plan에서 실행한다.
