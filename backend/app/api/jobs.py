from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.database import get_db
from app.job_sources.demo import demo_job_source
from app.models.cover_letter import CoverLetter
from app.models.job import Job
from app.models.resume import Resume
from app.models.saved_job import SavedJob
from app.models.user import User
from app.services.cover_letter import cover_letter_service
from app.services.job_matcher import job_matcher_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


def serialize_job(job: Job, match: dict | None = None) -> dict:
    data = {
        "id": job.id,
        "source": job.source,
        "external_id": job.external_id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "salary": job.salary,
        "employment_type": job.employment_type,
        "experience_required": job.experience_required,
        "url": job.url,
        "posted_at": job.posted_at.isoformat() if job.posted_at else None,
    }
    if match:
        data.update(match)
    return data


def latest_resume(db: Session, user_id: int) -> Resume | None:
    return db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).first()


def parse_posted_at(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


@router.post("/search")
def search_jobs(query: str, location: str | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    jobs = demo_job_source.search_jobs(query=query or "python developer", location=location)
    normalized = [demo_job_source.normalize_job(job) for job in jobs]
    persisted = []
    resume = latest_resume(db, user.id)
    candidate_profile = resume.parsed_data if resume and resume.parsed_data else {}
    for item in normalized:
        item["posted_at"] = parse_posted_at(item.get("posted_at"))
        existing = db.query(Job).filter(Job.source == item["source"], Job.external_id == item["external_id"]).first()
        if not existing:
            db_job = Job(**item)
            db.add(db_job)
            db.commit()
            db.refresh(db_job)
            persisted.append(db_job)
        else:
            persisted.append(existing)

    response_jobs = []
    for job in persisted:
        match = job_matcher_service.analyze_match(candidate_profile, job.description or "") if candidate_profile else None
        response_jobs.append(serialize_job(job, match))
    return {"success": True, "data": {"jobs": response_jobs}, "message": "Jobs retrieved"}


@router.get("")
def list_jobs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    jobs = db.query(Job).all()
    return {"success": True, "data": {"jobs": [serialize_job(job) for job in jobs]}, "message": "Jobs listed"}


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"success": True, "data": {"job": serialize_job(job)}, "message": "Job found"}


@router.post("/analyze-description")
def analyze_description(payload: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job_description = payload.get("job_description") or ""
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")
    resume = latest_resume(db, user.id)
    candidate_profile = payload.get("candidate_profile") or (resume.parsed_data if resume and resume.parsed_data else {})
    analysis = job_matcher_service.analyze_job_description(job_description, candidate_profile)
    match = job_matcher_service.analyze_match(candidate_profile, job_description)
    return {"success": True, "data": {"analysis": analysis, "match": match}, "message": "Job description analyzed"}


@router.post("/{job_id}/match")
def match_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    resume = latest_resume(db, user.id)
    candidate_profile = resume.parsed_data if resume and resume.parsed_data else {}
    result = job_matcher_service.analyze_match(candidate_profile, job.description or "")
    return {"success": True, "data": result, "message": "Match analysis complete"}


@router.post("/{job_id}/cover-letter")
def generate_cover_letter(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    resume = latest_resume(db, user.id)
    candidate_profile = resume.parsed_data if resume and resume.parsed_data else {"name": user.name}
    match = job_matcher_service.analyze_match(candidate_profile, job.description or "")
    content = cover_letter_service.generate(candidate_profile, job, match)
    cover_letter = CoverLetter(user_id=user.id, job_id=job.id, content=content)
    db.add(cover_letter)
    db.commit()
    db.refresh(cover_letter)
    return {"success": True, "data": {"id": cover_letter.id, "content": content}, "message": "Cover letter generated"}


@router.post("/{job_id}/save")
def save_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing = db.query(SavedJob).filter(SavedJob.user_id == user.id, SavedJob.job_id == job_id).first()
    if existing:
        return {"success": True, "data": {"saved": True}, "message": "Job already saved"}
    saved = SavedJob(user_id=user.id, job_id=job_id)
    db.add(saved)
    db.commit()
    return {"success": True, "data": {"saved": True}, "message": "Job saved"}


@router.delete("/{job_id}/save")
def remove_saved_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    saved = db.query(SavedJob).filter(SavedJob.user_id == user.id, SavedJob.job_id == job_id).first()
    if saved:
        db.delete(saved)
        db.commit()
    return {"success": True, "data": {"saved": False}, "message": "Job removed from saved list"}
