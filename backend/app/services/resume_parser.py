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
        skills = self._extract_skill_keywords(text)
        technical_skills = self._extract_skill_keywords(text, technical_only=True)
        candidate = {
            "raw_text": text,
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "location": self._extract_location(text),
            "summary": self._extract_summary(raw_text),
            "skills": skills,
            "technical_skills": technical_skills,
            "soft_skills": ["Communication", "Teamwork", "Leadership"],
            "education": self._extract_education(raw_text),
            "experience": self._extract_descriptive_section(raw_text, ["experience", "work experience", "professional experience", "employment"]),
            "projects": self._extract_descriptive_section(raw_text, ["projects", "academic projects", "personal projects"]),
            "certifications": self._extract_text_items(raw_text, [
                "certification", "certifications", "certificate", "certificates",
                "license", "licenses", "courses", "coursework", "training",
                "professional training",
            ]),
            "achievements": self._extract_text_items(raw_text, [
                "achievement", "achievements", "award", "awards", "honors",
                "accomplishment", "accomplishments",
            ]),
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
        for term in [
            "Bengaluru", "Bangalore", "Delhi", "Mumbai", "Hyderabad", "Pune",
            "Chennai", "Noida", "Gurugram", "Gurgaon", "Kolkata", "Ahmedabad",
            "Remote", "India",
        ]:
            if term.lower() in text.lower():
                return term
        return None

    def _extract_summary(self, text: str) -> str | None:
        summary = self._extract_section_text(text, ["summary", "professional summary", "profile", "objective"])
        if summary:
            return self.clean_text(summary)[:350]
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", self.clean_text(text)) if s.strip()]
        return sentences[0][:250] if sentences else None

    def _extract_skill_keywords(self, text: str, technical_only: bool = False) -> list[str]:
        skills = [
            "Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "React", "JavaScript",
            "TypeScript", "Node.js", "Docker", "AWS", "Kubernetes", "Redis",
            "Git", "REST API", "SQL", "Machine Learning", "AI", "LLM",
            "Playwright", "CSS", "HTML", "Tailwind", "Django", "Flask",
            "Java", "C++", "C#", "PHP", "Laravel", "Spring Boot", "MongoDB",
            "MySQL", "SQLite", "GraphQL", "Next.js", "Vue", "Angular",
            "TensorFlow", "PyTorch", "Pandas", "NumPy", "Power BI", "Tableau",
            "Excel", "Jupyter", "Scikit-learn", "NLP", "Computer Vision",
            "Azure", "GCP", "CI/CD", "Linux", "Figma",
        ]
        lowered = text.lower()
        matches = []
        for skill in skills:
            if skill.lower() in lowered:
                matches.append(skill)
        if technical_only:
            return matches
        return sorted(set(matches))

    def _extract_education(self, text: str) -> list[dict]:
        items = self._extract_text_items(text, ["education", "academic background", "qualification", "qualifications"])
        return [{"details": item} for item in items]

    def _extract_descriptive_section(self, text: str, headings: list[str]) -> list[dict]:
        return [{"description": item} for item in self._extract_text_items(text, headings)]

    def _extract_text_items(self, text: str, headings: list[str]) -> list[str]:
        section = self._extract_section_text(text, headings)
        if not section:
            return []

        lines = []
        for line in section.splitlines():
            clean = re.sub(r"^[\s\-*\u2022\u25cf\u25aa\u2013\u2014]+", "", line).strip()
            if clean:
                lines.append(clean)

        if not lines:
            lines = [part.strip() for part in re.split(r"(?<=[.!?])\s+", self.clean_text(section)) if part.strip()]

        return [line[:350] for line in lines[:8] if len(line) > 2]

    def _extract_section_text(self, text: str, headings: list[str]) -> str | None:
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        heading_patterns = {
            "summary", "professional summary", "profile", "objective", "skills",
            "technical skills", "education", "academic background", "qualification",
            "qualifications", "experience", "work experience", "professional experience",
            "employment", "projects", "academic projects", "personal projects",
            "certification", "certifications", "certificate", "certificates",
            "license", "licenses", "courses", "coursework", "training",
            "professional training", "achievement", "achievements", "award",
            "awards", "honors", "accomplishment", "accomplishments",
        }
        normalized_targets = {heading.lower() for heading in headings}
        start_index = None
        inline_content = None

        for index, line in enumerate(lines):
            heading_part, content_part = self._split_inline_heading(line)
            normalized = self._normalize_heading(heading_part)
            if self._heading_matches(normalized, normalized_targets):
                start_index = index + 1
                inline_content = content_part
                break

        if start_index is None:
            return None

        collected = []
        if inline_content:
            collected.append(inline_content)
        for line in lines[start_index:]:
            heading_part, _ = self._split_inline_heading(line)
            normalized = self._normalize_heading(heading_part)
            if self._heading_matches(normalized, heading_patterns):
                break
            collected.append(line)

        section_text = "\n".join(collected).strip()
        return section_text or None

    def _normalize_heading(self, line: str) -> str:
        normalized = re.sub(r"[^A-Za-z\s/&]", "", line).replace("&", "and").strip().lower()
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def _split_inline_heading(self, line: str) -> tuple[str, str | None]:
        match = re.match(r"^\s*([^:\-|]{2,60})\s*[:\-|]\s*(.+)$", line)
        if not match:
            return line, None
        return match.group(1), match.group(2).strip() or None

    def _heading_matches(self, normalized: str, targets: set[str]) -> bool:
        if normalized in targets:
            return True
        return any(
            normalized.startswith(f"{target} ")
            or normalized.endswith(f" {target}")
            for target in targets
        )


resume_parser_service = ResumeParserService()
