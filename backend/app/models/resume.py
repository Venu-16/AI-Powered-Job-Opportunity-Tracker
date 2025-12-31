from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..core.database import Base
import json

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    skills = Column(Text)  # JSON list
    embedding = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def skills_list(self):
        try:
            return json.loads(self.skills)
        except Exception:
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "skills": self.skills_list(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
