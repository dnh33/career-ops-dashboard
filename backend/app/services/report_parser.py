"""Parse career-ops report files and extract structured metadata from frontmatter.

Report filenames follow the pattern: {num}-{company-slug}.md
Frontmatter uses Markdown bold field names: **Field:** value

Recognized fields:
  - Score (e.g. "4.2/5" or "N/A")
  - Company
  - Role
  - Date (ISO date string)
  - Archetype (e.g. "AI Platform / LLMOps")
  - Legitimacy (High Confidence | Proceed with Caution | Suspicious)
  - URL (original job posting URL)
  - PDF (generated | not generated)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional


# Frontmatter pattern: **Field:** value  (field name may contain spaces, slashes)
FRONTMATTER_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.+)$", re.MULTILINE)

# Filename pattern: {num}-{slug}.md
FILENAME_RE = re.compile(r"^(\d+)-(.+)\.md$")


@dataclass
class ReportMeta:
    """Metadata extracted from a single report file."""

    id: str  # derived from filename prefix (e.g. "042")
    slug: str  # filename slug (e.g. "google-dublin")
    company: str = ""
    role: str = ""
    score: Optional[float] = None  # numeric score (1.0–5.0), None if N/A
    date: Optional[date] = None
    archetype: str = ""
    legitimacy: str = ""
    url: str = ""
    pdf: bool = False
    raw_frontmatter: dict[str, str] = field(default_factory=dict)

    @property
    def filename(self) -> str:
        return f"{self.id}-{self.slug}.md"


def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract all **Field:** value pairs from report text."""
    return {k.strip(): v.strip() for k, v in FRONTMATTER_RE.findall(text)}


def _parse_score(raw: str) -> Optional[float]:
    """Parse a score string like '4.2/5' or 'N/A'."""
    if not raw or raw.lower() in ("n/a", "na", "-"):
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", raw)
    if m:
        val = float(m.group(1))
        if 1.0 <= val <= 5.0:
            return val
    return None


def _parse_date(raw: str) -> Optional[date]:
    """Parse an ISO date string (YYYY-MM-DD)."""
    if not raw:
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", raw)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None


def _parse_pdf(raw: str) -> bool:
    """Check if PDF field indicates a generated PDF."""
    if not raw:
        return False
    return "not generated" not in raw.lower() and raw.strip() not in ("❌", "-", "no", "No")


def parse_report(filepath: Path) -> Optional[ReportMeta]:
    """Parse a single report file and return its metadata.

    Returns None if the file doesn't match the expected filename pattern.
    """
    if not filepath.exists() or not filepath.suffix == ".md":
        return None

    filename_match = FILENAME_RE.match(filepath.name)
    if not filename_match:
        return None

    report_id = filename_match.group(1)
    slug = filename_match.group(2)

    text = filepath.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    score = _parse_score(fm.get("Score", ""))
    report_date = _parse_date(fm.get("Date", ""))

    return ReportMeta(
        id=report_id,
        slug=slug,
        company=fm.get("Company", ""),
        role=fm.get("Role", ""),
        score=score,
        date=report_date,
        archetype=fm.get("Archetype", ""),
        legitimacy=fm.get("Legitimacy", ""),
        url=fm.get("URL", ""),
        pdf=_parse_pdf(fm.get("PDF", "")),
        raw_frontmatter=fm,
    )


def list_reports(reports_dir: Path) -> list[ReportMeta]:
    """Scan a directory for report files and return parsed metadata for each.

    Sorted by report ID (numeric) ascending.
    """
    if not reports_dir.exists() or not reports_dir.is_dir():
        return []

    reports: list[ReportMeta] = []
    for f in sorted(reports_dir.iterdir()):
        if f.is_file() and f.suffix == ".md":
            meta = parse_report(f)
            if meta:
                reports.append(meta)

    reports.sort(key=lambda r: int(r.id))
    return reports


def get_report(reports_dir: Path, report_id: str) -> Optional[ReportMeta]:
    """Find a report by its numeric ID (e.g. '042')."""
    if not reports_dir.exists() or not reports_dir.is_dir():
        return None

    for f in reports_dir.iterdir():
        if f.is_file() and f.suffix == ".md":
            m = FILENAME_RE.match(f.name)
            if m and m.group(1) == report_id:
                return parse_report(f)
    return None


def get_report_content(reports_dir: Path, report_id: str) -> Optional[str]:
    """Return the full markdown content of a report by ID."""
    if not reports_dir.exists() or not reports_dir.is_dir():
        return None

    for f in reports_dir.iterdir():
        if f.is_file() and f.suffix == ".md":
            m = FILENAME_RE.match(f.name)
            if m and m.group(1) == report_id:
                return f.read_text(encoding="utf-8")
    return None
