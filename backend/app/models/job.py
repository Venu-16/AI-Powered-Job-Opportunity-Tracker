from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..core.database import Base
import json

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    description = Column(Text)
    posted_date = Column(DateTime)
    apply_url = Column(String)
    embedding = Column(Text, nullable=True)  # store as JSON list
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "apply_url": self.apply_url,
        }
