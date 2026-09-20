"""
MoneyFollows - FastAPI Application
AI-Powered Government Scheme Discovery & Eligibility Assistant
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import health, search

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info(f"Starting MoneyFollows v{settings.app_version}")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"LLM Provider: {settings.llm_provider} / {settings.llm_model}")
    logger.info(f"Search Provider: {settings.search_provider}")
    
    # Validate configuration
    if not settings.get_llm_api_key():
        logger.warning("⚠️  LLM API key not configured. AI features will not work.")
    if settings.search_provider.lower() not in ["duckduckgo", "local"] and not settings.get_search_api_key():
        logger.warning("⚠️  Search API key not configured. Web search will not work.")
    
    yield
    logger.info("Shutting down MoneyFollows")


app = FastAPI(
    title="MoneyFollows API",
    description="AI-Powered Government Scheme Discovery & Eligibility Assistant",
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(search.router, prefix="/api", tags=["Search & Chat"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MoneyFollows API",
        "version": settings.app_version,
        "docs": "/docs",
    }
