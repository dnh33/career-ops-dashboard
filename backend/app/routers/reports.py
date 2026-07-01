"""Reports router — list and retrieve evaluation reports."""
from fastapi import APIRouter, HTTPException, Query

from app.config import REPORTS_DIR
from app.services.report_parser import (
    FILENAME_RE,
    ReportMeta,
    get_report,
    get_report_content,
    list_reports,
)

router = APIRouter(tags=["reports"])


def _to_dict(meta: ReportMeta) -> dict:
    """Convert a ReportMeta to a JSON-serializable dict for list responses."""
    return {
        "id": meta.id,
        "slug": meta.slug,
        "filename": meta.filename,
        "company": meta.company,
        "role": meta.role,
        "score": meta.score,
        "date": meta.date.isoformat() if meta.date else None,
        "archetype": meta.archetype,
        "legitimacy": meta.legitimacy,
        "url": meta.url,
        "pdf": meta.pdf,
    }


@router.get("/reports")
async def list_all_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """List all reports with pagination."""
    reports = list_reports(REPORTS_DIR)
    total = len(reports)
    start = (page - 1) * limit
    return {
        "reports": [_to_dict(r) for r in reports[start : start + limit]],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/reports/by-tracker/{tracker_number}")
async def get_report_by_tracker(tracker_number: int):
    """Find the report associated with a tracker entry number.

    Scans report frontmatter for a matching ``tracker_id`` field.
    Returns 404 if no report has been linked to this tracker entry yet.
    """
    if not REPORTS_DIR.exists():
        raise HTTPException(status_code=404, detail=f"No report for tracker #{tracker_number}")
    for f in REPORTS_DIR.iterdir():
        if f.suffix == ".md":
            content = f.read_text(encoding="utf-8")
            if f"tracker_id: {tracker_number}" in content:
                m = FILENAME_RE.match(f.name)
                if m:
                    return get_single_report(m.group(1))
    raise HTTPException(status_code=404, detail=f"No report for tracker #{tracker_number}")


@router.get("/reports/{report_id}")
async def get_single_report(report_id: str):
    """Get a single report's full content and metadata by ID.

    The report_id is the numeric prefix in the filename (e.g. "042").
    """
    meta = get_report(REPORTS_DIR, report_id)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")

    content = get_report_content(REPORTS_DIR, report_id)
    return {
        "id": meta.id,
        "slug": meta.slug,
        "filename": meta.filename,
        "company": meta.company,
        "role": meta.role,
        "score": meta.score,
        "date": meta.date.isoformat() if meta.date else None,
        "archetype": meta.archetype,
        "legitimacy": meta.legitimacy,
        "url": meta.url,
        "pdf": meta.pdf,
        "content": content,
    }
