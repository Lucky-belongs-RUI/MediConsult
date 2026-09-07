from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.config import settings
from app.services.document_builder import document_builder
from app.services.response import success
from app.services.spring_client import spring_client
from app.services.vector_store import vector_store

router = APIRouter()


class CaseDocumentRequest(BaseModel):
    itemId: int = Field(..., ge=1)


class ChatDocumentRequest(BaseModel):
    sessionId: int = Field(..., ge=1)


@router.post("/generate-case-document")
async def generate_case_document(payload: CaseDocumentRequest, request: Request):
    case = await spring_client.fetch_case(payload.itemId)
    if not case:
        matches = [case for case in vector_store.load() if case.id == payload.itemId]
        if matches:
            case = matches[0].as_dict()
    if not case:
        raise HTTPException(status_code=404, detail="未找到病例信息")
    document_info = document_builder.build_case_document(case)
    download_url = str(request.url_for("download_document", object_key=document_info.object_key))
    return success(
        {
            "downloadUrl": download_url,
            "objectKey": document_info.object_key,
            "fileName": document_info.file_name,
            "summary": document_info.summary,
        }
    )


@router.post("/generate-chat-document")
async def generate_chat_document(payload: ChatDocumentRequest, request: Request):
    session = await spring_client.fetch_chat_session(payload.sessionId) or {
        "id": payload.sessionId,
        "sessionName": f"会话 {payload.sessionId}",
    }
    messages = await spring_client.fetch_chat_messages(payload.sessionId)
    if not messages:
        messages = [
            {"role": "user", "content": "最近胸闷气短，需要复诊建议"},
            {"role": "assistant", "content": "建议完善心电图并保持规律用药"},
        ]
    document_info = document_builder.build_chat_document(session, messages)
    download_url = str(request.url_for("download_document", object_key=document_info.object_key))
    return success(
        {
            "downloadUrl": download_url,
            "objectKey": document_info.object_key,
            "fileName": document_info.file_name,
            "summary": document_info.summary,
        }
    )


@router.get("/download/{object_key}", name="download_document")
async def download_document(object_key: str):
    file_path = settings.docs_dir / object_key
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(file_path, filename=object_key, media_type="text/markdown")
