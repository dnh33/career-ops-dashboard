"""Career Ops Dashboard — backend configuration.

Paths point to career-ops directories. Override via env vars.
"""
import os
from pathlib import Path

# Career Ops root (where career-ops CLI data lives)
CAREER_OPS_ROOT: Path = Path(
    os.getenv("CAREER_OPS_ROOT", "/opt/career-ops")
)

# Sub-directories
DATA_DIR: Path = CAREER_OPS_ROOT / "data"
REPORTS_DIR: Path = CAREER_OPS_ROOT / "reports"
JDS_DIR: Path = CAREER_OPS_ROOT / "jds"
OUTPUT_DIR: Path = CAREER_OPS_ROOT / "output"
CONFIG_DIR: Path = CAREER_OPS_ROOT / "config"

# Dashboard root
DASHBOARD_ROOT: Path = Path(
    os.getenv("CAREER_OPS_DASHBOARD_ROOT", "/opt/career-ops-dashboard")
)

# API / model config
OPENROUTER_BASE_URL: str = os.getenv(
    "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
)
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
NVIDIA_NIM_BASE_URL: str = os.getenv(
    "NVIDIA_NIM_BASE_URL", "https://integrate.api.nvidia.com/v1"
)
NVIDIA_NIM_API_KEY: str = os.getenv("NVIDIA_NIM_API_KEY", "")

AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openrouter")  # openrouter | nvidia

# Server
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
RELOAD: bool = os.getenv("RELOAD", "true").lower() in ("1", "true", "yes")

# Allowed CORS origins (frontend dev server + tailscale)
CORS_ORIGINS: list[str] = os.getenv(
    "CORS_ORIGINS", "http://localhost:4321,http://localhost:3000"
).split(",")


def career_ops_connected() -> bool:
    """Check that the career-ops directory tree is reachable."""
    return (
        CAREER_OPS_ROOT.exists()
        and DATA_DIR.exists()
        and REPORTS_DIR.exists()
    )
