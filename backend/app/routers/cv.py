"""CV endpoint — separate from profile for cleaner API."""
from __future__ import annotations

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.config import CONFIG_DIR
from app.services import cv_optimize

router = APIRouter(tags=["cv"])
CV_FILE = CONFIG_DIR / "cv.md"


class CvOptimizeRule(BaseModel):
    id: str
    rule: str
    category: str
    currentCv: str
    target: str
    gap: int
    gapLabel: str
    priority: str
    priorityVariant: str
    role: str
    before: str
    after: str


class CvOptimizeResponse(BaseModel):
    overallScore: int
    keywordCoverage: int
    criticalGaps: int
    roleMatches: int
    rules: list[CvOptimizeRule]


@router.get("/cv")
async def get_cv():
    if CV_FILE.exists():
        return {"cv": CV_FILE.read_text(encoding="utf-8")}
    return {"cv": ""}


@router.put("/cv")
async def put_cv(body: dict):
    CV_FILE.parent.mkdir(parents=True, exist_ok=True)
    CV_FILE.write_text(body.get("cv", ""), encoding="utf-8")
    return {"ok": True}


@router.get("/cv/optimize", response_model=CvOptimizeResponse, tags=["cv"])
async def get_cv_optimize(
    role: str = Query("all", pattern="^(frontend|ai-engineer|fullstack|all)$"),
) -> CvOptimizeResponse:
    payload = cv_optimize.get_optimize_payload(role)
    return CvOptimizeResponse(
        overallScore=payload["overallScore"],
        keywordCoverage=payload["keywordCoverage"],
        criticalGaps=payload["criticalGaps"],
        roleMatches=payload["roleMatches"],
        rules=[CvOptimizeRule(**rule) for rule in payload["rules"]],
    )
