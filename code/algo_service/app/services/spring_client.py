from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from app.config import settings


class SpringClient:

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = (base_url or settings.springboot_api_base).rstrip("/")

    async def _request(self, method: str, path: str, **kwargs: Any) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                payload = response.json()
                if isinstance(payload, dict) and payload.get("code") == 200:
                    return payload.get("data")
                return None
        except httpx.HTTPError as exc:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Spring Boot API request failed: %s %s — %s", method, url, exc)
            return None
        except Exception as exc:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Unexpected error calling Spring Boot API: %s %s — %s", method, url, exc)
            return None

    async def fetch_items(self) -> List[Dict[str, Any]]:
        data = await self._request("GET", "/item/list")
        if isinstance(data, list):
            return data
        return []

    async def fetch_case(self, item_id: int) -> Optional[Dict[str, Any]]:
        data = await self._request("GET", f"/item/{item_id}")
        if isinstance(data, dict):
            return data
        return None

    async def fetch_chat_session(self, session_id: int) -> Optional[Dict[str, Any]]:
        data = await self._request("GET", f"/chat/sessions/{session_id}")
        if isinstance(data, dict):
            return data
        return None

    async def fetch_chat_messages(self, session_id: int) -> List[Dict[str, Any]]:
        data = await self._request("GET", f"/chat/messages?sessionId={session_id}")
        if isinstance(data, list):
            return data
        return []


spring_client = SpringClient()
