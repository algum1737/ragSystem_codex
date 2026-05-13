# Manual Deployment Guide

이 문서는 Git을 사용하지 않고 Ubuntu 20.04.5 LTS 회사 서버에 프로젝트를 수동 배포하고, 이후 수정 사항을 다시 반영하는 절차를 정리한다.

## Assumptions

- 서버 OS는 Ubuntu 20.04.5 LTS다.
- 배포 계정은 `ragsystem` 전용 계정을 사용한다.
- 배포 경로는 `/opt/ragSystem_codex`다.
- Git clone 대신 로컬 프로젝트를 `tar.gz`로 묶어 서버에 업로드한다.
- FastAPI는 `8000`, Streamlit은 `8501`, Ollama는 서버 내부 `11434` 포트를 사용한다.
- Ollama 포트 `11434`는 외부에 공개하지 않는다.

## 1. Server Prerequisites

관리자 권한이 있는 계정으로 서버에 접속해 기본 패키지와 Python 3.11을 설치한다.

```bash
sudo apt update
sudo apt install -y software-properties-common curl build-essential
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
```

Ollama를 설치하고 서비스로 기동한다.

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable ollama
sudo systemctl start ollama
curl http://localhost:11434/api/tags
```

기본 LLM 모델을 준비한다.

```bash
ollama pull gemma3:12b
```

## 2. Deployment Account

전용 계정이 없다면 생성한다.

```bash
sudo adduser ragsystem
sudo usermod -aG sudo ragsystem
sudo mkdir -p /home/ragsystem/.ssh
sudo chmod 700 /home/ragsystem/.ssh
sudo chown -R ragsystem:ragsystem /home/ragsystem/.ssh
```

로컬 PC의 공개키를 `/home/ragsystem/.ssh/authorized_keys`에 등록한다.

```bash
sudo nano /home/ragsystem/.ssh/authorized_keys
sudo chmod 600 /home/ragsystem/.ssh/authorized_keys
sudo chown ragsystem:ragsystem /home/ragsystem/.ssh/authorized_keys
```

배포 디렉터리를 만든다.

```bash
sudo mkdir -p /opt/ragSystem_codex
sudo chown -R ragsystem:ragsystem /opt/ragSystem_codex
```

## 3. Package Locally

로컬 머신에서 프로젝트를 압축한다.

```bash
cd /Users/hun/workspace

tar \
  --exclude='ragSystem_codex/.git' \
  --exclude='ragSystem_codex/.venv' \
  --exclude='ragSystem_codex/__pycache__' \
  --exclude='ragSystem_codex/**/__pycache__' \
  -czf ragSystem_codex.tar.gz ragSystem_codex
```

이미 인제스천한 데이터를 서버에 같이 올리려면 `chroma_db`를 제외하지 않는다. 서버에서 새로 인제스천할 계획이면 아래 옵션을 추가한다.

```bash
--exclude='ragSystem_codex/chroma_db'
```

## 4. Upload And Extract

로컬 머신에서 서버로 압축 파일을 업로드한다.

```bash
scp ragSystem_codex.tar.gz ragsystem@SERVER_IP:/home/ragsystem/
```

서버에 접속해 압축을 해제한다.

```bash
ssh ragsystem@SERVER_IP
cd /opt
tar -xzf /home/ragsystem/ragSystem_codex.tar.gz -C /opt
ls /opt/ragSystem_codex
```

## 5. Python Environment

서버에서 가상환경을 만들고 의존성을 설치한다.

```bash
cd /opt/ragSystem_codex
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Model Cache

임베딩 모델 캐시를 준비한다.

```bash
cd /opt/ragSystem_codex
source .venv/bin/activate
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-large')"
python -c "from sentence_transformers import SentenceTransformer; m=SentenceTransformer('intfloat/multilingual-e5-large'); print(m.get_sentence_embedding_dimension())"
```

정상 출력은 `1024`다.

서버가 오프라인이면 로컬 머신의 `~/.cache/huggingface/`를 서버의 같은 사용자 홈으로 복사한 뒤 위 확인 명령을 실행한다.

## 7. Manual Run

FastAPI를 실행한다.

```bash
cd /opt/ragSystem_codex
source .venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

다른 터미널에서 Streamlit Web UI를 실행한다.

```bash
cd /opt/ragSystem_codex
source .venv/bin/activate
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

서버 내부에서 확인한다.

```bash
curl http://localhost:8000/health
curl http://localhost:8000/stats
```

브라우저에서는 아래 주소로 접속한다.

```text
http://SERVER_IP:8501
```

## 8. systemd Services

상시 실행하려면 FastAPI와 Streamlit을 systemd 서비스로 등록한다.

`/etc/systemd/system/ragsystem-api.service`

```ini
[Unit]
Description=ragSystem FastAPI
After=network.target ollama.service

[Service]
User=ragsystem
WorkingDirectory=/opt/ragSystem_codex
Environment="PATH=/opt/ragSystem_codex/.venv/bin"
ExecStart=/opt/ragSystem_codex/.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

`/etc/systemd/system/ragsystem-web.service`

```ini
[Unit]
Description=ragSystem Streamlit Web
After=network.target ragsystem-api.service

[Service]
User=ragsystem
WorkingDirectory=/opt/ragSystem_codex
Environment="PATH=/opt/ragSystem_codex/.venv/bin"
ExecStart=/opt/ragSystem_codex/.venv/bin/streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

서비스를 적용한다.

```bash
sudo systemctl daemon-reload
sudo systemctl enable ragsystem-api ragsystem-web
sudo systemctl start ragsystem-api ragsystem-web
sudo systemctl status ragsystem-api
sudo systemctl status ragsystem-web
```

로그 확인:

```bash
journalctl -u ragsystem-api -f
journalctl -u ragsystem-web -f
```

## 9. Update And Redeploy Without Git

수정 사항을 반영할 때는 로컬에서 다시 압축해 서버에 올리고, 서버에서 기존 디렉터리를 백업한 뒤 교체한다.

로컬에서 새 패키지를 만든다.

```bash
cd /Users/hun/workspace

tar \
  --exclude='ragSystem_codex/.git' \
  --exclude='ragSystem_codex/.venv' \
  --exclude='ragSystem_codex/__pycache__' \
  --exclude='ragSystem_codex/**/__pycache__' \
  --exclude='ragSystem_codex/chroma_db' \
  -czf ragSystem_codex.tar.gz ragSystem_codex

scp ragSystem_codex.tar.gz ragsystem@SERVER_IP:/home/ragsystem/
```

서버에서 서비스를 중지하고 기존 배포본을 백업한다.

```bash
sudo systemctl stop ragsystem-web ragsystem-api

cd /opt
cp -a ragSystem_codex ragSystem_codex.backup.$(date +%Y%m%d_%H%M%S)
```

기존 런타임 데이터를 보존한다.

```bash
cp -a /opt/ragSystem_codex/chroma_db /home/ragsystem/chroma_db.backup 2>/dev/null || true
```

새 패키지를 풀고 런타임 데이터를 복구한다.

```bash
cd /opt
rm -rf ragSystem_codex
tar -xzf /home/ragsystem/ragSystem_codex.tar.gz -C /opt

if [ -d /home/ragsystem/chroma_db.backup ]; then
  cp -a /home/ragsystem/chroma_db.backup /opt/ragSystem_codex/chroma_db
fi

sudo chown -R ragsystem:ragsystem /opt/ragSystem_codex
```

의존성이 바뀌었을 수 있으므로 가상환경을 확인한다.

```bash
cd /opt/ragSystem_codex
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

검증 후 서비스를 재시작한다.

```bash
python -m py_compile eval/pipeline.py retriever/engine.py api/models.py api/main.py app.py
curl http://localhost:11434/api/tags

sudo systemctl start ragsystem-api ragsystem-web
sudo systemctl status ragsystem-api
sudo systemctl status ragsystem-web

curl http://localhost:8000/health
curl http://localhost:8000/stats
```

브라우저에서 `http://SERVER_IP:8501` 접속을 확인한다.

## 10. Firewall And Exposure

직접 포트 접속을 허용해야 한다면 최소한 Streamlit 포트만 제한적으로 연다.

```bash
sudo ufw allow from TRUSTED_IP to any port 8501 proto tcp
```

FastAPI `8000`과 Ollama `11434`는 외부에 직접 공개하지 않는 것을 원칙으로 한다. 외부 공개가 필요하면 Nginx reverse proxy, VPN, 사내망 접근 제한, 인증 계층을 먼저 둔다.

## 11. Rollback

배포 후 문제가 생기면 백업 디렉터리로 되돌린다.

```bash
sudo systemctl stop ragsystem-web ragsystem-api

cd /opt
rm -rf ragSystem_codex
cp -a ragSystem_codex.backup.YYYYMMDD_HHMMSS ragSystem_codex
sudo chown -R ragsystem:ragsystem ragSystem_codex

sudo systemctl start ragsystem-api ragsystem-web
curl http://localhost:8000/health
```
