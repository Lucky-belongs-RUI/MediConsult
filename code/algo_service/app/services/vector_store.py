from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from app.config import settings


TOKEN_PATTERN = re.compile(r"[\w']+")


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text or "")]


@dataclass
class CaseRecord:
    id: int
    title: str
    description: str
    categoryName: str
    categoryId: int | None
    tags: str | None
    extraData: Dict | None
    coverBucket: str | None
    coverObjectKey: str | None
    fileBucket: str | None
    fileObjectKey: str | None
    userId: int | None
    userName: str | None
    createTime: str | None
    updateTime: str | None

    def as_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "categoryName": self.categoryName,
            "categoryId": self.categoryId,
            "tags": self.tags,
            "extraData": self.extraData,
            "coverBucket": self.coverBucket,
            "coverObjectKey": self.coverObjectKey,
            "fileBucket": self.fileBucket,
            "fileObjectKey": self.fileObjectKey,
            "userId": self.userId,
            "userName": self.userName,
            "createTime": self.createTime,
            "updateTime": self.updateTime,
        }


class VectorStore:
    def __init__(self, storage_file: Path | None = None) -> None:
        self.storage_file = (storage_file or settings.vector_index_file)
        self._cases: List[CaseRecord] = []

    def exists(self) -> bool:
        return self.storage_file.exists()

    def save(self, cases: List[CaseRecord]) -> None:
        self._cases = cases
        payload = {"cases": [case.as_dict() for case in cases]}
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.storage_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def delete(self) -> None:
        if self.storage_file.exists():
            self.storage_file.unlink()
        self._cases = []

    def load(self) -> List[CaseRecord]:
        if self._cases:
            return self._cases
        if not self.storage_file.exists():
            return []
        try:
            payload = json.loads(self.storage_file.read_text(encoding="utf-8"))
            cases = payload.get("cases", [])
            self._cases = [CaseRecord(**case) for case in cases]
            return self._cases
        except (json.JSONDecodeError, OSError, KeyError) as exc:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Failed to load vector index from %s: %s", self.storage_file, exc)
            return []

    def stats(self) -> Dict[str, int]:
        cases = self.load()
        total_chars = sum(len(case.description or "") + len(case.title or "") for case in cases)
        return {"exists": bool(cases), "count": len(cases), "size": total_chars}

    def search(self, query: str, top_k: int = 5) -> List[CaseRecord]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        cases = self.load()
        scored: List[Tuple[float, CaseRecord]] = []
        query_freq = Counter(query_tokens)
        for case in cases:
            text_tokens = tokenize(" ".join([
                case.title or "",
                case.description or "",
                case.tags or "",
            ]))
            if not text_tokens:
                continue
            doc_freq = Counter(text_tokens)
            numerator = sum(query_freq[token] * doc_freq.get(token, 0) for token in query_freq)
            denominator = math.sqrt(sum(v * v for v in query_freq.values())) * math.sqrt(sum(v * v for v in doc_freq.values()))
            score = numerator / denominator if denominator else 0.0
            if score > 0:
                scored.append((score, case))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [case for _, case in scored[:top_k]]


vector_store = VectorStore()
