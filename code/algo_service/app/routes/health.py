from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

from app.services.response import success

router = APIRouter()


@router.get("/health_check")
async def health_check():
    return success(
        {
            "status": "ok",
            "service": "algo-service",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )
