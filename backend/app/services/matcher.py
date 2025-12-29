from .embedding_service import EmbeddingService
from typing import List, Dict
import numpy as np

class Matcher:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        # Dummy job descriptions
        self.jobs = [
            {
                "id": 1,
                "title": "Python Developer",
                "description": "We are looking for a Python developer with experience in FastAPI, SQL, and machine learning.",
                "skills": ["python", "fastapi", "sql", "machine learning"]
            },
            {
                "id": 2,
                "title": "Data Analyst",
                "description": "Seeking a data analyst skilled in Python, SQL, and data analysis techniques.",
                "skills": ["python", "sql", "data analysis"]
            },
            {
                "id": 3,
                "title": "Full Stack Developer",
                "description": "Need a full stack developer proficient in JavaScript, React, and backend technologies.",
                "skills": ["javascript", "react", "python", "sql"]
            }
        ]

    def compute_skill_overlap(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Compute skill overlap as Jaccard similarity."""
        if not resume_skills and not job_skills:
            return 1.0
        intersection = len(set(resume_skills) & set(job_skills))
        union = len(set(resume_skills) | set(job_skills))
        return intersection / union if union > 0 else 0.0

    def match_resume(self, resume_data: Dict) -> List[Dict]:
        """Match resume with jobs and return ranked list."""
        resume_embedding = self.embedding_service.generate_embedding(resume_data["text"])
        resume_skills = resume_data["skills"]
        matches = []

        for job in self.jobs:
            job_embedding = self.embedding_service.generate_embedding(job["description"])
            semantic_sim = self.embedding_service.cosine_similarity(resume_embedding, job_embedding)
            skill_overlap = self.compute_skill_overlap(resume_skills, job["skills"])
            final_score = 0.7 * semantic_sim + 0.3 * skill_overlap
            matches.append({
                "job_id": job["id"],
                "title": job["title"],
                "description": job["description"],
                "semantic_similarity": semantic_sim,
                "skill_overlap": skill_overlap,
                "final_score": final_score
            })

        # Rank by final_score descending
        matches.sort(key=lambda x: x["final_score"], reverse=True)
        return matches