# Handoff

이 문서는 다음 세션이 현재 상태를 빠르게 이어받기 위한 인계 문서다.

## Read First

1. `AGENTS.md`
2. `README.md`
3. `ARCHITECTURE.md`
4. `docs/index.md`
5. `docs/PLANS.md`
6. `docs/product-specs/terms-rag-system.md`
7. `docs/manual-deployment-guide.md`
8. `docs/references/quality-baseline-analysis.md`
9. `docs/references/answer-quality-analysis.md`
10. `docs/references/search-quality-improvement.md`
11. `docs/references/2026-05-14-work-report.md`
12. `docs/references/2026-05-14-before-after.md`
13. `docs/references/2026-05-14-next-quality-iteration-analysis.md`
14. `docs/references/2026-05-14-eval-case-alignment.md`
15. `docs/exec-plans/completed/2026-05-14-eval-case-alignment.md`
16. `docs/exec-plans/completed/2026-05-14-next-quality-iteration.md`
17. `docs/exec-plans/completed/2026-05-14-search-quality-improvement.md`
18. `docs/exec-plans/completed/2026-05-14-next-search-quality-experiment.md`
19. `docs/exec-plans/completed/2026-05-14-retrieval-metric-normalization.md`
20. `docs/references/2026-05-14-search-quality-ceiling-analysis.md`
21. `docs/references/2026-05-14-retrieval-metric-normalization.md`
22. `docs/references/2026-05-14-residual-answer-quality-analysis.md`
23. `docs/exec-plans/completed/2026-05-14-residual-answer-quality-analysis.md`
24. `docs/exec-plans/completed/2026-05-14-answer-format-prompt-experiment.md`
25. `docs/references/2026-05-15-faithfulness-eval-stability.md`
26. `docs/exec-plans/completed/2026-05-14-faithfulness-eval-stability.md`
27. `docs/exec-plans/completed/2026-05-15-faithfulness-context-selection.md`
28. `docs/references/2026-05-15-residual-keyword-accuracy.md`
29. `docs/exec-plans/completed/2026-05-15-residual-keyword-accuracy.md`
30. `docs/exec-plans/completed/2026-05-15-eval-generalization-review.md`
31. `docs/references/2026-05-22-eval-generalization-review.md`
32. `docs/exec-plans/completed/2026-05-22-eval-set-expansion.md`
33. `docs/references/2026-05-22-eval-set-expansion-result.md`
34. `docs/exec-plans/completed/2026-05-22-eval-failure-triage.md`
35. `docs/references/2026-05-22-eval-source-drift-calibration.md`
36. `docs/exec-plans/completed/2026-05-22-eval-source-drift-calibration.md`
37. `docs/exec-plans/completed/2026-05-22-source-drift-regression-guard.md`
38. `docs/references/2026-05-22-source-drift-regression-report.md`
39. `docs/references/2026-05-22-watch-case-review.md`
40. `docs/exec-plans/completed/2026-05-22-watch-case-review.md`
41. `docs/references/2026-05-28-source-scope-policy.md`
42. `docs/references/2026-05-28-watch-case-split-result.md`
43. `docs/references/2026-05-28-watch-case-split-source-drift-report.md`
44. `docs/exec-plans/completed/2026-05-28-watch-case-split.md`
45. `docs/references/2026-05-28-tc06-source-scope-review.md`
46. `docs/references/2026-05-28-tc06-source-scope-report.md`
47. `docs/exec-plans/completed/2026-05-28-tc06-source-scope-review.md`
48. `docs/references/2026-05-28-location-dispute-case-review.md`
49. `docs/references/2026-05-28-location-dispute-case-report.md`
50. `docs/exec-plans/completed/2026-05-28-location-dispute-case-review.md`
51. `docs/exec-plans/completed/2026-05-28-source-drift-ci-promotion.md`
52. `docs/exec-plans/completed/2026-05-13-github-actions-ci.md`
53. `docs/exec-plans/completed/2026-05-13-partial-answer-policy.md`
54. `docs/exec-plans/completed/2026-05-13-eval-accuracy-calibration.md`
55. `docs/exec-plans/completed/2026-05-13-answer-quality-improvement.md`
56. `docs/exec-plans/completed/2026-05-13-eval-harness-alignment.md`
57. `docs/exec-plans/completed/2026-05-13-quality-baseline-improvement.md`
58. `docs/exec-plans/completed/2026-05-13-architecture-doc-consolidation.md`
59. `docs/exec-plans/completed/2026-05-12-bootstrap-ragsystem-codex.md`
60. `docs/exec-plans/completed/2026-05-12-runtime-validation.md`
61. `docs/exec-plans/completed/2026-05-13-cross-encoder-offline.md`

## Current Baseline

- 현재 브랜치: `git branch --show-current`로 확인
- 기준 커밋: `git rev-parse --short HEAD`로 확인
- 제품/서비스: 로컬 RAG 기반 문서 초안 생성 시스템
- 현재 상태: `ragSystem` 소스 복사, 하네스 문서 전환, 런타임 검증, 임베딩/Cross-Encoder 오프라인 캐시 검증 완료
- 주요 목표: `.paul` 기반 운영 지식을 `docs/` 체계로 옮기고 이후 개선 작업을 Codex 방식으로 이어간다

## Latest Update

- Langfuse 도입 전 단계로 privacy-safe local JSONL trace sink를 구현했다.
- trace는 기본 off이며 `RAG_TRACE_ENABLED=true`일 때만 기록된다.
- 기본 경로는 `./logs/rag_traces.jsonl`이고 `RAG_TRACE_PATH`로 변경할 수 있다.
- API `/query`, CLI query, `RAGEngine.query()`는 route, trace id, model, top_k, source path, latency, answer length를 기록한다.
- eval pipeline은 `eval.case` event로 `case_id`, model, top_k, retrieved sources, query latency, score를 기록한다.
- full prompt, full answer, chunk text는 기본 저장하지 않는다.
- 구현 결과: `docs/references/2026-06-02-local-observability-trace-result.md`
- 완료 plan: `docs/exec-plans/completed/2026-06-02-local-observability-trace-schema.md`
- 현재 active plan: `docs/exec-plans/active/2026-06-09-selective-concise-answer-mode.md`
- Ubuntu 서버 `10.10.220.5`에는 최신 trace 코드가 배포됐고 서버 venv compile, 임시 API trace smoke, eval trace smoke가 통과했다.
- 서버에는 `/home/ragadmin/apply-ragsystem-trace.sh`가 업로드되어 있다.
- `sudo bash /home/ragadmin/apply-ragsystem-trace.sh` 실행 후 운영 8000 서비스에서 `/opt/ragSystem_codex/logs/rag_traces.jsonl` 생성을 확인했다.
- 최신 운영 query trace는 `api.query`, model `gemma4:26b`, total 약 218초, LLM 약 208초로 기록됐다.
- LLM latency triage 결과, retrieval은 약 10초이고 `gemma4:26b` LLM 구간이 208~351초 병목이다.
- `gemma4:26b`는 Ollama 기준 `15%/85% CPU/GPU`로 일부 CPU offload가 발생한다.
- 같은 RAG CLI 경로에서 `gemma3:12b`는 total 약 26.3초, LLM 약 16.5초였다.
- `gemma4` 계열은 LangChain 경로에서 `max_tokens` 적용 시 빈 응답 리스크가 있어 단순 token cap 패치는 보류한다.
- `/model` endpoint가 실제 RAGEngine 내부 모델을 바꾸도록 `RAGEngine.llm` setter를 추가했다.
- `gemma3:12b` 운영 API 임시 전환 smoke는 total 약 29.0초, LLM 약 19.2초였다.
- `gemma3:12b` full eval 결과는 `accuracy_mean=0.9891`, `faithfulness_mean=0.9565`, `not_found_success_rate=1.0`이다.
- 실험 후 운영 API는 `gemma4:26b`로 복구했다.
- `tc-07` gap은 실제 답변 품질보다 fixed keyword `면책` 표현 불일치에 가깝다.
- `tc-11` gap은 실제 answer grounding 문제로, source 혼합과 불필요한 미확인 섹션이 확인됐다.
- 프롬프트 후보 3종은 일부 회복했지만 `tc-07` faithfulness 회귀가 있어 보류했다.
- `gemma3:12b + top_k=3`은 `tc-07`, `tc-11` 2케이스 smoke에서 모두 `accuracy=1.0`, `faithfulness=1.0`을 기록했다.
- `gemma3:12b + top_k=3` full eval을 실행했다.
- 리포트는 `eval/results/eval_20260604_171559.json`이고 결과 문서는 `docs/references/2026-06-04-gemma3-topk3-full-eval-result.md`다.
- 결과는 `accuracy_mean=0.942`, `faithfulness_mean=0.9565`, `source_recall@k_mean=0.8449`, `not_found_success_rate=1.0`이다.
- trace `eval.case` 23건 기준 query_total은 mean 약 8.7초, median 약 8.5초, max 약 20.1초였다.
- `top_k=3`은 빠르지만 `gemma3:12b + top_k=5` 기준선 대비 source recall과 accuracy가 회귀해 운영 전환 후보로 채택하지 않는다.
- 서버 API `/health`는 작업 시점에 `model=gemma4:e4b`였다. 이번 eval은 CLI `--model gemma3:12b --top-k 3` 경로로 실행했고 운영 API 모델은 변경하지 않았다.
- 속도 개선 후속 비교를 완료했고 결과 문서는 `docs/references/2026-06-04-speed-improvement-followup-result.md`다.
- 현재 서버 API `/health`는 `model=gemma4:e4b`, `ollama ps`는 상주 모델 없음, GPU 0은 약 3.5GB 사용 상태였다.
- API trace 평균은 `gemma3:12b + top_k=5` 약 23.8초, `gemma4:e4b + top_k=5` 약 26.1초, `gemma4:26b + top_k=5` 약 221.4초였다.
- 다음 실행 후보는 `gemma3:12b + top_k=5` 운영 전환으로 좁혔다.
- `gemma3:12b + top_k=5` 운영 전환을 완료했다.
- 코드 기본 모델, CLI 기본 모델, Streamlit 추천 모델, 아키텍처 문서, 배포/기동 가이드를 `gemma3:12b` 기준으로 갱신했다.
- 서버 배포본에도 변경 파일을 반영했고 서버 compile이 통과했다.
- 서버 API는 `/model` endpoint로 `gemma4:e4b`에서 `gemma3:12b`로 전환했다.
- 대표 API query smoke는 status 200, elapsed 약 22.05초, answer length 998, source 5개였다.
- trace는 `api.query`, `model=gemma3:12b`, `top_k=5`, total 약 22.0초, LLM 약 21.9초, retrieval 약 0.14초로 기록됐다.
- `ollama ps`는 `gemma3:12b`, `100% GPU`, context 4096을 표시했다.
- API 프로세스 재시작 후 `/health`는 `model=gemma3:12b`, `/stats`는 `count=318`을 반환했다.
- Streamlit 재시작 후 HTTP 200을 확인했다.
- 결과 문서는 `docs/references/2026-06-04-gemma3-operating-transition-result.md`다.
- 전환 후 모니터링을 완료했고 결과 문서는 `docs/references/2026-06-04-post-transition-monitoring-result.md`다.
- 서버 상태는 `/health model=gemma3:12b`, `/stats count=318`, Streamlit HTTP 200이었다.
- 추가 대표 query 2건은 약 24.78초와 7.72초였고 둘 다 source 5개를 반환했다.
- 최신 trace 기준 전환 후 주요 3건은 total 약 22.0초, 24.8초, 7.7초였다.
- LLM 구간이 여전히 주 병목이며, 위치기반서비스 추가 query는 embedding/rerank cold load로 retrieval 약 9.6초가 걸렸다.
- 추가 query 후 `ollama ps`는 `gemma3:12b`, `100% GPU`, context 4096을 표시했다.
- 후속 후보로 `gemma3:12b` 전용 `max_tokens`/`num_predict` 제한 실험을 진행했다.
- API embedding/reranker CPU 모드와 `top_k=4`는 보조 후보로 보류한다.
- `gemma3:12b` token cap 실험을 완료했고 결과 문서는 `docs/references/2026-06-05-gemma3-token-cap-experiment-result.md`다.
- 128은 accuracy 회귀, 256/384/512/768은 답변 절단 리스크, 1024는 latency 개선 부족으로 제외했다.
- 기본 `num_predict`/`max_tokens` cap은 채택하지 않는다.
- 실험 중 임시 반영했던 token cap 구현은 로컬과 서버에서 되돌렸다.
- 서버 API는 `DEFAULT_MODEL=gemma3:12b`, 기본 token cap 없음, `/health model=gemma3:12b` 상태다.
- Gemma3 transition wrap-up에서 변경 범위, 로컬 검증, 서버 `/health`를 재확인했다.
- wrap-up plan은 completed로 이동했고 결과는 `docs/exec-plans/completed/2026-06-05-gemma3-transition-wrapup.md`에 기록했다.
- 다음 active plan은 `docs/exec-plans/active/2026-06-05-gemma3-pr-followup.md`다.
- 현재 브랜치 변경분은 `운영 기본 모델을 gemma3로 전환` 커밋으로 정리했다.
- PR #29를 생성했다: https://github.com/algum1737/ragSystem_codex/pull/29
- GitHub Actions `Static checks`는 코드 실행 전 차단됐다. run annotation은 계정 결제 실패 또는 spending limit 증가 필요를 표시했다.
- 다음 작업은 GitHub Actions 과금/한도 문제 해결 후 PR CI를 재실행하고 리뷰 피드백을 확인하는 것이다.
- 로컬 리소스 상태 패널을 구현했다.
- FastAPI `/runtime/resources` endpoint는 CPU/RAM, `nvidia-smi` 기반 GPU 상태, `ollama ps` 기반 적재 모델 상태를 반환한다.
- Streamlit 시스템 탭에는 `리소스 상태` 카테고리를 추가했다.
- 로컬 smoke 결과: `/runtime/resources` JSON 반환, `/health model=gemma3:12b`, Streamlit `_stcore/health=ok`.
- 완료 plan: `docs/exec-plans/completed/2026-06-08-local-resource-status-panel.md`
- GPU 사용량 heatmap을 로컬 구현했다.
- FastAPI `/runtime/resources/history` endpoint는 5초 주기 in-memory GPU 샘플을 반환한다.
- Streamlit 시스템 탭에서는 `GPU 사용률`과 `VRAM 사용률` 중 하나를 선택해 GPU별 heatmap을 표시한다.
- 로컬 Mac에는 `nvidia-smi`가 없어 실제 GPU heatmap 데이터는 비어 있으며, Ubuntu 서버 반영 후 GPU별 utilization/VRAM 샘플 표시를 확인해야 한다.
- 완료 plan: `docs/exec-plans/completed/2026-06-08-gpu-usage-heatmap.md`
- 리소스 상태 패널과 GPU heatmap을 Ubuntu 서버에 반영했다.
- 서버 systemd 서비스 PATH가 venv로 제한되어 `nvidia-smi`/`ollama`를 찾지 못하는 문제는 앱 코드에서 표준 절대 경로 fallback으로 해결했다.
- 서버 `/runtime/resources`는 GPU 0/1 `NVIDIA GeForce RTX 2080 Ti`, Ollama `gemma3:12b`, `100% GPU`, context `4096`을 반환한다.
- 서버 `/runtime/resources/history`는 5초 주기 샘플을 반환하며, 대표 RAG 질의 중 GPU 1 utilization `87.0%`, GPU 0/1 VRAM `31.3%`/`81.3%` 샘플을 확인했다.
- Streamlit 서버 health는 `ok`다.
- 완료 plan: `docs/exec-plans/completed/2026-06-08-server-resource-panel-deploy.md`
- 리소스 상태 패널/GPU heatmap/LLM latency HTML 문서는 `리소스 상태 패널과 GPU 히트맵 추가` 커밋으로 정리했다.
- 로컬 Homebrew Ollama 서비스는 `brew services stop ollama`로 정지했고, `brew services list`에서 `ollama none` 상태를 확인했다.
- PR #29를 main에 머지했고 로컬 main도 `origin/main`과 동기화했다.
- PR #29 merge commit은 `gh pr view 29 --json mergeCommit` 또는 `git log`로 확인한다.
- PR follow-up plan은 completed로 이동했다.
- concise-answer prompt 후보 검증을 완료했다.
- 결과 문서는 `docs/references/2026-06-08-concise-answer-prompt-experiment-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-08-concise-answer-prompt-experiment.md`다.
- 서버 final trace는 `/opt/ragSystem_codex/logs/concise_prompt_experiment_final_20260608.jsonl`이다.
- warmed benchmark 기준 baseline 평균 total은 약 11.2초, `concise_bullet`은 약 6.1초, `concise_summary`는 약 4.9초였다.
- `concise_summary`가 가장 빠르지만 관련성이 낮은 문장과 불필요한 미확인 문장 리스크가 있어 그대로 채택하지 않는다.
- refined concise bullet 후보 검증을 완료했다.
- 결과 문서는 `docs/references/2026-06-09-refined-concise-bullet-prompt-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-08-refined-concise-bullet-prompt.md`다.
- `refined_concise_bullet` v4는 smoke 기준 평균 total 약 5.1초, LLM 약 5.0초로 빨랐다.
- 하지만 운영 기본 프롬프트 임시 반영 후 full eval에서 `accuracy_mean=0.8804`, `not_found_success_rate=0.0` 회귀가 발생했다.
- 서버 full eval 리포트는 `/opt/ragSystem_codex/eval/results/eval_20260609_095553.json`이다.
- 회귀 확인 후 로컬과 서버의 기본 `PROMPT_TEMPLATE`는 기존 버전으로 원복했다.
- 서버 API는 `/health model=gemma3:12b` 정상 상태다.
- 선택형 concise answer mode 설계를 완료했다.
- 설계 문서는 `docs/references/2026-06-09-selective-concise-answer-mode-design.md`다.
- 결론: 자동 라우팅은 v1에서 배제하고, 사용자 명시 선택형 `answer_mode=standard|concise`로 간다.
- 선택형 concise answer mode 구현과 서버 반영을 완료했다.
- 결과 문서는 `docs/references/2026-06-09-selective-concise-answer-mode-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-09-selective-concise-answer-mode.md`다.
- 기본값은 `standard`이며 기존 `PROMPT_TEMPLATE`를 유지한다.
- `concise`는 명시적 요청에서만 refined concise bullet prompt를 사용한다.
- API `QueryRequest.answer_mode`, CLI `--answer-mode`, Streamlit query UI의 `표준`/`빠른 요약` 선택을 추가했다.
- `RAGEngine.query(answer_mode=...)`는 per-call prompt를 선택하고, module-level `PROMPT_TEMPLATE`를 요청 중 변경하지 않는다.
- trace metadata에는 `answer_mode`가 기록된다.
- 서버 API/Web health는 정상이고, API smoke에서 `standard`/`concise` 모두 status 200을 확인했다.
- standard full eval은 `/opt/ragSystem_codex/eval/results/eval_20260609_110223.json`이며 `accuracy_mean=0.9891`, `faithfulness_mean=0.9565`, `not_found_success_rate=1.0`이다.
- 선택형 concise mode 구현 변경분은 follow-up plan에서 커밋 대상으로 정리했다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-09-selective-concise-mode-followup.md`다.
- 로컬 `main`의 ahead 커밋 3개를 `origin/main`에 push했다.
- GitHub Actions `CI`는 push 직후 `completed/success`를 확인했다. 최신 run은 `gh run list --branch main --limit 1`로 확인한다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-09-push-and-ci-verification.md`다.
- 배포 후 모니터링을 완료했다.
- 배포 후 모니터링 결과 정리 커밋을 `origin/main`에 push했고, GitHub Actions `CI`는 push 직후 `completed/success`를 확인했다.
- 서버 API `/health`는 `status=ok`, `model=gemma3:12b`를 반환했다.
- Streamlit `_stcore/health`는 `ok`를 반환했다.
- 운영 API `/query` smoke에서 `standard`/`concise` 모두 status 200, source 5개를 반환했다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-09-post-deploy-monitoring.md`다.
- concise mode trace review를 완료했다.
- 운영 trace `api.query` 성공 이벤트 29건 중 `answer_mode`가 기록된 표본은 `standard` 3건, `concise` 4건이었다.
- 같은 질문 해시 기준 paired sample 3쌍에서 `concise`는 평균 total 5650.12ms, LLM 5536.59ms, answer length 307.33자, source 5개였다.
- 같은 paired sample에서 `standard`는 평균 total 16088.69ms, LLM 12737.12ms, answer length 496.33자, source 5개였다.
- 결과 문서는 `docs/references/2026-06-09-concise-mode-trace-review.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-09-concise-mode-trace-review.md`다.
- concise mode 전용 경량 평가셋과 판정 기준을 문서로 고정했다.
- 경량셋은 `concise-01`부터 `concise-06`까지 6개 케이스로 시작한다.
- 판정 기준은 `required_points` 충족률 0.75 이상, `forbidden_claims` 0건, source 3개 이상, 답변 700자 이하, warmed total latency 12000ms 이하 권장이다.
- no-answer 케이스 `concise-05`는 문서 미확인 또는 직접 근거 부족을 명시해야 하고 결제 주기/금액 변경 조건을 임의 생성하면 실패다.
- 결과 문서는 `docs/references/2026-06-10-concise-lightweight-eval-set.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-09-concise-lightweight-eval-set.md`다.
- concise lightweight eval harness를 구현했다.
- `eval/concise_test_cases.json`을 추가했고 `eval/pipeline.py --concise-lightweight` 실행 경로를 추가했다.
- 로컬 smoke는 `total_cases=6`, `passed_cases=6`, `pass_rate=1.0`, `required_points_score_mean=0.875`, `answer_length_mean=315.0`을 기록했다.
- 로컬 smoke 리포트는 `eval/results/concise_eval_20260610_092710.json`이다.
- trace route `eval.concise`와 `eval.concise.case`에 `answer_mode=concise` metadata가 기록됨을 확인했다.
- 결과 문서는 `docs/references/2026-06-10-concise-lightweight-eval-harness-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-10-concise-lightweight-eval-harness.md`다.
- concise eval harness를 Ubuntu 서버에 반영하고 운영 GPU/Ollama 환경에서 smoke를 실행했다.
- 서버 반영 파일은 `eval/pipeline.py`, `eval/concise_test_cases.json`이다.
- 서버 smoke report는 `/opt/ragSystem_codex/eval/results/concise_eval_20260610_105027.json`이다.
- 서버 smoke summary는 `total_cases=6`, `passed_cases=6`, `pass_rate=1.0`, `required_points_score_mean=0.875`, `answer_length_mean=315.3333`, `query_latency_ms_mean=8483.0783`이다.
- 서버 trace path는 `/opt/ragSystem_codex/logs/concise_lightweight_eval_20260610.jsonl`이고 route `eval.concise`, `eval.concise.case`, metadata `answer_mode=concise`를 확인했다.
- smoke 이후 서버 `/health`는 `{"status":"ok","model":"gemma3:12b"}`다.
- 결과 문서는 `docs/references/2026-06-10-concise-eval-server-verification-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-10-concise-eval-server-verification.md`다.
- concise lightweight eval의 CI/운영 루프 승격 판단을 완료했다.
- GitHub Actions에는 Ollama/Chroma가 필요한 runtime eval을 넣지 않고, `eval/concise_test_cases.json` schema 정적 검증만 추가했다.
- 추가 스크립트는 `scripts/validate_concise_eval_cases.py`다.
- CI workflow에는 `python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json` step을 추가했다.
- 서버 LLM/RAG smoke는 배포 후 수동 검증 루프로 유지한다.
- 결과 문서는 `docs/references/2026-06-10-concise-eval-ci-promotion-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-10-concise-eval-ci-promotion.md`다.
- 서버 concise lightweight eval smoke runbook/script를 정리했다.
- `scripts/run-concise-eval-smoke.sh`를 추가했고, `docs/manual-deployment-guide.md`에 `Concise Eval Smoke` 섹션을 추가했다.
- 서버 `/opt/ragSystem_codex/scripts/run-concise-eval-smoke.sh`에도 script를 반영했다.
- 서버 runbook script는 report와 trace를 생성했고, `concise-06` 실패를 감지해 exit code 1로 종료했다.
- 실패 report는 `/opt/ragSystem_codex/eval/results/concise_eval_20260610_114205.json`이다.
- 실패 원인은 유료서비스 중단/변경 통지 답변에서 통지 수단과 사전/사후 예외 required point가 누락된 것이다.
- 실패 후 서버 `/health`는 `{"status":"ok","model":"gemma3:12b"}`다.
- 결과 문서는 `docs/references/2026-06-10-concise-eval-runbook-script-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-10-concise-eval-runbook-script.md`다.
- `concise-06` 실패 triage를 완료했다.
- 결과 문서는 `docs/references/2026-06-11-concise-06-failure-triage-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-10-concise-06-failure-triage.md`다.
- 결론: primary 원인은 `concise` prompt 안정성 문제이고, secondary 원인은 deterministic rule의 동의 표현 허용 범위 부족이다. retrieval failure는 primary가 아니다.
- 서버 top-5 검색 청크에는 카카오 유료/결제서비스의 사전 통지와 부득이한 경우 사후 통지 근거가 포함됐다.
- 별도 통지 방법 검색에서는 카카오 제6조의 전자우편, 카카오톡 메시지, 팝업, 게시판/공지 근거가 확인됐다.
- 같은 질문의 `concise` 3회 반복 smoke에서 required score가 `0.5`, `0.75`, `0.75`로 흔들렸다.
- `concise-06` 안정화 구현을 완료했다.
- 결과 문서는 `docs/references/2026-06-11-concise-06-stability-fix-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-11-concise-06-stability-fix.md`다.
- `CONCISE_PROMPT_TEMPLATE`은 조건/제한/예외/통지 시점 질문에서 예외 조건을 생략하지 않고, 사전/사후 통지 예외가 있으면 별도 bullet로 쓰도록 보강했다.
- `concise-06` deterministic rule은 `통보`, `명시된 방법`, `약관에 따른 방법`, `미리`, `사후 통보`, `예측 불가능`, `예측할 수 없`, `통제할 수 없`을 좁게 허용한다.
- 서버 `concise-06` 3회 반복 smoke는 모두 통과했고 3회 모두 사전/사후 예외를 보존했다.
- 최종 서버 runbook smoke는 `/opt/ragSystem_codex/eval/results/concise_eval_20260611_102139.json`이며 `total_cases=6`, `passed_cases=6`, `pass_rate=1.0`, `required_points_score_mean=0.9583`이다.
- 운영 API/Web은 systemd `Restart=always` 확인 후 `ragadmin` 소유 프로세스에 `TERM`을 보내 자동 재기동했다. 재기동 후 API `/health`는 `status=ok`, `model=gemma3:12b`, Streamlit health는 `ok`였다.
- 운영 API `/query` concise smoke에서 사전/사후 예외 보존과 무관한 `사용기간`, `청약철회`, `환불` bullet 제거를 확인했다.
- post-fix monitoring을 완료했다.
- 결과 문서는 `docs/references/2026-06-11-concise-post-fix-monitoring-result.md`다.
- 완료 plan은 `docs/exec-plans/completed/2026-06-11-concise-post-fix-monitoring.md`다.
- 서버 API/Web health는 정상이다.
- 최근 `rag_traces.jsonl` 집계는 `api.query=31`, `eval.case=23`, `answer_mode=concise` API 표본 7건이다.
- post-fix 이후 실제 사용자 표본은 아직 부족하고 대부분 작업 smoke 표본이다.
- 표본 부족 보완으로 `concise-06` 운영 API smoke를 1회 실행했고 `answer_length=376`, `source_count=5`, 사전/사후 예외 포함, `사용기간`/`청약철회`/`환불` 무관 bullet 미재발을 확인했다.
- 다음 active plan은 `docs/exec-plans/active/2026-06-11-concise-real-usage-trace-review.md`다.
- real usage trace review 1차 확인 결과 서버 health는 정상이지만 post-fix 이후 실제 사용자 `concise` 표본은 아직 없다.
- 최신 집계는 `total_records=55`, `api.query=32`, `api.answer_mode.concise=7`, `post_fix_concise_count=1`, `post_fix_smoke_like_count=1`, `post_fix_non_smoke_count=0`이다.
- active plan은 완료하지 않고 유지한다.

## Working Rules

- 큰 작업은 구현 전에 `docs/exec-plans/active/`에 실행 계획을 작성한다.
- 실행 계획에는 작업 시작 전에 `Pre-flight checks`, `Automated tests`, `Manual/Runtime QA`, `Skipped/Not Run` 검증 계약을 고정하고 완료 시 `Validation Result`로 결과를 대조한다.
- 작업 완료 시 완료 범위, 남은 작업 여부, 검증 결과를 계획 문서에 남긴다.
- 완료된 계획은 `docs/exec-plans/completed/`로 이동하고 `docs/index.md`와 이 문서를 갱신한다.
- 구현 변경은 사용자가 명시적으로 승인한 경우에만 수행한다.
- 새 실제 작업은 `main`에서 직접 하지 않고 작업 브랜치에서 진행한다.
- 커밋 해시는 이 문서에 고정하지 말고 git 명령으로 확인하게 유지한다.
- PR 생성은 `gh pr create`를 우선 사용해 직접 수행하고, 제목/본문은 한국어로 작성한다.
- PR 본문에는 요약, 변경 사항, 검증 결과, 평가 결과가 있으면 해당 지표, 남은 작업을 포함한다.
- `gh` 사용이 불가능한 경우에만 PR 생성 링크와 입력 내용을 사용자에게 제공한다.

## Recent Progress

- `ragSystem` 프로젝트 코드를 현재 저장소로 복사했다.
- `.venv`, `chroma_db`, 로그, `.paul`, `.claude` 같은 런타임 또는 도구별 상태 디렉터리는 제외했다.
- `template-repo` 기반 `docs/`, `scripts/`, `.githooks/` 골격을 적용했다.
- `.paul`의 프로젝트 정의와 로드맵을 `README.md`, `ARCHITECTURE.md`, `docs/PLANS.md`, 제품 명세와 실행 계획으로 재구성했다.
- `bash scripts/validate-docs.sh` 통과와 플레이스홀더 제거 확인을 마쳤다.
- Git 저장소를 초기화하고 초기 기준 커밋을 만들었다.
- 런타임 검증용 실행 계획을 추가했고 작업 브랜치 `feature/runtime-validation`에서 다음 단계를 시작했다.
- `.venv` 생성과 의존성 설치를 완료했고 `pip check`와 경량 import 검증을 통과했다.
- FastAPI smoke test에서 `multilingual-e5-large` 로컬 캐시 부재로 인해 Hugging Face 접근이 필요했고, 오프라인 환경 때문에 앱 startup이 완료되지 않았다.
- `EmbeddingEngine`을 lazy initialization으로 바꿔 오프라인에서도 FastAPI startup과 `/health` 확인이 가능해졌다.
- Streamlit 앱도 startup과 HTTP 200 응답까지 확인했다.
- eval retrieval smoke test는 코드 오류 없이 실행됐고, 현재는 비어 있는 Chroma DB 때문에 조기 종료한다.
- 임베딩 모델 사전 다운로드 절차를 `docs/references/embedding-model-cache.md`에 문서화했다.
- `multilingual-e5-large` 모델 캐시를 실제로 준비했고, 오프라인 강제 모드에서도 `dim 1024` 로드를 확인했다.
- `SentenceTransformer` import 지연과 stale collection handle 복구를 적용해 `/stats`와 retrieval eval이 정상화됐다.
- 전체 eval도 실행됐지만 Ollama 미기동으로 accuracy/faithfulness는 비어 있었고, retrieval만 `0.48`로 산출됐다.
- 권한 상승으로 전체 eval을 다시 실행해 `precision@k_mean=0.48`, `accuracy_mean=0.575`, `faithfulness_mean=0.7`을 확인했다.
- Cross-Encoder 모델까지 오프라인화하기 위한 새 실행 계획을 추가했고 `feature/cross-encoder-offline` 브랜치에서 작업을 시작했다.
- `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` 캐시를 준비했고 오프라인 강제 모드 로드도 확인했다.
- Cross-Encoder 캐시 준비 후 full eval을 재실행했고, 로드 실패 경고 없이 `precision@k_mean=0.48`, `accuracy_mean=0.525`, `faithfulness_mean=0.8`을 확인했다.
- PR #2 `feature/cross-encoder-offline`을 `main`에 머지했고 로컬 `main`도 `origin/main`과 일치한다.
- 완료된 bootstrap, runtime validation, cross-encoder offline 실행 계획을 `docs/exec-plans/completed/`로 이동했다.
- 다음 작업으로 아키텍처 문서 통합 active plan을 생성했다.
- 루트 `ARCHITECTURE.md`를 canonical 요약 문서로 정리하고, `docs/architecture.md`를 상세 Mermaid 다이어그램 문서로 분리했다.
- `docs/architecture.md`의 오래된 모델명, 벡터 차원, Phase 표기를 현재 코드 기준으로 갱신했다.
- 다음 작업으로 품질 기준선 개선 active plan을 생성했다.
- 최신 평가 리포트 `eval/results/eval_20260513_100727.json`을 분석해 낮은 점수 원인을 분류했다.
- 분석 결과를 `docs/references/quality-baseline-analysis.md`에 기록했다.
- 첫 개선 실험은 검색 튜닝이 아니라 평가 하네스 정렬로 정했다.
- `eval/pipeline.py`에 `vector_precision@k`, `rag_precision@k`, `source_coverage@k`, `not_found_rate`를 추가했다.
- 전체 평가를 재실행해 `eval/results/eval_20260513_134658.json`을 저장했다.
- 새 기준선은 `vector_precision@k_mean=0.48`, `rag_precision@k_mean=0.54`, `source_coverage@k_mean=0.925`, `accuracy_mean=0.625`, `faithfulness_mean=0.8`, `not_found_rate=0.2`다.
- 최신 리포트의 낮은 accuracy 케이스를 분석했고 결과를 `docs/references/answer-quality-analysis.md`에 기록했다.
- 첫 구현 실험은 프롬프트 변경이 아니라 accuracy 평가셋/판정 보정으로 정했다.
- 약관 카테고리를 `일반`, `유료서비스`, `위치기반서비스`, `운영정책` 4개로 정리했다.
- API, UI, 평가셋에 새 doc_type 기준을 반영했고 기존 `일반약관`, `위치기반약관` DB 값도 검색되도록 호환 매핑을 추가했다.
- `answer_accuracy()`에 OR keyword group을 추가하고 `tc-08`, `tc-09`의 대체 표현을 반영했다.
- 전체 평가를 재실행해 `eval/results/eval_20260513_155642.json`을 저장했다.
- accuracy는 `0.625 -> 0.7`로 개선됐고, faithfulness는 `0.8`로 유지됐다.
- 부분 답변 정책을 적용해 `tc-04`를 no-answer에서 partial-answer로 개선했다.
- 전체 평가를 재실행해 `eval/results/eval_20260513_164755.json`을 저장했다.
- `not_found_rate`는 `0.2 -> 0.1`로 개선됐고 `faithfulness_mean=0.8`은 유지됐다.
- `accuracy_mean`은 `0.7 -> 0.675`로 소폭 하락했으며, 이는 `tc-01` no-answer 표현 변화에 따른 keyword accuracy 변동이다.
- Ubuntu 20.04.5 LTS 서버에 Git 없이 수동 배포하고 이후 수정 사항을 재반영하는 절차를 `docs/manual-deployment-guide.md`에 정리했다.
- `feature/github-actions-ci` 브랜치에서 GitHub Actions 최소 CI workflow를 추가했다.
- CI는 PR과 `main` push에서 `bash scripts/validate-docs.sh`와 Python compile 검증을 실행한다.
- 로컬 검증은 문서 검증 통과, `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py` 통과까지 확인했다.
- PR #15를 생성했고 GitHub Actions `Static checks`가 생성되어 통과했다.
- GitHub Actions CI 계획을 completed로 이동하고, 검색 품질 개선 계획을 새 active plan으로 승격했다.
- PR #15를 머지했고 로컬 `main`을 원격과 동기화했다.
- `feature/search-quality-improvement` 브랜치에서 RAG 검색 경로를 LLM 생성과 분리하고, rerank 이후 source 다양성 선택을 추가했다.
- 검색 지표는 `rag_precision@k_mean=0.54 -> 0.60`, `source_coverage@k_mean=0.925 -> 1.0`으로 개선됐다.
- 개선 후 full eval 리포트는 `eval/results/eval_20260514_113849.json`, 분석 기록은 `docs/references/search-quality-improvement.md`에 남겼다.
- PR #16 `RAG 검색 source coverage 개선`을 생성했고 GitHub Actions `Static checks`가 통과했다.
- 권한 상승 경로에서 Ollama 상태를 재확인했고 `gemma3:12b`가 사용 가능해 full eval 생성 지표까지 재검증했다.
- PR #16을 머지했고 로컬 `main`을 원격과 동기화했다.
- 검색 품질 개선 계획을 completed로 이동하고, 다음 품질 반복 계획을 active로 생성했다.
- 2026-05-14 작업 리포트와 before/after 비교 문서를 추가했다.
  - `docs/references/2026-05-14-work-report.md`
  - `docs/references/2026-05-14-before-after.md`
- 기존 RAG 요약 문서를 최신 평가 결과와 검색 품질 개선 내용으로 갱신했다.
  - `RAG_IMPROVEMENT_ROADMAP.md`
  - `RAG_BEFORE_AFTER.md`
  - `RAG_PERFORMANCE_REPORT.md`
- 최신 full eval 낮은 점수 케이스를 분석했고 다음 실험 후보를 평가셋 정합성 보정으로 정리했다.
  - `docs/references/2026-05-14-next-quality-iteration-analysis.md`
- 평가셋 정합성 보정을 수행했다.
  - `tc-01`: 해지 시 환불 정책 질문을 현재 문서 근거에 맞는 해지 후 데이터/게시물 처리 질문으로 재분류했다.
  - `tc-03`, `tc-04`, `tc-09`: expected keyword OR group을 보강했다.
- 전체 eval을 재실행해 `eval/results/eval_20260514_152044.json`을 저장했다.
- 평가셋 정렬 후 생성 지표는 `accuracy_mean=0.875`, `faithfulness_mean=1.0`, `not_found_rate=0.0`이다.
- 검색 지표는 변경 없음: `precision@k_mean=0.48`, `vector_precision@k_mean=0.48`, `rag_precision@k_mean=0.60`, `source_coverage@k_mean=1.0`.
- 평가셋 정렬 결과 문서를 추가했다.
  - `docs/references/2026-05-14-eval-case-alignment.md`
- 다음 품질 반복 계획과 평가셋 정렬 계획을 completed로 이동했다.
- 다음 후보로 검색 지표 추가 개선 계획을 active로 생성했다.
  - `docs/exec-plans/completed/2026-05-14-next-search-quality-experiment.md`
- PR #17 `평가 케이스 정합성 보정`을 생성했다.
- 검색 지표 추가 개선 후보를 분석했다.
  - 현 `rag_precision@k_mean=0.60`은 현재 `precision_at_k` 설계상 이론적 상한이다.
  - 모든 케이스가 `source_coverage_at_k=1.0`이다.
  - 검색 튜닝보다 retrieval metric normalization이 우선이다.
  - 분석 문서: `docs/references/2026-05-14-search-quality-ceiling-analysis.md`
- 다음 구현 후보로 retrieval metric normalization active plan을 생성했다.
  - `docs/exec-plans/completed/2026-05-14-retrieval-metric-normalization.md`
- retrieval metric normalization을 구현했다.
  - 기존 precision 계열 지표는 유지했다.
  - normalized source precision, chunk precision, source recall 지표를 추가했다.
  - 새 full eval 리포트: `eval/results/eval_20260514_164724.json`
  - 주요 결과: `rag_normalized_source_precision@k_mean=1.0`, `rag_chunk_precision@k_mean=0.96`, `source_recall@k_mean=1.0`
- 다음 후보로 잔여 답변 accuracy 분석 계획을 active로 생성했다.
  - `docs/exec-plans/completed/2026-05-14-residual-answer-quality-analysis.md`
- 잔여 답변 accuracy 케이스를 분석했다.
  - 분석 대상: `tc-06`, `tc-07`, `tc-09`
  - 분석 문서: `docs/references/2026-05-14-residual-answer-quality-analysis.md`
  - 결론: 검색 병목이 아니라 답변 표현과 keyword 기반 평가셋의 불일치가 주 원인이다.
  - 다음 후보: 프롬프트 보정 우선, 평가셋 보정 보조.
- 다음 작업으로 답변 형식 프롬프트 실험 active plan을 생성했다.
  - `docs/exec-plans/completed/2026-05-14-answer-format-prompt-experiment.md`
- 답변 형식 프롬프트 실험을 수행했다.
  - 분쟁/면책/의무 질문별 표지어 사용 지시를 추가한 프롬프트 실험은 `accuracy_mean`, `faithfulness_mean`, `not_found_rate`가 회귀해 철회했다.
  - 좁은 프롬프트 지시도 `accuracy_mean` 회귀가 있어 철회했다.
  - 최종 채택 변경은 `eval/test_cases.json`의 `tc-06`, `tc-09` expected keyword OR group 보정이다.
  - 최종 유효 리포트는 `eval/results/eval_20260514_180006.json`이다.
  - 최종 유효 지표: `accuracy_mean=0.975`, `faithfulness_mean=0.9`, `not_found_rate=0.0`.
- 다음 작업으로 faithfulness eval stability active plan을 생성했다.
  - `docs/exec-plans/completed/2026-05-14-faithfulness-eval-stability.md`
- `tc-10` faithfulness 판정 흔들림을 분석했다.
  - 분석 문서: `docs/references/2026-05-15-faithfulness-eval-stability.md`
  - `context_texts[:2]`로 judge를 실행하면 `YES`, 현재 코드와 같은 `context_texts[:3]`로 실행하면 `NO`가 재현됐다.
  - context 1, 2는 `tc-10` 답변 근거와 직접 일치하고, context 3은 이용 제한/해지 조항이라 무관하다.
  - 결론: 답변 근거 부족보다 faithfulness judge context selection 문제가 우선이다.
- 다음 작업으로 faithfulness context selection active plan을 생성했다.
  - `docs/exec-plans/completed/2026-05-15-faithfulness-context-selection.md`
- faithfulness 전용 context selector를 구현했다.
  - 질문/답변 lexical overlap과 source diversity를 함께 사용해 judge context를 고른다.
  - `tc-03`, `tc-10` 단건 faithfulness가 모두 `1.0`으로 판정됨을 확인했다.
  - 최종 full eval 리포트는 `eval/results/eval_20260515_110900.json`이다.
  - 최종 지표: `accuracy_mean=0.95`, `faithfulness_mean=1.0`, `not_found_rate=0.0`.
- 다음 작업으로 residual keyword accuracy active plan을 생성했다.
  - `docs/exec-plans/completed/2026-05-15-residual-keyword-accuracy.md`
- 잔여 keyword accuracy를 보정했다.
  - 분석 문서: `docs/references/2026-05-15-residual-keyword-accuracy.md`
  - `tc-03`, `tc-07`, `tc-09`, `tc-10` expected keyword OR group을 문서/답변 표현에 맞게 보정했다.
  - 최종 full eval 리포트는 `eval/results/eval_20260515_135903.json`이다.
  - 최종 지표: `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0`.
- 다음 작업으로 eval generalization review active plan을 생성했다.
  - `docs/exec-plans/active/2026-05-15-eval-generalization-review.md`
- RAG 보고서 3종을 최신 평가/인제스천 상태 기준으로 갱신했고, HTML 복사본과 `RAG_BEFORE_AFTER.pdf`를 추가했다.
  - `RAG_BEFORE_AFTER.md`, `RAG_PERFORMANCE_REPORT.md`, `RAG_IMPROVEMENT_ROADMAP.md`
  - `RAG_BEFORE_AFTER.html`, `RAG_PERFORMANCE_REPORT.html`, `RAG_IMPROVEMENT_ROADMAP.html`
  - `RAG_BEFORE_AFTER.pdf`
- 평가셋 일반화 검토를 수행했다.
  - 분석 문서: `docs/references/2026-05-22-eval-generalization-review.md`
  - 결론: 기존 10개 케이스는 다음/네이버 4개 약관 중심이라 최신 13개 문서, 318개 청크 corpus를 충분히 검증하지 못한다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-15-eval-generalization-review.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-22-eval-set-expansion.md`를 생성했다.
- 평가셋을 16개 케이스로 확장하고 full eval을 실행했다.
  - 최종 리포트: `eval/results/eval_20260522_091248.json`
  - 결과 문서: `docs/references/2026-05-22-eval-set-expansion-result.md`
  - `accuracy_mean=0.9062`, `faithfulness_mean=0.75`, `not_found_rate=0.0625`
  - 신규 `tc-11`, `tc-12`, `tc-13`은 통과했고, `tc-16`은 negative/no-answer 채점 정책 이슈를 드러냈다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-22-eval-set-expansion.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-22-eval-failure-triage.md`를 생성했다.
- 평가 실패 triage를 수행했다.
  - 결과 문서: `docs/references/2026-05-22-eval-failure-triage.md`
  - `expected_not_found`와 `not_found_success_rate`를 추가해 `tc-16` negative case를 정상 평가하도록 개선했다.
  - faithfulness judge context 선택 상한을 5개로 늘려 `tc-09`, `tc-10` faithfulness 회귀를 해소했다.
  - 최종 리포트: `eval/results/eval_20260522_131753.json`
  - 최종 지표: `accuracy_mean=0.9219`, `faithfulness_mean=0.9375`, `not_found_success_rate=1.0`
  - 완료된 계획: `docs/exec-plans/completed/2026-05-22-eval-failure-triage.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-22-eval-source-drift-calibration.md`를 생성했다.
- source drift calibration을 수행했다.
  - 결과 문서: `docs/references/2026-05-22-eval-source-drift-calibration.md`
  - `tc-04`를 자동 갱신 positive case로 재정의했다.
  - `tc-17`을 추가해 해지/개별 서비스 이용 종료 positive case를 분리했다.
  - `tc-06` 분쟁 해결 keyword와 relevant source를 확장 corpus 기준으로 보정했다.
  - 최종 리포트: `eval/results/eval_20260522_160844.json`
  - 최종 지표: `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`
  - 완료된 계획: `docs/exec-plans/completed/2026-05-22-eval-source-drift-calibration.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-22-source-drift-regression-guard.md`를 생성했다.
- source drift regression guard의 로컬 리포트 스크립트를 추가했다.
  - 스크립트: `scripts/source_drift_report.py`
  - 리포트: `docs/references/2026-05-22-source-drift-regression-report.md`
  - 최신 full eval 기준 critical case는 없다.
  - watch case는 `tc-02`, `tc-03`, `tc-06`, `tc-07`, `tc-08`, `tc-14`, `tc-15`다.
  - `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260522_160844.json --fail-on-critical` 통과.
  - 결정: critical case만 실패 조건으로 보고, watch case는 리포트와 후속 검토 후보로 유지한다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-22-source-drift-regression-guard.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-22-watch-case-review.md`를 생성했다.
- source drift watch case 7건을 검토했다.
  - 결과 문서: `docs/references/2026-05-22-watch-case-review.md`
  - 결론: `eval/test_cases.json`을 즉시 보정하지 않고 watch 상태로 유지한다.
  - 이유: 7건 모두 `answer_accuracy=1.0`, `faithfulness=1.0`이며, 현재 retrieved source에 맞춰 relevant source를 확장하면 평가셋 과적합 위험이 있다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-22-watch-case-review.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-22-source-scope-policy.md`를 생성했다.
- source scope policy를 정리했다.
  - 결과 문서: `docs/references/2026-05-28-source-scope-policy.md`
  - 결론: 기본 `relevant_sources` 범위는 가능한 모든 관련 문서가 아니라 답변에 충분한 대표 근거 문서 기준으로 둔다.
  - exhaustive corpus scope는 별도 coverage 평가나 명시적 cross-policy 케이스에만 사용한다.
  - 이번 작업에서는 `eval/test_cases.json`을 변경하지 않고 watch case를 케이스 분리 후보로 유지했다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-22-source-scope-policy.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-28-watch-case-split.md`를 생성했다.
- source scope policy에 따라 watch case split을 수행했다.
  - 결과 문서: `docs/references/2026-05-28-watch-case-split-result.md`
  - source drift report: `docs/references/2026-05-28-watch-case-split-source-drift-report.md`
  - `eval/test_cases.json`을 17개에서 22개 케이스로 확장했다.
  - `tc-02`, `tc-03`, `tc-07`, `tc-08`, `tc-14`, `tc-15`의 질문 범위를 명시적으로 좁혔다.
  - `tc-18`~`tc-22`를 추가해 위치기반서비스, 운영정책, 유료서비스, 계정 운영정책 범위를 분리했다.
  - 최종 재채점 리포트: `eval/results/eval_20260528_115250_recalibrated.json`
  - 최종 지표: `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`, `rag_normalized_source_precision@k_mean=0.9795`, `source_recall@k_mean=0.9692`
  - source drift report 기준 critical case는 없고, 남은 watch case는 `tc-06` 1건이다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-28-watch-case-split.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-28-tc06-source-scope-review.md`를 생성했다.
- `tc-06` source scope review를 수행했다.
  - 결과 문서: `docs/references/2026-05-28-tc06-source-scope-review.md`
  - source drift report: `docs/references/2026-05-28-tc06-source-scope-report.md`
  - `tc-06`은 explicit cross-policy coverage 케이스가 아니라 대표 근거 회귀 케이스로 유지했다.
  - `tc-06`의 `relevant_sources`를 7개에서 4개 대표 근거로 축소했다.
  - 최종 재범위화 리포트: `eval/results/eval_20260528_115250_tc06_rescoped.json`
  - 최종 지표: `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`, `rag_normalized_source_precision@k_mean=0.9886`, `source_recall@k_mean=0.9886`
  - source drift report 기준 critical/watch case는 없다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-28-tc06-source-scope-review.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-28-location-dispute-case-review.md`를 생성했다.
- 위치기반서비스 분쟁 해결 hard case를 추가했다.
  - 결과 문서: `docs/references/2026-05-28-location-dispute-case-review.md`
  - source drift report: `docs/references/2026-05-28-location-dispute-case-report.md`
  - `tc-23`을 추가해 위치정보 관련 분쟁 해결 절차를 별도 검증한다.
  - `tc-23`은 `doc_type=위치기반서비스`로 제한하고 다음/네이버/카카오 위치기반서비스 약관을 대표 근거로 둔다.
  - 최종 추가 리포트: `eval/results/eval_20260528_115250_location_dispute_added.json`
  - 최종 지표: `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`, `rag_normalized_source_precision@k_mean=0.9891`, `source_recall@k_mean=0.9891`
  - source drift report 기준 critical/watch case는 없다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-28-location-dispute-case-review.md`
  - 다음 active plan으로 `docs/exec-plans/active/2026-05-28-source-drift-ci-promotion.md`를 생성했다.

- source drift guard를 CI로 승격했다.
  - `.github/workflows/ci.yml`에 저장 리포트 기반 `scripts/source_drift_report.py eval/results/eval_20260528_115250_location_dispute_added.json --fail-on-critical` 단계를 추가했다.
  - 로컬 검증에서 source drift guard는 venv Python과 시스템 Python 모두 통과했고, 최신 리포트 기준 critical/watch case는 없다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-28-source-drift-ci-promotion.md`
- Ubuntu 20.04 서버 배포 중 발견한 런타임 호환 수정 사항을 로컬에도 반영했다.
  - `ingestion/embedder.py`의 지연 import 타입 힌트 런타임 오류를 제거했다.
  - `ingestion/vector_store.py`에 낮은 SQLite 버전에서 `pysqlite3`를 사용하도록 호환 처리를 추가했다.
  - `requirements.txt`에 Linux용 `pysqlite3-binary` 의존성을 추가했다.

- Ubuntu 배포 런타임 하드닝 문서화를 진행했다.
  - `docs/manual-deployment-guide.md`에 Python 3.11 소스 빌드 대체 경로, Chroma SQLite 대응, GPU/PyTorch CUDA 정합성 확인, `gemma4:26b` 모델 변경 절차를 추가했다.
  - 검증: `bash scripts/validate-docs.sh`, Python compile, source drift guard 통과.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-ubuntu-deployment-runtime-hardening.md`
- PR #28 `Source drift guard와 Ubuntu 배포 절차 보강`을 생성했고 Static checks 통과 후 main에 머지했다.
  - PR: https://github.com/algum1737/ragSystem_codex/pull/28
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-pr-28-merge-followup.md`
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-ubuntu-server-runtime-verification.md`
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-operating-model-default-policy.md`
  - 다음 active plan: `docs/exec-plans/active/2026-05-29-ubuntu-default-model-redeploy-verification.md`

- Ubuntu 서버 런타임 검증을 완료했다.
  - `ragsystem-api`, `ragsystem-web`, `ollama` 모두 active 상태였다.
  - `/health`는 `model=gemma4:26b`, `/stats`는 `count=318`을 반환했다.
  - PyTorch는 `2.3.1+cu118`, CUDA `11.8`, GPU `NVIDIA GeForce RTX 2080 Ti`를 정상 인식했다.
  - 위치기반서비스 분쟁 해결 RAG query가 HTTP 200과 5개 source를 반환했고, 쿼리 후 API 서비스가 계속 active 상태임을 확인했다.
  - Streamlit은 HTTP 200을 반환했다.

- 운영 기본 모델 정책을 정리했다.
  - 코드 기본값, CLI 기본값, Streamlit 추천 모델, 아키텍처 문서, 배포/기동 가이드를 `gemma4:26b` 기준으로 맞췄다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-operating-model-default-policy.md`

- 평가 기준 모델과 튜닝 정책을 정리했다.
  - 운영 기본 모델은 `gemma4:26b`, 평가 기준 모델은 `gemma3:12b`로 분리했다.
  - `eval/pipeline.py` 리포트 summary에 `llm_model`과 `top_k`를 기록하도록 보강했다.
  - `docs/references/2026-05-29-eval-model-tuning-policy.md`에 표준 eval 명령, 튜닝 순서, 안정화 판단 기준을 문서화했다.
  - retrieval-only 검증에서 `llm_model=gemma3:12b`, `top_k=5`, `rag_normalized_source_precision=0.9891`, `source_recall=0.9891` 출력을 확인했다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-eval-model-tuning-policy.md`

- Ubuntu 기본 모델 재배포 검증을 완료했다.
  - 서버 배포본의 `DEFAULT_MODEL`이 `gemma3:12b`로 남아 있음을 확인하고 최신 main 코드로 갱신했다.
  - 갱신 후 서버 배포본의 `DEFAULT_MODEL = "gemma4:26b"` 반영을 확인했다.
  - `ragsystem-api`, `ragsystem-web`, `ollama` 재기동 후 active 상태를 확인했다.
  - `/health`는 `model=gemma4:26b`, `/stats`는 `count=318`, Streamlit은 HTTP 200을 반환했다.
  - 실제 RAG query 1건이 응답과 5개 source를 반환했다.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-ubuntu-default-model-redeploy-verification.md`
  - 다음 active plan: `docs/exec-plans/active/2026-05-29-performance-tuning-baseline.md`

- 튜닝 전 기준선과 1차 no-answer 탐지 보정을 완료했다.
  - 기준선 full eval: `eval/results/eval_20260529_172801.json`
  - 보정 후 full eval: `eval/results/eval_20260529_173928.json`
  - no-answer 탐지식을 `문서에서 확인되지 않는 내용입니다`, `제공된 문서에는`, `제공된 문서에서 확인되지 않습니다` 시작 응답까지 인식하도록 보강했다.
  - 결과는 `accuracy_mean=1.0`, `faithfulness_mean=0.9565`, `not_found_success_rate=1.0`로 집계 지표 기준을 통과했다.
  - 다만 source drift guard는 `tc-04` faithfulness 0.0을 critical로 분류해 잔여 리뷰가 필요하다.
  - 결과 문서: `docs/references/2026-05-29-performance-tuning-baseline-result.md`
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-performance-tuning-baseline.md`
  - 다음 active plan: `docs/exec-plans/active/2026-05-29-residual-tuning-case-review.md`

- 잔여 튜닝 케이스 리뷰를 완료했다.
  - `tc-04`는 검색 누락이 아니라 답변 citation 표현 또는 faithfulness judge 안정성 문제로 분류했다.
  - 전역 출처 번호 프롬프트 보강은 단건 응답에서는 개선됐지만 full eval에서 `tc-05`, `tc-07`, `tc-11` 회귀가 발생해 채택하지 않았다.
  - `tc-17`은 답변 품질이 아니라 relevant source scope가 넓은 평가셋 문제 후보로 분류했다.
  - 결과 문서: `docs/references/2026-06-01-residual-tuning-case-review.md`
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-residual-tuning-case-review.md`
  - 다음 active plan: `docs/exec-plans/active/2026-06-01-tc04-faithfulness-tc17-source-scope.md`

- `tc-04` faithfulness와 `tc-17` source scope 보정을 완료했다.
  - faithfulness judge 입력에서 숫자 citation marker를 제거하도록 보강했다.
  - `tc-17` relevant source를 representative evidence 기준에 맞춰 3개 문서로 좁혔다.
  - `tc-21`은 서비스 제공 중단/서비스 변경 범위로 질문과 keyword를 좁혔다.
  - 문서 밖 추론 표현 금지 규칙을 RAG 프롬프트에 한 문장 추가했다.
  - 최종 full eval 리포트: `eval/results/eval_20260601_164832.json`
  - 최종 지표: `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_success_rate=1.0`, `rag_normalized_source_precision=1.0`, `source_recall=1.0`
  - source drift guard 기준 critical/watch case는 없다.
  - 완료된 계획: `docs/exec-plans/completed/2026-06-01-tc04-faithfulness-tc17-source-scope.md`
  - 다음 active plan: `docs/exec-plans/active/2026-06-01-observability-langfuse-review.md`

- Langfuse/observability 도입 검토를 완료했다.
  - 현재 프로젝트에는 Langfuse가 연동되어 있지 않고, eval JSON/source drift report/FastAPI 및 systemd 로그 중심으로 관측한다.
  - Langfuse는 Python SDK와 OpenTelemetry endpoint, self-hosted 옵션이 있어 후보로 적합하다.
  - 다만 약관 문서, 사용자 질의, 답변, 출처가 trace payload에 포함될 수 있어 외부 SaaS 즉시 연동은 보류한다.
  - 먼저 privacy-safe local JSONL trace sink를 구현하고, self-hosted Langfuse는 이후 optional exporter로 검토한다.
  - 결과 문서: `docs/references/2026-06-02-observability-langfuse-review.md`
  - 완료된 계획: `docs/exec-plans/completed/2026-06-01-observability-langfuse-review.md`
  - 다음 active plan: `docs/exec-plans/active/2026-06-02-local-observability-trace-schema.md`

## Current Gaps

- `/stats`는 최신 인제스천 후 현재 `count=318`을 반환한다.
- retrieval-only 기준 검증은 현재 `vector_precision@k_mean=0.4522`, `rag_precision@k_mean=0.5478`로 정상 완료된다.
- 튜닝 판단은 raw precision보다 `rag_normalized_source_precision@k_mean=0.9891`과 `source_recall@k_mean=0.9891` 중심으로 본다.
- 최신 full eval 리포트는 `eval/results/eval_20260601_164832.json`에 저장되어 있다.
- 최신 생성 지표는 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0435`, `not_found_success_rate=1.0`이다.
- 최신 정규화 검색 지표는 `rag_normalized_source_precision@k_mean=0.9891`, `rag_chunk_precision@k_mean=0.8609`, `source_recall@k_mean=0.9891`이다.
- 현재 평가셋 기준 source drift guard critical/watch case는 없다.
- 현재 active plan은 `docs/exec-plans/active/2026-06-02-local-observability-trace-schema.md`다.
- 이전 Cross-Encoder 캐시 반영 리포트는 `eval/results/eval_20260513_100727.json`에 저장되어 있다.
- 검색/인제스천/평가 경로에 필요한 임베딩 모델 캐시는 준비됐다.
- Cross-Encoder reranking 캐시도 준비됐다.
- 코드 내부의 명칭과 문서 상 제품 정의 사이에 일부 정리되지 않은 표현이 남아 있다.

## Suggested Next Work

1. active plan `docs/exec-plans/active/2026-06-11-concise-real-usage-trace-review.md`에 따라 실제 사용자 concise trace 표본이 더 쌓인 뒤 재검토한다.
2. 표본이 충분하지 않으면 active plan을 완료하지 말고 open work로 유지한다.

## Handoff Prompt

```text
이 프로젝트는 하네스 엔지니어링 방식으로 진행 중이다.

먼저 아래 파일을 읽고 현재 상태를 요약해라.
1. AGENTS.md
2. README.md
3. ARCHITECTURE.md
4. docs/index.md
5. docs/PLANS.md
6. docs/product-specs/terms-rag-system.md
7. docs/manual-deployment-guide.md
8. docs/references/quality-baseline-analysis.md
9. docs/references/answer-quality-analysis.md
10. docs/references/search-quality-improvement.md
11. docs/references/2026-05-14-work-report.md
12. docs/references/2026-05-14-before-after.md
13. docs/references/2026-05-14-next-quality-iteration-analysis.md
14. docs/references/2026-05-14-eval-case-alignment.md
15. docs/exec-plans/completed/2026-05-14-eval-case-alignment.md
16. docs/exec-plans/completed/2026-05-14-next-quality-iteration.md
17. docs/exec-plans/completed/2026-05-14-search-quality-improvement.md
18. docs/exec-plans/completed/2026-05-14-next-search-quality-experiment.md
19. docs/exec-plans/completed/2026-05-14-retrieval-metric-normalization.md
20. docs/references/2026-05-14-search-quality-ceiling-analysis.md
21. docs/references/2026-05-14-retrieval-metric-normalization.md
22. docs/references/2026-05-14-residual-answer-quality-analysis.md
23. docs/exec-plans/completed/2026-05-14-residual-answer-quality-analysis.md
24. docs/exec-plans/completed/2026-05-14-answer-format-prompt-experiment.md
25. docs/references/2026-05-15-faithfulness-eval-stability.md
26. docs/exec-plans/completed/2026-05-14-faithfulness-eval-stability.md
27. docs/exec-plans/completed/2026-05-15-faithfulness-context-selection.md
28. docs/references/2026-05-15-residual-keyword-accuracy.md
29. docs/exec-plans/completed/2026-05-15-residual-keyword-accuracy.md
30. docs/exec-plans/completed/2026-05-15-eval-generalization-review.md
31. docs/references/2026-05-22-eval-generalization-review.md
32. docs/exec-plans/completed/2026-05-22-eval-set-expansion.md
33. docs/references/2026-05-22-eval-set-expansion-result.md
34. docs/exec-plans/completed/2026-05-22-eval-failure-triage.md
35. docs/references/2026-05-22-eval-source-drift-calibration.md
36. docs/exec-plans/completed/2026-05-22-eval-source-drift-calibration.md
37. docs/exec-plans/completed/2026-05-22-source-drift-regression-guard.md
38. docs/references/2026-05-22-source-drift-regression-report.md
39. docs/references/2026-05-22-watch-case-review.md
40. docs/exec-plans/completed/2026-05-22-watch-case-review.md
41. docs/references/2026-05-28-source-scope-policy.md
42. docs/references/2026-05-28-watch-case-split-result.md
43. docs/references/2026-05-28-watch-case-split-source-drift-report.md
44. docs/exec-plans/completed/2026-05-28-watch-case-split.md
45. docs/references/2026-05-28-tc06-source-scope-review.md
46. docs/references/2026-05-28-tc06-source-scope-report.md
47. docs/exec-plans/completed/2026-05-28-tc06-source-scope-review.md
48. docs/references/2026-05-28-location-dispute-case-review.md
49. docs/references/2026-05-28-location-dispute-case-report.md
50. docs/exec-plans/completed/2026-05-28-location-dispute-case-review.md
51. docs/exec-plans/completed/2026-05-28-source-drift-ci-promotion.md
52. docs/exec-plans/completed/2026-05-13-github-actions-ci.md
53. docs/exec-plans/completed/2026-05-13-partial-answer-policy.md
54. docs/exec-plans/completed/2026-05-13-eval-accuracy-calibration.md
55. docs/exec-plans/completed/2026-05-13-answer-quality-improvement.md
56. docs/exec-plans/completed/2026-05-13-eval-harness-alignment.md
57. docs/exec-plans/completed/2026-05-13-quality-baseline-improvement.md
58. docs/exec-plans/completed/2026-05-13-architecture-doc-consolidation.md
59. docs/exec-plans/completed/2026-05-12-bootstrap-ragsystem-codex.md
60. docs/exec-plans/completed/2026-05-12-runtime-validation.md
61. docs/exec-plans/completed/2026-05-13-cross-encoder-offline.md
62. docs/exec-plans/completed/2026-05-29-ubuntu-deployment-runtime-hardening.md

현재 기준:
- branch: `git branch --show-current`
- commit: `git rev-parse --short HEAD`

작업 규칙:
- 큰 작업은 active exec plan을 먼저 작성해라.
- 작업 완료 시 완료 범위와 검증 결과를 기록하고 completed로 이동해라.
- 커밋 후에는 docs/HANDOFF.md를 갱신하되, 커밋 해시는 git 명령으로 확인하게 유지해라.
```
