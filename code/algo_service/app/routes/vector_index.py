from __future__ import annotations

import json

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.response import success
from app.services.spring_client import spring_client
from app.services.vector_store import CaseRecord, vector_store

router = APIRouter()


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=20)


def _to_case_record(payload: dict) -> CaseRecord:
    extra_data = payload.get("extraData")
    if isinstance(extra_data, str):
        try:
            extra_data = json.loads(extra_data)
        except Exception:
            extra_data = {"raw": extra_data}
    if not isinstance(extra_data, (dict, list)):
        extra_data = None
    return CaseRecord(
        id=int(payload.get("id", 0) or 0),
        title=payload.get("title") or "未命名病例",
        description=payload.get("description") or "",
        categoryName=payload.get("categoryName") or "未分类",
        categoryId=payload.get("categoryId"),
        tags=payload.get("tags"),
        extraData=extra_data if isinstance(extra_data, dict) else None,
        coverBucket=payload.get("coverBucket"),
        coverObjectKey=payload.get("coverObjectKey"),
        fileBucket=payload.get("fileBucket"),
        fileObjectKey=payload.get("fileObjectKey"),
        userId=payload.get("userId"),
        userName=payload.get("userName"),
        createTime=payload.get("createTime"),
        updateTime=payload.get("updateTime"),
    )


@router.get("/status")
async def status():
    stats = vector_store.stats()
    return success(stats)


@router.post("/create")
async def create_index():
    items = await spring_client.fetch_items()
    if not items:
        return success(msg="后端无病例数据，无法生成索引")
    cases = [_to_case_record(item) for item in items]
    vector_store.save(cases)
    return success(msg=f"索引已生成，共 {len(cases)} 条病例")


@router.delete("/delete")
async def delete_index():
    vector_store.delete()
    return success(msg="索引已删除")


@router.post("/search")
async def search(request: SearchRequest):
    if not vector_store.exists():
        return success([])
    results = vector_store.search(request.query, top_k=request.top_k)
    return success([case.as_dict() for case in results])
