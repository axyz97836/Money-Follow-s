"""
MoneyFollows - API Request/Response Schemas
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class UserProfileSchema(BaseModel):
    age: Optional[int] = None
    state: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    disability: Optional[str] = None


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    profile: Optional[UserProfileSchema] = None
    session_id: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: str
    profile: Optional[UserProfileSchema] = None


class SearchMetadata(BaseModel):
    sources_checked: int = 0
    official_sources: int = 0
    search_queries: List[str] = []


class SearchResponse(BaseModel):
    query: str
    summary: str
    schemes: List[Dict[str, Any]] = []
    disclaimer: str = ""
    search_metadata: SearchMetadata = SearchMetadata()
    session_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    services: Dict[str, str] = {}
