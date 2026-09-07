from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

import httpx

from app.config import settings


logger = logging.getLogger(__name__)


class AliyunLLMClientError(RuntimeError):
    pass


class AliyunLLMClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        default_model: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        self.api_key = api_key or settings.aliyun_api_key
        self.api_base = (api_base or settings.aliyun_api_base).rstrip("/")
        self.default_model = default_model or settings.aliyun_model
        self.timeout = timeout or settings.aliyun_timeout

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise AliyunLLMClientError("Aliyun API key is not configured.")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_base}{path}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, headers=self._headers(), json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as exc:
            logger.error("Aliyun LLM request failed: %s", exc)
            raise AliyunLLMClientError("Failed to call Aliyun LLM API.") from exc

    def chat(
        self,
        *,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.8,
        max_tokens: Optional[int] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        payload: Dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        data = self._post("/chat/completions", payload)
        choices = data.get("choices") or []
        if not choices:
            raise AliyunLLMClientError("Aliyun LLM returned empty choices.")
        content = choices[0].get("message", {}).get("content")
        if not content:
            raise AliyunLLMClientError("Aliyun LLM response does not contain content.")
        return content, data.get("usage", {})


aliyun_client = AliyunLLMClient()

