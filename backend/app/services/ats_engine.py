from __future__ import annotations

import re


class ATSScoreService:
    def analyze(self, resume_data: dict) -> dict:
        category_max = {
            "Contact Information": 10,
            "Resume Sections": 10,
            "Keyword Coverage": 25,
            "Action Verbs": 10,
            "Quantified Achievements": 15,
            "Formatting": 10,
            "Experience Relevance": 10,
            "Resume Length": 5,
            "Skills Clarity": 5,
        }

        recommendations = []
        strengths = []
        issues = []
        text = self._flatten(resume_data)
        words = re.findall(r"\w+", text.lower())
        word_count = len(words)

        contact_score = 0
        if resume_data.get("email"):
            contact_score += 4
        else:
            issues.append("Missing email address")
            recommendations.append("Add a professional email address in the header.")
        if resume_data.get("phone"):
            contact_score += 3
        else:
            issues.append("Missing phone number")
        if resume_data.get("location"):
            contact_score += 3

        sections_present = sum(1 for key in ["summary", "skills", "education", "experience", "projects", "certifications"] if resume_data.get(key))
        sections_score = min(10, round(sections_present / 6 * 10))
        if sections_score < 7:
            issues.append("Important resume sections are missing or thin")
            recommendations.append("Add clear sections for summary, skills, education, experience, projects, and certifications where applicable.")

        skills = set(str(skill).lower() for skill in resume_data.get("skills", []))
        technical_skills = set(str(skill).lower() for skill in resume_data.get("technical_skills", []))
        skill_count = len(skills | technical_skills)
        keyword_score = min(25, skill_count * 3)
        if skill_count == 0:
            issues.append("Skills section is weak or missing")
            recommendations.append("Add a dedicated skills section with technical and soft skills.")
        else:
            strengths.append("Skills section is present and relevant")

        action_verbs = {
            "built", "created", "developed", "designed", "implemented", "improved",
            "optimized", "automated", "led", "managed", "delivered", "reduced",
            "increased", "launched", "integrated", "analyzed",
        }
        action_hits = sum(1 for word in words if word in action_verbs)
        action_score = min(10, action_hits * 2)
        if action_score < 6:
            issues.append("Few strong action verbs found")
            recommendations.append("Start bullets with verbs such as built, improved, automated, led, delivered, or optimized.")

        quantified_hits = len(re.findall(r"(\d+%|\d+\+?|\$|₹|rs\.?|lpa|million|k\b)", text.lower()))
        achievement_score = min(15, quantified_hits * 3)
        if achievement_score < 6:
            issues.append("Achievements are not quantified enough")
            recommendations.append("Add measurable outcomes such as percentage improvements, scale, revenue, users, latency, or cost savings.")

        formatting_score = 10
        if word_count < 120:
            formatting_score -= 2
        if len(text) > 12000:
            formatting_score -= 2
        if "\t" in text:
            formatting_score -= 1

        experience_entries = resume_data.get("experience") or []
        experience_score = min(10, len(experience_entries) * 4)
        if not experience_entries:
            issues.append("Experience details are sparse")
            recommendations.append("Add detailed role descriptions with measurable outcomes.")

        if not resume_data.get("summary"):
            issues.append("Professional summary is missing")
            recommendations.append("Include a concise summary tailored to target job roles.")
        else:
            strengths.append("Professional summary is included")

        length_score = 5
        if word_count < 150:
            length_score = 2
            issues.append("Resume appears short")
        elif word_count > 1200:
            length_score = 3
            issues.append("Resume may be too long")

        skills_clarity_score = 5 if skill_count >= 6 else max(1, skill_count)

        if resume_data.get("certifications"):
            strengths.append("Relevant certifications are present")

        categories_result = {
            "Contact Information": contact_score,
            "Resume Sections": sections_score,
            "Keyword Coverage": keyword_score,
            "Action Verbs": action_score,
            "Quantified Achievements": achievement_score,
            "Formatting": max(0, formatting_score),
            "Experience Relevance": experience_score,
            "Resume Length": length_score,
            "Skills Clarity": skills_clarity_score,
        }
        score = min(100, sum(categories_result.values()))

        if score >= 75:
            strengths.append("Resume has a strong ATS-style foundation")

        category_details = {
            name: {"score": value, "max": category_max[name]}
            for name, value in categories_result.items()
        }

        return {
            "score": score,
            "categories": category_details,
            "strengths": strengths,
            "issues": issues,
            "recommendations": recommendations,
        }

    def _flatten(self, value) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return " ".join(self._flatten(item) for item in value)
        if isinstance(value, dict):
            return " ".join(self._flatten(item) for item in value.values())
        return str(value)


ats_score_service = ATSScoreService()
