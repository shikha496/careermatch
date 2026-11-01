import unittest

from services.ats_analyzer import analyze_ats
from services.skill_extractor import extract_skills


JOB_DESCRIPTION = (
    "software developer having a deep knowledge of apis, database, "
    "backend development."
)
RESUME_TEXT = (
    "Backend engineer. Experience: API design, database development, "
    "and backend development."
)


class SkillExtractorTests(unittest.TestCase):
    def test_extracts_common_backend_job_requirements(self):
        self.assertEqual(
            extract_skills(JOB_DESCRIPTION),
            ["API", "Database", "Backend Development"],
        )

    def test_ats_scores_common_backend_job_requirements(self):
        result = analyze_ats(RESUME_TEXT, JOB_DESCRIPTION)

        self.assertEqual(
            result["required_skills"],
            ["API", "Database", "Backend Development"],
        )
        self.assertEqual(result["matched_skills"], result["required_skills"])
        self.assertEqual(result["missing_skills"], [])
        self.assertIsNotNone(result["score"])


if __name__ == "__main__":
    unittest.main()
