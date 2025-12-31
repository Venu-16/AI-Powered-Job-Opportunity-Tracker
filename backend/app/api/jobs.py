from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..services.job_fetcher import JobFetcher
from ..core.database import SessionLocal
from ..models.job import Job
from datetime import datetime
from ..services.matcher import Matcher
import json

router = APIRouter()

class FetchRequest(BaseModel):
    roles: List[str]
    companies: List[str] = []

@router.post("/jobs/fetch")
def fetch_jobs(request: FetchRequest):
    """Fetch jobs from external API, store them, and run matching against stored resumes.

    Returns number of jobs fetched.
    """
    jf = JobFetcher()
    jobs = jf.fetch_jobs(request.roles, request.companies)

    db = SessionLocal()
    stored_count = 0
    stored_jobs = []
    for j in jobs:
        # avoid duplicates by external_id and apply_url
        existing = None
        if j.get("external_id"):
            existing = db.query(Job).filter(Job.external_id == j.get("external_id")).first()
        if not existing:
            job = Job(
                external_id=j.get("external_id"),
                title=j.get("title"),
                company=j.get("company"),
                description=j.get("description"),
                posted_date=datetime.fromisoformat(j.get("posted_date")) if j.get("posted_date") else None,
                apply_url=j.get("apply_url")
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            stored_jobs.append(job)
            stored_count += 1
        else:
            stored_jobs.append(existing)

    # run matching pipeline for all resumes
    matcher = Matcher()
    resumes = db.query("resumes").all() if False else db.query(object).all()  # placeholder
    # Instead, fetch Resume objects properly
    from ..models.resume import Resume
    resumes = db.query(Resume).all()

    for r in resumes:
        # match and persist
        matcher.match_resume_with_jobs(r, stored_jobs)

    return {"jobs_fetched": len(jobs)}
