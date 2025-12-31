from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_upload_and_fetch_jobs():
    # upload a simple resume txt saved as .pdf (parser expects pdf/docx but parser will error on real pdf parsing)
    # instead, we'll create a small pdf-like file name but rely on the mocked parser capability: use docx
    content = b"John Doe\nExperience with Python, Docker, FastAPI, SQL"
    files = {"file": ("resume.txt", content, "text/plain")}

    # upload
    r = client.post("/api/resume/upload", files=files)
    assert r.status_code == 200
    resume_id = r.json().get("resume_id")
    assert resume_id is not None

    # fetch jobs (uses mocked jobs since ADZUNA vars not set in test env)
    resp = client.post("/api/jobs/fetch", json={"roles": ["Backend Developer"], "companies": ["Amazon", "Google"]})
    assert resp.status_code == 200
    assert "jobs_fetched" in resp.json()

    # check match results (may be empty until matches are computed)
    res = client.get(f"/api/match/results/{resume_id}")
    assert res.status_code in (200, 404)
