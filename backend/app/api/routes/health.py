"""
MoneyFollows - Health Check Route
"""

from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    services = {}
    
    # Check LLM configuration
    api_key = settings.get_llm_api_key()
    services["llm"] = "configured" if api_key else "not_configured"
    services["llm_provider"] = settings.llm_provider
    services["llm_model"] = settings.llm_model
    
    # Check search configuration
    search_key = settings.get_search_api_key()
    services["search"] = "configured" if search_key else "not_configured"
    services["search_provider"] = settings.search_provider
    
    all_configured = all(
        v != "not_configured" for k, v in services.items()
        if k in ("llm", "search")
    )
    
    return {
        "status": "healthy" if all_configured else "degraded",
        "version": settings.app_version,
        "environment": settings.app_env,
        "services": services,
    }
