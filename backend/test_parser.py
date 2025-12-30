from app.services.resume_parser import ResumeParser

# Test the resume parser
parser = ResumeParser()

# Sample resume text
resume_text = """
John Doe
Python Developer

Experience:
- 3 years as Python developer at Tech Corp
- Worked with FastAPI, SQL databases, and machine learning

Skills:
- Python
- FastAPI
- SQL
- Machine Learning
- JavaScript
"""

# Test individual methods
skills = parser.extract_skills(resume_text)
experience = parser.extract_experience_years(resume_text)
seniority = parser.infer_seniority(experience)

print("Parsed Resume:")
print(f"Text: {resume_text[:100]}...")
print(f"Skills: {skills}")
print(f"Experience Years: {experience}")
print(f"Seniority: {seniority}")