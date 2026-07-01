"""GET /api/market/overview — Market intelligence dashboard data."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import market_data

router = APIRouter()


class MarketHealth(BaseModel):
    score: int
    trendPct: float
    sparkline: list[int]


class SkillDemandItem(BaseModel):
    skill: str
    category: str
    pct: float
    gap: str  # "none", "low", "medium", "high"


class SalaryRange(BaseModel):
    p25: int
    p50: int
    p75: int


class SalaryRanges(BaseModel):
    ai_engineer: dict[str, SalaryRange]
    frontend_engineer: dict[str, SalaryRange]
    full_stack_engineer: dict[str, SalaryRange]


class Company(BaseModel):
    slug: str
    name: str
    logo: str
    temperature: str  # "hot", "warm", "cool"
    openRoles: int
    topRoles: list[str]
    medianSalary: int
    location: str
    priority: int


class SkillGap(BaseModel):
    skill: str
    severity: str  # "high", "medium", "low"
    marketPct: float
    action: str


class CompanyDetail(BaseModel):
    slug: str
    name: str
    logo: str
    size: str
    fundingStage: str
    locations: list[str]
    openRoles: list[str]
    allRoles: list[dict]  # role details with title, department, level, salaryRange
    salaryComparison: dict  # company median vs market average
    techStack: list[str]
    cultureFitScore: int
    cultureFitFactors: list[str]
    description: str
    website: str
    applyUrl: str


class MarketMetrics(BaseModel):
    avgSalary: int
    avgSalarySparkline: list[int]
    topSkill: str
    topSkillSparkline: list[int]
    topCity: str
    topCitySparkline: list[int]
    velocity: int
    velocitySparkline: list[int]
    postingCount: int


class MarketPosting(BaseModel):
    id: str
    company: str
    companySlug: str
    role: str
    seniority: str
    location: str
    salary: int | None = None
    salaryLabel: str
    skills: list[str]
    skillsLabel: str
    postedDaysAgo: int
    postedLabel: str
    gap: int
    gapLabel: str
    url: str = ""


class MarketOverviewResponse(BaseModel):
    marketHealth: MarketHealth
    skillDemand: list[SkillDemandItem]
    salaryRanges: SalaryRanges
    companies: list[Company]
    skillGaps: list[SkillGap]
    metrics: MarketMetrics
    postings: list[MarketPosting]


class SkillGapRow(BaseModel):
    skill: str
    demandPct: float
    yourPct: int
    gap: int
    trend: str


class RadarPoint(BaseModel):
    skill: str
    demand: float
    coverage: int
    gap: int


class SkillGapResponse(BaseModel):
    skills: list[SkillGapRow]
    radarData: list[RadarPoint]


@router.get("/market/overview", response_model=MarketOverviewResponse, tags=["market"])
async def get_market_overview() -> MarketOverviewResponse:
    """
    Return market overview data for the dashboard.
    Data sourced from research files and computed health score.
    """
    # Market health score computed from research data
    market_health = MarketHealth(
        score=72,
        trendPct=4.2,
        sparkline=[68, 70, 69, 71, 72, 73, 72],
    )

    # Skill demand data from skill-demand-2026Q3.md
    skill_demand = [
        SkillDemandItem(skill="TypeScript", category="frontend", pct=27.5, gap="none"),
        SkillDemandItem(skill="Python", category="backend", pct=58.0, gap="none"),
        SkillDemandItem(skill="Docker", category="devops", pct=47.8, gap="none"),
        SkillDemandItem(skill="AWS", category="cloud", pct=37.7, gap="high"),
        SkillDemandItem(skill="SQL", category="data", pct=34.8, gap="medium"),
        SkillDemandItem(skill="Kubernetes", category="devops", pct=24.6, gap="high"),
        SkillDemandItem(skill="React.js", category="frontend", pct=23.2, gap="none"),
        SkillDemandItem(skill="Linux", category="devops", pct=14.5, gap="low"),
        SkillDemandItem(skill="Terraform", category="devops", pct=11.6, gap="medium"),
    ]

    # Salary ranges based on benchmarks for Copenhagen (adjust as needed for filters)
    salary_ranges = SalaryRanges(
        ai_engineer={
            "Copenhagen": SalaryRange(p25=55000, p50=65000, p75=75000),
            "Aarhus": SalaryRange(p25=50000, p50=58000, p75=65000),
            "Odense": SalaryRange(p25=48000, p50=55000, p75=62000),
            "Aalborg": SalaryRange(p25=47000, p50=54000, p75=60000),
            "Remote": SalaryRange(p25=52000, p50=62000, p75=72000),
        },
        frontend_engineer={
            "Copenhagen": SalaryRange(p25=50000, p50=58000, p75=65000),
            "Aarhus": SalaryRange(p25=45000, p50=52000, p75=58000),
            "Odense": SalaryRange(p25=43000, p50=50000, p75=55000),
            "Aalborg": SalaryRange(p25=42000, p50=50000, p75=54000),
            "Remote": SalaryRange(p25=48000, p50=55000, p75=62000),
        },
        full_stack_engineer={
            "Copenhagen": SalaryRange(p25=55000, p50=62000, p75=70000),
            "Aarhus": SalaryRange(p25=50000, p50=56000, p75=63000),
            "Odense": SalaryRange(p25=48000, p50=54000, p75=60000),
            "Aalborg": SalaryRange(p25=47000, p50=53000, p75=58000),
            "Remote": SalaryRange(p25=52000, p50=59000, p75=67000),
        },
    )

    # Company data from company targets
    companies = [
        Company(
            slug="corti",
            name="Corti",
            logo="/logos/corti.svg",
            temperature="hot",
            openRoles=5,
            topRoles=["AI Engineer", "ML Engineer"],
            medianSalary=60000,
            location="Copenhagen",
            priority=5,
        ),
        Company(
            slug="zendesk",
            name="Zendesk",
            logo="/logos/zendesk.svg",
            temperature="hot",
            openRoles=3,
            topRoles=["AI Software Developer", "Data Engineer"],
            medianSalary=55000,
            location="Copenhagen",
            priority=5,
        ),
        Company(
            slug="novonordisk",
            name="Novo Nordisk",
            logo="/logos/novonordisk.svg",
            temperature="hot",
            openRoles=8,
            topRoles=["Data Scientist", "ML Engineer", "AI Specialist"],
            medianSalary=65000,
            location="Ballerup/Copenhagen area",
            priority=5,
        ),
        Company(
            slug="maersk",
            name="A.P. Moller – Maersk",
            logo="/logos/maersk.svg",
            temperature="warm",
            openRoles=4,
            topRoles=["Data Scientist", "ML Engineer", "Data Engineer"],
            medianSalary=60000,
            location="Copenhagen",
            priority=5,
        ),
        Company(
            slug="universalrobots",
            name="Universal Robots",
            logo="/logos/universalrobots.svg",
            temperature="warm",
            openRoles=2,
            topRoles=["Robotics Software Engineer", "AI/ML for Robotics"],
            medianSalary=60000,
            location="Odense",
            priority=5,
        ),
        Company(
            slug="microsoft",
            name="Microsoft DK",
            logo="/logos/microsoft.svg",
            temperature="warm",
            openRoles=3,
            topRoles=["Data & AI Engineer", "AI Solutions Architect"],
            medianSalary=60000,
            location="Copenhagen",
            priority=5,
        ),
        Company(
            slug="spotify",
            name="Spotify",
            logo="/logos/spotify.svg",
            temperature="warm",
            openRoles=2,
            topRoles=["ML Engineer", "Data Engineer"],
            medianSalary=55000,
            location="Copenhagen",
            priority=4,
        ),
        Company(
            slug="trustpilot",
            name="Trustpilot",
            logo="/logos/trustpilot.svg",
            temperature="warm",
            openRoles=2,
            topRoles=["ML Engineer", "Data Scientist"],
            medianSalary=55000,
            location="Copenhagen",
            priority=4,
        ),
    ]

    # Skill gaps from market intelligence profile
    skill_gaps = [
        SkillGap(
            skill="AWS",
            severity="high",
            marketPct=37.7,
            action='Add "AWS Cloud Practitioner (in progress)"',
        ),
        SkillGap(
            skill="Kubernetes",
            severity="high",
            marketPct=24.6,
            action="Start CKAD path — 8 weeks",
        ),
        SkillGap(
            skill="Terraform",
            severity="medium",
            marketPct=11.6,
            action="Document Docker → TF workflow",
        ),
        SkillGap(
            skill="CI/CD",
            severity="medium",
            marketPct=8.7,
            action="Add GitHub Actions workflow to repo",
        ),
    ]

    postings_raw = market_data.get_postings()
    metrics_raw = market_data.compute_metrics(postings_raw)

    return MarketOverviewResponse(
        marketHealth=market_health,
        skillDemand=skill_demand,
        salaryRanges=salary_ranges,
        companies=companies,
        skillGaps=skill_gaps,
        metrics=MarketMetrics(**metrics_raw),
        postings=[MarketPosting(**p) for p in postings_raw],
    )


@router.get("/market/skill-gap", response_model=SkillGapResponse, tags=["market"])
async def get_skill_gap() -> SkillGapResponse:
    """Return skill gap table rows and radar chart data."""
    rows, radar = market_data.build_skill_gap_rows()
    return SkillGapResponse(
        skills=[SkillGapRow(**row) for row in rows],
        radarData=[RadarPoint(**point) for point in radar],
    )


class CompanyRole(BaseModel):
    title: str
    matchScore: int
    salary: dict[str, int]  # min, median, max
    location: str
    postedDaysAgo: int
    workMode: str
    requirements: list[str]


class SalaryComparison(BaseModel):
    company: dict[str, int]  # p25, p50, p75
    market: dict[str, int]
    deltaPct: int


class CultureFitFactor(BaseModel):
    name: str
    weight: float
    status: str  # "match", "gap", "neutral"


class CultureFit(BaseModel):
    score: int
    factors: list[CultureFitFactor]


class CompanyProfile(BaseModel):
    name: str
    logo: str
    location: str
    size: str
    funding: str
    founded: int
    techStack: list[str]
    culture: str
    links: dict[str, str]


class CompanyDeepDiveResponse(BaseModel):
    profile: CompanyProfile
    matchedRoles: list[CompanyRole]
    salaryComparison: SalaryComparison
    cultureFit: CultureFit


class CompanyPosting(BaseModel):
    id: str
    role: str
    seniority: str
    salary: int | None = None
    salaryLabel: str
    yourSkills: str
    gap: int
    gapLabel: str
    fitScore: int
    action: str


class CompanyPageCompany(BaseModel):
    slug: str
    name: str
    tier: str
    employees: str
    avgSalary: int
    openRoles: int
    hiringVelocity: list[int]
    location: str = ""
    techStack: list[str] = []


class CompanyPageResponse(BaseModel):
    company: CompanyPageCompany
    postings: list[CompanyPosting]
    profile: CompanyProfile
    salaryComparison: SalaryComparison
    cultureFit: CultureFit


def _build_company_page(slug: str, data: dict) -> CompanyPageResponse:
    profile = CompanyProfile(
        **{k: v for k, v in data.items() if k not in ["matchedRoles", "salaryComparison", "cultureFit"]}
    )
    matched = [CompanyRole(**r) for r in data["matchedRoles"]]
    salary_comparison = SalaryComparison(**data["salaryComparison"])
    culture_fit = CultureFit(**data["cultureFit"])

    postings: list[CompanyPosting] = []
    for index, role in enumerate(matched):
        reqs = role.requirements
        matched_skills = [
            skill for skill in reqs if market_data._user_level(skill) in ("Expert", "Some")
        ]
        gap = market_data._posting_gap(reqs)
        fit = role.matchScore
        postings.append(
            CompanyPosting(
                id=f"{slug}-role-{index}",
                role=role.title,
                seniority=market_data._parse_seniority(role.title),
                salary=role.salary.get("median"),
                salaryLabel=f"{role.salary.get('median', 0):,}",
                yourSkills=", ".join(matched_skills[:4]) or "—",
                gap=gap,
                gapLabel=f"{gap}%",
                fitScore=fit,
                action=market_data.action_label(fit, gap),
            )
        )

    salaries = [p.salary for p in postings if p.salary]
    avg_salary = int(round(sum(salaries) / len(salaries))) if salaries else salary_comparison.company.get("p50", 0)
    velocity = [2, 3, 2, 4, 3, 5, 4, 6, 5, 4, 7, len(postings)]

    company = CompanyPageCompany(
        slug=slug,
        name=profile.name,
        tier=market_data.company_tier(5),
        employees=profile.size,
        avgSalary=avg_salary,
        openRoles=len(postings),
        hiringVelocity=velocity,
        location=profile.location,
        techStack=profile.techStack,
    )

    return CompanyPageResponse(
        company=company,
        postings=postings,
        profile=profile,
        salaryComparison=salary_comparison,
        cultureFit=culture_fit,
    )


@router.get("/market/company/{slug}", response_model=CompanyPageResponse, tags=["market"])
async def get_company_deep_dive(slug: str) -> CompanyPageResponse:
    """
    Return detailed company intelligence for the deep-dive page.
    """
    company_data = {
        "corti": {
            "name": "Corti",
            "logo": "/logos/corti.svg",
            "location": "Copenhagen, DK",
            "size": "200-500",
            "funding": "Series B+",
            "founded": 2016,
            "techStack": ["Python", "TypeScript", "React", "Kubernetes", "AWS", "PostgreSQL", "PyTorch", "NLP/LLM"],
            "culture": "Mission-driven, clinical impact, remote OK",
            "links": {
                "website": "https://corti.ai",
                "linkedin": "https://linkedin.com/company/corti-ai",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Corti-EI_IE12345.htm",
                "careers": "https://jobs.ashbyhq.com/corti"
            },
            "matchedRoles": [
                {
                    "title": "Senior AI Engineer",
                    "matchScore": 92,
                    "salary": {"min": 55000, "median": 65000, "max": 75000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 14,
                    "workMode": "hybrid",
                    "requirements": ["Python", "LLMs", "RAG", "Kubernetes", "AWS"]
                },
                {
                    "title": "ML Platform Engineer",
                    "matchScore": 78,
                    "salary": {"min": 50000, "median": 60000, "max": 70000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 30,
                    "workMode": "onsite",
                    "requirements": ["Python", "Kubernetes", "MLOps", "Terraform"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 58000, "p50": 65000, "p75": 75000},
                "market": {"p25": 55000, "p50": 60000, "p75": 68000},
                "deltaPct": 8
            },
            "cultureFit": {
                "score": 84,
                "factors": [
                    {"name": "Mission alignment (healthcare AI)", "weight": 0.30, "status": "match"},
                    {"name": "Remote-friendly policy", "weight": 0.20, "status": "match"},
                    {"name": "Engineering-driven culture", "weight": 0.20, "status": "match"},
                    {"name": "Onsite bias (hybrid ≠ remote)", "weight": 0.15, "status": "gap"},
                    {"name": "Danish language preferred", "weight": 0.15, "status": "gap"}
                ]
            }
        },
        "zendesk": {
            "name": "Zendesk",
            "logo": "/logos/zendesk.svg",
            "location": "Copenhagen, DK",
            "size": "1000-5000",
            "funding": "Public (NYSE: ZEN)",
            "founded": 2007,
            "techStack": ["Python", "Spark", "LLMs", "AWS", "ML pipelines", "TypeScript", "React"],
            "culture": "Customer-obsessed, AI-first transformation, remote flexible",
            "links": {
                "website": "https://zendesk.com",
                "linkedin": "https://linkedin.com/company/zendesk",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Zendesk-EI_IE12345.htm",
                "careers": "https://www.zendesk.com/company/careers/"
            },
            "matchedRoles": [
                {
                    "title": "Data Engineer II – AI Agents",
                    "matchScore": 85,
                    "salary": {"min": 50000, "median": 58000, "max": 68000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 21,
                    "workMode": "hybrid",
                    "requirements": ["Python", "Spark", "LLMs", "AWS", "Data pipelines"]
                },
                {
                    "title": "Software Engineer – Analytics",
                    "matchScore": 72,
                    "salary": {"min": 48000, "median": 55000, "max": 65000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 45,
                    "workMode": "hybrid",
                    "requirements": ["TypeScript", "React", "Node.js", "Analytics"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 52000, "p50": 58000, "p75": 68000},
                "market": {"p25": 50000, "p50": 58000, "p75": 65000},
                "deltaPct": 0
            },
            "cultureFit": {
                "score": 78,
                "factors": [
                    {"name": "AI agents team expansion", "weight": 0.25, "status": "match"},
                    {"name": "Remote flexible policy", "weight": 0.20, "status": "match"},
                    {"name": "Large scale ML systems", "weight": 0.20, "status": "match"},
                    {"name": "Enterprise focus", "weight": 0.20, "status": "neutral"},
                    {"name": "Danish language not required", "weight": 0.15, "status": "gap"}
                ]
            }
        },
        "novonordisk": {
            "name": "Novo Nordisk",
            "logo": "/logos/novonordisk.svg",
            "location": "Ballerup/Copenhagen area",
            "size": "50000+",
            "funding": "Public (NYSE: NVO)",
            "founded": 1923,
            "techStack": ["Azure", "Python", "GenAI", "Agentic workflows", "Forecasting", "MLOps"],
            "culture": "Patient-first, science-driven, global impact, strong compliance",
            "links": {
                "website": "https://novonordisk.com",
                "linkedin": "https://linkedin.com/company/novonordisk",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Novo-Nordisk-EI_IE12345.htm",
                "careers": "https://www.novonordisk.com/careers.html"
            },
            "matchedRoles": [
                {
                    "title": "Senior Data Scientist – GenAI",
                    "matchScore": 88,
                    "salary": {"min": 60000, "median": 70000, "max": 85000},
                    "location": "Ballerup",
                    "postedDaysAgo": 10,
                    "workMode": "hybrid",
                    "requirements": ["Python", "GenAI", "LLMs", "Azure", "MLOps"]
                },
                {
                    "title": "Digital Innovation & AI Lead",
                    "matchScore": 75,
                    "salary": {"min": 65000, "median": 80000, "max": 100000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 20,
                    "workMode": "hybrid",
                    "requirements": ["Python", "Agentic AI", "Leadership", "Strategy"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 62000, "p50": 72000, "p75": 88000},
                "market": {"p25": 55000, "p50": 65000, "p75": 75000},
                "deltaPct": 11
            },
            "cultureFit": {
                "score": 82,
                "factors": [
                    {"name": "Massive AI investment", "weight": 0.25, "status": "match"},
                    {"name": "Global pharma leader", "weight": 0.20, "status": "match"},
                    {"name": "Mission-driven (healthcare)", "weight": 0.20, "status": "match"},
                    {"name": "Onsite bias (hybrid)", "weight": 0.20, "status": "gap"},
                    {"name": "Compliance-heavy culture", "weight": 0.15, "status": "gap"}
                ]
            }
        },
        "maersk": {
            "name": "A.P. Moller – Maersk",
            "logo": "/logos/maersk.svg",
            "location": "Copenhagen, DK",
            "size": "50000+",
            "funding": "Public (CSE: MAERSK-B)",
            "founded": 1904,
            "techStack": ["Python", "Spark", "Real-time data platforms", "Cloud-native", "Kubernetes", "Azure"],
            "culture": "Digital-first pivot, global logistics, transformation mindset",
            "links": {
                "website": "https://maersk.com",
                "linkedin": "https://linkedin.com/company/maersk",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Maersk-EI_IE12345.htm",
                "careers": "https://www.maersk.com/careers"
            },
            "matchedRoles": [
                {
                    "title": "Sr Engineering Manager – Data & AI Platforms",
                    "matchScore": 80,
                    "salary": {"min": 60000, "median": 72000, "max": 90000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 15,
                    "workMode": "hybrid",
                    "requirements": ["Python", "Spark", "Kubernetes", "Azure", "Leadership"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 60000, "p50": 70000, "p75": 85000},
                "market": {"p25": 55000, "p50": 65000, "p75": 75000},
                "deltaPct": 8
            },
            "cultureFit": {
                "score": 75,
                "factors": [
                    {"name": "Digital transformation leader", "weight": 0.25, "status": "match"},
                    {"name": "Real-time data at scale", "weight": 0.20, "status": "match"},
                    {"name": "Global logistics impact", "weight": 0.20, "status": "match"},
                    {"name": "Legacy enterprise culture", "weight": 0.20, "status": "gap"},
                    {"name": "Danish language preferred", "weight": 0.15, "status": "gap"}
                ]
            }
        },
        "universalrobots": {
            "name": "Universal Robots",
            "logo": "/logos/universalrobots.svg",
            "location": "Odense, DK",
            "size": "1000-5000",
            "funding": "Public (NYSE: TER, parent Teradyne)",
            "founded": 2005,
            "techStack": ["C++", "Python", "ROS", "Computer Vision", "Real-time", "Robotics"],
            "culture": "Robotics pioneers, engineering-first, Odense hub",
            "links": {
                "website": "https://universal-robots.com",
                "linkedin": "https://linkedin.com/company/universal-robots",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Universal-Robots-EI_IE12345.htm",
                "careers": "https://jobs.teradyne.com/UR"
            },
            "matchedRoles": [
                {
                    "title": "Robotics Software Engineer",
                    "matchScore": 70,
                    "salary": {"min": 50000, "median": 60000, "max": 70000},
                    "location": "Odense",
                    "postedDaysAgo": 25,
                    "workMode": "onsite",
                    "requirements": ["C++", "Python", "ROS", "Real-time systems"]
                },
                {
                    "title": "AI/ML for Robotics",
                    "matchScore": 75,
                    "salary": {"min": 55000, "median": 65000, "max": 75000},
                    "location": "Odense",
                    "postedDaysAgo": 30,
                    "workMode": "onsite",
                    "requirements": ["Python", "Computer Vision", "PyTorch", "Robotics"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 52000, "p50": 60000, "p75": 70000},
                "market": {"p25": 48000, "p50": 56000, "p75": 63000},
                "deltaPct": 7
            },
            "cultureFit": {
                "score": 72,
                "factors": [
                    {"name": "Robotics + AI intersection", "weight": 0.25, "status": "match"},
                    {"name": "Engineering-driven", "weight": 0.20, "status": "match"},
                    {"name": "Odense location (lower COL)", "weight": 0.20, "status": "match"},
                    {"name": "Onsite requirement", "weight": 0.20, "status": "gap"},
                    {"name": "Hardware-software integration", "weight": 0.15, "status": "neutral"}
                ]
            }
        },
        "microsoft": {
            "name": "Microsoft DK",
            "logo": "/logos/microsoft.svg",
            "location": "Copenhagen, DK",
            "size": "10000+",
            "funding": "Public (NASDAQ: MSFT)",
            "founded": 1975,
            "techStack": ["Azure AI", "ML.NET", "Python", "Power BI", "Copilot stack", "TypeScript", "React"],
            "culture": "Empower every person, growth mindset, diverse & inclusive",
            "links": {
                "website": "https://microsoft.com",
                "linkedin": "https://linkedin.com/company/microsoft",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Microsoft-EI_IE12345.htm",
                "careers": "https://careers.microsoft.com/"
            },
            "matchedRoles": [
                {
                    "title": "Data & AI Engineer",
                    "matchScore": 82,
                    "salary": {"min": 55000, "median": 68000, "max": 85000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 12,
                    "workMode": "hybrid",
                    "requirements": ["Python", "Azure AI", "ML", "Data engineering"]
                },
                {
                    "title": "AI Solutions Architect",
                    "matchScore": 78,
                    "salary": {"min": 60000, "median": 75000, "max": 95000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 18,
                    "workMode": "hybrid",
                    "requirements": ["Azure", "AI", "Architecture", "Pre-sales"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 58000, "p50": 70000, "p75": 88000},
                "market": {"p25": 55000, "p50": 65000, "p75": 75000},
                "deltaPct": 8
            },
            "cultureFit": {
                "score": 85,
                "factors": [
                    {"name": "Azure AI / Copilot stack", "weight": 0.25, "status": "match"},
                    {"name": "Global tech leader", "weight": 0.20, "status": "match"},
                    {"name": "Remote-friendly culture", "weight": 0.20, "status": "match"},
                    {"name": "Competitive compensation", "weight": 0.20, "status": "match"},
                    {"name": "Large org bureaucracy", "weight": 0.15, "status": "gap"}
                ]
            }
        },
        "spotify": {
            "name": "Spotify",
            "logo": "/logos/spotify.svg",
            "location": "Copenhagen, DK",
            "size": "8000+",
            "funding": "Public (SPOT)",
            "founded": 2006,
            "techStack": ["Python", "Java", "Kubernetes", "GCP", "TensorFlow", "PyTorch", "MLflow"],
            "culture": "Music + tech culture, autonomous squads, remote-friendly",
            "links": {
                "website": "https://spotify.com",
                "linkedin": "https://linkedin.com/company/spotify",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Spotify-EI_IE12345.htm",
                "careers": "https://spotifyjobs.com"
            },
            "matchedRoles": [
                {
                    "title": "ML Engineer",
                    "matchScore": 76,
                    "salary": {"min": 50000, "median": 58000, "max": 72000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 18,
                    "workMode": "hybrid",
                    "requirements": ["Python", "TensorFlow", "Kubernetes", "ML pipelines"]
                },
                {
                    "title": "Backend Engineer (ML Platform)",
                    "matchScore": 71,
                    "salary": {"min": 52000, "median": 62000, "max": 76000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 24,
                    "workMode": "hybrid",
                    "requirements": ["Python", "Java", "GCP", "Data engineering"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 52000, "p50": 58000, "p75": 72000},
                "market": {"p25": 50000, "p50": 58000, "p75": 65000},
                "deltaPct": 0
            },
            "cultureFit": {
                "score": 78,
                "factors": [
                    {"name": "Engineering autonomy", "weight": 0.25, "status": "match"},
                    {"name": "Open source culture", "weight": 0.20, "status": "match"},
                    {"name": "Remote-friendly", "weight": 0.20, "status": "match"},
                    {"name": "Large org scale", "weight": 0.20, "status": "neutral"},
                    {"name": "Music domain depth", "weight": 0.15, "status": "gap"}
                ]
            }
        },
        "trustpilot": {
            "name": "Trustpilot",
            "logo": "/logos/trustpilot.svg",
            "location": "Copenhagen, DK",
            "size": "1000-5000",
            "funding": "Public (TRUST)",
            "founded": 2007,
            "techStack": ["Python", "Kotlin", "Kubernetes", "GCP", "TensorFlow", "spaCy", "Hugging Face"],
            "culture": "Trust & transparency mission, consumer review data at scale",
            "links": {
                "website": "https://trustpilot.com",
                "linkedin": "https://linkedin.com/company/trustpilot",
                "glassdoor": "https://glassdoor.com/Overview/Working-at-Trustpilot-EI_IE12345.htm",
                "careers": "https://trustpilot.com/careers"
            },
            "matchedRoles": [
                {
                    "title": "ML Engineer",
                    "matchScore": 74,
                    "salary": {"min": 50000, "median": 57000, "max": 70000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 20,
                    "workMode": "hybrid",
                    "requirements": ["Python", "TensorFlow", "NLP", "ML pipelines"]
                },
                {
                    "title": "NLP Engineer",
                    "matchScore": 68,
                    "salary": {"min": 52000, "median": 62000, "max": 75000},
                    "location": "Copenhagen",
                    "postedDaysAgo": 28,
                    "workMode": "hybrid",
                    "requirements": ["Python", "spaCy", "Hugging Face", "LLMs"]
                }
            ],
            "salaryComparison": {
                "company": {"p25": 51000, "p50": 57000, "p75": 70000},
                "market": {"p25": 50000, "p50": 58000, "p75": 65000},
                "deltaPct": -2
            },
            "cultureFit": {
                "score": 73,
                "factors": [
                    {"name": "NLP / ML platform work", "weight": 0.25, "status": "match"},
                    {"name": "Copenhagen HQ", "weight": 0.20, "status": "match"},
                    {"name": "Engineering autonomy", "weight": 0.20, "status": "match"},
                    {"name": "Consumer review domain", "weight": 0.20, "status": "neutral"},
                    {"name": "Hybrid policy", "weight": 0.15, "status": "gap"}
                ]
            }
        }
    }
    
    if slug not in company_data:
        raise HTTPException(status_code=404, detail=f"Company '{slug}' not found")

    return _build_company_page(slug, company_data[slug])


@router.patch("/market/company/{slug}/priority", tags=["market"])
async def update_company_priority(slug: str, priority: int) -> dict:
    """Update company priority (1-5)."""
    if not 1 <= priority <= 5:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Priority must be 1-5")
    # In a real app, this would persist to DB
    return {"slug": slug, "priority": priority, "updated": True}


# Company detail data - in production this would come from a database
COMPANY_DETAILS: dict[str, CompanyDetail] = {
    "corti": CompanyDetail(
        slug="corti",
        name="Corti",
        logo="/logos/corti.svg",
        size="100-500",
        fundingStage="Series B",
        locations=["Copenhagen", "New York", "Remote"],
        openRoles=["AI Engineer", "ML Engineer", "Backend Engineer (Python)", "Data Scientist", "Clinical AI Researcher"],
        allRoles=[
            {"title": "AI Engineer", "department": "Engineering", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "ML Engineer", "department": "Engineering", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "Backend Engineer (Python)", "department": "Engineering", "level": "Mid", "salaryRange": "50000-65000 DKK"},
            {"title": "Data Scientist", "department": "Research", "level": "Senior", "salaryRange": "60000-80000 DKK"},
            {"title": "Clinical AI Researcher", "department": "Research", "level": "Lead", "salaryRange": "70000-95000 DKK"},
        ],
        salaryComparison={"companyMedian": 60000, "marketAverage": 62000, "difference": -2000, "vsMarketPct": -3.2},
        techStack=["Python", "PyTorch", "TensorFlow", "Kubernetes", "GCP", "PostgreSQL", "Redis", "Kafka", "FastAPI"],
        cultureFitScore=78,
        cultureFitFactors=["Strong ML research culture", "Clinical impact focus", "Remote-friendly", "Academic collaborations"],
        description="Corti is an AI company building voice-based AI for healthcare. Their AI co-pilot helps healthcare professionals make faster, more accurate decisions during patient consultations. Founded in 2016 in Copenhagen, they've raised Series B funding and work with healthcare systems globally.",
        website="https://corti.ai",
        applyUrl="https://corti.ai/careers",
    ),
    "zendesk": CompanyDetail(
        slug="zendesk",
        name="Zendesk",
        logo="/logos/zendesk.svg",
        size="5000+",
        fundingStage="Public (acquired by Permira)",
        locations=["Copenhagen", "San Francisco", "London", "Singapore", "Remote"],
        openRoles=["AI Software Developer", "Data Engineer", "ML Engineer", "Applied Scientist", "Backend Engineer"],
        allRoles=[
            {"title": "AI Software Developer", "department": "AI Platform", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "Data Engineer", "department": "Data Platform", "level": "Senior", "salaryRange": "55000-70000 DKK"},
            {"title": "ML Engineer", "department": "AI Platform", "level": "Staff", "salaryRange": "70000-90000 DKK"},
            {"title": "Applied Scientist", "department": "Research", "level": "Senior", "salaryRange": "65000-85000 DKK"},
            {"title": "Backend Engineer", "department": "Engineering", "level": "Mid", "salaryRange": "50000-65000 DKK"},
        ],
        salaryComparison={"companyMedian": 55000, "marketAverage": 62000, "difference": -7000, "vsMarketPct": -11.3},
        techStack=["Python", "Java", "Go", "Kubernetes", "AWS", "Kafka", "Spark", "Airflow", "TensorFlow", "PyTorch"],
        cultureFitScore=72,
        cultureFitFactors=["Large scale engineering", "Customer obsession", "Remote-first options", "Strong engineering culture"],
        description="Zendesk is a customer service software company with a major AI/ML presence in Copenhagen. Their AI platform powers automated customer support for 100k+ companies. Copenhagen office focuses on AI/ML engineering and data platform.",
        website="https://zendesk.com",
        applyUrl="https://zendesk.com/careers",
    ),
    "novonordisk": CompanyDetail(
        slug="novonordisk",
        name="Novo Nordisk",
        logo="/logos/novonordisk.svg",
        size="50000+",
        fundingStage="Public (Novo Holdings)",
        locations=["Ballerup", "Copenhagen area", "Global"],
        openRoles=["Data Scientist", "ML Engineer", "AI Specialist", "MLOps Engineer", "Bioinformatics Scientist"],
        allRoles=[
            {"title": "Data Scientist", "department": "Digital & IT", "level": "Senior", "salaryRange": "60000-80000 DKK"},
            {"title": "ML Engineer", "department": "Digital & IT", "level": "Senior", "salaryRange": "65000-85000 DKK"},
            {"title": "AI Specialist", "department": "Digital & IT", "level": "Lead", "salaryRange": "70000-95000 DKK"},
            {"title": "MLOps Engineer", "department": "Digital & IT", "level": "Mid", "salaryRange": "55000-70000 DKK"},
            {"title": "Bioinformatics Scientist", "department": "R&D", "level": "Senior", "salaryRange": "65000-85000 DKK"},
        ],
        salaryComparison={"companyMedian": 65000, "marketAverage": 62000, "difference": 3000, "vsMarketPct": 4.8},
        techStack=["Python", "R", "PyTorch", "TensorFlow", "Azure ML", "Databricks", "Kubernetes", "SQL", "Spark"],
        cultureFitScore=85,
        cultureFitFactors=["Life sciences impact", "Strong R&D investment", "Work-life balance", "Global opportunities", "Purpose-driven"],
        description="Novo Nordisk is a global healthcare company leading in diabetes care. Their Copenhagen-area Digital & IT division is heavily investing in AI/ML for drug discovery, clinical trials, and patient outcomes. World-class research environment with massive data assets.",
        website="https://novonordisk.com",
        applyUrl="https://novonordisk.com/careers",
    ),
    "maersk": CompanyDetail(
        slug="maersk",
        name="A.P. Moller – Maersk",
        logo="/logos/maersk.svg",
        size="80000+",
        fundingStage="Public (APMM)",
        locations=["Copenhagen", "Global"],
        openRoles=["Data Scientist", "ML Engineer", "Data Engineer", "MLOps Engineer", "Applied ML Researcher"],
        allRoles=[
            {"title": "Data Scientist", "department": "Technology", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "ML Engineer", "department": "Technology", "level": "Senior", "salaryRange": "60000-80000 DKK"},
            {"title": "Data Engineer", "department": "Technology", "level": "Mid", "salaryRange": "50000-65000 DKK"},
            {"title": "MLOps Engineer", "department": "Technology", "level": "Senior", "salaryRange": "60000-75000 DKK"},
            {"title": "Applied ML Researcher", "department": "Technology", "level": "Lead", "salaryRange": "75000-100000 DKK"},
        ],
        salaryComparison={"companyMedian": 60000, "marketAverage": 62000, "difference": -2000, "vsMarketPct": -3.2},
        techStack=["Python", "Java", "Scala", "Kubernetes", "GCP", "BigQuery", "Airflow", "TensorFlow", "PyTorch", "MLflow"],
        cultureFitScore=70,
        cultureFitFactors=["Global logistics scale", "Digital transformation", "Sustainability focus", "Complex data challenges"],
        description="Maersk is transforming from a shipping company to an integrated logistics technology company. Their Technology division in Copenhagen builds ML-powered supply chain optimization, demand forecasting, and vessel routing. Massive scale data challenges with real-world impact.",
        website="https://maersk.com",
        applyUrl="https://maersk.com/careers",
    ),
    "universalrobots": CompanyDetail(
        slug="universalrobots",
        name="Universal Robots",
        logo="/logos/universalrobots.svg",
        size="1000-5000",
        fundingStage="Subsidiary (Teradyne)",
        locations=["Odense", "Global"],
        openRoles=["Robotics Software Engineer", "AI/ML for Robotics", "Embedded Software Engineer", "Computer Vision Engineer"],
        allRoles=[
            {"title": "Robotics Software Engineer", "department": "R&D", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "AI/ML for Robotics", "department": "R&D", "level": "Senior", "salaryRange": "60000-80000 DKK"},
            {"title": "Embedded Software Engineer", "department": "R&D", "level": "Mid", "salaryRange": "50000-65000 DKK"},
            {"title": "Computer Vision Engineer", "department": "R&D", "level": "Senior", "salaryRange": "60000-80000 DKK"},
        ],
        salaryComparison={"companyMedian": 60000, "marketAverage": 62000, "difference": -2000, "vsMarketPct": -3.2},
        techStack=["C++", "Python", "ROS", "TensorFlow", "PyTorch", "OpenCV", "CUDA", "Linux", "GitLab CI"],
        cultureFitScore=75,
        cultureFitFactors=["Robotics pioneer", "Hardware-software integration", "Odense robotics cluster", "Innovation culture"],
        description="Universal Robots pioneered collaborative robots (cobots) and is the market leader. Based in Odense, they're at the center of Denmark's robotics cluster. R&D roles combine robotics, computer vision, and ML for next-gen collaborative automation.",
        website="https://universal-robots.com",
        applyUrl="https://universal-robots.com/careers",
    ),
    "microsoft": CompanyDetail(
        slug="microsoft",
        name="Microsoft DK",
        logo="/logos/microsoft.svg",
        size="200000+",
        fundingStage="Public (MSFT)",
        locations=["Copenhagen", "Lyngby", "Global"],
        openRoles=["Data & AI Engineer", "AI Solutions Architect", "ML Engineer", "Cloud Solution Architect (AI)"],
        allRoles=[
            {"title": "Data & AI Engineer", "department": "Azure", "level": "Senior", "salaryRange": "60000-80000 DKK"},
            {"title": "AI Solutions Architect", "department": "Azure", "level": "Principal", "salaryRange": "80000-110000 DKK"},
            {"title": "ML Engineer", "department": "Research", "level": "Senior", "salaryRange": "65000-90000 DKK"},
            {"title": "Cloud Solution Architect (AI)", "department": "Azure", "level": "Senior", "salaryRange": "70000-95000 DKK"},
        ],
        salaryComparison={"companyMedian": 60000, "marketAverage": 62000, "difference": -2000, "vsMarketPct": -3.2},
        techStack=["Python", "C#", ".NET", "Azure ML", "Azure Kubernetes", "MLflow", "ONNX", "PyTorch", "TensorFlow"],
        cultureFitScore=80,
        cultureFitFactors=["Cloud + AI platform leader", "Research access", "Global mobility", "Learning budget", "Flexible work"],
        description="Microsoft Denmark has a strong Azure AI and Data & AI engineering presence. Copenhagen office works on customer-facing AI solutions, Azure ML platform, and applied research. Access to massive compute, research partnerships, and global career mobility.",
        website="https://microsoft.com/denmark",
        applyUrl="https://careers.microsoft.com",
    ),
    "spotify": CompanyDetail(
        slug="spotify",
        name="Spotify",
        logo="/logos/spotify.svg",
        size="8000+",
        fundingStage="Public (SPOT)",
        locations=["Copenhagen", "Stockholm", "New York", "London", "Remote"],
        openRoles=["ML Engineer", "Data Engineer", "Research Scientist", "Backend Engineer (ML Platform)"],
        allRoles=[
            {"title": "ML Engineer", "department": "Personalization", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "Data Engineer", "department": "Data Platform", "level": "Senior", "salaryRange": "55000-70000 DKK"},
            {"title": "Research Scientist", "department": "Research", "level": "Senior", "salaryRange": "70000-100000 DKK"},
            {"title": "Backend Engineer (ML Platform)", "department": "Platform", "level": "Senior", "salaryRange": "60000-80000 DKK"},
        ],
        salaryComparison={"companyMedian": 55000, "marketAverage": 62000, "difference": -7000, "vsMarketPct": -11.3},
        techStack=["Python", "Java", "Scala", "Kubernetes", "GCP", "BigQuery", "Beam", "TensorFlow", "PyTorch", "MLflow"],
        cultureFitScore=78,
        cultureFitFactors=["Music + tech culture", "Autonomous squads", "Open source contributions", "Research publications", "Remote-friendly"],
        description="Spotify's Copenhagen office focuses on ML platform, personalization, and data engineering. Famous for autonomous squad model, open source contributions (Backstage, Luigi), and research publications. Strong engineering culture with music industry data.",
        website="https://spotify.com",
        applyUrl="https://spotifyjobs.com",
    ),
    "trustpilot": CompanyDetail(
        slug="trustpilot",
        name="Trustpilot",
        logo="/logos/trustpilot.svg",
        size="1000-5000",
        fundingStage="Public (TRUST)",
        locations=["Copenhagen", "London", "New York", "Remote"],
        openRoles=["ML Engineer", "Data Scientist", "Data Engineer", "NLP Engineer"],
        allRoles=[
            {"title": "ML Engineer", "department": "ML Platform", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "Data Scientist", "department": "Insights", "level": "Senior", "salaryRange": "55000-75000 DKK"},
            {"title": "Data Engineer", "department": "Data Platform", "level": "Mid", "salaryRange": "50000-65000 DKK"},
            {"title": "NLP Engineer", "department": "ML Platform", "level": "Senior", "salaryRange": "60000-80000 DKK"},
        ],
        salaryComparison={"companyMedian": 55000, "marketAverage": 62000, "difference": -7000, "vsMarketPct": -11.3},
        techStack=["Python", "Java", "Kotlin", "Kubernetes", "GCP", "Kafka", "TensorFlow", "PyTorch", "spaCy", "Hugging Face"],
        cultureFitScore=73,
        cultureFitFactors=["Trust & transparency mission", "Consumer review data", "ML for fraud detection", "Engineering autonomy", "Copenhagen HQ"],
        description="Trustpilot is the world's leading review platform. Their Copenhagen HQ houses ML platform, data engineering, and NLP teams working on review authenticity, fraud detection, and business insights from 150M+ reviews. Strong ML engineering culture with real consumer impact.",
        website="https://trustpilot.com",
        applyUrl="https://trustpilot.com/careers",
    ),
}


@router.get("/market/companies/{slug}", response_model=CompanyDetail, tags=["market"])
async def get_company_detail(slug: str) -> CompanyDetail:
    """
    Return detailed company intelligence for a single company.
    Returns 404 if company not found.
    """
    if slug not in COMPANY_DETAILS:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Company '{slug}' not found")

    return COMPANY_DETAILS[slug]