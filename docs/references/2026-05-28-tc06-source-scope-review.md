# 2026-05-28 TC06 Source Scope Review

## Summary

`tc-06` 분쟁 해결 케이스의 `relevant_sources` 범위를 source scope policy 기준으로 재검토했다.

결론:

- `tc-06`은 explicit cross-policy coverage 케이스가 아니라 대표 근거 회귀 케이스로 유지한다.
- 기존 `relevant_sources` 7개 중 위치기반서비스 약관과 네이버 이용약관은 보조 또는 별도 범위 근거로 분리한다.
- `tc-06`의 대표 근거는 실제 답변에 충분한 4개 문서로 좁힌다.

최종 `tc-06` representative sources:

- `카카오통합서비스약관20210701.pdf`
- `카카오계정약관20240416.pdf`
- `다음 이용약관.txt`
- `카카오 유료:결제서비스 이용약관.txt`

## Rationale

최신 답변은 위 4개 문서의 협의, 민사소송법상 관할법원, 제소 근거로 충분히 완결된다.

기존에 포함되어 있던 위치기반서비스 약관은 방송통신위원회 재정, 개인정보 분쟁조정위원회 조정이라는 별도 절차를 다룬다. 이는 같은 "분쟁" 주제지만 일반/계정/유료 약관의 민사소송 절차와 평가 목적이 다르므로 별도 hard case 후보로 보는 편이 낫다.

네이버 이용약관도 분쟁 처리 절차를 포함하지만, 현재 `tc-06`의 답변과 retrieved source가 이미 충분한 대표 근거를 제공한다. source recall을 높이기 위해 모든 가능한 관련 문서를 유지하면 top-k recall 해석이 흐려진다.

## Validation

최종 검증 기준 리포트:

- 이전 기준 리포트: `eval/results/eval_20260528_115250_recalibrated.json`
- `tc-06` 재범위화 리포트: `eval/results/eval_20260528_115250_tc06_rescoped.json`
- source drift report: `docs/references/2026-05-28-tc06-source-scope-report.md`

최종 지표:

| Metric | Value |
| --- | ---: |
| `total_cases` | `22` |
| `accuracy_mean` | `1.0` |
| `faithfulness_mean` | `1.0` |
| `not_found_success_rate` | `1.0` |
| `rag_normalized_source_precision@k_mean` | `0.9886` |
| `source_recall@k_mean` | `0.9886` |

최종 source drift report:

- Critical cases: 없음
- Watch cases: 없음

## Next Candidate

위치기반서비스 분쟁 해결 절차는 별도 후보로 남긴다. 추가한다면 질문 범위를 "위치기반서비스 약관에서 위치정보 관련 분쟁 발생 시 해결 절차"로 명시하고, `doc_type`은 `위치기반서비스`로 둔다.
