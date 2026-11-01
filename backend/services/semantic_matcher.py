
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)

    return [
        part.strip()
        for part in parts
        if len(part.strip().split()) >= 4
    ]


def find_similar_evidence(
    requirement,
    resume_text,
    top_n=3
):
    sentences = split_sentences(resume_text)

    if not sentences:
        return []

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        matrix = vectorizer.fit_transform(
            [requirement] + sentences
        )

        similarities = cosine_similarity(
            matrix[0:1],
            matrix[1:]
        ).flatten()

        ranked = sorted(
            enumerate(similarities),
            key=lambda item: item[1],
            reverse=True
        )

        results = []

        for index, score in ranked[:top_n]:
            if score >= 0.08:
                results.append({
                    "text": sentences[index],
                    "similarity": round(float(score), 3),
                    "review_required": True
                })

        return results

    except ValueError:
        return []


def semantic_requirement_analysis(job_text, resume_text):
    job_sentences = split_sentences(job_text)

    results = []

    for requirement in job_sentences:
        evidence = find_similar_evidence(
            requirement,
            resume_text,
            top_n=1
        )

        results.append({
            "requirement": requirement,
            "evidence": evidence
        })

    return results
