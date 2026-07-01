"""QA tests for output router — T6.2."""
from __future__ import annotations

import os
import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from pathlib import Path

# Ensure no API key in test env (dev mode = auth bypassed)
os.environ["CAREER_OPS_API_KEY"] = ""

from app.main import app
from app.config import OUTPUT_DIR


@pytest.fixture
def output_dir_with_pdf(tmp_path, monkeypatch):
    """Create a temp output dir with a test PDF."""
    pdf = tmp_path / "test_report.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake content")
    monkeypatch.setattr("app.config.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("app.routers.output.OUTPUT_DIR", tmp_path)
    return tmp_path, pdf


@pytest.fixture
def output_dir_empty(tmp_path, monkeypatch):
    """Empty output dir — no files."""
    monkeypatch.setattr("app.config.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("app.routers.output.OUTPUT_DIR", tmp_path)
    return tmp_path


def _client():
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


# ── Test 1: POST /api/output/generate with valid report_id ──────────────
@pytest.mark.asyncio
async def test_generate_pdf_success(output_dir_with_pdf):
    """POST /api/output/generate with valid report_id -> 200 + result."""
    mock_result = "PDF generated at output/report_123.pdf"
    # CursorAgent is imported inside generate_pdf(), so mock at module source
    with patch("app.services.cursor_agent.CursorAgent") as MockAgent:
        instance = MockAgent.return_value
        instance.run = AsyncMock(return_value=mock_result)
        async with _client() as c:
            resp = await c.post("/api/output/generate", json={"report_id": "123"})
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert data["status"] == "complete"
    assert "result" in data


@pytest.mark.asyncio
async def test_generate_pdf_invalid_report_id(output_dir_with_pdf):
    """POST /api/output/generate with non-numeric report_id -> 400."""
    async with _client() as c:
        resp = await c.post("/api/output/generate", json={"report_id": "abc"})
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}: {resp.text}"


@pytest.mark.asyncio
async def test_generate_pdf_missing_report_id(output_dir_with_pdf):
    """POST /api/output/generate with missing report_id -> 400."""
    async with _client() as c:
        resp = await c.post("/api/output/generate", json={})
    assert resp.status_code == 400


# ── Test 2: GET /api/output -> returns file list ────────────────────────
@pytest.mark.asyncio
async def test_list_output_with_files(output_dir_with_pdf):
    """GET /api/output -> returns file list with metadata."""
    tmp_path, pdf = output_dir_with_pdf
    async with _client() as c:
        resp = await c.get("/api/output")
    assert resp.status_code == 200
    data = resp.json()
    assert "files" in data
    assert len(data["files"]) == 1
    f = data["files"][0]
    assert f["filename"] == "test_report.pdf"
    assert f["id"] == "test_report"
    assert f["size_bytes"] > 0
    assert "created_at" in f


@pytest.mark.asyncio
async def test_list_output_empty(output_dir_empty):
    """GET /api/output with empty dir -> empty list."""
    async with _client() as c:
        resp = await c.get("/api/output")
    assert resp.status_code == 200
    assert resp.json()["files"] == []


# ── Test 3: GET /api/output/download/{file} -> PDF bytes ────────────────
@pytest.mark.asyncio
async def test_download_pdf_valid(output_dir_with_pdf):
    """GET /api/output/download/{file} -> PDF bytes."""
    async with _client() as c:
        resp = await c.get("/api/output/download/test_report.pdf")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF")


# ── Test 4: GET /api/output/download/..%2F..%2Fetc%2Fpasswd -> 400/403 ──
@pytest.mark.asyncio
async def test_download_path_traversal_encoded(output_dir_with_pdf):
    """Encoded path traversal ..%2F..%2Fetc%2Fpasswd -> 400 or 403."""
    async with _client() as c:
        # Use raw request to preserve %2F encoding
        req = httpx.Request("GET", "http://test/api/output/download/..%2F..%2Fetc%2Fpasswd")
        resp = await c.send(req)
    assert resp.status_code in (400, 403, 404), f"Expected 400/403/404, got {resp.status_code}"


# ── Test 5: GET /api/output/download/../../../etc/passwd -> 400/403 ─────
@pytest.mark.asyncio
async def test_download_path_traversal_raw(output_dir_with_pdf):
    """Raw path traversal ../../../etc/passwd -> 400 or 403."""
    async with _client() as c:
        # Send as percent-encoded so FastAPI decodes inside path param
        resp = await c.get("/api/output/download/..%2F..%2F..%2Fetc%2Fpasswd")
    assert resp.status_code in (400, 403, 404), f"Expected 400/403/404, got {resp.status_code}"


# ── Additional security edge cases ──────────────────────────────────────
@pytest.mark.asyncio
async def test_download_backslash_traversal(output_dir_with_pdf):
    r"""Backslash traversal ..\etc\passwd -> 400/403/404."""
    async with _client() as c:
        req = httpx.Request("GET", "http://test/api/output/download/..\\etc\\passwd")
        resp = await c.send(req)
    assert resp.status_code in (400, 403, 404)


@pytest.mark.asyncio
async def test_download_nonexistent_file(output_dir_with_pdf):
    """Non-existent file -> 404."""
    async with _client() as c:
        resp = await c.get("/api/output/download/nope.pdf")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_view_pdf_valid(output_dir_with_pdf):
    """GET /api/output/view/{file} -> inline PDF."""
    async with _client() as c:
        resp = await c.get("/api/output/view/test_report.pdf")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"


@pytest.mark.asyncio
async def test_view_path_traversal(output_dir_with_pdf):
    """View endpoint also blocks traversal."""
    async with _client() as c:
        req = httpx.Request("GET", "http://test/api/output/view/..%2F..%2Fetc%2Fpasswd")
        resp = await c.send(req)
    assert resp.status_code in (400, 403, 404)
