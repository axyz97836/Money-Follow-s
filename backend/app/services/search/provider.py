"""
MoneyFollows - Search Provider Abstraction
Pluggable search providers for web search functionality.
"""

import httpx
import logging
import asyncio
import json
import os
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse
from duckduckgo_search import DDGS

from app.models.search_result import SearchResult, SearchResponse
from app.config import settings

logger = logging.getLogger(__name__)

# Official government domain patterns for India
OFFICIAL_DOMAINS = [
    ".gov.in", ".nic.in", ".india.gov.in",
    "myscheme.gov.in", "scholarship.gov.in",
    "pmjay.gov.in", "pmkisan.gov.in",
    "nrega.nic.in", "education.gov.in",
]

TRUSTED_DOMAINS = [
    "vikaspedia.in", "indiafilings.com",
    "cleartax.in", "bankbazaar.com",
]


def classify_source(url: str) -> str:
    """Classify a source URL by authority level."""
    domain = urlparse(url).netloc.lower()
    if any(d in domain for d in OFFICIAL_DOMAINS):
        return "official_government"
    if any(d in domain for d in TRUSTED_DOMAINS):
        return "trusted_secondary"
    return "general"


def score_source(url: str) -> float:
    """Score a source URL by authority. Higher is better."""
    source_type = classify_source(url)
    scores = {
        "official_government": 1.0,
        "trusted_secondary": 0.6,
        "general": 0.3,
    }
    return scores.get(source_type, 0.2)


async def fetch_page_content(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch the text content of a webpage."""
    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            
            content_type = resp.headers.get("content-type", "")
            if "text/html" not in content_type and "text/plain" not in content_type:
                return None
            
            html = resp.text
            # Simple HTML to text extraction
            import re
            # Remove script and style tags
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', html)
            # Clean whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text[:8000] if text else None
    except Exception as e:
        logger.debug(f"Failed to fetch {url}: {e}")
        return None


class BaseSearchProvider(ABC):
    """Abstract base class for search providers."""

    @abstractmethod
    async def search(
        self, query: str, max_results: int = 8, filters: Optional[Dict] = None
    ) -> SearchResponse:
        pass


class TavilySearchProvider(BaseSearchProvider):
    """Tavily search provider implementation."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com"

    async def search(
        self, query: str, max_results: int = 8, filters: Optional[Dict] = None
    ) -> SearchResponse:
        try:
            async with httpx.AsyncClient(timeout=settings.search_timeout) as client:
                payload = {
                    "api_key": self.api_key,
                    "query": query,
                    "max_results": max_results,
                    "include_raw_content": True,
                    "search_depth": "advanced",
                }
                if filters and filters.get("include_domains"):
                    payload["include_domains"] = filters["include_domains"]

                resp = await client.post(f"{self.base_url}/search", json=payload)
                resp.raise_for_status()
                data = resp.json()

                results = []
                for r in data.get("results", []):
                    url = r.get("url", "")
                    domain = urlparse(url).netloc
                    results.append(
                        SearchResult(
                            title=r.get("title", ""),
                            url=url,
                            snippet=r.get("content", "")[:500],
                            domain=domain,
                            content=r.get("raw_content", r.get("content", ""))[:8000],
                            score=r.get("score", 0.0),
                            source_type=classify_source(url),
                        )
                    )

                # Sort by source authority then relevance
                results.sort(
                    key=lambda x: (score_source(x.url), x.score), reverse=True
                )

                return SearchResponse(
                    query=query,
                    results=results,
                    total_results=len(results),
                    provider="tavily",
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"Tavily API error: {e.response.status_code}")
            return SearchResponse(
                query=query, provider="tavily", error=f"Search API error: {e.response.status_code}"
            )
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return SearchResponse(
                query=query, provider="tavily", error=f"Search failed: {str(e)}"
            )


class SerperSearchProvider(BaseSearchProvider):
    """Serper.dev search provider implementation."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev"

    async def search(
        self, query: str, max_results: int = 8, filters: Optional[Dict] = None
    ) -> SearchResponse:
        try:
            async with httpx.AsyncClient(timeout=settings.search_timeout) as client:
                headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
                payload = {"q": query, "num": max_results, "gl": "in", "hl": "en"}

                resp = await client.post(
                    f"{self.base_url}/search", json=payload, headers=headers
                )
                resp.raise_for_status()
                data = resp.json()

                results = []
                for r in data.get("organic", []):
                    url = r.get("link", "")
                    domain = urlparse(url).netloc
                    results.append(
                        SearchResult(
                            title=r.get("title", ""),
                            url=url,
                            snippet=r.get("snippet", "")[:500],
                            domain=domain,
                            content=r.get("snippet", "")[:3000],
                            score=0.5,
                            source_type=classify_source(url),
                        )
                    )

                results.sort(
                    key=lambda x: score_source(x.url), reverse=True
                )

                return SearchResponse(
                    query=query,
                    results=results,
                    total_results=len(results),
                    provider="serper",
                )

        except Exception as e:
            logger.error(f"Serper search failed: {e}")
            return SearchResponse(
                query=query, provider="serper", error=f"Search failed: {str(e)}"
            )


class DuckDuckGoSearchProvider(BaseSearchProvider):
    """DuckDuckGo search provider implementation (100% Free)."""

    def __init__(self):
        self.provider_name = "duckduckgo"

    async def search(
        self, query: str, max_results: int = 8, filters: Optional[Dict] = None
    ) -> SearchResponse:
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ddgs_results = await asyncio.to_thread(
                    DDGS().text, query, max_results=max_results
                )
            
            results = []
            for r in ddgs_results:
                url = r.get("href", "")
                domain = urlparse(url).netloc
                body = r.get("body", "")
                results.append(
                    SearchResult(
                        title=r.get("title", ""),
                        url=url,
                        snippet=body[:500],
                        domain=domain,
                        content=body[:3000],  # DDG body is short; will be enriched later
                        score=0.5,
                        source_type=classify_source(url),
                    )
                )

            results.sort(
                key=lambda x: score_source(x.url), reverse=True
            )

            # Enrich top results by fetching actual page content
            enrichment_tasks = []
            for r in results[:6]:
                enrichment_tasks.append(fetch_page_content(r.url, timeout=settings.fetch_timeout))
            
            if enrichment_tasks:
                fetched_contents = await asyncio.gather(*enrichment_tasks, return_exceptions=True)
                for i, content in enumerate(fetched_contents):
                    if i < len(results) and isinstance(content, str) and len(content) > 100:
                        results[i].content = content

            return SearchResponse(
                query=query,
                results=results,
                total_results=len(results),
                provider=self.provider_name,
            )

        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return SearchResponse(
                query=query, provider=self.provider_name, error=f"Search failed: {str(e)}"
            )


class LocalDatabaseSearchProvider(BaseSearchProvider):
    """Local JSON database search provider."""

    def __init__(self):
        self.provider_name = "local"
        self.data_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "government_schemes_1200.json"
        )
        self.schemes = self._load_data()

    def _load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load local database: {e}")
            return []

    async def search(
        self, query: str, max_results: int = 8, filters: Optional[Dict] = None
    ) -> SearchResponse:
        try:
            # Simple keyword matching scoring
            query_terms = set(query.lower().replace(',', ' ').replace('.', ' ').split())
            
            scored_schemes = []
            for scheme in self.schemes:
                score = 0.0
                
                # Check text fields
                text_to_search = (
                    scheme.get("name", "") + " " + 
                    scheme.get("description", "") + " " + 
                    " ".join(scheme.get("benefits", [])) + " " +
                    " ".join(scheme.get("tags", [])) + " " +
                    " ".join(scheme.get("eligibility", {}).get("other_conditions", []))
                ).lower()
                
                # Boost if exact query terms are in the text
                for term in query_terms:
                    if len(term) > 3 and term in text_to_search:
                        score += 1.0
                
                if score > 0:
                    scored_schemes.append((score, scheme))
            
            # Sort by score descending
            scored_schemes.sort(key=lambda x: x[0], reverse=True)
            
            # Take top max_results
            top_schemes = [s[1] for s in scored_schemes[:max_results]]
            
            results = []
            for s in top_schemes:
                # Format content to simulate extracted web page
                content = f"Scheme Name: {s.get('name')}\\n"
                content += f"Description: {s.get('description')}\\n"
                content += f"Benefits: {', '.join(s.get('benefits', []))}\\n"
                content += f"Eligibility: {', '.join(s.get('eligibility', {}).get('other_conditions', []))}\\n"
                content += f"Documents: {', '.join(s.get('documents', []))}\\n"
                content += f"Application Steps: {', '.join(s.get('application', {}).get('steps', []))}"
                
                url = s.get("source", {}).get("url", "")
                
                results.append(
                    SearchResult(
                        title=s.get("name", ""),
                        url=url,
                        snippet=s.get("description", "")[:500],
                        domain="myscheme.gov.in",
                        content=content[:8000],
                        score=1.0,
                        source_type="official_government",
                    )
                )

            return SearchResponse(
                query=query,
                results=results,
                total_results=len(results),
                provider=self.provider_name,
            )

        except Exception as e:
            logger.error(f"Local database search failed: {e}")
            return SearchResponse(
                query=query, provider=self.provider_name, error=f"Search failed: {str(e)}"
            )


def get_search_provider() -> BaseSearchProvider:
    """Factory function to get the configured search provider."""
    provider = settings.search_provider.lower()
    if provider == "tavily":
        api_key = settings.tavily_api_key
        if not api_key:
            raise ValueError("TAVILY_API_KEY is not configured. Please set it in .env")
        return TavilySearchProvider(api_key)
    elif provider == "serper":
        api_key = settings.serper_api_key
        if not api_key:
            raise ValueError("SERPER_API_KEY is not configured. Please set it in .env")
        return SerperSearchProvider(api_key)
    elif provider == "duckduckgo":
        return DuckDuckGoSearchProvider()
    elif provider == "local":
        return LocalDatabaseSearchProvider()
    else:
        raise ValueError(
            f"Unknown search provider: {provider}. Supported: tavily, serper, duckduckgo, local"
        )


def generate_search_queries(
    intent: Optional[str],
    state: Optional[str],
    keywords: List[str],
    scheme_types: List[str],
    occupation: Optional[str] = None,
    education: Optional[str] = None,
) -> List[str]:
    """Generate targeted search queries for government scheme discovery."""
    queries = []
    
    # Build base components
    state_part = f" {state}" if state else " India"
    
    # Primary query from keywords
    if keywords:
        keyword_str = " ".join(keywords[:4])
        queries.append(f"government scheme {keyword_str}{state_part} site:gov.in")
        queries.append(f"{keyword_str} government scheme eligibility{state_part}")

    # Scheme-type specific queries
    for st in scheme_types[:2]:
        queries.append(f"government {st} scheme{state_part} site:gov.in")
    
    # Occupation-based queries
    if occupation:
        queries.append(f"government scheme for {occupation}{state_part} site:gov.in")
    
    # Education-based queries
    if education:
        queries.append(f"scholarship {education} student{state_part} government site:gov.in")
    
    # Fallback if nothing specific
    if not queries:
        queries.append(f"government welfare scheme{state_part} site:gov.in")

    # Deduplicate
    seen = set()
    unique = []
    for q in queries:
        if q not in seen:
            seen.add(q)
            unique.append(q)
    
    return unique[:4]  # Limit to 4 queries
