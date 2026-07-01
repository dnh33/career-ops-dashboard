"""Owl-alpha service — cheap extraction and classification via OpenRouter API.

Uses the owl-alpha model (OpenRouter) for lightweight, fast, low-cost tasks:
- extract_company: pull company name from job description
- assess_legitimacy: classify job posting legitimacy
- suggest_role_title: extract/normalize the role title
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

_HERMES_ENV = Path("/root/.hermes/.env")
if _HERMES_ENV.exists():
    load_dotenv(_HERMES_ENV)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_URL = OPENROUTER_BASE_URL + "/chat/completions"
MODEL = "openrouter/owl-alpha"

_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "Career Ops Dashboard",
}


class OwlAlphaError(Exception):
    pass


async def _call(system_prompt: str, user_content: str, max_tokens: int = 500) -> str:
    if not OPENROUTER_API_KEY:
        raise OwlAlphaError(
            "OPENROUTER_API_KEY not found. Ensure /root/.hermes/.env contains OPENROUTER_API_KEY=<key>"
        )
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.1,
        "max_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(OPENROUTER_URL, json=payload, headers=_HEADERS)
        resp.raise_for_status()
        data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise OwlAlphaError(f"Unexpected OpenRouter response shape: {type(data).__name__}") from e


def _clean(raw: str) -> str:
    """Strip whitespace, quotes, and periods from both ends iteratively."""
    s = raw.strip()
    while True:
        stripped = s.strip().strip('"').strip("'").strip(".")
        if stripped == s:
            break
        s = stripped
    return s


async def extract_company(jd_text: str) -> str:
    """Extract company name from job description text.

    Returns the company name as a string, or "unknown" if not found.
    """
    system = (
        "You extract company names from job descriptions. "
        "Return ONLY the company name, nothing else. "
        "If no company name is found, return 'unknown'."
    )
    raw = await _call(system, jd_text, max_tokens=50)
    cleaned = _clean(raw)
    return cleaned if cleaned else "unknown"


async def assess_legitimacy(jd_text: str) -> dict:
    """Assess the legitimacy of a job posting.

    Returns a dict: {"tier": str, "score": int (1-5), "reasoning": str}
    Tiers: legitimate, likely_legitimate, uncertain, suspicious, likely_scam
    """
    system = (
        "You assess job posting legitimacy. "
        "Return JSON with keys: tier (one of: legitimate, likely_legitimate, "
        "uncertain, suspicious, likely_scam), score (1-5, 5=most legitimate), "
        "reasoning (1-2 sentences). "
        "Be skeptical of vague descriptions, unrealistic pay, and requests for money."
    )
    raw = await _call(system, jd_text, max_tokens=200)
    # Try to parse JSON from response
    text = raw.strip()
    # Handle markdown code fences
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        data = json.loads(text)
        return {
            "tier": data.get("tier", "uncertain"),
            "score": int(data.get("score", 3)),
            "reasoning": data.get("reasoning", ""),
        }
    except (json.JSONDecodeError, ValueError):
        # Fallback: return raw text as reasoning
        return {"tier": "uncertain", "score": 3, "reasoning": raw.strip()}


async def suggest_role_title(jd_text: str) -> str:
    """Extract or suggest the role title from a job description.

    Returns the role title as a string, or "unknown" if not found.
    """
    system = (
        "You extract job titles from descriptions. "
        "Return ONLY the role title (e.g. 'Senior Python Developer'), nothing else. "
        "Normalize to a standard professional title. "
        "If no clear title is found, return 'unknown'."
    )
    raw = await _call(system, jd_text, max_tokens=50)
    cleaned = _clean(raw)
    return cleaned if cleaned else "unknown"
