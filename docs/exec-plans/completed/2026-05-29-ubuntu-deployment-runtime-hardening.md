# Ubuntu Deployment Runtime Hardening Plan

## Goal

Ubuntu 20.04 서버 수동 배포 중 확인한 Python, SQLite, GPU/PyTorch 런타임 이슈를 재배포 가능한 운영 절차로 문서화한다.

## Scope

- Ubuntu 20.04에서 `python3.11` apt 패키지가 없을 때의 소스 빌드 경로 정리
- Chroma SQLite 최소 버전 이슈와 `pysqlite3-binary` 대응 정리
- GPU 사용 시 NVIDIA driver와 PyTorch CUDA wheel 정합성 확인 절차 정리
- `gemma4:24b` 사용 시 기본 모델 변경/운영 절차 정리

## Out Of Scope

- 서버 드라이버 직접 변경
- Ollama 모델 교체 구현
- systemd 서비스 자동 모델 변경 구현
- full eval 재실행

## Assumptions

- 운영 서버는 Ubuntu 20.04.6 LTS일 수 있다.
- GPU를 사용할 수 있으나 NVIDIA driver와 PyTorch CUDA wheel 버전이 맞아야 한다.
- `gemma4:24b`는 서버 리소스가 충분한 경우에만 운영 모델로 사용한다.

## Pre-flight checks

- `docs/manual-deployment-guide.md` 현재 절차 확인
- `requirements.txt`의 Linux SQLite 대응 확인
- 서버에서 확인한 수동 조치 사항을 추정이 아닌 운영 메모로 분리

## Steps

1. Ubuntu 20.04 Python 3.11 소스 빌드 절차를 배포 가이드에 보강한다.
2. Chroma SQLite 오류와 대응 절차를 배포 가이드에 추가한다.
3. GPU 사용 시 `nvidia-smi`, PyTorch CUDA 확인, CUDA wheel 재설치 절차를 추가한다.
4. `gemma4:24b` 모델 사용 시 서비스 재시작 후 모델 변경 절차와 영구 기본값 변경 후보를 정리한다.
5. 문서 검증과 Python compile 검증을 실행한다.

## Automated tests

- `bash scripts/validate-docs.sh`
- `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py scripts/source_drift_report.py ingestion/embedder.py ingestion/vector_store.py`
- `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260528_115250_location_dispute_added.json --fail-on-critical`

## Manual/Runtime QA

- 실제 서버 명령은 문서화 범위로 제한하고, 이미 서버에서 확인한 증상과 조치 결과를 운영 절차에 반영한다.

## Skipped/Not Run

- Ubuntu 서버에서 드라이버 설치/재부팅은 이 로컬 문서 작업에서 실행하지 않는다.
- full eval은 로컬 모델/Ollama 런타임 의존성이 있어 이 문서 작업 범위에서 재실행하지 않는다.

## Progress

- `docs/manual-deployment-guide.md`에 Ubuntu 20.04.6 Python 3.11 소스 빌드 대체 경로를 추가했다.
- 낮은 SQLite 버전에서 Chroma가 실패하는 경우와 `pysqlite3-binary` 대응을 문서화했다.
- GPU 사용 시 NVIDIA driver와 PyTorch CUDA wheel 정합성 확인 및 `cu118` 재설치 절차를 문서화했다.
- `gemma4:24b` 운영 모델 사용 시 모델 pull과 모델 변경 API 절차를 문서화했다.

## Validation Result

- 통과: `bash scripts/validate-docs.sh`
- 통과: `.venv/bin/python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py scripts/source_drift_report.py ingestion/embedder.py ingestion/vector_store.py`
- 통과: `.venv/bin/python scripts/source_drift_report.py eval/results/eval_20260528_115250_location_dispute_added.json --fail-on-critical`

## Completion

- Ubuntu 20.04 서버 수동 배포 중 확인한 Python 3.11 소스 빌드, Chroma SQLite, GPU/PyTorch CUDA, `gemma4:24b` 운영 절차를 `docs/manual-deployment-guide.md`에 반영했다.
- source drift CI promotion 변경을 포함한 PR #28의 Static checks가 통과했다.

## Open Work

- 없음.
