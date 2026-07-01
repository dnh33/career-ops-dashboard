"""GET /api/companies — Company targets index."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.services import company_targets

router = APIRouter()


class TierSummaryItem(BaseModel):
    count: int
    avgSalary: int
    openRoles: int


class TierSummary(BaseModel):
    tier1: TierSummaryItem
    tier2: TierSummaryItem
    tier3: TierSummaryItem
    watchlist: TierSummaryItem


class CompanyTarget(BaseModel):
    slug: str
    name: str
    tier: str
    location: str
    size: str
    avgSalary: int
    openRoles: int
    skills: list[str]
    skillsLabel: str
    lastPosted: str
    lastPostedDays: int
    priority: int


class CompaniesResponse(BaseModel):
    companies: list[CompanyTarget]
    tierSummary: TierSummary


@router.get("/companies", response_model=CompaniesResponse, tags=["companies"])
async def get_companies() -> CompaniesResponse:
    payload = company_targets.get_companies_payload()
    summary = payload["tierSummary"]

    return CompaniesResponse(
        companies=[CompanyTarget(**company) for company in payload["companies"]],
        tierSummary=TierSummary(
            tier1=TierSummaryItem(**summary["1"]),
            tier2=TierSummaryItem(**summary["2"]),
            tier3=TierSummaryItem(**summary["3"]),
            watchlist=TierSummaryItem(**summary["Watchlist"]),
        ),
    )
