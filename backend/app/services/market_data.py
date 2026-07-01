"""Market intelligence data — postings, skill gaps, metrics."""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

from app.config import DASHBOARD_ROOT

POSTINGS_PATH = DASHBOARD_ROOT / "data" / "research" / "dk-job-postings-2026Q3.json"

LEVEL_SCORES = {
    "Expert": 90,
    "Some": 55,
    "Learning": 35,
    "None": 10,
}

USER_SKILL_LEVELS: dict[str, str] = {
    "TypeScript": "Expert",
    "React": "Expert",
    "React.js": "Expert",
    "Docker": "Expert",
    "Python": "Expert",
    "Git": "Expert",
    "LLM Integration": "Expert",
    "Prompt Engineering": "Expert",
    "HTML": "Some",
    "CSS": "Some",
    "CSS/Tailwind": "Some",
    "Node.js": "Some",
    "SQL": "Some",
    "PostgreSQL": "Some",
    "Linux": "Some",
    "Linux/VPS": "Some",
    "AWS": "Learning",
    "Kubernetes": "Learning",
    "Terraform": "Learning",
    "CI/CD": "Learning",
    "PyTorch": "None",
    "TensorFlow": "None",
    "Astro": "Expert",
    "Accessibility": "Expert",
    "JavaScript": "Expert",
}

SKILL_ALIASES = {
    "React.js": "React",
    "SQL": "PostgreSQL",
    "CSS": "CSS/Tailwind",
    "Linux": "Linux/VPS",
}

RESEARCH_MARKET: dict[str, dict] = {
    "Git": {"category": "devops", "pct": 78.3},
    "Python": {"category": "backend", "pct": 58.0},
    "Docker": {"category": "devops", "pct": 47.8},
    "AWS": {"category": "cloud", "pct": 37.7},
    "SQL": {"category": "data", "pct": 34.8},
    "TypeScript": {"category": "frontend", "pct": 27.5},
    "Kubernetes": {"category": "devops", "pct": 24.6},
    "React.js": {"category": "frontend", "pct": 23.2},
    "Linux": {"category": "devops", "pct": 14.5},
    "REST API": {"category": "backend", "pct": 13.0},
    "PyTorch": {"category": "ai", "pct": 11.6},
    "CSS": {"category": "frontend", "pct": 11.6},
    "Terraform": {"category": "devops", "pct": 11.6},
    "TensorFlow": {"category": "ai", "pct": 8.7},
    "CI/CD": {"category": "devops", "pct": 8.7},
    "JavaScript": {"category": "frontend", "pct": 10.1},
    "HTML": {"category": "frontend", "pct": 10.1},
    "Figma": {"category": "frontend", "pct": 10.1},
    "Statistics": {"category": "data", "pct": 10.1},
    "Power BI": {"category": "data", "pct": 11.6},
}

COMPANY_SLUGS: dict[str, str] = {
    "corti": "Corti",
    "zendesk": "Zendesk",
    "novonordisk": "Novo Nordisk",
    "maersk": "A.P. Moller – Maersk",
    "universalrobots": "Universal Robots",
    "microsoft": "Microsoft DK",
    "spotify": "Spotify",
    "trustpilot": "Trustpilot",
}


def _canonical_skill(name: str) -> str:
    return SKILL_ALIASES.get(name, name)


def _user_level(skill: str) -> str:
    key = _canonical_skill(skill)
    return USER_SKILL_LEVELS.get(key, USER_SKILL_LEVELS.get(skill, "None"))


def _user_score(skill: str) -> int:
    return LEVEL_SCORES.get(_user_level(skill), LEVEL_SCORES["None"])


def _slugify_company(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "", name.lower())
    for known_slug, known_name in COMPANY_SLUGS.items():
        if known_name.lower() in name.lower() or name.lower() in known_name.lower():
            return known_slug
    return slug or "unknown"


def _parse_seniority(role: str) -> str:
    role_lower = role.lower()
    if any(k in role_lower for k in ("principal", "staff", "lead")):
        return "Lead"
    if "senior" in role_lower or "sr." in role_lower or "sr " in role_lower:
        return "Senior"
    if any(k in role_lower for k in ("junior", "student", "graduate", "intern")):
        return "Junior"
    if "mid" in role_lower:
        return "Mid"
    return "Mid"


def _monthly_salary(raw: dict | None) -> int | None:
    if not raw:
        return None
    lo = raw.get("min")
    hi = raw.get("max")
    if lo is None and hi is None:
        return None
    avg_yearly = ((lo or hi) + (hi or lo)) / 2
    return int(round(avg_yearly / 12))


def _days_since(posted: str) -> int:
    try:
        posted_date = datetime.strptime(posted, "%Y-%m-%d").date()
    except ValueError:
        return 0
    return max(0, (date.today() - posted_date).days)


def _posting_gap(skills: list[str]) -> int:
    if not skills:
        return 0
    gaps: list[int] = []
    for skill in skills:
        demand = RESEARCH_MARKET.get(skill, RESEARCH_MARKET.get(_canonical_skill(skill), {})).get("pct", 15)
        user = _user_score(skill)
        gap = max(0, int(round(demand - user * (demand / 100))))
        gaps.append(gap)
    return int(round(sum(gaps) / len(gaps))) if gaps else 0


def load_raw_postings() -> list[dict]:
    if not POSTINGS_PATH.exists():
        return []
    with POSTINGS_PATH.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return data[:69]


def transform_posting(raw: dict, index: int) -> dict:
    skills = raw.get("skills_required") or []
    salary = _monthly_salary(raw.get("salary_range"))
    posted_days = _days_since(raw.get("posted_date", ""))
    company = raw.get("company", "Unknown")
    return {
        "id": f"posting-{index}",
        "company": company,
        "companySlug": _slugify_company(company),
        "role": raw.get("role", "Unknown"),
        "seniority": _parse_seniority(raw.get("role", "")),
        "location": raw.get("location", "—"),
        "salary": salary,
        "salaryLabel": f"{salary:,}" if salary else "—",
        "skills": skills,
        "skillsLabel": ", ".join(skills[:4]) + ("…" if len(skills) > 4 else ""),
        "postedDaysAgo": posted_days,
        "postedLabel": f"{posted_days}d" if posted_days else "—",
        "gap": _posting_gap(skills),
        "gapLabel": f"{_posting_gap(skills)}%",
        "url": raw.get("url", ""),
    }


def get_postings() -> list[dict]:
    return [transform_posting(raw, i) for i, raw in enumerate(load_raw_postings())]


def compute_metrics(postings: list[dict]) -> dict:
    salaries = [p["salary"] for p in postings if p.get("salary")]
    avg_salary = int(round(sum(salaries) / len(salaries))) if salaries else 0

    skill_counts: dict[str, int] = {}
    city_counts: dict[str, int] = {}
    for p in postings:
        city_counts[p["location"]] = city_counts.get(p["location"], 0) + 1
        for skill in p.get("skills") or []:
            key = _canonical_skill(skill)
            skill_counts[key] = skill_counts.get(key, 0) + 1

    top_skill = max(skill_counts, key=skill_counts.get) if skill_counts else "TypeScript"
    top_city = max(city_counts, key=city_counts.get) if city_counts else "Copenhagen"

    monthly_counts = [0] * 12
    for raw in load_raw_postings():
        try:
            month = datetime.strptime(raw.get("posted_date", ""), "%Y-%m-%d").month - 1
            monthly_counts[month] += 1
        except ValueError:
            continue
    velocity = sum(monthly_counts[-3:]) if any(monthly_counts) else len(postings)

    return {
        "avgSalary": avg_salary,
        "avgSalarySparkline": _sparkline_from_values(salaries[-7:] if len(salaries) >= 7 else salaries),
        "topSkill": top_skill,
        "topSkillSparkline": [68, 72, 70, 75, 78, 80, 82],
        "topCity": top_city,
        "topCitySparkline": [12, 14, 13, 15, 16, 18, 17],
        "velocity": velocity,
        "velocitySparkline": monthly_counts[-7:] if len(monthly_counts) >= 7 else [8, 9, 10, 11, 12, 13, 14],
        "postingCount": len(postings),
    }


def _sparkline_from_values(values: list[int]) -> list[int]:
    if not values:
        return [0, 0, 0, 0, 0, 0, 0]
    lo, hi = min(values), max(values)
    span = hi - lo or 1
    return [int(round((v - lo) / span * 100)) for v in values]


def build_skill_gap_rows() -> tuple[list[dict], list[dict]]:
    skills = list(RESEARCH_MARKET.keys())[:20]
    rows: list[dict] = []
    radar: list[dict] = []

    for skill in skills:
        demand = RESEARCH_MARKET[skill]["pct"]
        yours = _user_score(skill)
        gap = max(0, int(round(demand - yours * (demand / 100))))
        trend = "up" if gap >= 15 else "flat" if gap >= 8 else "down"
        rows.append(
            {
                "skill": skill,
                "demandPct": demand,
                "yourPct": yours,
                "gap": gap,
                "trend": trend,
            }
        )
        radar.append(
            {
                "skill": skill,
                "demand": demand,
                "coverage": yours,
                "gap": gap,
            }
        )

    rows.sort(key=lambda r: r["gap"], reverse=True)
    return rows, radar


def gap_variant(gap: int) -> str:
    if gap > 20:
        return "warm"
    if gap >= 10:
        return "warning"
    return "success"


def fit_variant(score: int) -> str:
    if score >= 80:
        return "success"
    if score >= 60:
        return "warning"
    return "error"


def action_label(match_score: int, gap: int) -> str:
    if match_score >= 80 and gap < 15:
        return "Apply"
    if match_score >= 60:
        return "Tailor"
    return "Skip"


def company_tier(priority: int = 5) -> str:
    if priority >= 5:
        return "Tier 1"
    if priority >= 3:
        return "Tier 2"
    return "Tier 3"
