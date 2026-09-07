from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class KnowledgeTriple:
    subject: str
    predicate: str
    object: str
    source: str
    category: str
    
    def as_dict(self) -> Dict:
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "source": self.source,
            "category": self.category
        }
    
    def as_text(self) -> str:
        return f"{self.subject} {self.predicate} {self.object}"


@dataclass
class KnowledgeGraphRecord:
    disease_name: str
    disease_info: Dict
    triples: List[KnowledgeTriple] = field(default_factory=list)
    
    def as_dict(self) -> Dict:
        return {
            "disease_name": self.disease_name,
            "disease_info": self.disease_info,
            "triples": [t.as_dict() for t in self.triples]
        }
