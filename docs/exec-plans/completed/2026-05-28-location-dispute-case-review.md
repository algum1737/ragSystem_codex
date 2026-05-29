# Location Dispute Case Review Plan

## Goal

위치기반서비스 분쟁 해결 절차를 별도 hard case로 추가할지 검토한다.

## Scope

- 위치기반서비스 약관의 분쟁 해결 절차 근거 확인
- `tc-06`과 분리된 평가 목적 정의
- 신규 케이스 추가 여부와 expected keyword 후보 검토

## Out Of Scope

- 검색 알고리즘 변경
- 신규 문서 인제스천
- 모델 교체
- 전체 평가셋 재설계

## Assumptions

- `tc-06`은 대표 근거 기준으로 정리되어 더 이상 watch case가 아니다.
- 위치기반서비스 분쟁 절차는 방송통신위원회 재정과 개인정보 분쟁조정위원회 조정이라는 별도 평가 목적을 갖는다.
- 별도 케이스를 추가한다면 `doc_type`은 `위치기반서비스`로 제한한다.

## Pre-flight checks

- `docs/references/2026-05-28-tc06-source-scope-review.md` 확인
- `docs/references/2026-05-28-tc06-source-scope-report.md` 확인
- Chroma에 저장된 위치기반서비스 분쟁 조정 청크 확인

## Steps

1. 위치기반서비스 분쟁 해결 조항의 공통 근거를 확인한다.
2. 신규 hard case 질문과 expected keyword 후보를 작성한다.
3. 평가셋 추가 여부를 결정한다.
4. 추가 시 retrieval/full eval 검증 범위를 정한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- 평가셋 변경 시 `.venv/bin/python -m json.tool eval/test_cases.json`
- 평가셋 변경 시 `.venv/bin/python eval/pipeline.py --metric retrieval`

## Manual/Runtime QA

- 위치기반서비스 분쟁 조정 근거와 신규 케이스 질문 범위 대조

## Skipped/Not Run

- 23개 전체 fresh full eval은 실행하지 않았다.
  - 이유: 기존 22개 케이스는 `eval/results/eval_20260528_115250_tc06_rescoped.json`에서 이미 검증됐고, 이번 변경은 신규 `tc-23` 1건 추가다.
  - 대신 `tc-23` 단건에 대해 로컬 Ollama 생성, keyword accuracy, faithfulness, retrieval 지표를 검증하고 기존 리포트에 추가한 `eval/results/eval_20260528_115250_location_dispute_added.json`을 생성했다.

## Open Work

- 남은 작업 없음.
- 다음 active plan: `docs/exec-plans/active/2026-05-28-source-drift-ci-promotion.md`

## Validation Result

- Pre-flight checks
  - `docs/references/2026-05-28-tc06-source-scope-review.md` 확인.
  - `docs/references/2026-05-28-tc06-source-scope-report.md` 확인.
  - Chroma에 저장된 위치기반서비스 분쟁 조정 청크 확인.
- Automated tests
  - `.venv/bin/python -m json.tool eval/test_cases.json` 통과.
  - `.venv/bin/python eval/pipeline.py --metric retrieval` 통과.
  - `tc-23` 단건 로컬 Ollama 생성/faithfulness 검증 통과.
  - `eval/results/eval_20260528_115250_location_dispute_added.json` 생성.
  - `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260528_115250_location_dispute_added.json --output docs/references/2026-05-28-location-dispute-case-report.md --fail-on-critical` 통과.
  - `bash scripts/validate-docs.sh` 통과.
- Manual/Runtime QA
  - 위치기반서비스 분쟁 조정 근거와 신규 케이스 질문 범위를 대조했다.
  - 최종 source drift report 기준 critical/watch case 없음.
  - 결과 문서: `docs/references/2026-05-28-location-dispute-case-review.md`
