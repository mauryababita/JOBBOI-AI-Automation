from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(80), nullable=False, index=True)
    external_id = Column(String(200), nullable=True, index=True)
    title = Column(String(250), nullable=False)
    company = Column(String(250), nullable=False)
    location = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    salary = Column(String(120), nullable=True)
    employment_type = Column(String(80), nullable=True)
    experience_required = Column(String(120), nullable=True)
    url = Column(String(500), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
