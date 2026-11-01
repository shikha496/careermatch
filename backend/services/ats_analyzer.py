
import re

from services.skill_extractor import (
    extract_skills,
    extract_skill_evidence
)

from services.semantic_matcher import (
    find_similar_evidence
)


SECTION_ALIASES = {
    "contact": [
        "email", "phone", "linkedin"
    ],
    "summary": [
        "summary", "professional profile",
        "career objective", "about me"
    ],
    "experience": [
        "experience", "employment history",
        "work history", "professional experience"
    ],
    "education": [
        "education", "academic background"
    ],
    "skills": [
        "skills", "technical skills",
        "core competencies"
    ],
    "projects": [
        "projects", "personal projects",
        "academic projects"
    ]
}


def section_check(text):
    lower = text.lower()

    return {
        section: any(
            alias in lower
            for alias in aliases
        )
        for section, aliases in SECTION_ALIASES.items()
    }


def extract_years(text):
    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?",
        text.lower()
    )

    if not matches:
        return None

    return max(float(value) for value in matches)


def estimate_experience_score(resume, job_description):

    resume_years = extract_years(resume)
    required_years = extract_years(job_description)

    has_experience = any(
        section in resume.lower()
        for section in [
            "experience",
            "employment",
            "internship",
            "work history"
        ]
    )

    if not has_experience:
        return 0, "No identifiable experience section."

    if required_years is None:
        return 75, "Experience section detected; no explicit job tenure requirement."

    if resume_years is None:
        return 35, "Experience section detected, but tenure could not be verified."

    if resume_years >= required_years:
        return 100, "Stated experience meets the listed tenure requirement."

    return round(
        resume_years / required_years * 100
    ), "Stated experience is below the listed tenure requirement."


def estimate_education_score(resume, job_description):

    job = job_description.lower()
    cv = resume.lower()

    degree_terms = [
        "bachelor", "b.tech", "b.e.",
        "master", "m.tech", "mba",
        "phd", "doctorate", "degree"
    ]

    job_requires_degree = any(
        term in job for term in degree_terms
    )

    resume_has_degree = any(
        term in cv for term in degree_terms
    )

    if not job_requires_degree:
        return 75, "No explicit degree requirement detected."

    if resume_has_degree:
        return 100, "Degree-related wording found; verify actual qualification."

    return 0, "Required education could not be identified in the resume."


def structure_score(checks):
    important = [
        "summary",
        "experience",
        "education",
        "skills"
    ]

    passed = sum(
        bool(checks[key])
        for key in important
    )

    return round(passed / len(important) * 100)


def keyword_score(job_description, resume_text, skills):

    # Compare unique meaningful words, excluding very common words.
    stopwords = {
        "the", "and", "for", "with", "from",
        "this", "that", "you", "your", "our",
        "are", "was", "will", "have", "has",
        "who", "what", "when", "where", "how",
        "a", "an", "to", "of", "in", "on",
        "at", "is", "be", "as", "or", "by"
    }

    def terms(text):
        words = re.findall(
            r"[a-zA-Z][a-zA-Z0-9+#./-]{2,}",
            text.lower()
        )

        return {
            word for word in words
            if word not in stopwords
        }

    job_terms = terms(job_description)
    resume_terms = terms(resume_text)

    if not job_terms:
        return 0

    # Remove already evaluated canonical skill aliases.
    # The remaining term overlap is a separate, lower-weight signal.
    from services.skill_extractor import SKILL_ALIASES

    excluded = set()

    for canonical, aliases in SKILL_ALIASES.items():
        excluded.add(canonical.lower())
        excluded.update(alias.lower() for alias in aliases)

    job_terms -= excluded
    resume_terms -= excluded

    if not job_terms:
        return 75

    return round(
        len(job_terms & resume_terms) / len(job_terms) * 100
    )


def analyze_ats(resume_text, job_description):

    if not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not job_description.strip():
        raise ValueError("Job description is empty.")

    required_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    matched = [
        skill for skill in required_skills
        if skill in resume_skills
    ]

    missing = [
        skill for skill in required_skills
        if skill not in resume_skills
    ]

    evidence = extract_skill_evidence(
        resume_text,
        matched
    )

    possible_evidence = {}

    for skill in missing:
        candidates = find_similar_evidence(
            skill,
            resume_text,
            top_n=2
        )

        if candidates:
            possible_evidence[skill] = candidates

    if required_skills:
        skill_score = round(
            len(matched) / len(required_skills) * 100
        )
        skill_coverage = True
    else:
        skill_score = None
        skill_coverage = False

    experience, experience_note = estimate_experience_score(
        resume_text,
        job_description
    )

    education, education_note = estimate_education_score(
        resume_text,
        job_description
    )

    checks = section_check(resume_text)
    structure = structure_score(checks)

    keywords = keyword_score(
        job_description,
        resume_text,
        required_skills
    )

    # If the job description has no recognized skills,
    # do not invent a skill match score.
    weights = {
        "skills": 55,
        "experience": 20,
        "education": 10,
        "keywords": 10,
        "structure": 5
    }

    scores = {
        "skills": skill_score,
        "experience": experience,
        "education": education,
        "keywords": keywords,
        "structure": structure
    }

    if skill_coverage:
        final_score = round(
            sum(
                scores[key] * weights[key]
                for key in scores
            ) / 100
        )
        confidence = "Moderate"
        explanation = (
            "A heuristic score based on extracted skills, "
            "experience signals, education signals, keywords "
            "and document structure."
        )
    else:
        # Do not give a misleading percentage when no
        # supported skill requirements were extracted.
        final_score = None
        confidence = "Low"
        explanation = (
            "No recognized skills were extracted from the job "
            "description. Review the requirements manually."
        )

    return {
        "score": final_score,
        "confidence": confidence,
        "explanation": explanation,
        "scores": scores,
        "weights": weights,
        "required_skills": required_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": resume_skills,
        "evidence": evidence,
        "possible_evidence": possible_evidence,
        "checks": checks,
        "experience_note": experience_note,
        "education_note": education_note,
        "keyword_score": keywords
    }
