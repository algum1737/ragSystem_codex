# Plans

## Rules

- 큰 작업은 구현 전에 반드시 `exec-plans/active/`에 실행 계획을 만든다.
- 실행 계획은 목표, 범위, 가정, 단계, 리스크, 검증 방법, 남은 작업 여부를 포함한다.
- 진행 중 계획은 `exec-plans/active/`에 둔다.
- 작업이 완료되면 완료 범위와 검증 결과를 계획 문서에 기록한다.
- 검증 기준을 충족하고 남은 작업이 없으면 계획 문서를 `exec-plans/completed/`로 이동한다.
- 계획을 이동할 때는 `docs/index.md`와 `docs/HANDOFF.md`도 함께 갱신한다.
- 완료됐는지 애매한 작업은 `active/`에 남기되 `Open Work`와 다음 판단 기준을 적는다.

## Validation Contract

실행 계획은 작업 시작 전에 검증 계약을 먼저 고정하고, 완료 시 같은 항목을 결과와 대조한다.

- `Pre-flight checks`: 브랜치, active plan 존재, 관련 문서/파일, 기존 상태, 외부 도구 연결 여부처럼 작업 전 확인해야 하는 항목을 적는다.
- `Automated tests`: 실행할 단위 테스트, 통합 테스트, E2E, 타입체크, 린트, 문서 검증 명령을 구체적인 명령어로 적는다.
- `Manual/Runtime QA`: 브라우저, 에뮬레이터, 실제 기기, 스크린샷, 접근성 트리, 로그처럼 사람이 보거나 런타임에서 확인할 흐름과 증거 기준을 적는다.
- `Skipped/Not Run`: 실행하지 않을 검증 또는 실행하지 못할 가능성이 있는 검증을 미리 적고, 범위 밖/환경 없음/네트워크 제한/기기 없음 같은 이유를 명시한다.
- `Validation Result`: 완료 시 실제 실행한 명령과 결과를 `통과`, `실패`, `미실행`으로 기록하고, 실패나 미실행은 후속 작업 또는 남은 리스크로 연결한다.

## Recommended Plan Sections

- `Goal`
- `Scope`
- `Out Of Scope`
- `Assumptions`
- `Pre-flight checks`
- `Steps`
- `Automated tests`
- `Manual/Runtime QA`
- `Skipped/Not Run`
- `Open Work`
- `Completion`
- `Validation Result`

## Current Roadmap

### Bootstrap

- `2026-05-12-bootstrap-ragsystem-codex.md`
  - 목표: 소스 프로젝트와 하네스 운영 체계를 결합한다.
  - 상태: Completed

### Runtime Validation

- `2026-05-12-runtime-validation.md`
  - 목표: 실행 환경을 복구하고 API, UI, eval smoke test를 수행한다.
  - 상태: Completed

### Cross-Encoder Offline Setup

- `2026-05-13-cross-encoder-offline.md`
  - 목표: reranking 모델 캐시를 준비해 완전 오프라인 경로를 맞춘다.
  - 상태: Completed

### Architecture Document Consolidation

- `2026-05-13-architecture-doc-consolidation.md`
  - 목표: 루트 아키텍처 요약과 상세 다이어그램 문서의 역할을 정리한다.
  - 상태: Completed

### Quality Baseline Improvement

- `2026-05-13-quality-baseline-improvement.md`
  - 목표: 최신 평가 기준선을 분석하고 첫 품질 개선 실험을 정한다.
  - 상태: Completed

### Eval Harness Alignment

- `2026-05-13-eval-harness-alignment.md`
  - 목표: 평가 retrieval 지표를 실제 RAG 검색 경로와 맞춘다.
  - 상태: Completed

### Answer Quality Improvement

- `2026-05-13-answer-quality-improvement.md`
  - 목표: 검색 이후 답변 품질과 평가셋 정합성 문제를 개선한다.
  - 상태: Completed

### Eval Accuracy Calibration

- `2026-05-13-eval-accuracy-calibration.md`
  - 목표: keyword exact-match에 치우친 accuracy 평가를 보정한다.
  - 상태: Completed

### Partial Answer Policy

- `2026-05-13-partial-answer-policy.md`
  - 목표: 근거가 일부 있을 때 no-answer 대신 부분 답변을 하도록 정책을 정한다.
  - 상태: Completed

### GitHub Actions CI

- `2026-05-13-github-actions-ci.md`
  - 목표: PR에서 최소 checks가 실행되도록 GitHub Actions를 추가한다.
  - 상태: Completed

### Search Quality Improvement

- `2026-05-14-search-quality-improvement.md`
  - 목표: 검색 기준선을 분석하고 `precision@k_mean=0.60+`를 향한 1차 개선안을 검증한다.
  - 상태: Completed

### Next Quality Iteration

- `2026-05-14-next-quality-iteration.md`
  - 목표: 검색 1차 개선 이후 남은 품질 병목을 재분류하고 다음 실험 후보를 정한다.
  - 상태: Completed

### Eval Case Alignment

- `2026-05-14-eval-case-alignment.md`
  - 목표: 낮은 accuracy 케이스의 질문과 expected keyword를 문서 근거에 맞게 정렬한다.
  - 상태: Completed

### Next Search Quality Experiment

- `2026-05-14-next-search-quality-experiment.md`
  - 목표: 평가셋 정합성 보정 이후 남은 검색 지표 병목을 분석하고 다음 검색 품질 실험을 정한다.
  - 상태: Completed

### Retrieval Metric Normalization

- `2026-05-14-retrieval-metric-normalization.md`
  - 목표: `precision@k` 계열 지표의 상한 문제를 보정하고 검색 평가 지표를 분리한다.
  - 상태: Completed

### Residual Answer Quality Analysis

- `2026-05-14-residual-answer-quality-analysis.md`
  - 목표: 검색 지표 정규화 이후 남은 답변 accuracy 병목을 분석한다.
  - 상태: Completed

### Answer Format Prompt Experiment

- `2026-05-14-answer-format-prompt-experiment.md`
  - 목표: 분쟁/면책/의무 질문의 답변 형식을 안정화해 잔여 accuracy 감점을 줄인다.
  - 상태: Completed

### Faithfulness Eval Stability

- `2026-05-14-faithfulness-eval-stability.md`
  - 목표: `tc-10` faithfulness 판정 흔들림을 분석하고 다음 개선 후보를 정한다.
  - 상태: Completed

### Faithfulness Context Selection

- `2026-05-15-faithfulness-context-selection.md`
  - 목표: faithfulness judge 입력 context 선택 방식을 개선한다.
  - 상태: Completed

### Residual Keyword Accuracy

- `2026-05-15-residual-keyword-accuracy.md`
  - 목표: `tc-03`, `tc-09` 잔여 keyword accuracy 감점을 분석한다.
  - 상태: Completed

### Eval Generalization Review

- `2026-05-15-eval-generalization-review.md`
  - 목표: 평가셋 상한 도달 이후 일반화와 확장 방향을 검토한다.
  - 상태: Completed

### Eval Set Expansion

- `2026-05-22-eval-set-expansion.md`
  - 목표: 최신 13개 문서, 318개 청크 corpus를 검증하도록 hard case를 추가한다.
  - 상태: Completed

### Eval Failure Triage

- `2026-05-22-eval-failure-triage.md`
  - 목표: 확장 평가셋 full eval에서 드러난 실패 케이스를 분류하고 우선 개선 대상을 정한다.
  - 상태: Completed

### Eval Source Drift Calibration

- `2026-05-22-eval-source-drift-calibration.md`
  - 목표: 확장 corpus 기준으로 남은 `tc-04`, `tc-06` 실패를 정리해 평가셋 정의와 keyword 기준을 안정화한다.
  - 상태: Completed

### Source Drift Regression Guard

- `2026-05-22-source-drift-regression-guard.md`
  - 목표: 신규 문서 추가 또는 평가셋 확장 후 source drift를 자동으로 발견할 수 있는 regression guard 후보를 검토한다.
  - 상태: Completed

### Source Drift Watch Case Review

- `2026-05-22-watch-case-review.md`
  - 목표: source drift 리포트의 watch case를 검토해 평가셋 relevant source를 더 좁힐지, 현 상태를 유지할지 결정한다.
  - 상태: Completed

### Source Scope Policy

- `2026-05-22-source-scope-policy.md`
  - 목표: 평가셋의 `relevant_sources` 범위를 어떻게 정의할지 기준을 정한다.
  - 상태: Active

### Follow-Up Candidates

- 런타임 환경 복구와 smoke test 계획
- 평가 파이프라인 실제 실행과 기준선 재확인
- 문서 명칭 정리와 아키텍처 문서 통합
- Phase 14 수준의 정확도와 faithfulness 평가 계획 재수립
- 답변 형식 안정화를 위한 프롬프트 보정 실험

## Active Plans

- `exec-plans/active/2026-05-22-source-scope-policy.md`

## Completed Plans

- `exec-plans/completed/2026-05-12-bootstrap-ragsystem-codex.md`
- `exec-plans/completed/2026-05-12-runtime-validation.md`
- `exec-plans/completed/2026-05-13-cross-encoder-offline.md`
- `exec-plans/completed/2026-05-13-architecture-doc-consolidation.md`
- `exec-plans/completed/2026-05-13-quality-baseline-improvement.md`
- `exec-plans/completed/2026-05-13-eval-harness-alignment.md`
- `exec-plans/completed/2026-05-13-answer-quality-improvement.md`
- `exec-plans/completed/2026-05-13-eval-accuracy-calibration.md`
- `exec-plans/completed/2026-05-13-partial-answer-policy.md`
- `exec-plans/completed/2026-05-13-github-actions-ci.md`
- `exec-plans/completed/2026-05-14-search-quality-improvement.md`
- `exec-plans/completed/2026-05-14-next-quality-iteration.md`
- `exec-plans/completed/2026-05-14-eval-case-alignment.md`
- `exec-plans/completed/2026-05-14-next-search-quality-experiment.md`
- `exec-plans/completed/2026-05-14-retrieval-metric-normalization.md`
- `exec-plans/completed/2026-05-14-residual-answer-quality-analysis.md`
- `exec-plans/completed/2026-05-14-answer-format-prompt-experiment.md`
- `exec-plans/completed/2026-05-14-faithfulness-eval-stability.md`
- `exec-plans/completed/2026-05-15-faithfulness-context-selection.md`
- `exec-plans/completed/2026-05-15-residual-keyword-accuracy.md`
- `exec-plans/completed/2026-05-15-eval-generalization-review.md`
- `exec-plans/completed/2026-05-22-eval-set-expansion.md`
- `exec-plans/completed/2026-05-22-eval-failure-triage.md`
- `exec-plans/completed/2026-05-22-eval-source-drift-calibration.md`
- `exec-plans/completed/2026-05-22-source-drift-regression-guard.md`
- `exec-plans/completed/2026-05-22-watch-case-review.md`
