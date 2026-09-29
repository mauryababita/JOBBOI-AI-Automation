class CoverLetterService:
    def generate(self, candidate_profile: dict, job: object, match: dict) -> str:
        candidate_name = candidate_profile.get("name") or "Candidate"
        matched_skills = match.get("matched_skills", [])
        missing_skills = match.get("missing_skills", [])
        skills_sentence = ""
        if matched_skills:
            skills_sentence = f"My background includes {', '.join(matched_skills[:6])}, which aligns with the role's core requirements. "

        experience_sentence = self._experience_sentence(candidate_profile)
        gap_sentence = ""
        if missing_skills:
            gap_sentence = f"I also noticed growth areas around {', '.join(missing_skills[:3])}, and I am prepared to close those gaps quickly through focused project work. "

        return (
            f"Dear Hiring Manager,\n\n"
            f"I am excited to apply for the {job.title} role at {job.company}. "
            f"{skills_sentence}{experience_sentence}{gap_sentence}"
            f"I would welcome the opportunity to discuss how my profile can contribute to your team.\n\n"
            f"Sincerely,\n"
            f"{candidate_name}"
        )

    def _experience_sentence(self, candidate_profile: dict) -> str:
        experience = candidate_profile.get("experience") or []
        if not experience:
            return ""
        latest = experience[0]
        if not isinstance(latest, dict):
            return ""
        title = latest.get("job_title")
        company = latest.get("company")
        if title and company:
            return f"My experience as {title} at {company} gives me practical context for this position. "
        if title:
            return f"My experience as {title} gives me practical context for this position. "
        return ""


cover_letter_service = CoverLetterService()
