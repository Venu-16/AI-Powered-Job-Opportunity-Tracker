from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import match
from .api import jobs
from .core.database import init_db

app = FastAPI(title="AI-Powered Job Matching System", version="1.0.0")

# Simple CORS for local frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure DB tables are created
init_db()

app.include_router(match.router, prefix="/api", tags=["match"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])
from .api import resume
app.include_router(resume.router, prefix="/api", tags=["resume"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Job Matching API"}