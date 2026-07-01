# 🔥 Grill / Roast: Career Ops Full Implementation Plan

**Plan under review:** `/opt/career-ops-dashboard/docs/plans/2026-06-29-full-plan.md`
**Codebase reviewed:** Every router, service, and frontend page in `/opt/career-ops-dashboard/`
**Grill date:** 2026-06-29

---

## 🔴 CRITICAL ISSUES (block shipping)

### C1: CursorAgent stdin design is wrong

The plan assumes:
```python
proc = await asyncio.create_subprocess_exec(
    "cursor", "--model", "auto",
    stdin=asyncio.subprocess.PIPE, ...
)
stdout, stderr = await asyncio.wait_for(
    proc.communicate(input=prompt.encode()), timeout=self.timeout
)
```

**Problem:** `cursor --model auto` does NOT read from stdin for task prompts. Cursor CLI is an interactive tool — it opens sessions, reads workspace context, and operates through its own protocol. You can't just pipe a string to stdin and get a response. The correct Cursor CLI invocation would be something like `cursor --model auto --task "prompt here"` or use its RPC/stdio protocol, but neither is documented for scripted use. **This is the single biggest architectural risk in the entire plan.** If Cursor CLI doesn't support non-interactive invocation, Phase 1-6 all fail.

**Fix:** Before building anything else:
1. SSH into the VPS and run `cursor --help` and `cursor --model auto --help`
2. Verify that Cursor CLI actually supports headless/non-interactive mode
3. If not, pivot to using the OpenRouter API for ALL AI tasks (owl-alpha is already on OpenRouter — switch evaluation to Opus via API too) and drop the Cursor CLI dependency entirely
4. Alternatively, investigate `cursor --wait` or cursor's LSP protocol for programmatic access

---

### C2: No authentication on any API endpoint

Every single API route (evaluate, scan, pipeline, tracker, output, tools, profile, CV, reports, stats) is **completely unauthenticated**. There is no middleware, no API key check, no session validation, nothing. 

The entire system — evaluation, scanning, PDF generation, file access — is exposed to anyone who can reach port 8000 or 8083. Combined with:

- **C2a:** `POST /api/evaluate` costs real money (OpenRouter API calls)
- **C2b:** `POST /api/tools/run` executes bash scripts on the server
- **C2c:** `POST /api/output/generate` triggers expensive Cursor operations
- **C2d:** `PUT /api/cv` overwrites the CV file
- **C2e:** `POST /api/pipeline` and `DELETE /api/pipeline` modify pipeline state

**Fix:** Add API key middleware to FastAPI:
```python
from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader

API_KEY = os.environ.get("CAREER_OPS_API_KEY", "")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(401, "Invalid API key")
```
Apply to ALL routes. The frontend should store the key (or it can be a hardcoded header in Astro's fetch calls since it's server-rendered).

---

### C3: Command injection in `/api/tools/run`

Task 7.2 creates:
```python
result = subprocess.run(
    ["bash", str(script), *args],
    ...
)
```

**Problem:** `args` comes directly from `body.get("args", [])` in the POST request. An attacker sends `{"tool": "dedup", "args": ["; rm -rf /"]}` and now arbitrary commands run. The `allowed` tool name check is good but `args` is NOT sanitized at all.

**Fix:** Either (a) reject all `args` and hardcode parameters per tool, or (b) validate args against a per-tool schema with strict allowlisting. Since these are maintenance scripts that take no arguments, just drop `args` entirely:
```python
if args:
    raise HTTPException(400, "Args not accepted")
```

---

### C4: File path traversal in output download

```python
@router.get("/output/download/{filename}")
async def download_pdf(filename: str):
    return FileResponse(OUTPUT_DIR / filename, ...)
```

**Problem:** `filename = "../../etc/passwd"` → reads arbitrary system files. `Path(filename)` doesn't sanitize `..` or absolute paths.

**Fix:**
```python
filepath = (OUTPUT_DIR / filename).resolve()
if not filepath.is_relative_to(OUTPUT_DIR.resolve()):
    raise HTTPException(403, "Access denied")
return FileResponse(filepath, ...)
```

Same pattern needed for `/api/reports/{report_id}` in the report router.

---

### C5: Race condition on report numbering and `applications.md`

Two concurrent `POST /api/evaluate` requests cause:

1. **Report number collision:** `_next_report_path()` reads the directory, finds the max number, increments. Two requests both see "041" as max and both write "042-...". One overwrites the other.

2. **`applications.md` corruption:** `_read_entries()` + `_write_entries()` in tracker.py has no file locking. Concurrent writes produce corrupted markdown.

**Fix:** 
- Use a file lock (`fcntl.flock` or `portalocker`) for both the report counter and applications.md writes
- Or: switch to a real database (even SQLite) for atomic operations
- At minimum, add FastAPI `BackgroundTasks` + a queue so evaluations are serialized

---

## 🟠 HIGH-SEVERITY ISSUES (will cause production failures)

### H1: No error handling for failed Cursor evaluations

The plan assumes Cursor always returns valid output. What actually happens:
- Cursor returns empty string → report has no content, saves blank file
- Cursor returns partial markdown (e.g., crashes mid-output) → report is truncated
- Cursor returns nonsense → downstream parsing breaks silently

**Fix:** Add validation to the evaluate flow:
```python
report_text = await agent.run(prompt)
# Validate structure
required_headers = {"## A)", "## B)", "## C)", "## D)", "## E)", "## F)", "## G)"}
found = {f"## {chr(65+i)})" for i in range(7) if f"## {chr(65+i)})" in report_text}
if not required_headers.issubset(found):
    # Retry or fall back to owl-alpha API evaluation
    ...
```

### H2: No timeout handling for long-running evaluations

The plan sets CursorAgent timeout at 300s, but:
- `asyncio.wait_for()` will cancel the subprocess, but the Cursor process itself may persist as an orphan
- No cleanup of partially-written report files
- The frontend has no mechanism to show "evaluation timed out" vs "still running"

**Fix:**
- Clean up orphan processes on timeout
- Delete partially-written report files on failure
- Add a `GET /api/evaluate/status/{id}` endpoint for polling
- Frontend should show time elapsed and a "cancel" option

### H3: `applications.md` format is fragile

The tracker uses a markdown table with pipe separators. If any cell content contains `|` (e.g., a URL with query params, or a role description with tables), the entire file becomes corrupted. There's no escaping.

**Fix:**
- Escape pipe characters in cell content: `cell.replace("|", "\\|")`
- Or: switch the tracker to a real data format (JSON, SQLite, or a proper database)
- At minimum: add validation in `_parse_row()` that catches malformed rows

### H4: No rate limiting or abuse prevention

- `/api/evaluate` costs money per call (OpenRouter credits)
- `/api/scan` could trigger expensive scanning operations
- `/api/output/generate` runs PDF generation

Without rate limiting, a single user (or bot) can drain your OpenRouter credits in minutes.

**Fix:** Add rate limiting middleware:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
# Apply per-route: @router.post("/evaluate", ...) + @limiter.limit("5/minute")
```

### H5: No logging infrastructure

The plan mentions "log every evaluation" but there's actually zero logging in the codebase. No request logging, no error logging, no audit trail. When something breaks (and it will), there's no way to diagnose what happened.

**Fix:** Add structured logging:
```python
import logging
logger = logging.getLogger(__name__)

# In every endpoint:
logger.info("evaluate requested", extra={"url": req.url, "company": company_raw})
logger.error("cursor failed", exc_info=True)
```
Add a `logging.config` that writes to both file and stderr (for Docker/systemd).

### H6: Frontend ↔ Backend API mismatch

- `profile.astro` fetches from `/api/profile` AND `/api/cv` (backend handles `/api/profile` but `/api/cv` doesn't exist) ✅ Already flagged
- `evaluate.astro` calls `GET /api/health` for nav status dot — need to verify this endpoint actually exists
- `output.astro` calls `GET /api/output` — endpoint doesn't exist yet ✅ Already flagged
- `tools.astro` calls `POST /api/tools/run` — endpoint doesn't exist yet ✅ Already flagged
- But also: no CORS configuration. If frontend and backend run on different ports during development, everything breaks.

**Fix:** Add CORS middleware to main.py:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
```
(Tighten origins for production.)

### H7: Missing `Python-Markdown` or sanitization for report rendering

`report.astro` renders report content by manually replacing `**bold**`, `*italic*`, backtick code, list items, and `### headers`. This is a half-baked markdown parser that will:
- Break on any markdown feature not explicitly handled (tables, blockquotes, images, links, footnotes)
- Be vulnerable to XSS via HTML in markdown (e.g., `<script>` in report content)
- Misparse nested formatting

**Fix:** Use a proper markdown-to-HTML library like `python-markdown` or on the frontend, use a well-tested renderer. At minimum, sanitize HTML output:
```python
import bleach
clean_html = bleach.clean(raw_html, tags=ALLOWED_TAGS)
```

---

## 🟡 MEDIUM ISSUES (quality/durability concerns)

### M1: Hardcoded paths everywhere

```python
WORKDIR = Path("/opt/career-ops")
CV_FILE = DATA_DIR / "cv.md"
REPORTS_DIR = Path("/opt/career-ops/reports")
```

These work on the current VPS but make testing impossible and deployment to another machine error-prone.

**Fix:** Use environment variables or a config object:
```python
CAREER_OPS_ROOT = Path(os.environ.get("CAREER_OPS_ROOT", "/opt/career-ops"))
```
(Already partially done in evaluator.py but not consistently applied.)

### M2: No session management for long-running Cursor tasks

The evaluate endpoint just calls `await agent.run(prompt)` and blocks until it finishes. For a 1-3 minute Cursor evaluation:
- The HTTP connection must stay alive the entire time
- If the connection drops, the evaluation is lost
- Multiple simultaneous evaluations can exhaust server resources

**Fix:** Implement async job queue:
- Accept the request, return a job ID immediately
- Process the job in a background task
- Client polls for result via `GET /api/evaluate/status/{job_id}`
- Store intermediate state (liveness check done, evaluation in progress, etc.)

### M3: No pagination on reports or tracker endpoints

`GET /api/reports` returns ALL reports. `GET /api/tracker` returns ALL entries. For a user with 500+ applications, this is a performance problem and a memory bomb.

**Fix:** Add pagination:
```python
@router.get("/reports")
async def list_all_reports(page: int = 1, per_page: int = 20):
    all_reports = list_reports(REPORTS_DIR)
    start = (page - 1) * per_page
    return {"reports": all_reports[start:start+per_page], "total": len(all_reports), "page": page}
```

### M4: The `owl-alpha` module is redundant with existing evaluation

The plan adds owl-alpha for company extraction and legitimacy. But `evaluator.py` already has `_extract_company()` that does regex-based extraction. The owl-alpha calls add latency, cost, and a failure surface for marginal benefit.

**Fix:** Use owl-alpha ONLY where regex extraction fails (return "Unknown"). Use regex as primary, owl-alpha as fallback. For legitimacy, owl-alpha is genuinely useful since there's no regex alternative — keep it.

### M5: Depedency ordering issue: Phase 7 depends on Phase 3, but Phase 3 isn't done yet

Tasks 7.1 (fix regex), 7.3 (evaluate progress), and 7.4 (tracker→report link) all depend on the evaluate endpoint actually working. But Tasks 3.1 and 3.2 refactor the evaluate endpoint. The plan correctly models this in the dependency graph but doesn't account for the fact that many frontend fixes can't be VERIFIED until the backend is done.

**Fix:** Add intermediate mock/stub phase where frontend fixes are verified against hardcoded mock responses, then re-verified against real backend after Phase 3 completes.

### M6: No mention of backup or data preservation

All data lives in markdown files in `/opt/career-ops/`. There's no backup strategy mentioned.

**Fix:** Add a cron job or systemd timer to rsync `/opt/career-ops/data/` and `/opt/career-ops/reports/` to a backup location daily. Or at minimum: document the backup process.

### M7: Tests don't cover integration points

The plan has unit tests for each module but no integration tests:
- Does the full evaluate → save → tracker → report chain actually work?
- Does concurrent access to applications.md corrupt data?
- Does frontend correctly parse real (messy) report content?

**Fix:** Add at least 2-3 integration test files that test end-to-end flows against a real (or mocked) FastAPI test client.

---

## 🔵 LOW-SEVERITY ISSUES (nice to have)

### L1: The plan is too ambitious for one sprint

28 tasks is a lot. Given that Cursor CLI viability (C1) is unknown and several tasks depend on sequential completion, this should be divided into:
- **Sprint 1 (Week 1):** Phases 0 + 1 + 2 + basic evaluate (just wiring) — prove the architecture works
- **Sprint 2 (Week 2):** Phases 3-6 — full AI pipeline
- **Sprint 3 (Week 3):** Phase 7 — frontend fixes + polish

### L2: No mention of Docker or deployment

The architecture discussion doesn't mention containerization, deployment scripts, or environment management. The "services" running are just systemd units with manual restarts.

### L3: Plan doesn't specify what "done" looks like

No acceptance criteria beyond "it works." Define measurable completion:
- "Evaluate endpoint processes a JD in < 3 minutes and returns valid A-G report 90% of the time"
- "Tracker page loads < 1 second with 500 entries"
- "All 10 frontend pages pass Lighthouse accessibility score > 90"

### L4: The tools.sh/maintenance scripts don't exist yet

Task 7.2 references tools like `doctor`, `verify`, `dedup`, etc., but none of these scripts exist. This is a whole sub-project that's glossed over in "Task 7.2: Fix tools endpoint."

---

## Summary Scorecard

| Category | Issues Found | Critical | High | Medium | Low |
|----------|-------------|----------|------|--------|-----|
| Architecture & Design | 3 | 2 | 0 | 1 | 0 |
| Security & Safety | 4 | 2 | 1 | 1 | 0 |
| Edge Cases & Failure | 3 | 0 | 2 | 1 | 0 |
| Completeness | 3 | 0 | 1 | 2 | 0 |
| Execution Risk | 2 | 0 | 0 | 1 | 1 |
| **Total** | **15** | **4** | **4** | **6** | **1** |

## Verdict

The plan's **core concept is sound** — dual-brain architecture with file-based storage is pragmatic for a solo developer. But it has **4 critical blockers** that will prevent shipping and **4 high-severity issues** that will cause production incidents. The biggest risks are:

1. **Cursor CLI might not work non-interactively** (kills Phases 1-6)
2. **Zero authentication** (anyone can drain your API credits and execute server commands)
3. **Command injection in tools endpoint** (remote code execution)
4. **Race conditions on flat-file storage** (data corruption under concurrent use)

These must all be resolved before any code is written.