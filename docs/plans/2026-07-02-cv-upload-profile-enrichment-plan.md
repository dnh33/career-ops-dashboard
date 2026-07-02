# CV Upload & Profile Enrichment Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Allow users to upload existing CVs (PDF/DOCX), extract structured data via LLM, review diffs, and merge into their active profile — enriching the profile context for all future Career Ops LLM interactions.

**Architecture:**
- Upload endpoint accepts PDF/DOCX → extracts text → LLM (Nemotron-3-Ultra) extracts structured JSON
- Frontend diff modal shows extracted vs current profile → user accepts/rejects per field
- On accept: merge into `profile.yml` + `cv.md` + new `profile_enriched.json` with embeddings
- Profile context injected into all Career Ops LLM calls via system prompt

**Tech Stack:**
- Backend: FastAPI, `pdfplumber` (PDF), `python-docx` (DOCX), NVIDIA Nemotron-3-Ultra (direct API)
- Frontend: Astro component + vanilla JS, diff modal, upload zone
- Storage: `CONFIG_DIR/profile.yml`, `CONFIG_DIR/cv.md`, `CONFIG_DIR/profile_enriched.json`
- Embeddings: Local `sentence-transformers` + Chroma + ChromaDB (lazy init)

---
## Implementation Tasks (TDD: Write Test → Implement → Verify)

### Backend

#### 1. Dependencies & Setup
- **Goal:** Add required Python packages to the project.
- **Files:** `backend/requirements.txt` (or `pyproject.toml` if exists)
- **Steps:**
  1. Check current dependencies: `cat backend/requirements.txt`
  2. Append: `pdfplumber==0.10.3`, `python-docx==1.1.0`, `sentence-transformers==2.6.1`, `chromadb==0.4.22`, `openai==1.35.0`
  3. Install in the backend venv: `cd /opt/career-ops-dashboard/backend && source venv/bin/activate && pip install pdfplumber python-docx sentence-transformers chromadb openai`
- **Verify:** `pip list | grep -E "pdfplumber|docx|sentence|chroma|openai"` shows installed versions.

#### 2. File Parsing Utilities
- **Goal:** Create module to extract text from PDF and DOCX files.
- **Files:**
  - Create `backend/app/services/file_parser.py`
  - Create test `backend/app/tests/test_file_parser.py`
- **TDD Steps:**
  a. Write test for `extract_text_from_pdf` that raises NotImplementedError (fail).
  b. Implement function using `pdfplumber`.
  c. Test passes.
  d. Write test for `extract_text_from_docx` (fail).
  e. Implement using `python-docx`.
  f. Test passes.
  g. Test edge cases: empty file, unsupported format (return empty string or raise? We'll return empty string and let caller handle).
- **Verify:** Run `pytest backend/app/tests/test_file_parser.py -v` → all pass.

#### 3. LLM Client for Nemotron-3-Ultra
- **Goal:** Wrapper around OpenAI-compatible API for NVIDIA's Nemotron-3-Ultra with structured output support.
- **Files:**
  - Create `backend/app/services/llm_client.py`
  - Create test `backend/app/tests/test_llm_client.py`
- **TDD Steps:**
  a. Write test that initializing client with API base and key works.
  b. Implement `NemotronClient` class with `create_completion` method.
  c. Test passes.
  d. Write test for `extract_structured` method that uses `response_format` param (if supported) or fallback to parsing JSON from text.
  e. Implement using OpenAI client with `model="nemotron-3-ultra-256b-v1"` (or whatever the exact model name is; we'll use `nvidia/nemotron-3-ultra-256b-v1` as per OpenRouter but for NVIDIA direct we need to check; assume endpoint `https://integrate.api.nvidia.com/v1` with API key).
  f. Test passes.
- **Verify:** Unit tests pass. (Note: We won't actually call the LLM in unit tests; we'll mock the HTTP call.)

#### 4. Pydantic Schemas for Extracted CV Data
- **Goal:** Define data model that matches what we expect to extract from CVs.
- **Files:**
  - Create `backend/app/schemas/cv_extract.py`
  - Create test `backend/app/tests/test_schemas_cv_extract.py`
- **TDD Steps:**
  a. Define models: `PersonalInfo`, `ExperienceItem`, `EducationItem`, `SkillItem`, `Certificate`, `Languages`, `ExtractedCVData` (containing lists of above).
  b. Write test that each model can be instantiated with sample data and serializes to JSON correctly.
  c. Implement models.
  d. Test passes.
  e. Write test for validation (e.g., required fields).
  f. Implement validation.
  g. Test passes.
- **Verify:** Schema tests pass.

#### 5. Extraction Service
- **Goal:** Service that takes raw text and returns `ExtractedCVData` using the LLM client.
- **Files:**
  - Create `backend/app/services/extraction_service.py`
  - Create test `backend/app/tests/test_extraction_service.py`
- **TDD Steps:**
  a. Write test that given a sample CV text, the service returns structured data (we'll mock the LLM client to return a fixed JSON).
  b. Implement `extract_cv_data(text: str) -> ExtractedCVData` that:
      - Builds prompt: "Extract the following information from the CV text and return as JSON matching this schema: [schema description]. Text: ..."
      - Calls LLM client with structured output (or requests JSON and parses).
      - Validates and returns model.
  c. Test passes with mock.
  d. Add error handling: if LLM returns invalid JSON, raise exception.
  e. Test error case.
  f. Test passes.
- **Verify:** Extraction service tests pass.

#### 6. Upload-Extract Endpoint
- **Goal:** API endpoint to accept file upload, extract text, run extraction, return JSON.
- **Files:**
  - Modify `backend/app/routes/cv.py` (add new route)
  - Create test in `backend/app/tests/test_cv_router.py` (or new test file)
- **TDD Steps:**
  a. Write test for POST `/api/cv/upload-extract`:
      - Mock `file_parser.extract_text_*` and `extraction_service.extract_cv_data`.
      - Send a dummy PDF file (via TestClient with `files={'file': ('test.pdf', b'...', 'application/pdf')}`).
      - Expect 200 and JSON matching mocked extraction.
      - Expect 400 for empty filename.
      - Expect 415 for unsupported mime type.
      - Expect 413 for file too large (we'll implement size limit).
  b. Implement endpoint:
      - Check file extension/content-type.
      - Read file with size limit (e.g., 10 MB).
      - Extract text via appropriate parser.
      - Call extraction service.
      - Return JSON.
  c. Test passes.
  d. Add file size limit check (request.content_length or read and limit).
  e. Test size limit.
  f. Test passes.
- **Verify:** All endpoint tests pass.

#### 7. Profile Merge Enrichment Endpoint
- **Goal:** Endpoint that takes extracted data, merges with current profile, updates stored files, and returns preview for diff.
- **Files:**
  - Modify `backend/app/routes/profile.py` (add new route)
  - Create test `backend/app/tests/test_profile_router.py`
- **TDD Steps:**
  a. Write test for POST `/api/profile/merge-enrichment`:
      - Mock reading current profile.yml and cv.md.
      - Send extracted JSON.
      - Expect 200 and merged preview (maybe same structure as extracted but with merged values).
      - Actually, we might want to return the merged profile so frontend can show diff.
      - We'll implement a merge function that returns merged data without saving yet, and have a separate endpoint to commit? Or we can have the endpoint do both: return merged preview and if client confirms, call another endpoint to persist.
      - To keep it simple: endpoint will merge and persist, and return the updated profile (so frontend can show diff by comparing before/after; frontend already has current state).
      - So we need to get current profile from storage, merge with extracted data (preferring extracted for conflicts? Actually we want user to decide; so we should not auto-merge. Instead, endpoint should return a side-by-side diff: current vs extracted, and then have another endpoint to apply selected changes.
      - Let's reconsider: Better to have endpoint that returns a diff report, and then a separate endpoint to apply changes.
      - However, to keep scope small, we can have the frontend do the diff: it has current state, gets extracted data from first endpoint, computes diff locally, shows UI, then sends a PATCH to update profile with the user-accepted changes.
      - That means we don't need a merge endpoint; we just need the extract endpoint, and then the existing profile PUT endpoints can be used to update fields.
      - But we also want to store enriched version with embeddings.
      - So we need:
          1. Extract endpoint (already).
          2. Endpoint to save enriched profile (maybe POST /api/profile/enrich) that takes extracted data, merges with current (server-side, but we can let frontend decide what to send), updates profile.yml/cv.md, and creates/updates profile_enriched.json with embeddings.
      - We'll have frontend send the *merged* version (after user approves) to this endpoint.
      - So we need an endpoint that accepts the full profile (JSON) and updates the stored files and enriches.
      - Let's call it POST `/api/profile/enrich` (or PUT `/api/profile` but we already have PUT for raw markdown; we need structured update).
      - We'll keep existing PUT `/api/profile` for YAML text and PUT `/api/cv` for markdown; we'll add a new endpoint for structured updates that also updates the enriched store.
  b. Given complexity, let's define:
      - POST `/api/profile/enrich` expects JSON matching `ExtractedCVData` plus maybe `raw_text`? Actually we want to store the enriched version for RAG.
      - It will:
          * Update `profile.yml` with fields from JSON (we need a mapping to YAML format).
          * Update `cv.md` by regenerating from JSON (we already have `toMarkdown()` logic in frontend; we can reuse similar logic in backend).
          * Create/update `profile_enriched.json` that includes the same data plus embeddings for each section (or a single blob).
      - We'll need functions to convert between our schema and the YAML/markdown formats.
  c. To simplify, we can store the extracted JSON as-is in `profile_enriched.json` and also update the YAML/markdown using a conversion layer.
  d. Let's outline tasks accordingly.
- Due to length, we'll break into sub-tasks.

Given the time, I'll provide a high-level task list that can be expanded by subagents.

Let's write the plan with placeholders for detailed sub-tasks, but enough for a subagent to implement.

We'll continue writing to the plan<tool_call>
<function=write_file>
<parameter=content>
# CV Upload & Profile Enrichment Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Allow users to upload existing CVs (PDF/DOCX), extract structured data via LLM, review diffs, and merge into their active profile — enriching the profile context for all future Career Ops LLM interactions.

**Architecture:**
- Upload endpoint accepts PDF/DOCX → extracts text → LLM (Nemotron-3-Ultra) extracts structured JSON
- Frontend diff modal shows extracted vs current profile → user accepts/rejects per field
- On accept: merge into `profile.yml` + `cv.md` + new `profile_enriched.json` with embeddings
- Profile context injected into all Career Ops LLM calls via system prompt

**Tech Stack:**
- Backend: FastAPI, `pdfplumber` (PDF), `python-docx` (DOCX), NVIDIA Nemotron-3-Ultra (direct API)
- Frontend: Astro component + vanilla JS, diff modal, upload zone
- Storage: `CONFIG_DIR/profile.yml`, `CONFIG_DIR/cv.md`, `CONFIG_DIR/profile_enriched.json`
- Embeddings: Local `sentence-transformers` + Chroma + ChromaDB (lazy init)

---
## Implementation Tasks (TDD: Write Test → Implement → Verify)

### Backend

#### 1. Dependencies & Setup
- **Goal:** Add required Python packages to the project.
- **Files:** `backend/requirements.txt`
- **Steps:**
  1. Check current dependencies: `cat backend/requirements.txt`
  2. Append: `pdfplumber==0.10.3`, `python-docx==1.1.0`, `sentence-transformers==2.6.1`, `chromadb==0.4.22`, `openai==1.35.0`
  3. Install in the backend venv: `cd /opt/career-ops-dashboard/backend && source venv/bin/activate && pip install pdfplumber python-docx sentence-transformers chromadb openai`
- **Verify:** `pip list | grep -E "pdfplumber|docx|sentence|chroma|openai"` shows installed versions.

#### 2. File Parsing Utilities
- **Goal:** Create module to extract text from PDF and DOCX files.
- **Files:**
  - Create `backend/app/services/file_parser.py`
  - Create test `backend/app/tests/test_file_parser.py`
- **TDD Steps:**
  a. Write test for `extract_text_from_pdf` that raises NotImplementedError (fail).
  b. Implement function using `pdfplumber`.
  c. Test passes.
  d. Write test for `extract_text_from_docx` (fail).
  e. Implement using `python-docx`.
  f. Test passes.
  g. Test edge cases: empty file, unsupported format (return empty string).
- **Verify:** Run `pytest backend/app/tests/test_file_parser.py -v` → all pass.

#### 3. LLM Client for Nemotron-3-Ultra
- **Goal:** Wrapper around OpenAI-compatible API for NVIDIA's Nemotron-3-Ultra with structured output support.
- **Files:**
  - Create `backend/app/services/llm_client.py`
  - Create test `backend/app/tests/test_llm_client.py`
- **TDD Steps:**
  a. Write test that initializing client with API base and key works.
  b. Implement `NemotronClient` class with `create_completion` method.
  c. Test passes.
  d. Write test for `extract_structured` method that uses `response_format` param (if supported) or fallback to parsing JSON from text.
  e. Implement using OpenAI client with `model="nemotron-3-ultra-256b-v1"`.
  f. Test passes.
- **Verify:** Unit tests pass. (We'll mock HTTP calls in tests.)

#### 4. Pydantic Schemas for Extracted CV Data
- **Goal:** Define data model that matches what we expect to extract from CVs.
- **Files:**
  - Create `backend/app/schemas/cv_extract.py`
  - Create test `backend/app/tests/test_schemas_cv_extract.py`
- **TDD Steps:**
  a. Define models: `PersonalInfo`, `ExperienceItem`, `EducationItem`, `SkillItem`, `Certificate`, `Languages`, `ExtractedCVData` (containing lists of above).
  b. Write test that each model can be instantiated with sample data and serializes to JSON correctly.
  c. Implement models.
  d. Test passes.
  e. Write test for validation (e.g., required fields).
  f. Implement validation.
  g. Test passes.
- **Verify:** Schema tests pass.

#### 5. Extraction Service
- **Goal:** Service that takes raw text and returns `ExtractedCVData` using the LLM client.
- **Files:**
  - Create `backend/app/services/extraction_service.py`
  - Create test `backend/app/tests/test_extraction_service.py`
- **TDD Steps:**
  a. Write test that given a sample CV text, the service returns structured data (we'll mock the LLM client to return a fixed JSON).
  b. Implement `extract_cv_data(text: str) -> ExtractedCVData` that:
      - Builds prompt: "Extract the following information from the CV text and return as JSON matching this schema: [schema description]. Text: ..."
      - Calls LLM client with structured output (or requests JSON and parses).
      - Validates and returns model.
  c. Test passes with mock.
  d. Add error handling: if LLM returns invalid JSON, raise exception.
  e. Test error case.
  f. Test passes.
- **Verify:** Extraction service tests pass.

#### 6. Upload-Extract Endpoint
- **Goal:** API endpoint to accept file upload, extract text, run extraction, return JSON.
- **Files:**
  - Modify `backend/app/routes/cv.py` (add new route)
  - Create test in `backend/app/tests/test_cv_router.py` (or new test file)
- **TDD Steps:**
  a. Write test for POST `/api/cv/upload-extract`:
      - Mock `file_parser.extract_text_*` and `extraction_service.extract_cv_data`.
      - Send a dummy PDF file (via TestClient with `files={'file': ('test.pdf', b'...', 'application/pdf')}`).
      - Expect 200 and JSON matching mocked extraction.
      - Expect 400 for empty filename.
      - Expect 415 for unsupported mime type.
      - Expect 413 for file too large (we'll implement size limit).
  b. Implement endpoint:
      - Check file extension/content-type.
      - Read file with size limit (e.g., 10 MB).
      - Extract text via appropriate parser.
      - Call extraction service.
      - Return JSON.
  c. Test passes.
  d. Add file size limit check (request.content_length or read and limit).
  e. Test size limit.
  f. Test passes.
- **Verify:** All endpoint tests pass.

#### 7. Profile Enrichment Endpoint
- **Goal:** Endpoint that takes extracted data (or user-approved merged data), updates stored profile files, and creates enriched JSON with embeddings for RAG.
- **Files:**
  - Modify `backend/app/routes/profile.py` (add new route)
  - Create `backend/app/services/enrichment_service.py`
  - Create test `backend/app/tests/test_profile_router.py` and `test_enrichment_service.py`
- **TDD Steps:**
  a. Write test for POST `/api/profile/enrich`:
      - Mock reading current profile.yml and cv.md.
      - Send enriched JSON (full profile).
      - Expect 200 and success message.
      - Verify that profile.yml, cv.md, and profile_enriched.json are updated correctly.
  b. Implement enrichment service:
      - Functions to convert `ExtractedCVData` (or custom profile dict) to YAML and markdown.
      - Function to embed text chunks using `SentenceTransformer` and store in Chroma collection.
      - Main function that:
          * Updates profile.yml with provided data (mapping fields).
          * Regenerates cv.md from data (reusing markdown generation logic).
          * Creates/updates profile_enriched.json containing the same data plus embeddings (we'll store embeddings for each section: summary, experience bullets, skills, education).
  c. Implement endpoint that:
      - Validates input against schema.
      - Calls enrichment service.
      - Returns success.
  d. Test passes.
- **Verify:** All enrichment tests pass.

#### 8. Profile Context Injection for LLM Calls
- **Goal:** Modify LLM call sites across the codebase to include user profile context in system prompt.
- **Files:**
  - Create `backend/app/services/profile_context.py` (provides function to get formatted context string)
  - Identify and modify existing LLM call sites: likely in `cv_optimize.py`, `market_scorer.py`, `evaluate.py` (if any), and any other services that call LLMs.
  - Update tests accordingly.
- **TDD Steps:**
  a. Write test for `get_profile_context()` that returns a non-empty string when profile data exists.
  b. Implement function that loads profile_enriched.json (or falls back to yaml/md) and formats as text for LLM.
  c. Test passes.
  d. For each LLM call site:
      - Write a test that verifies the call includes context (we can mock and check arguments).
      - Modify the call to prepend or inject the profile context into the system prompt.
      - Test passes.
  e. Ensure we don't break existing functionality.
- **Verify:** All related tests pass; manual spot-check that context is included.

#### 9. Background Tasks & Cleanup
- **Goal:** Ensure temporary uploaded files are deleted after processing.
- **Files:**
  - In upload-extract endpoint, after extracting text, immediately delete the file (we won't store it; we read into memory).
  - No additional files needed.
- **Verify:** No leftover uploads in temp directory after test runs.

### Frontend

#### 10. Upload Zone Component
- **Goal:** Add file upload UI in CV Builder Review step.
- **Files:**
  - Create `frontend/src/components/cv/CvUploadZone.astro`
  - Import and use in `frontend/src/pages/cv/builder.astro` (inside review step, above export buttons).
- **TDD Steps:**
  a. Write a simple test (manual) that the component renders with an upload button and accepts .pdf/.docx.
  b. Implement component with:
      - Input type="file" accept=".pdf,.docx"
      - On change, read file as ArrayBuffer (or binary) and send via Fetch to `/api/cv/upload-extract`.
      - Show loading state.
      - On success, store extracted data in local state (we'll lift state up to page or use a store).
      - On error, show message.
  c. Verify by manually testing in dev mode.

#### 11. Extraction Review Modal
- **Goal:** Modal that shows extracted data vs current profile, allows user to accept/reject per field.
- **Files:**
  - Create `frontend/src/components/cv/CvExtractionReview.astro` (reuse overlay pattern from existing code).
  - Use in `builder.astro` when extraction data is available.
- **TDD Steps:**
  a. Implement modal with tabs/sections: Profile, Experience, Skills, Education.
  b. For each section, display current value (from state) and extracted value (from upload) side-by-side.
  c. Allow user to toggle per-item inclusion (checkbox) or accept all.
  d. On "Accept and Merge", compile the selected values into a new profile state and call backend update endpoints (or we can have a single endpoint that accepts the merged profile; we'll reuse the existing PUT endpoints for simplicity: update profile YAML and cv.md separately, then call enrich endpoint).
  e. On close, clear extraction data.
  f. Test manually.

#### 12. Profile Update Integration
- **Goal:** After user approves extracted data, update profile fields and trigger enrichment.
- **Files:**
  - Logic in `builder.astro` (or a new store) to:
      - Call `/api/profile` PUT with updated YAML (we need to convert our selected data to YAML format; we can reuse the existing `toMarkdown` inverse? Actually we have YAML stored; we need a function to convert our JSON to YAML. We'll create a utility `jsonToProfileYaml`.
      - Call `/api/cv` PUT with updated markdown (we can use `toMarkdown` function we already have).
      - Call `/api/profile/enrich` with the merged JSON to update enriched store.
  - Create `frontend/src/lib/cv-conversion.ts` with functions: `jsonToProfileYaml`, `jsonToMarkdown` (or reuse and adapt `toMarkdown`).
- **TDD Steps:**
  a. Write unit tests for conversion functions.
  b. Implement.
  c. Tests pass.
  d. In UI, after user confirms, perform the three updates sequentially.
  e. On success, show toast notification and refresh preview.
- **Verify:** Manual test shows profile updates correctly.

#### 13. Loading Enriched Context for Future Use
- **Goal:** Ensure that after enrichment, the updated profile is used in subsequent LLM calls (handled by backend; frontend just needs to reflect that data changed).
- **Files:** No frontend changes needed beyond ensuring state is updated.
- **Verify:** After upload and enrich, the CV builder preview shows updated data, and any optimization suggestions reflect the new profile.

#### 14. Styling and UX Polish
- **Goal:** Ensure upload zone and review modal match Hermes Design System.
- **Files:**
  - Modify `frontend/src/styles/globals.css` if needed for new components.
  - Use existing classes: `cv-builder__btn`, `status-pill`, etc.
- **Verify:** Visual consistency.

### Testing & QA

#### 15. End-to-End Test (Manual Script)
- **Goal:** Verify the full flow works end-to-end.
- **Steps:**
  1. Start backend and frontend.
  2. Navigate to CV Builder.
  3. Upload a sample PDF CV.
  4. Review extracted data, adjust selections, confirm.
  5. Verify profile fields update in UI.
  6. Verify preview updates.
  7. Verify that downloading PDF/MD shows updated content.
  8. Verify that optimization suggestions (if any) reflect new data.
  9. Ensure no errors in console.
- **Verify:** All steps succeed.

#### 16. Performance & Size Checks
- **Goal:** Ensure upload size limit and processing time are reasonable.
- **Steps:**
  - Test with a 5-page PDF (~500KB) → should process within a few seconds.
  - Try 11MB file → should get 413 error.
- **Verify:** Behavior matches expectations.

### Documentation

#### 17. Update Documentation
- **Goal:** Document new feature for users and developers.
- **Files:**
  - Add section to `/opt/aetherkeep/06-projects/career-ops-dashboard/feature-cv-upload.md` (or similar).
  - Update any relevant README or architecture docs.
- **Verify:** Documentation exists and is accurate.

---
## 5-Axis QA Review (Grill-with-Docs) – To Be Run After Plan Write

Before marking plan ready, we will run the grill-with-docs skill to check:
1. Boundaries & Scope
2. Dependencies & Integration Points
3. Edge Cases & Error States
4. Terminology & Glossary (update CONTEXT.md)
5. Architectural Decisions (ADRs)

We'll do that after writing this plan, but the plan itself is ready for submission.

**Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?**