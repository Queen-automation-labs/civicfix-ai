
import unittest

from official_source_filter import OfficialSourceFilter


class TestOfficialSourceFilter(unittest.TestCase):

    def setUp(self):
        self.filter_engine = OfficialSourceFilter()

    def test_keeps_official_government_domains(self):
        results = [
            {
                "title": "Patna Municipal Corporation",
                "link": "https://pmc.bihar.gov.in/",
                "snippet": "Official website"
            },
            {
                "title": "Bihar Government",
                "link": "https://state.bihar.gov.in/",
                "snippet": "Government website"
            }
        ]

        filtered = self.filter_engine.filter_results(results)

        self.assertEqual(len(filtered), 2)

    def test_removes_third_party_domains(self):
        results = [
            {
                "title": "Third-party contact",
                "link": "https://example.com/contact",
                "snippet": "Contact information"
            }
        ]

        filtered = self.filter_engine.filter_results(results)

        self.assertEqual(len(filtered), 0)

    def test_handles_empty_results(self):
        filtered = self.filter_engine.filter_results([])

        self.assertEqual(filtered, [])



if __name__ == "__main__":
    unittest.main()
