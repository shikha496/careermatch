
import re


ACTION_WORDS = {
    "developed", "implemented", "created",
    "designed", "managed", "led",
    "improved", "analyzed", "built",
    "resolved", "delivered", "automated",
    "optimized", "coordinated"
}

RESULT_WORDS = {
    "increased", "reduced", "improved",
    "achieved", "saved", "delivered",
    "completed", "resulted", "decreased"
}


def evaluate_transcript(transcript):

    text = transcript.strip()

    if not text:
        raise ValueError("Transcript cannot be empty.")

    words = re.findall(r"\b[\w'-]+\b", text)
    lower_words = {word.lower() for word in words}

    word_count = len(words)

    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", text)
        if sentence.strip()
    ]

    action_count = len(lower_words & ACTION_WORDS)
    result_count = len(lower_words & RESULT_WORDS)

    # Transparent heuristics, not objective interview grades.
    length_score = min(100, round(word_count / 2))

    action_score = min(100, action_count * 20)

    result_score = min(100, result_count * 25)

    structure_score = 0

    if word_count >= 30:
        structure_score += 25

    if action_count:
        structure_score += 25

    if result_count:
        structure_score += 25

    if len(sentences) >= 3:
        structure_score += 25

    overall = round(
        length_score * 0.20
        + action_score * 0.25
        + result_score * 0.25
        + structure_score * 0.30
    )

    feedback = []

    if word_count < 40:
        feedback.append(
            "Provide more context and detail."
        )

    if action_count == 0:
        feedback.append(
            "Explain the specific actions you personally took."
        )

    if result_count == 0:
        feedback.append(
            "Include the outcome of your work."
        )

    if len(sentences) < 3:
        feedback.append(
            "Organize your answer into clear, complete sentences."
        )

    if not feedback:
        feedback.append(
            "Your response contains context, action and result signals. "
            "Review it for relevance and factual accuracy."
        )

    return {
        "overall_score": overall,
        "word_count": word_count,
        "sentence_count": len(sentences),
        "action_signals": action_count,
        "result_signals": result_count,
        "feedback": feedback,
        "disclaimer": (
            "This is a heuristic transcript assessment, not a "
            "validated measure of communication, confidence, "
            "pronunciation or hiring suitability."
        )
    }
