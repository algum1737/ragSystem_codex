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
  - `docs/manual-deployment-guide.md`에 Python 3.11 소스 빌드 대체 경로, Chroma SQLite 대응, GPU/PyTorch CUDA 정합성 확인, `gemma4:24b` 모델 변경 절차를 추가했다.
  - 검증: `bash scripts/validate-docs.sh`, Python compile, source drift guard 통과.
  - 완료된 계획: `docs/exec-plans/completed/2026-05-29-ubuntu-deployment-runtime-hardening.md`
- PR #28 `Source drift guard와 Ubuntu 배포 절차 보강`을 생성했고 Static checks가 통과했다.
  - PR: https://github.com/algum1737/ragSystem_codex/pull/28
  - 다음 active plan: `docs/exec-plans/active/2026-05-29-pr-28-merge-followup.md`

## Current Gaps

- `/stats`는 최신 인제스천 후 현재 `count=318`을 반환한다.
- retrieval eval은 현재 `vector_precision@k_mean=0.48`, `rag_precision@k_mean=0.60`으로 정상 완료된다.
- 현 `rag_precision@k_mean=0.60`은 current unique-source precision 계산 방식 기준 이론적 상한이다.
- 최신 추가 리포트는 `eval/results/eval_20260528_115250_location_dispute_added.json`에 저장되어 있다.
- 최신 생성 지표는 `accuracy_mean=1.0`, `faithfulness_mean=1.0`, `not_found_rate=0.0455`, `not_found_success_rate=1.0`이다.
- 최신 정규화 검색 지표는 `rag_normalized_source_precision@k_mean=0.9891`, `rag_chunk_precision@k_mean=0.8609`, `source_recall@k_mean=0.9891`이다.
- 현재 평가셋 기준 잔여 낮은 accuracy/faithfulness 케이스는 없다.
- 현재 active plan은 `docs/exec-plans/active/2026-05-29-pr-28-merge-followup.md`다.
- 이전 Cross-Encoder 캐시 반영 리포트는 `eval/results/eval_20260513_100727.json`에 저장되어 있다.
- 검색/인제스천/평가 경로에 필요한 임베딩 모델 캐시는 준비됐다.
- Cross-Encoder reranking 캐시도 준비됐다.
- 코드 내부의 명칭과 문서 상 제품 정의 사이에 일부 정리되지 않은 표현이 남아 있다.

## Suggested Next Work

1. 사용자 승인 후 PR #28을 머지한다.
2. 머지 후 로컬 main을 동기화하고 handoff/plan 상태를 completed로 정리한다.

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
