import logging

from langchain_community.llms import Ollama

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemma4:26b"
DEFAULT_BASE_URL = "http://localhost:11434"


class OllamaLLM:
    def __init__(self, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL):
        logger.info("OllamaLLM 초기화: model=%s, url=%s", model, base_url)
        # LangChain Ollama()는 생성자에서 네트워크 연결 없음 — 연결 오류는 predict()에서만 발생
        self._llm = Ollama(model=model, base_url=base_url)
        self.model = model
        self.base_url = base_url

    def predict(
        self,
        prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        if not prompt.strip():
            raise ValueError("prompt가 비어 있습니다")
        try:
            if temperature is not None or max_tokens is not None:
                kwargs: dict = {"model": self.model, "base_url": self.base_url}
                if temperature is not None:
                    kwargs["temperature"] = temperature
                if max_tokens is not None:
                    kwargs["num_predict"] = max_tokens  # Ollama 파라미터명
                response = Ollama(**kwargs).invoke(prompt)
            else:
                response = self._llm.invoke(prompt)
        except Exception as e:
            raise RuntimeError(
                f"Ollama 연결 실패: {self.base_url}. Ollama가 실행 중인지 확인하세요."
            ) from e
        # 빈 응답 무음 실패 방지 — AC-3 "answer는 비어있지 않음" 계약 보장
        if not response.strip():
            raise RuntimeError(f"LLM이 빈 응답을 반환했습니다: model={self.model}")
        logger.debug("LLM 응답 완료: model=%s, temp=%s, max_tokens=%s, 응답길이=%d",
                     self.model, temperature, max_tokens, len(response))
        return response
