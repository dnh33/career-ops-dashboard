# Career Ops Dashboard — Full Application Revamp Kanban Board

## Phase 0: Foundation Lock (Blocks Everything)

### T4.1 Fix - Token Audit & CSS Bug Resolution
- [ ] Fix globals.css @theme block: `--color-heading: var(--color-slate-900)` (DONE)
- [ ] Fix base h1-h6 rule: `color: var(--color-heading)` (DONE)  
- [ ] Fix base a rule: `a:not([class*="text-"]) { color: var(--accent-primary); }` (DONE)
- [ ] Run token audit: `npx tsx scripts/audit-tokens.ts src/` (IN PROGRESS - 1431 violations remaining)
- [ ] Verify all 4 audits pass: `npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build`

## Phase 1: Signature Moments Implementation (Parallelizable)

### Radar Sweep (Skill-Gap Radar) - T4.2.1
- [x] Create `src/components/skill-gap-radar.js` (COMPLETE)
- [x] Create `src/components/market/SkillGapRadar.astro` wrapper (COMPLETE)
- [x] Register component in `registry.ts` (PENDING)
- [x] Integrate into `src/pages/market/skill-gap.astro` (COMPLETE)

### Cmd+K Command Palette - T4.2.2
- [x] Create `src/scripts/command-palette.js` (COMPLETE)
- [x] Create `src/components/ui/CommandPalette.astro` (COMPLETE)
- [x] Register component in `registry.ts` (PENDING)
- [x] Add global listener in `PageLayout.astro` (PENDING)

### Signal Card Enhancement - T4.2.3
- [ ] Enhance `src/components/ui/Card.astro` with grade badge variant
- [ ] Add signal indicator dot
- [ ] Add radar-mini slot
- [ ] Register component in `registry.ts` (PENDING)

### ThemeSwitcher - T4.3.1
- [x] Create `src/components/ui/ThemeSwitcher.astro` (COMPLETE)
- [x] Verify functionality (NEEDS TESTING)

### DensitySwitcher - T4.3.2
- [x] Create `src/components/ui/DensitySwitcher.astro` (COMPLETE)
- [x] Verify functionality (NEEDS TESTING)

### PageLayout v2 - T4.3.3
- [x] Update `src/components/layout/PageLayout.astro` with slots + injection roots (COMPLETE)
- [x] Add `pagelayout:ready` event (COMPLETE)

### CommandLineBar - T4.3.4
- [x] Create `src/components/layout/CommandLineBar.astro` (COMPLETE)
- [x] Integrate ThemeSwitcher and DensitySwitcher (COMPLETE)
- [x] Add API budget display (COMPLETE)

### API Budget Guard - T4.3.5
- [x] Create `src/lib/api-budget.ts` (EXISTS)
- [x] Integrate into radar/deep-dive modules (PENDING)

### Component Registry - T4.3.6
- [x] Ensure `src/components/registry.ts` is complete (COMPLETE)
- [x] Register all components (PENDING)

## Phase 2: Page-by-Page Revamp (Sequential or Parallel)

### Dependency Order: PageLayout + CommandLineBar + Theme/Density + Registry → all pages

#### Page: Dashboard Home (`src/pages/index.astro`)
- [ ] Wrap in `<PageLayout>` with appropriate slots
- [ ] Register feature components via data-component attributes
- [ ] Use Signal Card for all data displays
- [ ] Integrate Cmd+K command palette actions
- [ ] Add FilterBar for any tabular data
- [ ] Ensure Theme/Theme switchers accessible via CommandLineBar
- [ ] Declare API budget for all fetch calls

#### Page: Market Overview (`src/pages/market.astro`)
- [ ] T4.1 fix: Remove `client:load` directives
- [ ] Implement Radar Sweep signature moment
- [ ] Add Signal Cards
- [ ] Add Cmd+K integration
- [ ] Add FilterBar
- [ ] Ensure Theme/Density switchers work

#### Page: Skill Gap Radar (`src/pages/market/skill-gap.astro`)
- [ ] T4.2: Implement Radar Sweep with grade-colored rings
- [ ] Ensure proper Signal Card usage
- [ ] Add Cmd+K integration
- [ ] Add FilterBar for tabular data views
- [ ] Ensure Theme/Density switchers work

#### Page: Company Deep-Dive (`src/pages/market/company/[slug].astro`)
- [ ] T4.3: Implement Ring + Table pattern
- [ ] Add Signal Cards
- [ ] Add Cmd+K with prefill
- [ ] Add FilterBar
- [ ] Ensure Theme/Density switchers work

#### Page: Companies Index (`src/pages/companies.astro`)
- [ ] Wrap in `<PageLayout>`
- [ ] Implement dense DataTable
- [ ] Add FilterBar
- [ ] Add Signal Cards
- [ ] Ensure Theme/Density switchers work

#### Page: CV Builder (`src/pages/cv/builder.astro`)
- [ ] Implement progressive disclosure (3-layer)
- [ ] Add Signal Cards
- [ ] Add Cmd+K for command palette actions
- [ ] Ensure Theme/Density switchers work

#### Page: CV Optimizer (`src/pages/cv/optimize.astro`)
- [ ] Implement Radar Sweep for skill gaps
- [ ] Add Cmd+K for rules access
- [ ] Add Signal Cards
- [ ] Ensure Theme/Density switchers work

#### Page: Scan/Import (`src/pages/scan.astro`)
- [ ] Wrap in `<PageLayout>`
- [ ] Implement upload flow
- [ ] Add Signal Card results
- [ ] Ensure Theme/Density switchers work

#### Page: Application Tracker (`src/pages/tracker.astro`)
- [ ] Implement dense table
- [ ] Add inline actions
- [ ] Add filter chips
- [ ] Add density toggle
- [ ] Ensure Theme/Density switchers work

#### Page: Pipeline (`src/pages/pipeline.astro`)
- [ ] Convert Kanban to dense table + Signal Cards
- [ ] Ensure Theme/Density switchers work

#### Page: Reports (`src/pages/reports.astro`)
- [ ] Add Signal Cards
- [ ] Add Radar Sweep where applicable
- [ ] Add export actions via Cmd+K
- [ ] Ensure Theme/Density switchers work

#### Page: Evaluate (`src/pages/evaluate.astro`)
- [ ] Implement company deep-dive pattern
- [ ] Add Signal Cards
- [ ] Ensure Theme/Density switchers work

#### Page: Profile (`src/pages/profile.astro`)
- [ ] Wrap in `<PageLayout>`
- [ ] Add Signal Cards
- [ ] Add ThemeSwitcher
- [ ] Add DensitySwitcher
- [ ] Ensure persistence

#### Page: Settings (`src/pages/settings.astro`)
- [ ] Add ThemeSwitcher
- [ ] Add DensitySwitcher
- [ ] Add API budget display
- [ ] Ensure Theme/Density switchers work

#### Page: Tools (`src/pages/tools.astro`)
- [ ] Implement Command palette as primary nav
- [ ] Add Signal Cards
- [ ] Ensure Theme/Density switchers work

#### Page: Output/Export (`src/pages/output.astro`)
- [ ] Implement dense preview
- [ ] Add Signal Cards
- [ ] Add Cmd+K actions
- [ ] Ensure Theme/Density switchers work

## Phase 3: Legacy Page Migration (9 Pages - Batch Process)

### Migration Script Execution
- [ ] For each legacy page in `src/pages/legacy/*.astro`:
  - [ ] Run token audit: `npx tsx scripts/audit-tokens.ts src/pages/legacy/[page].astro`
  - [ ] Run migration: `npx tsx scripts/migrate-page.ts src/pages/legacy/[page].astro`
  - [ ] Human review: visual regression, interaction parity, token compliance
  - [ ] Verify gates pass: `npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build`

## Phase 4: Cross-Cutting Polish (After All Pages Pass Gates)

### Micro-interactions
- [ ] Stagger entrance animations (`animate-fade-in`, `animate-slide-up`)
- [ ] Hover states on Signal Cards
- [ ] Focus transitions

### Command Palette Completeness
- [ ] Index all skills, companies, actions, report types, settings

### Empty States
- [ ] Honest, actionable messages (no "no data" - provide guidance)

### Loading States
- [ ] Skeleton screens matching density, not spinners

### Error States
- [ ] Signal Card variant with `--grade-low` border
- [ ] Retry action via Cmd+K prefill

### Keyboard Navigation
- [ ] Full tab order
- [ ] Arrow keys in tables/radar
- [ ] Esc closes drawers/modals

### Screen Reader Accessibility
- [ ] `aria-label` on radar rings
- [ ] Live regions for filter results
- [ ] Landmarks

### Performance
- [ ] Bundle analysis
- [ ] Lazy-load radar/command-palette/deep-dive via registry
- [ ] API budget respected

## Quality Gates - NO MERGES WITHOUT
- [ ] `npm run audit:tokens` (0 hardcoded hex/rgb/px in .astro/.js/.css except globals.css primitives)
- [ ] `npm run audit:accessibility` (cursor-pointer on all interactive, focus-visible gold ring, contrast WCAG AA)
- [ ] `npm run audit:consistency` (0 arbitrary rounded/p/gap/shadow values — only token-mapped)
- [ ] `npm run build` (Astro + TypeScript clean)
- [ ] `npm run test:e2e` (Playwright: Cmd+K opens, radar animates, theme/density persist, budget enforced)
- [ ] `npm run test:visual` (Percy/Chromatic: no regressions vs approved baselines)

## Deliverables
- [ ] Every page passes all 4 automated audits + build + e2e + visual regression
- [ ] Signature moments working: Radar Sweep, Cmd+K Signal, Signal Card
- [ ] Growth hooks active: theme/density persist, component registry loads features declaratively, API budget enforced
- [ ] Zero slop: anti-slop-audit passes on all copy (Name Swap Test, Janteloven Credibility, Hygge-Hustle Directness)
- [ ] Documentation updated: `DESIGN_SYSTEM_FOUNDATION.md` stays authoritative; component READMEs for each UI primitive

## Success Definition
> A Danish Frontend/AI engineer opens the dashboard at 11 PM, hits `Cmd+K`, types `cph react ts >600k`, gets a Signal Card per company with salary bands, stack reality, hiring manager names — then switches to `skill-gap` page, sees Radar Sweep animate their TypeScript/Rust gaps in emerald/amber/red, toggles density to `compact`, theme to `high-contrast`, and thinks: **"This is built for me. This is a command center. I trust this."** That is Forbes 100. That is KommandoCentralen. That is the bar.

## Current Status Summary
- **Phase 0**: IN PROGRESS (1431 token violations remaining)
- **Phase 1**: MOSTLY COMPLETE (components created, need registration and integration)
- **Phase 2**: NOT STARTED (awaiting Phase 0 completion)
- **Phase 3**: NOT STARTED (awaiting Phase 2 completion)
- **Phase 4**: NOT STARTED (awaiting Phase 3 completion)