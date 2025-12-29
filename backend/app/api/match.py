from fastapi import APIRouter
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
    matches = matcher.match_resume(resume.dict())
    return {"matches": matches}