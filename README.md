# ragSystem Codex

이 리포지터리는 특정 카테고리 문서를 인제스천해 검색하고, 로컬 LLM으로 내용을 생성한 뒤, 사용자 지정 템플릿 기반 문서 초안을 만드는 로컬 RAG 시스템을 Codex 운영 방식으로 이어가기 위한 작업 공간이다.

현재 상태:
- 코드베이스 상태: `ragSystem` 소스 프로젝트 이전, 하네스 문서 전환, 런타임 검증, 로컬 모델 캐시 검증을 완료했다.
- 주요 목표: 기존 기능을 유지하면서 문서와 검증 루프를 Codex 운영 방식으로 이어간다.
- 핵심 제약: 완전 로컬 실행, 한국어 문서 중심, 외부 API 미사용, 템플릿 기반 출력.

핵심 기능:
- PDF, Word, HWP, TXT, MD 문서 인제스천
- Chroma 기반 벡터 저장과 하이브리드 검색
- Ollama 기반 로컬 LLM 응답 생성
- Streamlit Web UI와 FastAPI API
- PPTX 템플릿 기반 초안 생성
- 평가 파이프라인과 검색 품질 개선 루프

실행 진입점:
- 인제스천 CLI: `python ingest.py <file-or-dir>`
- 질의 CLI: `python query.py "질문"`
- API 서버: `uvicorn api.main:app --port 8000`
- Web UI: `streamlit run app.py`

시작 지점:
- [AGENTS.md](./AGENTS.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [docs/index.md](./docs/index.md)
- [docs/HANDOFF.md](./docs/HANDOFF.md)
- [현재 실행 계획](./docs/exec-plans/active/2026-05-13-eval-harness-alignment.md)
