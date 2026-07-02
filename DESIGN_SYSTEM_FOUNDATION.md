# Career Ops Dashboard — Aesthetic Foundation Document
**Status:** AUTHORITATIVE SOURCE FOR CURSOR TASK CONTEXT  
**Version:** 1.0  
**Generated:** 2026-07-02  
**Sources:** Audience Strategist (3 constraints) + Execution Architect (token architecture, component patterns, growth hooks) + Aesthetic Alchemist (voice/tone, KommandoCentralen metaphor, signature moments)

---

## 1. UNIFIED NON-NEGOTIABLE CONSTRAINTS
*Merged from all three subagents — conflicts resolved, hierarchy established*

### 1.1 Semantic Density Tokens Over Visual Decoration (Audience Strategist #1 + Execution Architect Token Architecture)
- **Rule:** Every visual decision maps to a semantic token. Zero hardcoded values in `.astro`/`.js`/`.css` except `globals.css` primitives.
- **Enforcement:** Tailwind v4 `@theme` block in `globals.css` is single source of truth. NO `tailwind.config.ts` color extend.
- **Hierarchy:** Primitive (`--color-{hue}-{scale}`) → Semantic Global (`--color-heading`, `--accent-primary`) → Component-scoped (`--btn-primary-bg`).
- **Forbidden:** `--gold`, `--dark-blue`, `--glow`, `--card-dark`, `#D4A853` anywhere except `globals.css` primitives.
- **Token naming enforced:** `--color-{hue}-{scale}` (primitives), `--color-{role}` (global semantic), `--{component}-{role}` (component semantic).

### 1.2 Authority-Bearing Visual Language (Audience Strategist #2 + Alchemist Janteloven Credibility)
- **Typography:** Sora (display) + Inter (body) — NON-NEGOTIABLE. `font-display` utility maps to Sora.
- **Color Hierarchy (ENFORCED BY CONSTRUCTION):**
  - Headlines h1-h3: ALWAYS `text-heading` (slate-900) — NEVER brand color
  - Body: `text-body` (slate-600) — NOT slate-700, NOT muted
  - Muted/secondary: `text-muted` (slate-500) — NOT slate-400 (fails WCAG 4.5:1)
  - Accent gold: ONLY 1-2 words/section, star ratings, CTA underline via `.accent-gold` utility
- **Nordic Signal Colors (Alchemist):** Emerald (high/A–B+), Amber (mid/B–C+), Red (low/C–F) — semantic grade tokens ONLY, never color names.
- **Focus ring:** ALWAYS gold (`--focus-ring: var(--shadow-ring)`).
- **Dark Observatory default theme:** `--bg-page: #0a0e1a`, `--bg-card: #141b2d`, `--text-primary: #f1f5f9`.

### 1.3 Progressive Disclosure Without Hidden Complexity (Audience Strategist #3 + Execution Architect Component Patterns + Alchemist KommandoCentralen)
- **Radar Sweep (Signature Moment):** Skill-gap radar = primary progressive disclosure instrument. Animated SVG rings (grade-colored) reveal depth on demand.
- **Cmd+K → Signal Command Palette (Signature Moment):** Global command interface. Loads `src/components/command-palette.js` via component registry.
- **Signal Card Atomic Unit (Signature Moment):** Base component for all data cards. Enforces heading/body hierarchy via MutationObserver.
- **Instrument Panels:** PageLayout slots (hero, sidebar, breadcrumbs, actions, footer) + modal/toast/drawer injection points — opt-in, zero breaking changes.
- **Command Line Bar:** Persistent bottom bar with density/theme switchers + budget indicator.
- **Signal Layer:** Toast/drawer/modal roots in PageLayout — feature modules hook via `pagelayout:ready` event.

---

## 2. SKILL APPLICATION RULES FOR CURSOR TASKS
*Exactly what skills to load and how to reference them in task bodies*

### 2.1 Mandatory Skill Load Order (Every Cursor Task)
```yaml
# ALWAYS load these first, in order:
1. hermes-agent-skill-authoring        # Skill authoring conventions
2. design-tokens                       # Token architecture enforcement
3. frontend-design                     # Component pattern library
4. impeccable                          # Quality gates (audit:tokens, audit:accessibility, audit:consistency)
5. writing/anti-slop-audit             # Content quality check
```

### 2.2 Task Body Template (Copy-Paste for Every Cursor Task)
```markdown
## Task: [T4.1/T4.2/T4.3 specific]

### Skills Loaded
- hermes-agent-skill-authoring
- design-tokens
- frontend-design
- impeccable
- writing/anti-slop-audit

### Non-Negotiable Constraints (Reference: Aesthetic Foundation §1)
- [ ] Semantic Density Tokens: Zero hardcoded values. All colors/spacing/radii via Tailwind utilities from `globals.css` @theme.
- [ ] Authority-Bearing Visual Language: `text-heading` on h1-h3, `text-body` on p, `text-muted` on secondary. Accent gold ONLY 1-2 words via `.accent-gold`.
- [ ] Progressive Disclosure: Radar Sweep / Cmd+K Signal / Signal Card patterns per §1.3.

### Token Architecture Compliance (Reference: Execution Architect §1)
- [ ] Primitives only in `globals.css` @theme block
- [ ] Semantic globals in `:root` (--color-heading, --color-body, --color-muted, --accent-primary, --grade-high/mid/low)
- [ ] Component-scoped tokens in component `<style>` blocks (--btn-primary-bg, --card-bg, --ring-size, etc.)
- [ ] JS reads via `getComputedStyle(document.documentElement).getPropertyValue('--token')`

### Component Pattern Compliance (Reference: Execution Architect §2)
- [ ] Base layer rules in `globals.css` (specificity-safe :not([class*="text-"]) selectors)
- [ ] Module scripts only — NO inline onclick
- [ ] cursor-pointer via base CSS
- [ ] focus-visible via base CSS (gold ring)
- [ ] prefers-reduced-motion via base CSS
- [ ] Astro component + separate `.js` module pattern

### Growth Hooks (Reference: Execution Architect §3)
- [ ] Theme variants via `[data-theme]` on `<html>` (dark/light/high-contrast/sepia)
- [ ] Density variants via `[data-density]` on `<html>` or `.dense`/`.spacious` scope
- [ ] Feature slots in PageLayout (hero, sidebar, breadcrumbs, actions, footer, modal-root, toast-root, drawer-root)
- [ ] Component registry pattern for dynamic loading (`registerComponent`, `data-component` attributes)
- [ ] API budget guard (100 req limit) — components declare cost/priority

### Signature Moments (Reference: Alchemist)
- [ ] Radar Sweep animation (skill-gap-radar.js) — respects prefers-reduced-motion
- [ ] Cmd+K Signal command palette (command-palette.js) — component registry entry
- [ ] Signal Card atomic unit (Card.astro + MutationObserver enforcement)

### Verification Gates (MUST PASS before merge)
```bash
npm run audit:tokens        # 0 hardcoded values
npm run audit:accessibility # cursor-pointer, focus-visible, contrast
npm run audit:consistency   # 0 arbitrary rounded/p/gap/shadow values
npm run build               # Astro + TypeScript clean
```

### 2.3 Skill Reference Map (Quick Lookup)
| Task Type | Primary Skills | Secondary Skills |
|-----------|----------------|------------------|
| Token audit/fix | design-tokens, impeccable | hermes-agent-skill-authoring |
| New component | frontend-design, design-tokens | impeccable, writing/anti-slop-audit |
| Radar/animation | frontend-design (JS module pattern) | design-tokens (getComputedStyle) |
| Theme/density | design-tokens (CSS custom properties) | frontend-design (switcher components) |
| Command palette | frontend-design (registry pattern) | design-tokens (semantic tokens) |
| Migration (Phase 4) | impeccable (audit scripts) | design-tokens, frontend-design |

---

## 3. GROWTH-READY FOUNDATION
*Theming hooks, component patterns, token architecture, signature moments — ready for scale*

### 3.1 Token Architecture (Execution Architect §1 — Complete)
**File:** `src/styles/globals.css` (single source of truth)

```css
/* Primitive Layer — @theme block */
@theme {
  /* ── Color Primitives (single-source hex) ───────────────────────── */
  --color-gold-50:  #fef9e7;  --color-gold-100: #fdf2c9;  --color-gold-200: #f9e79f;
  --color-gold-300: #f5d06e;  --color-gold-400: #f0b941;  --color-gold-500: #D4A853;  /* brand gold */
  --color-gold-600: #b89045;  --color-gold-700: #92702a;  --color-gold-800: #765921;
  --color-gold-900: #5c4419;

  --color-slate-50:  #f8fafc;  --color-slate-100: #f1f5f9; --color-slate-200: #e2e8f0;
  --color-slate-300: #cbd5e1;  --color-slate-400: #94a3b8; --color-slate-500: #64748b;
  --color-slate-600: #475569;  --color-slate-700: #334155; --color-slate-800: #1e293b;
  --color-slate-900: #0f172a;  --color-slate-950: #020617;

  --color-emerald-500: #22c55e;  --color-emerald-600: #16a34a;
  --color-amber-500:  #eab308;   --color-amber-600:  #ca8a04;
  --color-red-500:    #ef4444;   --color-red-600:    #dc2626;
  --color-blue-500:   #3b82f6;   --color-blue-600:   #2563eb;

  /* ── Typography Primitives ──────────────────────────────────────── */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-display: 'Sora', system-ui, sans-serif;   /* NON-NEGOTIABLE: Sora for display */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-xs:   0.75rem;   --text-sm:  0.875rem;  --text-base: 1rem;
  --text-lg:   1.125rem;  --text-xl:  1.25rem;   --text-2xl:  1.5rem;
  --text-3xl:  1.875rem;  --text-4xl: 2.25rem;   --text-5xl:  3rem;
  --text-6xl:  3.75rem;   --text-7xl: 4.5rem;

  --font-normal: 400;  --font-medium: 500;  --font-semibold: 600;  --font-bold: 700;

  /* ── Spacing (4dp base unit) ────────────────────────────────────── */
  --space-1:  0.25rem;  --space-2:  0.5rem;   --space-3:  0.75rem;
  --space-4:  1rem;     --space-5:  1.25rem;  --space-6:  1.5rem;
  --space-8:  2rem;     --space-10: 2.5rem;   --space-12: 3rem;
  --space-16: 4rem;     --space-20: 5rem;     --space-24: 6rem;

  /* ── Radius ─────────────────────────────────────────────────────── */
  --radius-sm: 4px;    --radius-md: 8px;     --radius-lg: 12px;
  --radius-xl: 16px;   --radius-2xl: 24px;   --radius-full: 9999px;

  /* ── Shadows ────────────────────────────────────────────────────── */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1);
  --shadow-ring: 0 0 0 3px var(--color-gold-500/40);

  /* ── Motion ─────────────────────────────────────────────────────── */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-fast: 150ms;
  --duration-base: 200ms;
  --duration-slow: 300ms;

  /* ── Z-Index ────────────────────────────────────────────────────── */
  --z-base: 0;  --z-dropdown: 100;  --z-sticky: 200;
  --z-overlay: 300;  --z-modal: 400;   --z-toast: 500;  --z-tooltip: 600;
}

/* Semantic Global Layer — :root */
:root {
  /* ── Brand / Accent ── */
  --accent-primary: var(--color-gold-500);
  --accent-hover:  var(--color-gold-400);
  --accent-muted:  var(--color-gold-700);
  --accent-subtle: var(--color-gold-100/15);

  /* ── Semantic Color Hierarchy (NON-NEGOTIABLE HIERARCHY) ── */
  /* Headlines h1-h3: ALWAYS slate-900 — NEVER brand color */
  --color-heading: var(--color-slate-900);
  /* Body: slate-600 — NOT slate-700 (too harsh), NOT muted */
  --color-body:    var(--color-slate-600);
  /* Muted/secondary: slate-500 — NOT slate-400 (fails WCAG 4.5:1) */
  --color-muted:   var(--color-slate-500);
  /* Accent gold: ONLY 1-2 words/section, star ratings, CTA underline */
  --color-accent:  var(--color-gold-500);

  /* Background layers (Dark Observatory theme) */
  --bg-page:        #0a0e1a;   /* page */
  --bg-surface:     #111827;   /* sidebar, bottom nav */
  --bg-card:        #141b2d;   /* cards, panels */
  --bg-elevated:    #1a2236;   /* modals, dropdowns, tooltips */
  --bg-input:       #0d1117;   /* inputs */
  --bg-tertiary:    #1f2937;   /* tertiary surfaces */

  /* Text on dark */
  --text-primary:   #f1f5f9;   /* headings, primary */
  --text-secondary: #94a3b8;   /* labels, secondary */
  --text-muted:     #64748b;   /* placeholders, disabled */
  --text-inverse:   #0a0e1a;   /* on light */

  /* Borders */
  --border-default: #1e293b;
  --border-hover:   #334155;
  --border-focus:   var(--color-gold-500);

  /* Grade/Status (semantic, NOT color names) */
  --grade-high:      var(--color-emerald-500);  /* A–B+ */
  --grade-high-bg:   #166534;
  --grade-high-text: #86efac;
  --grade-mid:       var(--color-amber-500);    /* B–C+ */
  --grade-mid-bg:    #854d0e;
  --grade-mid-text:  #fde047;
  --grade-low:       var(--color-red-500);      /* C–F */
  --grade-low-bg:    #991b1b;
  --grade-low-text:  #fca5a5;

  /* Focus ring — ALWAYS gold */
  --focus-ring: var(--shadow-ring);

  /* Component-level semantic tokens (component-scoped) */
  --btn-primary-bg:      var(--accent-primary);
  --btn-primary-hover:   var(--accent-hover);
  --btn-primary-text:    var(--text-inverse);
  --btn-secondary-bg:    var(--bg-elevated);
  --btn-secondary-hover: var(--bg-tertiary);
  --btn-secondary-text:  var(--text-primary);
  --btn-ghost-hover:     var(--accent-subtle);
  --btn-ghost-text:      var(--accent-primary);

  --card-bg:        var(--bg-card);
  --card-border:    var(--border-default);
  --card-hover-bg:  var(--bg-elevated);
  --card-hover-border: var(--border-hover);

  --input-bg:       var(--bg-input);
  --input-border:   var(--border-default);
  --input-focus-border: var(--border-focus);
  --input-placeholder: var(--text-muted);

  --ring-size: 120px;        /* skill-gap radar ring */
  --ring-stroke: 8px;
  --ring-gap: 4px;
}

/* Theme Variants — [data-theme] on <html> */
[data-theme="light"] {
  /* Light mode — semantic tokens remap, primitives unchanged */
  --bg-page:        #ffffff;
  --bg-surface:     #f8fafc;
  --bg-card:        #ffffff;
  --bg-elevated:    #f1f5f9;
  --bg-input:       #ffffff;
  --bg-tertiary:    #e2e8f0;

  --text-primary:   #0f172a;
  --text-secondary: #475569;
  --text-muted:     #64748b;
  --text-inverse:   #ffffff;

  --border-default: #e2e8f0;
  --border-hover:   #cbd5e1;
  --border-focus:   var(--color-gold-600);

  --color-heading:  #0f172a;  /* slate-900 */
  --color-body:     #334155;  /* slate-600 */
  --color-muted:    #64748b;  /* slate-500 */

  --btn-primary-bg: var(--color-gold-600);
  --btn-primary-hover: var(--color-gold-700);
  --btn-secondary-bg: var(--bg-elevated);
  --btn-secondary-hover: var(--bg-tertiary);
  --btn-ghost-hover: var(--color-gold-100/30);
}

[data-theme="high-contrast"] {
  /* WCAG AAA — forced colors mode support */
  --bg-page:        #000000;
  --bg-surface:     #000000;
  --bg-card:        #000000;
  --bg-elevated:    #1a1a1a;
  --text-primary:   #ffffff;
  --text-secondary: #cccccc;
  --text-muted:     #999999;
  --border-default: #ffffff;
  --border-hover:   #ffffff;
  --accent-primary: #ffd700;
  --accent-hover:   #ffdf4d;
  --focus-ring:     0 0 0 3px #ffd700;
}

[data-theme="sepia"] {
  /* Reading mode — warm paper */
  --bg-page:        #fdf6e3;
  --bg-surface:     #f5ebd8;
  --bg-card:        #fdf6e3;
  --bg-elevated:    #eee4d1;
  --text-primary:   #3c2e1a;
  --text-secondary: #5a4a2e;
  --text-muted:     #7a6a4e;
  --border-default: #d4c4a0;
  --color-heading:  #2c1e0a;
  --color-body:     #4c3e1e;
}

/* Density Variants — [data-density] on <html> or .dense/.spacious scope */
:root {
  /* Default: comfortable */
  --density-multiplier: 1;
  --space-1: calc(0.25rem * var(--density-multiplier));
  --space-2: calc(0.5rem * var(--density-multiplier));
  --space-3: calc(0.75rem * var(--density-multiplier));
  --space-4: calc(1rem * var(--density-multiplier));
  --space-5: calc(1.25rem * var(--density-multiplier));
  --space-6: calc(1.5rem * var(--density-multiplier));
  --space-8: calc(2rem * var(--density-multiplier));
  --space-10: calc(2.5rem * var(--density-multiplier));
  --space-12: calc(3rem * var(--density-multiplier));
  --space-16: calc(4rem * var(--density-multiplier));
  --space-20: calc(5rem * var(--density-multiplier));
  --space-24: calc(6rem * var(--density-multiplier));
}

[data-density="compact"] {
  --density-multiplier: 0.75;
}

[data-density="spacious"] {
  --density-multiplier: 1.25;
}

/* Component-level density (scoped) */
.dense {
  --space-1: 0.125rem;  --space-2: 0.25rem;   --space-3: 0.375rem;
  --space-4: 0.5rem;    --space-5: 0.625rem;  --space-6: 0.75rem;
  --space-8: 1rem;      --space-10: 1.25rem;  --space-12: 1.5rem;
  --space-16: 2rem;     --space-20: 2.5rem;   --space-24: 3rem;
}

.spacious {
  --space-1: 0.375rem;  --space-2: 0.75rem;   --space-3: 1.125rem;
  --space-4: 1.5rem;    --space-5: 1.875rem;  --space-6: 2.25rem;
  --space-8: 3rem;      --space-10: 3.75rem;  --space-12: 4.5rem;
  --space-16: 6rem;     --space-20: 7.5rem;   --space-24: 9rem;
}

/* Tailwind v4 Utility Mapping — @theme */
@theme {
  /* Map semantic tokens to Tailwind utilities */
  --color-heading: var(--color-heading);
  --color-body:    var(--color-body);
  --color-muted:   var(--color-muted);
  --color-accent:  var(--color-accent);

  --color-primary: var(--accent-primary);
  --color-primary-hover: var(--accent-hover);

  --color-bg-page:   var(--bg-page);
  --color-bg-surface: var(--bg-surface);
  --color-bg-card:   var(--bg-card);
  --color-bg-elevated: var(--bg-elevated);
  --color-bg-input:  var(--bg-input);

  --color-text-primary:   var(--text-primary);
  --color-text-secondary: var(--text-secondary);
  --color-text-muted:     var(--text-muted);

  --color-border:       var(--border-default);
  --color-border-hover: var(--border-hover);
  --color-border-focus: var(--border-focus);

  --color-grade-high: var(--grade-high);
  --color-grade-mid:  var(--grade-mid);
  --color-grade-low:  var(--grade-low);

  --font-display: var(--font-display);
  --font-sans:    var(--font-sans);
  --font-mono:    var(--font-mono);

  --radius-sm: var(--radius-sm);
  --radius-md: var(--radius-md);
  --radius-lg: var(--radius-lg);
  --radius-xl: var(--radius-xl);
  --radius-2xl: var(--radius-2xl);
  --radius-full: var(--radius-full);

  --shadow-sm: var(--shadow-sm);
  --shadow-md: var(--shadow-md);
  --shadow-lg: var(--shadow-lg);
  --shadow-xl: var(--shadow-xl);

  --animate-fade-in: fade-in var(--duration-base) var(--ease-out);
  --animate-scale-in: scale-in var(--duration-fast) var(--ease-out);
  --animate-slide-up: slide-up var(--duration-slow) var(--ease-out);
}

@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes scale-in { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
@keyframes slide-up { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
```

**Tailwind utilities now available:** `text-heading`, `text-body`, `text-muted`, `bg-page`, `bg-card`, `border-border`, `font-display`, `rounded-lg`, `shadow-lg`, `animate-fade-in`, etc.

**NO `tailwind.config.ts` color extend.** Single source of truth = `globals.css`.

---

### 3.2 Component Patterns (Execution Architect §2 — Enforced by Construction)

#### Base Layer Rules (globals.css) — Specificity-Safe

```css
/* globals.css — base layer, specificity-safe */

/* Links: only apply brand color when NO text-* utility present */
a:not([class*="text-"]) {
  color: var(--accent-primary);
  text-decoration: none;
}
a:hover:not([class*="text-"]) { color: var(--accent-hover); }

/* Headings: ONLY neutral — NEVER brand color */
h1:not([class*="text-"]),
h2:not([class*="text-"]),
h3:not([class*="text-"]),
h4:not([class*="text-"]),
h5:not([class*="text-"]),
h6:not([class*="text-"]) {
  font-family: var(--font-display);
  color: var(--color-heading);  /* slate-900 */
  font-weight: var(--font-bold);
  line-height: 1.1;
}

/* Body text default */
p:not([class*="text-"]) { color: var(--color-body); line-height: 1.7; }

/* Buttons: only base styles, NO bg color (utilities own that) */
button:not([class*="bg-"]):not([class*="btn-"]) {
  font-family: var(--font-sans);
  font-weight: var(--font-medium);
  border-radius: var(--radius-md);
  transition: background var(--duration-fast) var(--ease-out),
              color var(--duration-fast) var(--ease-out),
              border-color var(--duration-fast) var(--ease-out);
}

/* Inputs */
input:not([class*="bg-"]),
textarea:not([class*="bg-"]),
select:not([class*="bg-"]) {
  background: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  padding: var(--space-2) var(--space-3);
}
input:focus:not([class*="bg-"]),
textarea:focus:not([class*="bg-"]),
select:focus:not([class*="bg-"]) {
  outline: none;
  border-color: var(--input-focus-border);
  box-shadow: var(--focus-ring);
}

/* Interactive cursor — non-negotiable accessibility */
button, a, [role="button"], [role="link"],
input[type="submit"], input[type="button"], input[type="reset"],
label[for], summary {
  cursor: pointer;
}

/* Focus visible — always gold ring */
*:focus-visible {
  outline: none;
  box-shadow: var(--focus-ring);
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

#### Component Template (All UI Components)

```astro
---
// src/components/ui/[Component].astro
// 🛡️ ENFORCED: Only semantic tokens, module script, cursor-pointer, focus-visible, prefers-reduced-motion

interface Props {
  variant?: 'primary'|'secondary'|'ghost';
  size?: 'sm'|'md'|'lg';
  class?: string;
  children: any;
}
---

<style>
  .component { /* component-scoped semantic tokens mapping to global semantic */ }
  .component-primary { background: var(--btn-primary-bg); color: var(--btn-primary-text); }
  /* size variants use spacing tokens ONLY */
</style>

<Tag class={classes} ...><slot /></Tag>

<script>
  // Module-scoped — no inline onclick
  // Auto-enforce hierarchy via MutationObserver where applicable
</script>
```

#### Implemented Components

| Component | Purpose | Key Enforcement |
|-----------|---------|-----------------|
| `Button.astro` + `button.js` | Variant/size, href→`<a>`, module click handler | Semantic tokens, focus ring, reduced motion |
| `Card.astro` | Variant: default/elevated/interactive, MutationObserver enforces `text-heading`/`text-body` | Color hierarchy by construction |
| `PageLayout.astro` | Slots: brand, navigation, header-actions, hero, sidebar, breadcrumbs, actions, footer + modal/toast/drawer roots | Future features inject without breaking changes |
| `ThemeSwitcher.astro` + `theme-switcher.js` | Theme switching (dark/light/high-contrast/sepia), persists to localStorage | Theme variants via `[data-theme]` |
| `DensitySwitcher.astro` | Density switching (compact/comfortable/spacious), persists to localStorage | Density variants via `[data-density]` |

---

### 3.3 Signature Moments (Aesthetic Alchemist — Implementation Specs)

#### 3.3.1 Radar Sweep Animation (`src/components/skill-gap-radar.js`)

```javascript
export function initSkillGapRadar(container: HTMLElement, data: SkillGapData) {
  const rootStyles = getComputedStyle(document.documentElement);
  // ALL values via getComputedStyle — ZERO hardcoded
  const ringSize = parseFloat(rootStyles.getPropertyValue('--ring-size')) || 120;
  const ringStroke = parseFloat(rootStyles.getPropertyValue('--ring-stroke')) || 8;
  const gradeHigh = rootStyles.getPropertyValue('--grade-high').trim();
  const gradeMid = rootStyles.getPropertyValue('--grade-mid').trim();
  const gradeLow = rootStyles.getPropertyValue('--grade-low').trim();
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Animated SVG rings with stroke-dashoffset transition
  // Grade-colored rings (emerald/amber/red) = Nordic signal colors
}
```

**Astro Wrapper:** `skill-gap.astro` passes data via `data-gaps` JSON attribute.

#### 3.3.2 Cmd+K Signal Command Palette (`src/components/command-palette.js`)

```javascript
// Component registry entry
registerComponent('command-palette', { init: initCommandPalette });
// Usage: <div data-component="command-palette" data-component-props='{}' />
// Features: fuzzy search, keyboard navigation, action registry, theme-aware
```

#### 3.3.3 Signal Card Atomic Unit (`src/components/ui/Card.astro`)

- MutationObserver auto-adds `text-heading` to headings, `text-body` to paragraphs
- Variant system: default/elevated/interactive
- Registers in component registry for declarative use

---

### 3.4 Component Registry & Dynamic Loading (`src/components/registry.ts`)

```typescript
export const componentRegistry = new Map<string, ComponentModule>();

export function registerComponent(name: string, module: ComponentModule);
export function getComponent(name: string): ComponentModule | undefined;

// Auto-init on pagelayout:ready event — scans [data-component] attributes
```

---

### 3.5 API Budget Guard (`src/lib/api-budget.ts`)

```typescript
const MAX_BUDGET = 100;
export function requestBudget(entry: BudgetEntry): boolean;
// Components declare: { component: 'skill-gap-radar', cost: 1, priority: 'high' }
// System enforces, evicts lower priority if needed
```

---

### 3.6 Phase 4 Migration Strategy (9 Legacy Pages)

**Per-page checklist:** Token audit → Component extraction → Layout migration (PageLayout) → JS module migration → Data passing (data-* attrs) → Verification gates (4 automated audits).

---

## 4. IMMEDIATE IMPLEMENTATION PRIORITY
*Specific files, specific patterns for T4.1 fix + T4.2 + T4.3*

### 4.1 T4.1 FIX — Token Audit & CSS Bug Resolution
**Problem:** Hardcoded values, brand color on headings, invisible CTA text (per CSS Color Bug Pattern)

| File | Action | Pattern |
|------|--------|---------|
| `src/styles/globals.css` | Fix `@theme` block: `--color-heading: var(--color-slate-900)` | Token Architecture §1.4 |
| `src/styles/globals.css` | Fix base `h1-h6` rule: `color: var(--color-heading)` | Base Layer §2.1 |
| `src/styles/globals.css` | Fix base `a` rule: `a:not([class*="text-"]) { color: var(--accent-primary); }` | Base Layer §2.1 |
| All `.astro` files | Replace hardcoded colors → Tailwind utilities (`text-heading`, `bg-card`, `border-border`) | Token Audit |
| All `.js` files | Replace hardcoded values → `getComputedStyle().getPropertyValue('--token')` | JS Module Pattern |

**Commands:**
```bash
# 1. Audit all hardcoded values
npx tsx scripts/audit-tokens.ts src/
# 2. Fix globals.css (3 bugs above)
# 3. Verify
npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build
```

---

### 4.2 T4.2 — Signature Moments Implementation

**Priority Order:**

#### 4.2.1 Radar Sweep (Skill-Gap Radar) — `src/components/skill-gap-radar.js` + `skill-gap.astro`
```bash
# Create files per Execution Architect §2.4 + Alchemist Radar Sweep spec
# Register in registry.ts
registerComponent('skill-gap-radar', { init: initSkillGapRadar });
```
**Integration:** Use in `skill-gap.astro` page and any dashboard view showing skill gaps.

#### 4.2.2 Cmd+K Signal Command Palette — `src/components/command-palette.js` + `command-palette.astro`
```bash
# Create per Alchemist spec + registry pattern
# Features: fuzzy search (skills, companies, actions), keyboard nav, theme-aware
registerComponent('command-palette', { init: initCommandPalette });
```
**Integration:** Global keyboard listener (Cmd+K) in `PageLayout.astro` script block.

#### 4.2.3 Signal Card Atomic Unit — Enhance `src/components/ui/Card.astro`
```bash
# Already has MutationObserver enforcement
# Add: grade badge variant, signal indicator dot, radar-mini slot
# Register: registerComponent('signal-card', { init: initSignalCard });
```

---

### 4.3 T4.3 — Growth Hooks Activation

| File | Purpose | Reference |
|------|---------|-----------|
| `src/components/ui/ThemeSwitcher.astro` + `theme-switcher.js` | Theme switching (dark/light/high-contrast/sepia) | Growth Hooks §3.1 |
| `src/components/ui/DensitySwitcher.astro` | Density switching (compact/comfortable/spacious) | Growth Hooks §3.2 |
| `src/components/ui/PageLayout.astro` | Feature slots + modal/toast/drawer roots + pagelayout:ready event | Growth Hooks §3.3 |
| `src/components/registry.ts` | Dynamic component loading | Growth Hooks §3.4 |
| `src/lib/api-budget.ts` | 100-request budget enforcement | Growth Hooks §3.5 |
| `scripts/audit-tokens.ts` | Token audit automation | Growth Hooks §3.6 |
| `scripts/migrate-page.ts` | Batch migration script | Growth Hooks §3.6 |

**Activation Checklist:**
- [ ] Add `[data-theme]` and `[data-density]` to `<html>` in base layout
- [ ] Import ThemeSwitcher + DensitySwitcher in command line bar (CommandLineBar.astro)
- [ ] Wrap all pages in `<PageLayout>` (provides feature injection points)
- [ ] Register all feature components in registry.ts (radar, command-palette, deep-dive, signal-card)
- [ ] Add API budget calls to radar/deep-dive modules
- [ ] Run migration on 9 legacy pages (parallel batch)

---

## 5. CURSOR TASK CONTEXT — QUICK REFERENCE
*Paste this into any Cursor task for immediate compliance*

```markdown
# CURSOR TASK CONTEXT — CAREER OPS DASHBOARD

## Load These Skills First
- hermes-agent-skill-authoring
- design-tokens
- frontend-design
- impeccable
- writing/anti-slop-audit

## Non-Negotiables (Check Every PR)
☐ Zero hardcoded colors/spacing/radii — only Tailwind utilities from globals.css @theme
☐ h1-h3 = text-heading (slate-900), p = text-body (slate-600), secondary = text-muted (slate-500)
☐ Accent gold = max 1-2 words/section via .accent-gold utility
☐ Module scripts only — NO inline onclick
☐ focus-visible = gold ring (via base CSS)
☐ prefers-reduced-motion respected (via base CSS)
☐ JS reads tokens via getComputedStyle('--token')

## Signature Moments to Implement
1. Radar Sweep → skill-gap-radar.js (grade-colored animated SVG rings)
2. Cmd+K Signal → command-palette.js (fuzzy search, registry-loaded)
3. Signal Card → Card.astro + MutationObserver (atomic data unit)

## Growth Hooks Active
- [data-theme]: dark/light/high-contrast/sepia (semantic remap only)
- [data-density]: compact/comfortable/spacious (--density-multiplier)
- PageLayout slots: hero, sidebar, breadcrumbs, actions, footer + modal/toast/drawer roots
- Component registry: registerComponent('name', { init }) + <div data-component="name" />
- API budget: requestBudget({ component, cost, priority }) — max 100

## Verification (Must Pass)
npm run audit:tokens && npm run audit:accessibility && npm run audit:consistency && npm run build
```

---

## 6. FILE STRUCTURE REFERENCE

```
src/
├── styles/
│   └── globals.css              # SINGLE SOURCE OF TRUTH — @theme + :root + themes + density
├── components/
│   ├── ui/
│   │   ├── Button.astro         # Base component template
│   │   ├── Card.astro           # Signal Card atomic unit
│   │   ├── PageLayout.astro     # Feature slots + injection points
│   │   ├── ThemeSwitcher.astro  # Theme switching
│   │   ├── DensitySwitcher.astro # Density switching
│   │   └── CommandLineBar.astro # Persistent bar (theme/density/budget)
│   ├── skill-gap-radar.js       # Radar Sweep signature moment
│   ├── skill-gap.astro          # Radar Astro wrapper
│   ├── command-palette.js       # Cmd+K Signal signature moment
│   ├── command-palette.astro    # Command palette Astro wrapper
│   ├── company-deep-dive.js     # Ring + Table pattern
│   └── registry.ts              # Dynamic component loading
├── lib/
│   └── api-budget.ts            # 100-request budget guard
├── pages/
│   ├── skill-gap.astro          # Uses skill-gap-radar
│   ├── company/[slug].astro     # Uses company-deep-dive
│   └── legacy/*.astro           # 9 pages → Phase 4 migration
└── scripts/
    ├── audit-tokens.ts          # Token audit automation
    └── migrate-page.ts          # Batch migration
```

---

**END OF DOCUMENT — THIS IS THE AUTHORITATIVE CURSOR TASK CONTEXT**