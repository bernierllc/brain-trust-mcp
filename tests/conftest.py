"""Pytest configuration and shared fixtures."""
import os
from typing import Generator

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


@pytest.fixture
def api_key() -> str:
    """Get OpenAI API key from environment."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set in environment")
    return key


@pytest.fixture
def test_environment() -> Generator[None, None, None]:
    """Set up test environment variables."""
    original_env = os.getenv("ENVIRONMENT")
    original_log_level = os.getenv("LOG_LEVEL")

    os.environ["ENVIRONMENT"] = "development"
    os.environ["LOG_LEVEL"] = "DEBUG"

    yield

    # Restore original values
    if original_env:
        os.environ["ENVIRONMENT"] = original_env
    else:
        os.environ.pop("ENVIRONMENT", None)

    if original_log_level:
        os.environ["LOG_LEVEL"] = original_log_level
    else:
        os.environ.pop("LOG_LEVEL", None)
