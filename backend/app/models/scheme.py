"""
MoneyFollows - Pydantic Models for Schemes
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class EligibilityStatus(str, Enum):
    LIKELY_ELIGIBLE = "LIKELY_ELIGIBLE"
    POSSIBLY_ELIGIBLE = "POSSIBLY_ELIGIBLE"
    NEEDS_MORE_INFORMATION = "NEEDS_MORE_INFORMATION"
    LIKELY_NOT_ELIGIBLE = "LIKELY_NOT_ELIGIBLE"
    UNVERIFIED = "UNVERIFIED"


class SourceInfo(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    domain: Optional[str] = None
    source_type: Optional[str] = None
    snippet: Optional[str] = None


class BenefitInfo(BaseModel):
    description: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = "INR"
    frequency: Optional[str] = None
    conditions: Optional[str] = None


class EligibilityCondition(BaseModel):
    criterion: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[str] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    unit: Optional[str] = None
    text: Optional[str] = None


class DocumentInfo(BaseModel):
    document: Optional[str] = None
    mandatory: Optional[bool] = None
    conditions: Optional[str] = None


class ApplicationStep(BaseModel):
    step: int
    description: str


class ApplicationInfo(BaseModel):
    mode: Optional[str] = None
    steps: List[ApplicationStep] = []
    application_url: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[str] = None


class AuthorityInfo(BaseModel):
    ministry: Optional[str] = None
    department: Optional[str] = None
    implementing_agency: Optional[str] = None


class GeographicScope(BaseModel):
    country: Optional[str] = "India"
    states: List[str] = []
    union_territories: List[str] = []


class EligibilityGroup(BaseModel):
    group: str = "default"
    conditions: List[EligibilityCondition] = []


class EligibilityResult(BaseModel):
    status: EligibilityStatus = EligibilityStatus.UNVERIFIED
    matched: List[str] = []
    not_matched: List[str] = []
    unknown: List[str] = []
    explanation: str = ""


class ExtractedScheme(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    authority: AuthorityInfo = AuthorityInfo()
    geographic_scope: GeographicScope = GeographicScope()
    benefits: List[BenefitInfo] = []
    eligibility_groups: List[EligibilityGroup] = []
    documents: List[DocumentInfo] = []
    application: ApplicationInfo = ApplicationInfo()
    source: SourceInfo = SourceInfo()
    confidence: str = "MEDIUM"


class SchemeResult(BaseModel):
    """Final scheme result sent to frontend."""
    name: Optional[str] = None
    status: EligibilityStatus = EligibilityStatus.UNVERIFIED
    description: Optional[str] = None
    category: Optional[str] = None
    authority: AuthorityInfo = AuthorityInfo()
    why_it_matches: List[str] = []
    unknown_requirements: List[str] = []
    not_matched: List[str] = []
    benefits: List[BenefitInfo] = []
    documents: List[DocumentInfo] = []
    application_steps: List[ApplicationStep] = []
    application_url: Optional[str] = None
    application_mode: Optional[str] = None
    deadline: Optional[str] = None
    official_url: Optional[str] = None
    sources: List[SourceInfo] = []
    confidence: str = "MEDIUM"
    geographic_scope: GeographicScope = GeographicScope()
