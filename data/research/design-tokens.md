# Design Tokens — Career Ops Dashboard

Single source of truth for all design tokens used in the Career Ops Dashboard.
Values are defined in `frontend/src/styles/globals.css` and referenced via CSS custom properties (`var(--token-name)`) in Astro components and inline JavaScript.

## Color Tokens

### Brand
| Token | Value | Description |
|-------|-------|-------------|
| `--accent-primary` | `#D4A853` | Warm gold — primary actions, focus rings |
| `--accent-hover` | `#E0B865` | Hover/pressed state for accent |
| `--accent-muted` | `#B8956B` | Muted accent for secondary elements |
| `--accent-subtle` | `rgba(212,168,83,0.15)` | Backgrounds, borders with accent tint |

### Semantic — Status / Grade
| Token | Value | Description |
|-------|-------|-------------|
| `--success` | `#10B981` | A–B+ / Success state |
| `--warning` | `#F59E0B` | B–C+ / Warning state |
| `--error` | `#EF4444` | C–F / Error state |
| `--info` | `#3B82F6` | Informational state |
| `--grade-high` | `#10B981` | Grade A–B+ (same as success) |
| `--grade-mid` | `#F59E0B` | Grade B–C+ (same as warning) |
| `--grade-low` | `#EF4444` | Grade C–F (same as error) |

### Background Layers
| Token | Value | Description |
|-------|-------|-------------|
| `--bg-base` | `#0A0E14` | Page background |
| `--bg-surface` | `#111820` | Cards, panels, modals |
| `--bg-elevated` | `#1A2230` | Elevated surfaces (drawers, menus) |
| `--bg-hover` | `#1E2A3A` | Hover state for interactive surfaces |

### Text
| Token | Value | Description |
|-------|-------|-------------|
| `--text-primary` | `#F1F5F9` | Headings, primary content |
| `--text-secondary` | `#94A3B8` | Labels, secondary content |
| `--text-muted` | `#64748B` | Placeholders, disabled text |

### Borders
| Token | Value | Description |
|-------|-------|-------------|
| `--border-default` | `#1E2A3A` | Default borders |
| `--border-strong` | `#334155` | Focus rings, emphasis borders |

## Typography Tokens

### Font Families
| Token | Value | Description |
|-------|-------|-------------|
| `--font-display` | `'Sora', system-ui, sans-serif` | Headings, numbers, brand |
| `--font-body` | `'Inter', system-ui, sans-serif` | Body text, UI |

### Fluid Type Scale (clamp() for responsive)
| Token | Value | Description |
|-------|-------|-------------|
| `--text-xs` | `clamp(0.7rem, 0.65rem + 0.25vw, 0.75rem)` | Extra small text |
| `--text-sm` | `clamp(0.8125rem, 0.75rem + 0.3125vw, 0.875rem)` | Small text |
| `--text-base` | `clamp(0.9375rem, 0.875rem + 0.3125vw, 1rem)` | Base text |
| `--text-lg` | `clamp(1.0625rem, 1rem + 0.3125vw, 1.125rem)` | Large text |
| `--text-xl` | `clamp(1.25rem, 1.125rem + 0.625vw, 1.375rem)` | Extra large text |
| `--text-2xl` | `clamp(1.5rem, 1.375rem + 0.625vw, 1.75rem)` | 2XL text |
| `--text-3xl` | `clamp(1.875rem, 1.625rem + 1.25vw, 2.25rem)` | 3XL text |
| `--text-4xl` | `clamp(2.25rem, 1.875rem + 1.875vw, 3rem)` | 4XL text |

### Font Weights
| Token | Value | Description |
|-------|-------|-------------|
| `--font-normal` | `400` | Regular weight |
| `--font-medium` | `500` | Medium weight |
| `--font-semibold` | `600` | Semi-bold weight |
| `--font-bold` | `700` | Bold weight |

## Spacing Tokens (4px base unit)
| Token | Value | Description |
|-------|-------|-------------|
| `--space-1` | `0.25rem` | 4px |
| `--space-2` | `0.5rem` | 8px |
| `--space-3` | `0.75rem` | 12px |
| `--space-4` | `1rem` | 16px |
| `--space-5` | `1.25rem` | 20px |
| `--space-6` | `1.5rem` | 24px |
| `--space-8` | `2rem` | 32px |
| `--space-10` | `2.5rem` | 40px |
| `--space-12` | `3rem` | 48px |
| `--space-16` | `4rem` | 64px |

## Border Radius Tokens
| Token | Value | Description |
|-------|-------|-------------|
| `--radius-sm` | `0.25rem` | 4px |
| `--radius-md` | `0.375rem` | 6px |
| `--radius-lg` | `0.5rem` | 8px |
| `--radius-xl` | `0.75rem` | 12px |
| `--radius-2xl` | `1rem` | 16px |
| `--radius-full` | `9999px` | Pills, rings |

## Shadow Tokens
| Token | Value | Description |
|-------|-------|-------------|
| `--shadow-sm` | `0 1px 2px 0 rgba(0,0,0,0.3)` | Small shadow |
| `--shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.4), 0 2px 4px -2px rgba(0,0,0,0.3)` | Medium shadow |
| `--shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.4), 0 4px 6px -4px rgba(0,0,0,0.3)` | Large shadow |
| `--shadow-xl` | `0 20px 25px -5px rgba(0,0,0,0.5), 0 8px 10px -6px rgba(0,0,0,0.4)` | Extra large shadow |
| `--shadow-ring` | `0 0 0 3px var(--accent-subtle)` | Focus ring |

## Transition Tokens
| Token | Value | Description |
|-------|-------|-------------|
| `--transition-fast` | `100ms ease` | Fast transitions (e.g., hover) |
| `--transition-base` | `200ms ease` | Base transitions |
| `--transition-slow` | `300ms ease` | Slow transitions |
| `--transition-spring` | `400ms cubic-bezier(0.34, 1.56, 0.64, 1)` | Spring-like motion |

## Z-Index Tokens
| Token | Value | Description |
|-------|-------|-------------|
| `--z-dropdown` | `100` | Dropdown menus |
| `--z-sticky` | `200` | Sticky headers |
| `--z-modal` | `300` | Modals, drawers |
| `--z-popover` | `400` | Popovers, tooltips |
| `--z-toast` | `500` | Toast notifications |
| `--z-tooltip` | `600` | Tooltips |

## Usage Rules

### 1. Zero Hardcoded Values
- **Forbidden:** Hex (`#D4A853`), RGB (`rgb(212,168,83)`), HSL (`hsl(38,60%,58%)`), pixel/rem values not derived from tokens.
- **Required:** Use `var(--token-name)` for all colors, spacing, typography, shadows, radii, transitions, z-index.
- **Exception:** Token definitions in `globals.css` only.

### 2. Semantic Naming
- **Good:** `--grade-high`, `--bg-surface`, `--text-muted`, `--shadow-ring`
- **Bad:** `--gold`, `--dark-card`, `--gray-text`, `--glow`

### 3. Component Contract
Each Astro component must:
- Import no colors from outside `globals.css`
- Use only `var(--token-name)` in `<style>` blocks
- Inline JavaScript reads tokens via `getComputedStyle(document.documentElement).getPropertyValue('--token-name')`

### 4. Enforcement
- Run audit script to detect violations:
  ```bash
  # Find hardcoded colors
  grep -r "#[0-9a-fA-F]\{3,8\}" frontend/src/ --include="*.astro" --include="*.ts" --include="*.js" --include="*.css" | grep -v "globals.css" | grep -v "node_modules"
  # Find hardcoded spacing (px/rem not from tokens)
  grep -r "w-\[.*px\]" frontend/src/ --include="*.astro"
  grep -r "h-\[.*px\]" frontend/src/ --include="*.astro"
  # Find inline styles with colors
  grep -r "style=" frontend/src/ --include="*.astro" | grep -E "(color|background|border).*#[0-9a-f]"
  ```
- CI pipeline must fail on token violations.

## Reference
This file is auto-generated from `globals.css` and updated when tokens change.
Last updated: 2026-06-30