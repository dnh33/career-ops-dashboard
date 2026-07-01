"""Evaluator service — dual-brain evaluation pipeline.

Flow:
  1. owl-alpha extracts company + assesses legitimacy (cheap, fast)
  2. If SCAM: short-circuit with warning (no Cursor call)
  3. CursorAgent runs full A-G evaluation (expensive, thorough)
  4. Validate output (length >= 50, has A-G blocks)
  5. Save with file lock
  6. Return report
"""
import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from filelock import FileLock

import asyncio

from app.services.owl_alpha import extract_company, assess_legitimacy
from app.services.cursor_agent import CursorAgent, CursorError
from app.services.market_scorer import MarketScorer, _get_company_keywords

_HERMES_ENV = Path("/root/.hermes/.env")
if _HERMES_ENV.exists():
    load_dotenv(_HERMES_ENV)

_REPORT_LOCK = Path("/tmp/career-ops-report.lock")

# Legitimacy tiers that should short-circuit (no Cursor call)
_SCAM_TIERS = {"likely_scam", "suspicious"}

# CursorAgent timeout for full evaluation (seconds)
_CURSOR_TIMEOUT = 600


def career_ops_root() -> Path:
    env = os.getenv("CAREER_OPS_ROOT", "")
    if env:
        return Path(env)
    return Path("/opt/career-ops")


def _next_report_path(company_slug: str) -> Path:
    reports_dir = career_ops_root() / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    with FileLock(str(_REPORT_LOCK), timeout=10):
        existing = []
        for f in reports_dir.glob("[0-9][0-9][0-9]-*.md"):
            m = re.match(r"^(\d{3})-", f.name)
            if m:
                existing.append(int(m.group(1)))
        next_num = (max(existing) + 1) if existing else 1
        return reports_dir / f"{next_num:03d}-{company_slug}-{date.today().isoformat()}.md"


def _slugify(raw: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    return s or "unknown"


def load_cv() -> str:
    root = career_ops_root()
    return (root / "cv.md").read_text(encoding="utf-8") if (root / "cv.md").exists() else ""


def _build_cursor_prompt(jd_text: str, cv_text: str, company: str) -> str:
    return (
        f"Evaluate the following job description for the position at {company}.\n\n"
        "Produce a structured evaluation with blocks A-G:\n"
        "A) Role Summary\n"
        "B) Match with CV\n"
        "C) Level & Strategy\n"
        "D) Comp & Demand\n"
        "E) Customization Plan\n"
        "F) Interview Plan\n"
        "G) Legitimacy\n\n"
        "End with **Score:** X/5 and **Legitimacy:** [tier].\n"
        "Be specific, cite CV content, never invent metrics.\n\n"
        f"---\n\nHere is the CV:\n\n{cv_text}\n\n"
        f"---\n\nHere is the job description:\n\n{jd_text}"
    )


def _validate_report(report: str) -> None:
    """Raise RuntimeError if the report doesn't meet quality thresholds."""
    if not report or len(report.strip()) < 50:
        raise RuntimeError("Cursor returned empty or too-short response")
    has_blocks = sum(1 for c in "ABCDEFG" if f"**{c}" in report or f"## {c}" in report) >= 3
    if not has_blocks:
        raise RuntimeError("Cursor response missing A-G block structure")


async def evaluate(jd_text: str, target_role: str = "FE-DEV", target_company: Optional[str] = None) -> dict:
    """Dual-brain evaluation pipeline with market scoring.

    1. owl-alpha extracts company + assesses legitimacy
    2. If SCAM: short-circuit with warning
    3. CursorAgent runs full A-G evaluation
    4. Validate output
    5. Save with file lock
    6. Market scoring (new)
    7. Return report

    Returns dict with keys: report, company, role, report_path, legitimacy,
    market_score, market_grade, top_gaps, top_strengths, company_fit.
    On scam: returns report with scam warning, no Cursor call made.
    """
    # Phase 1: owl-alpha triage (cheap, fast)
    company, legitimacy = await asyncio.gather(
        extract_company(jd_text),
        assess_legitimacy(jd_text),
    )

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
        return {
            "report": scam_report,
            "company": company,
            "role": "",
            "report_path": "",
            "legitimacy": legitimacy,
            "market_score": None,
            "market_grade": None,
            "top_gaps": [],
            "top_strengths": [],
            "company_fit": None,
        }

    # Phase 3: CursorAgent full evaluation
    cv_text = load_cv()
    prompt = _build_cursor_prompt(jd_text, cv_text, company)

    agent = CursorAgent(timeout=_CURSOR_TIMEOUT)
    try:
        report = await agent.run(prompt)
    except CursorError as e:
        raise RuntimeError(f"Cursor evaluation failed: {e}") from e

    # Phase 4: Validate output
    _validate_report(report)

    # Phase 5: Save with file lock
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

    # Phase 6: Market scoring
    market_result = None
    try:
        rules_path = str(career_ops_root() / "data" / "research" / "cv-optimization-rules.md")
        scorer = MarketScorer(rules_path)
        market_result = scorer.score_cv(cv_text, target_role, target_company)
    except Exception:
        # Market scoring is non-blocking — fail gracefully
        market_result = None

    return {
        "report": report,
        "company": company,
        "role": "",
        "report_path": str(report_path),
        "legitimacy": legitimacy,
        "market_score": market_result.get("score") if market_result else None,
        "market_grade": market_result.get("label") if market_result else None,
        "top_gaps": market_result.get("gaps", [])[:5] if market_result else [],
        "top_strengths": market_result.get("strengths", [])[:5] if market_result else [],
        "company_fit": (
            {
                "company": target_company,
                "fit_score": market_result.get("breakdown", {}).get("company_fit", 0) if target_company else 0,
                "key_skills_match": _get_company_keywords(target_role, target_company) if target_company else [],
            }
            if target_company and market_result
            else None
        ),
    }
