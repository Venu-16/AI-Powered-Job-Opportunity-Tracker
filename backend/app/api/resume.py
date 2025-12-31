from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.resume_parser import ResumeParser
from ..core.database import SessionLocal
from ..models.resume import Resume
import json
from ..services.embedding_service import EmbeddingService

router = APIRouter()

@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a resume (pdf or docx), parse it, store it and return the resume id."""
    filename = file.filename.lower()
    if filename.endswith(".pdf"):
        ftype = "pdf"
    elif filename.endswith(".docx"):
        ftype = "docx"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    # write temporarily
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as f:
        f.write(content)

    parser = ResumeParser()
    parsed = parser.parse_resume(tmp_path, ftype)

    # store in DB
    db = SessionLocal()
    emb_service = EmbeddingService()
    emb = emb_service.generate_embedding(parsed["text"]).tolist()

    resume = Resume(text=parsed["text"], skills=json.dumps(parsed["skills"]), embedding=json.dumps(emb))
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"resume_id": resume.id}
