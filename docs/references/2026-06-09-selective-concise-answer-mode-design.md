# 2026-06-09 Selective Concise Answer Mode Design

## Summary

`refined_concise_bullet` v4는 smoke 기준으로 빠르지만, 기본 프롬프트를 전면 교체하면 full eval에서 회귀가 발생했다. 따라서 기본 RAG 답변 품질 계약은 유지하고, 사용자가 빠른 요약을 명시적으로 선택할 때만 concise prompt를 적용하는 선택형 모드로 설계한다.

결론:

- 기본값은 반드시 `standard`로 유지한다.
- `concise`는 명시적 요청에서만 실행한다.
- v1에서는 자동 라우팅을 하지 않는다.
- full eval 기준선은 `standard` 모드로 유지한다.
- `concise`는 speed/summary convenience 기능으로 취급하고, 정확도 보장 모드로 표기하지 않는다.

## Why Not Replace The Default Prompt

운영 기본 프롬프트 임시 교체 후 full eval 결과:

| metric | value |
|---|---:|
| accuracy_mean | 0.8804 |
| faithfulness_mean | 1.0 |
| not_found_success_rate | 0.0 |
| rag_normalized_source_precision@k_mean | 1.0 |
| source_recall@k_mean | 1.0 |

검색과 faithfulness는 유지됐지만, 답변 형식과 키워드 포함률이 회귀했다.

대표 회귀:

| case | issue |
|---|---|
| `tc-05` | 손해배상/위약금 조건 일부 키워드 누락 |
| `tc-07` | 면책 조항 외 분쟁/변경 내용이 섞임 |
| `tc-09` | 이용자 의무 키워드 누락 |
| `tc-11` | 청약철회/환불 제한 조건에 관련성 낮은 이용 제한 문장 혼입 |
| `tc-12` | 게시물 제한 유형 일부 누락 |
| `tc-16` | expected no-answer 계약 실패 |
| `tc-21` | 통지 조건 일부 누락 |

## Current Query Surface

- API `QueryRequest`: `question`, `top_k`, `doc_type`
- API `/query`: 현재 `question`, `doc_type`만 `RAGEngine.query()`에 전달한다.
- CLI `query.py`: `question`, `model`, `ollama-url`, `db-path`, `collection`, `top-k`, `verbose`, `dry-run`
- Streamlit Query UI: `doc_type`, `question`, `top_k`, search button
- `RAGEngine.query()`: 전역 `PROMPT_TEMPLATE`만 사용한다.

## Proposed Interface

### API

Add an optional answer mode field:

```json
{
  "question": "...",
  "top_k": 5,
  "doc_type": "운영정책",
  "answer_mode": "standard"
}
```

Allowed values:

- `standard`: existing default prompt, current behavior
- `concise`: refined concise bullet prompt

Default:

- omitted or `null` -> `standard`

### CLI

Add:

```bash
--answer-mode standard|concise
```

Default:

```bash
--answer-mode standard
```

### Streamlit

Add a compact mode control near the search button:

- `표준`
- `빠른 요약`

Default:

- `표준`

## Engine Design

Avoid mutating module-level `PROMPT_TEMPLATE` at runtime.

Recommended structure:

1. Keep existing `PROMPT_TEMPLATE` as the standard prompt.
2. Add `CONCISE_PROMPT_TEMPLATE` as a separate constant.
3. Add `ANSWER_MODE_PROMPTS = {"standard": PROMPT_TEMPLATE, "concise": CONCISE_PROMPT_TEMPLATE}`.
4. Add `answer_mode: str = "standard"` to `RAGEngine.query()`.
5. Select the prompt per call:

```python
prompt_template = ANSWER_MODE_PROMPTS[answer_mode]
prompt = prompt_template.format(context=context, question=question)
```

6. Record `answer_mode` in `trace_metadata`.

This keeps concurrent API requests safe because no global prompt value is changed per request.

## Safety Policy

### v1 behavior

- No automatic concise routing.
- No automatic no-answer detection before generation.
- Users must explicitly choose `concise`.
- `standard` remains the only mode used by full eval quality gates.

### Why no automatic routing in v1

The concise prompt failed both keyword completeness and no-answer contract in full eval. A pre-generation heuristic cannot reliably know whether a question is answerable because retrieval can return adjacent but insufficient chunks. Automatic routing would risk hiding no-answer or partial-answer cases.

## Validation Contract

### Automated

- `.venv/bin/python -m py_compile retriever/engine.py api/models.py api/main.py query.py app.py`
- `bash scripts/validate-docs.sh`

### API smoke

Run both modes for the same representative questions:

- standard: 위치기반서비스 개인위치정보 목적
- concise: 위치기반서비스 개인위치정보 목적
- standard: 운영정책 계정 이용 제한/해지 조건
- concise: 운영정책 계정 이용 제한/해지 조건

Check:

- `standard` answer remains current shape
- `concise` answer uses short bullet format
- trace includes `answer_mode`
- `concise` has lower `answer_length` and lower LLM latency on warmed calls

### Eval

If implementation only adds optional mode and leaves `standard` as default:

- full eval is optional but recommended once before merge.

If any default behavior changes:

- full eval is mandatory.

## Implementation Recommendation

Proceed with implementation only if the goal is user-facing fast-summary mode.

Do not implement automatic routing yet. A second phase can add routing only after collecting enough traces to identify reliable intent signals.
