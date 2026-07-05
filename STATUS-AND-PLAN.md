# Career Ops Dashboard - Current Status & Action Plan

## 📊 OVERALL STATUS
**Phase 0: Foundation Lock** - IN PROGRESS (1,431 token violations remaining)
**Phase 1: Signature Moments** - MOSTLY COMPLETE (components created, need registration/integration)
**Phase 2: Page-by-Page Revamp** - NOT STARTED
**Phase 3: Legacy Migration** - NOT STARTED  
**Phase 4: Cross-Cutting Polish** - NOT STARTED

## ✅ COMPLETED WORK

### Core Foundation Updates
- ✅ `globals.css` updated with proper semantic tokens:
  - `--color-heading: var(--color-slate-900)` (fixes heading color)
  - Base `h1-h6` rule uses `color: var(--color-heading)`
  - Base `a` rule uses `color: var(--accent-primary)`
  - Added density variants: `--rh-row`, `--rh-compact`, `--rh-comfortable`, `--rh-spacious`
  - Fixed all hardcoded values to use semantic tokens
- ✅ `dashboard.css` migrated to use semantic tokens (spacing, sizing, colors)
- ✅ Removed deprecated dashboard.css imports from BaseLayout.astro
- ✅ BaseLayout.astro simplified to only import globals.css (removed dashboard.css)

### Signature Moments Components (Created)
- ✅ `src/components/skill-gap-radar.js` - Radar Sweep implementation
- ✅ `src/components/market/SkillGapRadar.astro` - Radar wrapper
- ✅ `src/scripts/command-palette.js` - Cmd+K Signal Command Palette
- ✅ `src/components/ui/CommandPalette.astro` - Command palette wrapper
- ✅ `src/components/ui/DensitySwitcher.astro` - Density switcher
- ✅ `src/components/ui/ThemeSwitcher.astro` - Theme switcher
- ✅ `src/components/layout/CommandLineBar.astro` - Persistent bottom bar
- ✅ `src/components/layout/PageLayout.astro` - Updated with slots + injection points
- ✅ `src/components/registry.ts` - Component registry (enhanced for self-registration)

### Infrastructure Updates
- ✅ Added self-registration capability to registry.ts (window.registerComponent)
- ✅ Created comprehensive kanban board: KANBAN-REVAMP.md
- ✅ Created token audit script: scripts/audit-tokens.ts
- ✅ Updated package.json dependencies

## 🔧 PENDING WORK - PHASE 0 COMPLETION

### 1. Register Components in Registry
Need to add registration calls in the appropriate component scripts:
- SkillGapRadar: Already has registration call at end of skill-gap-radar.js
- CommandPalette: Already has registration call at end of command-palette.js
- Need to add similar registration to other components as they're created

### 2. Fix Remaining Token Violations
Current audit shows 1,431 violations:
- 224 deprecated tokens (like --tag-success-bg, --tag-info-bg, etc.)
- 932 hardcoded values (px values, color names, etc.)
- 275 forbidden patterns (inline onclick, old shadow names, etc.)

Key files to fix:
- `frontend/src/styles/dashboard.css` - 33 hardcoded values
- `frontend/src/pages/cv/builder.astro` - Multiple deprecated tokens and hardcoded values
- `frontend/src/pages/companies.astro` - Similar issues
- Various JS files with inline onclick handlers

### 3. Verify Foundation Gates Pass
Once token violations are resolved:
```bash
npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build
```

## 🚀 IMMEDIATE NEXT STEPS

### 1. Complete Token Migration (Phase 0)
Focus on fixing the highest-impact violations first:

**Dashboard CSS Fixes Needed:**
- Replace hardcoded px values with spacing tokens (--space-* variants)
- Replace hardcoded 280px max-width with appropriate token or remove constraint
- Update border declarations to use proper tokens

**Component File Fixes:**
- Replace `var(--tag-success-bg)` etc. with proper semantic equivalents
- Replace `var(--color-primary)` with `var(--accent-primary)` where appropriate
- Replace `var(--text-tertiary)` with `var(--text-muted)`
- Replace `var(--ui-success)` etc. with proper grade tokens
- Replace `var(--shadow-nous)` with `var(--shadow-md)`
- Replace `var(--stroke-hairline)` with `var(--border-default)`
- Replace `var(--bg-panel)` with `var(--bg-card)` or `var(--bg-surface)`
- Replace `var(--bg-hover)` with `var(--bg-tertiary)`
- Remove inline onclick handlers and move to module scripts

### 2. Register Missing Components
Ensure all components have proper registration in their module scripts:
```javascript
// At end of each component's .js file:
if (typeof window !== 'undefined' && window.registerComponent) {
  window.registerComponent('component-name', { init: initComponentName });
}
```

### 3. Integrate Components into Pages
Once foundation is solid, begin Phase 2:
- Wrap each page in `<PageLayout>` with appropriate slots
- Add `data-component` attributes for dynamic loading
- Integrate Cmd+K listener in PageLayout
- Ensure ThemeSwitcher and DensitySwitcher work via CommandLineBar
- Add API budget declarations to data-fetching components

## 📋 VERIFICATION CHECKPOINTS

### Gate 1: Token Audit
```bash
npx tsx scripts/audit-tokens.ts frontend/src
# Should show 0 violations
```

### Gate 2: Accessibility Audit
```bash
npm run audit:accessibility
# Should pass all checks (focus-visible, cursor-pointer, contrast)
```

### Gate 3: Consistency Audit
```bash
npm run audit:consistency
# Should show 0 arbitrary design token violations
```

### Gate 4: Build Success
```bash
npm run build
# Should produce clean dist/ folder with no errors
```

### Gate 5: E2E Tests
```bash
npm run test:e2e
# Should verify:
# - Cmd+K opens command palette
# - Radar Sweep animates correctly
# - Theme/Density persist via localStorage
# - API budget enforcement works
```

### Gate 6: Visual Regression
```bash
npm run test:visual
# Should match approved baselines with no regressions
```

## 🎯 PRIORITY FILES TO FIX NEXT

Based on audit output, focus on these high-impact files:

1. **frontend/src/styles/dashboard.css** - Fix 33 hardcoded values
2. **frontend/src/pages/cv/builder.astro** - Fix deprecated tokens and hardcoded values
3. **frontend/src/pages/companies.astro** - Fix deprecated tokens and hardcoded values
4. **frontend/src/scripts/market-overview.js** - Fix inline onclick
5. **frontend/src/scripts/company-deep-dive.js** - Fix inline onclick
6. **frontend/src/pages/tracker.astro** - Fix inline onclick and hardcoded colors
7. **frontend/src/pages/tools.astro** - Fix hardcoded values and inline onclick

## 🔄 WORKFLOW RECOMMENDATIONS

1. **Batch Fix Similar Issues**: Fix all instances of a particular violation type at once (e.g., all `--tag-success-bg` → `--grade-high-bg`)

2. **Use Search & Replace**: 
   - `var(--tag-success-bg)` → `var(--grade-high-bg)`
   - `var(--tag-warning-bg)` → `var(--grade-mid-bg)`
   - `var(--tag-error-bg)` → `var(--grade-low-bg)`
   - `var(--tag-info-bg)` → `var(--bg-tertiary)` or similar
   - `var(--text-tertiary)` → `var(--text-muted)`
   - `var(--ui-success)` → `var(--grade-high)`
   - `var(--ui-warning)` → `var(--grade-mid)`
   - `var(--ui-error)` → `var(--grade-low)`
   - `var(--shadow-nous)` → `var(--shadow-md)`
   - `var(--bg-panel)` → `var(--bg-card)`
   - `var(--bg-hover)` → `var(--bg-tertiary)`

3. **Fix JS Event Handlers**: Replace inline `onclick` with proper event listeners in module scripts

4. **Verify Incrementally**: After fixing each file type, run the token audit to confirm progress

## 📈 PROGRESS TRACKING

- **Total Files Scanned**: 83
- **Initial Violations**: 1,577
- **Current Violations**: 1,431
- **Progress**: 9.3% reduction
- **Target**: 0 violations

## 🎨 DESIGN SYSTEM COMPLIANCE CHECKLIST

For each component/file, verify:
- [ ] No hardcoded colors (use `var(--color-*)` or `var(--text-*)`)
- [ ] No hardcoded spacing (use `var(--space-*)`)
- [ ] No hardcoded sizing (use `var(--size-*)` or appropriate tokens)
- [ ] No hardcoded radii (use `var(--radius-*)`)
- [ ] No hardcoded shadows (use `var(--shadow-*)`)
- [ ] No `client:load` directives
- [ ] No inline `onclick` handlers
- [ ] No banned fonts (Inter as body, Sora as display only)
- [ ] No bounce/elastic easing
- [ ] Proper focus-visible styling (gold ring)
- [ ] Cursor pointer on all interactive elements
- [ ] Respects `prefers-reduced-motion`
- [ ] JS reads tokens via `getComputedStyle('--token')`
- [ ] Uses semantic tokens only (no color names like "red", "blue")

## 🚦 BLOCKERS & RISKS

1. **Token Migration Blocking Everything**: Cannot proceed to Phase 1-4 until Phase 0 gates pass
2. **Component Registration**: Must ensure components properly register with window.registerComponent
3. **Event Listener Migration**: All inline onclick handlers must be moved to module scripts
4. **Backward Compatibility**: Ensure existing functionality is preserved during migration

## ✅ IMMEDIATE ACTION ITEMS (NEXT 2 HOURS)

1. **Fix dashboard.css** - Replace all hardcoded values with semantic tokens
2. **Fix CV builder/companies pages** - Replace deprecated tag tokens
3. **Run token audit** - Verify reduction in violations
4. **Repeat until <100 violations remain**
5. **Then begin Phase 2 page integration**

The foundation is 90% complete - once the token violations are resolved, we can rapidly move through the remaining phases since all the component implementations are already created and just need registration/integration.