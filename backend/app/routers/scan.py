"""Scan router — job board scanning endpoints."""

import asyncio
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional

from app.limiter import limiter
from app.services.cursor_agent import CursorAgent

router = APIRouter(tags=["scan"])

# In-memory scan state
_scan_state = {"status": "idle", "progress": "", "results": [], "error": None}


class ScanRequest(BaseModel):
    dry_run: bool = False
    company: Optional[str] = None
    verify: bool = False


@router.post("/scan")
@limiter.limit("3/minute")
async def trigger_scan(request: Request, req: ScanRequest = ScanRequest()):
    """Trigger a job board scan via the career-ops CLI."""
    if _scan_state["status"] == "running":
        return {"status": "already_running", "message": "Scan is already in progress"}

    _scan_state["status"] = "running"
    _scan_state["progress"] = "Starting scan..."
    _scan_state["results"] = []
    _scan_state["error"] = None

    # Run scan in background
    async def _run():
        try:
            agent = CursorAgent(timeout=600)
            result = await agent.run(
                "Run the career-ops scan mode. Scan configured job boards, "
                "find new postings, add them to data/pipeline.md. "
                "Return a summary of postings found."
            )
            _scan_state["results"] = result.strip().splitlines()
            _scan_state["status"] = "completed"
            _scan_state["progress"] = f"Found {len(_scan_state['results'])} results"
        except Exception as e:
            _scan_state["error"] = str(e)
            _scan_state["status"] = "error"

    asyncio.create_task(_run())
    return {"status": "running", "message": "Scan started"}


@router.get("/scan/status")
async def scan_status():
    """Get scan status/results."""
    return _scan_state


# ---- Maintenance tools (doctor, verify, dedup, merge, reconcile, liveness) ----

VALID_TOOLS = {
    "doctor":     {"cmd": ["./cops", "doctor"],     "desc": "Health check and diagnostics"},
    "verify":     {"cmd": ["./cops", "verify"],     "desc": "Verify data integrity"},
    "dedup":      {"cmd": ["./cops", "dedup"],      "desc": "Remove duplicate tracker entries"},
    "merge":      {"cmd": ["./cops", "merge"],      "desc": "Merge tracker entries"},
    "normalize":  {"cmd": ["./cops", "normalize"],  "desc": "Normalize status values"},
    "reconcile":  {"cmd": ["./cops", "reconcile"],  "desc": "Reconcile pipeline with tracker"},
    "liveness":   {"cmd": ["./cops", "liveness"],   "desc": "Check if postings are still live"},
    "patterns":   {"cmd": ["./cops", "patterns"],   "desc": "Analyze job market patterns"},
}


class ToolRunRequest(BaseModel):
    tool: str
    args: List[str] = []


@router.get("/tools")
async def list_tools():
    """List available maintenance tools."""
    return {
        "tools": [
            {"id": k, "description": v["desc"]}
            for k, v in VALID_TOOLS.items()
        ]
    }


@router.post("/tools/run")
@limiter.limit("5/minute")
async def run_tool(request: Request, req: ToolRunRequest):
    """Run a maintenance tool and return its output."""
    if req.tool not in VALID_TOOLS:
        raise HTTPException(status_code=422, detail=f"Unknown tool: {req.tool}")

    if req.args:
        raise HTTPException(status_code=400, detail="Args not accepted — tools run with fixed parameters")
    cmd = VALID_TOOLS[req.tool]["cmd"]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/opt/career-ops",
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
        return {
            "tool": req.tool,
            "exit_code": proc.returncode,
            "stdout": stdout.decode().strip(),
            "stderr": stderr.decode().strip(),
        }
    except asyncio.TimeoutError:
        return {"tool": req.tool, "exit_code": -1, "stdout": "", "stderr": "Timed out after 60s"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
