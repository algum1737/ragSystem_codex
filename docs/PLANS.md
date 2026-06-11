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
  - 상태: Completed

### Watch Case Split

- `2026-05-28-watch-case-split.md`
  - 목표: source scope policy에 따라 broad watch case를 목적별 평가 케이스로 분리할지 결정한다.
  - 상태: Completed

### TC06 Source Scope Review

- `2026-05-28-tc06-source-scope-review.md`
  - 목표: `tc-06` 분쟁 해결 케이스의 `relevant_sources` 범위를 source scope policy 기준으로 재검토한다.
  - 상태: Completed

### Location Dispute Case Review

- `2026-05-28-location-dispute-case-review.md`
  - 목표: 위치기반서비스 분쟁 해결 절차를 별도 hard case로 추가할지 검토한다.
  - 상태: Completed

### Source Drift CI Promotion

- `2026-05-28-source-drift-ci-promotion.md`
  - 목표: source drift report를 CI 또는 정적 검증 루프에 승격할지 검토한다.
  - 상태: Completed

### Ubuntu Deployment Runtime Hardening

- `2026-05-29-ubuntu-deployment-runtime-hardening.md`
  - 목표: Ubuntu 20.04 서버 수동 배포 중 확인한 Python, SQLite, GPU/PyTorch 런타임 이슈를 재배포 가능한 운영 절차로 문서화한다.
  - 상태: Completed

### PR 28 Merge Follow-Up

- `2026-05-29-pr-28-merge-followup.md`
  - 목표: PR #28의 CI 통과 상태를 바탕으로 사용자 승인 후 머지와 후속 handoff 정리를 수행한다.
  - 상태: Completed

### Ubuntu Server Runtime Verification

- `2026-05-29-ubuntu-server-runtime-verification.md`
  - 목표: 머지된 배포 호환 변경을 기준으로 Ubuntu 서버 런타임 상태를 재확인하고 필요한 후속 운영 작업을 정리한다.
  - 상태: Completed

### Operating Model Default Policy

- `2026-05-29-operating-model-default-policy.md`
  - 목표: 운영 서버 모델 상태와 코드 기본값 차이를 정리하고 기본 모델 운영 정책을 결정한다.
  - 상태: Completed

### Ubuntu Default Model Redeploy Verification

- `2026-05-29-ubuntu-default-model-redeploy-verification.md`
  - 목표: 코드 기본 모델 `gemma4:26b` 변경이 Ubuntu 서버 재배포 또는 서비스 재시작 시 의도대로 적용되는지 확인한다.
  - 상태: Completed

### Performance Tuning Baseline

- `2026-05-29-performance-tuning-baseline.md`
  - 목표: 성능 튜닝 전 기준선 full eval을 고정하고 1차 튜닝 후보를 결정한다.
  - 상태: Completed

### Residual Tuning Case Review

- `2026-05-29-residual-tuning-case-review.md`
  - 목표: 안정화 기준 통과 이후 남은 `tc-04`, `tc-17` 케이스의 추가 튜닝 필요 여부를 결정한다.
  - 상태: Completed

### TC04 Faithfulness And TC17 Source Scope

- `2026-06-01-tc04-faithfulness-tc17-source-scope.md`
  - 목표: `tc-04` faithfulness와 `tc-17` source scope를 좁게 보정한다.
  - 상태: Completed

### Observability And Langfuse Review

- `2026-06-01-observability-langfuse-review.md`
  - 목표: Langfuse 같은 LLM observability 도구 도입 필요성과 최소 범위를 검토한다.
  - 상태: Completed

### Local Observability Trace Schema

- `2026-06-02-local-observability-trace-schema.md`
  - 목표: Langfuse 도입 전 privacy-safe local trace sink를 구현한다.
  - 상태: Completed

### Trace Runtime Verification

- `2026-06-02-trace-runtime-verification.md`
  - 목표: Ubuntu 서버에서 local trace sink가 systemd API 서비스와 eval 실행에서 의도대로 동작하는지 검증한다.
  - 상태: Completed

### LLM Latency Triage

- `2026-06-02-llm-latency-triage.md`
  - 목표: 운영 trace에서 확인된 `gemma4:26b` LLM 생성 지연을 분류하고 성능 튜닝 후보를 정한다.
  - 상태: Completed

### Operating Model Latency Experiment

- `2026-06-02-operating-model-latency-experiment.md`
  - 목표: 운영 기본 모델을 `gemma3:12b`로 전환할지 판단하기 위해 latency와 품질을 함께 검증한다.
  - 상태: Completed

### Gemma3 Quality Gap Review

- `2026-06-02-gemma3-quality-gap-review.md`
  - 목표: `gemma3:12b` 전환 실험에서 하락한 `tc-07`, `tc-11` 품질 gap을 분석하고 기준선 회복 가능성을 판단한다.
  - 상태: Completed

### Gemma3 Top-K 3 Full Eval

- `2026-06-02-gemma3-topk3-full-eval.md`
  - 목표: `gemma3:12b + top_k=3` 조합이 latency 개선과 품질 기준선을 동시에 만족하는지 full eval로 검증한다.
  - 상태: Completed

### Speed Improvement Follow-Up

- `2026-06-04-speed-improvement-followup.md`
  - 목표: `gemma3:12b + top_k=3` 회귀 이후 답변 속도 개선을 위한 다음 운영 후보를 결정한다.
  - 상태: Completed

### Gemma3 Operating Transition

- `2026-06-04-gemma3-operating-transition.md`
  - 목표: 운영 응답 기본 모델을 `gemma3:12b + top_k=5`로 전환할지 승인받고, 승인 시 코드/운영 설정/문서를 일관되게 반영한다.
  - 상태: Completed

### Post Transition Monitoring

- `2026-06-04-post-transition-monitoring.md`
  - 목표: `gemma3:12b + top_k=5` 운영 전환 후 실제 응답 속도와 안정성을 관찰하고 추가 튜닝 필요 여부를 결정한다.
  - 상태: Completed

### Gemma3 Token Cap Experiment

- `2026-06-04-gemma3-token-cap-experiment.md`
  - 목표: `gemma3:12b + top_k=5` 운영 조합에서 답변 길이 제한이 latency를 줄이면서 품질을 유지하는지 검증한다.
  - 상태: Completed

### Gemma3 Transition Wrap-Up

- `2026-06-05-gemma3-transition-wrapup.md`
  - 목표: `feature/gemma3-operating-transition` 브랜치의 운영 전환 변경분을 검토하고 커밋/PR 진행 여부를 결정한다.
  - 상태: Completed

### Gemma3 PR Follow-Up

- `2026-06-05-gemma3-pr-followup.md`
  - 목표: `feature/gemma3-operating-transition` 브랜치의 운영 전환 변경분을 커밋하고 PR을 생성한 뒤, PR 상태와 남은 후속 작업을 추적한다.
  - 상태: Completed

### Local Resource Status Panel

- `2026-06-08-local-resource-status-panel.md`
  - 목표: 로컬 FastAPI와 Streamlit UI에 CPU/GPU/Ollama 적재 상태를 확인할 수 있는 리소스 상태 카테고리를 추가한다.
  - 상태: Completed

### GPU Usage Heatmap

- `2026-06-08-gpu-usage-heatmap.md`
  - 목표: Streamlit 시스템 탭에서 GitHub contributions 그래프처럼 GPU별 사용량 히스토리를 heatmap으로 확인할 수 있게 한다.
  - 상태: Completed

### Server Resource Panel Deploy

- `2026-06-08-server-resource-panel-deploy.md`
  - 목표: 로컬에서 구현한 CPU/GPU/Ollama 리소스 상태 패널과 GPU 사용량 heatmap을 Ubuntu 서버에 반영하고 런타임에서 동작을 확인한다.
  - 상태: Completed

### Concise Answer Prompt Experiment

- `2026-06-08-concise-answer-prompt-experiment.md`
  - 목표: `gemma3:12b + top_k=5` 운영 조합에서 답변 길이를 줄여 LLM 생성 시간을 낮출 수 있는 concise-answer prompt 후보를 검증한다.
  - 상태: Completed

### Refined Concise Bullet Prompt

- `2026-06-08-refined-concise-bullet-prompt.md`
  - 목표: `concise_bullet` 실험 결과를 바탕으로 불필요한 no-answer 문장을 줄인 운영 프롬프트 후보를 검증한다.
  - 상태: Completed

### Selective Concise Answer Mode

- `2026-06-09-selective-concise-answer-mode.md`
  - 목표: 기본 프롬프트를 교체하지 않고 사용자가 빠른 요약 답변을 원할 때만 선택적으로 concise prompt를 적용하는 안전한 답변 모드를 설계한다.
  - 상태: Completed

### Selective Concise Mode Follow-Up

- `2026-06-09-selective-concise-mode-followup.md`
  - 목표: 선택형 concise answer mode 구현 변경분을 커밋하고, 필요 시 원격 반영과 후속 확인을 진행한다.
  - 상태: Completed

### Push And CI Verification

- `2026-06-09-push-and-ci-verification.md`
  - 목표: 로컬 `main`에 누적된 커밋을 원격에 push하고 GitHub Actions 상태를 확인한다.
  - 상태: Completed

### Post Deploy Monitoring

- `2026-06-09-post-deploy-monitoring.md`
  - 목표: 선택형 concise answer mode가 원격 반영된 뒤 운영 API/Web 상태와 사용자-facing 동작을 짧게 모니터링하고 다음 개선 후보를 정한다.
  - 상태: Completed

### Concise Mode Trace Review

- `2026-06-09-concise-mode-trace-review.md`
  - 목표: 선택형 `concise` answer mode의 실제 사용 trace를 모아 빠른 요약 모드가 별도 경량 평가셋이나 추가 UX 보강이 필요한지 판단한다.
  - 상태: Completed

### Concise Lightweight Eval Set

- `2026-06-09-concise-lightweight-eval-set.md`
  - 목표: 선택형 `concise` answer mode가 짧은 답변을 만들면서 필수 근거와 예외사항을 누락하지 않는지 확인할 수 있는 경량 평가셋과 판정 기준을 정의한다.
  - 상태: Completed

### Concise Lightweight Eval Harness

- `2026-06-10-concise-lightweight-eval-harness.md`
  - 목표: 문서로 정의한 concise mode 경량 평가셋을 실행 가능한 eval harness로 반영한다.
  - 상태: Completed

### Concise Eval Server Verification

- `2026-06-10-concise-eval-server-verification.md`
  - 목표: 로컬에서 구현한 concise lightweight eval harness를 Ubuntu 서버에 반영하고 운영 GPU/Ollama 환경에서 smoke 결과를 확인한다.
  - 상태: Completed

### Concise Eval CI Promotion

- `2026-06-10-concise-eval-ci-promotion.md`
  - 목표: concise lightweight eval을 CI 또는 배포 후 수동 검증 루프에 승격할지 결정한다.
  - 상태: Completed

### Concise Eval Runbook Script

- `2026-06-10-concise-eval-runbook-script.md`
  - 목표: 서버 concise lightweight eval smoke를 반복 가능하게 실행할 수 있도록 runbook 또는 script를 정리한다.
  - 상태: Completed

### Concise 06 Failure Triage

- `2026-06-10-concise-06-failure-triage.md`
  - 목표: runbook script가 감지한 `concise-06` 실패를 분석해 prompt 문제인지 평가 기준 문제인지 결정한다.
  - 상태: Completed

### Concise 06 Stability Fix

- `2026-06-11-concise-06-stability-fix.md`
  - 목표: `concise-06`가 통지 방법과 사전/사후 예외를 안정적으로 보존하도록 평가 rule과 concise prompt 보강 후보를 좁게 적용하고 검증한다.
  - 상태: Completed

### Concise Post-Fix Monitoring

- `2026-06-11-concise-post-fix-monitoring.md`
  - 목표: `concise-06` 안정화 변경 이후 운영 trace와 짧은 smoke를 확인해 concise prompt 보강이 실제 운영 질문에서 불필요한 bullet을 줄이고 필수 예외를 유지하는지 점검한다.
  - 상태: Active

### Eval Model Tuning Policy

- `2026-05-29-eval-model-tuning-policy.md`
  - 목표: 운영 모델과 평가 기준 모델을 분리하고 튜닝 기준선 절차를 문서화한다.
  - 상태: Completed

### Follow-Up Candidates

- 런타임 환경 복구와 smoke test 계획
- 평가 파이프라인 실제 실행과 기준선 재확인
- 문서 명칭 정리와 아키텍처 문서 통합
- Phase 14 수준의 정확도와 faithfulness 평가 계획 재수립
- 답변 형식 안정화를 위한 프롬프트 보정 실험

## Active Plans

- `exec-plans/active/2026-06-11-concise-post-fix-monitoring.md`

## Completed Plans

- `exec-plans/completed/2026-06-11-concise-06-stability-fix.md`
- `exec-plans/completed/2026-06-10-concise-06-failure-triage.md`
- `exec-plans/completed/2026-06-10-concise-eval-runbook-script.md`
- `exec-plans/completed/2026-06-10-concise-eval-ci-promotion.md`
- `exec-plans/completed/2026-06-10-concise-eval-server-verification.md`
- `exec-plans/completed/2026-06-10-concise-lightweight-eval-harness.md`
- `exec-plans/completed/2026-06-09-concise-lightweight-eval-set.md`
- `exec-plans/completed/2026-06-09-concise-mode-trace-review.md`
- `exec-plans/completed/2026-06-09-post-deploy-monitoring.md`
- `exec-plans/completed/2026-06-09-push-and-ci-verification.md`
- `exec-plans/completed/2026-06-09-selective-concise-mode-followup.md`
- `exec-plans/completed/2026-06-09-selective-concise-answer-mode.md`
- `exec-plans/completed/2026-06-08-refined-concise-bullet-prompt.md`
- `exec-plans/completed/2026-06-08-concise-answer-prompt-experiment.md`
- `exec-plans/completed/2026-06-05-gemma3-pr-followup.md`
- `exec-plans/completed/2026-06-08-server-resource-panel-deploy.md`
- `exec-plans/completed/2026-06-08-gpu-usage-heatmap.md`
- `exec-plans/completed/2026-06-08-local-resource-status-panel.md`
- `exec-plans/completed/2026-06-05-gemma3-transition-wrapup.md`
- `exec-plans/completed/2026-06-04-gemma3-token-cap-experiment.md`
- `exec-plans/completed/2026-06-04-post-transition-monitoring.md`
- `exec-plans/completed/2026-06-04-gemma3-operating-transition.md`
- `exec-plans/completed/2026-06-04-speed-improvement-followup.md`
- `exec-plans/completed/2026-06-02-gemma3-topk3-full-eval.md`
- `exec-plans/completed/2026-06-02-gemma3-quality-gap-review.md`
- `exec-plans/completed/2026-06-02-operating-model-latency-experiment.md`
- `exec-plans/completed/2026-06-02-llm-latency-triage.md`
- `exec-plans/completed/2026-06-02-trace-runtime-verification.md`
- `exec-plans/completed/2026-06-02-local-observability-trace-schema.md`
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
- `exec-plans/completed/2026-05-22-source-scope-policy.md`
- `exec-plans/completed/2026-05-28-watch-case-split.md`
- `exec-plans/completed/2026-05-28-tc06-source-scope-review.md`
- `exec-plans/completed/2026-05-28-location-dispute-case-review.md`
- `exec-plans/completed/2026-05-28-source-drift-ci-promotion.md`
- `exec-plans/completed/2026-05-29-ubuntu-deployment-runtime-hardening.md`
- `exec-plans/completed/2026-05-29-pr-28-merge-followup.md`
- `exec-plans/completed/2026-05-29-ubuntu-server-runtime-verification.md`
- `exec-plans/completed/2026-05-29-operating-model-default-policy.md`
- `exec-plans/completed/2026-05-29-ubuntu-default-model-redeploy-verification.md`
- `exec-plans/completed/2026-05-29-eval-model-tuning-policy.md`
- `exec-plans/completed/2026-05-29-performance-tuning-baseline.md`
- `exec-plans/completed/2026-05-29-residual-tuning-case-review.md`
- `exec-plans/completed/2026-06-01-tc04-faithfulness-tc17-source-scope.md`
- `exec-plans/completed/2026-06-01-observability-langfuse-review.md`
