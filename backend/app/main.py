from fastapi import FastAPI
from .api import resume, match

app = FastAPI(title="AI-Powered Job Matching System", version="1.0.0")

app.include_router(resume.router, prefix="/api", tags=["resume"])
app.include_router(match.router, prefix="/api", tags=["match"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Job Matching API"}