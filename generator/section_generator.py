import logging
from dataclasses import dataclass, field

from .rfp_analyzer import RFPAnalysis

logger = logging.getLogger(__name__)

DEFAULT_SECTIONS = [
    "cover", "executive_summary", "problem_analysis",
    "solution", "implementation_plan", "team", "cost",
]

SECTION_PARAMS = {
    "cover":               {"temperature": 0.1,  "max_tokens": 1500},
    "executive_summary":   {"temperature": 0.2,  "max_tokens": 2500},
    "problem_analysis":    {"temperature": 0.15, "max_tokens": 3500},
    "solution":            {"temperature": 0.35, "max_tokens": 6144},
    "implementation_plan": {"temperature": 0.2,  "max_tokens": 5000},
    "team":                {"temperature": 0.1,  "max_tokens": 2000},
    "cost":                {"temperature": 0.1,  "max_tokens": 3000},
}

SECTION_DEPS = {
    "cover":               [],
    "executive_summary":   ["cover"],
    "problem_analysis":    [],
    "solution":            ["problem_analysis"],
    "implementation_plan": ["solution"],
    "team":                [],
    "cost":                ["implementation_plan"],
}

SECTION_DISPLAY = {
    "cover": "표지",
    "executive_summary": "경영진 요약",
    "problem_analysis": "현황 및 문제점",
    "solution": "제안 솔루션",
    "implementation_plan": "추진 계획",
    "team": "수행 조직",
    "cost": "사업비",
}

SECTION_INSTRUCTIONS = {
    "cover": "제안서 표지를 작성하세요. 사업명, 제출 기관, 제안 기관 정보를 포함하세요.",
    "executive_summary": "경영진을 위한 요약을 작성하세요. 핵심 가치, 차별점, 기대 효과를 간결하게 정리하세요.",
    "problem_analysis": "현황 및 문제점을 분석하세요. 고객이 직면한 문제와 기존 방식의 한계를 서술하세요.",
    "solution": "제안 솔루션을 상세히 작성하세요. 기술적 접근 방식, 핵심 기능, 차별화 요소를 포함하세요.",
    "implementation_plan": "추진 계획을 작성하세요. 단계별 일정, WBS, 주요 마일스톤을 포함하세요.",
    "team": "수행 조직을 소개하세요. 조직 구성, 역할 분담, 주요 인력의 역량을 서술하세요.",
    "cost": "사업비 내역을 작성하세요. 항목별 비용, 산정 근거, 지불 조건을 포함하세요.",
}


@dataclass
class GeneratedSection:
    section_name: str
    content: str
    rag_sources: list = field(default_factory=list)
    validated: bool = False


def _build_waves(sections: list[str]) -> list[list[str]]:
    section_set = set(sections)
    completed: set[str] = set()
    remaining = list(sections)
    waves: list[list[str]] = []

    while remaining:
        wave = [
            s for s in remaining
            if all(dep in completed or dep not in section_set for dep in SECTION_DEPS.get(s, []))
        ]
        if not wave:
            # 순환 의존 방어: 남은 섹션 전부를 단일 wave로 처리
            logger.warning("순환 의존 감지 — 잔여 섹션 단일 wave 처리: %s", remaining)
            waves.append(list(remaining))
            break
        waves.append(wave)
        completed.update(wave)
        remaining = [s for s in remaining if s not in completed]

    return waves


def _fallback_content(section_name: str, rfp_analysis: RFPAnalysis, project_name: str) -> str:
    display = SECTION_DISPLAY.get(section_name, section_name)
    summary = rfp_analysis.project_summary[:200] if rfp_analysis.project_summary else project_name
    return f"## {display}\n\n{summary}...\n\n(자동 생성 실패 — 수동 작성이 필요합니다.)"


def _build_prompt(
    section_name: str,
    rfp_text: str,
    rag_context: str,
    rfp_analysis: RFPAnalysis,
    project_name: str,
) -> str:
    display = SECTION_DISPLAY.get(section_name, section_name)
    instruction = SECTION_INSTRUCTIONS.get(section_name, f"{display} 섹션을 작성하세요.")
    rfp_context = rfp_analysis.to_context_string()

    base = (
        f"당신은 제안서 작성 전문가입니다. 다음 정보를 바탕으로 '{project_name}' 사업의 "
        f"제안서 중 '{display}' 섹션을 한국어로 작성하세요.\n\n"
        f"[지시사항]\n{instruction}\n\n"
        f"[RFP 분석]\n{rfp_context}\n\n"
        f"[참고 제안서 내용]\n{{rag_context}}\n\n"
        f"[RFP 원문 (요약)]\n{rfp_text[:500]}\n\n"
        f"[{display} 섹션 작성 시작]"
    )

    # 프롬프트 총 길이 4000자 초과 시 rag_context 잘라내기
    max_len = 4000
    rag_placeholder = "{rag_context}"
    overhead = len(base) - len(rag_placeholder) + len(rag_context)
    if overhead > max_len:
        allowed = max(0, max_len - (len(base) - len(rag_placeholder)))
        rag_context = rag_context[:allowed]

    return base.replace("{rag_context}", rag_context)


class SectionGenerator:
    def __init__(self, rag_engine, llm):
        self._rag = rag_engine
        self._llm = llm

    def generate_all(
        self,
        rfp_analysis: RFPAnalysis,
        rfp_text: str,
        project_name: str,
        sections: list[str] | None = None,
    ) -> list[GeneratedSection]:
        sections = sections or DEFAULT_SECTIONS
        waves = _build_waves(sections)
        results: dict[str, GeneratedSection] = {}

        for wave in waves:
            for section_name in wave:
                logger.info("섹션 생성 중: %s", section_name)
                results[section_name] = self._generate_safe(
                    section_name, rfp_analysis, rfp_text, project_name
                )

        return [results[s] for s in sections if s in results]

    def _generate_safe(
        self,
        section_name: str,
        rfp_analysis: RFPAnalysis,
        rfp_text: str,
        project_name: str,
    ) -> GeneratedSection:
        for attempt in range(3):
            try:
                return self._generate(section_name, rfp_analysis, rfp_text, project_name)
            except Exception as e:
                logger.warning("섹션 생성 실패 (attempt %d/3): %s — %s", attempt + 1, section_name, e)
        return GeneratedSection(
            section_name=section_name,
            content=_fallback_content(section_name, rfp_analysis, project_name),
            rag_sources=[],
            validated=False,
        )

    def _generate(
        self,
        section_name: str,
        rfp_analysis: RFPAnalysis,
        rfp_text: str,
        project_name: str,
    ) -> GeneratedSection:
        rag_query = f"{section_name} {rfp_analysis.to_query_string()}"[:600]
        try:
            rag_result = self._rag.query(rag_query)
            rag_context = rag_result.get("answer", "")
            rag_sources = rag_result.get("sources", [])
        except Exception as e:
            logger.warning("RAG 검색 실패 (무시): %s", e)
            rag_context = "(RAG 검색 결과 없음)"
            rag_sources = []

        prompt = _build_prompt(section_name, rfp_text, rag_context, rfp_analysis, project_name)
        params = SECTION_PARAMS.get(section_name, {})
        content = self._llm.predict(
            prompt,
            temperature=params.get("temperature"),
            max_tokens=params.get("max_tokens"),
        )
        return GeneratedSection(
            section_name=section_name,
            content=content,
            rag_sources=rag_sources,
            validated=True,
        )
