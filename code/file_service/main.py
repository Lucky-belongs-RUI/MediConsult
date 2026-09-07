from __future__ import annotations

import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

SUCCESS_CODE = 200

STORAGE_ROOT = Path(os.getenv("FILE_STORAGE_ROOT", Path(__file__).resolve().parent / "file"))
STORAGE_ROOT.mkdir(parents=True, exist_ok=True)


app = FastAPI(title="Medical File Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _response(data=None, msg="success", code=SUCCESS_CODE):
    return {"code": code, "msg": msg, "data": data}


def _sanitize_bucket(bucket: str) -> str:
    if not re.match(r"^[a-zA-Z0-9_-]+$", bucket):
        raise HTTPException(status_code=400, detail="bucket 非法")
    return bucket


def _sanitize_object_key(key: str) -> str:
    if ".." in key or key.startswith("/"):
        raise HTTPException(status_code=400, detail="objectKey 非法")
    return key


def _build_object_key(filename: str) -> str:
    suffix = Path(filename).suffix
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex}{suffix}"


def _file_path(bucket: str, object_key: str) -> Path:
    bucket_dir = STORAGE_ROOT / bucket
    bucket_dir.mkdir(parents=True, exist_ok=True)
    return bucket_dir / object_key


def _file_url(request: Request, bucket: str, object_key: str) -> str:
    base = str(request.base_url).rstrip("/")
    return f"{base}/file/{bucket}/{object_key}"


@app.get("/api/health")
async def health_check():
    return _response({"status": "healthy", "service": "file-service"})


@app.post("/api/file/upload/{bucket}")
async def upload_file(bucket: str, request: Request, file: UploadFile = File(...), is_cache: Optional[str] = Form(None)):
    bucket = _sanitize_bucket(bucket)
    object_key = _build_object_key(file.filename or "upload.bin")
    file_path = _file_path(bucket, object_key)
    with file_path.open("wb") as fh:
        while chunk := file.file.read(1024 * 1024):
            fh.write(chunk)
    url = _file_url(request, bucket, object_key)
    payload = {"url": url, "bucket": bucket, "objectKey": object_key}
    return _response(payload)


@app.get("/api/file/{bucket}/{object_key:path}")
async def download_file(bucket: str, object_key: str):
    bucket = _sanitize_bucket(bucket)
    object_key = _sanitize_object_key(object_key)
    file_path = _file_path(bucket, object_key)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    media_type = "application/octet-stream"
    return FileResponse(file_path, filename=file_path.name, media_type=media_type)


@app.delete("/api/file/{bucket}/{object_key:path}")
async def delete_file(bucket: str, object_key: str):
    bucket = _sanitize_bucket(bucket)
    object_key = _sanitize_object_key(object_key)
    file_path = _file_path(bucket, object_key)
    if file_path.exists():
        file_path.unlink()
        return _response(msg="文件已删除")
    return _response(msg="文件不存在", data={"deleted": False})


@app.get("/api/")
async def root():
    return _response({"service": "file-service", "upload": "/file/upload/{bucket}"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
