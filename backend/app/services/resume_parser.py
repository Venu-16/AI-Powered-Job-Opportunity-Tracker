import pdfplumber
from docx import Document
import re
import spacy
from typing import Dict, List

nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """Extract raw text from PDF, DOCX or TXT file."""
        if file_type == "pdf":
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        elif file_type == "docx":
            doc = Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        elif file_type == "txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            raise ValueError("Unsupported file type")

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Extract skills using keyword matching and spaCy NER."""
        # Simple keyword list (expand as needed)
        skill_keywords = [
            "python", "java", "javascript", "sql", "machine learning", "data analysis",
            "fastapi", "django", "react", "aws", "docker", "git"
        ]
        skills = []
        doc = nlp(text.lower())
        for token in doc:
            if token.text in skill_keywords:
                skills.append(token.text)
        # Remove duplicates
        return list(set(skills))

    @staticmethod
    def extract_experience_years(text: str) -> int:
        """Extract years of experience using regex."""
        # Patterns like "X years", "X+ years"
        patterns = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'experience\s*of\s*(\d+)\s*years?',
            r'(\d+)\s*years?\s*in\s*',
        ]
        max_years = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                years = int(match)
                if years > max_years:
                    max_years = years
        return max_years

    @staticmethod
    def infer_seniority(years: int) -> str:
        """Infer seniority level based on years of experience."""
        if years < 2:
            return "Junior"
        elif years <= 5:
            return "Mid"
        else:
            return "Senior"

    def parse_resume(self, file_path: str, file_type: str) -> Dict:
        """Parse the resume and return extracted data."""
        text = self.extract_text(file_path, file_type)
        skills = self.extract_skills(text)
        years = self.extract_experience_years(text)
        seniority = self.infer_seniority(years)
        return {
            "text": text,
            "skills": skills,
            "experience_years": years,
            "seniority": seniority
        }