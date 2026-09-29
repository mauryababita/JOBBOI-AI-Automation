from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.saved_job import SavedJob
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
def get_analytics(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    total_jobs_found = db.query(Job).count()
    applications = db.query(Application).filter(Application.user_id == user.id).all()
    saved_jobs = db.query(SavedJob).filter(SavedJob.user_id == user.id).count()
    interview_responses = sum(1 for item in applications if item.status == "INTERVIEW" or item.response_status == "INTERVIEW")

    by_status = {}
    by_platform = {}
    for application in applications:
        by_status[application.status] = by_status.get(application.status, 0) + 1
        if application.job:
            by_platform[application.job.source] = by_platform.get(application.job.source, 0) + 1

    return {
        "success": True,
        "data": {
            "total_jobs_found": total_jobs_found,
            "matched_jobs": total_jobs_found,
            "applications": len(applications),
            "interview_responses": interview_responses,
            "saved_jobs": saved_jobs,
            "average_match_score": 0,
            "applications_by_status": [{"name": key, "value": value} for key, value in by_status.items()],
            "applications_by_platform": [{"name": key, "value": value} for key, value in by_platform.items()],
            "response_rate": round((interview_responses / len(applications)) * 100, 1) if applications else 0,
        },
        "message": "Analytics retrieved",
    }
