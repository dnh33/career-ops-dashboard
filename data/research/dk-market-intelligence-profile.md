# DK Market Intelligence Profile — Q3 2026

> **Purpose:** Single source of truth that drives CV optimization and scoring in Career Ops.
> **Generated:** 2026-06-30 from T1.1–T1.5 research + Daniel's CV + profile.yml.
> **Career Ops consumer:** `dk-market-scorer.py`, CV generation template, and job-ranking pipeline.

---

## 1. Daniel's Skill Gap Analysis

### 1.1 Skills Daniel Currently Has (from CV + profile.yml)

| Skill | Evidence | Market Demand % |
|-------|----------|-----------------|
| TypeScript | Primary frontend language, all roles | 27.5% |
| React.js / React 19 | "Production e-commerce interfaces" | 23.2% |
| Docker | "I run my own infra when needed" | 47.8% |
| Python | FastAPI backend (Career Ops Dashboard) | 58.0% |
| HTML | Implied by frontend depth | 10.1% |
| CSS / Tailwind | Primary styling approach | 11.6% (CSS) |
| Node.js | Backend (when needed) | ~5.8% |
| PostgreSQL | Backend (when needed) | subset of SQL 34.8% |
| Git | Implied by professional workflow | 78.3% |
| LLM integration (SSE, multi-provider) | Plugly AI Chat, Career Ops | Emerging ( fastest-growing) |
| Prompt engineering | "AI widget architecture" | Emerging |
| nginx | Self-hosted infra | not explicitly tracked |
| Linux / VPS | Self-hosted infra | 14.5% |
| Flutter / Dart | Mobile web apps | ~4.3% |
| Astro (SSG/SSR) | Career Ops Dashboard | niche |
| Figma / Design systems | "Anti-slop methodology" | 10.1% |

### 1.2 Gap Analysis — Market Demand vs. Daniel's Profile

| Priority | Skill | Market Demand | Daniel's Level | Gap Severity | Action |
|----------|-------|---------------|----------------|--------------|--------|
| 1 | **Kubernetes** | 24.6% | None | HIGH | Acquire fundamentals (CKAD cert path) |
| 2 | **AWS** | 37.7% | None/implicit | HIGH | AWS Cloud Practitioner → Solutions Architect Assoc. |
| 3 | **SQL (explicit)** | 34.8% | Some (PostgreSQL used) | MEDIUM | Highlight explicitly on CV as "SQL / PostgreSQL" |
| 4 | **CI/CD** | 8.7% | Implicit (self-hosted deploy) | MEDIUM | Make explicit — GitHub Actions or similar |
| 5 | **TensorFlow** | 8.7% | None | MEDIUM | Add to AI framework competence (besides PyTorch-as-user) |
| 6 | **Terraform / IaC** | 11.6% | None | MEDIUM | "Infrastructure-as-Code" messaging around Linux/Docker work |
| 7 | **Statistics** | 10.1% | None visible | LOW-MED | Mention if applicable to A/B testing, agent evaluation |
| 8 | **Danish language** | N/A (soft signal) | Bilingual (per CV) | NONE | Already a strength — keep prominent |
| 9 | **RAG / LLMs explicitly** | 11.6%+ (PyTorch proxy) | Strong (real projects) | LOW | Already differentiator — ensure CV uses market keywords |
| 10 | **Power BI / BI tools** | 11.6% | None | LOW | Not critical for engineering track |

### 1.3 Key Strategic Insight

Daniel is **strong on the frontend+AI intersection** (rare and growing) but **weak on backend/infrastructure depth** that Danish cloud-native employers expect. The market sees "Frontend + Docker + some Python" — Daniel needs to signal **"Full-stack capable with AI specialization"** rather than "Frontend who added AI."

---

## 2. Top 10 Highest-Value Company Targets

**Formula:** Value Score = (Median Salary for role at company's location, mid-level) × (Priority 1-5 as probability proxy) × (Hiring velocity signal)

| # | Company | Location | Est. Mid Salary (DKK/mo) | Priority | Hiring Signal | Value Score | Rationale |
|---|---------|----------|--------------------------|----------|---------------|-------------|-----------|
| 1 | **Corti** | Copenhagen | 60,000 (AI Engineer) | 5 | Active ML/LLM roles | 300 | Pure-play AI, strongest startup signal, Series B+ |
| 2 | **Novo Nordisk** | Ballerup/CPH | 60,000–65,000 | 5 | Massive AI hiring across units | 290 | Financial fortress, GenAI/agentic workflows active |
| 3 | **Zendesk** | Copenhagen | 55,000 (AI Software Dev) | 5 | AI Agents team actively expanding | 275 | Python + LLMs + MCP exactly Daniel's stack |
| 4 | **A.P. Moller – Maersk** | Copenhagen | 60,000 | 5 | Digital-first pivot, platform hiring | 270 | Real-time data platforms, cloud-native |
| 5 | **Universal Robots** | Odense | 60,000 | 5 | Active robotics + perception roles | 250 | Python + CV + real-time systems, Odense (lower COL) |
| 6 | **Microsoft DK** | Copenhagen | 60,000+ (Levels.fyi) | 5 | Data & AI Engineer active | 245 | Copilot stack, Azure AI, brand premium |
| 7 | **Spotify** | Copenhagen | 55,000+ | 4 | ML Engineer, Recommendation Sys | 220 | Scale, Python, data pipelines |
| 8 | **Trustpilot** | Copenhagen | 55,000 | 4 | ML Engineer, NLP systems | 200 | Python + ML + NLP, proven scale-up |
| 9 | **Pleo** | Copenhagen | 55,000 | 4 | Data Engineer, Fraud Detection ML | 190 | FinTech, unicorn, AI/ML investment |
| 10 | **Kognic** | Copenhagen office | 55,000 | 4 | AI Alignment, Sensor Fusion | 185 | Computer vision, PyTorch, small high-signal team |

**Hiring velocity signal sources:** Company target prioritization (T1.4) + job posting frequency (T1.1, 74 postings across Aug–Sep hiring season).

---

## 3. Top 10 Skills to Add / Highlight

Ranked by (market demand %) × (Daniel's ability to acquire plausibly):

| Rank | Skill | Category | Market % | Why Critical for Daniel | Acquisition Path |
|------|-------|----------|----------|-------------------------|------------------|
| 1 | **LLM Application Patterns** (RAG, agents, streaming) | AI/ML | ~15%+ and rising | Already doing this — must name it properly | CV rewrite using market terms |
| 2 | **TypeScript + React patterns** (server components, streaming) | Frontend | 27.5% + 23.2% | Already expert — ensure "AI-native" framing | Reframe existing experience |
| 3 | **Python (production grade)** | Programming | 58.0% | FastAPI + Career Ops counts — make it front-and-center | Highlight on CV as primary backend language |
| 4 | **AWS fundamentals** | Cloud | 37.7% | Biggest pure gap vs. market demand | AWS Cloud Practitioner cert (2-4 weeks) |
| 5 | **Docker + container orchestration** | DevOps | 47.8% | Already have Docker → extend to K8s | CKAD or KodeKloud K8s course |
| 6 | **CI/CD (GitHub Actions)** | DevOps | 8.7% | Implicit in self-hosted infra — make explicit | Set up for Career Ops repo, add to CV |
| 7 | **SQL** | Data | 34.8% | Already using PostgreSQL — just rename | Map "PostgreSQL" → "SQL / PostgreSQL" on CV |
| 8 | **Prompt engineering / LLM ops** | AI/ML | ~11.6%+ (PyTorch proxy) | Already core to Plugly AI | Use exact market terminology on CV |
| 9 | **Accessibility (WCAG) + Design Systems** | Frontend | 10.1% (Figma) | Already expert — rare combination with AI | Emphasize as differentiator |
| 10 | **Danish language** | Language | Soft signal | Already bilingual — massive competitive edge | Keep prominent on CV (already done) |

---

## 4. CV Template Rules (from Danish Cultural Norms)

Derived from T1.5 (dk-market-culture-guide.md). These are **enforced rules** for Career Ops CV generation targeting Danish tech companies.

### 4.1 Hard Rules (Never Violate)

| Rule | Specification |
|------|---------------|
| **Max length** | 2 pages absolute maximum. Danes discard 4+ page CVs. |
| **Personal section** | Must include: hobbies, interests, family status (optional), photo placeholder. This is non-negotiable for Danish market. |
| **Language** | Match the job posting language. For English-only postings, write in English but include a Languages section showing Danish proficiency. |
| **Tone** | Humble, collaborative. No superlatives ("world-class", "guru", "ninja", "rockstar"). Use "experienced in", "comfortable with", "passionate about". |
| **No overtime signaling** | Never say "work long hours", "24/7 availability", "go the extra mile". Use "efficient delivery", "sustainable pace". |
| **No union info** | Never include union membership on CV. Not a field in Career Ops. |
| **Structure** | Reverse chronological. Sections → Personal Info → Work Experience → Education → Skills → Languages → Interests/Hobbies. |

### 4.2 Soft Rules (Recommended)

| Rule | Specification |
|------|---------------|
| **Photo** | Include professional headshot by default (DK norm). Optional for big-tech/US-style companies. |
| **Languages section** | Always present with CEFR levels. Daniel: Danish (native), English (C1/C2). |
| **Cover letter** | Max 300–400 words / 1 page. Subject-line format (no "Dear Hiring Manager"). Include 1 sentence on "why Denmark / why this company". |
| **Personal profile summary** | Warm, collaborative tone. Include hobbies/interests signal for cultural fit. |
| **Application timing** | System should recommend campaigns in Jan–Feb and Aug–Sep. Current date (June–July) is slow season — expect delayed responses. |

### 4.3 Career Ops Implementation Checklist

- [ ] CV generator produces max 2-page output
- [ ] CV has personal details section with hobbies/interests (auto-populated from profile.yml)
- [ ] Tone checker flags: "ninja", "guru", "world-class", "rockstar", "synergy", "leverage" (DK cultural misfits)
- [ ] Languages section auto-generated with CEFR levels
- [ ] Photo placeholder is ON by default
- [ ] Cover letter generator: max 400 words, template starts with subject line
- [ ] Cover letter includes "why Denmark" sentence pulled from profile.yml notes
- [ ] System detects current date and warns if in slow hiring period
- [ ] Skills section maps internal skill names to Danish market terminology (e.g., "PostgreSQL" → "SQL / PostgreSQL")

---

## 5. Market Score Formula (0–100)

This formula scores how well a given CV matches the Danish Q3 2026 market for target roles.

### 5.1 Formula

```python
def market_score(cv: dict) -> float:
    """
    Score how well a CV matches the Danish tech market (Q3 2026).

    Input: dict with keys:
        - skills: list[str]            # skills on the CV
        - years_experience: int
        - has_danish: bool
        - roles_targeted: list[str]    # e.g. ["AI Engineer", "Frontend"]
        - cv_length_pages: int
        - has_personal_section: bool
        - has_photo: bool
        - tone_score: float            # 0.0–1.0 from tone checker

    Returns: float 0–100
    """
    score = 0.0

    # ── 1. Skill Match (40 points max) ──────────────────────────
    # Top 10 in-demand skills from T1.2, weighted by market %
    TOP_SKILLS = {
        "git":              0.783,
        "python":           0.580,
        "docker":           0.478,
        "aws":              0.377,
        "sql":              0.348,
        "typescript":       0.275,
        "kubernetes":       0.246,
        "react":            0.232,
        "linux":            0.145,
        "terraform":        0.116,
    }
    skill_score = 0.0
    cv_skills_lower = {s.lower() for s in cv["skills"]}
    for skill, weight in TOP_SKILLS.items():
        if skill in cv_skills_lower:
            skill_score += weight * 10  # max ~37.6 points if all present
    score += min(skill_score, 40.0)   # cap at 40

    # ── 2. AI/LLM Specialization Bonus (15 points max) ──────────
    AI_SKILLS = {"rag", "llm", "prompt_engineering", "agent", "streaming",
                 "pytorch", "tensorflow", "langchain", "openai", "openrouter"}
    ai_matches = len(AI_SKILLS & cv_skills_lower)
    score += min(ai_matches * 3.0, 15.0)

    # ── 3. Experience Level Fit (15 points max) ─────────────────
    # Optimal: 3–7 years. Below 2 = junior penalty. Above 10 = senior-but-expensive risk.
    years = cv["years_experience"]
    if 3 <= years <= 7:
        score += 15.0
    elif 2 <= years < 3:
        score += 10.0
    elif 7 < years <= 10:
        score += 12.0
    elif years >= 10:
        score += 8.0   # still qualified but may be seen as overpriced
    else:
        score += 5.0   # junior

    # ── 4. Danish Language Bonus (10 points) ────────────────────
    # Market data: English is sufficient but Danish is major competitive edge
    if cv.get("has_danish", False):
        score += 10.0
    elif cv.get("learning_danish", False):
        score += 5.0

    # ── 5. CV Format Compliance (10 points max) ──────────────────
    if cv.get("cv_length_pages", 3) <= 2:
        score += 5.0
    if cv.get("has_personal_section", False):
        score += 3.0   # Danish norm: personal/hobbies section expected
    if cv.get("has_photo", False):
        score += 2.0   # Danish norm: photo expected

    # ── 6. Tone & Cultural Fit (10 points max) ───────────────────
    score += cv.get("tone_score", 0.5) * 10.0
    # tone_score from: 1.0=humble+collaborative, 0.5=neutral, 0.0=superlatives

    return round(min(max(score, 0.0), 100.0), 1)
```

### 5.2 Score Interpretation

| Score | Label | Meaning | Career Ops Action |
|-------|-------|---------|-------------------|
| 85–100 | **Excellent** | Top-tier match for DK market | Auto-generate PDF, prioritize applications |
| 70–84 | **Strong** | Competitive, minor gaps | Generate PDF, recommend 1–2 skill additions |
| 55–69 | **Good** | Viable but needs optimization | Show skill gap recommendations, suggest CV rewrite |
| 40–54 | **Fair** | Significant gaps | Trigger CV rewrite mode, highlight missing skills |
| 0–39 | **Weak** | Major redesign needed | Full CV overhaul T1.2–T1.5 inputs |

### 5.3 Daniel's Current Estimated Score

Based on current CV analysis:

| Component | Estimate | Points |
|-----------|----------|--------|
| Skill Match (has: git, python, docker, sql, typescript, react, linux) | ~26/40 | 26.0 |
| AI/LLM Spec (has: llm, streaming, prompt_engineering, openrouter, openai) | ~5 of 10 | 15.0 |
| Experience (6 years) | Optimal band | 15.0 |
| Danish Language | Native | 10.0 |
| CV Format (2 pages ✓, has personal section ✓, no photo, some superlatives) | ~7/10 | 7.0 |
| Tone ("I ship", "rare and real", slight overselling) | 0.7 × 10 | 7.0 |
| **Total** | | **~80 / 100** |

**Verdict:** Strong (80). Main improvements needed: add AWS + Kubernetes to CV (even as "learning"), ensure photo is included, soften tone on "rare/real" language, and explicitly name SQL/PostgreSQL and CI/CD on CV.

---

## 6. Metadata & Source Files

| Source | File | Key Data Consumed |
|--------|------|-------------------|
| T1.1 (Job Postings) | `dk-job-postings-2026Q3.json` | 74 postings, role distribution, hiring velocity |
| T1.2 (Skill Demand) | `dk-skill-demand-2026Q3.md` | Top 20 skills, % demand, gap analysis |
| T1.3 (Salary) | `dk-salary-benchmarks-2026Q3.md` | P25/Median/P75 by role × location |
| T1.4 (Companies) | `dk-company-targets.md` | 34 companies, priority scoring, hiring signal |
| T1.5 (Culture) | `dk-market-culture-guide.md` | 9 topics, DO/DON'T, CV template rules |
| Daniel's CV | `/opt/career-ops/cv.md` | Current skills, experience, phrasing |
| Daniel's Profile | `/opt/career-ops/config/profile.yml` | Languages, experience years, notes |

---

## 7. Next Actions for Career Ops Integration

1. **Implement `dk-market-scorer.py`** using the formula in Section 5.1.
2. **Update CV generation prompt** to enforce rules from Section 4.
3. **Add skill gap alert**: when a posting requires AWS/K8s/Terraform and Daniel doesn't list them, flag for CV optimization.
4. **Company ranker**: use the Value Score from Section 2 to sort job listings in the dashboard.
5. **Seasonal timing banner**: show current hiring season status ("Summer slow period active — expect 3+ week response times").
