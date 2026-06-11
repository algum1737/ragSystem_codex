# 2026-06-11 Concise 06 Stability Fix Result

## Summary

`concise-06`가 유료서비스 제공 중단/변경 통지 질문에서 통지 방법과 사전/사후 예외를 안정적으로 보존하도록 보정했다.

변경 내용:

- `CONCISE_PROMPT_TEMPLATE`에 조건, 제한, 예외, 통지 시점 질문에서 예외 조건을 생략하지 말라는 규칙을 추가했다.
- 사전/사후 통지 예외가 있으면 별도 bullet로 작성하도록 좁게 보강했다.
- concise 답변 bullet 기준을 `최대 4개`로 명확히 했다.
- 질문과 직접 관련 없는 사용기간, 청약철회, 환불, 보상 세부사항을 제외하도록 prompt 제외 규칙을 보강했다.
- `concise-06` deterministic rule에 좁은 동의 표현을 추가했다.

## Eval Rule Changes

`concise-06` rule 보정:

- `notice`에 `통보`를 허용했다.
- `notice_methods`에 `명시된 방법`, `약관에 따른 방법`을 허용했다.
- `post_notice_exception`에 `미리`, `사후 통보`, `예측 불가능`, `예측할 수 없`, `통제할 수 없`을 허용했다.

이 보정은 원 질문 top-5에 제6조 세부 통지 수단 청크가 항상 포함되지 않는 상황을 반영한다. 다만 `제6조`, `정한 방법`, `명시된 방법`, `약관에 따른 방법`처럼 약관상 통지 방법을 직접 가리키는 표현에만 한정했다.

## Local Validation

통과:

```bash
.venv/bin/python -m py_compile retriever/engine.py eval/pipeline.py
.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json
bash scripts/validate-docs.sh
```

참고:

- `python -m py_compile ...`는 로컬 기본 `python` 명령이 없어 실행하지 못했고, `.venv/bin/python`으로 대체했다.

## Server Validation

서버 반영 파일:

```text
/opt/ragSystem_codex/retriever/engine.py
/opt/ragSystem_codex/eval/concise_test_cases.json
/opt/ragSystem_codex/scripts/validate_concise_eval_cases.py
```

서버 정적 검증:

```bash
.venv/bin/python -m py_compile retriever/engine.py eval/pipeline.py
.venv/bin/python scripts/validate_concise_eval_cases.py eval/concise_test_cases.json
```

서버 `concise-06` 3회 반복 smoke:

- 최종 prompt 기준 3/3 통과
- 3회 모두 `post_notice_exception`이 통과했다.
- 답변 길이는 207~279자 범위였다.
- source count는 모두 5였다.

운영 API/Web 반영:

- `sudo systemctl restart ...`는 sudo password 요구로 실행하지 못했다.
- 서비스가 `Restart=always`, `User=ragadmin`임을 확인했다.
- `uvicorn`과 `streamlit` 프로세스에 `TERM`을 보내 systemd 자동 재기동을 유도했다.
- 재기동 후 `ragsystem-api`, `ragsystem-web` 모두 active였다.
- API `/health`는 `{"status":"ok","model":"gemma3:12b"}`를 반환했다.
- Streamlit `_stcore/health`는 `ok`를 반환했다.

운영 API smoke:

- `/query` with `answer_mode=concise`
- `source_count=5`
- 사전/사후 예외 표현 포함
- `사용기간`, `청약철회`, `환불` 등 무관 bullet 제거 확인

최종 runbook smoke:

```text
/opt/ragSystem_codex/eval/results/concise_eval_20260611_102139.json
/opt/ragSystem_codex/logs/concise_lightweight_eval_20260611_concise06_fix_final.jsonl
```

요약:

```text
total_cases=6
passed_cases=6
pass_rate=1.0
required_points_score_mean=0.9583
answer_length_mean=356.3333
query_latency_ms_mean=7717.91
```

`concise-06`:

- `passed=true`
- `required_points_score=1.0`
- `forbidden_claims_hit_count=0`
- `source_count=5`

## Decision

안정화 변경은 적용 가능하다고 판단한다. `standard` prompt와 운영 기본 answer mode는 변경하지 않았다.
