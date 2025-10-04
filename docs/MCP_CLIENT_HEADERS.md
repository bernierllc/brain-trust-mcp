# MCP Client Header Configuration

This document explains how to configure your MCP client to send configuration as HTTP headers, eliminating the need to pass API keys and settings on every tool call.

## Client Configuration

### Option 1: Standard MCP Client Config (Cursor/Claude Desktop)

In your `~/.cursor/mcp.json` or MCP client configuration:

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

**Note**: Standard MCP protocol may not support custom headers directly. This depends on your MCP client implementation.

### Option 2: Using FastMCP Client (Python)

```python
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async with Client(
    transport=StreamableHttpTransport(
        "http://localhost:8000/mcp",
        headers={
            "X-OpenAI-API-Key": "sk-your-api-key-here",
            "X-OpenAI-Model": "gpt-4",
            "X-OpenAI-Max-Tokens": "2000"
        }
    )
) as client:
    # Headers are sent with every request
    result = await client.call_tool(
        "phone_a_friend",
        question="What is the capital of France?"
        # No need to pass api_key, model, or max_tokens!
    )
```

### Option 3: Environment Variables in Client Config

Some MCP clients support environment variable expansion:

```json
{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "sk-your-key-here",
        "OPENAI_MODEL": "gpt-4",
        "OPENAI_MAX_TOKENS": "2000"
      }
    }
  }
}
```

**Note**: Environment variables are typically passed to the server process, not as HTTP headers. Check your MCP client documentation.

## Server Implementation

### Current Approach (Parameters)

Currently, the server requires parameters on each call:

```python
phone_a_friend(
    question="What is 2+2?",
    api_key="sk-...",      # Required
    model="gpt-4",         # Optional, defaults to gpt-4
    max_tokens=1000        # Optional, defaults to 1000
)
```

### Proposed Approach (Headers + Optional Parameters)

With header support, parameters become optional:

```python
# Option 1: Use headers only
phone_a_friend(
    question="What is 2+2?"
    # api_key, model, max_tokens read from headers
)

# Option 2: Override headers with parameters
phone_a_friend(
    question="What is 2+2?",
    model="gpt-3.5-turbo"  # Override header value
    # api_key and max_tokens still from headers
)
```

## Implementation Plan

See the implementation guide in `/docs/HEADER_IMPLEMENTATION.md` for step-by-step instructions on:

1. Reading HTTP headers in tool functions
2. Making API key parameter optional
3. Implementing header fallback logic
4. Testing header-based configuration
5. Backward compatibility with existing parameter-based calls

## Security Considerations

### Headers vs Parameters

**Headers (Recommended for Production):**

- ✅ Configured once in client
- ✅ Not logged in tool parameters
- ✅ Simpler tool calls
- ⚠️ Visible in HTTP logs
- ⚠️ Require HTTPS in production

**Parameters (Current Implementation):**

- ✅ Explicit per-call control
- ✅ Different keys for different calls
- ⚠️ Must pass on every call
- ⚠️ Logged in debug mode

### Best Practices

1. **Use HTTPS** when sending API keys in headers
2. **Log header names** but not values in production
3. **Support both methods** for flexibility
4. **Validate headers** before use
5. **Document which headers** the server expects

## Example Header Names

Standard conventions for custom headers:

```
X-OpenAI-API-Key       # API key
X-OpenAI-Model         # Model name (gpt-4, gpt-3.5-turbo, etc.)
X-OpenAI-Max-Tokens    # Maximum tokens for response
X-Request-ID           # Custom request tracking
X-Client-ID            # Client identification
```

**Note**: Custom headers should start with `X-` prefix by convention.

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

### Test with Python

```python
import httpx

headers = {
    "X-OpenAI-API-Key": "sk-your-key",
    "X-OpenAI-Model": "gpt-4",
    "X-OpenAI-Max-Tokens": "1000"
}

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/mcp",
        headers=headers,
        json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "phone_a_friend",
                "arguments": {"question": "What is 2+2?"}
            },
            "id": 1
        }
    )
    print(response.json())
```

## Related Documentation

- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP HTTP Transport](https://gofastmcp.com/docs/transports/http)
- [Logging System](./LOGGING.md)
