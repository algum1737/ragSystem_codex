# Cross-Encoder Offline Setup Plan

## Goal

`cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` 모델을 로컬 캐시에 준비해 reranking 경로도 오프라인에서 동작하게 만든다.

## Scope

- Cross-Encoder 모델 1회 다운로드
- 로컬 캐시 존재 확인
- 오프라인 강제 모드에서 모델 로드 검증
- 관련 문서와 handoff에 결과 반영

## Assumptions

- `feature/cross-encoder-offline` 브랜치에서 작업한다.
- 인터넷 연결이 가능한 순간이 있어야 최초 1회 다운로드가 가능하다.
- 현재 retrieval/full eval은 Cross-Encoder 없이도 폴백 경로로 동작한다.

## Steps

1. 현재 active 계획과 handoff 기준으로 작업 범위를 고정한다.
2. `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`를 로컬 캐시에 내려받는다.
3. 오프라인 강제 모드에서 Cross-Encoder 로드를 검증한다.
4. 결과를 문서와 handoff에 반영한다.

## Risks

- 모델 다운로드 중 네트워크 장애가 발생할 수 있다.
- Hugging Face 캐시가 부분적으로만 남으면 오프라인 검증이 실패할 수 있다.

## Validation

- 모델 캐시 디렉터리가 생성되어야 한다.
- 오프라인 강제 모드에서 `CrossEncoder` 인스턴스 생성이 성공해야 한다.
- `bash scripts/validate-docs.sh`가 통과해야 한다.

## Progress

- `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` 다운로드 완료
- 캐시 디렉터리 확인 완료
- 오프라인 강제 모드 로드 확인 완료
- Cross-Encoder 캐시 준비 후 full eval 재실행 완료

## Verification Notes

- 캐시 디렉터리:
  - `~/.cache/huggingface/hub/models--cross-encoder--mmarco-mMiniLMv2-L12-H384-v1`
- 오프라인 검증:
  - `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`
  - `local_files_only=True`
  - 결과: `cross-encoder-offline-ok`
- full eval 재검증:
  - 리포트: `eval/results/eval_20260513_100727.json`
  - `precision@k_mean: 0.48`
  - `accuracy_mean: 0.525`
  - `faithfulness_mean: 0.8`
  - Cross-Encoder 로드 실패 경고 없음

## Completion

- 완료일: 2026-05-13
- PR #2로 `main`에 머지 완료했다.
- 결과를 `docs/HANDOFF.md`, `docs/PLANS.md`, `docs/index.md`에 반영했다.
- 남은 작업 없음.
