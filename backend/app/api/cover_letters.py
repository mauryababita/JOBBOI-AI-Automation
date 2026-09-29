from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.models.cover_letter import CoverLetter
from app.models.user import User

router = APIRouter(prefix="/cover-letters", tags=["cover-letters"])


@router.get("")
def list_cover_letters(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    letters = db.query(CoverLetter).filter(CoverLetter.user_id == user.id).order_by(CoverLetter.created_at.desc()).all()
    return {
        "success": True,
        "data": {
            "cover_letters": [
                {
                    "id": letter.id,
                    "job_id": letter.job_id,
                    "content": letter.content,
                    "created_at": letter.created_at.isoformat() if letter.created_at else None,
                }
                for letter in letters
            ]
        },
        "message": "Cover letters retrieved",
    }
