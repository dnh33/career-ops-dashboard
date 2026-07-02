# CV Upload & Profile Enrichment — Design Document

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
- Embeddings: Local `sentence-transformers` + ChromaDB (lazy init)

---

## 5-Axis QA Review (Grill-with-Docs)

### Axis 1: Boundaries & Scope
- **In scope:** PDF/DOCX upload → text extraction → LLM extraction → diff UI → merge → profile context injection
- **Out of scope:** Multi-user auth (Phase 6b), virus scanning, batch upload, OCR for scanned PDFs
- **Decision:** Single-file upload, max 10MB, PDF/DOCX only

### Axis 2: Dependencies & Integration Points
- **Depends on:** Existing `profile.yml` / `cv.md` / `cv_optimize.py` / `OptimizationPanel`
- **Integrates with:** `/api/profile` (GET/PUT), `/api/cv` (GET/PUT), `OptimizationPanel` context injection
- **New endpoints:** `/api/cv/upload-extract`, `/api/profile/merge-enrichment`

### Axis 3: Edge Cases & Error States
- Empty/corrupt file → 400 with clear message
- LLM extraction fails → fallback to raw text + manual entry
- Merge conflicts (e.g., skill exists at different level) → diff shows both, user chooses
- Large files (>10MB) → 413 Payload Too Large
- Unsupported format → 415 Unsupported Media Type

### Axis 4: Terminology & Glossary (CONTEXT.md updates)
```
## Language
**CV Upload**: User-submitted PDF/DOCX file for profile enrichment
**Extraction**: LLM-structured parsing of CV text into JSON schema
**Enrichment**: Merged profile data + embeddings stored for RAG
**Profile Context**: Injected system prompt block for all Career Ops LLM calls
**Merge Conflict**: Field exists in both current profile and extraction with different values
```

### Axis 5: Architectural Decisions (ADRs)

**ADR-0001: Local Embeddings with ChromaDB**
- Context: Need RAG for profile context injection
- Decision: Local `sentence-transformers/all-MiniLM-L6-v2` + ChromaDB (file-based)
- Why: Zero cost, offline, no external deps, sufficient for ~100 docs

**ADR-0002: Structured LLM Output via Pydantic**
- Context: Need reliable JSON from Nemotron-3-Ultra
- Decision: Pydantic models + instructor-style structured prompting
- Why: Type safety, validation, retry on parse failure

**ADR-0003: Single-User Profile Store (YAML + JSON)**
- Context: No auth yet; single active user
- Decision: Extend `profile.yml` + new `profile_enriched.json` with embeddings
- Why: Minimal migration, human-readable, diff-friendly

---

## Clarifying Questions (Resolved)

1. **Multi-file upload?** → No, single file per request (YAGNI)
2. **Auto-delete uploaded file after extraction?** → Yes, immediately after text extraction
3. **Merge strategy for lists (skills, experience)?** → Item-level diff by ID/name; user chooses per item
3. **Embedding model?** → `sentence-transformers/all-MiniLM-L6-v2` (384-dim, fast)
4. **LLM prompt template location?** → New `backend/app/prompts/cv_extraction.txt`
5. **Frontend upload zone location?** → Review step in CV Builder (next to export buttons)

---

## Approved — Ready for Implementation Plan