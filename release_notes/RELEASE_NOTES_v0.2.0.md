# Release Notes - v0.2.0

**Release Date:** October 4, 2025

## 🚨 Breaking Changes

This release introduces a breaking change to how API keys are provided to the MCP server.

### API Key Authentication Change

- **REMOVED**: `api_key` parameter from `phone_a_friend` and `review_plan` tools
- **NEW**: API keys must now be provided via `X-OpenAI-API-Key` HTTP header

**Migration Required:** Update your MCP client configuration to include the API key in headers instead of passing it as a parameter.

## 📝 Summary

This release removes the `api_key` parameter from all tool calls and implements header-based authentication. This provides a cleaner API and follows MCP best practices where credentials are passed via HTTP headers.

## ✨ What's New

### Header-Based Configuration
- API keys are now extracted from `X-OpenAI-API-Key` HTTP header
- `model` and `max_tokens` can be configured via headers: `X-OpenAI-Model` and `X-OpenAI-Max-Tokens`
- Parameters can still override header values when explicitly provided
- Added `get_config_from_headers()` function to extract configuration from HTTP headers

### Tool Signature Changes

**Before (v0.1.x):**
```python
phone_a_friend(
    question="What is Python?",
    api_key="sk-...",  # Required parameter
    model="gpt-4",
    max_tokens=1000
)
```

**After (v0.2.0):**
```python
phone_a_friend(
    question="What is Python?",
    # api_key removed - now from headers
    model="gpt-4",      # Optional, can be set in headers
    max_tokens=1000     # Optional, can be set in headers
)
```

## 🔧 Changes

### Modified
- `phone_a_friend` tool no longer accepts `api_key` parameter
- `review_plan` tool no longer accepts `api_key` parameter
- `model` parameter is now optional (defaults to header or "gpt-4")
- `max_tokens` parameter is now optional (defaults to header or 1000/2000)
- Updated logging to show configuration source (header vs parameter)

### Added
- `get_config_from_headers()` function to extract configuration from HTTP headers
- Support for `X-OpenAI-API-Key` header
- Support for `X-OpenAI-Model` header  
- Support for `X-OpenAI-Max-Tokens` header
- Import of `get_http_headers` from `fastmcp.server.dependencies`

### Updated
- All tests to work without `api_key` parameter
- Documentation to reflect header-based API key configuration
- README.md with header-based configuration instructions
- tests/README.md to document the authentication changes

## 🔒 Security Improvements

- **Improved**: API keys passed securely via HTTP headers on each request
- **Improved**: No need to store API keys in environment variables or server configuration
- **Improved**: Each MCP client can use different API keys via header configuration
- **Cleaner**: API keys are not part of tool signatures

## 🚀 Migration Guide

### Update MCP Client Configuration

Update your MCP client configuration (e.g., Cursor's `mcp.json`) to include headers:

```json
{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "headers": {
        "X-OpenAI-API-Key": "sk-your-api-key-here",
        "X-OpenAI-Model": "gpt-4",
        "X-OpenAI-Max-Tokens": "2000"
      }
    }
  }
}
```

### Update Tool Calls

Remove the `api_key` parameter from all tool calls:

```diff
- result = await phone_a_friend(
-     question="What is Python?",
-     api_key="sk-...",
-     model="gpt-4"
- )

+ result = await phone_a_friend(
+     question="What is Python?",
+     model="gpt-4"  # Optional if set in headers
+ )
```

## 📋 Technical Details

### Implementation
- Added header parsing using FastMCP's `get_http_headers()` function
- OpenAI client is now created per-request with API key from headers
- Configuration priority: explicit parameters > headers > defaults

### Testing
- All existing tests updated and passing
- Tests now rely on API key being passed via HTTP headers
- No changes required to test functionality, only to test setup

## 📚 Documentation

For more information, see:
- [MCP Client Headers Documentation](../docs/MCP_CLIENT_HEADERS.md)
- [Header Implementation Guide](../docs/HEADER_IMPLEMENTATION.md)

## 🙏 Acknowledgments

This release implements the standard MCP pattern for credential management, making the server more secure and easier to use.

---

**Full Changelog**: https://github.com/bernierllc/brain-trust-mcp/compare/v0.1.1...v0.2.0

