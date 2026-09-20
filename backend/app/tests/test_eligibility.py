"""
MoneyFollows - Eligibility Engine Tests
"""

import pytest
from app.models.scheme import (
    ExtractedScheme,
    EligibilityCondition,
    EligibilityGroup,
    EligibilityStatus,
    GeographicScope,
)
from app.models.user_profile import UserProfile
from app.services.eligibility.engine import evaluate_eligibility


def _make_scheme(conditions=None, states=None):
    """Helper to create a test scheme."""
    groups = []
    if conditions:
        groups.append(EligibilityGroup(group="default", conditions=conditions))
    return ExtractedScheme(
        name="TEST_SCHEME",
        description="A test scheme for unit testing",
        geographic_scope=GeographicScope(states=states or []),
        eligibility_groups=groups,
    )


class TestAgeEligibility:
    """Test A & B: Age requirement satisfied and violated."""

    def test_age_satisfied(self):
        scheme = _make_scheme(conditions=[
            EligibilityCondition(
                criterion="age",
                operator="greater_than_or_equal",
                value="18",
                text="Must be 18 or older",
            )
        ])
        profile = UserProfile(age=20)
        result = evaluate_eligibility(scheme, profile)
        assert result.status in (EligibilityStatus.LIKELY_ELIGIBLE, EligibilityStatus.POSSIBLY_ELIGIBLE)
        assert len(result.matched) > 0

    def test_age_violated(self):
        scheme = _make_scheme(conditions=[
            EligibilityCondition(
                criterion="age",
                operator="greater_than_or_equal",
                value="18",
                text="Must be 18 or older",
            )
        ])
        profile = UserProfile(age=15)
        result = evaluate_eligibility(scheme, profile)
        assert result.status == EligibilityStatus.LIKELY_NOT_ELIGIBLE
        assert len(result.not_matched) > 0


class TestIncomeEligibility:
    """Test C & D: Income requirement satisfied and violated."""

    def test_income_satisfied(self):
        scheme = _make_scheme(conditions=[
            EligibilityCondition(
                criterion="income",
                operator="less_than_or_equal",
                value="300000",
                text="Annual family income ≤ ₹3 lakh",
            )
        ])
        profile = UserProfile(income=250000)
        result = evaluate_eligibility(scheme, profile)
        assert result.status in (EligibilityStatus.LIKELY_ELIGIBLE, EligibilityStatus.POSSIBLY_ELIGIBLE)

    def test_income_violated(self):
        scheme = _make_scheme(conditions=[
            EligibilityCondition(
                criterion="income",
                operator="less_than_or_equal",
                value="300000",
                text="Annual family income ≤ ₹3 lakh",
            )
        ])
        profile = UserProfile(income=500000)
        result = evaluate_eligibility(scheme, profile)
        assert result.status == EligibilityStatus.LIKELY_NOT_ELIGIBLE


class TestMissingInformation:
    """Test E: Missing income information."""

    def test_missing_income(self):
        scheme = _make_scheme(conditions=[
            EligibilityCondition(
                criterion="income",
                operator="less_than_or_equal",
                value="300000",
                text="Annual family income ≤ ₹3 lakh",
            )
        ])
        profile = UserProfile(age=20)
        result = evaluate_eligibility(scheme, profile)
        assert result.status in (
            EligibilityStatus.NEEDS_MORE_INFORMATION,
            EligibilityStatus.POSSIBLY_ELIGIBLE,
        )
        assert len(result.unknown) > 0


class TestStateMismatch:
    """Test F: State mismatch."""

    def test_state_mismatch(self):
        scheme = _make_scheme(
            states=["Uttar Pradesh"],
            conditions=[],
        )
        profile = UserProfile(state="Maharashtra")
        result = evaluate_eligibility(scheme, profile)
        assert result.status == EligibilityStatus.LIKELY_NOT_ELIGIBLE

    def test_state_match(self):
        scheme = _make_scheme(
            states=["Uttar Pradesh"],
            conditions=[],
        )
        profile = UserProfile(state="Uttar Pradesh")
        result = evaluate_eligibility(scheme, profile)
        assert EligibilityStatus.LIKELY_NOT_ELIGIBLE != result.status


class TestMultipleMissing:
    """Test G: Multiple missing conditions."""

    def test_multiple_missing(self):
        scheme = _make_scheme(conditions=[
            EligibilityCondition(
                criterion="age",
                operator="greater_than_or_equal",
                value="18",
            ),
            EligibilityCondition(
                criterion="income",
                operator="less_than_or_equal",
                value="300000",
            ),
            EligibilityCondition(
                criterion="education",
                operator="equals",
                value="B.Tech",
            ),
        ])
        profile = UserProfile()  # All empty
        result = evaluate_eligibility(scheme, profile)
        assert result.status == EligibilityStatus.NEEDS_MORE_INFORMATION
        assert len(result.unknown) >= 3


class TestFullEligibility:
    """Combined scenario matching the demo profile."""

    def test_demo_profile(self):
        scheme = _make_scheme(
            states=["Uttar Pradesh"],
            conditions=[
                EligibilityCondition(
                    criterion="age",
                    operator="greater_than_or_equal",
                    value="18",
                ),
                EligibilityCondition(
                    criterion="income",
                    operator="less_than_or_equal",
                    value="250000",
                ),
            ],
        )
        profile = UserProfile(
            age=20,
            state="Uttar Pradesh",
            education="B.Tech",
            occupation="Student",
            income=250000,
        )
        result = evaluate_eligibility(scheme, profile)
        assert result.status == EligibilityStatus.LIKELY_ELIGIBLE
