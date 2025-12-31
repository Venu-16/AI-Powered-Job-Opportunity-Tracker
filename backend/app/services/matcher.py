from .embedding_service import EmbeddingService
from typing import List, Dict
from ..core.database import SessionLocal, init_db
from ..models.job import Job
from ..models.match import Match
from ..models.resume import Resume
import numpy as np
import json
from datetime import datetime

# Ensure tables exist
init_db()

class Matcher:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.db = SessionLocal()

    def compute_skill_overlap(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Compute skill overlap as Jaccard similarity."""
        if not resume_skills and not job_skills:
            return 1.0
        intersection = len(set(resume_skills) & set(job_skills))
        union = len(set(resume_skills) | set(job_skills))
        return intersection / union if union > 0 else 0.0

    def recency_bonus(self, posted_date_iso: str) -> float:
        """Compute recency bonus between 0 and 1 for jobs posted within the last 5 days.

        Newer jobs get higher bonus; jobs older than 5 days get 0.
        Linear decay: 1.0 at 0 days, 0.0 at 5 days.
        """
        if not posted_date_iso:
            return 0.0
        try:
            posted = datetime.fromisoformat(posted_date_iso)
        except Exception:
            return 0.0
        days_old = (datetime.utcnow() - posted).days
        if days_old < 0:
            days_old = 0
        if days_old >= 5:
            return 0.0
        return max(0.0, 1 - (days_old / 5.0))

    def match_resume_with_jobs(self, resume: Resume, jobs: List[Job]) -> List[Dict]:
        """Match a resume with provided jobs and persist Match records.

        Scoring: 0.65 * semantic_similarity + 0.25 * skill_overlap + 0.1 * recency_bonus
        """
        # load resume embedding or generate
        if resume.embedding:
            resume_emb = np.array(json.loads(resume.embedding))
        else:
            resume_emb = self.embedding_service.generate_embedding(resume.text)
            resume.embedding = json.dumps(resume_emb.tolist())
            self.db.add(resume)
            self.db.commit()

        resume_skills = resume.skills_list()
        matches = []

        for job in jobs:
            # job.embedding may not exist - generate on the fly
            if job.embedding:
                job_emb = np.array(json.loads(job.embedding))
            else:
                job_emb = self.embedding_service.generate_embedding(job.description or "")
                job.embedding = json.dumps(job_emb.tolist())
                self.db.add(job)
                self.db.commit()

            semantic_sim = float(self.embedding_service.cosine_similarity(resume_emb, job_emb))

            # Attempt to extract skills from job description by simple keyword matching
            # This is a simple approach; a production system should use a proper skills extractor
            job_skills = []
            # naive split by non-alphanumeric
            tokens = set((job.description or "").lower().split())
            for sk in resume_skills:
                if sk.lower() in tokens:
                    job_skills.append(sk.lower())

            skill_overlap = float(self.compute_skill_overlap(resume_skills, job_skills))
            rec_bonus = float(self.recency_bonus(job.posted_date.isoformat() if job.posted_date else None))

            final_score = 0.65 * semantic_sim + 0.25 * skill_overlap + 0.1 * rec_bonus
            final_score_pct = round(final_score * 100, 0)

            # compute missing skills as difference (simple approximation)
            missing = [s for s in (set(job_skills) - set([s.lower() for s in resume_skills]))]

            # persist match
            match = Match(
                resume_id=resume.id,
                job_id=job.id,
                score=float(final_score_pct),
                semantic_similarity=float(semantic_sim),
                skill_overlap=float(skill_overlap),
                missing_skills=json.dumps(missing)
            )
            self.db.add(match)
            self.db.commit()

            matches.append({
                "title": job.title,
                "company": job.company,
                "score": int(final_score_pct),
                "missing_skills": missing,
                "apply_url": job.apply_url
            })

        # sort by score desc
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches

    def get_matches_for_resume(self, resume_id: int) -> List[Dict]:
        rows = self.db.query(Match).filter(Match.resume_id == resume_id).all()
        results = []
        for r in rows:
            # get job details
            job = self.db.query(Job).filter(Job.id == r.job_id).first()
            results.append({
                "title": job.title if job else None,
                "company": job.company if job else None,
                "score": int(round(r.score)),
                "missing_skills": r.missing_skills_list(),
                "apply_url": job.apply_url if job else None
            })
        # sort
        results.sort(key=lambda x: x["score"], reverse=True)
        return results