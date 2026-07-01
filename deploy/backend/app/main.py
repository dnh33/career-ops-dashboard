"""Career Ops Dashboard — FastAPI application."""
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

from app.config import CORS_ORIGINS
from app.routers import (
    evaluate,
    scan,
    tracker,
    reports,
    pipeline,
    profile,
    output,
    stats,
)

API_KEY = os.environ.get("CAREER_OPS_API_KEY", "")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(key: str = Depends(api_key_header)):
    if not API_KEY:
        return  # dev mode — no key configured
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


app = FastAPI(
    title="Career Ops Dashboard API",
    description="Web backend for career-ops CLI",
    version="0.1.0",
    dependencies=[Depends(verify_api_key)],
)

# CORS — allow frontend dev server and tailscale origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(tracker.router, prefix="/api", tags=["tracker"])
app.include_router(reports.router, prefix="/api", tags=["reports"])
app.include_router(evaluate.router, prefix="/api", tags=["evaluate"])
app.include_router(scan.router, prefix="/api", tags=["scan"])
app.include_router(pipeline.router, prefix="/api", tags=["pipeline"])
app.include_router(profile.router, prefix="/api", tags=["profile"])
app.include_router(output.router, prefix="/api", tags=["output"])


@app.get("/api/health", tags=["system"])
async def health():
    """Health check — verifies backend is up and career-ops dirs are reachable."""
    from app.config import career_ops_connected

    connected = career_ops_connected()
    return {
        "status": "ok" if connected else "degraded",
        "career_ops_connected": connected,
    }
