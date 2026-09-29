from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    reminder_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(80), default="PENDING", nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
