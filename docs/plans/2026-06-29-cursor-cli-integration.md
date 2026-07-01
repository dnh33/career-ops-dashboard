# Career Ops — Cursor CLI + owl-alpha Integration Plan

> **For Hermes:** Implement via kanban board. Each task = one granular unit of work.
> Profile: `runeforge-coder` for all implementation + QA tasks.

**Goal:** Make Career Ops fully functional — backend uses Cursor CLI (`auto` model) for A-G evaluation, scan, pipeline, and PDF generation. owl-alpha via OpenRouter API handles simple inferences (legitimacy triage, company extraction) where full Cursor tool access isn't needed. Frontend connects to all endpoints and works end-to-end.

**Architecture:** 
- Backend FastAPI routes JSON to the right brain: Cursor CLI for complex tool-using tasks, owl-alpha for simple extraction/classification, direct file I/O for CRUD (tracker, profile, reports, stats, pipeline).
- Cursor Agent service wraps `cursor --model auto` subprocess with timeout, error handling, and backend mode.
- Frontend: all 10 pages already exist — fix connectivity, loading states, and data binding.

**Tech Stack:** Python 3.11, FastAPI, Cursor CLI (`--model auto`), `openrouter/owl-alpha` via API, Astro frontend, existing markdown file storage.

**Current State Assessment:**
| Component | Status | Needs |
|-----------|--------|-------|
| tracker router (CRUD) | ✅ Done | Frontend wiring |
| reports router (list/read) | ✅ Done | Frontend wiring |
| stats router (dashboard) | ✅ Done | Frontend wiring |
| profile router (CRUD) | ✅ Done | Frontend wiring |
| pipeline router (add/list/del) | ✅ Done | Evaluate-pending endpoint |
| evaluate router | ⚠️ API-only, no mode file | Cursor integration for full A-G |
| scan router | ⚠️ Missing/empty | Cursor-dispatched scan |
| output router | ⚠️ Missing/empty | PDF generation |
| url_fetcher service | ✅ Done (from prior work) | Wire into evaluate |
| cursor_agent service | ❌ Not created | Build this |
| Frontend 10 pages | ⚠️ Scaffold exists | Wire all to API |

---

## Phase 1: CursorAgent Service (Foundation)

### Task 1.1: Create CursorAgent service

**Objective:** Create the Cursor CLI wrapper that backend services dispatch to.

**Files:**
- Create: `backend/app/services/cursor_agent.py`
- Test: `tests/test_cursor_agent.py`

**Step 1: Write failing test**

```python
# tests/test_cursor_agent.py
import pytest
from app.services.cursor_agent import CursorAgent

@pytest.mark.asyncio
async def test_cursor_agent_basic():
    agent = CursorAgent(workdir="/opt/career-ops", timeout=60)
    result = agent.run("Reply with only the word TEST")
    assert isinstance(result, str)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_cursor_agent_timeout():
    agent = CursorAgent(workdir="/opt/career-ops", timeout=5)
    with pytest.raises(TimeoutError):
        agent.run("Run a sleep 30 command")
```

**Step 2: Run** → FAIL (module doesn't exist)

**Step 3: Implement**

```python
# backend/app/services/cursor_agent.py
"""Cursor CLI agent wrapper — runs tasks via cursor with --model auto."""
from __future__ import annotations
import asyncio
import shutil
from pathlib import Path

WORKDIR = Path("/opt/career-ops")


class CursorAgent:
    def __init__(self, workdir: str | Path = WORKDIR, timeout: int = 300):
        self.workdir = Path(workdir)
        self.timeout = timeout

    def run(self, prompt -> str:
        """Run a task via Cursor CLI synchronously."""
        if not shutil.which("cursor"):
            raise RuntimeError("cursor CLI not found in PATH")
        
        result = subprocess.run(
            ["cursor", "--model", "auto", prompt],
            cwd=str(self.workdir),
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"cursor failed (exit {result.returncode}): {result.stderr}")
        
        return result.stdout.strip()
```

**Step 4: Run** → PASS

**Step 5: Commit**

---

### Task 1.2: QA — CursorAgent works end-to-end

**Verification:**
1. `cd backend && python -m pytest tests/test_cursor_agent.py -v` → PASS
2. `python -c "from app.services.cursor_agent import CursorAgent; a=CursorAgent(); print(a.run('Reply OK'))"` → outputs text
3. **Fix failures before completing.**

---

## Phase 2: owl-alpha Service (Simple AI)

### Task 2.1: Create owl-alpha service

**Objective:** Thin OpenRouter API client for simple extraction/classification that doesn't need Cursor tools.

**Files:**
- Create: `backend/app/services/owl_alpha.py`
- Test: `tests/test_owl_alpha.py`

**Implementation:**
```python
"""owl-alpha via OpenRouter — for simple extraction/classification."""
import os, httpx

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "owl-alpha"

async def call_owl(system: str, user: str, max_tokens=2000) -> str:
    async with httpx.AsyncClient() as c:
        resp = await c.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={"model": MODEL, "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ], "max_tokens": max_tokens},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

async def extract_company(jd_text: str) -> str:
    return await call_owl(
        "Extract the company name from this job description. Reply with ONLY the name.",
        jd_text[:3000]
    )

async def assess_legitimacy(jd_text: str) -> str:
    return await call_owl(
        "Assess if this job posting is legitimate. Reply LEGIT or SCAM and one sentence why.",
        jd_text[:3000]
    )
```

**Test, verify, commit.**

---

### Task 2.2: QA — owl-alpha service

**Verification:**
1. `cd backend && python -m pytest tests/test_owl_alpha.py -v` → PASS (2 tests)
2. `python -c "from app.services.owl_alpha import extract_company; import asyncio; print(asyncio.run(extract_company('Google is hiring a Frontend Engineer...')))"` → "Google"
3. **Fix failures before completing.**

---

## Phase 3: Evaluate Route — Dual Brain (owl-alpha triage + Cursor full eval)

### Task 3.1: BUILD — Refactor evaluate endpoint to dispatch correctly

**Objective:** Evaluate endpoint first checks liveness (if URL), uses owl-alpha for quick triage, then dispatches Cursor for full A-G report.

**Files:**
- Modify: `backend/app/routers/evaluate.py`
- Test: `tests/test_evaluate.py`

**Implementation:**

Current evaluate endpoint calls `_evaluate_with_api`. New flow:
1. If URL provided → url_fetcher checks liveness → dead returns warning
2. owl-alpha extracts company name + quick legitimacy triage
3. CursorAgent runs full evaluation with Career Ops mode context (reads `_shared.md`, builds prompt from mode)
4. Parse Cursor output → save report to `reports/` → add to tracker → return

```python
@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(req: EvaluateRequest):
    if not req.text and not req.url:
        raise HTTPException(400, "Provide 'text' or 'url'")
    
    # 1. Fetch from URL if needed
    if req.url:
        fetched = await fetch_job_posting(req.url)
        if not fetched.is_live:
            return EvaluateResponse(
                report=f"⚠️ Posting appears inactive: {fetched.error}",
                company="", role="", report_path=""
            )
        jd_text = fetched.text
    else:
        jd_text = req.text

    # 2. Quick triage with owl-alpha (cheap, fast)
    company_raw = await extract_company(jd_text)
    
    # 3. Full evaluation via Cursor (expensive, thorough)
    agent = CursorAgent(workdir="/opt/career-ops", timeout=300)
    
    # Load the evaluation mode context
    mode_path = Path("/opt/career-ops/modes/_shared.md")
    mode_context = mode_path.read_text() if mode_path.exists() else ""
    
    prompt = f"""You are evaluating a job application.

{mode_context}

## Job Description

{jd_text[:8000]}

## Instructions

1. Read the CV from /opt/career-ops/cv.md
2. Perform full A-G analysis as defined in the mode context
3. Save the report to /opt/career-ops/reports/ with proper frontmatter (next number)
4. Add an entry to /opt/career-ops/data/applications.md tracker
5. Return the full report content as your final response text.
"""
    
    report = agent.run(prompt)
    
    return EvaluateResponse(
        report=report,
        company=company_raw,
        role="",
        report_path=""
    )
```

**Step 1: Write test first (TDD)**
```python
@pytest.mark.asyncio
async def test_evaluate_with_text(client):
    resp = client.post("/api/evaluate", json={
        "text": "Frontend Developer at Acme Corp. React, TypeScript required."
    })
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["report"]) > 0

@pytest.mark.asyncio
async def test_evaluate_with_url_dead(client):
    resp = client.post("/api/evaluate", json={
        "url": "https://this-definitely-does-not-exist-12345.com/job"
    })
    # Should return liveness warning
    assert "inactive" in resp.json()["report"]
```

**Step 2-5: Test → Fail → Implement → Pass → Commit**

---

### Task 3.2: QA — Full evaluate flow works

**Verification:**
1. `pytest tests/test_evaluate.py -v` → PASS (3 tests)
2. POST to `/api/evaluate` with real JD → returns full A-G report
3. `ls -la /opt/career-ops/reports/ | tail -3` → new report file exists
4. `tail -3 /opt/career-ops/data/applications.md` → tracker has new entry
5. POST with dead URL → returns liveness warning, no crash
6. **Fix failures before completing.**

---

## Phase 4: Scan Route — Cursor Dispatcher

### Task 4.1: BUILD — Scan endpoint dispatches Cursor

**Objective:** `/api/scan` triggers Cursor to run Career Ops scan mode (scans job sources, populates pipeline).

**Files:**
- Create/Modify: `backend/app/routers/scan.py`
- Test: `tests/test_scan.py`

**Implementation:**
```python
@router.post("/scan")
async def trigger_scan():
    agent = CursorAgent(workdir="/opt/career-ops", timeout=300)
    result = agent.run(
        "Run the career scan. Check job sources, find new postings, "
        "add them to data/pipeline.md. Return list of new postings found."
    )
    return {"status": "complete", "result": result}

@router.get("/scan/status")
async def scan_status():
    """Check if a scan is running / last result."""
    last_scan = _last_scan_date(REPORTS_DIR)
    return {"last_scan": last_scan, "status": "idle"}
```

**Test, verify, commit.**

---

### Task 4.2: QA — Scan works

**Verification:**
1. `pytest tests/test_scan.py -v` → PASS
2. POST `/api/scan` → returns complete with postings found tail
3. Check `data/pipeline.md` → entries added
4. GET `/api/scan/status` → returns last_scan date

---

## Phase 5: Pipeline — Evaluate Pending

### Task 5.1: BUILD — Evaluate-pending endpoint

**Objective:** Processes all pending URLs in pipeline: liveness check → Cursor evaluation → tracker update.

**Files:**
- Modify: `backend/app/routers/pipeline.py`
- Test: `tests/test_pipeline_evaluate.py`

**Implementation:**
```python
@router.post("/pipeline/evaluate-pending")
async def evaluate_pending():
    pipeline = read_pipeline()
    pending = pipeline.get("pending", [])
    if not pending:
        return {"status": "no_pending", "count": 0}
    
    agent = CursorAgent(workdir="/opt/career-ops", timeout=600)
    result = agent.run(
        f"Evaluate these {len(pending)} pending job postings: "
        f"{json.dumps(pending)}. For each: check liveness, evaluate live ones, "
        f"generate reports, update tracker. Skip dead URLs."
    )
    return {"status": "complete", "evaluated": len(pending), "result": result}
```

**Test, verify, commit.**

---

### Task 5.2: QA — Pipeline evaluate works

**Verification:**
1. Add a URL to `data/pipeline.md` manually
2. POST `/api/pipeline/evaluate-pending`
3. Check `reports/` → new report for that company
4. Check `applications.md` → new entry

---

## Phase 6: Output — PDF Generation

### Task 6.1: BUILD — PDF generation endpoint

**Objective:** Generate ATS-compatible PDF for a given report, tailored to the job.

**Files:**
- Create/Modify: `backend/app/routers/output.py`
- Test: `tests/test_output.py`

**Implementation:**
```python
@router.post("/output/generate")
async def generate_pdf(report_id: str):
    report_path = REPORTS_DIR / f"{report_id}-*.md"
    agent = CursorAgent(workdir="/opt/career-ops", timeout=120)
    result = agent.run(
        f"Generate a tailored CV PDF for report {report_id}. "
        f"Read the report from reports/, read cv.md, and run generate-pdf.mjs "
        f"with the tailored content. Return the output PDF path."
    )
    return {"status": "complete", "result": result}

@router.get("/output/{filename}")
async def download_pdf(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "PDF not found")
    return FileResponse(file_path, media_type="application/pdf")
```

**Test, verify, commit.**

---

### Task 6.2: QA — PDF generation works

**Verification:**
1. POST `/api/output/generate` with valid report_id
2. `ls /opt/career-ops/output/` → new PDF
3. GET `/api/output/{filename}` → returns PDF bytes (status 200, content-type application/pdf)

---

## Phase 7: Frontend Wiring (All Pages)

### Task 7.1: BUILD — Tracker page wired to API

**Objective:** Tracker page lists, adds, and updates applications from backend.

**Files:**
- Modify: `frontend/src/pages/tracker.astro`

**Changes:**
1. Fetch GET `/api/stats` on load → show summary cards
2. Fetch GET `/api/tracker` → populate table
3. "Add" form → POST `/api/tracker`
4. Status dropdown → PATCH `/api/tracker`
5. Loading spinner while fetching, empty state when no apps

**Verify:** `npm run build` → 0 errors. Manual: page shows data.

**Commit**

---

### Task 7.2: BUILD — Reports page wired

**Files:**
- Modify: `frontend/src/pages/reports.astro`
- Modify: `frontend/src/pages/report.astro`

**Changes:**
1. Reports list page: GET `/api/reports` → show table
2. Single report page: GET `/api/reports/{id}` → render full markdown

**Verify, commit.**

---

### Task 7.3: BUILD — Stats/Dashboard page wired

**Files:**
- Modify: `frontend/src/pages/index.astro`

**Changes:**
1. GET `/api/stats` → show stats cards
2. Conversion funnel → parse from tracker data
3. Activity timeline → recent reports + tracker entries

**Verify, commit.**

---

### Task 7.4: BUILD — Profile page wired

**Files:**
- Modify: `frontend/src/pages/profile.astro`

**Changes:**
1. GET `/api/profile` → show current profile
2. PUT `/api/profile` → save changes
3. GET `/api/profile/cv` + PUT → edit CV

**Verify, commit.**

---

### Task 7.5: BUILD — Evaluate page enhanced

**Files:**
- Modify: `frontend/src/pages/evaluate.astro`

**Changes:**
1. URL input with liveness indicator
2. Text paste for direct JD
3. Progress indicator (liveness → evaluating → done) — Cursor can take 1-3 min
4. Full A-G report displayed as expandable section cards

**Verify, commit.**

---

### Task 7.6: BUILD — Pipeline, Scan, Output, Tools pages wired

**Files:**
- Modify: `frontend/src/pages/pipeline.astro`
- Modify: `frontend/src/pages/scan.astro`
- Modify: `frontend/src/pages/output.astro`
- Modify: `frontend/src/pages/tools.astro`

**Changes:**
- Pipeline: list URLs, add URL form, evaluate-pending button, results
- Scan: trigger button, last scan status, recent results
- Output: list reports, per-report PDF generate button, download link
- Tools: status indicators, maybe config

**Verify, commit.**

---

### Task 7.7: QA — All frontend pages work end-to-end

**Verification:**
1. `cd frontend && npm run build` → 0 errors, 10 pages
2. Navigate to `/` → dashboard shows stats
3. Navigate to `/tracker` → table populated, can add/update
4. Navigate to `/evaluate` → paste JD → get report → see on page
5. Navigate to `/scan` → run scan → see results
6. Navigate to `/output` → generate PDF → download
7. All API calls return 200
8. Browser console: 0 errors

---

## Phase 8: Integration + Final QA

### Task 8.1: QA — Full integration test

**Verification:**
1. `cd backend && python -m pytest tests/ -v` → ALL pass
2. Backend health: GET `/api/health` → `{"status":"ok"}`
3. Full flow: paste JD → evaluate → report saved → tracker updated → view in reports → generate PDF
4. Full flow: add URL to pipeline → evaluate-pending → reports + tracker updated
5. Full flow: scan → pipeline populated → evaluate
6. Frontend: all 10 pages return 200, no console errors
7. `npm run build` in frontend → 0 errors

---

## Dependency Graph

```
Task 1.1 (CursorAgent)   → Task 1.2 (QA)
Task 2.1 (owl-alpha)     → Task 2.2 (QA)
Task 1.2                → Task 3.1 (Evaluate)
Task 2.2                → Task 3.1
Task 3.1 (Evaluate)      → Task 3.2 (QA)
Task 3.2                → Task 4.1 (Scan)
Task 4.1                → Task 4.2 (QA)
Task 3.2                → Task 5.1 (Pipeline eval)
Task 5.1                → Task 5.2 (QA)
Task 3.2                → Task 6.1 (PDF)
Task 6.1                → Task 6.2 (QA)
Task 3.2                → Task 7.1 (Tracker UI)
Task 7.1                → Task 7.2 (Reports UI)
Task 7.2                → Task 7.3 (Dashboard UI)
Task 7.3                → Task 7.4 (Profile UI)
Task 7.4                → Task 7.5 (Evaluate UI)
Task 7.5                → Task 7.6 (Other pages UI)
Task 7.6                → Task 7.7 (All UI QA)
Task 4.2                → Task 7.6
Task 5.2                → Task 7.6
Task 6.2                → Task 7.6
Task 7.7                → Task 8.1 (Integration QA)
```

## Profile Assignment

| Task | Profile | Reason |
|------|---------|--------|
| 1.1, 1.2, 2.1, 2.2, 3.1, 4.1, 5.1, 6.1 | runeforge-coder | All build tasks |
| 3.2, 4.2, 5.2, 6.2, 7.1-7.7, 8.1 | runeforge-coder | All QA tasks |

## Task Attributes (for kanban)

For each task, include:
```yaml
attributes:
  phase: 1-8
  kind: build | qa
  depends_on: [previous task nqc]
  files: [exact paths]
  verify: "exact command + expected output"
```

## Risks + Mitigations

| Risk | Mitigation |
|------|-----------|
| Cursor `--model auto` picks Opus — slow/expensive | Wrap with timeout, cache results |
| Cursor auth expires | Catch auth error, return clear message "Cursor auth expired — run `cursor auth` on VPS" |
| Cursor bash command restrictions | Dispatching prompt should use file tools, not bash |
| Concurrent cursor runs conflict | Pipeline/Scan use sequential, not parallel |
| Frontend slow to update after Cursor task | Polling endpoint for status, or just show "evaluating..." with timeout |
| OpenRouter key rate limits | owl-alpha calls are small (<1000 tokens), rate limits unlikely |

## Architecture Decision Record

**Why both Cursor and owl-alpha?**
- Cursor CLI (`auto` model) = complex tool-using tasks: reads modes, saves files, runs scripts, generates PDFs. Expensive but powerful.
- owl-alpha (OpenRouter API) = simple classification/extraction: company name, legitimacy triage. Fast and cheap (free tier).
- Direct file I/O = CRUD operations: tracker, profile, reports listing, stats. Zero AI needed, instant.

**Why not Cursor for everything?** + speed. Company extraction via Opus 4.8 is like using a Ferrari to check the weather.

**Why not owl-alpha for everything?** It has no tool access. Can't read mode files, save reports, or run scan scripts. Career Ops evaluation needs tool-using Agent.

**Report file format:** Markdown with frontmatter. Parsed by reports.py router globally. Cursor generates, backend just reads.
