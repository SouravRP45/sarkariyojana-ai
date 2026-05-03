"""Pydantic models for the application."""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """Citizen profile for scheme matching."""
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=18, le=120)
    gender: Literal["male", "female", "other"]
    state: str
    district: Optional[str] = None
    occupation: Literal[
        "farmer", "student", "entrepreneur", "salaried",
        "unemployed", "retired", "homemaker", "artisan",
        "street_vendor", "other"
    ]
    annual_income: Optional[int] = Field(None, ge=0)
    caste_category: Literal["general", "obc", "sc", "st"]
    is_bpl: bool = False
    has_disability: bool = False
    marital_status: Literal["single", "married", "widowed", "divorced"] = "single"
    num_children: Optional[int] = Field(None, ge=0)
    has_bank_account: bool = True
    has_aadhaar: bool = True
    is_land_owner: bool = False
    preferred_language: Literal["en", "hi"] = "en"


class SchemeMatch(BaseModel):
    """A matched government scheme with score."""
    scheme_id: str
    scheme_name: str
    scheme_name_hi: str = ""
    ministry: str = ""
    category: str = ""
    match_score: float = Field(..., ge=0, le=100)
    match_reasons: list[str] = []
    benefits_summary: str = ""
    how_to_apply: str = ""
    documents_needed: list[str] = []
    official_url: str = ""
    helpline: str = ""
    description: str = ""
    description_hi: str = ""
    scheme_type: str = "central"


class SchemeMatchResponse(BaseModel):
    """Response containing all matched schemes."""
    total_matches: int
    schemes: list[SchemeMatch]
    profile_summary: str = ""


class ChatRequest(BaseModel):
    """Chat request body."""
    message: str = Field(..., min_length=1)
    user_profile: Optional[UserProfile] = None
    chat_history: list[dict] = []


class ChatResponse(BaseModel):
    """Chat response body."""
    role: str = "assistant"
    content: str
    timestamp: str = ""
    schemes_referenced: list[str] = []


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    version: str = ""
    schemes_loaded: int = 0
