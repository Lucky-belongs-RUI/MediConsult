from __future__ import annotations

from typing import Dict, List, Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.llm_engine import llm_engine
from app.services.response import success

router = APIRouter()


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1)


class ImageInfo(BaseModel):
    bucket: str
    objectKey: str


class ConsultInfo(BaseModel):
    """问诊基础信息（新建问诊时填写，随每次提问作为 prompt 一部分）"""
    consultName: Optional[str] = None
    patientName: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    categoryName: Optional[str] = None
    remark: Optional[str] = None


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    enable_rag: bool = False
    enable_knowledge_graph: bool = False
    image_info: Optional[ImageInfo] = None
    consult_info: Optional[ConsultInfo] = None


class CaseFormatRequest(BaseModel):
    """记录病例：将问诊记录 + 病例库格式要求组装为 prompt，模型输出规定 JSON"""
    model: str
    messages: List[Message]
    consult_info: Optional[ConsultInfo] = None
    categories: Optional[List[Dict]] = None


@router.get("/models")
async def list_models():
    return success(llm_engine.list_models())


@router.post("/chat")
async def chat(payload: ChatRequest):
    if not payload.messages:
        raise HTTPException(status_code=400, detail="messages不能为空")
    try:
        result = llm_engine.generate(
            model=payload.model,
            messages=[msg.model_dump() for msg in payload.messages],
            enable_rag=payload.enable_rag,
            enable_knowledge_graph=payload.enable_knowledge_graph,
            image_info=payload.image_info.model_dump() if payload.image_info else None,
            consult_info=payload.consult_info.model_dump() if payload.consult_info else None,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return success(
        {
            "response": result.response,
            "relevant_cases": result.relevant_cases,
            "relevant_knowledge": result.relevant_knowledge,
            "used_rag": result.used_rag,
            "used_knowledge_graph": result.used_knowledge_graph,
            "rewritten_query": result.rewritten_query,
        }
    )


@router.post("/summarize-case")
async def summarize_case(payload: CaseFormatRequest):
    if not payload.messages:
        raise HTTPException(status_code=400, detail="messages不能为空")
    try:
        result = llm_engine.format_case(
            model=payload.model,
            messages=[msg.model_dump() for msg in payload.messages],
            consult_info=payload.consult_info.model_dump() if payload.consult_info else None,
            categories=payload.categories,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return success(result)
