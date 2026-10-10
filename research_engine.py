from serpapi_client import SerpApiClient


class CivicResearchEngine:
    """Collects civic evidence from multiple SerpApi sources."""

    def __init__(self):
        self.serpapi = SerpApiClient()

    def research(self, problem, location):
        """Research a civic problem in a specific location."""
        search_query = (
            f'{location} {problem} '
            'municipal corporation road department '
            'site:gov.in OR site:nic.in'
        )

        maps_query = (
            f"{problem} municipal corporation road maintenance office {location}"
        )

        news_query = f"{problem} {location}"

        google_queries = [
            search_query,
            f'"{location}" {problem} complaint site:bihar.gov.in',
            f'"{location}" {problem} grievance site:gov.in',
        ]
        google_results = {"organic_results": []}
        seen_links = set()
        for query in google_queries:
            response = self.serpapi.google_search(query, location)
            for item in response.get("organic_results", []):
                link = item.get("link", "")
                if link and link not in seen_links:
                    seen_links.add(link)
                    google_results["organic_results"].append(item)

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
