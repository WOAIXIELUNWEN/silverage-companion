from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.retrieval import search, format_context

router = APIRouter(prefix="/api/health", tags=["health"])


class HealthQuery(BaseModel):
    query: str


@router.post("/search")
def health_search(req: HealthQuery):
    results = search(req.query, top_k=5)
    return {
        "query": req.query,
        "results": results,
        "count": len(results),
    }
