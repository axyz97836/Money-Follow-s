"""
MoneyFollows - Search & Chat API Routes
"""

import logging
from fastapi import APIRouter, HTTPException
from app.api.schemas import SearchRequest, ChatRequest
from app.models.user_profile import UserProfile
from app.services.orchestrator import search_schemes, chat_followup

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/search")
async def search_endpoint(request: SearchRequest):
    """Main scheme search endpoint."""
    try:
        profile = None
        if request.profile:
            profile = UserProfile(**request.profile.model_dump())

        result = await search_schemes(
            query=request.query,
            profile=profile,
            session_id=request.session_id,
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Search endpoint error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="We couldn't process your request right now. Please try again.",
        )


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Follow-up chat endpoint."""
    try:
        result = await chat_followup(
            message=request.message,
            session_id=request.session_id,
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="We couldn't process your follow-up right now. Please try again.",
        )
