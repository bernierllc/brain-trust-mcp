# Ask MCP - Hosted OpenAI MCP Server

🧠 **Connect your IDE to OpenAI for intelligent question answering and structured plan reviews.**

A hosted FastMCP server with 3 simple tools that connect your IDE directly to OpenAI. No local installation needed.

**🌐 [Visit ask-mcp.com](https://ask-mcp.com)** - Try it instantly in your browser with setup guides for 8+ IDEs!

---

## 🎉 What's New in v0.1.2

- ⭐ **DEEP_DIVE Review Level** - Technical FMEA-style analysis for implementation planning
- 📊 **Master Review Framework** - 10-point structured evaluation across all review levels
- 🔍 **Comprehensive Logging** - Full request/response tracing with environment-aware API key masking
- ✅ **Professional Test Suite** - 18 pytest tests with 92% code coverage
- 🎨 **Pre-commit Hooks** - Automated code quality with black, isort, flake8, mypy
- 🐳 **Enhanced Docker Config** - Environment variable passthrough for easier configuration
- 📖 **Complete Documentation** - Logging guide, testing guide, header configuration examples

See [Release Notes v0.1.2](./release_notes/RELEASE_NOTES_v0.1.2.md) for full details.

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

Get AI-powered feedback on planning documents using the **Master Review Framework** - a structured 10-point evaluation system.

**Master Review Framework Dimensions:**

- Structure & Organization
- Completeness
- Clarity
- Assumptions & Dependencies
- Risks
- Feasibility
- Alternatives
- Validation
- Stakeholders
- Long-term Sustainability

**Review Levels (Progressive Depth):**

- `quick` - Basic checklist (1-2 suggestions)
- `standard` - Standard analysis (2-3 questions)
- `comprehensive` - Detailed coverage (3-5 questions)
- `deep_dive` - **NEW!** Technical FMEA-style analysis (4-6 questions)
- `expert` - Professional enterprise-level review (5-7 strategic questions)

```python
# Deep technical review
review_plan(
    plan_content="# Q4 2025 Roadmap\n...",
    review_level="deep_dive",  # NEW technical level
    context="Startup with $500K budget, need to launch in 6 months",
    focus_areas=["scalability", "risks", "timeline"]
)

# Expert enterprise review
review_plan(
    plan_content="# Migration Plan\n...",
    review_level="expert",
    context="Fortune 500 company, 1M+ users"
)
```

**Returns:**

- Overall score (0.0-1.0)
- Strengths (list)
- Weaknesses (list)
- Suggestions (list)
- Detailed feedback (structured analysis)
- Review level used
- Timestamp

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

- The `OPENAI_API_KEY` from the MCP client configuration is set as an environment variable for the server
- The server reads the API key from the environment and uses it to authenticate with OpenAI
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

The server supports environment-based configuration. Create a `.env` file:

```bash
# Server Configuration
ENVIRONMENT=development           # development or production
LOG_LEVEL=DEBUG                  # DEBUG, INFO, WARNING, ERROR, CRITICAL
PORT=8000                        # Default: 8000

# Optional: For development/testing only
OPENAI_API_KEY=sk-...           # Only needed for local testing
```

**Logging Modes:**

**Development (DEBUG):**

- Full API keys visible in logs (for debugging)
- All request/response details logged
- Complete header information

**Production (INFO):**

- API keys masked (first 8 + last 4 chars only)
- Essential information only
- Reduced sensitive data logging

See `docs/LOGGING.md` for comprehensive logging documentation.

**Note:** OpenAI API key is **NOT** required as an environment variable for production. The API key is passed directly from the MCP client with each tool call.

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

### Quick Test

Test that the server is working:

```bash
# Check health
curl http://localhost:8000/health

# In Cursor, try:
# "Use phone_a_friend to ask: What is FastMCP?"
```

### Test Suite

Run the comprehensive pytest test suite:

```bash
# Run all tests (18 tests, ~95 seconds)
pytest tests/

# Run with coverage report (92% coverage)
pytest --cov=server --cov-report=term-missing tests/

# Run only unit tests (fast, no API calls)
pytest tests/test_logging.py

# Run only integration tests (real OpenAI API calls)
pytest tests/test_tools.py

# Run specific test
pytest tests/test_tools.py::TestPhoneAFriend::test_phone_a_friend_basic -v
```

**Test Coverage:**

- ✅ 18 tests total
- ✅ 8 unit tests (logging, utilities)
- ✅ 10 integration tests (real OpenAI API calls)
- ✅ 92% code coverage
- ✅ All MCP tools tested
- ✅ All 5 review levels tested

**Requirements:**

- Tests require `OPENAI_API_KEY` in `.env` file for integration tests
- Unit tests run without API key
- Tests automatically skip if API key not available

See `tests/README.md` for complete testing documentation.

---

## 📁 Project Structure

```
mcp-ask-questions/
├── server.py                    # Main MCP server with 3 tools
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-container orchestration
├── nginx.conf                   # Reverse proxy config
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration (black, isort, mypy)
├── fastmcp.json                # FastMCP deployment config
├── .env.example                # Environment variables template
├── README.md                   # This file
├── docs/                       # Documentation
│   ├── LOGGING.md             # Comprehensive logging guide
│   ├── HEADER_IMPLEMENTATION.md  # Header-based config guide
│   └── MCP_CLIENT_HEADERS.md  # Client configuration guide
├── tests/                      # Pytest test suite (92% coverage)
│   ├── conftest.py            # Shared fixtures
│   ├── test_tools.py          # Tool tests (10 tests)
│   ├── test_logging.py        # Logging tests (8 tests)
│   └── README.md              # Testing documentation
├── release_notes/             # Release notes
│   ├── RELEASE_NOTES_v0.1.2.md
│   └── RELEASE_NOTES_v0.1.1.md
├── examples/                   # Example implementations
│   └── server_with_headers.py # Header-based config example
└── plans/                      # Planning documents
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
# Create/activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Auto-activates in VS Code/Cursor workspace

# Install dependencies
pip install -r requirements.txt

# Run server locally
python server.py

# Server runs on http://localhost:8000
```

**Note:** The server starts without requiring an OpenAI API key. The API key is provided by the MCP client when calling tools.

### Code Quality

**Pre-commit Hooks:**

Automated code quality checks run on every commit:

```bash
# Pre-commit automatically runs:
→ black      # Code formatting
→ isort      # Import sorting
→ flake8     # Linting
→ mypy       # Type checking
```

Commits are blocked if any check fails. The hook is automatically set up in `.git/hooks/pre-commit`.

**Manual Quality Checks:**

```bash
# Format code
black server.py

# Sort imports
isort server.py

# Lint
flake8 server.py

# Type check
mypy server.py

# Run all checks
black server.py && isort server.py && flake8 server.py && mypy server.py
```

### Making Changes

1. Create a feature branch
2. Make your changes to `server.py`
3. Run tests: `pytest tests/`
4. Pre-commit hooks will run automatically on commit
5. Rebuild Docker: `docker-compose up -d --build`
6. Restart Cursor to pick up changes

### Adding New Tools

1. Create a plan in `plans/your-tool-name.md`
2. Implement the tool in `server.py` with `@mcp.tool()` decorator
3. Add tests in `tests/test_tools.py`
4. Update documentation
5. Submit a pull request

See `plans/compare-options-tool.md` for an example plan.

---

## 📚 Documentation

### Core Documentation

- **README.md** (this file) - Overview and quick start
- **docs/LOGGING.md** - Comprehensive logging system guide
- **docs/HEADER_IMPLEMENTATION.md** - Header-based configuration guide
- **docs/MCP_CLIENT_HEADERS.md** - Client configuration options
- **tests/README.md** - Testing documentation and examples

### Release Notes

- **release_notes/RELEASE_NOTES_v0.1.2.md** - Latest release (current)
- **release_notes/RELEASE_NOTES_v0.1.1.md** - Previous release

### Examples

- **examples/server_with_headers.py** - HTTP header configuration example

### Planning Documents

- **plans/** - Detailed planning documents and proposals
  - contextual-qa-mcp-server.md
  - technical-implementation.md
  - quick-start-guide.md
  - compare-options-tool.md

---

## ⭐ Features

### Master Review Framework

- **10-point structured evaluation** for comprehensive plan analysis
- **5 progressive review levels** from quick to expert
- **FMEA-style failure analysis** in deep_dive mode
- **Enterprise-grade reviews** with RACI, TCO, SLOs

### Comprehensive Logging

- **Full request/response tracing** for debugging
- **Environment-aware masking** (debug vs production)
- **5+ log events per request** with structured JSON output
- **API key validation** at every step

### Professional Testing

- **92% code coverage** with 18 pytest tests
- **10 integration tests** with real OpenAI API calls
- **Automatic skipping** if API key not available
- **Type-safe** with full mypy compliance

### Development Tools

- **Pre-commit hooks** enforce code quality automatically
- **Auto-activate venv** in VS Code/Cursor workspace
- **Docker support** for easy deployment
- **HTTP header config** support (optional)

---

## 🎯 Why brain-trust?

### Simple

- Only 3 tools to learn
- Direct, straightforward usage
- No complex context management
- Clear, comprehensive documentation

### Powerful

- Use your favorite GPT Model
- Context-aware answers
- 5 progressive review levels
- Master Review Framework with 10-point analysis

### Practical

- Solves real problems (questions, plan reviews)
- Easy to integrate with Cursor
- Production-ready with Docker
- 92% test coverage ensures reliability

### Extensible

- Easy to add new tools
- Clean, maintainable codebase
- Well-documented for contributions
- Professional testing infrastructure

---

## 🤝 Contributing

We welcome contributions! Here's how to contribute:

### Adding a New Tool

1. **Plan**: Create a plan in `plans/your-tool-name.md`
2. **Implement**: Add tool to `server.py` with `@mcp.tool()` decorator
3. **Test**: Add tests in `tests/test_tools.py`
4. **Document**: Update README and add to `docs/` if needed
5. **Quality**: Pre-commit hooks will run automatically
6. **Submit**: Create a pull request

See `plans/compare-options-tool.md` for an example plan.

### Code Standards

- **Python 3.12+** with type hints
- **Black** formatting (line length 88)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking
- **pytest** for testing (aim for >80% coverage)
- **Conventional commits** for commit messages

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=server tests/

# Pre-commit hooks run automatically
git commit -m "feat: add new tool"
```

### Documentation Standards

- Add docstrings to all public functions
- Update README.md for user-facing changes
- Add examples for new features
- Keep docs/ up to date
- Follow existing documentation style

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) - Fast, Pythonic MCP framework
- Inspired by the [Model Context Protocol](https://modelcontextprotocol.io/) specification
- Uses OpenAI's GPT-4 for intelligent responses
- Testing powered by [pytest](https://pytest.org/) and [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- Logging with [structlog](https://www.structlog.org/)
- Code quality with [black](https://black.readthedocs.io/), [isort](https://pycqa.github.io/isort/), [flake8](https://flake8.pycqa.org/), and [mypy](https://mypy-lang.org/)

Thanks to all contributors who provided feedback on the review framework and logging system!

---

## 📊 Project Stats

- **Version**: 0.1.2
- **Python**: 3.12+
- **Tools**: 3 (phone_a_friend, review_plan, health_check)
- **Review Levels**: 5 (quick, standard, comprehensive, deep_dive, expert)
- **Test Coverage**: 92% (18 tests)
- **Lines of Code**: ~650 (server.py)
- **Dependencies**: FastMCP, OpenAI, Pydantic, Structlog

---

## 🔗 Links

- **Repository**: https://github.com/bernierllc/brain-trust-mcp
- **Issues**: https://github.com/bernierllc/brain-trust-mcp/issues
- **FastMCP Docs**: https://gofastmcp.com
- **MCP Specification**: https://modelcontextprotocol.io/

---

**Questions? Issues? Feedback?**

Open an issue or reach out! We're here to help. 🧠✨
