"""Tests for MCP tool functions."""
import pytest

from server import ReviewLevel, mcp

# Get the underlying functions from the MCP tools
phone_a_friend = mcp._tool_manager._tools["phone_a_friend"].fn  # type: ignore[attr-defined]
review_plan = mcp._tool_manager._tools["review_plan"].fn  # type: ignore[attr-defined]
health_check = mcp._tool_manager._tools["health_check"].fn  # type: ignore[attr-defined]


class TestPhoneAFriend:
    """Tests for the phone_a_friend tool."""

    @pytest.mark.asyncio
    async def test_phone_a_friend_basic(self) -> None:
        """Test basic phone_a_friend call."""
        result = await phone_a_friend(
            question="What is 2+2?",
            model="gpt-4",
            max_tokens=100,
        )

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_phone_a_friend_with_context(self) -> None:
        """Test phone_a_friend with context."""
        result = await phone_a_friend(
            question="What is the capital?",
            context="The country is France",
            model="gpt-4",
            max_tokens=100,
        )

        assert result is not None
        assert isinstance(result, str)
        assert "Paris" in result or "paris" in result.lower()

    @pytest.mark.asyncio
    async def test_phone_a_friend_empty_response(self) -> None:
        """Test phone_a_friend handles edge cases."""
        # Test with a question that should get a response
        result = await phone_a_friend(
            question="What is Python?",
            model="gpt-4",
            max_tokens=100,
        )

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_phone_a_friend_different_models(self) -> None:
        """Test phone_a_friend with different models."""
        # Test with gpt-3.5-turbo (faster and cheaper for testing)
        result = await phone_a_friend(
            question="Say hello",
            model="gpt-3.5-turbo",
            max_tokens=50,
        )

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0


class TestReviewPlan:
    """Tests for the review_plan tool."""

    @pytest.fixture
    def sample_plan(self) -> str:
        """Sample plan content for testing."""
        return """
        # Project Plan: New Feature

        ## Objectives
        - Implement user authentication
        - Add role-based access control

        ## Timeline
        - Week 1: Design
        - Week 2: Implementation
        - Week 3: Testing

        ## Resources
        - 2 developers
        - 1 QA engineer

        ## Risks
        - Integration complexity
        - Timeline constraints
        """

    @pytest.mark.asyncio
    async def test_review_plan_quick(self, sample_plan: str) -> None:
        """Test quick review level."""
        result = await review_plan(
            plan_content=sample_plan,
            review_level=ReviewLevel.QUICK,
            model="gpt-4",
            max_tokens=500,
        )

        assert result is not None
        assert isinstance(result, dict)
        assert "plan_id" in result
        assert "review_level" in result
        assert "overall_score" in result
        assert "strengths" in result
        assert "weaknesses" in result
        assert "suggestions" in result
        assert result["review_level"] == "quick"

    @pytest.mark.asyncio
    async def test_review_plan_standard(self, sample_plan: str) -> None:
        """Test standard review level."""
        result = await review_plan(
            plan_content=sample_plan,
            review_level=ReviewLevel.STANDARD,
            model="gpt-4",
            max_tokens=1000,
        )

        assert result is not None
        assert isinstance(result, dict)
        assert result["review_level"] == "standard"
        assert isinstance(result["strengths"], list)
        assert isinstance(result["weaknesses"], list)
        assert isinstance(result["suggestions"], list)

    @pytest.mark.asyncio
    async def test_review_plan_deep_dive(self, sample_plan: str) -> None:
        """Test deep_dive review level."""
        result = await review_plan(
            plan_content=sample_plan,
            review_level=ReviewLevel.DEEP_DIVE,
            model="gpt-4",
            max_tokens=2000,
        )

        assert result is not None
        assert isinstance(result, dict)
        assert result["review_level"] == "deep_dive"
        assert len(result["detailed_feedback"]) > 0

    @pytest.mark.asyncio
    async def test_review_plan_with_focus_areas(
        self, sample_plan: str
    ) -> None:
        """Test review with focus areas."""
        result = await review_plan(
            plan_content=sample_plan,
            review_level=ReviewLevel.STANDARD,
            focus_areas=["timeline", "resources"],
            model="gpt-4",
            max_tokens=1000,
        )

        assert result is not None
        assert isinstance(result, dict)
        # Verify focus areas influenced the review
        feedback = result["detailed_feedback"].lower()
        assert "timeline" in feedback or "resource" in feedback

    @pytest.mark.asyncio
    async def test_review_plan_with_context(
        self, sample_plan: str
    ) -> None:
        """Test review with additional context."""
        result = await review_plan(
            plan_content=sample_plan,
            review_level=ReviewLevel.STANDARD,
            context="This is a critical production system with 1M+ users",
            model="gpt-4",
            max_tokens=1000,
        )

        assert result is not None
        assert isinstance(result, dict)
        assert len(result["detailed_feedback"]) > 0

    @pytest.mark.asyncio
    async def test_review_plan_all_levels(self, sample_plan: str) -> None:
        """Test all review levels."""
        levels = [
            ReviewLevel.QUICK,
            ReviewLevel.STANDARD,
            ReviewLevel.COMPREHENSIVE,
            ReviewLevel.DEEP_DIVE,
            ReviewLevel.EXPERT,
        ]

        for level in levels:
            result = await review_plan(
                plan_content=sample_plan,
                review_level=level,
                model="gpt-4",
                max_tokens=2000,
            )

            assert result is not None
            assert result["review_level"] == level.value
            assert 0.0 <= result["overall_score"] <= 1.0
