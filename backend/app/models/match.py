from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base
import json

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), index=True)
    score = Column(Float)
    semantic_similarity = Column(Float)
    skill_overlap = Column(Float)
    missing_skills = Column(Text)  # JSON list
    created_at = Column(DateTime, server_default=func.now())

    def missing_skills_list(self):
        try:
            return json.loads(self.missing_skills)
        except Exception:
            return []

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "score": self.score,
            "semantic_similarity": self.semantic_similarity,
            "skill_overlap": self.skill_overlap,
            "missing_skills": self.missing_skills_list(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
