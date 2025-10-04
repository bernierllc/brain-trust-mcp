# Contributing to brain-trust

🧠 Thank you for your interest in contributing to brain-trust! We welcome contributions from the community.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, Docker version)
- **Logs or error messages**
- **Screenshots** if applicable

### Suggesting Features

Feature requests are welcome! Please:

- **Check existing issues** to avoid duplicates
- **Describe the problem** you're trying to solve
- **Propose a solution** with as much detail as possible
- **Explain use cases** and benefits
- **Consider alternatives** you've thought about

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our code style
3. **Add tests** if applicable
4. **Update documentation** to reflect your changes
5. **Ensure tests pass** and code is formatted
6. **Write clear commit messages** following conventional commits
7. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Git

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/brain-trust.git
cd brain-trust

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black isort pylint flake8 mypy pytest
```

### Running Locally

```bash
# Set up environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Run server
python server.py

# Or with Docker
docker-compose up -d
```

### Testing

```bash
# Run linting
black server.py --check
isort server.py --check
pylint server.py
flake8 server.py

# Run type checking
mypy server.py

# Test with curl
curl http://localhost:8000/health
```

## Code Style Guidelines

### Python

- **Format**: Use `black` for formatting
- **Imports**: Use `isort` for import sorting
- **Linting**: Follow `pylint` and `flake8` guidelines
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Add docstrings to all public functions

### Formatting

```bash
# Format code
black server.py
isort server.py

# Check formatting
black server.py --check
isort server.py --check
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new compare_options tool
fix: resolve OpenAI timeout issue
docs: update README with new examples
refactor: simplify phone_a_friend logic
test: add tests for review_plan
chore: update dependencies
```

## Project Structure

```
brain-trust/
├── server.py              # Main MCP server
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-container setup
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
└── README.md             # Documentation
```

## Adding a New Tool

To add a new MCP tool:

1. **Create a plan** in `plans/your-tool-name.md` (see `plans/compare-options-tool.md` for example)
2. **Implement the tool** in `server.py`:
   ```python
   @mcp.tool()
   async def your_tool(
       param: Annotated[str, "Parameter description"]
   ) -> str:
       """Tool description."""
       # Implementation
   ```
3. **Add parameter descriptions** using `Annotated`
4. **Update README.md** with tool documentation
5. **Test thoroughly** before submitting PR

## Documentation

- Keep README.md up-to-date
- Add docstrings to new functions
- Update CHANGELOG.md for notable changes
- Include examples for new features

## Questions?

- **Open an issue** for questions
- **Start a discussion** for ideas
- **Check existing issues** for answers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to brain-trust! 🎉
