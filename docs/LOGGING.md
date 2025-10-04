# Logging System

This document describes the comprehensive logging system implemented in the MCP Ask Questions server for debugging API key passing and request/response flow.

## Overview

The server includes detailed logging at multiple levels to help debug issues with API key passing from MCP clients to OpenAI API calls.

## Configuration

### Environment Variables

Set these in your `.env` file:

```bash
ENVIRONMENT=development  # or production
LOG_LEVEL=DEBUG          # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Log Levels

- **DEBUG**: Full logging including API keys (development only)
- **INFO**: Standard logging with masked API keys
- **WARNING**: Only warnings and errors
- **ERROR**: Only errors
- **CRITICAL**: Only critical errors

## Logging Features

### 1. MCP Tool Call Logging

Every tool call from the MCP client is logged with:
- Tool name
- All parameters (API keys masked based on environment)
- Request metadata

**Example log output:**
```json
{
  "event": "MCP Tool Call Received",
  "environment": "development",
  "log_level": "DEBUG",
  "tool_name": "phone_a_friend",
  "parameters": {
    "question": "What is the capital of France?",
    "api_key": "sk-proj-...pjMA",
    "model": "gpt-4",
    "max_tokens": 1000
  }
}
```

### 2. OpenAI Client Creation

Logs when the OpenAI client is created with:
- API key provided (boolean)
- API key length
- Masked API key

**Example log output:**
```json
{
  "event": "Creating OpenAI client",
  "api_key_provided": true,
  "api_key_length": 164,
  "api_key_masked": "sk-proj-...pjMA"
}
```

### 3. OpenAI API Request Logging

Before each OpenAI API call, logs:
- Model name
- Messages (full content)
- Max tokens
- API key (masked or full depending on environment)
- Request headers

**Example log output:**
```json
{
  "event": "OpenAI API Request",
  "environment": "development",
  "log_level": "DEBUG",
  "model": "gpt-4",
  "messages": [
    {
      "role": "user",
      "content": "Question: What is the capital of France?\n\nPlease provide a comprehensive answer."
    }
  ],
  "max_tokens": 1000,
  "api_key": "sk-proj-EXAMPLE1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
  "api_key_length": 164,
  "headers": {
    "Authorization": "Bearer sk-proj-EXAMPLE1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "Content-Type": "application/json"
  }
}
```

### 4. OpenAI API Response Logging

After each OpenAI API call, logs:
- Response ID
- Model used
- Token usage
- Number of choices
- Response headers

**Example log output:**
```json
{
  "event": "OpenAI API Response",
  "environment": "development",
  "log_level": "DEBUG",
  "response_id": "chatcmpl-AaBbCcDd1234567890",
  "model": "gpt-4-0613",
  "usage": {
    "prompt_tokens": 23,
    "completion_tokens": 15,
    "total_tokens": 38
  },
  "choices_count": 1,
  "response_headers": {
    "content-type": "application/json"
  }
}
```

### 5. Error Logging

Enhanced error logging includes:
- Error message
- Error type
- API key status (provided, length)
- Context information

**Example log output:**
```json
{
  "event": "Failed to phone a friend",
  "error": "Invalid API key provided",
  "error_type": "AuthenticationError",
  "api_key_provided": true,
  "api_key_length": 164
}
```

## API Key Masking

### Development Environment (ENVIRONMENT=development, LOG_LEVEL=DEBUG)

- **Full API keys are logged** for debugging purposes
- All request/response details are logged
- Sensitive data is visible

### Production Environment or Non-DEBUG Log Level

- **API keys are masked** showing only first 8 and last 4 characters
- Example: `sk-proj-EXAMPLE...6789`
- Reduced logging of sensitive data

## Usage

### Enable Full Debug Logging

1. Update your `.env` file:
   ```bash
   ENVIRONMENT=development
   LOG_LEVEL=DEBUG
   ```

2. Restart the server:
   ```bash
   python server.py
   ```

3. Make a tool call from your MCP client

4. Check the logs for detailed information about:
   - Incoming MCP call with all parameters
   - OpenAI client creation with API key details
   - OpenAI API request with full headers and API key
   - OpenAI API response with usage statistics

### Disable Sensitive Logging (Production)

1. Update your `.env` file:
   ```bash
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

2. Restart the server

3. API keys will now be masked in all logs

## Troubleshooting API Key Issues

When debugging API key passing issues, check the logs for:

1. **MCP Tool Call**: Verify the API key is being passed from the client
   - Look for `"api_key"` parameter in the MCP Tool Call log
   - Check the length: should be ~164 characters for OpenAI keys

2. **OpenAI Client Creation**: Verify the API key is reaching the client creation
   - Check `"api_key_provided": true`
   - Check `"api_key_length"` matches expected length

3. **OpenAI API Request**: Verify the API key is in the authorization header
   - Look for `"Authorization": "Bearer sk-..."` in headers
   - Full key will be visible in DEBUG mode

4. **Error Messages**: If API call fails, check error logs
   - `"error_type": "AuthenticationError"` indicates invalid API key
   - `"api_key_provided": false` indicates API key not passed
   - `"api_key_length": 0` indicates empty API key

## Log File Location

By default, logs are written to:
- **Console**: stdout/stderr with JSON formatting
- **File**: `logs/` directory (if configured)

## Best Practices

1. **Never commit `.env` with sensitive data** to version control
2. **Use DEBUG logging only in development**
3. **Always use production settings in production environments**
4. **Rotate log files regularly** to prevent disk space issues
5. **Monitor logs for security incidents** in production

## Related Documentation

- [Environment Configuration](../env.example)
- [Server Configuration](../README.md)
- [MCP Client Configuration](../docs/MCP_CLIENT.md)

