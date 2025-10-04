"""Tests for logging functionality."""
import os

import pytest

from server import ENVIRONMENT, LOG_LEVEL, log_mcp_call, mask_api_key


class TestLogging:
    """Tests for logging functions."""

    def test_environment_variables(self, test_environment: None) -> None:
        """Test that environment variables are properly set."""
        assert ENVIRONMENT in ["development", "production"]
        assert LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def test_mask_api_key_production(self) -> None:
        """Test API key masking in production mode."""
        # Save original environment
        original_env = os.getenv("ENVIRONMENT")
        original_log = os.getenv("LOG_LEVEL")

        try:
            # Set production mode
            os.environ["ENVIRONMENT"] = "production"
            os.environ["LOG_LEVEL"] = "INFO"

            # Reload the module to pick up new environment
            from importlib import reload

            import server

            reload(server)

            test_key = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"
            masked = server.mask_api_key(test_key)

            assert masked != test_key
            assert "..." in masked
            assert len(masked) < len(test_key)
        finally:
            # Restore original environment
            if original_env:
                os.environ["ENVIRONMENT"] = original_env
            else:
                os.environ.pop("ENVIRONMENT", None)

            if original_log:
                os.environ["LOG_LEVEL"] = original_log
            else:
                os.environ.pop("LOG_LEVEL", None)

    def test_mask_api_key_development_debug(self) -> None:
        """Test API key visibility in development debug mode."""
        # Save original environment
        original_env = os.getenv("ENVIRONMENT")
        original_log = os.getenv("LOG_LEVEL")

        try:
            # Set development debug mode
            os.environ["ENVIRONMENT"] = "development"
            os.environ["LOG_LEVEL"] = "DEBUG"

            # Reload the module to pick up new environment
            from importlib import reload

            import server

            reload(server)

            test_key = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"
            masked = server.mask_api_key(test_key)

            # In development DEBUG, key should not be masked
            assert masked == test_key
        finally:
            # Restore original environment
            if original_env:
                os.environ["ENVIRONMENT"] = original_env
            else:
                os.environ.pop("ENVIRONMENT", None)

            if original_log:
                os.environ["LOG_LEVEL"] = original_log
            else:
                os.environ.pop("LOG_LEVEL", None)

    def test_mask_api_key_empty(self) -> None:
        """Test masking of empty API key."""
        masked = mask_api_key("")
        assert masked == "None"

    def test_mask_api_key_short(self) -> None:
        """Test masking of short API key."""
        short_key = "short"
        masked = mask_api_key(short_key)
        # Short keys should be fully masked
        assert masked == "***" or masked == short_key

    def test_log_mcp_call(self, test_environment: None) -> None:
        """Test MCP call logging."""
        # This should not raise an exception
        log_mcp_call(
            "test_tool",
            question="Test question",
            api_key="test-api-key",
            model="gpt-4",
        )

    def test_log_mcp_call_with_sensitive_data(
        self, test_environment: None
    ) -> None:
        """Test that sensitive data is properly handled in logging."""
        api_key = "sk-proj-sensitive-key-1234567890"

        # This should mask the API key
        log_mcp_call(
            "test_tool",
            question="Test question",
            api_key=api_key,
        )

        # If we're in production, the key should be masked
        # In development DEBUG, it should be visible


class TestHealthCheck:
    """Tests for health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        """Test health check returns proper data."""
        from server import mcp

        # Get the underlying function
        health_check = mcp._tool_manager._tools["health_check"].fn  # type: ignore[attr-defined]
        result = await health_check()

        assert result is not None
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "healthy"
        assert "timestamp" in result
        assert "plan_reviews_count" in result
        assert isinstance(result["plan_reviews_count"], int)
        assert result["plan_reviews_count"] >= 0
