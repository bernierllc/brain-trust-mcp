#!/usr/bin/env python3
"""
Contextual Q&A MCP Server with OpenAI integration and plan review capabilities.
"""

import json
import logging
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, cast

import openai
import structlog
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, Field
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND

# Get environment and log level from environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG" if ENVIRONMENT == "development" else "INFO")

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Set the log level
logging.basicConfig(level=LOG_LEVEL)
logger = structlog.get_logger()

# Initialize FastMCP server
mcp = FastMCP("brain-trust")

# Create HTTP app for custom routes/static assets
http_app = mcp.http_app()

# Serve static files from dist directory
dist_path = Path(__file__).parent / "dist"
if dist_path.exists():
    http_app.mount(
        "/assets", StaticFiles(directory=str(dist_path / "assets")), name="assets"
    )


def get_config_from_headers() -> Dict[str, Any]:
    """Extract configuration from HTTP headers."""
    headers = get_http_headers()

    config: Dict[str, Any] = {}

    # Read API key from header
    if api_key := headers.get("x-openai-api-key"):
        config["api_key"] = api_key

    # Read model from header
    if model := headers.get("x-openai-model"):
        config["model"] = model

    # Read max tokens from header
    if max_tokens_str := headers.get("x-openai-max-tokens"):
        try:
            config["max_tokens"] = int(max_tokens_str)
        except ValueError:
            logger.warning(f"Invalid max_tokens header: {max_tokens_str}")

    logger.debug(
        "Configuration from headers",
        has_api_key=bool(config.get("api_key")),
        api_key_length=len(config.get("api_key", "")),
        model=config.get("model"),
        max_tokens=config.get("max_tokens"),
    )

    return config


# Helper functions for logging
def mask_api_key(api_key: str) -> str:
    """Mask API key for logging in production."""
    if not api_key:
        return "None"
    if ENVIRONMENT == "production" or LOG_LEVEL != "DEBUG":
        return f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
    return api_key


def log_openai_request(
    model: str, messages: List[Dict[str, Any]], max_tokens: int, api_key: str
) -> None:
    """Log OpenAI request details."""
    logger.debug(
        "OpenAI API Request",
        environment=ENVIRONMENT,
        log_level=LOG_LEVEL,
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        api_key=mask_api_key(api_key),
        api_key_length=len(api_key) if api_key else 0,
        headers={
            "Authorization": f"Bearer {mask_api_key(api_key)}",
            "Content-Type": "application/json",
        },
    )


def log_openai_response(response: Any) -> None:
    """Log OpenAI response details."""
    logger.debug(
        "OpenAI API Response",
        environment=ENVIRONMENT,
        log_level=LOG_LEVEL,
        response_id=getattr(response, "id", None),
        model=getattr(response, "model", None),
        usage=getattr(response, "usage", None),
        choices_count=len(response.choices) if hasattr(response, "choices") else 0,
        response_headers={
            "content-type": "application/json",
        },
    )


def log_mcp_call(tool_name: str, **kwargs: Any) -> None:
    """Log incoming MCP tool call."""
    # Mask sensitive parameters
    safe_kwargs = kwargs.copy()
    if "api_key" in safe_kwargs:
        safe_kwargs["api_key"] = mask_api_key(safe_kwargs["api_key"])

    logger.debug(
        "MCP Tool Call Received",
        environment=ENVIRONMENT,
        log_level=LOG_LEVEL,
        tool_name=tool_name,
        parameters=safe_kwargs,
    )


# Data Models
class ReviewLevel(str, Enum):
    """Review levels for plan analysis."""

    QUICK = "quick"  # Basic structure and completeness
    STANDARD = "standard"  # Detailed analysis with suggestions
    COMPREHENSIVE = "comprehensive"  # Deep analysis with alternatives
    DEEP_DIVE = "deep_dive"  # Technical analysis with implementation considerations
    EXPERT = "expert"  # Professional-level review with best practices


class PlanReview(BaseModel):
    """Plan review result."""

    plan_id: str
    review_level: ReviewLevel
    overall_score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    detailed_feedback: str
    reviewed_at: datetime = Field(default_factory=datetime.now)


# In-memory storage for plan reviews
plan_reviews: Dict[str, PlanReview] = {}


# OpenAI Integration Tools
@mcp.tool()
async def phone_a_friend(
    question: Annotated[str, "The question to ask OpenAI"],
    context: Annotated[
        Optional[str],
        "Optional context information to provide background for the question",
    ] = None,
    model: Annotated[
        Optional[str], "OpenAI model to use (optional if set in headers)"
    ] = None,
    max_tokens: Annotated[
        Optional[int], "Maximum tokens for response (optional if set in headers)"
    ] = None,
) -> str:
    """Phone a friend (OpenAI) to get help with a question."""
    # Get configuration from headers
    header_config = get_config_from_headers()

    # Use parameters if provided, otherwise fall back to headers
    final_api_key = header_config.get("api_key")
    final_model = model or header_config.get("model", "gpt-4")
    final_max_tokens = max_tokens or header_config.get("max_tokens", 1000)

    # Validate API key is available
    if not final_api_key:
        raise ValueError("API key must be provided in X-OpenAI-API-Key header")

    # Log incoming MCP call
    log_mcp_call(
        "phone_a_friend",
        question=question[:100] if len(question) > 100 else question,
        context=context[:100] if context and len(context) > 100 else context,
        model=final_model,
        model_source="parameter" if model else "header",
        max_tokens=final_max_tokens,
        max_tokens_source="parameter" if max_tokens else "header",
    )

    # Build prompt with optional context
    if context:
        prompt = (
            f"Context: {context}\n\n"
            f"Question: {question}\n\n"
            f"Please provide a comprehensive answer."
        )
    else:
        prompt = f"Question: {question}\n\nPlease provide a comprehensive answer."

    messages = cast(
        List[ChatCompletionMessageParam], [{"role": "user", "content": prompt}]
    )

    try:
        # Create OpenAI client with API key from headers
        client = openai.OpenAI(api_key=final_api_key)

        # Log OpenAI request
        log_openai_request(
            final_model,
            [{"role": "user", "content": prompt}],
            final_max_tokens,
            final_api_key,
        )

        response = client.chat.completions.create(
            model=final_model,
            messages=messages,  # type: ignore[arg-type]
            max_tokens=final_max_tokens,
            temperature=0.3,
        )

        # Log OpenAI response
        log_openai_response(response)

        answer = response.choices[0].message.content
        if not answer:
            raise ValueError("Empty response from OpenAI")

        logger.info("Friend called successfully", question=question[:50])
        result: str = answer.strip()
        return result

    except Exception as e:
        logger.error(
            "Failed to phone a friend",
            error=str(e),
            error_type=type(e).__name__,
            api_key_provided=bool(final_api_key),
            api_key_length=len(final_api_key) if final_api_key else 0,
        )
        raise


# Plan Review Tool
@mcp.tool()
async def review_plan(
    plan_content: Annotated[str, "The full content of the plan document to review"],
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
        Optional[str], "OpenAI model to use (optional if set in headers)"
    ] = None,
    max_tokens: Annotated[
        Optional[int], "Maximum tokens for response (optional if set in headers)"
    ] = None,
) -> Dict[str, Any]:
    """
    Review a plan file and provide feedback based on the specified review level.

    Args:
        plan_content: The content of the plan file to review
        review_level: Level of review depth (quick, standard, comprehensive, deep_dive, expert)
        context: Optional context information about the project, team, or constraints
        plan_id: Optional identifier for the plan
        focus_areas: Optional list of specific areas to focus the review on
        model: OpenAI model to use (optional if set in headers, default: gpt-4)
        max_tokens: Maximum tokens for response (optional if set in headers, default: 2000)

    Returns:
        Dictionary containing review results and feedback
    """
    # Get configuration from headers
    header_config = get_config_from_headers()

    # Use parameters if provided, otherwise fall back to headers
    final_api_key = header_config.get("api_key")
    final_model = model or header_config.get("model", "gpt-4")
    final_max_tokens = max_tokens or header_config.get("max_tokens", 2000)

    # Validate API key is available
    if not final_api_key:
        raise ValueError("API key must be provided in X-OpenAI-API-Key header")

    # Log incoming MCP call
    log_mcp_call(
        "review_plan",
        plan_content_length=len(plan_content),
        plan_content_preview=(
            plan_content[:200] if len(plan_content) > 200 else plan_content
        ),
        review_level=review_level,
        context=context[:100] if context and len(context) > 100 else context,
        plan_id=plan_id,
        focus_areas=focus_areas,
        model=final_model,
        model_source="parameter" if model else "header",
        max_tokens=final_max_tokens,
        max_tokens_source="parameter" if max_tokens else "header",
    )

    # Generate plan ID if not provided
    if not plan_id:
        plan_id = f"plan_{int(datetime.now().timestamp())}"

    # Create review prompt based on level
    # All reviews follow the Master Review Framework with varying depth
    review_prompts = {
        ReviewLevel.QUICK: """
        Provide a quick review of this plan using the following framework:

        STRUCTURE & ORGANIZATION:
        - Is the plan logically structured and easy to follow?

        COMPLETENESS:
        - Are key sections present (objectives, scope, timeline)?

        CLARITY:
        - Any obvious ambiguities or "must-fix" clarity issues?

        ASSUMPTIONS & RISKS:
        - Any glaring unstated assumptions or obvious risks?

        Keep feedback concise, actionable, and in checklist form if possible.
        Provide 1-2 key improvement suggestions.
        """,
        ReviewLevel.STANDARD: """
        Provide a standard review of this plan using the following framework:

        STRUCTURE & ORGANIZATION:
        - Is the plan logically structured and easy to follow?

        COMPLETENESS:
        - Are all key sections present (objectives, scope, resources, risks, timeline, success criteria)?
        - Is there appropriate level of detail for each section?

        CLARITY:
        - Is the language unambiguous, readable, and accessible to stakeholders?

        ASSUMPTIONS & DEPENDENCIES:
        - Are hidden assumptions, constraints, or external dependencies called out?

        RISKS:
        - What risks or failure modes are unaddressed?

        FEASIBILITY:
        - Are timeline and resource estimates realistic?

        Provide specific suggestions and 2-3 clarifying questions the plan should answer.
        """,
        ReviewLevel.COMPREHENSIVE: """
        Provide a comprehensive review of this plan using the following framework:

        STRUCTURE & ORGANIZATION:
        - Is the plan logically structured and easy to follow?
        - Does it flow naturally from problem → solution → implementation?

        COMPLETENESS:
        - Are all key sections present and thoroughly developed (objectives, scope, resources, risks, timeline, success criteria)?
        - Is the level of detail appropriate for each section?

        CLARITY:
        - Is the language unambiguous, readable, and accessible to all stakeholders?
        - Are technical terms and concepts clearly explained?

        ASSUMPTIONS & DEPENDENCIES:
        - Are hidden assumptions, constraints, or external dependencies explicitly called out?
        - What implicit assumptions need to be validated?

        RISKS:
        - What risks, failure modes, or edge cases are unaddressed?
        - Are mitigation strategies defined for key risks?

        FEASIBILITY:
        - Are timeline and resource estimates realistic?
        - Is the plan testable and measurable?
        - Can success be validated objectively?

        ALTERNATIVES:
        - Have trade-offs and alternative approaches been considered?
        - Are design decisions justified?

        VALIDATION:
        - Does the plan define success criteria, KPIs, or metrics?
        - How will progress be tracked and measured?

        STAKEHOLDERS:
        - Are roles, responsibilities, and stakeholder impacts clear?

        LONG-TERM SUSTAINABILITY:
        - Does the plan account for scalability, maintainability, and adaptability?

        Provide detailed feedback with examples, alternatives, and 3-5 clarifying questions that expose potential blind spots.
        """,
        ReviewLevel.DEEP_DIVE: """
        Provide a deep-dive technical review of this plan using the following framework:

        STRUCTURE & ORGANIZATION:
        - Evaluate logical flow, section coherence, and information architecture
        - Assess whether structure supports understanding and execution

        COMPLETENESS:
        - Section-by-section completeness audit (objectives, scope, resources, risks, timeline, success criteria, rollout plan)
        - Identify missing technical details, specifications, or requirements

        CLARITY:
        - Evaluate technical precision and unambiguous language
        - Assess readability for both technical and non-technical stakeholders

        ASSUMPTIONS & DEPENDENCIES:
        - Identify ALL stated and unstated assumptions
        - Map out dependency chains and potential bottlenecks
        - Validate technical feasibility of each assumption

        RISKS:
        - Comprehensive risk analysis: technical, operational, security, performance
        - Failure mode analysis (FMEA-style): what could go wrong and when?
        - Edge cases, race conditions, and boundary conditions
        - Mitigation and rollback strategies for each major risk

        FEASIBILITY:
        - Detailed timeline realism check with critical path analysis
        - Resource allocation validation (team capacity, skills, budget)
        - Technical feasibility of proposed solutions
        - Testing strategy and validation approach

        ALTERNATIVES:
        - Compare against alternative technical approaches
        - Evaluate trade-offs (performance vs complexity, cost vs speed, etc.)
        - Justify architectural and design decisions

        VALIDATION:
        - Define measurable success criteria and KPIs
        - Specify testing, monitoring, and observability requirements
        - Outline validation checkpoints throughout implementation

        STAKEHOLDERS:
        - Map stakeholder roles, responsibilities, and approval gates
        - Identify communication touchpoints and escalation paths

        LONG-TERM SUSTAINABILITY:
        - Scalability analysis: how will this perform at 10x, 100x scale?
        - Maintainability: code quality, documentation, knowledge transfer
        - Adaptability: how easily can this evolve with changing requirements?
        - Operational considerations: deployment, monitoring, incident response

        Provide rigorous, technically detailed feedback with specific examples, actionable improvements, and 4-6 probing questions.
        """,
        ReviewLevel.EXPERT: """
        Provide an expert-level review of this plan using the Master Review Framework with professional rigor:

        STRUCTURE & ORGANIZATION:
        - Evaluate against industry-standard plan structures (PRDs, RFCs, technical specifications)
        - Assess information architecture and accessibility for diverse audiences

        COMPLETENESS:
        - Comprehensive audit of all sections (objectives, scope, resources, risks, timeline, success criteria, rollout, communication plan)
        - Evaluate against professional planning standards and best practices
        - Identify gaps that would concern executive stakeholders or auditors

        CLARITY:
        - Assess precision, unambiguity, and professional communication standards
        - Evaluate for multi-stakeholder accessibility (technical, business, executive)
        - Check for regulatory or compliance language requirements

        ASSUMPTIONS & DEPENDENCIES:
        - Exhaustive mapping of assumptions with validation requirements
        - Dependency analysis including external systems, teams, and third parties
        - Constraint analysis (technical, business, legal, compliance)
        - Market or competitive landscape assumptions

        RISKS:
        - Enterprise-level risk assessment (technical, operational, business, legal, reputational)
        - Comprehensive failure mode analysis with probability and impact assessment
        - Security, privacy, and compliance risks
        - Business continuity and disaster recovery considerations
        - Risk mitigation, transfer, acceptance strategies

        FEASIBILITY:
        - Multi-dimensional feasibility analysis: technical, operational, financial, organizational
        - Realistic timeline assessment with uncertainty ranges
        - Resource allocation optimization and capacity planning
        - Financial modeling and ROI analysis where applicable
        - Testability, measurability, and validation strategy

        ALTERNATIVES:
        - Comprehensive alternatives analysis with decision matrices
        - Trade-off evaluation across multiple dimensions (cost, time, quality, risk)
        - Competitive analysis and industry benchmarking
        - Build vs buy vs partner considerations

        VALIDATION:
        - Define SMART success criteria and KPIs aligned with business objectives
        - Comprehensive testing strategy (unit, integration, system, acceptance)
        - Monitoring, observability, and alerting requirements
        - Metrics dashboard and reporting cadence
        - Go/no-go decision criteria at each milestone

        STAKEHOLDERS:
        - Complete stakeholder mapping with RACI matrix
        - Communication plan with appropriate cadence and channels
        - Change management and stakeholder buy-in strategy
        - Executive reporting and governance structure

        LONG-TERM SUSTAINABILITY:
        - Scalability with specific load projections and capacity planning
        - Maintainability with documentation, knowledge transfer, and support plans
        - Adaptability and extensibility for future requirements
        - Total cost of ownership (TCO) analysis
        - Technical debt management strategy
        - Operational excellence: SLAs, SLOs, error budgets
        - Team sustainability: on-call rotation, burnout prevention

        Provide expert insights with industry context, citing best practices and standards where relevant.
        Suggest measurable improvements with business impact.
        Provide 5-7 strategic questions the leadership team should address before execution.
        """,
    }

    base_prompt = review_prompts[review_level]

    # Add focus areas if specified
    if focus_areas:
        areas = ", ".join(focus_areas)
        focus_text = f"\n\nFocus the review specifically on these areas: {areas}"
        base_prompt += focus_text

    # Add context if provided
    context_section = ""
    if context:
        context_section = f"\n\nAdditional Context:\n{context}\n"

    prompt = f"""
    {base_prompt}
    {context_section}
    Plan Content:
    {plan_content}

    Please provide your review in the following JSON format:
    {{
        "overall_score": 0.0-1.0,
        "strengths": ["strength1", "strength2", ...],
        "weaknesses": ["weakness1", "weakness2", ...],
        "suggestions": ["suggestion1", "suggestion2", ...],
        "detailed_feedback": "comprehensive feedback text"
    }}
    """

    messages = [{"role": "user", "content": prompt}]

    try:
        # Create OpenAI client with API key from headers
        client = openai.OpenAI(api_key=final_api_key)

        # Log OpenAI request
        log_openai_request(
            final_model, [dict(m) for m in messages], final_max_tokens, final_api_key
        )

        response = client.chat.completions.create(
            model=final_model,
            messages=messages,  # type: ignore[arg-type]
            max_tokens=final_max_tokens,
            temperature=0.3,
        )

        # Log OpenAI response
        log_openai_response(response)

        # Parse JSON response
        review_content = response.choices[0].message.content
        if not review_content:
            raise ValueError("Empty response from OpenAI")
        review_text: str = review_content.strip()

        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            start_idx = review_text.find("{")
            end_idx = review_text.rfind("}") + 1
            if start_idx != -1 and end_idx != 0:
                json_text = review_text[start_idx:end_idx]
                review_data = json.loads(json_text)
            else:
                # Fallback if no JSON found
                review_data = {
                    "overall_score": 0.7,
                    "strengths": ["Plan structure is present"],
                    "weaknesses": ["Unable to parse detailed review"],
                    "suggestions": ["Review the plan manually"],
                    "detailed_feedback": review_text,
                }
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            review_data = {
                "overall_score": 0.7,
                "strengths": ["Plan structure is present"],
                "weaknesses": ["Unable to parse detailed review"],
                "suggestions": ["Review the plan manually"],
                "detailed_feedback": review_text,
            }

        # Create plan review object
        plan_review = PlanReview(
            plan_id=plan_id,
            review_level=review_level,
            overall_score=review_data.get("overall_score", 0.7),
            strengths=review_data.get("strengths", []),
            weaknesses=review_data.get("weaknesses", []),
            suggestions=review_data.get("suggestions", []),
            detailed_feedback=review_data.get("detailed_feedback", review_text),
        )

        # Store the review
        plan_reviews[plan_id] = plan_review

        logger.info(
            "Plan reviewed",
            plan_id=plan_id,
            review_level=review_level,
            score=plan_review.overall_score,
        )

        reviewed_at_value: datetime = cast(
            datetime, getattr(plan_review, "reviewed_at")
        )
        reviewed_at_iso: str = reviewed_at_value.isoformat()
        return {
            "plan_id": plan_id,
            "review_level": review_level,
            "overall_score": plan_review.overall_score,
            "strengths": plan_review.strengths,
            "weaknesses": plan_review.weaknesses,
            "suggestions": plan_review.suggestions,
            "detailed_feedback": plan_review.detailed_feedback,
            "reviewed_at": reviewed_at_iso,
        }

    except Exception as e:
        logger.error(
            "Failed to review plan",
            error=str(e),
            error_type=type(e).__name__,
            plan_id=plan_id,
            api_key_provided=bool(final_api_key),
            api_key_length=len(final_api_key) if final_api_key else 0,
        )
        raise


# Health check endpoint
@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """Check server health and status."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "plan_reviews_count": len(plan_reviews),
    }


# REST API endpoints for interactive demo
class DemoRequest(BaseModel):
    """Request model for demo API endpoints."""

    question: Optional[str] = None
    context: Optional[str] = None
    plan_content: Optional[str] = None
    review_level: Optional[str] = "standard"
    focus_areas: Optional[List[str]] = None
    api_key: str


@mcp.custom_route("/api/demo/phone-a-friend", methods=["POST"])
async def demo_phone_a_friend(request: Request) -> JSONResponse:
    """REST API endpoint for phone_a_friend demo."""
    try:
        payload = await request.json()
        data = DemoRequest.model_validate(payload)

        if not data.question:
            raise HTTPException(status_code=400, detail="Question is required")
        if not data.api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        if data.context:
            prompt = (
                f"Context: {data.context}\n\n"
                f"Question: {data.question}\n\n"
                f"Please provide a comprehensive answer."
            )
        else:
            prompt = (
                f"Question: {data.question}\n\n"
                f"Please provide a comprehensive answer."
            )

        messages = cast(
            List[ChatCompletionMessageParam], [{"role": "user", "content": prompt}]
        )

        client = openai.OpenAI(api_key=data.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.3,
        )

        answer = response.choices[0].message.content
        if not answer:
            raise HTTPException(status_code=500, detail="Empty response from OpenAI")

        return JSONResponse(content={"answer": answer.strip()})

    except openai.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API key")
    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logger.error("Demo API error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@mcp.custom_route("/api/demo/review-plan", methods=["POST"])
async def demo_review_plan(request: Request) -> JSONResponse:
    """REST API endpoint for review_plan demo."""
    try:
        payload = await request.json()
        data = DemoRequest.model_validate(payload)

        if not data.plan_content:
            raise HTTPException(status_code=400, detail="Plan content is required")
        if not data.api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        review_level = ReviewLevel(data.review_level or "standard")

        review_prompts = {
            ReviewLevel.QUICK: "Provide a quick review focusing on structure and completeness.",
            ReviewLevel.STANDARD: "Provide a standard review covering key areas.",
            ReviewLevel.COMPREHENSIVE: "Provide a comprehensive review with detailed analysis.",
            ReviewLevel.DEEP_DIVE: "Provide a deep-dive technical review.",
            ReviewLevel.EXPERT: "Provide an expert-level professional review.",
        }

        prompt = f"""
        {review_prompts[review_level]}

        Plan Content:
        {data.plan_content}

        Please provide your review in JSON format:
        {{
            "overall_score": 0.0-1.0,
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "suggestions": ["suggestion1", "suggestion2"],
            "detailed_feedback": "comprehensive feedback text"
        }}
        """

        messages = cast(
            List[ChatCompletionMessageParam], [{"role": "user", "content": prompt}]
        )

        client = openai.OpenAI(api_key=data.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=2000,
            temperature=0.3,
        )

        review_content = response.choices[0].message.content
        if not review_content:
            raise HTTPException(status_code=500, detail="Empty response from OpenAI")

        review_text = review_content.strip()

        try:
            start_idx = review_text.find("{")
            end_idx = review_text.rfind("}") + 1
            if start_idx != -1 and end_idx != 0:
                json_text = review_text[start_idx:end_idx]
                review_data = json.loads(json_text)
            else:
                review_data = {
                    "overall_score": 0.7,
                    "strengths": ["Plan structure is present"],
                    "weaknesses": ["Unable to parse detailed review"],
                    "suggestions": ["Review the plan manually"],
                    "detailed_feedback": review_text,
                }
        except json.JSONDecodeError:
            review_data = {
                "overall_score": 0.7,
                "strengths": ["Plan structure is present"],
                "weaknesses": ["Unable to parse detailed review"],
                "suggestions": ["Review the plan manually"],
                "detailed_feedback": review_text,
            }

        return JSONResponse(content=review_data)

    except openai.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API key")
    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logger.error("Demo API error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@mcp.custom_route("/api/demo/health", methods=["GET"])
async def demo_health(_request: Request) -> JSONResponse:
    """REST API endpoint for health check demo."""
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "plan_reviews_count": len(plan_reviews),
        }
    )


@mcp.custom_route("/", methods=["GET"])
async def serve_homepage(_request: Request) -> FileResponse:
    """Serve the homepage."""
    index_path = dist_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return FileResponse("frontend/index.html")


# Container/infra health probe
@mcp.custom_route("/health", methods=["GET"])
async def health_route(_request: Request) -> JSONResponse:
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "plan_reviews_count": len(plan_reviews),
        }
    )


# Static asset fallback route (ensures assets are served even if mount is not applied)
@mcp.custom_route("/assets/{asset_path:path}", methods=["GET"])
async def serve_asset(_request: Request) -> Response:
    # Extract the matched path from the URL
    # Starlette injects it into scope; FastMCP passes through Request
    # Using request.url.path to compute relative path after "/assets/"
    url_path = _request.url.path
    prefix = "/assets/"
    if url_path.startswith(prefix):
        path = url_path.replace(prefix, "", 1)
    else:
        path = url_path.lstrip("/")
    asset_file = dist_path / "assets" / path
    if asset_file.is_file():
        return FileResponse(str(asset_file))
    return JSONResponse({"detail": "Not Found"}, status_code=HTTP_404_NOT_FOUND)


@mcp.custom_route("/favicon.ico", methods=["GET"])
async def favicon(_request: Request) -> Response:
    # Prefer SVG; many browsers accept SVG favicons
    svg_path = dist_path / "favicon.svg"
    if svg_path.is_file():
        return FileResponse(str(svg_path), media_type="image/svg+xml")
    # Fallback to built icon in frontend assets
    svg_src = Path(__file__).parent / "frontend" / "src" / "assets" / "favicon.svg"
    if svg_src.is_file():
        return FileResponse(str(svg_src), media_type="image/svg+xml")
    return JSONResponse({"detail": "Not Found"}, status_code=HTTP_404_NOT_FOUND)


@mcp.custom_route("/favicon.svg", methods=["GET"])
async def favicon_svg(_request: Request) -> Response:
    svg_path = dist_path / "favicon.svg"
    if svg_path.is_file():
        return FileResponse(str(svg_path), media_type="image/svg+xml")
    svg_src = Path(__file__).parent / "frontend" / "src" / "assets" / "favicon.svg"
    if svg_src.is_file():
        return FileResponse(str(svg_src), media_type="image/svg+xml")
    return JSONResponse({"detail": "Not Found"}, status_code=HTTP_404_NOT_FOUND)


# Server startup logging
logger.info(
    "MCP server initialized successfully",
    environment=ENVIRONMENT,
    log_level=LOG_LEVEL,
    debug_logging_enabled=(LOG_LEVEL == "DEBUG"),
    sensitive_data_logging=(ENVIRONMENT == "development" and LOG_LEVEL == "DEBUG"),
)

if __name__ == "__main__":
    # Run the server
    logger.info(
        "Starting MCP server",
        transport="http",
        host="0.0.0.0",
        port=8000,
        environment=ENVIRONMENT,
        log_level=LOG_LEVEL,
    )
    mcp.run(transport="http", host="0.0.0.0", port=8000)
