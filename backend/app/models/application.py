from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    resume_version_id = Column(Integer, ForeignKey("resume_versions.id"), nullable=True)
    status = Column(String(80), default="DISCOVERED", nullable=False)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    response_status = Column(String(80), nullable=True)
    notes = Column(Text, nullable=True)
    automation_status = Column(String(80), default="PENDING", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")
    job = relationship("Job")
