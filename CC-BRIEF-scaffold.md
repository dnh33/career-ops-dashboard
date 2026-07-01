# Career Ops Dashboard — Project Scaffold Brief

## Context
You are scaffolding a full-stack dashboard at `/opt/career-ops-dashboard/`. The architecture spec is at `/opt/aetherkeep/06-projects/career-ops-dashboard/architecture.md` — READ IT FIRST, it is canonical.

## Current State
- `/opt/career-ops-dashboard/` already has `backend/app/config.py` (good, don't overwrite)
- `/opt/career-ops/` is the existing career-ops CLI repo with data, reports, jds, output, config dirs
- The config.py already uses path-based references to /opt/career-ops/ (no symlinks needed — the backend reads directly from the career-ops tree)

## What to Build

### Frontend (Astro 7.x + Tailwind v4)
1. Initialize fresh Astro project in `/opt/career-ops-dashboard/frontend/`
   - Use `npm create astro@latest` with template "minimal" or do it manually
   - Astro 7.0.3 is latest. Tailwind CSS 4.3.1 is latest.
2. Setup Tailwind v4 — use the `@astrojs/tailwind` integration or the v4 CSS-first approach (`@import "tailwindcss"` in globals.css). Tailwind v4 uses CSS-first config, NOT a tailwind.config.ts file.
3. Create the directory structure per architecture.md:
   - `src/pages/` — create ALL page stubs: index.astro, evaluate.astro, tracker.astro, reports.astro, scan.astro, pipeline.astro, profile.astro, output.astro
   - `src/pages/reports/[id].astro` — dynamic route stub
   - `src/components/` — create subdirs: layout/, dashboard/, evaluate/, tracker/, reports/
   - `src/layouts/BaseLayout.astro` — dark observatory theme base layout with nav
   - `src/styles/globals.css` — Tailwind v4 import + custom CSS vars for the design system
4. Design system (dark observatory theme):
   - Background: #0a0e1a (deep navy)
   - Accent: #D4A853 (warm amber)
   - Text: slate colors (#94a3b8 body, #e2e8f0 headings, #64748b muted)
   - Font: system font stack (Inter if available, else system-ui)
   - Monospace: for data/code blocks
5. BaseLayout should include:
   - Sidebar nav with links to all pages (use Astro page URLs)
   - Dark theme as default (only dark for v1)
   - Mobile-responsive (hamburger nav on small screens is fine as a stub)
6. Each page should be a minimal stub with the page title and a placeholder paragraph — enough to verify routing works.

### Backend (FastAPI)
1. In `/opt/career-ops-dashboard/backend/`:
   - `requirements.txt` with: fastapi, uvicorn[standard], watchdog, httpx, python-dotenv, pydantic
   - `app/main.py` — FastAPI app with CORS middleware (allow origins from config), health check endpoint, router includes
   - `app/routers/` — create ALL router stubs: evaluate.py, scan.py, tracker.py, reports.py, pipeline.py, profile.py, output.py
   - Each router: minimal `APIRouter` with the endpoints from architecture.md as stubs (return placeholder dicts)
   - `app/services/` — create empty `__init__.py` files in services/ and models/ subdirs
   - `app/models/` — create __init__.py
   - `app/config.py` — ALREADY EXISTS, do not overwrite
   - `tests/` — create empty dir with a `test_health.py` that hits the health endpoint
2. The `main.py` should:
   - Import config from app.config
   - Add CORS middleware using config.CORS_ORIGINS
   - Include all routers with `/api` prefix
   - Add a `@app.get("/api/health")` endpoint that checks career_ops_connected()
   - Add a `@app.get("/api/stats")` stub returning placeholder dashboard stats

### Root-level files
1. `/opt/career-ops-dashboard/CLAUDE.md` — project rules for AI assistants:
   - Project structure overview
   - How to run frontend (cd frontend && npm run dev)
   - How to run backend (cd backend && uvicorn app.main:app --reload)
   - Port conventions (frontend: 4321, backend: 8000)
   - Key paths: career-ops data at /opt/career-ops/
   - Design system: dark observatory theme specs
2. `/opt/career-ops-dashboard/scripts/setup.sh` — installs deps:
   - `cd frontend && npm install`
   - `cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
   - Must be executable
3. `/opt/career-ops-dashboard/scripts/start.sh` — starts both:
   - Backend: cd backend, source venv, uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   - Frontend: cd frontend, npm run dev -- --host 0.0.0.0
   - Start both in background, log to files, print PIDs
   - Must be executable
4. `/opt/career-ops-dashboard/README.md` — brief project description + how to setup/start

### Data symlinks (SKIP)
The architecture.md mentions symlinks for data/, reports/, jds/, output/, config/. Since config.py already uses direct path references to /opt/career-ops/, we do NOT need symlinks at the dashboard root. The backend reads from /opt/career-ops/ directly. Skip symlink creation.

## Verification (MUST DO)
After building everything, verify:
1. `cd /opt/career-ops-dashboard/frontend && npm install` succeeds
2. `cd /opt/career-ops-dashboard/backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt` succeeds
3. `cd /opt/career-ops-dashboard/frontend && npx astro build` succeeds (confirms all pages compile)
4. `cd /opt/career-ops-dashboard/backend && source venv/bin/activate && python3 -c "from app.main import app; print('FastAPI app created OK")"` succeeds
5. Start backend, curl the health endpoint: `curl http://localhost:8000/api/health`
6. If #5 works, kill the backend process

Do NOT skip verification. If any step fails, fix it before reporting.

## Constraints
- Use latest stable versions: Astro 7.0.3, Tailwind CSS 4.3.1, FastAPI latest
- Python venv at backend/venv/ (not global)
- Node modules at frontend/node_modules/
- Do NOT install anything globally
- Do NOT start long-running processes without proper cleanup
- The project is single-tenant, no auth needed
- Keep stubs minimal but functional — they must compile/run
