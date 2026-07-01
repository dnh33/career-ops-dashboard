"""Evaluate router -- POST /api/evaluate.

Flow (dual-brain):
  1. owl-alpha extracts company + assesses legitimacy (fast triage)
  2. If SCAM: short-circuit with warning, no Cursor call
  3. CursorAgent runs full A-G evaluation
  4. Validate + save with file lock

Accepts either:
  {"text": "<raw job description text>"}
  {"url": "<job posting URL>"}  (callers must fetch first, re-POST with text)
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, validator
from typing import Optional

from app.limiter import limiter
from app.services.evaluator import evaluate as do_evaluate

router = APIRouter(tags=["evaluate"])


class EvaluateRequest(BaseModel):
    text: Optional[str] = Field(None, description="Raw job description text")
    url: Optional[str] = Field(None, description="Job posting URL (not yet fetched)")
    target_role: Optional[str] = Field("FE-DEV", description="Target role: FE-DEV, AI-SDEV, AI-ENG, GENAI, ML-ENG")
    target_company: Optional[str] = Field(None, description="Optional company for company-specific tailoring")

    @validator("text")
    def _not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("text must be non-empty")
        return v

    @validator("target_role")
    def _valid_role(cls, v):
        valid_roles = {"FE-DEV", "AI-SDEV", "AI-ENG", "GENAI", "ML-ENG"}
        if v and v not in valid_roles:
            raise ValueError(f"target_role must be one of: {valid_roles}")
        return v


class LegitimacyInfo(BaseModel):
    tier: str = "uncertain"
    score: int = 3
    reasoning: str = ""


class EvaluateResponse(BaseModel):
    report: str
    company: str
    role: str
    report_path: str
    legitimacy: LegitimacyInfo
    scam_warning: bool = False
    market_score: Optional[int] = None
    market_grade: Optional[str] = None
    top_gaps: list[str] = []
    top_strengths: list[str] = []
    company_fit: Optional[dict] = None


@router.post("/evaluate", response_model=EvaluateResponse)
@limiter.limit("10/minute")
async def submit_evaluation(req: EvaluateRequest, request: Request):
    """Submit a JD text for dual-brain evaluation with market scoring."""
    if not req.text and not req.url:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'text' (job description) or 'url' (job posting URL).",
        )
    if not req.text:
        raise HTTPException(
            status_code=202,
            detail=(
                "URL input not fetched server-side. Retrieve the page text and re-POST "
                "with {'text': <extracted job description>}."
            ),
        )
    result = await do_evaluate(req.text, req.target_role, req.target_company)

    # Determine if this was a scam short-circuit
    leg = result.get("legitimacy", {})
    scam_warning = leg.get("tier", "") in {"likely_scam", "suspicious"}

    return EvaluateResponse(
        report=result["report"],
        company=result["company"],
        role=result.get("role", ""),
        report_path=result.get("report_path", ""),
        legitimacy=LegitimacyInfo(
            tier=leg.get("tier", "uncertain"),
            score=int(leg.get("score", 3)),
            reasoning=leg.get("reasoning", ""),
        ),
        scam_warning=scam_warning,
        market_score=result.get("market_score"),
        market_grade=result.get("market_grade"),
        top_gaps=result.get("top_gaps", []),
        top_strengths=result.get("top_strengths", []),
        company_fit=result.get("company_fit"),
    )
