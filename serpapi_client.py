import os

import serpapi
from dotenv import load_dotenv


load_dotenv()


class SerpApiClient:
    """Central client for CivicFix web research."""

    def __init__(self):
        api_key = os.getenv("SERPAPI_KEY")

        if not api_key:
            raise ValueError("SERPAPI_KEY is missing from .env")

        self.client = serpapi.Client(api_key=api_key)

    def google_search(self, query, location):
        """Search Google for authorities and complaint channels."""
        return self.client.search({
            "engine": "google",
            "q": query,
            "location": location,
        })

    def google_maps_search(self, query, location):
        """Find relevant local authorities and offices."""
        return self.client.search({
            "engine": "google_maps",
            "q": query,
            "ll": "@25.5941,85.1376,12z",
            "type": "search",
        })

    def google_news_search(self, query):
        """Find recent news and public evidence."""
        return self.client.search({
            "engine": "google_news",
            "q": query,
            "gl": "in",
            "hl": "en",
        })
