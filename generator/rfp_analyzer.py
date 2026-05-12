import json
import logging
import re
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)

ANALYZE_PROMPT = """다음 RFP 문서를 분석하여 반드시 아래 JSON 형식으로만 응답하십시오. JSON 외 텍스트 없음.

{{
  "project_summary": "사업 핵심 요약 (2~3문장)",
  "requirements": ["요구사항1", "요구사항2"],
  "constraints": ["제약사항1"],
  "keywords": ["키워드1", "키워드2"],
  "industry": "산업 분야",
  "budget_hint": "예산 관련 언급 (없으면 빈 문자열)",
  "deadline_hint": "납기/일정 관련 언급 (없으면 빈 문자열)"
}}

[RFP 문서]
{rfp_text}"""


@dataclass
class RFPAnalysis:
    project_summary: str = ""
    requirements: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    industry: str = ""
    budget_hint: str = ""
    deadline_hint: str = ""

    def to_context_string(self) -> str:
        parts = []
        if self.project_summary:
            parts.append(f"사업 개요: {self.project_summary}")
        if self.requirements:
            req_lines = "\n".join(f"- {r}" for r in self.requirements)
            parts.append(f"핵심 요구사항:\n{req_lines}")
        if self.constraints:
            con_lines = "\n".join(f"- {c}" for c in self.constraints)
            parts.append(f"제약사항:\n{con_lines}")
        if self.budget_hint:
            parts.append(f"예산: {self.budget_hint}")
        if self.deadline_hint:
            parts.append(f"일정: {self.deadline_hint}")
        return "\n".join(parts)

    def to_query_string(self) -> str:
        tokens = filter(None, [
            self.project_summary[:200],
            " ".join(self.keywords[:10]),
            self.industry,
        ])
        return " ".join(tokens)[:500]


class RFPAnalyzer:
    def __init__(self, llm):
        self._llm = llm

    def analyze(self, rfp_text: str) -> RFPAnalysis:
        if not rfp_text or not rfp_text.strip():
            return RFPAnalysis(project_summary="")

        trimmed = rfp_text[:8000]
        prompt = ANALYZE_PROMPT.format(rfp_text=trimmed)

        try:
            raw = self._llm.predict(prompt)
            match = re.search(r'\{[\s\S]+\}', raw)
            if not match:
                raise ValueError("JSON 블록 없음")
            data = json.loads(match.group())
            return RFPAnalysis(
                project_summary=str(data.get("project_summary", "")),
                requirements=list(data.get("requirements", [])),
                constraints=list(data.get("constraints", [])),
                keywords=list(data.get("keywords", [])),
                industry=str(data.get("industry", "")),
                budget_hint=str(data.get("budget_hint", "")),
                deadline_hint=str(data.get("deadline_hint", "")),
            )
        except Exception as e:
            logger.warning("RFP 분석 실패 (fallback): %s", e)
            return RFPAnalysis(project_summary=rfp_text[:300])
