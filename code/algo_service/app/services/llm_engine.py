from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

from app.config import settings
from app.services.aliyun_client import AliyunLLMClientError, aliyun_client
from app.services.vector_store import CaseRecord, vector_store
from app.services.knowledge_graph import knowledge_graph_store
from app.services.knowledge_graph.models import KnowledgeTriple


logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    response: str
    relevant_cases: List[Dict]
    relevant_knowledge: List[Dict]
    used_rag: bool
    used_knowledge_graph: bool
    rewritten_query: Optional[str]


class LLMEngine:
    def __init__(self) -> None:
            aliyun_defaults = [
                {"key": "qwen-plus", "name": "通义千问 Plus"},
                {"key": "qwen-turbo", "name": "通义千问 Turbo"},
                {"key": "qwen-max", "name": "通义千问 Max"},
            ]
            self.available_models = [
                {"key": settings.aliyun_model, "name": f"默认模型（{settings.aliyun_model}）"},
                *[model for model in aliyun_defaults if model["key"] != settings.aliyun_model],
            ]

    def list_models(self) -> List[Dict[str, str]]:
        return self.available_models

    def _augment_messages_with_context(
        self,
        messages: List[Dict[str, str]],
        rag_cases: List[CaseRecord],
        knowledge_triples: List[KnowledgeTriple],
        image_info: Optional[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        context_parts: List[str] = []

        if rag_cases:
            case_lines = "\n".join(
                f"- {case.title}（{case.categoryName}）：{(case.description or '')[:120]}..."
                for case in rag_cases
                if case.description
            )
            if case_lines:
                context_parts.append(
                    "以下为与用户问诊最相似的病例摘要，可在回答中参考：\n" + case_lines
                )
        
        if knowledge_triples:
            knowledge_lines = "\n".join(
                f"- {t.subject} {t.predicate} {t.object}"
                for t in knowledge_triples
            )
            if knowledge_lines:
                context_parts.append(
                    "以下为医学知识图谱中的相关知识：\n" + knowledge_lines
                )
        
        if image_info:
            context_parts.append(
                f"用户上传的影像资料存储在 Bucket={image_info.get('bucket')}、ObjectKey={image_info.get('objectKey')}，可结合描述进行初步分析。"
            )
        
        if not context_parts:
            return messages
        
        system_prompt = "请基于提供的信息，以专业且易懂的语言给出医学建议：\n\n" + "\n\n".join(context_parts)
        return [{"role": "system", "content": system_prompt}, *messages]

    def _resolve_model(self, requested_model: Optional[str]) -> str:
        return requested_model or settings.aliyun_model

    def generate(self, model: str, messages: List[Dict[str, str]],
                 enable_rag: bool, enable_knowledge_graph: bool = False,
                 image_info: Optional[Dict[str, str]] = None) -> LLMResponse:
        user_question = next((msg["content"] for msg in reversed(messages) if msg.get("role") == "user"), "")
        
        rag_cases: List[CaseRecord] = []
        if enable_rag and user_question:
            rag_cases = vector_store.search(user_question, top_k=3)
        
        knowledge_triples: List[KnowledgeTriple] = []
        if enable_knowledge_graph and user_question:
            knowledge_triples = knowledge_graph_store.search(user_question, top_k=5)
        
        rewritten_query = None
        if enable_rag and user_question:
            rewritten_query = f"面向病例检索的医学问句：{user_question.strip()}"
        
        if aliyun_client.is_configured():
            augmented_messages = self._augment_messages_with_context(
                messages, rag_cases, knowledge_triples, image_info
            )
            try:
                content, _usage = aliyun_client.chat(
                    messages=augmented_messages,
                    model=self._resolve_model(model),
                )
                return LLMResponse(
                    response=content,
                    relevant_cases=[case.as_dict() for case in rag_cases],
                    relevant_knowledge=[t.as_dict() for t in knowledge_triples],
                    used_rag=enable_rag and bool(rag_cases),
                    used_knowledge_graph=enable_knowledge_graph and bool(knowledge_triples),
                    rewritten_query=rewritten_query,
                )
            except AliyunLLMClientError as exc:
                logger.error("Aliyun LLM call failed: %s", exc)
                raise

        raise RuntimeError("LLM service is not configured. Please set ALIYUN_API_KEY.")


llm_engine = LLMEngine()
