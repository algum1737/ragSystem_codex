import asyncio
import os
import platform
import re
import logging
import shutil
import subprocess
import tempfile
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
import uuid
from contextlib import asynccontextmanager, suppress
from datetime import datetime, timezone
from pathlib import Path

import requests

from fastapi import FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from ingestion.parsers import DocxParser, PdfParser, HwpParser
from ingestion.pipeline import IngestionPipeline
from ingestion.vector_store import VectorStore
from ingestion.embedder import EmbeddingEngine
from retriever.llm import OllamaLLM
from retriever.engine import RAGEngine
from generator.rfp_analyzer import RFPAnalyzer
from generator.section_generator import SectionGenerator, DEFAULT_SECTIONS
from generator.pptx_writer import PptxWriter
from .models import (
    HealthResponse,
    RuntimeResourcesHistoryResponse,
    RuntimeResourcesResponse,
    StatsResponse,
    QueryRequest,
    QueryResponse,
    SourceItem,
    IngestResponse,
    GenerateResponse,
    StatusResponse,
    ModelChangeRequest,
    ModelChangeResponse,
    PullRequest,
    PullResponse,
    PullStatusResponse,
    ModelDeleteRequest,
    ModelDeleteResponse,
    ResetResponse,
    VALID_DOC_TYPES,
    VALID_DOC_TYPES_LABEL,
)

logger = logging.getLogger(__name__)

_DB_PATH = "./chroma_db"
_COLLECTION = "ragSystem"
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # audit-added: 50MB 상한 — 무제한 read()로 OOM 방지
RESOURCE_SAMPLE_INTERVAL_SECONDS = 5
RESOURCE_HISTORY_MAX_SAMPLES = 720

# in-memory task store: task_id → {status, progress, current_section, output_path, error}
_task_store: dict[str, dict] = {}

# in-memory pull store: pull_id → {model, status, progress, current_status, error}
_pull_store: dict[str, dict] = {}

# in-memory runtime resource samples. API 프로세스 재시작 시 초기화된다.
_resource_history: deque[dict] = deque(maxlen=RESOURCE_HISTORY_MAX_SAMPLES)


def _run_command(args: list[str], timeout: int = 5) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as e:
        return 127, "", str(e)
    except subprocess.TimeoutExpired as e:
        return 124, e.stdout or "", e.stderr or "command timed out"
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def _find_command(name: str, candidates: list[str]) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for candidate in candidates:
        path = Path(candidate)
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
    return None


def _bytes_to_gb(value: float | int | None) -> float | None:
    if value is None:
        return None
    return round(float(value) / 1024 / 1024 / 1024, 2)


def _collect_cpu_memory() -> tuple[dict, dict]:
    cpu: dict = {
        "available": True,
        "source": "stdlib",
        "logical_cpus": os.cpu_count(),
        "platform": platform.system(),
    }
    memory: dict = {"available": False, "source": "unavailable"}

    try:
        import psutil  # type: ignore

        vm = psutil.virtual_memory()
        cpu.update(
            {
                "source": "psutil",
                "usage_percent": psutil.cpu_percent(interval=0.1),
                "load_average_1m": os.getloadavg()[0] if hasattr(os, "getloadavg") else None,
            }
        )
        memory = {
            "available": True,
            "source": "psutil",
            "total_gb": _bytes_to_gb(vm.total),
            "used_gb": _bytes_to_gb(vm.used),
            "available_gb": _bytes_to_gb(vm.available),
            "usage_percent": vm.percent,
        }
        return cpu, memory
    except Exception as e:
        cpu["psutil_error"] = str(e)

    if hasattr(os, "getloadavg"):
        load1, load5, load15 = os.getloadavg()
        logical_cpus = os.cpu_count() or 1
        cpu.update(
            {
                "load_average_1m": round(load1, 2),
                "load_average_5m": round(load5, 2),
                "load_average_15m": round(load15, 2),
                "load_percent_1m": round((load1 / logical_cpus) * 100, 1),
            }
        )

    if platform.system() == "Linux":
        meminfo_path = Path("/proc/meminfo")
        if meminfo_path.exists():
            values: dict[str, int] = {}
            for line in meminfo_path.read_text(encoding="utf-8").splitlines():
                key, _, rest = line.partition(":")
                parts = rest.strip().split()
                if parts and parts[0].isdigit():
                    values[key] = int(parts[0]) * 1024
            total = values.get("MemTotal")
            available = values.get("MemAvailable")
            if total and available is not None:
                used = total - available
                memory = {
                    "available": True,
                    "source": "/proc/meminfo",
                    "total_gb": _bytes_to_gb(total),
                    "used_gb": _bytes_to_gb(used),
                    "available_gb": _bytes_to_gb(available),
                    "usage_percent": round((used / total) * 100, 1),
                }
    elif platform.system() == "Darwin":
        total_code, total_out, total_err = _run_command(["sysctl", "-n", "hw.memsize"], timeout=3)
        vm_code, vm_out, vm_err = _run_command(["vm_stat"], timeout=3)
        if total_code == 0 and vm_code == 0 and total_out.strip().isdigit():
            total = int(total_out.strip())
            page_size_match = re.search(r"page size of (\d+) bytes", vm_out)
            page_size = int(page_size_match.group(1)) if page_size_match else 4096
            pages: dict[str, int] = {}
            for line in vm_out.splitlines():
                key, _, rest = line.partition(":")
                number = re.sub(r"[^0-9]", "", rest)
                if number:
                    pages[key.strip()] = int(number)
            free_pages = (
                pages.get("Pages free", 0)
                + pages.get("Pages inactive", 0)
                + pages.get("Pages speculative", 0)
            )
            available = free_pages * page_size
            used = max(total - available, 0)
            memory = {
                "available": True,
                "source": "vm_stat",
                "total_gb": _bytes_to_gb(total),
                "used_gb": _bytes_to_gb(used),
                "available_gb": _bytes_to_gb(available),
                "usage_percent": round((used / total) * 100, 1),
            }
        else:
            memory = {
                "available": False,
                "source": "vm_stat",
                "error": total_err or vm_err or "memory command failed",
            }

    return cpu, memory


def _collect_gpus() -> tuple[bool, list[dict], str]:
    nvidia_smi = _find_command("nvidia-smi", ["/usr/bin/nvidia-smi", "/bin/nvidia-smi", "/usr/local/bin/nvidia-smi"])
    if not nvidia_smi:
        return False, [], "nvidia-smi not found"

    query = "index,name,utilization.gpu,memory.used,memory.total,temperature.gpu"
    code, out, err = _run_command(
        [nvidia_smi, f"--query-gpu={query}", "--format=csv,noheader,nounits"],
        timeout=5,
    )
    if code != 0:
        return False, [], err or out or f"nvidia-smi exited with {code}"

    gpus: list[dict] = []
    for line in out.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 6:
            continue
        index, name, util, mem_used, mem_total, temp = parts
        try:
            used = float(mem_used)
            total = float(mem_total)
            memory_percent = round((used / total) * 100, 1) if total else None
        except ValueError:
            memory_percent = None
        gpus.append(
            {
                "index": index,
                "name": name,
                "utilization_percent": float(util) if util.replace(".", "", 1).isdigit() else None,
                "memory_used_mib": float(mem_used) if mem_used.replace(".", "", 1).isdigit() else None,
                "memory_total_mib": float(mem_total) if mem_total.replace(".", "", 1).isdigit() else None,
                "memory_percent": memory_percent,
                "temperature_c": float(temp) if temp.replace(".", "", 1).isdigit() else None,
            }
        )
    return True, gpus, ""


def _collect_ollama_ps() -> dict:
    ollama = _find_command("ollama", ["/usr/local/bin/ollama", "/usr/bin/ollama", "/bin/ollama"])
    if not ollama:
        return {"available": False, "loaded": False, "models": [], "error": "ollama command not found"}

    code, out, err = _run_command([ollama, "ps"], timeout=5)
    if code != 0:
        return {"available": False, "loaded": False, "models": [], "error": err or out}

    lines = [line for line in out.splitlines() if line.strip()]
    models: list[dict] = []
    for line in lines[1:]:
        parts = re.split(r"\s{2,}", line.strip())
        models.append(
            {
                "name": parts[0] if len(parts) > 0 else "",
                "id": parts[1] if len(parts) > 1 else "",
                "size": parts[2] if len(parts) > 2 else "",
                "processor": parts[3] if len(parts) > 3 else "",
                "context": parts[4] if len(parts) > 4 else "",
                "until": parts[5] if len(parts) > 5 else "",
            }
        )
    return {
        "available": True,
        "loaded": bool(models),
        "models": models,
        "raw": out,
    }


def _collect_runtime_resources() -> dict:
    cpu, memory = _collect_cpu_memory()
    gpu_available, gpus, gpu_error = _collect_gpus()
    ollama = _collect_ollama_ps()
    if gpu_error:
        gpu_status = {"available": gpu_available, "error": gpu_error}
    else:
        gpu_status = {"available": gpu_available}
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cpu": cpu,
        "memory": memory,
        "gpu_status": gpu_status,
        "gpu_available": gpu_available,
        "gpus": gpus,
        "ollama": ollama,
    }


def _append_resource_sample(resources: dict) -> None:
    sample = {
        "timestamp": resources["generated_at"],
        "gpu_available": resources.get("gpu_available", False),
        "gpus": [
            {
                "index": gpu.get("index"),
                "name": gpu.get("name"),
                "utilization_percent": gpu.get("utilization_percent"),
                "memory_percent": gpu.get("memory_percent"),
                "memory_used_mib": gpu.get("memory_used_mib"),
                "memory_total_mib": gpu.get("memory_total_mib"),
                "temperature_c": gpu.get("temperature_c"),
            }
            for gpu in resources.get("gpus", [])
        ],
    }
    _resource_history.append(sample)


async def _resource_sampler() -> None:
    while True:
        try:
            resources = await asyncio.to_thread(_collect_runtime_resources)
            _append_resource_sample(resources)
        except Exception as e:
            logger.debug("리소스 샘플 수집 실패: %s", e)
        await asyncio.sleep(RESOURCE_SAMPLE_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("서버 시작: 싱글턴 서비스 초기화 중...")
    # audit-added: 시작 실패 시 어느 서비스가 원인인지 명시적 로깅
    try:
        # VectorStore와 EmbeddingEngine은 query/ingest 양쪽에서 공유
        app.state.vector_store = VectorStore(db_path=_DB_PATH, collection_name=_COLLECTION)
        app.state.embedding_engine = EmbeddingEngine()
        app.state.llm = OllamaLLM()
        app.state.rag_engine = RAGEngine(
            vector_store=app.state.vector_store,
            embedding_engine=app.state.embedding_engine,
            llm=app.state.llm,
        )
        # IngestionPipeline은 자체 EmbeddingEngine을 내부 생성하나
        # sentence-transformers가 모델을 메모리 캐싱하므로 두 번째 로드는 무시할 수준
        app.state.pipeline = IngestionPipeline(db_path=_DB_PATH, collection_name=_COLLECTION)
        app.state.rfp_analyzer = RFPAnalyzer(llm=app.state.llm)
        app.state.section_generator = SectionGenerator(
            rag_engine=app.state.rag_engine,
            llm=app.state.llm,
        )
        app.state.pptx_writer = PptxWriter()
    except Exception as e:
        logger.critical("서버 시작 실패 — 서비스 초기화 오류: %s", e, exc_info=True)
        raise
    app.state.resource_sampler = asyncio.create_task(_resource_sampler())
    logger.info("서버 시작 완료")
    try:
        yield
    finally:
        app.state.resource_sampler.cancel()
        with suppress(asyncio.CancelledError):
            await app.state.resource_sampler
        logger.info("서버 종료")


app = FastAPI(title="ragSystem API", version="0.1.0", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
async def health(request: Request):
    return HealthResponse(status="ok", model=request.app.state.llm.model)


@app.put("/model", response_model=ModelChangeResponse)
async def change_model(body: ModelChangeRequest, request: Request):
    previous = request.app.state.llm.model
    request.app.state.llm = OllamaLLM(model=body.model, base_url=request.app.state.llm.base_url)
    request.app.state.rag_engine.llm = request.app.state.llm
    request.app.state.rfp_analyzer.llm = request.app.state.llm
    request.app.state.section_generator.llm = request.app.state.llm
    logger.info("모델 변경: %s → %s", previous, body.model)
    return ModelChangeResponse(model=body.model, previous_model=previous)


@app.delete("/model", response_model=ModelDeleteResponse)
async def delete_model(body: ModelDeleteRequest):
    resp = requests.delete(
        "http://localhost:11434/api/delete",
        json={"name": body.model},
        timeout=30,
    )
    if resp.status_code not in (200, 404):
        raise HTTPException(status_code=resp.status_code, detail=f"Ollama 삭제 실패: {resp.text}")
    logger.info("모델 삭제: %s", body.model)
    return ModelDeleteResponse(model=body.model, deleted=True)


def _do_pull(pull_id: str, model: str) -> None:
    """Ollama pull API를 스트리밍으로 호출해 진행률을 _pull_store에 기록."""
    import json as _json
    _pull_store[pull_id]["status"] = "pulling"
    try:
        with requests.post(
            "http://localhost:11434/api/pull",
            json={"name": model},
            stream=True,
            timeout=1800,
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    chunk = _json.loads(line)
                except Exception:
                    continue
                status_msg = chunk.get("status", "")
                total = chunk.get("total", 0)
                completed = chunk.get("completed", 0)
                if total and total > 0:
                    _pull_store[pull_id]["progress"] = int(completed / total * 100)
                _pull_store[pull_id]["current_status"] = status_msg
                if chunk.get("status") == "success":
                    break
        _pull_store[pull_id]["status"] = "completed"
        _pull_store[pull_id]["progress"] = 100
        logger.info("모델 pull 완료: %s", model)
    except Exception as e:
        logger.error("모델 pull 실패 model=%s: %s", model, e)
        _pull_store[pull_id]["status"] = "failed"
        _pull_store[pull_id]["error"] = str(e)


async def _pull_model_task(pull_id: str, model: str) -> None:
    await asyncio.get_event_loop().run_in_executor(None, _do_pull, pull_id, model)


@app.post("/model/pull", response_model=PullResponse)
async def pull_model(body: PullRequest):
    pull_id = str(uuid.uuid4())
    _pull_store[pull_id] = {
        "model": body.model,
        "status": "queued",
        "progress": 0,
        "current_status": "",
        "error": "",
    }
    asyncio.create_task(_pull_model_task(pull_id, body.model))
    return PullResponse(pull_id=pull_id, model=body.model, status="queued")


@app.get("/model/pull/{pull_id}", response_model=PullStatusResponse)
async def pull_status(pull_id: str):
    if pull_id not in _pull_store:
        raise HTTPException(status_code=404, detail="pull_id를 찾을 수 없습니다")
    p = _pull_store[pull_id]
    return PullStatusResponse(
        pull_id=pull_id,
        model=p["model"],
        status=p["status"],
        progress=p["progress"],
        current_status=p["current_status"],
        error=p["error"],
    )


@app.delete("/reset", response_model=ResetResponse)
async def reset_db(request: Request):
    request.app.state.vector_store.reset()
    request.app.state.pipeline._store.reset()
    logger.warning("벡터 DB 초기화 완료")
    return ResetResponse(reset=True, collection_name=_COLLECTION)


@app.get("/stats", response_model=StatsResponse)
async def stats(request: Request):
    s = request.app.state.vector_store.get_stats()
    return StatsResponse(**s)


@app.get("/runtime/resources", response_model=RuntimeResourcesResponse)
async def runtime_resources():
    resources = _collect_runtime_resources()
    _append_resource_sample(resources)
    return RuntimeResourcesResponse(**resources)


@app.get("/runtime/resources/history", response_model=RuntimeResourcesHistoryResponse)
async def runtime_resources_history():
    if not _resource_history:
        resources = _collect_runtime_resources()
        _append_resource_sample(resources)
    return RuntimeResourcesHistoryResponse(
        generated_at=datetime.now(timezone.utc).isoformat(),
        interval_seconds=RESOURCE_SAMPLE_INTERVAL_SECONDS,
        max_samples=RESOURCE_HISTORY_MAX_SAMPLES,
        samples=list(_resource_history),
    )


@app.post("/query", response_model=QueryResponse)
async def query(body: QueryRequest, request: Request):
    try:
        result = request.app.state.rag_engine.query(
            body.question,
            doc_type=body.doc_type,
            trace_route="api.query",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    sources = [SourceItem(**s) for s in result["sources"]]
    return QueryResponse(answer=result["answer"], sources=sources, query=result["query"])


@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile, request: Request, doc_type: str | None = Form(None)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".docx", ".doc", ".hwp", ".txt", ".md"}:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식: {suffix or '(없음)'}. 지원: .pdf, .docx, .doc, .hwp, .txt, .md",
        )
    if doc_type not in VALID_DOC_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"유효하지 않은 doc_type: {doc_type!r}. 허용 값: {VALID_DOC_TYPES_LABEL}",
        )
    content = await file.read()
    # audit-added: 무제한 read()로 OOM 방지 — 50MB 초과 시 413
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"파일 크기 초과: {len(content) // 1024 // 1024}MB (최대 {MAX_UPLOAD_BYTES // 1024 // 1024}MB)",
        )
    # audit-added: tmp_path = None 초기화 후 단일 try/finally — write 실패 시에도 파일 누수 없음
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)
        result = request.app.state.pipeline.ingest(tmp_path, source_name=file.filename, doc_type=doc_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("인제스천 실패: %s", e)
        raise HTTPException(status_code=500, detail=f"인제스천 오류: {e}")
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
    return IngestResponse(**result)


async def _run_generation(
    task_id: str,
    rfp_content: bytes,
    rfp_suffix: str,
    template_content: bytes | None,
    project_name: str,
    section_names: list[str],
    request: Request,
) -> None:
    _task_store[task_id]["status"] = "processing"
    tmp_rfp = None
    tmp_template = None
    try:
        with tempfile.NamedTemporaryFile(suffix=rfp_suffix, delete=False) as f:
            f.write(rfp_content)
            tmp_rfp = Path(f.name)

        if template_content is not None:
            with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as f:
                f.write(template_content)
                tmp_template = Path(f.name)

        _parser_map = {".pdf": PdfParser, ".docx": DocxParser, ".doc": DocxParser, ".hwp": HwpParser}
        parser = _parser_map.get(rfp_suffix, DocxParser)()
        rfp_text = parser.parse(tmp_rfp).text
        rfp_analysis = await asyncio.get_event_loop().run_in_executor(
            None, lambda: request.app.state.rfp_analyzer.analyze(rfp_text)
        )

        for i, section_name in enumerate(section_names):
            _task_store[task_id]["current_section"] = section_name
            _task_store[task_id]["progress"] = int(i / len(section_names) * 90)

        sections_result = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: request.app.state.section_generator.generate_all(
                rfp_analysis, rfp_text, project_name
            ),
        )

        output_path = Path("data/outputs") / f"{task_id}.pptx"
        request.app.state.pptx_writer.write(sections_result, tmp_template, output_path)

        _task_store[task_id]["status"] = "completed"
        _task_store[task_id]["progress"] = 100
        _task_store[task_id]["output_path"] = str(output_path)
    except Exception as e:
        logger.error("생성 작업 실패 task_id=%s: %s", task_id, e, exc_info=True)
        _task_store[task_id]["status"] = "failed"
        _task_store[task_id]["error"] = str(e)
    finally:
        if tmp_rfp is not None:
            tmp_rfp.unlink(missing_ok=True)
        if tmp_template is not None:
            tmp_template.unlink(missing_ok=True)


@app.post("/generate", response_model=GenerateResponse)
async def generate(
    rfp_file: UploadFile,
    request: Request,
    project_name: str = Form(...),
    template_file: UploadFile | None = None,
):
    _SUPPORTED = {".pdf", ".docx", ".doc", ".hwp"}
    suffix = Path(rfp_file.filename or "").suffix.lower()
    if suffix not in _SUPPORTED:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 형식: {suffix or '(없음)'}. 지원: .pdf, .docx, .doc, .hwp",
        )

    rfp_content = await rfp_file.read()
    if len(rfp_content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"파일 크기 초과 (최대 {MAX_UPLOAD_BYTES // 1024 // 1024}MB)",
        )

    template_content: bytes | None = None
    if template_file is not None:
        template_content = await template_file.read()

    task_id = str(uuid.uuid4())
    section_names = DEFAULT_SECTIONS
    _task_store[task_id] = {
        "status": "queued",
        "progress": 0,
        "current_section": "",
        "output_path": "",
        "error": "",
    }

    asyncio.create_task(
        _run_generation(
            task_id, rfp_content, suffix, template_content,
            project_name, section_names, request,
        )
    )
    return GenerateResponse(
        task_id=task_id,
        status="queued",
        estimated_seconds=len(section_names) * 30,
    )


@app.get("/status/{task_id}", response_model=StatusResponse)
async def get_status(task_id: str):
    if task_id not in _task_store:
        raise HTTPException(status_code=404, detail="task_id를 찾을 수 없습니다")
    t = _task_store[task_id]
    return StatusResponse(
        task_id=task_id,
        status=t["status"],
        progress=t["progress"],
        current_section=t["current_section"],
        error=t["error"],
    )


@app.get("/download/{task_id}")
async def download(task_id: str):
    if task_id not in _task_store:
        raise HTTPException(status_code=404, detail="task_id를 찾을 수 없습니다")
    t = _task_store[task_id]
    if t["status"] != "completed":
        raise HTTPException(status_code=400, detail="아직 생성 중입니다")
    output_path = Path(t["output_path"])
    if not output_path.exists():
        raise HTTPException(status_code=500, detail="출력 파일을 찾을 수 없습니다")
    return FileResponse(
        str(output_path),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=f"{task_id}.pptx",
    )
