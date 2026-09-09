from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.config import settings
from app.services.aliyun_client import AliyunLLMClientError, aliyun_client
from app.services.vector_store import CaseRecord, vector_store
from app.services.knowledge_graph import knowledge_graph_store
from app.services.knowledge_graph.models import KnowledgeTriple


logger = logging.getLogger(__name__)


CASE_FORMAT_SYSTEM_PROMPT = """你是医学病例结构化助手。请根据患者信息和问诊记录，整理出符合病例库数据表格式的 JSON 数据。

JSON 字段要求：
1. title：简洁病例标题，包含年龄段、性别与主要问题（如"56岁男性高血压复诊"），不超过30字
2. description：病例概述，完整概括主诉、病情经过、关键症状表现以及 AI 给出的诊疗建议，200-300字
3. basic_info：患者基本信息，整理为姓名、年龄、性别、问诊科室、特殊情况备注等
4. clinical：临床表现，详细列出症状、体征、持续时间、诱因、加重缓解因素等（依据问诊记录中的患者描述）
5. diagnosis：诊断结果，给出初步诊断或疾病判断，必要时包含鉴别诊断分析
6. treatment：治疗方案，给出治疗原则、用药建议（含剂量与用法）、生活方式干预等具体可执行建议
7. follow_up：注意事项与随访，列出需警惕的危险信号、复查周期、随访计划与生活注意事项
8. tags：症状标签，3-5个中文关键词，用英文逗号分隔
9. category_id：从给定的科室列表中选择最匹配的科室ID；无法判断时填 null

要求：所有文字性字段内容必须充实、完整、专业，能直接填充病例详情表格（病例概述、患者基本信息、临床表现、诊断结果、治疗方案、注意事项与随访），禁止空字段或简略占位；内容仅基于给定信息整理，不得编造问诊中未出现的信息。

只输出一个 JSON 对象，不要输出任何其他文字、解释或代码块标记。
JSON 格式示例：{"title":"56岁男性高血压复诊","description":"患者高血压病史5年，近期晨起血压偏高，伴头晕心悸，AI建议连续监测血压并调整生活方式。","basic_info":"姓名：王建国；年龄：56岁；性别：男；问诊科室：心内科；特殊情况备注：高血压病史5年","clinical":"晨起血压145/95mmHg左右，伴头晕、心悸，活动后加重","diagnosis":"初步诊断：原发性高血压2级（高危），需排除继发性高血压","treatment":"1.药物治疗：建议在医生指导下使用降压药，不可自行调量；2.生活方式：低盐低脂饮食，每日食盐不超过5克，戒烟限酒，规律作息","follow_up":"1.连续监测血压一周并记录；2.若持续高于140/90或出现胸痛、视物模糊等请及时就医；3.每月复查血压，每3-6个月复查肝肾功能","tags":"高血压,头晕,心悸","category_id":1}"""


def _extract_json(text: str) -> Dict[str, Any]:
    """从模型输出中容错提取 JSON（支持剥离 markdown 代码块与前后杂文）"""
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"模型输出无法解析为 JSON: {text[:200]}")


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
        glm_defaults = [
            {"key": "glm-4-flash", "name": "智谱 GLM-4-Flash（免费）"},
            {"key": "glm-4-plus", "name": "智谱 GLM-4-Plus"},
            {"key": "glm-4-air", "name": "智谱 GLM-4-Air"},
        ]
        self.available_models = [
            {"key": settings.aliyun_model, "name": f"默认模型（{settings.aliyun_model}）"},
            *[model for model in glm_defaults if model["key"] != settings.aliyun_model],
        ]

    def list_models(self) -> List[Dict[str, str]]:
        return self.available_models

    def format_case(self, model: str, messages: List[Dict[str, str]],
                    consult_info: Optional[Dict] = None,
                    categories: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """将问诊记录与病例库格式要求组装成 prompt，让模型输出规定的 JSON 病例数据"""
        if not messages:
            raise ValueError("问诊记录不能为空")

        info_lines: List[str] = []
        if consult_info:
            if consult_info.get("consultName"):
                info_lines.append(f"问诊主题：{consult_info.get('consultName')}")
            if consult_info.get("patientName"):
                info_lines.append(f"患者姓名：{consult_info.get('patientName')}")
            if consult_info.get("age") is not None:
                info_lines.append(f"年龄：{consult_info.get('age')}")
            if consult_info.get("gender"):
                info_lines.append(f"性别：{consult_info.get('gender')}")
            if consult_info.get("categoryName"):
                info_lines.append(f"问诊科室：{consult_info.get('categoryName')}")
            if consult_info.get("remark"):
                info_lines.append(f"特殊情况备注：{consult_info.get('remark')}")

        transcript_lines = [
            f"{'患者' if msg.get('role') == 'user' else 'AI医生'}：{msg.get('content', '')}"
            for msg in messages
        ]

        user_prompt_parts = []
        if info_lines:
            user_prompt_parts.append("【患者信息】\n" + "\n".join(info_lines))
        if categories:
            category_lines = "\n".join(
                f"- {cat.get('id')}: {cat.get('name')}" for cat in categories
            )
            user_prompt_parts.append("【可选科室列表】\n" + category_lines)
        user_prompt_parts.append("【问诊记录】\n" + "\n".join(transcript_lines))
        user_prompt = "\n\n".join(user_prompt_parts)

        if not aliyun_client.is_configured():
            raise RuntimeError("LLM service is not configured. Please set ALIYUN_API_KEY.")

        try:
            content, _usage = aliyun_client.chat(
                messages=[
                    {"role": "system", "content": CASE_FORMAT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                model=self._resolve_model(model),
            )
        except AliyunLLMClientError as exc:
            logger.error("Aliyun LLM format_case failed: %s", exc)
            raise RuntimeError("病例结构化生成失败，请稍后重试") from exc

        try:
            data = _extract_json(content)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.error("format_case JSON parse failed: %s", exc)
            raise RuntimeError("模型输出格式异常，未能解析出规定 JSON，请重试") from exc

        def _text(key: str) -> str:
            value = data.get(key)
            return str(value).strip() if value is not None else ""

        return {
            "title": _text("title"),
            "description": _text("description"),
            "basic_info": _text("basic_info"),
            "clinical": _text("clinical"),
            "diagnosis": _text("diagnosis"),
            "treatment": _text("treatment"),
            "follow_up": _text("follow_up"),
            "tags": _text("tags"),
            "category_id": data.get("category_id"),
            "raw": content,
        }

    def _augment_messages_with_context(
        self,
        messages: List[Dict[str, str]],
        rag_cases: List[CaseRecord],
        knowledge_triples: List[KnowledgeTriple],
        image_info: Optional[Dict[str, str]],
        consult_info: Optional[Dict] = None,
    ) -> List[Dict[str, str]]:
        context_parts: List[str] = []

        if consult_info:
            patient_lines = []
            if consult_info.get("patientName"):
                patient_lines.append(f"患者姓名：{consult_info.get('patientName')}")
            if consult_info.get("age") is not None:
                patient_lines.append(f"年龄：{consult_info.get('age')}")
            if consult_info.get("gender"):
                patient_lines.append(f"性别：{consult_info.get('gender')}")
            if consult_info.get("categoryName"):
                patient_lines.append(f"问诊科室：{consult_info.get('categoryName')}")
            if consult_info.get("consultName"):
                patient_lines.append(f"问诊主题：{consult_info.get('consultName')}")
            if consult_info.get("remark"):
                patient_lines.append(f"特殊情况备注：{consult_info.get('remark')}")
            if patient_lines:
                context_parts.append(
                    "以下是本次问诊的患者基础信息，请结合这些信息给出更贴合患者情况的建议：\n"
                    + "\n".join(f"- {line}" for line in patient_lines)
                )

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
                 image_info: Optional[Dict[str, str]] = None,
                 consult_info: Optional[Dict] = None) -> LLMResponse:
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
                messages, rag_cases, knowledge_triples, image_info, consult_info
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
