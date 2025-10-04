# Header-Based Configuration Implementation Guide

This guide shows how to modify the server to read configuration from HTTP headers, making API keys and settings configurable in the MCP client without passing them on every tool call.

## Architecture

### Flow

```
MCP Client Config
  ↓
HTTP Headers (X-OpenAI-API-Key, X-OpenAI-Model, etc.)
  ↓
FastMCP Server (reads headers)
  ↓
Tool Functions (use headers or parameters)
  ↓
OpenAI API
```

### Benefits

- ✅ Configure once in client
- ✅ Cleaner tool calls
- ✅ Consistent settings across calls
- ✅ Backward compatible (parameters still work)
- ✅ Override headers with parameters when needed

## Implementation

### Step 1: Add Header Reading Helper

Add this helper function to `server.py`:

```python
from fastmcp.server.dependencies import get_http_headers

def get_config_from_headers() -> Dict[str, Any]:
    """Extract configuration from HTTP headers."""
    headers = get_http_headers()

    config = {}

    # Read API key from header
    if api_key := headers.get("x-openai-api-key"):
        config["api_key"] = api_key

    # Read model from header
    if model := headers.get("x-openai-model"):
        config["model"] = model

    # Read max tokens from header
    if max_tokens := headers.get("x-openai-max-tokens"):
        try:
            config["max_tokens"] = int(max_tokens)
        except ValueError:
            logger.warning(f"Invalid max_tokens header: {max_tokens}")

    logger.debug(
        "Configuration from headers",
        has_api_key=bool(config.get("api_key")),
        api_key_length=len(config.get("api_key", "")),
        model=config.get("model"),
        max_tokens=config.get("max_tokens"),
    )

    return config
```

### Step 2: Update phone_a_friend Tool

Make parameters optional and read from headers:

```python
@mcp.tool()
async def phone_a_friend(
    question: Annotated[str, "The question to ask OpenAI"],
    api_key: Annotated[
        Optional[str],
        "OpenAI API key for authentication (optional if set in headers)"
    ] = None,
    context: Annotated[
        Optional[str],
        "Optional context information to provide background for the question",
    ] = None,
    model: Annotated[
        Optional[str],
        "OpenAI model to use (optional if set in headers)"
    ] = None,
    max_tokens: Annotated[
        Optional[int],
        "Maximum tokens for response (optional if set in headers)"
    ] = None,
) -> str:
    """Phone a friend (OpenAI) to get help with a question."""

    # Get configuration from headers
    header_config = get_config_from_headers()

    # Use parameters if provided, otherwise fall back to headers
    final_api_key = api_key or header_config.get("api_key")
    final_model = model or header_config.get("model", "gpt-4")
    final_max_tokens = max_tokens or header_config.get("max_tokens", 1000)

    # Validate API key is available
    if not final_api_key:
        raise ValueError(
            "API key must be provided either as parameter or in X-OpenAI-API-Key header"
        )

    # Log incoming MCP call
    log_mcp_call(
        "phone_a_friend",
        question=question[:100] if len(question) > 100 else question,
        api_key=final_api_key,
        api_key_source="parameter" if api_key else "header",
        context=context[:100] if context and len(context) > 100 else context,
        model=final_model,
        model_source="parameter" if model else "header",
        max_tokens=final_max_tokens,
    )

    # Rest of the function uses final_api_key, final_model, final_max_tokens
    client = openai.OpenAI(api_key=final_api_key)

    # ... continue with existing logic
```

### Step 3: Update review_plan Tool

Similar pattern for review_plan:

```python
@mcp.tool()
async def review_plan(
    plan_content: Annotated[str, "The full content of the plan document to review"],
    api_key: Annotated[
        Optional[str],
        "OpenAI API key for authentication (optional if set in headers)"
    ] = None,
    review_level: Annotated[
        ReviewLevel,
        "Level of review depth: 'quick', 'standard', 'comprehensive', 'deep_dive', or 'expert'",
    ] = ReviewLevel.STANDARD,
    context: Annotated[
        Optional[str],
        "Optional context information about the project, team, or constraints",
    ] = None,
    plan_id: Annotated[Optional[str], "Optional identifier for the plan"] = None,
    focus_areas: Annotated[
        Optional[List[str]],
        (
            "Specific areas to focus on "
            "(e.g., 'timeline', 'resources', 'risks', 'budget')"
        ),
    ] = None,
    model: Annotated[
        Optional[str],
        "OpenAI model to use (optional if set in headers)"
    ] = None,
    max_tokens: Annotated[
        Optional[int],
        "Maximum tokens for response (optional if set in headers)"
    ] = None,
) -> Dict[str, Any]:
    """Review a plan file and provide feedback based on the specified review level."""

    # Get configuration from headers
    header_config = get_config_from_headers()

    # Use parameters if provided, otherwise fall back to headers
    final_api_key = api_key or header_config.get("api_key")
    final_model = model or header_config.get("model", "gpt-4")
    final_max_tokens = max_tokens or header_config.get("max_tokens", 2000)

    # Validate API key is available
    if not final_api_key:
        raise ValueError(
            "API key must be provided either as parameter or in X-OpenAI-API-Key header"
        )

    # ... continue with existing logic
```

### Step 4: Enhanced Logging

Update logging to show configuration source:

```python
def log_openai_request(
    model: str,
    messages: List[Dict[str, Any]],
    max_tokens: int,
    api_key: str,
    config_source: Dict[str, str] = None,
) -> None:
    """Log OpenAI request details with configuration source."""
    logger.debug(
        "OpenAI API Request",
        environment=ENVIRONMENT,
        log_level=LOG_LEVEL,
        model=model,
        model_source=config_source.get("model", "default") if config_source else "parameter",
        messages=messages,
        max_tokens=max_tokens,
        max_tokens_source=config_source.get("max_tokens", "default") if config_source else "parameter",
        api_key=mask_api_key(api_key),
        api_key_source=config_source.get("api_key", "default") if config_source else "parameter",
        api_key_length=len(api_key) if api_key else 0,
        headers={
            "Authorization": f"Bearer {mask_api_key(api_key)}",
            "Content-Type": "application/json",
        },
    )
```

## Testing

### Test with curl

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "X-OpenAI-API-Key: sk-your-key" \
  -H "X-OpenAI-Model: gpt-4" \
  -H "X-OpenAI-Max-Tokens: 1000" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "phone_a_friend",
      "arguments": {
        "question": "What is 2+2?"
      }
    },
    "id": 1
  }'
```

### Test Header Priority

```bash
# Headers provide defaults
curl -X POST http://localhost:8000/mcp \
  -H "X-OpenAI-Model: gpt-4" \
  -H "X-OpenAI-API-Key: sk-header-key" \
  -d '{
    "params": {
      "name": "phone_a_friend",
      "arguments": {
        "question": "Test",
        "model": "gpt-3.5-turbo"  # Overrides header
      }
    }
  }'
```

## Backward Compatibility

The implementation maintains full backward compatibility:

### Old Code (still works)

```python
# Explicit parameters
phone_a_friend(
    question="What is 2+2?",
    api_key="sk-...",
    model="gpt-4",
    max_tokens=1000
)
```

### New Code (with headers)

```python
# Headers provide configuration
phone_a_friend(
    question="What is 2+2?"
)

# Mix headers and parameters
phone_a_friend(
    question="What is 2+2?",
    model="gpt-3.5-turbo"  # Override header
)
```

## MCP Client Compatibility

### Known Compatible Clients

- **FastMCP Python Client** - Full header support
- **Custom HTTP clients** - Full header support
- **Cursor** - Check if headers are supported in mcp.json
- **Claude Desktop** - Check if headers are supported in config

### Fallback Strategy

If your MCP client doesn't support headers:

1. Continue using parameter-based API
2. Use environment variables on server side
3. Create a client-side wrapper

## Migration Guide

### Phase 1: Add Header Support (Non-Breaking)

- Add `get_config_from_headers()` helper
- Make API key/model/max_tokens optional
- Read from headers with parameter fallback
- Existing code continues to work

### Phase 2: Update Clients (Optional)

- Update client configurations to use headers
- Simplify tool calls (remove redundant parameters)
- Test both methods work

### Phase 3: Deprecation (Future)

- Eventually can make parameters-only deprecated
- Force header-based configuration
- Update all clients

## Related Documentation

- [Logging System](./LOGGING.md)
- [MCP Client Configuration](./MCP_CLIENT_HEADERS.md)
- [Security Best Practices](../SECURITY.md)
