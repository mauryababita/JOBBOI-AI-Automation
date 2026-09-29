from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.models.followup import FollowUp
from app.models.user import User

router = APIRouter(prefix="/followups", tags=["followups"])


@router.post("")
def create_followup(payload: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    follow_up = FollowUp(
        application_id=payload.get("application_id"),
        reminder_date=payload.get("reminder_date"),
        status="PENDING",
        notes=payload.get("notes"),
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)
    return {"success": True, "data": {"followup": follow_up}, "message": "Follow-up created"}


@router.get("")
def list_followups(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    followups = db.query(FollowUp).all()
    return {"success": True, "data": {"followups": followups}, "message": "Follow-ups retrieved"}
