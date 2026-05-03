from app.models import UserProfile, SchemeMatch
from app.services.data_loader import data_loader

class SchemeMatcher:
    def match_user(self, profile: UserProfile) -> list[SchemeMatch]:
        matches = []
        all_schemes = data_loader.get_all_schemes()

        for scheme in all_schemes:
            score, reasons = self._evaluate_scheme(profile, scheme)
            if score >= 40:
                matches.append(SchemeMatch(
                    scheme_id=scheme["id"],
                    scheme_name=scheme["name"],
                    scheme_name_hi=scheme.get("name_hi", ""),
                    ministry=scheme.get("ministry", ""),
                    category=scheme.get("category", ""),
                    match_score=score,
                    match_reasons=reasons,
                    benefits_summary=scheme.get("benefits", ""),
                    how_to_apply=scheme.get("application_process", ""),
                    documents_needed=scheme.get("documents_required", []),
                    official_url=scheme.get("official_url", ""),
                    helpline=scheme.get("helpline", ""),
                    description=scheme.get("description", ""),
                    description_hi=scheme.get("description_hi", ""),
                    scheme_type=scheme.get("type", "central")
                ))
        
        # Sort by score descending
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches

    def _evaluate_scheme(self, profile: UserProfile, scheme: dict):
        e = scheme.get("eligibility", {})
        score = 100
        reasons = []

        # Hard criteria - if these fail, score drops to 0
        if e.get("states") and "all" not in e["states"] and profile.state not in e["states"]:
            return 0, ["State mismatch"]
        
        if e.get("gender") and e["gender"] != "all" and profile.gender != e["gender"]:
            return 0, ["Gender mismatch"]

        if e.get("min_age") and profile.age < e["min_age"]:
            return 0, [f"Age below minimum required ({e['min_age']})"]
            
        if e.get("max_age") and profile.age > e["max_age"]:
            return 0, [f"Age above maximum allowed ({e['max_age']})"]

        if e.get("income_limit") and profile.annual_income is not None:
            if profile.annual_income > e["income_limit"]:
                return 0, [f"Income exceeds limit ({e['income_limit']})"]
            else:
                reasons.append("Income criteria met")

        # Soft criteria - partial points
        if e.get("occupation") and "all" not in e["occupation"]:
            if profile.occupation in e["occupation"]:
                reasons.append("Occupation matches")
            else:
                score -= 20
                
        if e.get("caste_category") and "all" not in e["caste_category"]:
             if profile.caste_category not in e["caste_category"]:
                 score -= 20

        if e.get("bpl") is not None:
            if e["bpl"] == True and not profile.is_bpl:
                score -= 30
            elif e["bpl"] == True and profile.is_bpl:
                reasons.append("BPL criteria met")

        if e.get("marital_status") and profile.marital_status not in e["marital_status"]:
            score -= 10
            
        if e.get("land_ownership") is True and not profile.is_land_owner:
            score -= 20
            
        if not reasons:
            reasons.append("Meets basic eligibility criteria")

        return max(0, score), reasons

scheme_matcher = SchemeMatcher()
