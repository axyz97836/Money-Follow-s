"""
MoneyFollows - User Profile Model
"""

from typing import Optional, List
from pydantic import BaseModel


class UserProfile(BaseModel):
    """User profile for eligibility matching."""
    age: Optional[int] = None
    state: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    disability: Optional[str] = None


class QueryUnderstanding(BaseModel):
    """Structured output from query understanding."""
    intent: Optional[str] = None
    state: Optional[str] = None
    age: Optional[int] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    disability: Optional[str] = None
    keywords: List[str] = []
    scheme_types: List[str] = []
