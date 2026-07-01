"""Output router — PDF generation and listing endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["output"])


@router.get("/output")
async def list_output():
    """List generated PDFs."""
    return {"files": []}


@router.post("/output/generate")
async def generate_pdf(data: dict):
    """Generate a tailored PDF."""
    return {"status": "not_implemented"}
