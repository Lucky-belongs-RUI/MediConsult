import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.config import settings
from app.services.knowledge_graph import knowledge_graph_store
from app.services.response import success


logger = logging.getLogger(__name__)

router = APIRouter()


class BuildRequest(BaseModel):
    file_path: str


@router.get("/status")
async def status():
    stats = knowledge_graph_store.stats()
    return success(stats)


@router.get("/graph")
async def get_graph():
    """返回已构建知识图谱的图数据（节点+关系），供前端可视化展示"""
    return success(knowledge_graph_store.get_graph_data())


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    kg_data_dir = settings.BASE_DIR / "data" / "kg_uploaded"
    kg_data_dir.mkdir(parents=True, exist_ok=True)
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="仅支持Excel文件 (.xlsx, .xls)")
    
    file_path = kg_data_dir / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return success({
        "file_name": file.filename,
        "file_path": str(file_path),
        "relative_path": str(file_path.relative_to(settings.BASE_DIR))
    })


@router.post("/build")
async def build_knowledge_graph(payload: BuildRequest):
    from app.services.knowledge_graph.build import build_from_excel

    file_path = Path(payload.file_path)
    if not file_path.is_absolute():
        file_path = settings.BASE_DIR / file_path
        
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        result = build_from_excel(file_path)
        if result is None:
            raise HTTPException(status_code=500, detail="构建知识图谱失败：文件读取错误")
        triples, category = result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"执行构建时出错: {e}")
        raise HTTPException(status_code=500, detail="构建知识图谱失败")

    if not triples:
        raise HTTPException(status_code=400, detail="未从Excel中提取到任何三元组，请检查LLM API配置与文件内容")

    from app.services.knowledge_graph.models import KnowledgeGraphRecord

    record = KnowledgeGraphRecord(
        disease_name=category,
        disease_info={"source": str(file_path)},
        triples=triples
    )

    # 同类别覆盖更新、不同类别累积保存（支持多次构建多个知识类别）
    existing = knowledge_graph_store.load()
    kept = [r for r in existing if r.disease_name != category]
    kept.append(record)
    knowledge_graph_store.save(kept)

    return success({
        "category": category,
        "triple_count": len(triples),
        "message": "知识图谱构建成功"
    })


@router.delete("/delete")
async def delete_knowledge_graph():
    knowledge_graph_store.delete()
    return success(msg="知识图谱已删除")
