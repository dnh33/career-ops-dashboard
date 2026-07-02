# Career Ops Dashboard — Full Application Revamp Goal Prompt
**Authoritative Source:** `DESIGN_SYSTEM_FOUNDATION.md` (this repo)  
**Target:** Every element, page, UX pattern, and interaction → Forbes 100 / "KommandoCentralen" caliber  
**Mode:** Zero-slop, skill-enforced, token-governed, signature-moment-driven

---

## 🎯 MISSION

**Revamp the entire Career Ops Dashboard frontend** — all pages, components, interactions, and UX flows — to strictly conform to the **Aesthetic Foundation Document** (`DESIGN_SYSTEM_FOUNDATION.md`). No exceptions. No "good enough." Every pixel must earn its place in a product that Danish devs trust as their market intelligence command center, and that could scale to a broader platform.

**Quality bar:** Linear / Vercel / Stripe Dashboard / Hermes Agent dark observatory.  
**Forbidden:** Startup template aesthetics, AI-default fonts, decorative gradients, numbered markers, bounce easing, generic Inter-as-display, marketing fluff copy.

---

## 📋 SCOPE: WHAT MUST BE REVAMPED

### Pages (10+ current → all must pass verification gates)
| Page | Status | Required Patterns |
|------|--------|-------------------|
| `src/pages/index.astro` | Dashboard home | PageLayout, Signal Cards, CommandLineBar, Theme/Density switchers |
| `src/pages/market.astro` | Market Overview | **T4.1 fix**: remove `client:load`, Radar Sweep, Signal Cards, Cmd+K |
| `src/pages/market/skill-gap.astro` | Skill Gap Radar | **T4.2**: Radar Sweep signature moment, grade-colored rings |
| `src/pages/market/company/[slug].astro` | Company Deep-Dive | **T4.3**: Ring + Table, Signal Cards, Cmd+K prefill |
| `src/pages/companies.astro` | Companies index | PageLayout, dense DataTable, FilterBar, Signal Cards |
| `src/pages/cv/builder.astro` | CV Builder | Progressive disclosure, Signal Cards, command palette actions |
| `src/pages/cv/optimize.astro` | CV Optimizer | Radar Sweep for skill gaps, Cmd+K for rules |
| `src/pages/scan.astro` | Scan/Import | PageLayout, upload flow, Signal Card results |
| `src/pages/tracker.astro` | Application Tracker | Dense table, inline actions, filter chips, density toggle |
| `src/pages/pipeline.astro` | Pipeline | Kanban → convert to dense table + Signal Cards |
| `src/pages/reports.astro` | Reports | Signal Cards, Radar Sweep, export actions |
| `src/pages/evaluate.astro` | Evaluate | Company deep-dive pattern, Signal Cards |
| `src/pages/profile.astro` | Profile | PageLayout, Signal Cards, theme/density persist |
| `src/pages/settings.astro` | Settings | ThemeSwitcher, DensitySwitcher, API budget display |
| `src/pages/tools.astro` | Tools | Command palette as primary nav, Signal Cards |
| `src/pages/output.astro` | Output/Export | Dense preview, Signal Cards, Cmd+K actions |

### Components (All must enforce aesthetic rules by construction)
| Category | Components | Enforcement |
|----------|------------|-------------|
| **UI Primitives** | Button, Card, DataTable, Switch, SegmentedControl, StatusPill, Badge, TabNav, TextInput, SearchField, ProgressBar, Sparkline, ScoreBadge, MetricCard, EmptyState, Loader, ErrorState, Overlay, CodeBlock | Base layer rules, MutationObserver hierarchy, semantic tokens only |
| **Layout** | PageLayout, Sidebar, TopBar, Breadcrumb, BrandMark, ThemeToggle, UserAvatar, Nav, FilterBar, CommandLineBar | Slots + injection points, registry-ready |
| **Market** | MarketScoreBadge, GapAnalysisPanel, SkillGapRadar, CompanyDeepDive | Signature moments (Radar Sweep, Signal Card) |
| **CV** | OptimizationPanel | Progressive disclosure, Signal Cards |

### Interactions & UX Patterns (All must be rebuilt to spec)
| Pattern | Spec Reference | Implementation |
|---------|----------------|----------------|
| **Cmd+K Command Palette** | §1.3, §3.3.2, §5 | Global listener in PageLayout, registry-loaded, fuzzy search over skills/companies/actions |
| **Radar Sweep Animation** | §1.3, §3.3.1, §5 | `skill-gap-radar.js` — grade rings, `prefers-reduced-motion`, token-driven |
| **Signal Card Atomic Unit** | §1.3, §3.3.3, §5 | `Card.astro` + MutationObserver, grade badge, signal dot, radar-mini slot |
| **Progressive Disclosure (3-layer)** | §1.3 | Layer 0: 4 stats + filter chips + top 20 rows; Layer 1: row click → drawer; Layer 2: density/theme/export/Deep-Dive |
| **Density Toggle** | §3.2, §5 | `DensitySwitcher` → `[data-density]` on `<html>`, persists localStorage |
| **Theme Toggle** | §3.1, §5 | `ThemeSwitcher` → `[data-theme]` on `<html>`, 4 variants, persists localStorage |
| **API Budget Guard** | §3.5, §5 | `requestBudget({component, cost, priority})` — max 100, evicts low priority |
| **Component Registry** | §3.4, §5 | `registerComponent('name', {init})` + `<div data-component="name" />` declarative |
| **PageLayout Slots** | §3.3, §5 | hero, sidebar, breadcrumbs, actions, footer + modal/toast/drawer roots + `pagelayout:ready` event |
| **Filter Bar** | §1.3, Execution Architect | Horizontal scrollable chips, no wrapping, instant client-side filter (<1000 items) |

---

## ⚙️ EXECUTION PROTOCOL

### Phase 0: Foundation Lock (Do First — Blocks Everything)
```bash
# 1. Fix globals.css bugs (T4.1)
#    - @theme: --color-heading: var(--color-slate-900)
#    - base h1-h6: color: var(--color-heading)
#    - base a:not([class*="text-"]) { color: var(--accent-primary); }
# 2. Run token audit
npx tsx scripts/audit-tokens.ts src/
# 3. Verify gates pass
npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build
```
**Gate:** All 4 audits pass + build clean. No further work until this passes.

### Phase 1: Signature Moments Implementation (T4.2 + T4.3 Core)
**Parallelizable — dispatch as separate Cursor tasks with full skill load:**

| Task | Files to Create/Modify | Skill Bundle (Mandatory) |
|------|------------------------|--------------------------|
| **Radar Sweep** | `src/components/skill-gap-radar.js`, `src/components/skill-gap.astro`, `registry.ts` | `frontend-design`, `design-tokens`, `impeccable`, `writing/anti-slop-audit`, `hermes-agent-skill-authoring` |
| **Cmd+K Command Palette** | `src/components/command-palette.js`, `src/components/command-palette.astro`, `registry.ts`, `PageLayout.astro` (global listener) | Same bundle |
| **Signal Card Enhancement** | `src/components/ui/Card.astro` (grade badge, signal dot, radar-mini slot), `registry.ts` | Same bundle |
| **ThemeSwitcher** | `src/components/ui/ThemeSwitcher.astro`, `theme-switcher.js` | `design-tokens`, `frontend-design`, `impeccable` |
| **DensitySwitcher** | `src/components/ui/DensitySwitcher.astro` | Same |
| **PageLayout v2** | `src/components/layout/PageLayout.astro` (slots + injection roots + `pagelayout:ready`) | `frontend-design`, `design-tokens` |
| **CommandLineBar** | `src/components/layout/CommandLineBar.astro` (theme/density/budget display) | `frontend-design`, `design-tokens` |
| **API Budget Guard** | `src/lib/api-budget.ts` + integrate into radar/deep-dive modules | `frontend-design`, `impeccable` |
| **Component Registry** | `src/components/registry.ts` (type-safe, auto-init on `pagelayout:ready`) | `frontend-design`, `hermes-agent-skill-authoring` |

**Each task body MUST include the full template from `DESIGN_SYSTEM_FOUNDATION.md` §2.2** — checkbox gates included.

### Phase 2: Page-by-Page Revamp (Sequential or Parallel with Dependency Order)
**Dependency order:** `PageLayout` + `CommandLineBar` + `Theme/Density` + `Registry` → all pages.

For **EACH page** — dispatch Cursor task with:

```markdown
## Task: Revamp [page-name] to Aesthetic Foundation Spec

### Skills Loaded
- hermes-agent-skill-authoring
- design-tokens
- frontend-design
- impeccable
- writing/anti-slop-audit

### Non-Negotiable Constraints (Foundation §1)
- [ ] Zero hardcoded values — only Tailwind utilities from globals.css @theme
- [ ] h1-h3 = text-heading, p = text-body, secondary = text-muted
- [ ] Accent gold = max 1-2 words/section via .accent-gold
- [ ] Module scripts only — NO inline onclick
- [ ] focus-visible = gold ring (base CSS)
- [ ] prefers-reduced-motion respected (base CSS)
- [ ] JS reads tokens via getComputedStyle('--token')

### Page-Specific Requirements
- [ ] Wrap in <PageLayout> with appropriate slots (hero, sidebar, actions, etc.)
- [ ] Register feature components via data-component attributes
- [ ] Use Signal Card for all data displays
- [ ] Integrate Cmd+K command palette actions relevant to page
- [ ] Radar Sweep where skill gaps shown
- [ ] FilterBar with horizontal chips for any tabular data
- [ ] Density/Theme switchers accessible via CommandLineBar
- [ ] API budget declared for all fetch calls

### Verification Gates (MUST PASS)
npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build
```

### Phase 3: Legacy Page Migration (9 Pages — Batch Process)
**Script-driven, then human QA per page:**

```bash
# For each legacy page in src/pages/legacy/*.astro:
npx tsx scripts/audit-tokens.ts src/pages/legacy/[page].astro
npx tsx scripts/migrate-page.ts src/pages/legacy/[page].astro
# Human review: visual regression, interaction parity, token compliance
npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build
```

**Migration checklist per page (from Foundation §3.6):**
1. Token audit → map hardcoded → semantic tokens
2. Component extraction → `src/components/ui/` + registry
3. Layout migration → wrap in `<PageLayout>`
4. JS module migration → `src/components/[feature].js` + module script
5. Data passing → `data-*` JSON attributes
6. Verification gates (4 audits + build)

### Phase 4: Cross-Cutting Polish (After All Pages Pass Gates)
- **Micro-interactions:** stagger entrance animations (`animate-fade-in`, `animate-slide-up`), hover states on Signal Cards, focus transitions
- **Command palette completeness:** index all skills, companies, actions, report types, settings
- **Empty states:** honest, actionable (no "no data" — "No Copenhagen React roles >600k yet. Adjust filter or cmd+k: cop react ts >500k")
- **Loading states:** skeleton screens matching density, not spinners
- **Error states:** Signal Card variant with `--grade-low` border, retry action via Cmd+K prefill
- **Keyboard navigation:** full tab order, arrow keys in tables/radar, Esc closes drawers/modals
- **Screen reader:** `aria-label` on radar rings, live regions for filter results, landmarks
- **Performance:** bundle analysis, lazy-load radar/command-palette/deep-dive via registry, API budget respected

---

## 🛡️ QUALITY GATES — NO MERGES WITHOUT

```bash
# Run in CI and locally before ANY PR merge
npm run audit:tokens        # 0 hardcoded hex/rgb/px in .astro/.js/.css (except globals.css primitives)
npm run audit:accessibility # cursor-pointer on all interactive, focus-visible gold ring, contrast WCAG AA
npm run audit:consistency   # 0 arbitrary rounded/p/gap/shadow values — only token-mapped
npm run build               # Astro + TypeScript clean
npm run test:e2e            # Playwright: Cmd+K opens, radar animates, theme/density persist, budget enforced
npm run test:visual         # Percy/Chromatic: no regressions vs approved baselines
```

---

## 📦 DELIVERABLES

1. **Every page** passes all 4 automated audits + build + e2e + visual regression
2. **Signature moments** working: Radar Sweep, Cmd+K Signal, Signal Card — recognizable as "this product"
3. **Growth hooks active:** theme/density persist, component registry loads features declaratively, API budget enforced
4. **Zero slop:** anti-slop-audit passes on all copy (Name Swap Test, Janteloven Credibility, Hygge-Hustle Directness)
5. **Documentation updated:** `DESIGN_SYSTEM_FOUNDATION.md` stays authoritative; component READMEs for each UI primitive

---

## 🚀 HOW TO RUN THIS

**For orchestrators:** Split into Cursor tasks per Phase 1 item + Phase 2 page + Phase 3 batch.  
**For Cursor workers:** Paste the task template from Phase 1/2 above — skills load automatically via task body.  
**For human review:** Verify gates pass, then spot-check: "Does this feel like Linear/Vercel/Stripe/Hermes?" and "Does a Danish dev trust this at first glance?"

---

## 🎖️ SUCCESS DEFINITION

> A Danish Frontend/AI engineer opens the dashboard at 11 PM, hits `Cmd+K`, types `cph react ts >600k`, gets a Signal Card per company with salary bands, stack reality, hiring manager names — then switches to `skill-gap` page, sees Radar Sweep animate their TypeScript/Rust gaps in emerald/amber/red, toggles density to `compact`, theme to `high-contrast`, and thinks: **"This is built for me. This is a command center. I trust this."**

That is Forbes 100. That is KommandoCentralen. That is the bar.

---

**Reference:** `DESIGN_SYSTEM_FOUNDATION.md` (this repo) — every rule, token, pattern, and gate defined there is law.