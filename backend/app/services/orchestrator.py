"""
MoneyFollows - Main Orchestration Service
Coordinates query understanding, search, extraction, eligibility, and answer generation.
"""

import json
import logging
import asyncio
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse

from app.config import settings
from app.models.scheme import (
    ExtractedScheme,
    SchemeResult,
    EligibilityResult,
    SourceInfo,
    BenefitInfo,
    DocumentInfo,
    ApplicationStep,
    EligibilityCondition,
    EligibilityGroup,
    AuthorityInfo,
    GeographicScope,
    ApplicationInfo,
    EligibilityStatus,
)
from app.models.user_profile import UserProfile, QueryUnderstanding
from app.models.search_result import SearchResult, SearchResponse
from app.services.search.provider import (
    get_search_provider,
    generate_search_queries,
    classify_source,
    score_source,
)
from app.services.llm.provider import get_llm_provider
from app.services.eligibility.engine import evaluate_eligibility

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

# In-memory session store for follow-up context
_sessions: Dict[str, Dict[str, Any]] = {}


def _load_prompt(name: str) -> str:
    """Load a prompt template from file."""
    path = PROMPTS_DIR / f"{name}.txt"
    return path.read_text(encoding="utf-8")


def _merge_profile(profile: Optional[UserProfile], understood: QueryUnderstanding) -> UserProfile:
    """Merge user profile with query understanding, preferring explicit profile values."""
    if profile is None:
        profile = UserProfile()
    
    return UserProfile(
        age=profile.age or understood.age,
        state=profile.state or understood.state,
        education=profile.education or understood.education,
        occupation=profile.occupation or understood.occupation,
        income=profile.income or understood.income,
        gender=profile.gender or understood.gender,
        category=profile.category or understood.category,
        disability=profile.disability or understood.disability,
    )


def _deduplicate_results(results: List[SearchResult]) -> List[SearchResult]:
    """Deduplicate search results by normalized URL."""
    seen_urls = set()
    unique = []
    for r in results:
        normalized = r.url.lower().rstrip("/").split("?")[0].split("#")[0]
        if normalized not in seen_urls:
            seen_urls.add(normalized)
            unique.append(r)
    return unique


def _parse_extracted_scheme(data: Dict, source: SearchResult) -> ExtractedScheme:
    """Parse LLM extraction output into an ExtractedScheme model."""
    try:
        eligibility_groups = []
        for eg in data.get("eligibility_groups", []):
            conditions = []
            for c in eg.get("conditions", []):
                conditions.append(EligibilityCondition(
                    criterion=c.get("criterion"),
                    operator=c.get("operator"),
                    value=str(c.get("value")) if c.get("value") is not None else None,
                    minimum=c.get("minimum"),
                    maximum=c.get("maximum"),
                    unit=c.get("unit"),
                    text=c.get("text"),
                ))
            eligibility_groups.append(EligibilityGroup(
                group=eg.get("group", "default"),
                conditions=conditions,
            ))

        benefits = []
        for b in data.get("benefits", []):
            benefits.append(BenefitInfo(
                description=b.get("description"),
                amount=b.get("amount"),
                frequency=b.get("frequency"),
                conditions=b.get("conditions"),
            ))

        documents = []
        for d in data.get("documents", []):
            documents.append(DocumentInfo(
                document=d.get("document"),
                mandatory=d.get("mandatory"),
                conditions=d.get("conditions"),
            ))

        app_data = data.get("application", {})
        app_steps = []
        for s in app_data.get("steps", []):
            app_steps.append(ApplicationStep(
                step=s.get("step", 1),
                description=s.get("description", ""),
            ))

        authority_data = data.get("authority", {})
        geo_data = data.get("geographic_scope", {})

        return ExtractedScheme(
            name=data.get("name"),
            description=data.get("description"),
            category=data.get("category"),
            authority=AuthorityInfo(
                ministry=authority_data.get("ministry"),
                department=authority_data.get("department"),
                implementing_agency=authority_data.get("implementing_agency"),
            ),
            geographic_scope=GeographicScope(
                country=geo_data.get("country", "India"),
                states=geo_data.get("states", []),
                union_territories=geo_data.get("union_territories", []),
            ),
            benefits=benefits,
            eligibility_groups=eligibility_groups,
            documents=documents,
            application=ApplicationInfo(
                mode=app_data.get("mode"),
                steps=app_steps,
                application_url=app_data.get("application_url"),
                deadline=app_data.get("deadline"),
                status=app_data.get("status"),
            ),
            source=SourceInfo(
                title=source.title,
                url=source.url,
                domain=source.domain,
                source_type=source.source_type,
                snippet=source.snippet[:300] if source.snippet else None,
            ),
            confidence=data.get("confidence", "MEDIUM"),
        )
    except Exception as e:
        logger.error(f"Error parsing extracted scheme: {e}")
        return ExtractedScheme(
            name=data.get("name", "Unknown Scheme"),
            description=data.get("description"),
            source=SourceInfo(
                title=source.title,
                url=source.url,
                domain=source.domain,
                source_type=source.source_type,
            ),
        )


async def _understand_query(query: str, profile: Optional[UserProfile]) -> QueryUnderstanding:
    """Use LLM to understand the user's query."""
    try:
        llm = get_llm_provider()
        prompt_template = _load_prompt("query_understanding")
        prompt = prompt_template.format(
            query=query,
            profile=json.dumps(profile.model_dump() if profile else {}, indent=2),
        )
        
        result = await llm.generate_json(prompt)
        return QueryUnderstanding(**result)
    except Exception as e:
        logger.error(f"Query understanding failed: {e}")
        # Fallback: extract basic keywords
        words = query.lower().split()
        return QueryUnderstanding(
            intent="find_schemes",
            keywords=[w for w in words if len(w) > 3][:5],
        )


async def _extract_scheme(source: SearchResult, query: str) -> List[ExtractedScheme]:
    """Extract scheme information from a search result using LLM."""
    try:
        if not source.content or len(source.content.strip()) < 50:
            return []

        llm = get_llm_provider()
        prompt_template = _load_prompt("scheme_extraction")
        prompt = prompt_template.format(
            source_title=source.title,
            source_url=source.url,
            source_domain=source.domain,
            source_content=source.content[:6000],
            query=query,
        )

        result = await llm.generate_json(prompt)

        if not result.get("is_scheme", False):
            return []

        schemes = []
        for scheme_data in result.get("schemes", []):
            scheme = _parse_extracted_scheme(scheme_data, source)
            if scheme.name:
                schemes.append(scheme)

        return schemes
    except Exception as e:
        logger.error(f"Scheme extraction failed for {source.url}: {e}")
        return []


async def _generate_answer(
    query: str,
    profile: UserProfile,
    scheme_results: List[SchemeResult],
) -> str:
    """Generate a user-friendly answer using LLM."""
    try:
        llm = get_llm_provider()
        prompt_template = _load_prompt("answer_generation")
        
        schemes_data = []
        eligibility_data = []
        for sr in scheme_results:
            schemes_data.append({
                "name": sr.name,
                "description": sr.description,
                "benefits": [b.model_dump() for b in sr.benefits],
                "sources": [s.model_dump() for s in sr.sources],
            })
            eligibility_data.append({
                "scheme": sr.name,
                "status": sr.status.value,
                "matched": sr.why_it_matches,
                "unknown": sr.unknown_requirements,
                "not_matched": sr.not_matched,
            })

        prompt = prompt_template.format(
            query=query,
            profile=json.dumps(profile.model_dump(), indent=2),
            schemes=json.dumps(schemes_data, indent=2),
            eligibility_results=json.dumps(eligibility_data, indent=2),
        )

        return await llm.generate(prompt)
    except Exception as e:
        logger.error(f"Answer generation failed: {e}")
        return "We found some potentially relevant schemes. Please review the details below and verify eligibility on the official government portals."


def _scheme_to_result(
    scheme: ExtractedScheme, eligibility: EligibilityResult
) -> SchemeResult:
    """Convert extracted scheme + eligibility into a frontend-ready result."""
    return SchemeResult(
        name=scheme.name,
        status=eligibility.status,
        description=scheme.description,
        category=scheme.category,
        authority=scheme.authority,
        why_it_matches=eligibility.matched,
        unknown_requirements=eligibility.unknown,
        not_matched=eligibility.not_matched,
        benefits=scheme.benefits,
        documents=scheme.documents,
        application_steps=scheme.application.steps,
        application_url=scheme.application.application_url,
        application_mode=scheme.application.mode,
        deadline=scheme.application.deadline,
        official_url=scheme.source.url,
        sources=[scheme.source],
        confidence=scheme.confidence,
        geographic_scope=scheme.geographic_scope,
    )


async def search_schemes(
    query: str,
    profile: Optional[UserProfile] = None,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main orchestration function: search → extract → evaluate → generate answer.
    """
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Starting scheme search: {query[:80]}")

    # Step 1: Understand the query
    understood = await _understand_query(query, profile)
    logger.info(f"[{request_id}] Query understood: intent={understood.intent}, keywords={understood.keywords}")

    # Merge profile
    merged_profile = _merge_profile(profile, understood)

    # Step 2: Generate search queries
    search_queries = generate_search_queries(
        intent=understood.intent,
        state=merged_profile.state,
        keywords=understood.keywords,
        scheme_types=understood.scheme_types,
        occupation=merged_profile.occupation,
        education=merged_profile.education,
    )
    logger.info(f"[{request_id}] Generated {len(search_queries)} search queries")

    # Step 3: Execute searches
    search_provider = get_search_provider()
    all_results: List[SearchResult] = []

    search_tasks = [
        search_provider.search(q, max_results=5) for q in search_queries
    ]
    search_responses = await asyncio.gather(*search_tasks, return_exceptions=True)

    for resp in search_responses:
        if isinstance(resp, SearchResponse) and not resp.error:
            all_results.extend(resp.results)
        elif isinstance(resp, Exception):
            logger.error(f"[{request_id}] Search error: {resp}")

    # Deduplicate
    unique_results = _deduplicate_results(all_results)
    logger.info(f"[{request_id}] Found {len(unique_results)} unique results")

    if not unique_results:
        return {
            "query": query,
            "summary": "We couldn't find sufficiently relevant schemes from the sources we checked. Try refining your question or adding more details like your state, education, or occupation.",
            "schemes": [],
            "disclaimer": "MoneyFollows is an independent AI-powered discovery prototype. Always verify on the official government portal.",
            "search_metadata": {
                "sources_checked": 0,
                "official_sources": 0,
                "search_queries": search_queries,
            },
        }

    # Step 4: Extract schemes from top results (limit to avoid cost/latency)
    top_results = unique_results[:6]
    extraction_tasks = [_extract_scheme(r, query) for r in top_results]
    extraction_results = await asyncio.gather(*extraction_tasks, return_exceptions=True)

    extracted_schemes: List[ExtractedScheme] = []
    for result in extraction_results:
        if isinstance(result, list):
            extracted_schemes.extend(result)
        elif isinstance(result, Exception):
            logger.error(f"[{request_id}] Extraction error: {result}")

    logger.info(f"[{request_id}] Extracted {len(extracted_schemes)} schemes")

    # Deduplicate by scheme name
    seen_names = set()
    unique_schemes = []
    for s in extracted_schemes:
        name_key = (s.name or "").lower().strip()
        if name_key and name_key not in seen_names:
            seen_names.add(name_key)
            unique_schemes.append(s)
        elif not name_key:
            unique_schemes.append(s)

    # Step 5: Evaluate eligibility
    scheme_results: List[SchemeResult] = []
    for scheme in unique_schemes:
        eligibility = evaluate_eligibility(scheme, merged_profile)
        result = _scheme_to_result(scheme, eligibility)
        scheme_results.append(result)

    # Sort by eligibility status priority
    status_priority = {
        EligibilityStatus.LIKELY_ELIGIBLE: 0,
        EligibilityStatus.POSSIBLY_ELIGIBLE: 1,
        EligibilityStatus.NEEDS_MORE_INFORMATION: 2,
        EligibilityStatus.UNVERIFIED: 3,
        EligibilityStatus.LIKELY_NOT_ELIGIBLE: 4,
    }
    scheme_results.sort(key=lambda x: status_priority.get(x.status, 5))

    # Step 6: Generate answer
    summary = await _generate_answer(query, merged_profile, scheme_results)

    # Count official sources
    official_count = sum(
        1 for r in unique_results if classify_source(r.url) == "official_government"
    )

    # Store session context for follow-ups
    if session_id:
        _sessions[session_id] = {
            "profile": merged_profile.model_dump(),
            "schemes": [sr.model_dump() for sr in scheme_results],
            "query": query,
        }

    response = {
        "query": query,
        "summary": summary,
        "schemes": [sr.model_dump() for sr in scheme_results],
        "disclaimer": "MoneyFollows is an independent AI-powered discovery prototype. Information is retrieved from available sources and may change. Always verify eligibility, documents, deadlines, and application requirements on the official government portal before applying.",
        "search_metadata": {
            "sources_checked": len(unique_results),
            "official_sources": official_count,
            "search_queries": search_queries,
        },
        "session_id": session_id or str(uuid.uuid4()),
    }

    logger.info(f"[{request_id}] Returning {len(scheme_results)} schemes")
    return response


async def chat_followup(
    message: str,
    session_id: str,
) -> Dict[str, Any]:
    """Handle follow-up questions using session context."""
    session = _sessions.get(session_id, {})
    
    if not session:
        # No prior context, treat as new search
        return await search_schemes(message, session_id=session_id)

    # Check if this is a refinement or new question
    profile = UserProfile(**session.get("profile", {}))
    previous_schemes = session.get("schemes", [])
    previous_query = session.get("query", "")

    try:
        llm = get_llm_provider()
        
        context = f"""Previous question: {previous_query}
Previous schemes found: {json.dumps([s.get('name', '') for s in previous_schemes])}
User profile: {json.dumps(profile.model_dump())}

New question: {message}

Determine if this is:
1. A follow-up about previously found schemes (answer from context)
2. A new search query (requires new search)

Return JSON: {{"type": "followup" or "new_search", "answer": "answer if followup, null if new_search"}}"""

        result = await llm.generate_json(context)

        if result.get("type") == "followup" and result.get("answer"):
            return {
                "query": message,
                "summary": result["answer"],
                "schemes": previous_schemes,
                "disclaimer": "MoneyFollows is an independent AI-powered discovery prototype. Always verify on the official government portal.",
                "search_metadata": {
                    "sources_checked": 0,
                    "official_sources": 0,
                    "search_queries": [],
                },
                "session_id": session_id,
            }
        else:
            return await search_schemes(message, profile, session_id)

    except Exception as e:
        logger.error(f"Follow-up handling failed: {e}")
        return await search_schemes(message, profile, session_id)
