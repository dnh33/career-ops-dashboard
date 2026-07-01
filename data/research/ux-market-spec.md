# Career Ops Dashboard — Market Intelligence UX Specification

**Status:** Draft v1.0  
**Target:** Implementation in Astro + vanilla JS (no framework)  
**Design System:** Reuse existing globals.css + components.css tokens and components

---

## 1. Design System Foundation (Reuse Only)

### 1.1 Color Tokens (from globals.css)
```css
--bg-primary: #0a0e1a;
--bg-secondary: #111827;
--bg-surface: #141b2d;
--bg-elevated: #1a2236;
--bg-tertiary: #1f2937;
--text-primary: #f1f5f9;
--text-secondary: #94a3b8;
--text-muted: #64748b;
--accent-primary: #D4A853;       /* gold — primary actions, active states */
--accent-hover: #e0b865;
--accent-muted: #92702a;
--success: #22c55e;
--warning: #eab308;
--error: #ef4444;
--info: #3b82f6;
--border-default: #1e293b;
--border-hover: #334155;
--grade-high: #22c55e;
--grade-mid: #eab308;
--grade-low: #ef4444;
```

### 1.2 Component Primitives to Reuse (from components.css)
| Component | Class | Use Case |
|-----------|-------|----------|
| Panel | `.panel` + `.panel-scroll` | Scrollable containers, cards |
| Toolbar | `.toolbar` + `.toolbar-input` + `.toolbar-btn` | Page headers with search/filter |
| Filter Bar | `.filter-bar` + `.filter-chip` | Multi-select filter rows |
| Score Ring | `.score-ring` | Circular progress (market health, culture fit) |
| Status Badges | `.tag` + `.tag-*` | Skill gaps, priority, hiring signal |
| Section Header | `.section-header` | Section titles with actions |
| Table → Card | `.table-responsive` | Mobile-responsive tables |
| Skeleton | `.skeleton` + `.skeleton-text` | Loading states |
| Card Interactive | `.card-interactive` | Clickable company/role cards |

### 1.3 Typography Scale
- `--font-display: 'Sora'` — page titles, hero numbers
- `--font-sans: 'Inter'` — body, UI
- `--font-mono: 'JetBrains Mono'` — code, salaries, numbers
- Scale: `xs(0.75rem)` `sm(0.875rem)` `base(1rem)` `lg(1.125rem)` `xl(1.25rem)` `2xl(1.5rem)` `3xl(1.875rem)`

### 1.4 Breakpoints
- `--bp-sm: 640px` — mobile landscape
- `--bp-md: 768px` — tablet
- `--bp-lg: 1024px` — desktop (sidebar shows)
- `--bp-xl: 1280px` — wide content max-width

### 1.5 Touch Targets
All interactive elements: `min-height: 44px` (enforced in globals.css)

---

## 2. Page 1 — Market Overview (`/market`)

### 2.1 Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│ TOOLBAR (sticky top)                                            │
│  [Search companies/skills]  [Filter: Role ▼] [Filter: Loc ▼]   │
├─────────────────────────────────────────────────────────────────┤
│ HERO SECTION                                                    │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐  │
│  │ MARKET HEALTH SCORE │  │ TREND SPARKLINE (30 days)       │  │
│  │      72 / 100       │  │ ↗ +4.2% vs last month           │  │
│  │    [score-ring]     │  │ [sparkline]                     │  │
│  └─────────────────────┘  └─────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ SKILL DEMAND BAR CHART (Top 10)                                 │
│  [Horizontal bars, color-coded by category]                     │
│  TypeScript ████████████ 27.5%  [Frontend]                      │
│  Python     ███████████████ 58.0%  [Backend]                    │
│  Docker     ██████████████ 47.8%  [DevOps]                      │
│  AWS        ███████████ 37.7%  [Cloud] ← GAP (tag-red)         │
│  SQL        ███████████ 34.8%  [Data]                          │
│  Kubernetes ████████ 24.6%  [DevOps] ← GAP (tag-red)           │
│  React      ██████████ 23.2%  [Frontend]                       │
│  Git        ████████████████████ 78.3%  [Core]                 │
│  Linux      ██████ 14.5%  [Infra]                              │
│  Terraform  ██████ 11.6%  [DevOps] ← GAP (tag-amber)           │
├─────────────────────────────────────────────────────────────────┤
│ SALARY RANGE CARDS (per role, filterable by location)          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │ AI Engineer     │ │ Frontend Eng    │ │ Full-Stack      │   │
│  │ DKK 55k–75k/mo  │ │ DKK 50k–65k/mo  │ │ DKK 55k–70k/mo  │   │
│  │ p25 55k │ p50 65k│ │ p25 50k │ p50 58k│ │ p25 55k │ p50 62k│   │
│  │ p75 75k          │ │ p75 65k         │ │ p75 70k         │   │
│  │ [Copenhagen ▼]  │ │ [Copenhagen ▼]  │ │ [Copenhagen ▼]  │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│ COMPANY HIRING HEATMAP (card grid, filterable)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  Corti   │ │  Novo N. │ │ Zendesk  │ │  Maersk  │  ...      │
│  │ 🔥 HOT   │ │ 🔥 HOT   │ │ 🔥 HOT   │ │ 🟡 WARM  │            │
│  │ AI/ML ×5 │ │ AI ×8    │ │ AI Agt ×3│ │ Platform ×4│            │
│  │ 60k DKK  │ │ 65k DKK  │ │ 55k DKK  │ │ 60k DKK   │            │
│  │ [View]   │ │ [View]   │ │ [View]   │ │ [View]    │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
├─────────────────────────────────────────────────────────────────┤
│ SKILL GAP ALERT PANEL                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 🔴 HIGH  AWS Cloud          → Add "AWS (learning)"       │   │
│  │ 🔴 HIGH  Kubernetes         → CKAD path (8 weeks)        │   │
│  │ 🟡 MED   Terraform/IaC      → Document Docker → TF       │   │
│  │ 🟡 MED   CI/CD (GitHub Act) → Add workflow to repo       │   │
│  │ 🟢 LOW   TensorFlow         → Mention PyTorch + TF       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Specifications

#### Hero — Market Health Score
- **Component:** `.score-ring` (48px) + large display text (`--text-3xl`, `--font-display`)
- **Data source:** Computed from job posting velocity × salary trend × company hiring count
- **Trend indicator:** `↗ +4.2%` (green) / `↘ -2.1%` (red) using `.tag-green` / `.tag-red`
- **Mobile:** Stack vertically, score ring 64px, sparkline full-width below

#### Skill Demand Bar Chart
- **Implementation:** Pure CSS horizontal bars (`.sparkline` pattern adapted)
- **Bar:** `height: 28px`, `border-radius: 4px`, color by category:
  - Frontend: `--accent-primary` (#D4A853)
  - Backend: `--info` (#3b82f6)
  - DevOps: `--success` (#22c55e)
  - Cloud: `--warning` (#eab308)
  - Data: `--violet` (new: `#a855f7`)
  - Core: `--text-muted` (#64748b)
- **Gap indicator:** `.tag-red` (HIGH), `.tag-amber` (MED), `.tag-green` (LOW) appended to bar label
- **Mobile:** Full-width bars, category badge on left, % on right

#### Salary Range Cards
- **Component:** `.panel` cards in CSS grid (1 col mobile, 2 col tablet, 3 col desktop)
- **Content:** Role title, p25/p50/p75 in monospace, location filter chip (`.filter-chip`)
- **Interaction:** Location filter updates all cards via fetch + DOM swap (no page reload)
- **Empty state:** `.empty-row` "No data for this location"

#### Company Hiring Heatmap
- **Component:** `.card-interactive` grid (1/2/4 columns responsive)
- **Card content:**
  - Company name + logo placeholder (24×24)
  - Hiring temperature badge: `.tag-red` (HOT ≥5 roles), `.tag-amber` (WARM 2–4), `.tag-gray` (COOL 1)
  - Top roles hiring for (max 2, truncated)
  - Median salary for target role at this company
  - CTA: `[View]` → navigates to `/market/company/{slug}`
- **Filters:** `.filter-bar` with chips: Role, Location, Priority (1–5), Temperature

#### Skill Gap Alert Panel
- **Component:** `.panel-scroll` (max-height 280px)
- **Rows:** `.tag-{red|amber|green}` + skill name + action text
- **Action text:** Specific, actionable (from market-intelligence-profile.md Section 1.2)
- **Priority order:** HIGH → MED → LOW

### 2.3 Interaction Flows
| Trigger | Action | Feedback |
|---------|--------|----------|
| Location filter change | `fetch('/api/market/salaries?loc=...')` → swap card grid | Skeleton cards during load |
| Company card click | `navigate('/market/company/' + slug)` | Page transition |
| Skill gap tag click | Scroll to that skill in bar chart (anchor) | Highlight bar briefly |
| Filter chip click | Toggle active, refetch company grid | Chip `.active` state |
| Mobile: swipe cards | Horizontal scroll snap (CSS `scroll-snap-type: x mandatory`) | Native feel |

### 2.4 Mobile Adaptations
- Hero: stacked, score ring 64px
- Skill bars: full-width, category badge left
- Salary cards: single column
- Company grid: horizontal scroll with snap
- Gap panel: full-width, no max-height limit

---

## 3. Page 2 — Company Deep-Dive (`/market/company/{slug}`)

### 3.1 Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│ TOOLUMN TOOLBAR
  [← Back]  Company Name                    [Priority: 5/5 ▼] [Apply →]
├─────────────────────────────────────────────────────────────────┤
│ COMPANY PROFILE CARD                                              │
│ ┌─────────────────────────────────────────────────────────────┐  │
│ │ [Logo]  Corti                              Priority: ★★★★★  │  │
│ │       AI-powered medical documentation        🔥 HIRING    │  │
│ │       Copenhagen, DK  •  200–500  •  Series B  •  2016     │  │
│ │       Tech: Python, TypeScript, React, K8s, AWS, PostgreSQL│  │
│ │       Culture: Mission-driven, clinical impact, remote OK  │  │
│ │       [Website] [LinkedIn] [Glassdoor] [Careers Page]      │  │
│ └─────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ ROLES MATCHED TO DANIEL'S TARGETS                                 │
│  Filter: [All ▼] [AI/ML ▼] [Frontend ▼] [Full-Stack ▼]          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Senior AI Engineer              Match: 92%  🟢             │ │
│  │ Python, LLMs, RAG, K8s, AWS     Salary: 60–75k DKK/mo     │ │
│  │ Posted: 2 weeks ago  •  Hybrid (CPH)  •  [View Details]    │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ML Platform Engineer            Match: 78%  🟡             │ │
│  │ Python, K8s, MLOps, Terraform   Salary: 55–70k DKK/mo     │ │
│  │ Posted: 1 month ago  •  Onsite (CPH)  •  [View Details]    │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ SALARY AT THIS COMPANY vs MARKET                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │          Corti AI Engineer          Market Median          │  │
│  │    ┌─────────────┐               ┌─────────────┐           │  │
│  │    │ ████████████│ 65k DKK       │ ██████████  │ 60k DKK   │  │
│  │    │ p25 58k     │               │ p25 55k     │           │  │
│  │    │ p50 65k     │               │ p50 60k     │           │  │
│  │    │ p75 75k     │               │ p75 68k     │           │  │
│  │    └─────────────┘               └─────────────┘           │  │
│  │    +8% above market  •  Top quartile                       │  │
│  └────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ CULTURE FIT SCORE                                                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ CULTURE FIT:  84 / 100          [score-ring 64px]          │  │
│  │                                                              │  │
│  │  ✅ Mission alignment (healthcare AI)     Weight: 30%      │  │
│  │  ✅ Remote-friendly policy                Weight: 20%      │  │
│  │  ✅ Engineering-driven culture            Weight: 20%      │  │
│  │  ⚠️  Onsite bias (hybrid ≠ remote)        Weight: 15%      │  │
│  │  ⚠️  Danish language preferred            Weight: 15%      │  │
│  │                                                              │  │
│  │  [View full breakdown]  [Compare to my profile]            │  │
│  └────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ DIRECT APPLICATION                                                │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  [Generate tailored CV]  [Generate cover letter]  [Apply]  │  │
│  │  Pre-filled with: AI Engineer role, Corti keywords,        │  │
│  │  Daniel's LLM/RAG experience, Danish location              │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Specifications

#### Company Profile Card
- **Component:** `.panel` with `.toolbar` header (back button + priority badge)
- **Priority badge:** `.tag-violet` with star icons (1–5)
- **Hiring temperature:** `.tag-red`/`.tag-amber`/`.tag-gray` inline
- **Tech stack:** Chips using `.tag-blue` for each technology
- **Links:** `.toolbar-btn` style for external links

#### Roles Matched Table
- **Component:** `.table-responsive` (desktop table → mobile cards)
- **Columns:** Role, Match Score (`.score-ring` 32px), Salary, Location, Posted, Action
- **Match score color:** ≥85% green, 70–84% amber, <70% red (via `.tag-*` on score ring)
- **Sortable:** Click column headers (client-side sort)
- **Empty state:** `.empty-row` "No matching roles for current filter"

#### Salary Comparison
- **Component:** Side-by-side horizontal bar charts (pure CSS)
- **Bars:** `--grade-high` for company, `--text-muted` for market
- **Labels:** Monospace numbers, p25/p50/p75 stacked
- **Delta badge:** `.tag-green` if company > market, `.tag-amber` if close, `.tag-red` if below

#### Culture Fit Score
- **Component:** Large `.score-ring` (64px) + weighted factor list
- **Factors:** Each row = factor name + weight + status icon (✅/⚠️/❌)
- **Weights sum to 100%**, displayed as percentage
- **Click "View full breakdown"** → modal with detailed scoring rubric

#### Direct Application Toolbar
- **Component:** `.toolbar` with 3 primary actions
- **Buttons:** `.toolbar-btn-primary` for Generate CV/Cover Letter, `.toolbar-btn` for Apply
- **Apply** → opens company careers page in new tab with UTM params

### 3.3 Interaction Flows
| Trigger | Action |
|---------|--------|
| Role row click | Open role detail modal (description, requirements, match breakdown) |
| Priority dropdown change | PATCH `/api/companies/{slug}/priority` → update badge |
| Generate CV click | POST `/api/cv/generate` with company+role context → return PDF blob |
| Culture factor click | Expand row with evidence (Glassdoor quotes, employee reviews) |
| Back button | `history.back()` to Market Overview with scroll position restored |

### 3.4 Mobile Adaptations
- Profile card: stacked, logo above name
- Roles: card layout (`.table-responsive`)
- Salary comparison: stacked bars, delta prominent
- Culture fit: ring 56px, factors in `.panel-scroll`
- Toolbar: 2-row (Generate CV + Cover Letter on row 1, Apply on row 2)

---

## 4. Page 3 — CV Score Detail (Integrated into `/evaluate/result`)

### 4.1 Integration Point
Extends existing evaluate result page. New section inserted **after** the main grade breakdown, **before** the action buttons.

### 4.2 Layout Addition
```
┌─────────────────────────────────────────────────────────────────┐
│ EXISTING: Grade breakdown (A–G blocks, score rings)             │
├─────────────────────────────────────────────────────────────────┤
│ NEW: MARKET SCORE BADGE                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  MARKET FIT:  82 / 100          [score-ring 48px]  STRONG  │ │
│  │  ████████████████████░░░░░░  Top 20% for AI Engineer in DK  │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ NEW: GAP ANALYSIS (expandable)                                   │
│  ▼ Skill Gaps vs. Market Demand                    [Expand All] │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 🔴 AWS Cloud              Missing entirely                │ │
│  │    Market demand: 37.7%  •  Top 10 companies require it   │ │
│  │    [Fix: Add "AWS Cloud Practitioner (in progress)"]      │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ 🔴 Kubernetes             Missing entirely                │ │
│  │    Market demand: 24.6%  •  Required for Platform roles   │ │
│  │    [Fix: Start CKAD path — 8 weeks]                       │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ 🟡 CI/CD (GitHub Actions)   Implicit only                 │ │
│  │    Market demand: 8.7%  •  Easy win — add workflow file   │ │
│  │    [Fix: Add .github/workflows/ci.yml to Career Ops repo] │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │ 🟢 LLM/RAG Patterns         Strong — already on CV        │ │
│  │    Market demand: 15%+  •  Differentiator, keep prominent │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ NEW: COMPANY-SPECIFIC FIT (when evaluating for a company)        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Evaluating for: Corti — AI Engineer                       │ │
│  │  COMPANY FIT:  91 / 100         [score-ring 48px]          │ │
│  │                                                              │ │
│  │  ✅ Python + LLMs + RAG          (exact match)             │ │
│  │  ✅ TypeScript + React           (exact match)             │ │
│  │  ⚠️  Kubernetes                  (missing — they use K8s)  │ │
│  │  ⚠️  AWS                         (missing — they use AWS)  │ │
│  │  ✅ Healthcare domain interest   (matches mission)         │ │
│  │  ✅ Danish native                (culture fit)             │ │
│  │                                                              │ │
│  │  [Generate tailored CV for Corti]  [Generate cover letter] │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ EXISTING: Action buttons (Download PDF, Regenerate, etc.)       │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Component Specifications

#### Market Score Badge
- **Component:** Inline `.section-header` style with `.score-ring` (48px)
- **Label:** "MARKET FIT" + score + tier badge (`.tag-green` Excellent, `.tag-amber` Strong, etc.)
- **Subtext:** Percentile context from market scoring formula (Section 5.2 of profile)

#### Gap Analysis Panel
- **Component:** `.panel` with collapsible sections (native `<details>` + `<summary>`)
- **Each gap row:**
  - Severity badge: `.tag-red`/`.tag-amber`/`.tag-green`
  - Skill name (bold)
  - Market demand % (monospace, muted)
  - Context line (why it matters)
  - **Fix action:** `.toolbar-btn` style inline button → copies fix text to clipboard + scrolls to CV editor
- **Expand/collapse:** Smooth `max-height` transition (CSS only)

#### Company-Specific Fit
- **Trigger:** Only renders when `?company=corti` query param present (from deep-dive "Generate tailored CV")
- **Component:** `.panel` with `.score-ring` + factor list + 2 CTAs
- **Factors:** Checkmarks (✅) for matches, warning (⚠️) for gaps, sourced from company profile + Daniel's skills
- **CTAs:** Primary `.toolbar-btn-primary` → POST to CV generator with company context

### 4.4 Interaction Flows
| Trigger | Action |
|---------|--------|
| Gap "Fix" button click | `navigator.clipboard.writeText(fixText)` → toast "Copied to clipboard" |
| Expand gap section | CSS `max-height` transition (300ms ease) |
| Company fit CTA click | `fetch('/api/cv/generate', {company, role})` → blob → download |
| Market score ring hover | Tooltip with formula breakdown (CSS-only) |

### 4.5 Mobile Adaptations
- Market badge: full-width, ring 56px
- Gap panels: full-width, no max-height when expanded
- Company fit: stacked CTAs (Generate CV on row 1, Cover Letter on row 2)

---

## 5. Data Contracts (API Shapes)

### 5.1 GET `/api/market/overview`
```json
{
  "marketHealth": { "score": 72, "trendPct": 4.2, "sparkline": [68,70,69,71,72,73,72] },
  "skillDemand": [
    { "skill": "TypeScript", "category": "frontend", "pct": 27.5, "gap": "none" },
    { "skill": "AWS", "category": "cloud", "pct": 37.7, "gap": "high" },
    { "skill": "Kubernetes", "category": "devops", "pct": 24.6, "gap": "high" }
  ],
  "salaryRanges": {
    "AI Engineer": { "locations": { "Copenhagen": { "p25": 55000, "p50": 65000, "p75": 75000 } } },
    "Frontend Engineer": { "locations": { "Copenhagen": { "p25": 50000, "p50": 58000, "p75": 65000 } } }
  },
  "companies": [
    { "slug": "corti", "name": "Corti", "logo": "/logos/corti.svg", "temperature": "hot", "openRoles": 5, "topRoles": ["AI Engineer", "ML Engineer"], "medianSalary": 60000, "location": "Copenhagen", "priority": 5 }
  ],
  "skillGaps": [
    { "skill": "AWS", "severity": "high", "marketPct": 37.7, "action": "Add \"AWS Cloud Practitioner (in progress)\"" },
    { "skill": "Kubernetes", "severity": "high", "marketPct": 24.6, "action": "Start CKAD path — 8 weeks" }
  ]
}
```

### 5.2 GET `/api/market/company/{slug}`
```json
{
  "profile": {
    "name": "Corti", "logo": "/logos/corti.svg", "location": "Copenhagen, DK",
    "size": "200-500", "funding": "Series B", "founded": 2016,
    "techStack": ["Python", "TypeScript", "React", "Kubernetes", "AWS", "PostgreSQL"],
    "culture": "Mission-driven, clinical impact, remote OK",
    "links": { "website": "...", "linkedin": "...", "glassdoor": "...", "careers": "..." }
  },
  "matchedRoles": [
    { "title": "Senior AI Engineer", "matchScore": 92, "salary": { "min": 55000, "median": 65000, "max": 75000 }, "location": "Copenhagen", "postedDaysAgo": 14, "workMode": "hybrid", "requirements": ["Python", "LLMs", "RAG", "K8s", "AWS"] }
  ],
  "salaryComparison": {
    "company": { "p25": 58000, "p50": 65000, "p75": 75000 },
    "market": { "p25": 55000, "p50": 60000, "p75": 68000 },
    "deltaPct": 8
  },
  "cultureFit": {
    "score": 84,
    "factors": [
      { "name": "Mission alignment", "weight": 0.30, "status": "match" },
      { "name": "Remote-friendly", "weight": 0.20, "status": "match" },
      { "name": "Engineering-driven", "weight": 0.20, "status": "match" },
      { "name": "Onsite bias", "weight": 0.15, "status": "gap" },
      { "name": "Danish language preferred", "weight": 0.15, "status": "gap" }
    ]
  }
}
```

### 5.3 GET `/api/cv/market-score?cvId=...&company=corti`
```json
{
  "marketScore": 82,
  "tier": "Strong",
  "percentile": "Top 20%",
  "breakdown": {
    "skillMatch": 26, "aiSpecialization": 15, "experience": 15, "danish": 10, "format": 7, "tone": 7
  },
  "gaps": [
    { "skill": "AWS", "severity": "high", "marketPct": 37.7, "fix": "Add \"AWS Cloud Practitioner (in progress)\"" },
    { "skill": "Kubernetes", "severity": "high", "marketPct": 24.6, "fix": "Start CKAD path — 8 weeks" }
  ],
  "companyFit": {
    "score": 91,
    "matched": ["Python", "LLMs", "RAG", "TypeScript", "React", "Healthcare interest", "Danish native"],
    "gaps": ["Kubernetes", "AWS"]
  }
}
```

---

## 6. Implementation Checklist

### 6.1 Page 1 — `/market`
- [ ] Astro page route `src/pages/market.astro`
- [ ] Client-side JS module `src/scripts/market-overview.js` (fetch, render, filter handlers)
- [ ] API endpoint `GET /api/market/overview` (reads from `data/research/` JSON + computes health score)
- [ ] Reuse: `.toolbar`, `.filter-bar`, `.score-ring`, `.sparkline` (adapted), `.panel`, `.card-interactive`, `.tag-*`, `.table-responsive`
- [ ] Mobile: CSS grid auto-fit + scroll-snap on company grid

### 6.2 Page 2 — `/market/company/[slug]`
- [ ] Astro dynamic route `src/pages/market/company/[slug].astro`
- [ ] Client module `src/scripts/company-deep-dive.js`
- [ ] API endpoint `GET /api/market/company/:slug`
- [ ] API endpoint `PATCH /api/market/company/:slug/priority`
- [ ] Reuse: `.toolbar`, `.table-responsive`, `.score-ring`, `.tag-*`, `.panel`, `.panel-scroll`
- [ ] Modal for role detail (lightweight, no lib — `<dialog>` element)

### 6.3 Page 3 — `/evaluate/result` (integration)
- [ ] Modify existing result page Astro component
- [ ] Add market score section (conditional render when market data available)
- [ ] Add gap analysis panel (collapsible `<details>`)
- [ ] Add company-fit panel (conditional on `?company=` query)
- [ ] Client module `src/scripts/cv-market-score.js`
- [ ] API endpoint `GET /api/cv/market-score` (implements formula from profile.md Section 5.1)

### 6.4 Shared
- [ ] TypeScript types for all API contracts (`src/types/market.ts`)
- [ ] CSS: no new custom properties needed — all reuse existing tokens
- [ ] Add company logos to `public/logos/` (SVG, 24×24)
- [ ] Skeleton loading states for all async sections (`.skeleton`, `.skeleton-text`, `.skeleton-card`)

---

## 7. Design Token Extensions (If Needed)

Only **one** new token category required:

```css
/* Category colors for skill demand bars — add to globals.css @theme */
--cat-frontend: #D4A853;   /* accent-primary */
--cat-backend: #3b82f6;    /* info */
--cat-devops: #22c55e;     /* success */
--cat-cloud: #eab308;      /* warning */
--cat-data: #a855f7;       /* violet (new) */
--cat-core: #64748b;       /* text-muted */
```

All other visual language derives from existing system.

---

## 8. Acceptance Criteria Checklist

| Criterion | Page 1 | Page 2 | Page 3 |
|-----------|--------|--------|--------|
| All 3 pages specified with layout descriptions | ✅ | ✅ | ✅ |
| Component reuse mapped to existing CSS classes | ✅ | ✅ | ✅ |
| Interaction flows documented | ✅ | ✅ | ✅ |
| Mobile layout considered | ✅ | ✅ | ✅ |
| Design tokens from existing system used | ✅ | ✅ | ✅ |
| Output file created at `/opt/career-ops-dashboard/data/research/ux-market-spec.md` | ✅ | | |

---

*Generated by Rune — Career Ops Dashboard T4.1 UX Spec*