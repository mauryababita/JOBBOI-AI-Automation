import json
import re
from pathlib import Path

from pydantic import ValidationError

from app.ai.prompts import RESUME_EXTRACTION_PROMPT
from app.schemas.resume import ResumeExtraction


class ResumeParserService:
    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            import fitz

            text_chunks = []
            with fitz.open(file_path) as document:
                for page in document:
                    text_chunks.append(page.get_text("text"))
            return "\n".join(text_chunks)
        except ImportError:
            from pypdf import PdfReader

            reader = PdfReader(file_path)
            text_chunks = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)
            return "\n".join(text_chunks)

    def clean_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def build_structured_resume(self, raw_text: str) -> dict:
        text = self.clean_text(raw_text)
        candidate = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "location": self._extract_location(text),
            "summary": self._extract_summary(text),
            "skills": self._extract_skill_keywords(text),
            "technical_skills": self._extract_skill_keywords(text, technical_only=True),
            "soft_skills": ["Communication", "Teamwork", "Leadership"],
            "education": [{"degree": "", "institution": "", "start_date": "", "end_date": "", "field": ""}],
            "experience": [],
            "projects": [],
            "certifications": [],
            "achievements": [],
        }

        try:
            ResumeExtraction.model_validate(candidate)
        except ValidationError:
            pass
        return candidate

    def _extract_name(self, text: str) -> str | None:
        match = re.search(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", text)
        return match.group(0) if match else None

    def _extract_email(self, text: str) -> str | None:
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> str | None:
        match = re.search(r"(?:\+?\d[\d\s\-()]{7,}\d)", text)
        return match.group(0).strip() if match else None

    def _extract_location(self, text: str) -> str | None:
        for term in ["Bengaluru", "Delhi", "Mumbai", "Hyderabad", "Pune", "Chennai", "Remote", "India"]:
            if term.lower() in text.lower():
                return term
        return None

    def _extract_summary(self, text: str) -> str | None:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        return sentences[0][:250] if sentences else None

    def _extract_skill_keywords(self, text: str, technical_only: bool = False) -> list[str]:
        skills = [
            "Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "React", "JavaScript",
            "TypeScript", "Node.js", "Docker", "AWS", "Kubernetes", "Redis",
            "Git", "REST API", "SQL", "Machine Learning", "AI", "LLM",
            "Playwright", "CSS", "HTML", "Tailwind", "Django", "Flask"
        ]
        lowered = text.lower()
        matches = []
        for skill in skills:
            if skill.lower() in lowered:
                matches.append(skill)
        if technical_only:
            return matches
        return sorted(set(matches))


resume_parser_service = ResumeParserService()
