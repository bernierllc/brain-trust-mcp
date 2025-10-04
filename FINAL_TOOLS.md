# 🧠 brain-trust - Final Simple Design

## The 3 Essential Tools

brain-trust now has just **3 core tools** that do everything you need:

### 1. 📞 **phone_a_friend**

Ask OpenAI any question, with optional context.

```python
phone_a_friend(
    question: str,              # Required: Your question
    context: str | None = None  # Optional: Background information
) -> str
```

**Examples:**

```python
# Simple question
answer = phone_a_friend("What is Docker?")

# Context-aware question
answer = phone_a_friend(
    question="Should we add more health checks?",
    context="We run a FastMCP server in Docker with health checks every 30s"
)
```

---

### 2. 📋 **review_plan**

Get AI-powered feedback on planning documents.

```python
review_plan(
    plan_content: str,                      # Required: Plan to review
    review_level: ReviewLevel = "standard", # Optional: quick/standard/comprehensive/expert
    context: str | None = None,             # Optional: Project context
    plan_id: str | None = None,             # Optional: Plan identifier
    focus_areas: List[str] | None = None    # Optional: Specific focus areas
) -> Dict[str, Any]
```

**Returns:**

- `overall_score` (0.0-1.0)
- `strengths` (list)
- `weaknesses` (list)
- `suggestions` (list)
- `detailed_feedback` (text)

**Examples:**

```python
# Basic review
review = review_plan(
    plan_content="# Q4 Roadmap\n..."
)

# Comprehensive review with context
review = review_plan(
    plan_content="# Q4 Roadmap\n...",
    review_level="comprehensive",
    context="5-person startup, $500K budget, 6 month timeline",
    focus_areas=["timeline", "resources", "risks"]
)
```

---

### 3. ❤️ **health_check**

Check server status and OpenAI configuration.

```python
health_check() -> Dict[str, Any]
```

**Returns:**

- `status` - "healthy"
- `timestamp` - Current time
- `openai_configured` - True/False
- `plan_reviews_count` - Number of stored reviews

---

## What We Removed

### ❌ Removed 5 tools:

1. `create_context` - Context is now a direct parameter
2. `get_context` - No longer needed
3. `search_contexts` - No longer needed
4. `generate_questions` - Not needed for Q&A workflow
5. `contextual_qa_workflow` - Simplified into direct tool calls

### ✅ Result:

- **Before**: 8 complex tools with context management
- **After**: 3 simple, focused tools
- **Benefit**: 75% reduction in complexity!

---

## Complete Usage Examples

### Example 1: Quick Question

```python
# Just ask!
answer = phone_a_friend("What are Python best practices?")
```

### Example 2: Project-Specific Question

```python
# Add context for better answers
answer = phone_a_friend(
    question="How should we structure our API tests?",
    context="We use FastAPI with pytest, SQLAlchemy for database, and Docker for deployment"
)
```

### Example 3: Plan Review

```python
# Get feedback on a plan
review = review_plan(
    plan_content="""
    # Project Migration Plan
    ## Phase 1: Assessment
    - Review current architecture
    - Identify dependencies
    ## Phase 2: Implementation
    - Migrate services
    - Update documentation
    """,
    review_level="standard"
)

print(f"Score: {review['overall_score']}")
print(f"Strengths: {review['strengths']}")
print(f"Suggestions: {review['suggestions']}")
```

### Example 4: Contextual Plan Review

```python
# Review with project context
review = review_plan(
    plan_content="# API Redesign Plan\n...",
    context="Legacy monolith, 100K daily users, need zero downtime, team of 3 engineers",
    review_level="expert",
    focus_areas=["risks", "timeline", "resources"]
)
```

---

## Tool Comparison

| Tool               | Purpose              | OpenAI | Context Support |
| ------------------ | -------------------- | ------ | --------------- |
| **phone_a_friend** | Ask any question     | ✅ Yes | ✅ Optional     |
| **review_plan**    | Review planning docs | ✅ Yes | ✅ Optional     |
| **health_check**   | Server status        | ❌ No  | ❌ N/A          |

---

## Why This Design?

### ✅ **Simple**

- Only 3 tools to learn
- Direct, straightforward usage
- No context management overhead

### ✅ **Flexible**

- Add context when you need it
- Skip it when you don't
- Works for simple and complex scenarios

### ✅ **Focused**

- Each tool does one thing well
- No overlapping functionality
- Clear separation of concerns

### ✅ **Powerful**

- Full OpenAI capabilities
- Multiple review levels
- Optional context for better answers

---

## Migration from Old Version

### Old Way (Complex):

```python
# Step 1: Create context
ctx = create_context(title="Project", content="...")

# Step 2: Generate questions
questions = generate_questions(context_id=ctx)

# Step 3: Answer questions
for q in questions:
    answer = phone_a_friend(q, context_id=ctx)
```

### New Way (Simple):

```python
# Just ask directly!
answer = phone_a_friend(
    question="Your question here",
    context="Your project context..."
)
```

---

## Quick Reference

```python
# 1. Simple question
phone_a_friend("What is X?")

# 2. Question with context
phone_a_friend("What is X?", context="We use Y...")

# 3. Review plan
review_plan("# Plan content...")

# 4. Review with context
review_plan("# Plan...", context="Team of 5...", review_level="expert")

# 5. Check health
health_check()
```

---

## Next Steps

1. **Restart Cursor** to see the simplified tools
2. **Try phone_a_friend** with and without context
3. **Test review_plan** on your actual plans
4. **Share feedback** on what works!

---

**brain-trust: Your simple, powerful AI assistant for questions and plan reviews! 🧠**
