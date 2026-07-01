"""Evaluator service -- calls OpenRouter API to produce an A-G evaluation report.

Takes job description text, assembles the system prompt from
career-ops/modes/_shared.md + career-ops/modes/oferta.md, loads the CV
from career-ops/cv.md, and calls OpenRouter's chat completions endpoint
via httpx async. The raw markdown report is saved to the career-ops
reports/ directory and returned.
"""
import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv

_HERMES_ENV = Path("/root/.hermes/.env")
if _HERMES_ENV.exists():
    load_dotenv(_HERMES_ENV)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "") or os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")
OPENROUTER_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1") + "/chat/completions"


def career_ops_root() -> Path:
    env = os.getenv("CAREER_OPS_ROOT", "")
    if env:
        return Path(env)
    return Path("/opt/career-ops")


def _next_report_path(company_slug: str) -> Path:
    reports_dir = career_ops_root() / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
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


def _extract_company(jd_text: str) -> str:
    for line in jd_text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.search(r"\bat\s+([A-Z][A-Za-z0-9& .]+?)(?:\s*(?:is|seeks|hiring|,|\.|\()))", line)
        if m:
            return m.group(1).strip()
        m = re.search(r"^([A-Z][A-Za-z0-9& .]{1,40})\s*[-][-]\s*", line)
        if m:
            return m.group(1).strip()
    return "company"


def load_system_prompt() -> str:
    root = career_ops_root()
    shared = (root / "modes" / "_shared.md").read_text(encoding="utf-8") if (root / "modes" / "_shared.md").exists() else ""
    oferta = (root / "modes" / "oferta.md").read_text(encoding="utf-8") if (root / "modes" / "oferta.md").exists() else ""
    return (shared + "\n\n---\n\n" + oferta).strip()


def load_cv() -> str:
    root = career_ops_root()
    return (root / "cv.md").read_text(encoding="utf-8") if (root / "cv.md").exists() else ""


async def _call_openrouter(system_prompt: str, user_content: str) -> str:
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY not found. Ensure /root/.hermes/.env contains OPENROUTER_API_KEY=<key>"
        )
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Career Ops Dashboard",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.4,
        "max_tokens": 8000,
    }
    async with httpx.AsyncClient(timeout=300.0) as client:
        resp = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected OpenRouter response shape: {type(data).__name__}") from e


async def evaluate(jd_text: str) -> dict:
    """Produce a full A-G evaluation for the given job description text.

    Returns dict with keys: report, company, role, report_path.
    """
    system_prompt =    cv_text = load_cv()

    user_content = (
        "Here is my CV:\n\n"
        + cv_text
        + "\n\n---\n\n"
        + "Here is the job description to evaluate against my CV:\n\n"
        + jd_text
    )

    report = await _call_openrouter(system_prompt, user_content)

    raw_company = _extract_company(jd_text)
    company_slug = _slugify(raw_company)
    report_path = _next_report_path(company_slug)

    file_body = (
        "# Evaluation: " + raw_company
        + "\n\n**Date:**" + date.today().isoformat()
        + "\n**URL:**\n**Archetype:**\n**Score:** ?/5"
        + "\n**Legitimacy:** Proceed with Caution\n**PDF:** pending\n\n---\n\n"
        + report
        + "\n"
    )
    report_path.write_text(file_body, encoding="utf-8")

    return {
        "report": report,
        "company": raw_company,
        "role": "",
        "report_path": str(report_path),
    }
