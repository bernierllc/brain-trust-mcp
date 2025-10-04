# Tests

This directory contains pytest-based tests for the MCP Ask Questions server.

## Test Structure

```
tests/
├── __init__.py           # Test suite initialization
├── conftest.py           # Shared pytest fixtures and configuration
├── test_tools.py         # Tests for MCP tools (phone_a_friend, review_plan)
├── test_logging.py       # Tests for logging functionality
└── README.md            # This file
```

## Running Tests

### Run All Tests

```bash
# From project root
pytest tests/

# With verbose output
pytest -v tests/

# With coverage
pytest --cov=server tests/
```

### Run Specific Test Files

```bash
# Test tools only
pytest tests/test_tools.py

# Test logging only
pytest tests/test_logging.py
```

### Run Specific Test Classes or Methods

```bash
# Run a specific test class
pytest tests/test_tools.py::TestPhoneAFriend

# Run a specific test method
pytest tests/test_tools.py::TestPhoneAFriend::test_phone_a_friend_basic
```

## Test Requirements

### Environment Setup

Tests require the following environment variables:

```bash
# Required for API integration tests
OPENAI_API_KEY=sk-...

# Optional (will be set by fixtures if not provided)
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

Create a `.env` file in the project root or export these variables.

### Dependencies

All test dependencies are included in `requirements.txt`:

- `pytest>=7.0.0`
- `pytest-asyncio>=0.21.0`
- `pytest-cov>=4.0.0`

Install with:

```bash
pip install -r requirements.txt
```

## Test Categories

### Integration Tests

Tests that make actual API calls to OpenAI:

- `test_tools.py::TestPhoneAFriend` - Tests phone_a_friend tool
- `test_tools.py::TestReviewPlan` - Tests review_plan tool

**Note:** These tests will:

- Consume OpenAI API tokens
- Require a valid `OPENAI_API_KEY`
- Be skipped if API key is not set

### Unit Tests

Tests that don't require external API calls:

- `test_logging.py::TestLogging` - Tests logging functions
- `test_logging.py::TestHealthCheck` - Tests health check endpoint

## Test Fixtures

Shared fixtures are defined in `conftest.py`:

- `load_env` - Loads environment variables from `.env` (autouse, session-scoped)
- `api_key` - Provides OpenAI API key and skips tests if not available (currently not used as the server reads the API key from environment)
- `test_environment` - Sets up test environment variables
- `sample_plan` - Provides sample plan content for review tests (defined in test classes)

## Skipping Tests

### Skip Tests Without API Key

Tests requiring an API key will automatically skip if `OPENAI_API_KEY` is not set:

```bash
# This will skip API integration tests
unset OPENAI_API_KEY
pytest tests/
```

### Skip Specific Tests

Use pytest markers:

```bash
# Skip slow tests
pytest -m "not slow" tests/

# Run only fast tests
pytest -m "fast" tests/
```

## Test Coverage

Generate a coverage report:

```bash
# Terminal report
pytest --cov=server --cov-report=term tests/

# HTML report
pytest --cov=server --cov-report=html tests/
open htmlcov/index.html
```

## Continuous Integration

Tests run automatically on:

- Every commit (via pre-commit hooks for fast tests)
- Pull requests (full test suite)
- Main branch pushes

## Writing New Tests

### Test Structure

Follow pytest best practices:

1. **Use descriptive test names**: `test_<what_is_being_tested>`
2. **Organize tests in classes**: Group related tests
3. **Use fixtures**: Reuse setup code
4. **Add docstrings**: Explain what the test does
5. **Use assertions**: Clear, specific assertions

### Example Test

```python
import pytest

class TestNewFeature:
    """Tests for new feature."""

    @pytest.fixture
    def sample_data(self):
        """Provide sample data for tests."""
        return {"key": "value"}

    @pytest.mark.asyncio
    async def test_feature_works(self, sample_data, api_key):
        """Test that feature works correctly."""
        result = await new_feature(sample_data, api_key)

        assert result is not None
        assert result["status"] == "success"
```

## Debugging Tests

### Run with Debug Output

```bash
# Print stdout/stderr
pytest -s tests/

# More verbose output
pytest -vv tests/

# Stop on first failure
pytest -x tests/

# Enter debugger on failure
pytest --pdb tests/
```

### Debug Specific Test

```bash
# Run single test with output
pytest -s tests/test_tools.py::TestPhoneAFriend::test_phone_a_friend_basic
```

## Known Issues

- Some tests may be slow due to OpenAI API latency
- Tests requiring API calls will fail if API key is invalid
- Environment variable changes may require module reloading

## Contributing

When adding new features:

1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain >80% code coverage
4. Update this README if adding new test categories
