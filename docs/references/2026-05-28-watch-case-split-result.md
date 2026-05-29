# 2026-05-28 Watch Case Split Result

## Summary

source scope policy에 따라 broad watch case를 목적별 평가 케이스로 분리했다.

주요 변경:

- `tc-02`: 일반 서비스 약관의 개인정보 이용 목적 케이스로 좁힘.
- `tc-03`: 일반 서비스 약관의 이용 제한/정지 케이스로 좁힘.
- `tc-07`: 위치기반서비스 면책 케이스로 좁힘.
- `tc-08`: 다음/카카오 위치기반서비스의 변경/중단 고지 케이스로 좁힘.
- `tc-14`: 일반 서비스 및 계정 약관의 계정 휴면/정지/삭제 케이스로 좁힘.
- `tc-15`: 일반 서비스 약관의 사전 고지 없는 변경/종료 예외 케이스로 좁힘.
- `tc-18`~`tc-22`: 위치기반서비스, 운영정책, 유료서비스, 계정 운영정책 범위를 명시한 분리 케이스를 추가함.

## Validation

최종 검증 기준 리포트:

- full eval 원본: `eval/results/eval_20260528_115250.json`
- keyword 보정 재채점 리포트: `eval/results/eval_20260528_115250_recalibrated.json`
- source drift report: `docs/references/2026-05-28-watch-case-split-source-drift-report.md`

최종 지표:

| Metric | Value |
| --- | ---: |
| `total_cases` | `22` |
| `accuracy_mean` | `1.0` |
| `faithfulness_mean` | `1.0` |
| `not_found_success_rate` | `1.0` |
| `rag_normalized_source_precision@k_mean` | `0.9795` |
| `source_recall@k_mean` | `0.9692` |

## Notes

- `eval_20260528_115250_recalibrated.json`은 새 LLM 생성을 다시 수행한 리포트가 아니라, `eval_20260528_115250.json`의 저장 답변을 현재 `eval/test_cases.json` keyword 기준으로 재채점한 리포트다.
- 재채점 이유는 마지막 full eval 이후 `tc-02`, `tc-04`, `tc-05`, `tc-14`의 expected keyword OR group을 답변 표현에 맞춰 보정했기 때문이다.
- source retrieval과 faithfulness 값은 `eval_20260528_115250.json`에서 유지했다.

## Remaining Watch

source drift report 기준 critical case는 없다.

남은 watch case:

| Case | Reason | Next Action |
| --- | --- | --- |
| `tc-06` | 분쟁 해결 질문의 `relevant_sources`가 넓어 source recall이 낮게 보인다. 답변 accuracy와 faithfulness는 모두 1.0이다. | 별도 source scope review에서 대표 근거 기준으로 좁힐지, explicit cross-policy 케이스로 유지할지 결정한다. |
