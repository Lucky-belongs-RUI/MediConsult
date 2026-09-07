from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import router as api_router


app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"] ,
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": f"{settings.app_name} is running",
        "health": "/health/health_check",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
