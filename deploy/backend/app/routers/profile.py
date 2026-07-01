"""Profile router — CV and profile management endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import CONFIG_DIR

router = APIRouter(tags=["profile"])


class ProfileData(BaseModel):
    profile: str


class CVData(BaseModel):
    cv: str


@router.get("/profile")
async def get_profile():
    """Get user profile from config/profile.yml."""
    profile_path = CONFIG_DIR / "profile.yml"
    if not profile_path.exists():
        return {"profile": None, "message": "Profile file not found"}
    content = profile_path.read_text(encoding="utf-8")
    return {"profile": content}


@router.put("/profile")
async def update_profile(data: ProfileData):
    """Update user profile YAML."""
    try:
        profile_path = CONFIG_DIR / "profile.yml"
        profile_path.write_text(data.profile, encoding="utf-8")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cv")
async def get_cv():
    """Get CV markdown content."""
    cv_path = CONFIG_DIR / "cv.md"
    if not cv_path.exists():
        return {"cv": None, "message": "CV file not found"}
    content = cv_path.read_text(encoding="utf-8")
    return {"cv": content}


@router.put("/cv")
async def update_cv(data: CVData):
    """Update CV markdown content."""
    try:
        cv_path = CONFIG_DIR / "cv.md"
        cv_path.write_text(data.cv, encoding="utf-8")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
