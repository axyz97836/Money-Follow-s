"""
MoneyFollows - Search Result Model
"""

from typing import Optional, List
from pydantic import BaseModel


class SearchResult(BaseModel):
    """Individual search result from a search provider."""
    title: str
    url: str
    snippet: str = ""
    domain: str = ""
    content: Optional[str] = None
    score: float = 0.0
    source_type: str = "general"


class SearchResponse(BaseModel):
    """Collection of search results."""
    query: str
    results: List[SearchResult] = []
    total_results: int = 0
    provider: str = ""
    error: Optional[str] = None
