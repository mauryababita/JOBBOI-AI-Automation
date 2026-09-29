from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.models.resume import Resume
from app.models.user import User
from app.services.ats_engine import ats_score_service

router = APIRouter(prefix="/ats", tags=["ats"])


@router.post("/analyze/{resume_id}")
def analyze_resume(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    result = ats_score_service.analyze(resume.parsed_data or {})
    resume.ats_score = result["score"]
    db.commit()
    return {"success": True, "data": result, "message": "ATS analysis complete"}
