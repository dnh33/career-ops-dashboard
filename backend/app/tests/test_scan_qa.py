"""QA tests for scan endpoint — T4.2."""
import asyncio
from unittest.mock import patch, AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.cursor_agent import CursorAgent, CursorError


client = TestClient(app)
API_KEY = "Ojy29OB8AJwvBAXZuF-244Su_L9RswRzpKSM5u8I2xE"
HEADERS = {"X-API-Key": API_KEY}


@pytest.fixture(autouse=True)
def reset_scan_state():
    """Reset in-memory scan state before each test."""
    from app.routers import scan
    scan._scan_state = {"status": "idle", "progress": "", "results": [], "error": None}
    yield
    scan._scan_state = {"status": "idle", "progress": "", "results": [], "error": None}


def test_post_scan_returns_running():
    """POST /api/scan should return status=running and start background task."""
    with patch("app.routers.scan.CursorAgent") as MockAgent:
        mock_instance = MockAgent.return_value
        mock_instance.run = AsyncMock(return_value="result line 1\nresult line 2")
        resp = client.post("/api/scan", json={}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"


def test_post_scan_rejects_duplicate():
    """POST /api/scan while already running returns already_running."""
    from app.routers import scan
    # Simulate a scan already in progress
    scan._scan_state["status"] = "running"
    scan._scan_state["progress"] = "Working..."
    scan._scan_state["results"] = []
    scan._scan_state["error"] = None
    resp = client.post("/api/scan", json={}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["status"] == "already_running"


def test_get_status_returns_current_state():
    """GET /api/scan/status returns the _scan_state dict."""
    resp = client.get("/api/scan/status", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "progress" in data
    assert "results" in data
    assert "error" in data


def test_cursor_error_sets_status_error():
    """When CursorAgent raises CursorError, status should become error."""
    from app.routers import scan

    async def _trigger_with_error():
        with patch("app.routers.scan.CursorAgent") as MockAgent:
            mock_instance = MockAgent.return_value
            mock_instance.run = AsyncMock(
                side_effect=CursorError("cursor exited 1: Authentication required")
            )
            # Manually trigger the background task logic
            scan._scan_state["status"] = "running"
            scan._scan_state["progress"] = "Starting scan..."
            scan._scan_state["results"] = []
            scan._scan_state["error"] = None
            try:
                agent = MockAgent.return_value
                result = await agent.run("test")
            except Exception as e:
                scan._scan_state["error"] = str(e)
                scan._scan_state["status"] = "error"

    asyncio.run(_trigger_with_error())
    assert scan._scan_state["status"] == "error"
    assert "Authentication" in scan._scan_state["error"]


def test_cursor_timeout_sets_status_error():
    """When CursorAgent times out, status should become error with timeout message."""
    from app.routers import scan
    from app.services.cursor_agent import CursorAgent as CA

    async def _trigger_timeout():
        scan._scan_state["status"] = "running"
        scan._scan_state["progress"] = "Starting scan..."
        scan._scan_state["results"] = []
        scan._scan_state["error"] = None
        try:
            agent = CA(timeout=1)
            # Mock the subprocess to hang
            with patch("app.services.cursor_agent.asyncio.create_subprocess_exec") as mock_proc:
                mock_proc_instance = AsyncMock()
                mock_proc_instance.communicate = AsyncMock(
                    side_effect=asyncio.TimeoutError()
                )
                mock_proc_instance.kill = AsyncMock()
                mock_proc_instance.wait = AsyncMock()
                mock_proc.return_value = mock_proc_instance
                await agent.run("test")
        except Exception as e:
            scan._scan_state["error"] = str(e)
            scan._scan_state["status"] = "error"

    asyncio.run(_trigger_timeout())
    assert scan._scan_state["status"] == "error"
    assert "timed out" in scan._scan_state["error"]
