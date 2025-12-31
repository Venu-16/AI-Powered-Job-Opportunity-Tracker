from fastapi import APIRouter, HTTPException
from ..services.matcher import Matcher
from pydantic import BaseModel
from typing import List, Dict

class ResumeData(BaseModel):
    text: str
    skills: List[str]
    experience_years: int
    seniority: str

router = APIRouter()

@router.post("/run")
def run_match(resume: ResumeData):
    """Run job matching for the given resume data."""
    matcher = Matcher()
    # create an in-memory Resume-like dict for one-off matching
    from ..models.resume import Resume
    temp = Resume(text=resume.text, skills=resume.skills)
    matches = matcher.match_resume_with_jobs(temp, [])
    return {"matches": matches}

@router.get("/results/{resume_id}")
def get_results(resume_id: int):
    """Return stored match results for a given resume id."""
    matcher = Matcher()
    results = matcher.get_matches_for_resume(resume_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Resume not found or no matches")
    return results