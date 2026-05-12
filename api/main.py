import asyncio
import logging
import tempfile

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
import uuid
from contextlib import asynccontextmanager
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
)

logger = logging.getLogger(__name__)

_DB_PATH = "./chroma_db"
_COLLECTION = "ragSystem"
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # audit-added: 50MB 상한 — 무제한 read()로 OOM 방지
_VALID_DOC_TYPES = {None, "일반약관", "위치기반약관"}

# in-memory task store: task_id → {status, progress, current_section, output_path, error}
_task_store: dict[str, dict] = {}

# in-memory pull store: pull_id → {model, status, progress, current_status, error}
_pull_store: dict[str, dict] = {}


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
    logger.info("서버 시작 완료")
    yield
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


@app.post("/query", response_model=QueryResponse)
async def query(body: QueryRequest, request: Request):
    try:
        result = request.app.state.rag_engine.query(body.question, doc_type=body.doc_type)
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
    if doc_type not in _VALID_DOC_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"유효하지 않은 doc_type: {doc_type!r}. 허용 값: 일반약관, 위치기반약관",
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
