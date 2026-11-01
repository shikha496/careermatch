
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_ALIASES = {
    "Python": ["python", "python3"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "React": ["react", "reactjs", "react.js"],
    "FastAPI": ["fastapi", "fast api"],
    "Django": ["django"],
    "Flask": ["flask"],
    "SQL": ["sql", "structured query language"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo db"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["natural language processing", "nlp"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Git": ["git", "github"],
    "CI/CD": ["ci/cd", "continuous integration",
              "continuous deployment"],
    "Terraform": ["terraform"],
    "HTML": ["html"],
    "CSS": ["css"],
    "Communication": ["communication skills"],
    "Leadership": ["leadership"],
    "Problem Solving": ["problem solving", "problem-solving"]
}


def contains_term(text, term):

    pattern = (
        r"(?<![a-zA-Z0-9+#])"
        + re.escape(term)
        + r"(?![a-zA-Z0-9+#])"
    )

    return bool(
        re.search(pattern, text, re.IGNORECASE)
    )


class SkillMatcher:

    def extract_skills(self, text):

        if not text:
            return []

        found = []

        for skill, aliases in SKILL_ALIASES.items():

            terms = [skill] + aliases

            if any(
                contains_term(text, term)
                for term in terms
            ):
                found.append(skill)

        return found

    def compare_skills(
        self,
        resume_text,
        job_description
    ):

        resume_skills = set(
            self.extract_skills(resume_text)
        )

        job_skills = set(
            self.extract_skills(job_description)
        )

        matched = sorted(
            resume_skills & job_skills
        )

        missing = sorted(
            job_skills - resume_skills
        )

        extra = sorted(
            resume_skills - job_skills
        )

        if job_skills:
            score = round(
                len(matched) / len(job_skills) * 100
            )
        else:
            score = None

        return {
            "score": score,
            "resume_skills": sorted(resume_skills),
            "required_skills": sorted(job_skills),
            "matched_skills": matched,
            "missing_skills": missing,
            "extra_skills": extra
        }

    def semantic_similarity(
        self,
        resume_text,
        job_description
    ):

        if not resume_text.strip() or not job_description.strip():
            return 0.0

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        try:

            matrix = vectorizer.fit_transform([
                resume_text,
                job_description
            ])

            similarity = cosine_similarity(
                matrix[0:1],
                matrix[1:2]
            )[0][0]

            return round(float(similarity) * 100, 2)

        except ValueError:
            return 0.0
