"""Tracker router — list and add job applications."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.config import DATA_DIR

router = APIRouter()

# Where the markdown tracker lives
APPLICATIONS_MD = DATA_DIR / "applications.md"

# The table columns
HEADER = "| # | Date | Company | Role | Score | Status | Applied | Link |"
SEPARATOR = "|---|------|---------|------|-------|--------|---------|------|"

VALID_STATUSES = {
    "Evaluated", "Applied", "Responded", "Interview",
    "Offer", "Rejected", "Discarded", "SKIP",
}


class TrackerEntry(BaseModel):
    number: int = Field(default=0, ge=0)
    date: str = ""
    company: str
    role: str
    score: Optional[float] = Field(None, ge=0, le=10)
    status: str = "Evaluated"
    applied: str | bool = ""
    link: str = ""

    def __init__(self, **data):
        if isinstance(data.get("applied"), bool):
            data["applied"] = "Yes" if data["applied"] else ""
        super().__init__(**data)


def _parse_row(line: str) -> Optional[TrackerEntry]:
    """Parse a single markdown table row into a TrackerEntry."""
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    if len(parts) < 5:
        return None
    try:
        number = int(parts[0])
    except ValueError:
        return None
    status = parts[5] if len(parts) > 5 and parts[5] in VALID_STATUSES else "Evaluated"
    score: Optional[float] = None
    if len(parts) > 4 and parts[4]:
        try:
            score = float(parts[4])
        except ValueError:
            score = None
    return TrackerEntry(
        number=number,
        date=parts[1] if len(parts) > 1 else "",
        company=parts[2] if len(parts) > 2 else "",
        role=parts[3] if len(parts) > 3 else "",
        score=score,
        status=status,
        applied=parts[6] if len(parts) > 6 else "",
        link=parts[7] if len(parts) > 7 else "",
    )


def _read_entries() -> list[TrackerEntry]:
    """Read all entries from applications.md. Returns empty list if missing."""
    if not APPLICATIONS_MD.exists():
        return []
    text = APPLICATIONS_MD.read_text(encoding="utf-8")
    entries: list[TrackerEntry] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if "Date" in line and "Company" in line:
            continue  # skip header row
        if re.match(r"^\|[-| ]+\|$", line):
            continue  # skip separator row
        entry = _parse_row(line)
        if entry:
            entries.append(entry)
    return entries


def _write_entries(entries: list[TrackerEntry]) -> None:
    """Write entries to applications.md in canonical markdown table format."""
    APPLICATIONS_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [HEADER, SEPARATOR]
    for e in entries:
        score_str = f"{e.score:.1f}" if e.score is not None else "-"
        lines.append(
            f"| {e.number} | {e.date} | {e.company} | {e.role} "
            f"| {score_str} | {e.status} | {e.applied} | {e.link} |"
        )
    APPLICATIONS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


@router.get("/tracker", tags=["tracker"])
async def tracker_list() -> dict:
    """List all applications as a JSON array."""
    entries = _read_entries()
    return {
        "items": [e.model_dump() for e in entries],
        "total": len(entries),
    }


@router.post("/tracker", tags=["tracker"], status_code=status.HTTP_201_CREATED)
async def tracker_add(entry: TrackerEntry) -> dict:
    """Add a new application entry."""
    if entry.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid status '{entry.status}'. Must be one of: {sorted(VALID_STATUSES)}",
        )

    entries = _read_entries()
    existing_numbers = {e.number for e in entries}

    # Auto-increment number if not specified or duplicate
    if entry.number in existing_numbers or entry.number == 0:
        entry.number = (max(existing_numbers) + 1) if existing_numbers else 1

    # Default date to today if not provided
    if not entry.date:
        entry.date = datetime.now().strftime("%Y-%m-%d")

    entries.append(entry)
    entries.sort(key=lambda e: e.number)
    _write_entries(entries)

    return {"ok": True, "entry": entry.model_dump(), "total": len(entries)}
