"""Tests for owl-alpha service."""
from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.services.owl_alpha import (
    OwlAlphaError,
    assess_legitimacy,
    extract_company,
    suggest_role_title,
)


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-123")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    # Re-apply env to module-level constant
    import app.services.owl_alpha as mod
    mod.OPENROUTER_API_KEY = "test-key-123"


# ── extract_company ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_extract_company_success(mock_env):
    """extract_company returns cleaned company name from API response."""
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = "Acme Corp"
        result = await extract_company("We at Acme Corp are hiring...")
    assert result == "Acme Corp"


@pytest.mark.asyncio
async def test_extract_company_strips_formatting(mock_env):
    """extract_company strips wrapping quotes and trailing periods."""
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = '"Globion".'
        result = await extract_company("Hiring at Globion...")
    assert result == "Globion"


@pytest.mark.asyncio
async def test_extract_company_empty_returns_unknown(mock_env):
    """extract_company returns 'unknown' when API returns empty string."""
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = "   "
        result = await extract_company("No company mentioned here")
    assert result == "unknown"


# ── assess_legitimacy ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_assess_legitimacy_parses_json(mock_env):
    """assess_legitimacy parses JSON response into structured dict."""
    response_data = {
        "tier": "legitimate",
        "score": 4,
        "reasoning": "Clear company info, realistic requirements, professional tone."
    }
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = json.dumps(response_data)
        result = await assess_legitimacy("Senior Dev at Google. Requirements: 5 years Python...")

    assert result["tier"] == "legitimate"
    assert result["score"] == 4
    assert "Clear company" in result["reasoning"]


@pytest.mark.asyncio
async def test_assess_legitimacy_handles_code_fences(mock_env):
    """assess_legitimacy strips markdown code fences from response."""
    response_data = {"tier": "suspicious", "score": 2, "reasoning": "Vague, too-good-true pay."}
    raw = '```json\n' + json.dumps(response_data) + '\n```'
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = raw
        result = await assess_legitimacy("Make $5000/week from home!")

    assert result["tier"] == "suspicious"
    assert result["score"] == 2


@pytest.mark.asyncio
async def test_assess_legitimacy_fallback_on_bad_json(mock_env):
    """assess_legitimacy falls back to raw text when JSON parse fails."""
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = "This looks like a scam because..."
        result = await assess_legitimacy("Send money to start working")

    assert result["tier"] == "uncertain"
    assert result["score"] == 3
    assert "scam" in result["reasoning"]


# ── suggest_role_title ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_suggest_role_title_success(mock_env):
    """suggest_role_title returns cleaned title from API response."""
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = "Senior Python Developer"
        result = await suggest_role_title("Looking for a senior Python dev with Django experience...")
    assert result == "Senior Python Developer"


@pytest.mark.asyncio
async def test_suggest_role_title_strips_formatting(mock_env):
    """suggest_role_title strips quotes and periods."""
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = '"Data Scientist".'
        result = await suggest_role_title("Hiring data scientist for ML team")
    assert result == "Data Scientist"


@pytest.mark.asyncio
async def test_suggest_role_title_empty_returns_unknown(mock_env):
    """suggest_role_title returns 'unknown' when API returns empty."""
    with patch("app.services.owl_alpha._call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = ""
        result = await suggest_role_title("No clear role here")
    assert result == "unknown"


# ── _call HTTP mock test ────────────────────────────────────────


@pytest.mark.asyncio
async def test_call_uses_owl_alpha_model(mock_env):
    """_call sends correct model name to OpenRouter."""
    captured_payload = {}

    async def fake_send(self, request, **kwargs):
        import httpx
        body = json.loads(request.content)
        captured_payload.update(body)
        return httpx.Response(
            200,
            request=request,
            json={"choices": [{"message": {"content": "Acme Corp"}}]},
        )

    with patch("httpx.AsyncClient.send", new=fake_send):
        from app.services.owl_alpha import _call
        result = await _call("extract company", "Hiring at Acme...")

    assert result == "Acme Corp"
    assert captured_payload["model"] == "openrouter/owl-alpha"
    assert captured_payload["max_tokens"] == 500
    assert len(captured_payload["messages"]) == 2
    assert captured_payload["messages"][0]["role"] == "system"
    assert captured_payload["messages"][1]["role"] == "user"


@pytest.mark.asyncio
async def test_call_no_api_key_raises(mock_env, monkeypatch):
    """_call raises OwlAlphaError when OPENROUTER_API_KEY is empty."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    import app.services.owl_alpha as mod
    mod.OPENROUTER_API_KEY = ""

    with pytest.raises(OwlAlphaError, match="OPENROUTER_API_KEY not found"):
        await mod._call("sys", "user")
