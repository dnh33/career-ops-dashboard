"""Pipeline router — URL inbox / pipeline endpoints.

Data lives in /opt/career-ops/data/pipeline.md using markdown sections:
  ## Pending   — URLs not yet evaluated
  ## Processed — URLs that have been evaluated or expired

Follows the same read/parse/write pattern as tracker.py.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator

from app.config import DATA_DIR
from app.services.cursor_agent import CursorAgent, CursorError

router = APIRouter(tags=["pipeline"])

PIPELINE_MD = DATA_DIR / "pipeline.md"

# Pending section columns: URL | Date Added | Source
PENDING_HEADER = "| URL | Date Added | Source |"
PENDING_SEP = "|---|---|---|"

# Processed section columns: URL | Date Added | Source | Status | Report # |
PROCESSED_HEADER = "| URL | Date Added | Source | Status | Report # |"
PROCESSED_SEP = "|---|---|---|---|---|"

VALID_STATUSES = {"pending", "evaluated", "expired"}
VALID_SOURCES = {"manual", "scan"}


class PipelineEntry(BaseModel):
    url: str
    date_added: str = ""
    source: str = "manual"
    status: str = "pending"
    report_number: Optional[int] = None

    @validator("url")
    def _valid_url(cls, v):
        if not v or not v.strip():
            raise ValueError("url must be non-empty")
        return v.strip()

    @validator("source")
    def _valid_source(cls, v):
        if v not in VALID_SOURCES:
            raise ValueError(f"source must be one of {VALID_SOURCES}")
        return v

    @validator("status")
    def _valid_status(cls, v):
        if v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        return v


class PipelineAddRequest(BaseModel):
    url: str
    source: str = "manual"

    @validator("url")
    def _valid_url(cls, v):
        if not v or not v.strip():
            raise ValueError("url must be non-empty")
        return v.strip()

    @validator("source")
    def _valid_source(cls, v):
        if v not in VALID_SOURCES:
            raise ValueError(f"source must be one of {VALID_SOURCES}")
        return v


class PipelineUpdateRequest(BaseModel):
    url: str
    status: str = "evaluated"
    report_number: Optional[int] = None

    @validator("url")
    def _valid_url(cls, v):
        if not v or not v.strip():
            raise ValueError("url must be non-empty")
        return v.strip()

    @validator("status")
    def _valid_status(cls, v):
        if v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}")
        return v


def _read_entries() -> list[PipelineEntry]:
    """Read all entries from pipeline.md. Returns empty list if missing."""
    if not PIPELINE_MD.exists():
        return []
    text = PIPELINE_MD.read_text(encoding="utf-8")
    entries: list[PipelineEntry] = []
    current_status = "pending"

    for line in text.splitlines():
        line = line.strip()
        if line == "## Pending":
            current_status = "pending"
            continue
        if line == "## Processed":
            current_status = "evaluated"
            continue
        if not line.startswith("|"):
            continue
        if "URL" in line and "Date Added" in line:
            continue  # header row
        if re.match(r"^\|[-| ]+\|$", line):
            continue  # separator row

        parts = [p.strip() for p in line.strip().strip("|").split("|")]

        if current_status == "pending" and len(parts) >= 3:
            entries.append(PipelineEntry(
                url=parts[0],
                date_added=parts[1] if len(parts) > 1 else "",
                source=parts[2] if len(parts) > 2 else "manual",
                status="pending",
            ))
        elif current_status == "evaluated" and len(parts) >= 4:
            entry_status = parts[3] if parts[3] in VALID_STATUSES else "evaluated"
            report_num = None
            if len(parts) > 4 and parts[4] and parts[4] != "-":
                try:
                    report_num = int(parts[4])
                except ValueError:
                    report_num = None
            entries.append(PipelineEntry(
                url=parts[0],
                date_added=parts[1] if len(parts) > 1 else "",
                source=parts[2] if len(parts) > 2 else "manual",
                status=entry_status,
                report_number=report_num,
            ))

    return entries


def _write_entries(entries: list[PipelineEntry]) -> None:
    """Write entries to pipeline.md in canonical markdown format."""
    PIPELINE_MD.parent.mkdir(parents=True, exist_ok=True)

    pending = [e for e in entries if e.status == "pending"]
    processed = [e for e in entries if e.status != "pending"]

    lines = ["## Pending"]
    if pending:
        lines.append(PENDING_HEADER)
        lines.append(PENDING_SEP)
        for e in pending:
            lines.append(f"| {e.url} | {e.date_added} | {e.source} |")
    else:
        lines.append("")
        lines.append("_No pending URLs._")

    lines.append("")
    lines.append("## Processed")
    if processed:
        lines.append(PROCESSED_HEADER)
        lines.append(PROCESSED_SEP)
        for e in processed:
            report_str = str(e.report_number) if e.report_number is not None else "-"
            lines.append(f"| {e.url} | {e.date_added} | {e.source} | {e.status} | {report_str} |")
    else:
        lines.append("")
        lines.append("_No processed URLs._")

    PIPELINE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


@router.get("/pipeline")
async def list_pipeline() -> dict:
    """List all pipeline entries (pending and processed)."""
    entries = _read_entries()
    return {
        "entries": [e.model_dump() for e in entries],
        "total": len(entries),
    }


@router.post("/pipeline", status_code=status.HTTP_201_CREATED)
async def add_pipeline_entry(data: PipelineAddRequest) -> dict:
    """Add a URL to the pipeline."""
    entries = _read_entries()

    # Dedup: check if URL already in pending
    for e in entries:
        if e.url == data.url and e.status == "pending":
            raise HTTPException(
                status_code=409,
                detail=f"URL already in pipeline (pending): {data.url}",
            )

    new_entry = PipelineEntry(
        url=data.url,
        date_added=datetime.now().strftime("%Y-%m-%d"),
        source=data.source,
        status="pending",
    )
    entries.append(new_entry)
    _write_entries(entries)

    return {"ok": True, "entry": new_entry.model_dump()}


@router.delete("/pipeline")
async def remove_pipeline_entry(url: str) -> dict:
    """Remove a URL from the pipeline."""
    entries = _read_entries()
    original_len = len(entries)
    entries = [e for e in entries if e.url != url]

    if len(entries) == original_len:
        raise HTTPException(
            status_code=404,
            detail=f"URL not found in pipeline: {url}",
        )

    _write_entries(entries)
    return {"ok": True, "removed": url}


@router.patch("/pipeline")
async def update_pipeline_entry(data: PipelineUpdateRequest) -> dict:
    """Update a pipeline entry's status (e.g., mark as evaluated)."""
    entries = _read_entries()
    found = False

    for e in entries:
        if e.url == data.url:
            e.status = data.status
            if data.report_number is not None:
                e.report_number = data.report_number
            found = True
            updated = e
            break

    if not found:
        raise HTTPException(
            status_code=404,
            detail=f"URL not found in pipeline: {data.url}",
        )

    _write_entries(entries)
    return {"ok": True, "entry": updated.model_dump()}


@router.post("/pipeline/evaluate-pending")
async def evaluate_pending():
    """Process all pending URLs through Cursor agent."""
    entries = _read_entries()
    pending = [e for e in entries if e.status == "pending"]
    if not pending:
        return {"status": "no_pending", "count": 0}

    agent = CursorAgent(timeout=600)
    try:
        result = await agent.run(
            f"Process these {len(pending)} pending job postings: "
            f"{json.dumps([e.model_dump() for e in pending])}. "
            f"For each: check liveness, evaluate live ones, "
            f"generate reports, update tracker. Skip dead URLs."
        )
        return {"status": "complete", "evaluated": len(pending), "result": result}
    except CursorError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Cursor agent failed: {exc}",
        )
