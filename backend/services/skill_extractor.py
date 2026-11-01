
import re


SKILL_ALIASES = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "FastAPI": ["fastapi", "fast api"],
    "Django": ["django"],
    "Flask": ["flask"],
    "API": [
        "api",
        "apis",
        "application programming interface",
        "application programming interfaces",
    ],
    "Database": ["database", "databases"],
    "Backend Development": [
        "backend",
        "back-end",
        "back end",
        "server-side development",
        "server side development",
    ],
    "Streamlit": ["streamlit"],
    "SQL": ["sql", "structured query language"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo db"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud platform"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Terraform": ["terraform"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous delivery"],
    "Git": ["git", "version control"],
    "Linux": ["linux"],
    "REST API": ["rest api", "restful api", "rest services"],
    "GraphQL": ["graphql"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "NLP": ["natural language processing", "nlp"],
    "Generative AI": ["generative ai", "genai", "gen ai"],
    "LLM": ["large language model", "llm", "large language models"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Visualization": ["data visualization"],
    "Communication": ["communication skills", "communication"],
    "Leadership": ["leadership", "team leadership"],
    "Teamwork": ["teamwork", "collaboration"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Project Management": ["project management"],
    "Agile": ["agile", "agile methodology"],
    "Scrum": ["scrum"],
    "Jira": ["jira"],
    "Microservices": ["microservices", "microservice architecture"],
    "Redis": ["redis"],
    "Kafka": ["kafka", "apache kafka"],
    "Spark": ["apache spark", "spark"],
    "Airflow": ["airflow", "apache airflow"],
}


def normalize(text):
    return re.sub(r"\s+", " ", text.lower())


def contains_alias(text, alias):
    pattern = r"(?<![a-z0-9])" + re.escape(alias.lower()) + r"(?![a-z0-9])"
    return bool(re.search(pattern, text))


def extract_skills(text):
    normalized = normalize(text)
    found = []

    for canonical, aliases in SKILL_ALIASES.items():
        if any(contains_alias(normalized, alias) for alias in aliases):
            found.append(canonical)

    return found


def find_skill_evidence(text, skill):
    aliases = SKILL_ALIASES.get(skill, [skill])
    lines = text.splitlines()

    evidence = []

    for index, line in enumerate(lines):
        for alias in aliases:
            if contains_alias(line.lower(), alias):
                evidence.append({
                    "line": index + 1,
                    "text": line.strip(),
                    "alias": alias
                })
                break

    return evidence


def extract_skill_evidence(text, skills):
    result = {}

    for skill in skills:
        result[skill] = find_skill_evidence(text, skill)

    return result
