# brain-trust - AI-Powered Q&A and Plan Review MCP Server

🧠 **Your trusted brain trust for getting AI help with questions and plan reviews.**

A simple, powerful FastMCP server with just 3 tools that connect Cursor to OpenAI for intelligent question answering and plan analysis.

---

## 🎯 What is brain-trust?

brain-trust is a Model Context Protocol (MCP) server that gives your AI agents direct access to OpenAI for:

- **Asking questions** with optional context
- **Reviewing planning documents** with multiple analysis depths
- **Getting expert answers** tailored to your specific situation

Think of it as **phoning a friend** (OpenAI) when you need help!

---

## ✨ The 3 Simple Tools

### 1. 📞 `phone_a_friend`

Ask OpenAI any question, with optional context for better answers.

```python
# Simple question
phone_a_friend("What is Docker?")

# Context-aware question
phone_a_friend(
    question="Should we use microservices?",
    context="Team of 5 engineers, launching MVP in 3 months"
)
```

### 2. 📋 `review_plan`

Get AI-powered feedback on planning documents with structured analysis.

**Review Levels:**

- `quick` - Basic structure and completeness check
- `standard` - Detailed analysis with suggestions
- `comprehensive` - Deep analysis with alternatives
- `expert` - Professional-level review with best practices

```python
review_plan(
    plan_content="# Q4 2025 Roadmap\n...",
    review_level="comprehensive",
    context="Startup with $500K budget, need to launch in 6 months",
    focus_areas=["timeline", "resources", "risks"]
)
```

**Returns:**

- Overall score (0.0-1.0)
- Strengths (list)
- Weaknesses (list)
- Suggestions (list)
- Detailed feedback (text)

### 3. ❤️ `health_check`

Check server status and configuration.

```python
health_check()
# Returns: {status, timestamp, plan_reviews_count}
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key
- Docker (optional, but recommended)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd mcp-ask-questions

# Start the server (no API key needed)
docker-compose up -d

# Check logs
docker-compose logs -f
```

The server starts immediately without requiring an OpenAI API key. Configure the API key in your MCP client (see below).

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

---

## 🔧 Configure in Cursor

### Quick Install Button

<details>
<summary>Click to expand Cursor setup</summary>

#### Click the button to install:

[<img src="https://cursor.com/deeplink/mcp-install-dark.svg" alt="Install in Cursor">](https://cursor.com/en/install-mcp?name=brain-trust&config=eyJ1cmwiOiAiaHR0cDovL2xvY2FsaG9zdDo4MDAwL21jcCIsICJ0cmFuc3BvcnQiOiAiaHR0cCIsICJlbnYiOiB7Ik9QRU5BSV9BUElfS0VZIjogInlvdXJfb3BlbmFpX2FwaV9rZXlfaGVyZSJ9fQ==)

#### Or install manually:

Go to `Cursor Settings` -> `MCP` -> `Add new MCP Server`. Name it "brain-trust", use HTTP transport:

- **URL**: `http://localhost:8000/mcp`
- **Transport**: `http`
- **Environment Variables**: Add `OPENAI_API_KEY` with your OpenAI API key

</details>

### Add to `~/.cursor/mcp.json`

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

**How it works:**

- The `OPENAI_API_KEY` from the MCP client configuration is automatically passed to each tool call
- The server receives the API key with each request and uses it to authenticate with OpenAI
- Optional: You can override the model and max_tokens per tool call

**Important**: Make sure Docker is running and the server is started before using in Cursor!

---

## 💡 Usage Examples

### Example 1: Quick Question

Ask OpenAI directly:

```
Use phone_a_friend to ask: "What are Python best practices?"
```

### Example 2: Context-Aware Question

Get answers specific to your situation:

```
Use phone_a_friend with the question "How should we structure our tests?"
and context "We use FastAPI with pytest, SQLAlchemy, and Docker"
```

### Example 3: Plan Review

Get feedback on a planning document:

```
Use review_plan to review the file plans/compare-options-tool.md
with review_level "standard"
```

### Example 4: Comprehensive Plan Analysis

Get deep analysis with specific focus:

```
Use review_plan on plans/compare-options-tool.md with review_level "expert",
context "Team of 2 engineers, need to build quickly",
and focus_areas ["timeline", "implementation", "risks"]
```

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Cursor / AI    │
│     Agent       │
└────────┬────────┘
         │ MCP Protocol (HTTP)
         │
┌────────▼────────┐
│   brain-trust   │
│   MCP Server    │
│  (FastMCP)      │
└────────┬────────┘
         │ OpenAI API
         │
┌────────▼────────┐
│    OpenAI       │
│    (GPT-4)      │
└─────────────────┘
```

**Flow:**

1. Agent calls MCP tool with API key from MCP client config
2. brain-trust server receives request with API key via HTTP
3. Server creates OpenAI client with provided API key
4. Server formats prompt and calls OpenAI API
5. OpenAI returns AI-generated response
6. Server returns structured response to agent

---

## 🐳 Docker Setup

The server runs in Docker with:

- **FastMCP Server**: Python 3.12, running on port 8000
- **Nginx**: Reverse proxy for HTTP requests
- **Health Checks**: Every 30 seconds
- **Non-root User**: Security best practice

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
curl http://localhost:8000/health

# Stop services
docker-compose down
```

---

## 🛠️ Configuration

### Environment Variables

The server requires minimal configuration. Create a `.env` file if needed:

```bash
# Server Configuration
LOG_LEVEL=INFO                    # Default: INFO
PORT=8000                         # Default: 8000
```

**Note:** OpenAI API key is **NOT** required as an environment variable. The API key is passed directly from the MCP client with each tool call.

### MCP Client Configuration (Required)

Configure your OpenAI API key in the MCP client settings (e.g., Cursor's `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "brain-trust": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "env": {
        "OPENAI_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

**How it works:**

1. You configure the API key in your MCP client
2. The MCP client automatically passes the key to tool calls
3. The server uses the key to authenticate with OpenAI per-request
4. No API key storage on the server side

**Benefits:**

- ✅ No API keys in Docker containers or environment files
- ✅ Secure key management via MCP client
- ✅ Different clients can use different API keys
- ✅ Per-request authentication

---

## 📊 API Endpoints

When running locally:

- **MCP Endpoint**: `http://localhost:8000/mcp`
- **Health Check**: `http://localhost:8000/health`

Test the health endpoint:

```bash
curl http://localhost:8000/health
# Returns: {"status":"healthy","timestamp":"...","plan_reviews_count":0}
```

---

## 🧪 Testing

Test that the server is working:

```bash
# Check health
curl http://localhost:8000/health

# In Cursor, try:
# "Use phone_a_friend to ask: What is FastMCP?"
```

---

## 📁 Project Structure

```
mcp-ask-questions/
├── server.py              # Main MCP server with 3 tools
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-container orchestration
├── nginx.conf             # Reverse proxy config
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── fastmcp.json          # FastMCP deployment config
├── .env.example          # Environment variables template
├── README.md             # This file
├── FINAL_TOOLS.md        # Detailed tool documentation
├── SIMPLIFIED_TOOLS.md   # Simplification notes
└── plans/                # Planning documents
    ├── contextual-qa-mcp-server.md
    ├── technical-implementation.md
    ├── quick-start-guide.md
    └── compare-options-tool.md
```

---

## 🔒 Security

- ✅ **No API keys in Docker** - API keys are passed per-request from MCP client
- ✅ **No environment file secrets** - No `.env` file with API keys required
- ✅ **Per-request authentication** - Each request uses client-provided credentials
- ✅ **Non-root Docker user** - Runs as `mcpuser` in container
- ✅ **Input validation** - Pydantic models validate all inputs
- ✅ **Error handling** - Comprehensive error handling and logging
- ✅ **Client-side key management** - Keys managed securely by MCP client

---

## 🐛 Troubleshooting

### Server won't start

```bash
# Check if port 8000 is in use
lsof -i:8000

# View Docker logs
docker-compose logs -f
```

### Cursor can't connect

1. Verify server is running: `curl http://localhost:8000/health`
2. Check MCP config in `~/.cursor/mcp.json`
3. Restart Cursor after config changes
4. Ensure `OPENAI_API_KEY` is set in MCP client config

### OpenAI API errors

1. Verify API key is correct and active in `~/.cursor/mcp.json`
2. Check OpenAI account has credits
3. Ensure API key has proper permissions
4. View logs: `docker-compose logs -f`

### "API key required" errors

The API key must be configured in your **MCP client** (not in Docker):

1. Open `~/.cursor/mcp.json`
2. Add `OPENAI_API_KEY` to the `env` section
3. Restart Cursor
4. The API key is automatically passed with each tool call

### Tools not showing in Cursor

1. Restart Docker: `docker-compose restart`
2. Restart Cursor completely
3. Check MCP settings are correct

---

## 🚦 Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server locally (no API key needed for startup)
python server.py

# Server runs on http://localhost:8000
```

**Note:** The server starts without requiring an OpenAI API key. The API key is provided by the MCP client when calling tools.

### Making Changes

1. Edit `server.py` for tool changes
2. Rebuild Docker: `docker-compose up -d --build`
3. Restart Cursor to pick up changes

### Adding New Tools

See `plans/compare-options-tool.md` for an example of how to propose and plan new tools.

---

## 📚 Documentation

- **FINAL_TOOLS.md** - Complete tool documentation with examples
- **SIMPLIFIED_TOOLS.md** - Notes on simplification from original design
- **PARAMETER_DESCRIPTIONS_ADDED.md** - Parameter documentation details
- **plans/** - Detailed planning documents and proposals

---

## 🎯 Why brain-trust?

### Simple

- Only 3 tools to learn
- Direct, straightforward usage
- No complex context management

### Powerful

- Full OpenAI GPT-4 capabilities
- Context-aware answers
- Multiple review levels

### Practical

- Solves real problems (questions, plan reviews)
- Easy to integrate with Cursor
- Production-ready with Docker

### Extensible

- Easy to add new tools
- Clean, maintainable codebase
- Well-documented for contributions

---

## 🤝 Contributing

We welcome contributions! To add a new tool:

1. Create a plan in `plans/your-tool-name.md`
2. Implement the tool in `server.py`
3. Add tests and documentation
4. Submit a pull request

See `plans/compare-options-tool.md` for an example plan.

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Inspired by the Model Context Protocol specification
- Uses OpenAI's GPT-4 for intelligent responses

---

**Questions? Issues? Feedback?**

Open an issue or reach out! We're here to help. 🧠✨
