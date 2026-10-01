import re

from app.job_sources.base import JobSourceAdapter


class DemoJobSourceAdapter(JobSourceAdapter):
    source_name = "DEMO"

    def search_jobs(self, query: str, location: str | None = None, page: int = 1):
        jobs = [
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
            {
                "external_id": "demo-103",
                "title": "React Frontend Developer",
                "company": "Glassline Digital",
                "location": location or "Noida",
                "description": "Requirements: React, JavaScript, HTML, CSS, Tailwind, API integration, responsive UI, and Git workflow.",
                "salary": "INR 6-10 LPA",
                "experience_required": "1-3 years",
                "employment_type": "Full-time",
                "url": "https://example.com/jobs/demo-103",
                "posted_at": "2026-09-26",
            },
            {
                "external_id": "demo-104",
                "title": "Data Analyst",
                "company": "Times Analytics",
                "location": location or "Mumbai",
                "description": "Requirements: SQL, Excel, Power BI, dashboards, reporting, data cleaning, stakeholder communication, and basic Python.",
                "salary": "INR 5-9 LPA",
                "experience_required": "0-2 years",
                "employment_type": "Full-time",
                "url": "https://example.com/jobs/demo-104",
                "posted_at": "2026-09-25",
            },
            {
                "external_id": "demo-105",
                "title": "Java Spring Boot Developer",
                "company": "Shine Systems",
                "location": location or "Hyderabad",
                "description": "Requirements: Java, Spring Boot, REST API, MySQL, Git, unit testing, debugging, and production support.",
                "salary": "INR 8-14 LPA",
                "experience_required": "2-4 years",
                "employment_type": "Full-time",
                "url": "https://example.com/jobs/demo-105",
                "posted_at": "2026-09-24",
            },
            {
                "external_id": "demo-106",
                "title": "Machine Learning Intern",
                "company": "Foundit AI Labs",
                "location": location or "Remote",
                "description": "Requirements: Python, NumPy, Pandas, Scikit-learn, Jupyter, machine learning basics, model evaluation, and Git.",
                "salary": "INR 20-35K stipend",
                "experience_required": "Fresher",
                "employment_type": "Internship",
                "url": "https://example.com/jobs/demo-106",
                "posted_at": "2026-09-23",
            },
            {
                "external_id": "demo-107",
                "title": "Web Development Intern",
                "company": "Internshala Partner Studio",
                "location": location or "Remote",
                "description": "Requirements: HTML, CSS, JavaScript, React basics, Git, responsive pages, forms, and willingness to learn.",
                "salary": "INR 12-20K stipend",
                "experience_required": "Fresher",
                "employment_type": "Internship",
                "url": "https://example.com/jobs/demo-107",
                "posted_at": "2026-09-22",
            },
        ]
        return [job for job in jobs if self._matches_query(job, query)]

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

    def _matches_query(self, job: dict, query: str | None) -> bool:
        tokens = self._query_tokens(query)
        if not tokens:
            return True

        generic_terms = {
            "job", "jobs", "role", "opening", "openings", "hiring", "developer",
            "engineer", "intern", "fresher", "full", "time",
        }
        specific_tokens = [token for token in tokens if token not in generic_terms]
        role_tokens = [token for token in tokens if token in generic_terms]
        title = str(job.get("title", "")).lower()
        haystack = " ".join(
            str(job.get(key, ""))
            for key in ["title", "company", "description", "employment_type", "experience_required"]
        ).lower()

        if specific_tokens:
            has_specific_match = any(self._contains_token(haystack, token) for token in specific_tokens)
            if not has_specific_match:
                return False
            if role_tokens:
                return any(self._matches_role(title, token) for token in role_tokens)
            return True
        return any(self._matches_role(title, token) or self._contains_token(haystack, token) for token in tokens)

    def _query_tokens(self, query: str | None) -> list[str]:
        return [
            token
            for token in re.findall(r"[a-z0-9+#.]+", (query or "").lower())
            if len(token) > 1
        ]

    def _contains_token(self, text: str, token: str) -> bool:
        pattern = r"(?<![a-z0-9])" + re.escape(token) + r"(?![a-z0-9])"
        return bool(re.search(pattern, text))

    def _matches_role(self, title: str, token: str) -> bool:
        equivalents = {
            "developer": ["developer", "engineer", "full stack", "frontend", "backend", "web"],
            "engineer": ["engineer", "developer", "full stack", "frontend", "backend"],
            "intern": ["intern", "internship"],
            "fresher": ["fresher", "entry-level", "entry level", "intern"],
        }
        terms = equivalents.get(token, [token])
        return any(term in title for term in terms)


demo_job_source = DemoJobSourceAdapter()
