# 2026-06-10 Concise Eval CI Promotion Result

## Summary

concise lightweight eval의 CI/운영 검증 루프 승격 여부를 검토하고, GitHub Actions에는 runtime eval 대신 정적 schema 검증만 추가했다.

결론:

- `eval/pipeline.py --concise-lightweight`는 GitHub Actions 직접 gate로 넣지 않는다.
- 이유는 Ollama, Chroma corpus, 운영 모델 캐시가 필요하기 때문이다.
- CI에는 `eval/concise_test_cases.json` schema 검증을 추가한다.
- 실제 LLM/RAG smoke는 Ubuntu 서버 배포 후 수동 검증 루프로 유지한다.
- 다음 작업은 서버 smoke 명령을 runbook 또는 script로 정리하는 것이다.

## Current CI

현재 GitHub Actions는 아래 정적 검증을 실행한다.

- `bash scripts/validate-docs.sh`
- `python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- `python scripts/source_drift_report.py ... --fail-on-critical`

이번 작업에서 추가한 검증:

```bash
python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json
```

## Why Runtime Eval Is Not A CI Gate

`--concise-lightweight`는 아래 런타임 의존성이 필요하다.

- Chroma DB corpus
- sentence-transformers embedding model cache
- cross-encoder reranker cache
- Ollama server
- `gemma3:12b` model

GitHub Actions 기본 runner에는 위 상태가 없다. 이를 CI에서 매번 구성하면 실행 시간이 길고, 모델 다운로드와 외부 네트워크 의존성이 생기며, 현재 프로젝트의 완전 로컬 운영 원칙에도 맞지 않는다.

## CI Promotion Decision

CI에 승격한 항목:

- concise eval case schema 정적 검증
- Python compile 대상에 추가 스크립트 포함은 로컬 검증에서 수행하고, CI는 `python scripts/validate_concise_eval_cases.py` 실행으로 문법/import를 함께 확인한다.

CI에 승격하지 않은 항목:

- `eval/pipeline.py --concise-lightweight`
- 서버 trace 확인
- Ollama 기반 generation smoke

운영 루프로 유지할 항목:

- 서버에서 `RAG_TRACE_ENABLED=true`와 별도 trace path를 지정해 concise lightweight eval smoke 실행
- 결과 JSON의 `pass_rate`, `required_points_score_mean`, `answer_length_mean`, `query_latency_ms_mean` 확인
- trace route `eval.concise`, `eval.concise.case`, metadata `answer_mode=concise` 확인

## Implementation

추가 파일:

- `scripts/validate_concise_eval_cases.py`

수정 파일:

- `.github/workflows/ci.yml`

## Validation

- 통과: `.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json`
- 통과: `.venv/bin/python -m py_compile scripts/validate_concise_eval_cases.py eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py`
- 통과: `bash scripts/validate-docs.sh`

로컬에는 `python` 명령이 없어 `python scripts/validate_concise_eval_cases.py ...`는 실패했다. GitHub Actions의 `actions/setup-python` 환경에서는 `python` 명령이 제공되므로 CI step은 그대로 둔다.

## Remaining Work

- 서버 concise lightweight eval smoke를 반복 실행하기 위한 runbook 또는 script를 추가한다.
- 배포 후 수동 검증에서 어떤 trace/report 파일명을 사용할지 고정한다.
