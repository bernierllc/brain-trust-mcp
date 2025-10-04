#!/usr/bin/env python3
"""
Contextual Q&A MCP Server with OpenAI integration and plan review capabilities.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Dict, List, Optional

import openai
import structlog
from fastmcp import FastMCP
from pydantic import BaseModel, Field

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

logger = structlog.get_logger()

# Initialize FastMCP server
mcp = FastMCP("brain-trust")

# Note: OpenAI client is created per-request with API key from tool parameters


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
    api_key: Annotated[str, "OpenAI API key for authentication"],
    context: Annotated[
        Optional[str],
        "Optional context information to provide background for the question",
    ] = None,
    model: Annotated[str, "OpenAI model to use"] = "gpt-4",
    max_tokens: Annotated[int, "Maximum tokens for response"] = 1000,
) -> str:
    """Phone a friend (OpenAI) to get help with a question."""
    # Create OpenAI client with provided API key
    client = openai.OpenAI(api_key=api_key)

    # Build prompt with optional context
    if context:
        prompt = (
            f"Context: {context}\n\n"
            f"Question: {question}\n\n"
            f"Please provide a comprehensive answer."
        )
    else:
        prompt = f"Question: {question}\n\nPlease provide a comprehensive answer."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.3,
        )

        answer = response.choices[0].message.content
        if not answer:
            raise ValueError("Empty response from OpenAI")

        logger.info("Friend called successfully", question=question[:50])
        result: str = answer.strip()
        return result

    except Exception as e:
        logger.error("Failed to phone a friend", error=str(e))
        raise


# Plan Review Tool
@mcp.tool()
async def review_plan(
    plan_content: Annotated[str, "The full content of the plan document to review"],
    api_key: Annotated[str, "OpenAI API key for authentication"],
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
    model: Annotated[str, "OpenAI model to use"] = "gpt-4",
    max_tokens: Annotated[int, "Maximum tokens for response"] = 2000,
) -> Dict[str, Any]:
    """
    Review a plan file and provide feedback based on the specified review level.

    Args:
        plan_content: The content of the plan file to review
        api_key: OpenAI API key for authentication
        review_level: Level of review depth (quick, standard, comprehensive, deep_dive, expert)
        context: Optional context information about the project, team, or constraints
        plan_id: Optional identifier for the plan
        focus_areas: Optional list of specific areas to focus the review on
        model: OpenAI model to use (default: gpt-4)
        max_tokens: Maximum tokens for response (default: 2000)

    Returns:
        Dictionary containing review results and feedback
    """
    # Create OpenAI client with provided API key
    client = openai.OpenAI(api_key=api_key)

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

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.3,
        )

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

        return {
            "plan_id": plan_id,
            "review_level": review_level,
            "overall_score": plan_review.overall_score,
            "strengths": plan_review.strengths,
            "weaknesses": plan_review.weaknesses,
            "suggestions": plan_review.suggestions,
            "detailed_feedback": plan_review.detailed_feedback,
            "reviewed_at": plan_review.reviewed_at.isoformat(),
        }

    except Exception as e:
        logger.error("Failed to review plan", error=str(e), plan_id=plan_id)
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


# Server startup logging
logger.info("MCP server initialized successfully")

if __name__ == "__main__":
    # Run the server
    mcp.run(transport="http", host="0.0.0.0", port=8000)
