"""
MoneyFollows - Eligibility Engine
Deterministic eligibility evaluation comparing user profile against scheme requirements.
"""

import logging
from typing import List, Optional, Tuple

from app.models.scheme import (
    EligibilityStatus,
    EligibilityResult,
    EligibilityCondition,
    EligibilityGroup,
    ExtractedScheme,
)
from app.models.user_profile import UserProfile

logger = logging.getLogger(__name__)


def _parse_numeric(value: Optional[str]) -> Optional[float]:
    """Attempt to parse a numeric value from a string."""
    if value is None:
        return None
    try:
        # Handle lakh/crore notation
        v = str(value).lower().strip()
        v = v.replace(",", "").replace("₹", "").replace("rs.", "").replace("rs", "").strip()
        if "lakh" in v:
            v = v.replace("lakh", "").strip()
            return float(v) * 100000
        if "crore" in v:
            v = v.replace("crore", "").strip()
            return float(v) * 10000000
        return float(v)
    except (ValueError, TypeError):
        return None


def _check_numeric_condition(
    condition: EligibilityCondition, user_value: Optional[float]
) -> Tuple[str, str]:
    """
    Check a numeric condition against user value.
    Returns: (status, explanation)
    """
    if user_value is None:
        return "unknown", f"Your {condition.criterion} is needed to verify: {condition.text or condition.criterion}"

    threshold = None
    if condition.value is not None:
        threshold = _parse_numeric(str(condition.value))
    if threshold is None and condition.minimum is not None:
        threshold = condition.minimum
    if threshold is None and condition.maximum is not None:
        threshold = condition.maximum

    if threshold is None:
        # Qualitative condition, can't check deterministically
        return "unknown", f"Cannot verify {condition.criterion} requirement: {condition.text or ''}"

    op = (condition.operator or "").lower()

    if op in ("less_than", "lt", "<"):
        if user_value < threshold:
            return "matched", f"Your {condition.criterion} ({user_value}) meets the requirement (< {threshold})"
        return "not_matched", f"Your {condition.criterion} ({user_value}) exceeds the limit (< {threshold})"

    elif op in ("less_than_or_equal", "lte", "<="):
        if user_value <= threshold:
            return "matched", f"Your {condition.criterion} ({user_value}) meets the requirement (≤ {threshold})"
        return "not_matched", f"Your {condition.criterion} ({user_value}) exceeds the limit (≤ {threshold})"

    elif op in ("greater_than", "gt", ">"):
        if user_value > threshold:
            return "matched", f"Your {condition.criterion} ({user_value}) meets the requirement (> {threshold})"
        return "not_matched", f"Your {condition.criterion} ({user_value}) doesn't meet the minimum (> {threshold})"

    elif op in ("greater_than_or_equal", "gte", ">="):
        if user_value >= threshold:
            return "matched", f"Your {condition.criterion} ({user_value}) meets the requirement (≥ {threshold})"
        return "not_matched", f"Your {condition.criterion} ({user_value}) doesn't meet the minimum (≥ {threshold})"

    elif op in ("equals", "eq", "=", "=="):
        if abs(user_value - threshold) < 0.01:
            return "matched", f"Your {condition.criterion} matches the requirement"
        return "not_matched", f"Your {condition.criterion} ({user_value}) doesn't match ({threshold})"

    elif op in ("between", "range"):
        minimum = condition.minimum or 0
        maximum = condition.maximum or float("inf")
        if minimum <= user_value <= maximum:
            return "matched", f"Your {condition.criterion} ({user_value}) is within the range ({minimum}-{maximum})"
        return "not_matched", f"Your {condition.criterion} ({user_value}) is outside the range ({minimum}-{maximum})"

    return "unknown", f"Cannot evaluate {condition.criterion} condition: {condition.text or ''}"


def _check_string_condition(
    condition: EligibilityCondition, user_value: Optional[str]
) -> Tuple[str, str]:
    """Check a string-based condition against user value."""
    if user_value is None:
        return "unknown", f"Your {condition.criterion} is needed to verify: {condition.text or condition.criterion}"

    cond_value = str(condition.value or "").lower().strip()
    user_val = user_value.lower().strip()
    op = (condition.operator or "").lower()

    if op in ("equals", "eq", "=", "=="):
        if user_val == cond_value or cond_value in user_val or user_val in cond_value:
            return "matched", f"Your {condition.criterion} ({user_value}) matches the requirement"
        return "not_matched", f"Your {condition.criterion} ({user_value}) doesn't match ({condition.value})"

    elif op in ("not_equals", "neq", "!="):
        if user_val != cond_value and cond_value not in user_val:
            return "matched", f"Your {condition.criterion} is not excluded"
        return "not_matched", f"Your {condition.criterion} ({user_value}) is excluded ({condition.value})"

    elif op in ("in", "includes", "contains"):
        if user_val in cond_value or cond_value in user_val:
            return "matched", f"Your {condition.criterion} ({user_value}) matches"
        return "not_matched", f"Your {condition.criterion} ({user_value}) is not in the eligible list"

    elif cond_value == "all" or cond_value == "unspecified":
        return "matched", f"No specific {condition.criterion} restriction"

    # Default: try fuzzy match
    if cond_value and (cond_value in user_val or user_val in cond_value):
        return "matched", f"Your {condition.criterion} ({user_value}) appears to match ({condition.value})"

    return "unknown", f"Cannot verify {condition.criterion}: {condition.text or ''}"


def _get_user_value_for_criterion(
    criterion: str, profile: UserProfile
) -> Tuple[Optional[float], Optional[str]]:
    """Get the appropriate user value for a criterion."""
    criterion_lower = criterion.lower()
    
    if criterion_lower in ("age", "age_requirement"):
        return profile.age, str(profile.age) if profile.age else None
    elif criterion_lower in ("income", "income_requirement", "family_income", "annual_income"):
        return profile.income, str(profile.income) if profile.income else None
    elif criterion_lower in ("state", "residence", "domicile"):
        return None, profile.state
    elif criterion_lower in ("education", "education_requirement", "qualification"):
        return None, profile.education
    elif criterion_lower in ("occupation", "employment", "employment_status"):
        return None, profile.occupation
    elif criterion_lower in ("gender", "sex"):
        return None, profile.gender
    elif criterion_lower in ("category", "caste", "social_category"):
        return None, profile.category
    elif criterion_lower in ("disability", "pwd"):
        return None, profile.disability
    
    return None, None


def evaluate_eligibility(
    scheme: ExtractedScheme, profile: UserProfile
) -> EligibilityResult:
    """
    Evaluate a user's eligibility for a scheme using deterministic rules.
    """
    matched = []
    not_matched = []
    unknown = []

    # Check geographic scope
    if scheme.geographic_scope.states:
        if profile.state:
            state_lower = profile.state.lower()
            scheme_states = [s.lower() for s in scheme.geographic_scope.states]
            if any(state_lower in s or s in state_lower for s in scheme_states):
                matched.append(f"Your state ({profile.state}) is covered by this scheme")
            elif "all" in scheme_states or "india" in scheme_states or "all india" in scheme_states:
                matched.append("This scheme is available across India")
            else:
                not_matched.append(
                    f"This scheme appears to be for {', '.join(scheme.geographic_scope.states)}; your state is {profile.state}"
                )
        else:
            unknown.append(f"Scheme is for {', '.join(scheme.geographic_scope.states)} — your state is not specified")

    # Check all eligibility conditions
    all_conditions = []
    for group in scheme.eligibility_groups:
        all_conditions.extend(group.conditions)

    for condition in all_conditions:
        criterion = (condition.criterion or "").lower()
        numeric_value, string_value = _get_user_value_for_criterion(criterion, profile)

        # Numeric criteria
        if criterion in ("age", "income", "income_requirement", "family_income", "annual_income", "age_requirement"):
            status, explanation = _check_numeric_condition(condition, numeric_value)
        else:
            status, explanation = _check_string_condition(condition, string_value)

        if status == "matched":
            matched.append(explanation)
        elif status == "not_matched":
            not_matched.append(explanation)
        else:
            unknown.append(explanation)

    # Determine overall status
    if not_matched:
        status = EligibilityStatus.LIKELY_NOT_ELIGIBLE
        explanation = "Based on the available information, you may not meet one or more requirements for this scheme."
    elif unknown and not matched:
        status = EligibilityStatus.NEEDS_MORE_INFORMATION
        explanation = "We need more information about you to determine eligibility."
    elif matched and not unknown:
        status = EligibilityStatus.LIKELY_ELIGIBLE
        explanation = "Based on the information provided, you appear to meet the listed conditions. Always verify on the official portal."
    elif matched and unknown:
        status = EligibilityStatus.POSSIBLY_ELIGIBLE
        explanation = "You meet some conditions but some requirements need verification."
    else:
        status = EligibilityStatus.UNVERIFIED
        explanation = "Insufficient information to determine eligibility. Please check the official source."

    return EligibilityResult(
        status=status,
        matched=matched,
        not_matched=not_matched,
        unknown=unknown,
        explanation=explanation,
    )
