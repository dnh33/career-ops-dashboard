# Career Ops Dashboard — AI Assistant Rules

## Project Overview
Web dashboard for career-ops CLI. Single-tenant (Daniel only), served via Tailscale.

## Stack
- Frontend: Astro 7.x + Tailwind CSS v4 (via @tailwindcss/vite, CSS-first config in globals.css)
- Backend: FastAPI + uvicorn + Pydantic v2
- AI: OpenRouter (primary) / NVIDIA NIM (fallback)
- Backend reads career-ops data directly from `/opt/career-ops/` via path constants in `app.config`

## Running
- Frontend: `cd frontend && npm run dev` (port 4321)
- Backend: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload` (port 8000)
- Both: `./scripts/start.sh`
- Setup: `./scripts/setup.sh`

## Design System
- Dark observatory theme only (no light mode for v1)
- Background: #0a0e1a (deep navy), Accent: #D4A853 (warm amber)
- Text: slate-body #94a3b8, slate-heading #e2e8f0, slate-muted #64748b
- Tailwind v4: CSS-first config in `frontend/src/styles/globals.css` using `@theme`
- Font: Inter / system-ui, Monospace: JetBrains Mono / Fira Code

## Implemented Services
- `report_parser.py` — Parses career-ops report .md files (frontmatter `**Field:** value` format)
- `tracker_parser.py` — Parses `applications.md` markdown table into structured records

## Routers
All routers in `backend/app/routers/` with `/api` prefix:
- `stats.py` — GET /api/stats (live dashboard stats from applications.md + reports dir)
- `reports.py` — GET /api/reports, GET /api/reports/{id} (parses actual report files)
- `tracker.py` — GET /api/tracker, POST /api/tracker (reads applications.md)
- `evaluate.py` — POST /api/evaluate, GET /api/evaluate/{id} (stub)
- `scan.py` — POST /api/scan, GET /api/scan/status (stub)
- `pipeline.py` — GET /api/pipeline, POST /api/pipeline (stub)
- `profile.py` — GET/PUT /api/profile, GET/PUT /api/cv (reads config/profile.yml, config/cv.md)
- `output.py` — GET /api/output, POST /api/output/generate (stub)

## Testing
- Backend: `cd backend && source venv/bin/activate && pytest`
- Frontend: `cd frontend && npx astro check`
