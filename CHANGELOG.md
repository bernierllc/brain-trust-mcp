# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-10-04

### Changed

- **BREAKING**: Removed `api_key` parameter from `phone_a_friend` and `review_plan` tools
- API keys must now be provided via `X-OpenAI-API-Key` HTTP header in MCP requests
- Added `get_config_from_headers()` function to extract configuration from HTTP headers
- `model` and `max_tokens` parameters are now optional and can be provided via headers or parameters
- Updated all tests to work without `api_key` parameter
- Updated documentation to reflect header-based API key configuration

### Added

- Header-based configuration support for API key, model, and max_tokens
- Configuration can be set in MCP client's header configuration
- Parameters can override header values when provided

### Security

- **Improved**: API keys passed securely via HTTP headers on each request
- No need to store API keys in environment variables or server configuration
- Each MCP client can use different API keys via header configuration

## [0.1.1] - 2025-10-04

### Changed

- **BREAKING**: Refactored authentication architecture to pass OpenAI API key per-request instead of at server startup
- `phone_a_friend` now requires `api_key` parameter and accepts optional `model` and `max_tokens` parameters
- `review_plan` now requires `api_key` parameter and accepts optional `model` and `max_tokens` parameters
- `health_check` no longer returns `openai_configured` field
- Updated README with comprehensive documentation of new per-request authentication flow
- Updated MCP client configuration examples to reflect API key passing from client

### Removed

- Removed `OPENAI_API_KEY`, `OPENAI_MODEL`, and `OPENAI_MAX_TOKENS` from Docker environment variables
- Removed global OpenAI client initialization at server startup
- Removed API key requirement from `.env.example` file
- Removed `OPENAI_*` environment variables from `fastmcp.json` deployment configuration

### Security

- **Improved**: API keys are no longer stored in Docker containers or environment files
- **Improved**: Per-request authentication allows different MCP clients to use different API keys
- **Improved**: API key management handled securely by MCP client configuration
- **Improved**: Server no longer requires access to OpenAI credentials at startup

### Fixed

- Server now starts successfully without requiring OpenAI API key configuration
- Cleaned up unused imports (`asyncio`, `os`) from server.py

## [0.1.0] - 2025-10-04

### Added

- Initial release of brain-trust MCP server
- `phone_a_friend` tool for AI Q&A with optional context
- `review_plan` tool with review levels (quick, standard, comprehensive, expert)
- `health_check` endpoint for server status
- Docker setup (Dockerfile, docker-compose, nginx reverse proxy)
- FastMCP HTTP transport on `http://localhost:8000/mcp`
- Comprehensive README with setup, usage, and configuration
- Open-source documentation: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG
- GitHub workflows: Python lint/type-check (black, isort, flake8, mypy) and Docker build
- GitHub templates: Issue templates (bug report, feature request) and PR template
- Dependabot configuration for pip and GitHub Actions
- Smoke test script (`scripts/smoke.sh`) for health endpoint validation

[0.2.0]: https://github.com/bernierllc/brain-trust-mcp/releases/tag/v0.2.0
[0.1.1]: https://github.com/bernierllc/brain-trust-mcp/releases/tag/v0.1.1
[0.1.0]: https://github.com/bernierllc/brain-trust-mcp/releases/tag/v0.1.0
