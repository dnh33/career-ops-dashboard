"""GET /api/stats — Dashboard statistics."""
from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import DATA_DIR, REPORTS_DIR
from app.services.tracker_parser import parse_applications

router = APIRouter()


class StatsResponse(BaseModel):
    total_applications: int
    total_reports: int
    avg_score: float | None
    active_pipeline_count: int
    last_scan_date: str | None


def _last_scan_date(reports_dir: Path) -> str | None:
    """Find the most recent report file modification time as last scan date."""
    if not reports_dir.exists():
        return None

    latest: datetime | None = None
    for f in reports_dir.iterdir():
        if f.is_file() and not f.name.startswith("."):
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if latest is None or mtime > latest:
                latest = mtime

    return latest.strftime("%Y-%m-%d") if latest else None


@router.get("/stats", response_model=StatsResponse, tags=["stats"])
async def get_stats() -> StatsResponse:
    """Return dashboard-wide statistics."""
    try:
        applications_file = DATA_DIR / "applications.md"
        summary = parse_applications(applications_file)

        reports = 0
        if REPORTS_DIR.exists():
            reports = sum(
                1 for f in REPORTS_DIR.rglob("*")
                if f.is_file() and not f.name.startswith(".")
            )

        return StatsResponse(
            total_applications=summary.total,
            total_reports=reports,
            avg_score=summary.avg_score,
            active_pipeline_count=summary.active_pipeline,
            last_scan_date=_last_scan_date(REPORTS_DIR),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/sse", tags=["stats"])
async def sse_status():
    """Server-Sent Events stream for real-time dashboard status."""

    async def event_generator():
        import json
        while True:
            payload = json.dumps({"status": "connected", "ts": datetime.utcnow().isoformat()})
            yield f"data: {payload}\n\n"
            await asyncio.sleep(5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
