from serpapi_client import SerpApiClient


class CivicResearchEngine:
    """Collects civic evidence from multiple SerpApi sources."""

    def __init__(self):
        self.serpapi = SerpApiClient()

    def research(self, problem, location):
        """Research a civic problem in a specific location."""

        search_query = f"{problem} {location} complaint grievance site:gov.in"

        maps_query = (
            f"government authority department {problem} {location}"
        )

        news_query = f"{problem} {location}"

        google_results = self.serpapi.google_search(
            search_query,
            location
        )

        maps_results = self.serpapi.google_maps_search(
            maps_query,
            location
        )

        news_results = self.serpapi.google_news_search(
            news_query
        )

        return {
            "problem": problem,
            "location": location,
            "google": google_results,
            "maps": maps_results,
            "news": news_results,
        }
