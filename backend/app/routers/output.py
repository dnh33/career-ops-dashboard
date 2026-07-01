"""Output router — PDF listing, generation, download, and view endpoints."""

from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.config import OUTPUT_DIR

router = APIRouter(tags=["output"])


def _safe_path(filename: str, base_dir: Path) -> Path:
    """Reject path traversal; ensure target is within base_dir."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    target = (base_dir / filename).resolve()
    if not target.is_relative_to(base_dir.resolve()):
        raise HTTPException(status_code=403, detail="Path traversal detected")
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return target


@router.get("/output")
async def list_output():
    """List all PDFs in output dir, sorted by mtime descending."""
    files = []
    if OUTPUT_DIR.exists():
        for f in sorted(OUTPUT_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.suffix.lower() == ".pdf":
                files.append({
                    "id": f.stem,
                    "filename": f.name,
                    "size_bytes": f.stat().st_size,
                    "created_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                })
    return {"files": files}


@router.post("/output/generate")
async def generate_pdf(body: dict):
    """Generate a PDF for a given report_id (direct pandoc + playwright)."""
    import asyncio
    import tempfile
    import subprocess

    report_id = body.get("report_id", "")
    if not report_id or not report_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid report_id")

    from app.config import REPORTS_DIR, OUTPUT_DIR, CAREER_OPS_ROOT

    # Find the report markdown file
    report_file = None
    if REPORTS_DIR.exists():
        for f in REPORTS_DIR.iterdir():
            if f.stem.startswith(f"{report_id}-") and f.suffix == ".md":
                report_file = f
                break
    if not report_file:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")

    # Also check CAREER_OPS_ROOT/reports as fallback
    if not report_file or not report_file.exists():
        alt_dir = CAREER_OPS_ROOT / "reports"
        if alt_dir.exists():
            for f in alt_dir.iterdir():
                if f.stem.startswith(f"{report_id}-") and f.suffix == ".md":
                    report_file = f
                    break
    if not report_file or not report_file.exists():
        raise HTTPException(status_code=404, detail=f"Report {report_id} file not found")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = OUTPUT_DIR / f"{report_id}.pdf"

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = f"{tmpdir}/{report_id}.html"

            # Convert markdown → HTML with pandoc
            proc = await asyncio.create_subprocess_exec(
                "pandoc", str(report_file), "-f", "markdown", "-t", "html",
                "-o", html_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
            if proc.returncode != 0:
                raise HTTPException(status_code=500, detail=f"pandoc failed: {stderr.decode()[:200]}")

            if not Path(html_path).exists():
                raise HTTPException(status_code=500, detail="pandoc produced no output")

            # Generate PDF via playwright
            proc = await asyncio.create_subprocess_exec(
                "node", str(CAREER_OPS_ROOT / "generate-pdf.mjs"),
                html_path, str(pdf_path), "--format=a4",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(CAREER_OPS_ROOT),
            )
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
            if proc.returncode != 0:
                raise HTTPException(status_code=500, detail=f"PDF generation failed: {stderr.decode()[:200]}")

        return {"status": "complete", "pdf": f"{report_id}.pdf", "size": pdf_path.stat().st_size}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=500, detail="PDF generation timed out")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)[:200]}")


@router.get("/output/download/{filename}")
async def download_pdf(filename: str):
    """Download a PDF with path traversal protection."""
    target = _safe_path(filename, OUTPUT_DIR)
    return FileResponse(
        target,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/output/view/{filename}")
async def view_pdf(filename: str):
    """View a PDF inline with path traversal protection."""
    target = _safe_path(filename, OUTPUT_DIR)
    return FileResponse(target, media_type="application/pdf")
