# Career Ops Dashboard — Full Revamp Kanban Board

## Phase 0: Foundation Lock (BLOCKS ALL)
| Task | Status | Assignee | Files | Verification |
|------|--------|----------|-------|--------------|
| T0.1 Fix globals.css @theme block (3 bugs) | 🔴 READY | cursor | `src/styles/globals.css` | audit:tokens, build |
| T0.2 Replace all hardcoded values in .astro/.js/.css | 🔴 READY | cursor | All src/ | audit:tokens |
| T0.3 Add audit scripts (audit-tokens.ts, migrate-page.ts) | 🔴 READY | cursor | `scripts/` | audit:tokens passes |
| T0.4 Run all 4 gates | 🔴 READY | cursor | - | ALL PASS |

## Phase 1: Signature Moments (PARALLEL)
| Task | Status | Assignee | Files | Skills |
|------|--------|----------|-------|--------|
| T1.1 Radar Sweep (skill-gap-radar.js + skill-gap.astro + registry) | 🔴 READY | cursor | `src/components/skill-gap-radar.js`, `src/components/skill-gap.astro`, `src/components/registry.ts` | hermes-agent-skill-authoring, design-tokens, frontend-design, impeccable, writing/anti-slop-audit |
| T1.2 Cmd+K Command Palette (command-palette.js + .astro + registry + PageLayout listener) | 🔴 READY | cursor | `src/components/command-palette.js`, `src/components/command-palette.astro`, `src/components/registry.ts`, `src/components/layout/PageLayout.astro` | Same bundle |
| T1.3 Signal Card Enhancement (Card.astro + MutationObserver + grade badge + signal dot + radar-mini) | 🔴 READY | cursor | `src/components/ui/Card.astro`, `src/components/registry.ts` | Same bundle |
| T1.4 ThemeSwitcher (ThemeSwitcher.astro + theme-switcher.js) | 🔴 READY | cursor | `src/components/ui/.../ui/ThemeSwitcher.astro`, `src/scripts/theme-switcher.js` | design-tokens, frontend-design, impeccable |
| T1.5 DensitySwitcher (DensitySwitcher.astro) | 🔴 READY | cursor | `src/components/ui/DensitySwitcher.astro` | Same |
| T1.6 PageLayout v2 (slots + injection roots + pagelayout:ready event) | 🔴 READY | cursor | `src/components/layout/PageLayout.astro` | frontend-design, design-tokens |
| T1.7 CommandLineBar (theme/density/budget display) | 🔴 READY | cursor | `src/components/layout/CommandLineBar.astro` | frontend-design, design-tokens |
| T1.8 API Budget Guard (api-budget.ts + integrate) | 🔴 READY | cursor | `src/lib/api-budget.ts`, radar/deep-dive modules | frontend-design, impeccable |
| T1.9 Component Registry (type-safe, auto-init on pagelayout:ready) | 🔴 READY | cursor | `src/components/registry.ts` | frontend-design, hermes-agent-skill-authoring |

## Phase 2: Page-by-Page Revamp (DEPENDENCY ORDER)
| Task | Status | Assignee | Depends On |
|------|--------|----------|------------|
| T2.1 index.astro (Dashboard home) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.2 market.astro (Market Overview) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.3 market/skill-gap.astro (Skill Gap Radar) | 🔴 READY | cursor | T1.1, T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.4 market/company/[slug].astro (Company Deep-Dive) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.5 companies.astro (Companies index) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.6 cv/builder.astro (CV Builder) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.7 cv/optimize.astro (CV Optimizer) | 🔴 READY | cursor | T1.1, T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.8 scan.astro (Scan/Import) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.9 tracker.astro (Application Tracker) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.10 pipeline.astro (Pipeline) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.11 reports.astro (Reports) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.12 evaluate.astro (Evaluate) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.13 profile.astro (Profile) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.14 settings.astro (Settings) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.15 tools.astro (Tools) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |
| T2.16 output.astro (Output/Export) | 🔴 READY | cursor | T1.6, T1.7, T1.4, T1.5, T1.9 |

## Phase 3: Legacy Migration (BATCH)
| Task | Status | Assignee |
|------|--------|----------|
| T3.1 Legacy pages audit + migration (9 pages) | 🔴 READY | cursor |

## Phase 4: Cross-Cutting Polish
| Task | Status | Assignee |
|------|--------|----------|
| T4.1 Micro-interactions (stagger, hover, focus) | 🔴 READY | cursor |
| T4.2 Command palette completeness | 🔴 READY | cursor |
| T4.3 Empty states (honest, actionable) | 🔴 READY | cursor |
| T4.4 Loading states (skeletons) | 🔴 READY | cursor |
| T4.5 Error states (Signal Card variant) | 🔴 READY | cursor |
| T4.6 Keyboard navigation (full tab order) | 🔴 READY | cursor |
| T4.7 Screen reader (aria, live regions) | 🔴 READY | cursor |
| T4.8 Performance (bundle analysis, lazy load) | 🔴 READY | cursor |

## Quality Gates (MUST PASS BEFORE ANY MERGE)
- `npm run audit:tokens` — 0 hardcoded values
- `npm run audit:accessibility` — cursor-pointer, focus-visible, contrast
- `npm run audit:consistency` — 0 arbitrary rounded/p/gap/shadow values
- `npm run build` — Astro + TypeScript clean
- `npm run test:e2e` — Playwright: Cmd+K, radar, theme/density persist, budget
- `npm run test:visual` — Percy/Chromatic: no regressions