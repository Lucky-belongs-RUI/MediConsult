from fastapi import APIRouter

from . import document, health, llm, vector_index, knowledge_graph

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(llm.router, prefix="/llm", tags=["llm"])
router.include_router(vector_index.router, prefix="/vector-index", tags=["vector-index"])
router.include_router(document.router, prefix="/document", tags=["document"])
router.include_router(knowledge_graph.router, prefix="/knowledge-graph", tags=["knowledge-graph"])
