# Terms RAG System

## Goal

- 특정 카테고리 문서를 인제스천하고 로컬 LLM으로 검색·생성해 사용자가 원하는 형태의 문서 초안을 자동으로 만든다.
- 현재 검증 도메인은 이용약관이며, 현재 구현된 출력 형식은 PPTX다.

## Users

- 반복적으로 문서 초안을 작성하는 실무 담당자
- 외부 API 사용이 어려운 보안 환경의 팀
- 한국어 문서 기반 검색과 초안 생성이 필요한 사용자

## Core Flows

- 참고 문서를 업로드하고 Chroma에 인제스천한다.
- 질문 또는 요청사항을 입력해 관련 청크와 생성 결과를 확인한다.
- 템플릿 파일을 제공해 PPTX 초안을 생성하고 다운로드한다.
- 평가 스크립트로 검색 품질과 응답 품질을 측정한다.

## Current Capabilities

- 지원 포맷: PDF, DOCX, DOC, HWP, TXT, MD
- 검색: 벡터 검색, BM25, RRF, Cross-Encoder 재순위
- 생성: Ollama 기반 Gemma 모델
- 인터페이스: CLI, FastAPI, Streamlit
- 메타데이터 필터: `doc_type`

## Assumptions

- 현재 저장소는 원본 `ragSystem`을 기반으로 한 Codex 운영 전환 버전이다.
- `.venv`, Chroma 데이터, 로그는 버전 관리 대상이 아니다.
- 이후 작업은 이 문서 체계와 실행 계획을 기준으로 이어간다.

## Open Questions

- 제품의 공식 이름을 `ragSystem`으로 유지할지, 더 일반적인 이름으로 바꿀지 미정이다.
- PPTX 외 다른 출력 형식을 언제 지원할지 미정이다.
- 이용약관 외 다른 도메인 예시 데이터를 기본 검증 세트로 포함할지 미정이다.
