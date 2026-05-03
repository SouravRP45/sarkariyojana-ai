from fastapi import APIRouter, HTTPException
from typing import List
import json
import os
from app.models import UserProfile, SchemeMatch, SchemeMatchResponse
from app.services.scheme_matcher import scheme_matcher
from app.services.data_loader import data_loader
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/schemes", tags=["schemes"])

@router.post("/find", response_model=SchemeMatchResponse)
async def find_schemes(profile: UserProfile):
    """Find eligible schemes based on user profile."""
    matches = scheme_matcher.match_user(profile)
    
    # Filter to only return matches with score >= 40
    filtered_matches = [m for m in matches if m.match_score >= 40]
    
    profile_summary = f"Found {len(filtered_matches)} schemes for a {profile.age}-year-old {profile.gender} from {profile.state}."
    if profile.preferred_language == "hi":
         profile_summary = f"{profile.state} के {profile.age} वर्षीय {profile.gender} के लिए {len(filtered_matches)} योजनाएं मिलीं।"

    return SchemeMatchResponse(
        total_matches=len(filtered_matches),
        schemes=filtered_matches,
        profile_summary=profile_summary
    )

@router.get("/categories")
async def get_categories():
    """Get all scheme categories."""
    filepath = os.path.join(settings.DATA_DIR, "scheme_categories.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"categories": []}

@router.get("/{scheme_id}")
async def get_scheme(scheme_id: str):
    """Get details of a specific scheme."""
    scheme = data_loader.get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme
