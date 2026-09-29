from app.job_sources.base import JobSourceAdapter


class DemoJobSourceAdapter(JobSourceAdapter):
    source_name = "DEMO"

    def search_jobs(self, query: str, location: str | None = None, page: int = 1):
        return [
            {
                "external_id": "demo-100",
                "title": "Fresher Python Developer",
                "company": "StarterStack",
                "location": location or "Pune",
                "description": "Entry-level role for freshers with Python, SQL, HTML, CSS, Git, and REST API fundamentals.",
                "salary": "INR 4-7 LPA",
                "experience_required": "0-1 years",
                "employment_type": "Full-time",
                "url": "https://example.com/jobs/demo-100",
                "posted_at": "2026-09-29",
            },
            {
                "external_id": "demo-101",
                "title": "Python Backend Engineer",
                "company": "Northstar Labs",
                "location": location or "Bengaluru",
                "description": "Build APIs with Python, FastAPI, PostgreSQL, Docker, AWS, and cloud deployment automation.",
                "salary": "INR 18-28 LPA",
                "experience_required": "2-4 years",
                "employment_type": "Full-time",
                "url": "https://example.com/jobs/demo-101",
                "posted_at": "2026-09-28",
            },
            {
                "external_id": "demo-102",
                "title": "Full Stack Engineer",
                "company": "Orbit Foundry",
                "location": "Remote",
                "description": "Work across React, TypeScript, Python, SQL, Redis, and REST APIs in a modern product team.",
                "salary": "INR 20-30 LPA",
                "experience_required": "3-5 years",
                "employment_type": "Remote",
                "url": "https://example.com/jobs/demo-102",
                "posted_at": "2026-09-27",
            },
        ]

    def get_job_details(self, job_id: str):
        return {"external_id": job_id, "title": "Python Backend Engineer", "company": "Northstar Labs"}

    def normalize_job(self, raw_job: dict):
        return {
            "source": self.source_name,
            "external_id": raw_job.get("external_id", "demo-unknown"),
            "title": raw_job.get("title", "").strip(),
            "company": raw_job.get("company", "").strip(),
            "location": raw_job.get("location", "").strip(),
            "description": raw_job.get("description", "").strip(),
            "salary": raw_job.get("salary", ""),
            "experience_required": raw_job.get("experience_required", ""),
            "employment_type": raw_job.get("employment_type", ""),
            "url": raw_job.get("url", ""),
            "posted_at": raw_job.get("posted_at", ""),
        }

    def supports_application(self, job: dict) -> bool:
        return False

    def start_application(self, job: dict):
        return {"status": "NEEDS_USER_ACTION", "reason": "Demo adapter does not submit applications"}

    def fill_application(self, job: dict, user_profile: dict):
        return {"status": "READY_TO_REVIEW", "fields": []}

    def submit_application(self, job: dict):
        return {"status": "NEEDS_USER_ACTION", "reason": "Manual review required"}


demo_job_source = DemoJobSourceAdapter()
