# brain-trust v0.1.2 - Enhanced Plan Review & Comprehensive Logging

## 🎯 Overview

This release significantly enhances the plan review capabilities with a structured Master Review Framework and adds comprehensive logging for debugging API key passing and request/response flows.

---

## ✨ What's New

### 1. Master Review Framework Integration

All review levels now follow a **consistent 10-point evaluation framework** for comprehensive plan analysis:

**Framework Dimensions:**
- **Structure & Organization** - Logical flow and accessibility
- **Completeness** - All required sections present and detailed
- **Clarity** - Unambiguous language for all stakeholders
- **Assumptions & Dependencies** - Hidden constraints explicitly called out
- **Risks** - Failure modes, edge cases, and mitigation strategies
- **Feasibility** - Realistic timelines, resources, and validation approach
- **Alternatives** - Trade-offs and alternative approaches considered
- **Validation** - Success criteria, KPIs, and metrics defined
- **Stakeholders** - Roles, responsibilities, and impacts clear
- **Long-term Sustainability** - Scalability, maintainability, adaptability

### 2. New DEEP_DIVE Review Level

A new technical-focused review level between `comprehensive` and `expert`:

```python
review_plan(
    plan_content="...",
    api_key="sk-...",
    review_level="deep_dive",  # NEW!
)
```

**DEEP_DIVE includes:**
- Section-by-section technical feasibility analysis
- FMEA-style failure mode analysis (what could go wrong and when)
- Comprehensive risk analysis: technical, operational, security, performance
- Critical path analysis with timeline validation
- Edge cases, race conditions, and boundary conditions
- Scalability projections (10x, 100x scale analysis)
- Detailed mitigation and rollback strategies
- 4-6 probing technical questions

**Review Levels (Progressive Depth):**
1. `quick` - Basic checklist (1-2 suggestions)
2. `standard` - Standard analysis (2-3 questions)
3. `comprehensive` - Detailed coverage (3-5 questions)
4. **`deep_dive`** - Technical depth with FMEA (4-6 questions) ⭐ **NEW**
5. `expert` - Professional rigor with industry standards (5-7 strategic questions)

### 3. Comprehensive Logging System

Full request/response tracing for debugging API key passing:

**Logged Information:**
- ✅ **MCP Tool Calls** - All incoming parameters from client
- ✅ **OpenAI Client Creation** - API key validation and length
- ✅ **OpenAI API Requests** - Full headers including Authorization bearer token
- ✅ **OpenAI API Responses** - Response IDs, token usage, model info
- ✅ **Success/Error States** - Detailed context for troubleshooting

**Environment-Aware Logging:**

**Development Mode (DEBUG):**
```bash
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```
- Full API keys visible in logs
- Complete request/response details
- All headers logged
- Maximum debugging information

**Production Mode (INFO+):**
```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
```
- API keys masked (first 8 + last 4 chars only)
- Essential information only
- Reduced sensitive data logging

**Example Debug Log Output:**
```json
{
  "event": "MCP Tool Call Received",
  "tool_name": "phone_a_friend",
  "parameters": {
    "api_key": "sk-proj-...full_key_in_debug...",
    "api_key_length": 164
  }
}

{
  "event": "OpenAI API Request",
  "model": "gpt-4",
  "headers": {
    "Authorization": "Bearer sk-proj-...full_key..."
  }
}

{
  "event": "OpenAI API Response",
  "response_id": "chatcmpl-...",
  "usage": {
    "prompt_tokens": 30,
    "completion_tokens": 309,
    "total_tokens": 339
  }
}
```

### 4. Pre-Commit Hooks

Automated code quality checks on every commit:

**Pre-commit Hook Runs:**
- ✅ **black** - Code formatting
- ✅ **isort** - Import sorting
- ✅ **flake8** - Linting
- ✅ **mypy** - Type checking

**Auto-configured mypy** to ignore missing imports for external dependencies.

**Location:** `.git/hooks/pre-commit`

Commits are blocked if any check fails, ensuring code quality.

### 5. Development Environment Improvements

**Auto-activate Python venv:**
- VS Code/Cursor workspace automatically activates virtual environment on terminal open
- No more manual `source venv/bin/activate`
- Graceful error handling with helpful messages

**Enhanced Docker Configuration:**
```yaml
environment:
  - ENVIRONMENT=${ENVIRONMENT:-development}
  - LOG_LEVEL=${LOG_LEVEL:-DEBUG}
  - OPENAI_API_KEY=${OPENAI_API_KEY}
```
- Environment variables properly passed to container
- Full debug logging available in containerized environment
- Simplified configuration management

---

## 🔧 Technical Improvements

### Enhanced Type Safety
- Added proper type hints for logging functions
- Fixed mypy compatibility with OpenAI SDK types
- Type-safe message handling throughout

### Logging Infrastructure
- Structured logging with JSON output
- Environment-based masking strategies
- Helper functions for consistent log formatting
- Comprehensive error context capture

### Code Quality
- Pre-commit hooks enforce standards
- Automated formatting and linting
- Type checking on every commit
- Consistent code style

---

## 📋 Review Levels Comparison

| Level | Depth | Questions | Use Case |
|-------|-------|-----------|----------|
| **quick** | Basic | 1-2 | Initial sanity check |
| **standard** | Moderate | 2-3 | Regular review |
| **comprehensive** | Detailed | 3-5 | Important projects |
| **deep_dive** ⭐ NEW | Technical | 4-6 | Technical feasibility |
| **expert** | Professional | 5-7 | Strategic decisions |

---

## 🐛 Bug Fixes

- Fixed type compatibility with OpenAI SDK message types
- Improved error handling in logging functions
- Enhanced Docker environment variable handling

---

## 📚 Documentation

### New Documentation
- **`docs/LOGGING.md`** - Complete logging system guide
  - Configuration instructions
  - Example log outputs
  - Troubleshooting guide for API key issues
  - Best practices for production use

### Updated Documentation
- **`env.example`** - Enhanced with logging configuration details
- **Pre-commit hook** - Installation and usage documentation

---

## 🚀 Usage Examples

### Deep Dive Review
```python
# Get technical-depth review with FMEA analysis
review_plan(
    plan_content=plan_text,
    api_key="sk-...",
    review_level="deep_dive",
    focus_areas=["scalability", "security", "performance"]
)
```

### Debug Mode
```bash
# Enable full debug logging
export ENVIRONMENT=development
export LOG_LEVEL=DEBUG

# Start server
python server.py

# Watch logs in real-time
tail -f server.log
```

### Docker with Debug Logging
```bash
# Run with full logging
ENVIRONMENT=development LOG_LEVEL=DEBUG docker-compose up

# Check logs
docker-compose logs -f
```

---

## 🔒 Security Notes

- **Development logging** shows full API keys - use only in development
- **Production logging** masks API keys automatically
- Never commit `.env` files with real API keys
- Pre-commit hooks help prevent accidental sensitive data commits

---

## 📦 Installation

```bash
# Pull latest changes
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Pre-commit hook is automatically available in .git/hooks/
```

---

## 🐳 Docker Deployment

```bash
# Build with latest changes
docker-compose build --no-cache

# Run with environment configuration
ENVIRONMENT=production LOG_LEVEL=INFO docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Server Configuration
ENVIRONMENT=development  # or production
LOG_LEVEL=DEBUG         # DEBUG, INFO, WARNING, ERROR, CRITICAL
PORT=8000

# Optional: OpenAI API key (for development/testing)
OPENAI_API_KEY=sk-...
```

### Workspace Configuration

The `.code-workspace` file now auto-activates the Python virtual environment on terminal open. Reload your workspace to enable.

---

## 🔄 Migration Guide

### From v0.1.1

No breaking changes. All existing code continues to work.

**Optional Enhancements:**
1. **Use new `deep_dive` review level** for technical plans
2. **Enable debug logging** during development for troubleshooting
3. **Verify pre-commit hooks** are working: `git commit` should run checks

---

## 📊 Metrics

- **Review Framework**: 10-point comprehensive coverage
- **Review Levels**: 5 distinct levels (added 1 new)
- **Logging Points**: 5+ log events per request
- **Code Quality**: 100% pre-commit enforcement
- **Type Safety**: Full mypy compliance

---

## 🙏 Acknowledgments

Thanks to all contributors who provided feedback on the review framework and logging system!

---

## 📝 Commit History

```
4694d6a feat(logging): add comprehensive logging system for API key debugging
c1c7dfd feat(review): enhance review framework with Master Review Framework structure
```

---

## 🔗 Links

- **Documentation**: `/docs/LOGGING.md`
- **Repository**: https://github.com/bernierllc/mcp-ask-questions
- **Issues**: https://github.com/bernierllc/mcp-ask-questions/issues

---

**Release Date**: October 4, 2025
**Version**: v0.1.2
**Status**: Stable

