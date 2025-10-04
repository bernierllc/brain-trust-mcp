# brain-trust v0.1.1 - Per-Request Authentication

## 🔐 Major Security and Architecture Improvement

This release refactors the authentication architecture to use **per-request API key passing** instead of server-side credential storage. This is a **breaking change** that significantly improves security.

---

## ⚡ What Changed

### New Authentication Flow

- **Before (v0.1.0)**: API key was required in Docker environment variables at server startup
- **After (v0.1.1)**: API key is passed from MCP client with each tool request

### Benefits

- ✅ **No credentials in Docker** - API keys never stored in containers or environment files
- ✅ **Per-request authentication** - Each request authenticated independently
- ✅ **Multi-client support** - Different MCP clients can use different API keys
- ✅ **Simplified deployment** - Server starts without any OpenAI configuration
- ✅ **Better security** - Keys managed by MCP client, not server

---

## 🔄 Breaking Changes

### Tool Signatures Updated

Both `phone_a_friend` and `review_plan` now require an `api_key` parameter:

```python
# phone_a_friend - NEW signature
phone_a_friend(
    question="Your question here",
    api_key="sk-...",  # NEW: Required
    context="Optional context",
    model="gpt-4",  # NEW: Optional, default gpt-4
    max_tokens=1000  # NEW: Optional, default 1000
)

# review_plan - NEW signature
review_plan(
    plan_content="Your plan content",
    api_key="sk-...",  # NEW: Required
    review_level="standard",
    context="Optional context",
    plan_id="optional-id",
    focus_areas=["timeline", "resources"],
    model="gpt-4",  # NEW: Optional, default gpt-4
    max_tokens=2000  # NEW: Optional, default 2000
)
```

### Configuration Changes

**Old Configuration (v0.1.0):**

```bash
# .env file
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
```

**New Configuration (v0.1.1):**

```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

The MCP client automatically passes the API key to tool calls.

---

## 📋 Full Changelog

### Changed

- **BREAKING**: Refactored authentication architecture to pass OpenAI API key per-request
- `phone_a_friend` now requires `api_key` parameter and accepts optional `model` and `max_tokens`
- `review_plan` now requires `api_key` parameter and accepts optional `model` and `max_tokens`
- `health_check` no longer returns `openai_configured` field
- Updated README with comprehensive documentation of new authentication flow

### Removed

- Removed `OPENAI_API_KEY`, `OPENAI_MODEL`, and `OPENAI_MAX_TOKENS` from Docker environment
- Removed global OpenAI client initialization at server startup
- Removed API key requirement from `.env.example` file
- Removed `OPENAI_*` environment variables from `fastmcp.json`

### Security

- **Improved**: API keys are no longer stored in Docker containers or environment files
- **Improved**: Per-request authentication allows different MCP clients to use different API keys
- **Improved**: API key management handled securely by MCP client configuration
- **Improved**: Server no longer requires access to OpenAI credentials at startup

### Fixed

- Server now starts successfully without requiring OpenAI API key configuration
- Cleaned up unused imports (`asyncio`, `os`) from server.py

---

## 🚀 Upgrade Guide

### Step 1: Update Your Server

```bash
# Pull the latest changes
git pull origin main

# Rebuild Docker container
docker-compose down
docker-compose up -d --build
```

### Step 2: Update MCP Client Configuration

Add the API key to your MCP client configuration file (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}
```

### Step 3: Remove Old Environment Variables

You can now remove the OpenAI configuration from:

- Docker environment variables
- `.env` files
- Any other server-side configuration

### Step 4: Restart Cursor

Restart Cursor to pick up the new MCP client configuration.

---

## 📚 Documentation

- [README.md](README.md) - Updated with new authentication flow
- [CHANGELOG.md](CHANGELOG.md) - Full version history
- [env.example](env.example) - Updated to reflect minimal server configuration

---

## 🙏 Acknowledgments

Thanks to everyone who provided feedback on making the authentication flow more secure and flexible!

---

**Full Changelog**: https://github.com/bernierllc/brain-trust-mcp/compare/v0.1.0...v0.1.1
