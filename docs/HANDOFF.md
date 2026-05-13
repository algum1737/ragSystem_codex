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
10. `docs/exec-plans/active/2026-05-13-github-actions-ci.md`
11. `docs/exec-plans/completed/2026-05-13-partial-answer-policy.md`
12. `docs/exec-plans/completed/2026-05-13-eval-accuracy-calibration.md`
13. `docs/exec-plans/completed/2026-05-13-answer-quality-improvement.md`
14. `docs/exec-plans/completed/2026-05-13-eval-harness-alignment.md`
15. `docs/exec-plans/completed/2026-05-13-quality-baseline-improvement.md`
16. `docs/exec-plans/completed/2026-05-13-architecture-doc-consolidation.md`
17. `docs/exec-plans/completed/2026-05-12-bootstrap-ragsystem-codex.md`
18. `docs/exec-plans/completed/2026-05-12-runtime-validation.md`
19. `docs/exec-plans/completed/2026-05-13-cross-encoder-offline.md`

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

## Current Gaps

- `/stats`는 현재 `count=89`를 반환한다.
- retrieval eval은 현재 `precision@k_mean=0.48`로 정상 완료된다.
- 최신 full eval 리포트는 `eval/results/eval_20260513_164755.json`에 저장되어 있다.
- 이전 Cross-Encoder 캐시 반영 리포트는 `eval/results/eval_20260513_100727.json`에 저장되어 있다.
- 검색/인제스천/평가 경로에 필요한 임베딩 모델 캐시는 준비됐다.
- Cross-Encoder reranking 캐시도 준비됐다.
- 코드 내부의 명칭과 문서 상 제품 정의 사이에 일부 정리되지 않은 표현이 남아 있다.

## Suggested Next Work

1. GitHub Actions workflow를 추가해 PR checks가 표시되게 한다.
2. CI에서는 `bash scripts/validate-docs.sh`와 Python compile 검증을 실행한다.
3. full eval은 Ollama/Chroma/모델 캐시 의존성 때문에 로컬 검증으로 유지한다.

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
10. docs/exec-plans/active/2026-05-13-github-actions-ci.md
11. docs/exec-plans/completed/2026-05-13-partial-answer-policy.md
12. docs/exec-plans/completed/2026-05-13-eval-accuracy-calibration.md
13. docs/exec-plans/completed/2026-05-13-answer-quality-improvement.md
14. docs/exec-plans/completed/2026-05-13-eval-harness-alignment.md
15. docs/exec-plans/completed/2026-05-13-quality-baseline-improvement.md
16. docs/exec-plans/completed/2026-05-13-architecture-doc-consolidation.md
17. docs/exec-plans/completed/2026-05-12-bootstrap-ragsystem-codex.md
18. docs/exec-plans/completed/2026-05-12-runtime-validation.md
19. docs/exec-plans/completed/2026-05-13-cross-encoder-offline.md

현재 기준:
- branch: `git branch --show-current`
- commit: `git rev-parse --short HEAD`

작업 규칙:
- 큰 작업은 active exec plan을 먼저 작성해라.
- 작업 완료 시 완료 범위와 검증 결과를 기록하고 completed로 이동해라.
- 커밋 후에는 docs/HANDOFF.md를 갱신하되, 커밋 해시는 git 명령으로 확인하게 유지해라.
```
