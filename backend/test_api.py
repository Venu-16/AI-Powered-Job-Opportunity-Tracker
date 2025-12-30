from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test data
resume_data = {
    "text": "I am a Python developer with 3 years of experience in web development using FastAPI, SQL, and machine learning.",
    "skills": ["python", "fastapi", "sql", "machine learning"],
    "experience_years": 3,
    "seniority": "Mid"
}

# Make the request
response = client.post("/api/run", json=resume_data)

print("Status Code:", response.status_code)
print("Response:", response.json())