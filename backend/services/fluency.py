
import re
from collections import Counter


class FluencyAnalyzer:
    """Analyzes an interview transcript for basic speech fluency."""

    FILLER_WORDS = [
        "um",
        "uh",
        "umm",
        "uhh",
        "like",
        "basically",
        "actually",
        "literally",
        "you know",
        "i mean",
        "sort of",
        "kind of",
    ]

    @staticmethod
    def analyze_transcript(transcript: str, duration_seconds: float):
        """
        Analyze a transcript and return speech fluency metrics.

        Args:
            transcript: Speech converted into text.
            duration_seconds: Duration of the spoken answer.

        Returns:
            Dictionary containing fluency metrics and suggestions.
        """

        if not isinstance(transcript, str) or not transcript.strip():
            raise ValueError("Transcript cannot be empty.")

        if duration_seconds <= 0:
            raise ValueError("Duration must be greater than zero.")

        # Normalize transcript
        text = transcript.lower().strip()

        # Extract words
        words = re.findall(r"\b[\w']+\b", text)
        word_count = len(words)

        if word_count == 0:
            raise ValueError("No valid words found in transcript.")

        # Calculate speaking speed
        duration_minutes = duration_seconds / 60
        words_per_minute = round(word_count / duration_minutes, 2)

        # Count filler words
        filler_counts = {}

        for filler in FluencyAnalyzer.FILLER_WORDS:
            pattern = r"\b" + re.escape(filler) + r"\b"
            count = len(re.findall(pattern, text))
            if count:
                filler_counts[filler] = count

        total_fillers = sum(filler_counts.values())

        filler_percentage = round(
            (total_fillers / word_count) * 100, 2
        )

        # Vocabulary variety
        unique_words = len(set(words))

        vocabulary_diversity = round(
            (unique_words / word_count) * 100, 2
        )

        # Speaking pace feedback
        if words_per_minute < 100:
            pace_feedback = "Your speaking pace is relatively slow."
        elif words_per_minute <= 160:
            pace_feedback = "Your speaking pace is within a typical conversational range."
        else:
            pace_feedback = "Your speaking pace is relatively fast."

        # Filler word feedback
        if filler_percentage <= 2:
            filler_feedback = "Excellent control over filler words."
        elif filler_percentage <= 5:
            filler_feedback = "Good fluency, but try reducing filler words."
        else:
            filler_feedback = "Practice speaking with fewer filler words."

        # Generate suggestions
        suggestions = []

        if words_per_minute < 100:
            suggestions.append(
                "Practice speaking at a slightly more natural pace."
            )
        elif words_per_minute > 160:
            suggestions.append(
                "Slow down slightly and pronounce words clearly."
            )

        if total_fillers > 0:
            suggestions.append(
                "Replace filler words with short pauses."
            )

        if vocabulary_diversity < 40:
            suggestions.append(
                "Try using more varied vocabulary in your answers."
            )

        if not suggestions:
            suggestions.append(
                "Keep practicing to maintain your speaking fluency."
            )

        return {
            "word_count": word_count,
            "duration_seconds": duration_seconds,
            "words_per_minute": words_per_minute,
            "filler_word_count": total_fillers,
            "filler_words": filler_counts,
            "filler_percentage": filler_percentage,
            "unique_words": unique_words,
            "vocabulary_diversity": vocabulary_diversity,
            "pace_feedback": pace_feedback,
            "filler_feedback": filler_feedback,
            "suggestions": suggestions,
        }
