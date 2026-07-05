"""Evaluate router -- POST /api/evaluate.

Flow (dual-brain):
  1. owl-alpha extracts company + assesses legitimacy (fast triage)
  2. If SCAM: short-circuit with warning, no Cursor call
  3. CursorAgent runs full A-G evaluation
  4. Validate + save with file lock

Accepts either:
  {"text": "<raw job description text>"}
  , "url": "<job posting URL>"}  (callers must fetch first, re-POST with text)

SSE Streaming:
  GET /api/evaluate/{job_id}/stream -> text/event-stream
  Events: {type: "init|stage|token|complete|error", job_id, stage, progress, message, content?}
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, validator
from typing import Optional
import asyncio
from datetime import datetime

from app.limiter import limiter
from app.services.evaluator import evaluate as do_evaluate
from app.services.job_queue import get_job_queue, EvaluationJob, JobStatus, JobStage

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


@router.post("/evaluate/async")
@limiter.limit("10/minute")
async def submit_evaluation_async(req: EvaluateRequest, request: Request):
    """Submit a JD text for async evaluation - returns job_id immediately."""
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

    job_queue = get_job_queue()
    job = job_queue.create_job(
        jd_text=req.text,
        target_role=req.target_role,
        target_company=req.target_company,
    )

    # Start evaluation in background
    asyncio.create_task(_run_evaluation_job(job.job_id, req.text, req.target_role, req.target_company))

    return {"job_id": job.job_id, "status": "pending", "stream_url": f"/api/evaluate/{job.job_id}/stream"}


async def _run_evaluation_job(job_id: str, jd_text: str, target_role: str, target_company: Optional[str]):
    """Background task to run evaluation and update job status via SSE."""
    job_queue = get_job_queue()
    job = job_queue.get_job(job_id)
    if not job:
        return

    try:
        job.status = JobStatus.RUNNING
        job.started_at = datetime.utcnow().isoformat()
        job.stage = JobStage.OWL_ALPHA
        job.progress = 10
        job.message = "Analyzing job description with owl-alpha..."
        job_queue.update_job(job)

        # Import here to avoid circular imports
        from app.services.owl_alpha import extract_company, assess_legitimacy
        from app.services.cursor_agent import CursorAgent, CursorError
        from app.services.market_scorer import MarketScorer, _get_company_keywords
        from app.services.evaluator import _validate_report, _build_cursor_prompt, load_cv, _slugify, _next_report_path, _SCAM_TIERS
        from datetime import date
        from pathlib import Path
        from filelock import FileLock

        # Phase 1: owl-alpha triage
        company, legitimacy = await asyncio.gather(
            extract_company(jd_text),
            assess_legitimacy(jd_text),
        )

        job.company = company
        job.legitimacy = legitimacy
        job_queue.update_job(job)

        tier = legitimacy.get("tier", "uncertain")
        reasoning = legitimacy.get("reasoning", "")

        # Phase 2: Short-circuit on scam
        if tier in _SCAM_TIERS:
            scam_report = (
                f"# SCAM WARNING\n\n"
                f"**Company:** {company}\n"
                f"**Legitimacy Tier:** {tier}\n"
                f"**Reasoning:** {reasoning}\n\n"
                f"This job posting has been flagged as {tier}. "
                f"Full evaluation was skipped to avoid wasting resources.\n\n"
                f"**Recommendation:** Do not proceed with this posting."
            )
            job.report = scam_report
            job.status = JobStatus.COMPLETED
            job.stage = JobStage.COMPLETE
            job.progress = 100
            job.message = "Scam detected - evaluation skipped"
            job.completed_at = datetime.utcnow().isoformat()
            job.scam_warning = True
            job_queue.update_job(job)
            return

        # Phase 3: CursorAgent full evaluation
        job.stage = JobStage.CURSOR_EVAL
        job.progress = 30
        job.message = "Running Cursor evaluation..."
        job_queue.update_job(job)

        cv_text = load_cv()
        prompt = _build_cursor_prompt(jd_text, cv_text, company)

        agent = CursorAgent(timeout=600)
        try:
            # Run cursor and stream tokens
            report_parts = []
            async for token in agent.run_stream(prompt):
                report_parts.append(token)
                # Emit token event for real-time display
                job_queue.emit_token(job.job_id, token)
            report = "".join(report_parts)
        except CursorError as e:
            raise RuntimeError(f"Cursor evaluation failed: {e}") from e

        # Phase 4: Validate output
        job.stage = JobStage.VALIDATING
        job.progress = 70
        job.message = "Validating report..."
        job_queue.update_job(job)

        _validate_report(report)

        # Phase 5: Save with file lock
        job.stage = JobStage.SAVING
        job.progress = 80
        job.message = "Saving report..."
        job_queue.update_job(job)

        company_slug = _slugify(company)
        report_path = _next_report_path(company_slug)

        file_body = (
            "# Evaluation: " + company + "\n\n"
            + "**Date:** " + date.today().isoformat() + "\n"
            + "**URL:**\n**Archetype:**\n**Score:** ?/5\n"
            + f"**Legitimacy:** {tier}\n**PDF:** pending\n\n---\n\n"
            + report + "\n"
        )
        report_path.write_text(file_body, encoding="utf-8")

        job.report = report
        job.report_path = str(report_path)
        job.role = ""
        job_queue.update_job(job)

        # Phase 6: Market scoring
        job.stage = JobStage.MARKET_SCORING
        job.progress = 90
        job.message = "Computing market score..."
        job_queue.update_job(job)

        market_result = None
        try:
            rules_path = str(Path("/opt/career-ops") / "data" / "research" / "cv-optimization-rules.md")
            scorer = MarketScorer(rules_path)
            market_result = scorer.score_cv(cv_text, target_role, target_company)
        except Exception:
            market_result = None

        job.market_score = market_result.get("score") if market_result else None
        job.market_grade = market_result.get("label") if market_result else None
        job.top_gaps = market_result.get("gaps", [])[:5] if market_result else []
        job.top_strengths = market_result.get("strengths", [])[:5] if market_result else []
        job.company_fit = (
            {
                "company": target_company,
                "fit_score": market_result.get("breakdown", {}).get("company_fit", 0) if target_company else 0,
                "key_skills_match": _get_company_keywords(target_role, target_company) if target_company else [],
            }
            if target_company and market_result
            else None
        )

        # Complete
        job.status = JobStatus.COMPLETED
        job.stage = JobStage.COMPLETE
        job.progress = 100
        job.message = "Evaluation complete"
        job.completed_at = datetime.utcnow().isoformat()
        job_queue.update_job(job)

    except Exception as e:
        job.status = JobStatus.FAILED
        job.error = str(e)
        job.message = f"Evaluation failed: {e}"
        job.completed_at = datetime.utcnow().isoformat()
        job_queue.update_job(job)


@router.get("/evaluate/{job_id}/stream")
async def stream_evaluation(job_id: str):
    """SSE stream for evaluation job progress."""
    job_queue = get_job_queue()
    job = job_queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator():
        async for event in job_queue.stream_events(job_id):
            yield event

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/evaluate/{job_id}/status")
async def get_job_status(job_id: str):
    """Get job status for polling fallback."""
    job_queue = get_job_queue()
    job = job_queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_dict()
