# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/bernierllc/brain-trust-mcp/releases/tag/v0.1.0
