from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.models.application import Application
from app.models.user import User

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("")
def create_application(payload: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    application = Application(
        user_id=user.id,
        job_id=payload.get("job_id"),
        resume_version_id=payload.get("resume_version_id"),
        status="DISCOVERED",
        notes=payload.get("notes"),
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return {"success": True, "data": {"application": application}, "message": "Application created"}


@router.get("")
def list_applications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    applications = db.query(Application).filter(Application.user_id == user.id).all()
    return {"success": True, "data": {"applications": applications}, "message": "Applications listed"}


@router.get("/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == application_id, Application.user_id == user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "data": {"application": application}, "message": "Application found"}


@router.post("/{application_id}/start")
def start_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == application_id, Application.user_id == user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = "APPLICATION_STARTED"
    application.automation_status = "NEEDS_USER_ACTION"
    db.commit()
    return {
        "success": True,
        "data": {
            "application": application,
            "automation": {"status": "NEEDS_USER_ACTION", "reason": "Demo adapter pauses before real website submission"},
        },
        "message": "Application started",
    }


@router.post("/{application_id}/review")
def review_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == application_id, Application.user_id == user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = "READY_TO_APPLY"
    db.commit()
    return {"success": True, "data": {"application": application}, "message": "Application reviewed"}


@router.post("/{application_id}/submit")
def submit_application(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == application_id, Application.user_id == user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.status != "READY_TO_APPLY":
        raise HTTPException(status_code=400, detail="Review application before submission")
    application.status = "SUBMITTED"
    application.automation_status = "SUBMITTED"
    db.commit()
    return {"success": True, "data": {"application": application}, "message": "Application submitted"}
