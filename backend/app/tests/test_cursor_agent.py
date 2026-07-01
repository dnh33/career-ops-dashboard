"""Tests for CursorAgent service."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.services.cursor_agent import CursorAgent, CursorError


@pytest.fixture
def agent():
    return CursorAgent(workdir="/tmp", timeout=5)


@pytest.mark.asyncio
async def test_run_success(agent: CursorAgent):
    """cursor --print returns output → returns stripped stdout."""
    fake_proc = AsyncMock()
    fake_proc.communicate = AsyncMock(return_value=(b"hello world\n", b""))
    fake_proc.returncode = 0

    with patch("shutil.which", return_value="/usr/bin/cursor"), \
         patch("asyncio.create_subprocess_exec", return_value=fake_proc) as mock_exec:
        result = await agent.run("test prompt")

    assert result == "hello world"
    mock_exec.assert_called_once_with(
        "cursor", "--print", "--model", "auto", "test prompt",
        stdout=-1, stderr=-1, cwd="/tmp",
    )


@pytest.mark.asyncio
async def test_run_nonzero_exit_raises(agent: CursorAgent):
    """cursor exits non-zero → raises CursorError with stderr snippet."""
    fake_proc = AsyncMock()
    fake_proc.communicate = AsyncMock(return_value=(b"", b"some error occurred"))
    fake_proc.returncode = 1

    with patch("shutil.which", return_value="/usr/bin/cursor"), \
         patch("asyncio.create_subprocess_exec", return_value=fake_proc):
        with pytest.raises(CursorError, match="cursor exited 1: some error occurred"):
            await agent.run("bad prompt")


@pytest.mark.asyncio
async def test_run_empty_output_raises(agent: CursorAgent):
    """cursor returns empty stdout → raises CursorError."""
    fake_proc = AsyncMock()
    fake_proc.communicate = AsyncMock(return_value=(b"   \n", b""))
    fake_proc.returncode = 0

    with patch("shutil.which", return_value="/usr/bin/cursor"), \
         patch("asyncio.create_subprocess_exec", return_value=fake_proc):
        with pytest.raises(CursorError, match="cursor returned empty output"):
            await agent.run("empty prompt")


@pytest.mark.asyncio
async def test_run_timeout_kills_process(agent: CursorAgent):
    """cursor exceeds timeout → process killed, raises CursorError."""
    fake_proc = AsyncMock()
    fake_proc.communicate = AsyncMock(side_effect=asyncio.TimeoutError())
    fake_proc.kill = MagicMock()
    fake_proc.wait = AsyncMock()

    with patch("shutil.which", return_value="/usr/bin/cursor"), \
         patch("asyncio.create_subprocess_exec", return_value=fake_proc):
        with pytest.raises(CursorError, match="cursor timed out after 5s"):
            await agent.run("slow prompt")

    fake_proc.kill.assert_called_once()
    fake_proc.wait.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_cursor_not_found_raises():
    """cursor binary missing → raises CursorError."""
    with patch("shutil.which", return_value=None):
        agent = CursorAgent(workdir="/tmp", timeout=5)
        with pytest.raises(CursorError, match="cursor CLI not found"):
            await agent.run("any prompt")
