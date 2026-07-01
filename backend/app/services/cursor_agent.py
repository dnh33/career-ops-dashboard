"""Cursor CLI agent wrapper — runs tasks via cursor --print."""
from __future__ import annotations

import asyncio
import shutil
from pathlib import Path


class CursorError(Exception):
    pass


class CursorAgent:
    def __init__(self, workdir: str | Path = Path("/opt/career-ops"), timeout: int = 300):
        self.workdir = Path(workdir)
        self.timeout = timeout

    async def run(self, prompt: str) -> str:
        if not shutil.which("cursor"):
            raise CursorError("cursor CLI not found — run: npm install -g cursor")

        try:
            proc = await asyncio.create_subprocess_exec(
                "cursor", "--print", "--model", "auto", "--trust", prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workdir),
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout,
            )

            if proc.returncode != 0:
                raise CursorError(f"cursor exited {proc.returncode}: {stderr.decode()[:500]}")

            output = stdout.decode().strip()
            if not output:
                raise CursorError("cursor returned empty output")
            return output

        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            raise CursorError(f"cursor timed out after {self.timeout}s")
