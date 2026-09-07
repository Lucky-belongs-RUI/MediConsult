from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from app.config import settings
from app.services.knowledge_graph.models import KnowledgeTriple, KnowledgeGraphRecord


TOKEN_PATTERN = re.compile(r"[\w']+")


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text or "")]


@dataclass
class KnowledgeGraphStore:

    def __init__(self, storage_file: Optional[Path] = None) -> None:
        self.storage_file = storage_file or (settings.data_dir / "knowledge_graph.json")
        self._records: List[KnowledgeGraphRecord] = []
    
    @property
    def data_dir(self) -> Path:
        return settings.data_dir
    
    def exists(self) -> bool:
        return self.storage_file.exists()
    
    def save(self, records: List[KnowledgeGraphRecord]) -> None:
        self._records = records
        payload = {
            "count": len(records),
            "total_triples": sum(len(r.triples) for r in records),
            "records": [r.as_dict() for r in records]
        }
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.storage_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    
    def delete(self) -> None:
        if self.storage_file.exists():
            self.storage_file.unlink()
        self._records = []
    
    def load(self) -> List[KnowledgeGraphRecord]:
        if self._records:
            return self._records
        if not self.storage_file.exists():
            return []

        try:
            payload = json.loads(self.storage_file.read_text(encoding="utf-8"))
            records_data = payload.get("records", [])

            records = []
            for rd in records_data:
                triples = [
                    KnowledgeTriple(**t) for t in rd.get("triples", [])
                ]
                record = KnowledgeGraphRecord(
                    disease_name=rd.get("disease_name", ""),
                    disease_info=rd.get("disease_info", {}),
                    triples=triples
                )
                records.append(record)

            self._records = records
            return records
        except (json.JSONDecodeError, OSError, KeyError) as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Failed to load knowledge graph from %s: %s", self.storage_file, e)
            return []
    
    def stats(self) -> Dict[str, int]:
        records = self.load()
        total_triples = sum(len(r.triples) for r in records)
        return {
            "exists": len(records) > 0,
            "disease_count": len(records),
            "triple_count": total_triples
        }
    
    def search(self, query: str, top_k: int = 5) -> List[KnowledgeTriple]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        
        records = self.load()
        if not records:
            return []
        
        scored: List[Tuple[float, KnowledgeTriple]] = []
        query_freq = Counter(query_tokens)
        
        for record in records:
            for triple in record.triples:
                triple_text = " ".join([
                    triple.subject,
                    triple.predicate,
                    triple.object
                ])
                text_tokens = tokenize(triple_text)
                
                if not text_tokens:
                    continue
                
                doc_freq = Counter(text_tokens)
                numerator = sum(
                    query_freq.get(token, 0) * doc_freq.get(token, 0) 
                    for token in query_freq
                )
                query_norm = math.sqrt(sum(v * v for v in query_freq.values()))
                doc_norm = math.sqrt(sum(v * v for v in doc_freq.values()))
                score = numerator / (query_norm * doc_norm) if query_norm and doc_norm else 0.0
                
                if score > 0:
                    scored.append((score, triple))
        
        scored.sort(key=lambda item: item[0], reverse=True)
        return [triple for _, triple in scored[:top_k]]
    
    def search_by_category(self, query: str, category: str, top_k: int = 3) -> List[KnowledgeTriple]:
        all_results = self.search(query, top_k * 2)
        return [t for t in all_results if t.category == category][:top_k]
    
    def get_all_triples_text(self) -> List[str]:
        records = self.load()
        texts = []
        for record in records:
            for triple in record.triples:
                texts.append(triple.as_text())
        return texts


knowledge_graph_store = KnowledgeGraphStore()
