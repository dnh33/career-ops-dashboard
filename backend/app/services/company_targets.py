"""Parse dk-company-targets.md and enrich with job posting data."""
from __future__ import annotations

import re
from pathlib import Path

from app.config import DASHBOARD_ROOT
from app.services import market_data

TARGETS_PATH = DASHBOARD_ROOT / "data" / "research" / "dk-company-targets.md"

TIER_DEFAULT_SALARY: dict[str, int] = {
    "1": 62000,
    "2": 55000,
    "3": 50000,
    "Watchlist": 52000,
}


def _clean_md(text: str) -> str:
    return re.sub(r"\*\*", "", text).strip()


def _estimate_open_roles(roles_label: str, priority: int) -> int:
    parts = [part.strip() for part in roles_label.split(",") if part.strip()]
    return max(len(parts), 1 if priority <= 2 else 2)


def parse_company_targets() -> list[dict]:
    if not TARGETS_PATH.exists():
        return []

    content = TARGETS_PATH.read_text(encoding="utf-8")
    current_tier = "1"
    companies: list[dict] = []

    for line in content.splitlines():
        if line.startswith("## Tier 1"):
            current_tier = "1"
            continue
        if line.startswith("## Tier 2"):
            current_tier = "2"
            continue
        if line.startswith("## Tier 3"):
            current_tier = "3"
            continue
        if "Remote-First" in line:
            current_tier = "Watchlist"
            continue
        if not line.startswith("|") or line.startswith("| #") or line.startswith("|---"):
            continue
        if "Company |" in line or "Priority Domain" in line or "Metric |" in line:
            continue

        parts = [_clean_md(part) for part in line.split("|")[1:-1]]

        if current_tier == "Watchlist" and len(parts) >= 3:
            name = parts[0]
            domain = parts[1]
            skills = [skill.strip() for skill in re.split(r"[,/]", domain) if skill.strip()]
            companies.append(
                {
                    "name": name,
                    "slug": market_data._slugify_company(name),
                    "tier": "Watchlist",
                    "location": "Remote",
                    "size": "—",
                    "rolesLabel": domain,
                    "skills": skills[:6],
                    "skillsLabel": ", ".join(skills[:4]) + ("…" if len(skills) > 4 else domain),
                    "priority": 2,
                }
            )
            continue

        if len(parts) < 8:
            continue
        try:
            int(parts[0])
        except ValueError:
            continue

        name = parts[1]
        skills = [skill.strip() for skill in parts[6].split(",") if skill.strip()]
        priority = int(parts[7]) if parts[7].isdigit() else 3

        companies.append(
            {
                "name": name,
                "slug": market_data._slugify_company(name),
                "tier": current_tier,
                "location": parts[5].split("(")[0].strip(),
                "size": parts[2],
                "rolesLabel": parts[4],
                "skills": skills,
                "skillsLabel": ", ".join(skills[:5]) + ("…" if len(skills) > 5 else ""),
                "priority": priority,
            }
        )

    return companies


def enrich_companies(companies: list[dict]) -> list[dict]:
    postings = market_data.get_postings()
    by_slug: dict[str, list[dict]] = {}
    for posting in postings:
        by_slug.setdefault(posting["companySlug"], []).append(posting)

    enriched: list[dict] = []
    for company in companies:
        slug = company["slug"]
        matched = by_slug.get(slug, [])
        salaries = [posting["salary"] for posting in matched if posting.get("salary")]
        avg_salary = (
            int(round(sum(salaries) / len(salaries)))
            if salaries
            else TIER_DEFAULT_SALARY.get(company["tier"], 55000)
        )
        open_roles = len(matched) if matched else _estimate_open_roles(
            company["rolesLabel"], company["priority"]
        )
        last_days = min((posting["postedDaysAgo"] for posting in matched), default=21 + company["priority"])

        enriched.append(
            {
                **company,
                "avgSalary": avg_salary,
                "openRoles": open_roles,
                "lastPostedDays": last_days,
                "lastPosted": f"{last_days}d",
            }
        )

    return enriched


def compute_tier_summary(companies: list[dict]) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for tier in ("1", "2", "3", "Watchlist"):
        tier_companies = [company for company in companies if company["tier"] == tier]
        if not tier_companies:
            summary[tier] = {"count": 0, "avgSalary": 0, "openRoles": 0}
            continue
        summary[tier] = {
            "count": len(tier_companies),
            "avgSalary": int(
                round(sum(company["avgSalary"] for company in tier_companies) / len(tier_companies))
            ),
            "openRoles": sum(company["openRoles"] for company in tier_companies),
        }
    return summary


def get_companies_payload() -> dict:
    companies = enrich_companies(parse_company_targets())
    return {
        "companies": companies,
        "tierSummary": compute_tier_summary(companies),
    }
