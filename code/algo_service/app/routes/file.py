"""文件路由（由原 file_service 合并而来）。

接口路径、参数、返回结构与原独立文件服务保持一致：
- POST   /api/file/upload/{bucket}         上传文件（multipart/form-data）
- GET    /api/file/{bucket}/{objectKey}    下载文件
- DELETE /api/file/{bucket}/{objectKey}    删除文件
- GET    /api/file/health                  健康检查
"""
from __future__ import annotations

import mimetypes
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from app.config import settings
from app.services.response import success

router = APIRouter()


def _sanitize_bucket(bucket: str) -> str:
    if not re.match(r"^[a-zA-Z0-9_-]+$", bucket):
        raise HTTPException(status_code=400, detail="bucket 非法")
    return bucket


def _sanitize_object_key(key: str) -> str:
    if ".." in key or key.startswith("/") or "\\" in key:
        raise HTTPException(status_code=400, detail="objectKey 非法")
    return key


def _build_object_key(filename: str) -> str:
    suffix = Path(filename).suffix
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex}{suffix}"


def _file_path(bucket: str, object_key: str) -> Path:
    bucket_dir = settings.file_storage_root / bucket
    bucket_dir.mkdir(parents=True, exist_ok=True)
    return bucket_dir / object_key


def _file_url(request: Request, bucket: str, object_key: str) -> str:
    base = str(request.base_url).rstrip("/")
    return f"{base}/api/file/{bucket}/{object_key}"


@router.get("/health")
async def health_check():
    return success({"status": "healthy", "service": "algo-service/files"})


@router.post("/upload/{bucket}")
async def upload_file(
    bucket: str,
    request: Request,
    file: UploadFile = File(...),
    is_cache: Optional[str] = Form(None),
):
    bucket = _sanitize_bucket(bucket)
    object_key = _build_object_key(file.filename or "upload.bin")
    file_path = _file_path(bucket, object_key)
    with file_path.open("wb") as fh:
        while chunk := file.file.read(1024 * 1024):
            fh.write(chunk)
    url = _file_url(request, bucket, object_key)
    payload = {"url": url, "bucket": bucket, "objectKey": object_key}
    return success(payload)


@router.get("/{bucket}/{object_key:path}")
async def download_file(bucket: str, object_key: str):
    bucket = _sanitize_bucket(bucket)
    object_key = _sanitize_object_key(object_key)
    file_path = _file_path(bucket, object_key)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    media_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    return FileResponse(file_path, filename=file_path.name, media_type=media_type)


@router.delete("/{bucket}/{object_key:path}")
async def delete_file(bucket: str, object_key: str):
    bucket = _sanitize_bucket(bucket)
    object_key = _sanitize_object_key(object_key)
    file_path = _file_path(bucket, object_key)
    if file_path.exists():
        file_path.unlink()
        return success(msg="文件已删除")
    return success(msg="文件不存在", data={"deleted": False})
