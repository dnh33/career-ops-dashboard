# Grill-with-Docs Review: CV Upload & Profile Enrichment Plan

## 5-Axis Review

### Axis 1: Boundaries & Scope
- **In scope:** PDF/DOCX upload → text extraction → LLM extraction (Nemotron-3-Ultra) → diff UI → merge → profile context injection.
- **Out of scope:** Multi-user auth, virus scanning, OCR for scanned PDFs, batch upload, real-time collaboration.
- **Verdict:** Scope is clear and appropriately limited (YAGNI satisfied). No scope creep observed.

### Axis 2: Dependencies & Integration Points
- **Depends on:** Existing `profile.yml`, `cv.md`, `cv_optimize.py`, `OptimizationPanel`, `/api/profile` and `/api/cv` endpoints.
- **Integrates with:** New endpoints `/api/cv/upload-extract` and `/api/profile/enrich` (note: we changed from merge-enrichment to enrich for simplicity).
- **Integration points:** Frontend calls existing export endpoints; backend uses existing config dir.
- **Verdict:** Dependencies are well-defined. Integration uses existing patterns (PUT for profile/cv, new POST for extract/enrich). No circular dependencies.

### Axis 3: Edge Cases & Error States
- **Covered:** Empty/corrupt file (400), unsupported mime (415), file too large (413), LLM extraction failure (fallback to raw text? we plan to raise error and show UI message), merge conflicts (handled in UI via per-field acceptance).
- **Missing:** What happens if the user cancels upload? UI should clear state. What if the backend is down during extraction? Show error and allow retry.
- **Verdict:** Most edge cases addressed; minor additions needed for UX (cancel, retry). Will be noted in implementation.

### Axis 4: Terminology & Glossary (CONTEXT.md updates)
- **CV Upload**: User-submitted PDF/DOCX file for profile enrichment.
- **Extraction**: LLM-structured parsing of CV text into JSON schema.
- **Enrichment**: Merged profile data + embeddings stored for RAG.
- **Profile Context**: Injected system prompt block for all Career Ops LLM calls.
- **Merge Conflict**: Field exists in both current profile and extraction with different values (resolved via per-field acceptance UI).
- **Verdict:** Terms are clear, consistent with existing domain (CV, profile). Add to CONTEXT.md.

### Axis 5: Architectural Decisions (ADRs)
- **ADR-0001: Local Embeddings with ChromaDB** – Chosen for zero cost, offline, sufficient for profile-scale data.
- **ADR-0002: Structured LLM Output via Pydantic** – Ensures reliable JSON from Nemotron-3-Ultra.
- **ADR-0003: Single-User Profile Store (YAML + JSON)** – Minimal migration, human-readable, diff-friendly.
- **ADR-0004: Frontend-Driven Merge UI** – Avoids complex server-side conflict resolution; gives user full control.
- **Verdict:** Each addresses a real trade-off, documented, and not easily reversible without cost.

## Summary
The plan satisfies the 5-axis review. Minor enhancements (cancel/retry UX) can be added during implementation but do not block the plan.

**Decision:** Plan is approved and ready for implementation via subagent-driven-development.