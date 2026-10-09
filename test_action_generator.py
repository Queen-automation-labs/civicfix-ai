
import unittest

from action_generator import ActionGenerator


class TestActionGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ActionGenerator()

        self.problem = "Road potholes in my area"
        self.location = "Patna, Bihar, India"

        self.authority_result = {
            "recommended": {
                "authority": "Local Municipal Authority",
                "score": 90,
                "reason": "Commonly handled at the local municipal level."
            }
        }

        self.google_results = [
            {
                "title": "Road complaint information",
                "link": "https://example.com"
            }
        ]

    def test_generates_complaint_draft(self):
        result = self.generator.generate(
            self.problem,
            self.location,
            self.authority_result,
            self.google_results,
            [],
            []
        )

        self.assertIn("complaint_draft", result)
        self.assertIn(self.problem, result["complaint_draft"])

    def test_returns_recommended_authority(self):
        result = self.generator.generate(
            self.problem,
            self.location,
            self.authority_result,
            self.google_results,
            [],
            []
        )

        self.assertEqual(
            result["authority"],
            "Local Municipal Authority"
        )

    def test_returns_preliminary_authority_status(self):
        result = self.generator.generate(
            self.problem,
            self.location,
            self.authority_result,
            self.google_results,
            [],
            []
        )

        self.assertIn("not verified", result["authority_status"].lower())


if __name__ == "__main__":
    unittest.main()
