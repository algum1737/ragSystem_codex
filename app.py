import time

import requests
import streamlit as st

API_BASE = "http://localhost:8000"


def _detail(resp) -> str:
    try:
        return resp.json().get("detail", resp.text)
    except Exception:
        return resp.text or f"HTTP {resp.status_code}"

st.set_page_config(page_title="ragSystem", layout="wide")
st.title("ragSystem — 문서 조회")

tab_ingest, tab_query, tab_system, tab_ppt = st.tabs(["인제스천", "쿼리", "시스템", "PPT 생성"])


# ── 인제스천 탭 ──────────────────────────────────────────────────────────────
with tab_ingest:
    st.header("문서 인제스천")
    st.caption("PDF, DOCX, DOC, HWP, TXT, MD 파일을 업로드하여 벡터 DB에 인덱싱합니다.")

    uploaded_files = st.file_uploader(
        "문서 업로드 (여러 파일 동시 선택 가능)",
        type=["pdf", "docx", "doc", "hwp", "txt", "md"],
        key="ingest_file",
        accept_multiple_files=True,
    )

    _ingest_doc_type_options = {"선택 안 함": None, "일반약관": "일반약관", "위치기반약관": "위치기반약관"}
    _ingest_doc_type = _ingest_doc_type_options[
        st.selectbox("문서 유형", list(_ingest_doc_type_options.keys()), key="ingest_doc_type")
    ]

    start_btn = st.button(
        "인제스천 시작",
        disabled=(not uploaded_files),
        key="ingest_btn",
    )

    @st.dialog("벡터 DB 초기화 확인")
    def confirm_reset_dialog():
        st.warning("인덱싱된 모든 문서가 삭제됩니다. 이 작업은 되돌릴 수 없습니다.")
        c1, c2 = st.columns(2)
        if c1.button("초기화 실행", type="primary", key="reset_confirm_btn"):
            try:
                resp = requests.delete(f"{API_BASE}/reset", timeout=30)
                if resp.status_code == 200:
                    st.success("초기화 완료")
                    st.rerun()
                else:
                    st.error(f"초기화 실패: {_detail(resp)}")
            except requests.exceptions.ConnectionError:
                st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")
        if c2.button("취소", key="reset_cancel_btn"):
            st.rerun()

    if st.button("🗑 전체 초기화", key="reset_btn"):
        confirm_reset_dialog()

    if start_btn and uploaded_files:
        total = len(uploaded_files)
        success_count = 0
        total_chunks = 0
        progress_bar = st.progress(0, text=f"0 / {total} 처리 중...")

        for i, uf in enumerate(uploaded_files):
            progress_bar.progress((i) / total, text=f"({i + 1}/{total}) {uf.name} 처리 중...")
            try:
                _ingest_data = {"doc_type": _ingest_doc_type} if _ingest_doc_type else {}
                resp = requests.post(
                    f"{API_BASE}/ingest",
                    files={"file": (uf.name, uf.getvalue())},
                    data=_ingest_data,
                    timeout=120,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.success(
                        f"✔ {uf.name} — 청크 {data['chunks_added']}개 추가 | 파서: {data['parser']}"
                    )
                    success_count += 1
                    total_chunks += data["chunks_added"]
                elif resp.status_code == 400:
                    st.error(f"✘ {uf.name} — {_detail(resp)}")
                elif resp.status_code == 413:
                    st.error(f"✘ {uf.name} — 파일이 너무 큽니다 (최대 50MB)")
                else:
                    st.error(f"✘ {uf.name} — 서버 오류 {resp.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")
                break
            except Exception as e:
                st.error(f"✘ {uf.name} — {e}")

        progress_bar.progress(1.0, text="완료")
        if total > 1:
            st.info(f"총 {success_count}/{total}개 파일 완료 | 청크 {total_chunks}개 추가됨")


# ── 쿼리 탭 ──────────────────────────────────────────────────────────────────
with tab_query:
    st.header("RAG 질의")
    st.caption("인덱싱된 문서를 기반으로 LLM이 답변을 생성합니다.")

    _query_doc_type_options = {"전체 문서": None, "일반약관": "일반약관", "위치기반약관": "위치기반약관"}
    _query_doc_type = _query_doc_type_options[
        st.selectbox("문서 유형 필터", list(_query_doc_type_options.keys()), key="query_doc_type")
    ]

    question = st.text_area(
        "질문",
        placeholder="예: 서비스 해지 시 환불 정책은 어떻게 되는가?",
        height=100,
        key="query_question",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        top_k = st.slider("Top-K", min_value=1, max_value=10, value=5, key="query_topk")
    with col2:
        search_btn = st.button("검색", key="query_btn")

    if search_btn:
        if not question.strip():
            st.warning("질문을 입력해 주세요.")
            st.stop()

        with st.spinner("LLM 답변 생성 중..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/query",
                    json={"question": question, "top_k": top_k, "doc_type": _query_doc_type},
                    timeout=180,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.markdown("### 답변")
                    st.markdown(data["answer"])

                    sources = data.get("sources", [])
                    if sources:
                        st.markdown("### 출처")
                        st.divider()
                        for src in sources:
                            source_path = src.get("source_path", "알 수 없음")
                            text = src.get("text", "")
                            with st.expander(f"📄 {source_path}"):
                                st.caption(text[:300])
                elif resp.status_code == 422:
                    st.warning("질문을 입력해 주세요.")
                else:
                    st.error(f"서버 오류 {resp.status_code}: {resp.text[:200]}")
            except requests.exceptions.ConnectionError:
                st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")
            except Exception as e:
                st.error(str(e))


# ── 시스템 탭 ──────────────────────────────────────────────────────────────
with tab_system:
    st.header("시스템 상태")

    st.button("새로고침", key="system_refresh")  # 클릭 시 Streamlit 재실행 → API 재호출

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("헬스체크")
        current_model = "-"
        try:
            resp = requests.get(f"{API_BASE}/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                current_model = data.get("model", "-")
                st.metric("상태", data.get("status", "-"))
                st.metric("모델", current_model)
            else:
                st.error(f"헬스체크 실패 ({resp.status_code})")
        except requests.exceptions.ConnectionError:
            st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")
        except Exception as e:
            st.error(str(e))

    with col2:
        st.subheader("벡터 DB 통계")
        try:
            resp = requests.get(f"{API_BASE}/stats", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                st.metric("컬렉션", data.get("collection_name", "-"))
                st.metric("청크 수", data.get("count", 0))
            else:
                st.error(f"통계 조회 실패 ({resp.status_code})")
        except requests.exceptions.ConnectionError:
            st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")
        except Exception as e:
            st.error(str(e))

    st.divider()

    # ── 모델 관리 다이얼로그 ────────────────────────────────────────────────────
    RECOMMENDED_MODELS = [
        {"name": "gemma3:1b",    "size": "815 MB", "desc": "Gemma 3 초경량"},
        {"name": "gemma3:4b",    "size": "3.3 GB",  "desc": "Gemma 3 경량 (빠름)"},
        {"name": "gemma3:12b",   "size": "8.1 GB",  "desc": "Gemma 3 표준 (기본값)"},
        {"name": "gemma3:27b",   "size": "17 GB",   "desc": "Gemma 3 고성능"},
        {"name": "llama3.2:1b",  "size": "1.3 GB",  "desc": "Meta Llama 3.2 초경량"},
        {"name": "llama3.2:3b",  "size": "2.0 GB",  "desc": "Meta Llama 3.2 경량"},
        {"name": "qwen2.5:3b",   "size": "2.0 GB",  "desc": "Qwen 2.5 경량"},
        {"name": "qwen2.5:7b",   "size": "4.7 GB",  "desc": "Qwen 2.5 표준"},
        {"name": "mistral:7b",   "size": "4.1 GB",  "desc": "Mistral 7B"},
        {"name": "phi4-mini:3.8b","size": "2.5 GB", "desc": "Microsoft Phi-4 Mini"},
    ]

    @st.dialog("모델 관리", width="large")
    def model_manager_dialog():
        installed_raw = []
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            if r.status_code == 200:
                installed_raw = r.json().get("models", [])
        except Exception:
            st.warning("Ollama에 연결할 수 없습니다 (localhost:11434)")

        installed_names = {m["name"] for m in installed_raw}

        # ── 설치된 모델 ──
        st.subheader("설치된 모델")
        if installed_raw:
            for m in installed_raw:
                size_gb = m.get("size", 0) / 1024 ** 3
                c1, c2, c3 = st.columns([3, 2, 1])
                c1.write(f"**{m['name']}**")
                c2.caption(f"{size_gb:.1f} GB")
                if c3.button("삭제", key=f"del_{m['name']}"):
                    try:
                        dr = requests.delete(f"{API_BASE}/model", json={"model": m["name"]}, timeout=30)
                        if dr.status_code == 200:
                            st.success(f"`{m['name']}` 삭제 완료")
                            st.rerun()
                        else:
                            st.error(f"삭제 실패: {_detail(dr)}")
                    except requests.exceptions.ConnectionError:
                        st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")
        else:
            st.caption("설치된 모델이 없습니다.")

        st.divider()

        # ── 설치 가능한 모델 ──
        st.subheader("추천 모델")
        custom_name = st.text_input(
            "직접 입력 (ollama.com에서 모델명 복사)",
            placeholder="예: deepseek-r1:7b",
            key="dialog_custom_model",
        )
        for rec in RECOMMENDED_MODELS:
            already = rec["name"] in installed_names
            c1, c2, c3, c4 = st.columns([3, 2, 3, 1])
            c1.write(f"**{rec['name']}**")
            c2.caption(rec["size"])
            c3.caption(rec["desc"])
            label = "설치됨" if already else "설치"
            if c4.button(label, key=f"inst_{rec['name']}", disabled=already):
                _start_pull(rec["name"])

        if custom_name.strip() and custom_name.strip() not in installed_names:
            if st.button(f"**{custom_name.strip()}** 설치", key="inst_custom"):
                _start_pull(custom_name.strip())

    def _start_pull(model_name: str):
        try:
            resp = requests.post(f"{API_BASE}/model/pull", json={"model": model_name}, timeout=10)
            if resp.status_code == 200:
                st.session_state["pull_id"] = resp.json()["pull_id"]
                st.session_state["pull_model"] = model_name
                st.rerun()
            else:
                st.error(f"설치 요청 실패: {_detail(resp)}")
        except requests.exceptions.ConnectionError:
            st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")

    # ── 모델 변경 + 관리 버튼 ──────────────────────────────────────────────────
    st.subheader("모델")
    mgmt_col, change_col = st.columns([1, 3])

    with mgmt_col:
        if st.button("🗂 모델 관리", key="open_model_mgr"):
            model_manager_dialog()

    ollama_models = []
    installed_info = []
    try:
        ollama_resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        if ollama_resp.status_code == 200:
            installed_info = ollama_resp.json().get("models", [])
            ollama_models = [m["name"] for m in installed_info]
    except Exception:
        pass

    with change_col:
        if ollama_models:
            default_idx = ollama_models.index(current_model) if current_model in ollama_models else 0
            selected_model = st.selectbox("사용할 모델", ollama_models, index=default_idx, key="model_select")
            if st.button("변경 적용", key="model_change_btn"):
                try:
                    resp = requests.put(f"{API_BASE}/model", json={"model": selected_model}, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.success(f"변경 완료: {data['previous_model']} → {data['model']}")
                        st.rerun()
                    else:
                        st.error(f"변경 실패: {_detail(resp)}")
                except requests.exceptions.ConnectionError:
                    st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")
        else:
            st.caption("Ollama 모델을 불러올 수 없습니다. 모델 관리에서 설치하세요.")

    # ── 설치 진행률 (다이얼로그 닫힌 후 메인 화면에 표시) ─────────────────────
    if "pull_id" in st.session_state:
        pull_id = st.session_state["pull_id"]
        pull_model_name = st.session_state.get("pull_model", "")
        try:
            pull_resp = requests.get(f"{API_BASE}/model/pull/{pull_id}", timeout=10)
            pull_data = pull_resp.json()
        except requests.exceptions.ConnectionError:
            st.error("API 서버에 연결할 수 없습니다")
            st.stop()

        pull_status = pull_data.get("status", "unknown")
        pull_progress = pull_data.get("progress", 0)
        pull_current = pull_data.get("current_status", "")

        st.divider()
        if pull_status in ("queued", "pulling"):
            st.info(f"`{pull_model_name}` 설치 중... {pull_current}")
            st.progress(min(max(pull_progress, 0), 100) / 100)
            time.sleep(2)
            st.rerun()
        elif pull_status == "completed":
            st.success(f"`{pull_model_name}` 설치 완료!")
            if st.button("확인", key="pull_done_btn"):
                st.session_state.pop("pull_id", None)
                st.session_state.pop("pull_model", None)
                st.rerun()
        elif pull_status == "failed":
            st.error(f"설치 실패: {pull_data.get('error', '알 수 없는 오류')}")
            if st.button("닫기", key="pull_fail_btn"):
                st.session_state.pop("pull_id", None)
                st.session_state.pop("pull_model", None)
                st.rerun()


# ── PPT 생성 탭 ────────────────────────────────────────────────────────────────
with tab_ppt:
    st.header("📊 제안서 초안 생성 — 개발 대기")
    st.caption("RFP 문서를 업로드하면 AI가 7개 섹션 제안서를 자동 생성합니다.")

    rfp_file = st.file_uploader("RFP 문서 (.pdf, .docx, .doc, .hwp)", type=["pdf", "docx", "doc", "hwp"], key="rfp_upload")
    template_file = st.file_uploader("PPT 템플릿 (선택, .pptx)", type=["pptx"], key="tpl_upload")
    project_name = st.text_input("프로젝트명", placeholder="예: 스마트시티 플랫폼 구축")

    col1, col2 = st.columns([1, 4])
    with col1:
        start_btn = st.button(
            "제안서 생성 시작",
            disabled=(rfp_file is None or not project_name.strip()),
            key="ppt_start_btn",
        )

    if start_btn:
        st.session_state.pop("ppt_task_id", None)
        st.session_state.pop("ppt_status", None)
        files = {"rfp_file": (rfp_file.name, rfp_file.getvalue())}
        if template_file:
            files["template_file"] = (template_file.name, template_file.getvalue())
        try:
            resp = requests.post(
                f"{API_BASE}/generate",
                data={"project_name": project_name},
                files=files,
            )
            if resp.status_code == 200:
                task_id = resp.json()["task_id"]
                st.session_state["ppt_task_id"] = task_id
                st.session_state["ppt_status"] = "queued"
                st.session_state["ppt_project_name"] = project_name
                st.rerun()
            else:
                st.error(f"생성 요청 실패: {_detail(resp)}")
        except requests.exceptions.ConnectionError:
            st.error("API 서버에 연결할 수 없습니다 (localhost:8000)")

    if "ppt_task_id" in st.session_state:
        task_id = st.session_state["ppt_task_id"]
        project_name_saved = st.session_state.get("ppt_project_name", "제안서")

        try:
            status_resp = requests.get(f"{API_BASE}/status/{task_id}", timeout=10)
            status_data = status_resp.json()
        except requests.exceptions.ConnectionError:
            st.error("API 서버에 연결할 수 없습니다")
            st.stop()

        status = status_data.get("status", "unknown")
        progress = status_data.get("progress", 0)
        current_section = status_data.get("current_section", "")

        if status in ("queued", "processing"):
            st.info(f"생성 중... {current_section or '준비 중'}")
            st.progress(min(max(progress, 0), 100) / 100)
            time.sleep(1)
            st.rerun()

        elif status == "completed":
            st.success("제안서 초안 생성 완료!")
            try:
                dl_resp = requests.get(f"{API_BASE}/download/{task_id}", timeout=30)
                st.download_button(
                    label="📥 PPTX 다운로드",
                    data=dl_resp.content,
                    file_name=f"{project_name_saved}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )
            except Exception as e:
                st.error(f"다운로드 실패: {e}")
            if st.button("새 제안서 생성", key="ppt_new_btn"):
                st.session_state.pop("ppt_task_id")
                st.rerun()

        elif status == "failed":
            st.error(f"생성 실패: {status_data.get('error', '알 수 없는 오류')}")
            if st.button("다시 시도", key="ppt_retry_btn"):
                st.session_state.pop("ppt_task_id")
                st.rerun()
