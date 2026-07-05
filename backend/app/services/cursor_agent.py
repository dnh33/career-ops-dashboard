"cursor CLI agent wrapper — runs tasks via cursor --print."
from __future__ import annotations

import asyncio
import os
import shutil
from pathlib import Path
from typing import AsyncGenerator


class CursorError(Exception):
    pass


class CursorAgent:
    def __init__(self, workdir: str | Path = Path("/opt/career-ops"), timeout: int = 300):
        self.workdir = Path(workdir)
        self.timeout = timeout
        self.mock_mode = os.environ.get("CURSOR_MOCK_MODE", "false").lower() == "true"

    async def run(self, prompt: str) -> str:
        """Run cursor and return full output."""
        if self.mock_mode:
            # Return a mock response for testing
            await asyncio.sleep(0.2)
            return "This is a mock response from the Cursor agent."

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

    async def run_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Run cursor and yield tokens as they arrive from stdout."""
        if self.mock_mode:
            # Yield some fake tokens for testing
            for token in ["Hello ", "this ", "is ", "a ", "mock ", "response. ", "The ", "quick ", "brown ", "fox ", "jumps ", "over ", "the ", "lazy ", "dog."]:
                await asyncio.sleep(0.05)  # simulate delay
                yield token
            return

        if not shutil.which("cursor"):
            raise CursorError("cursor CLI not found — run: npm install -g cursor")

        proc = await asyncio.create_subprocess_exec(
            "cursor", "--print", "--model", "auto", "--trust", prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.workdir),
        )

        try:
            # Read stdout line by line as it streams
            assert proc.stdout is not None
            async for line in proc.stdout:
                if line:
                    decoded = line.decode("utf-8", errors="ignore")
                    yield decoded

            # Wait for process to complete and check return code
            await asyncio.wait_for(proc.wait(), timeout=self.timeout)

            if proc.returncode != 0:
                assert proc.stderr is not None
                stderr_output = (await proc.stderr.read()).decode()[:500]
                raise CursorError(f"cursor exited {proc.returncode}: {stderr_output}")

        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            raise CursorError(f"cursor timed out after {self.timeout}s")