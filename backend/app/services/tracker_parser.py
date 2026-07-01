"""Parse data/applications.md into structured records.

Format (markdown table):
| # | Date | Company | Role | Score | Status | PDF | Report | Notes |

Statuses: Evaluated, Applied, Responded, Interview, Offer, Rejected, Discarded, SKIP
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# Active pipeline statuses — applications still in play
ACTIVE_STATUSES = {"Evaluated", "Applied", "Responded", "Interview"}

ALL_STATUSES = {
    "Evaluated", "Applied", "Responded", "Interview",
    "Offer", "Rejected", "Discarded", "SKIP",
}


@dataclass
class Application:
    number: int
    date: str
    company: str
    role: str
    score: Optional[float]
    status: str
    has_pdf: bool
    has_report: bool
    notes: str = ""


@dataclass
class TrackerSummary:
    total: int
    active_pipeline: int
    avg_score: Optional[float]
    by_status: dict[str, int]
    applications: list[Application] = field(default_factory=list)


def parse_applications(path: Path) -> TrackerSummary:
    """Parse applications.md and return a summary.

    Returns an empty summary if the file doesn't exist or has no data rows.
    """
    if not path.exists():
        return _empty_summary()

    text = path.read_text(encoding="utf-8")
    lines = text.strip().splitlines()

    applications: list[Application] = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Skip header and separator rows
        if re.match(r"^\|\s*#?\s*\|", line) or re.match(r"^\|[-: ]+\|$", line):
            if "---" in line or not any(c.isalpha() for c in line.replace("|", "")):
                continue
        # Skip the header row (contains "Date", "Company", etc.)
        if "Date" in line and "Company" in line and "Role" in line:
            continue
        # Skip separator rows
        if re.match(r"^\|[-\s|]+\|$", line):
            continue

        parts = [p.strip() for p in line.split("|")]
        # First and last are empty due to leading/trailing |
        parts = [p for p in parts if p != "" or parts.index(p) not in (0, len(parts) - 1)]
        # Re-split properly
        parts = [p.strip() for p in line.strip("|").split("|")]

        if len(parts) < 6:
            continue

        try:
            number = int(parts[0])
        except (ValueError, IndexError):
            continue

        date = parts[1] if len(parts) > 1 else ""
        company = parts[2] if len(parts) > 2 else ""
        role = parts[3] if len(parts) > 3 else ""

        score: Optional[float] = None
        if len(parts) > 4 and parts[4]:
            try:
                score = float(parts[4])
            except ValueError:
                score = None

        status = parts[5] if len(parts) > 5 else "Evaluated"
        if status not in ALL_STATUSES:
            status = "Evaluated"

        has_pdf = len(parts) > 6 and parts[6].strip() not in ("", "-", "No", "no")
        has_report = len(parts) > 7 and parts[7].strip() not in ("", "-", "No", "no")
        notes = parts[8] if len(parts) > 8 else ""

        applications.append(Application(
            number=number,
            date=date,
            company=company,
            role=role,
            score=score,
            status=status,
            has_pdf=has_pdf,
            has_report=has_report,
            notes=notes,
        ))

    return _summarize(applications)


def _summarize(applications: list[Application]) -> TrackerSummary:
    if not applications:
        return _empty_summary()

    scores = [a.score for a in applications if a.score is not None]
    avg_score = round(sum(scores) / len(scores), 2) if scores else None

    active = sum(1 for a in applications if a.status in ACTIVE_STATUSES)

    by_status: dict[str, int] = {}
    for a in applications:
        by_status[a.status] = by_status.get(a.status, 0) + 1

    return TrackerSummary(
        total=len(applications),
        active_pipeline=active,
        avg_score=avg_score,
        by_status=by_status,
        applications=applications,
    )


def _empty_summary() -> TrackerSummary:
    return TrackerSummary(
        total=0,
        active_pipeline=0,
        avg_score=None,
        by_status={},
        applications=[],
    )
