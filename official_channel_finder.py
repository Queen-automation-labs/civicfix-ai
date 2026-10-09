
from serpapi_client import SerpApiClient


class OfficialChannelFinder:
    """Find relevant official civic complaint channels."""

    def __init__(self):
        self.serpapi = SerpApiClient()

    def find(self, problem, location):
        """Find relevant official civic complaint channels."""
        query = (
            f"{location} municipal corporation road pothole repair complaint "
            "grievance official portal site:gov.in"
        )
        results = self.serpapi.google_search(query, location)
        organic = results.get("organic_results", [])
        channels = []

        for item in organic:
            link = item.get("link", "")
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            text = (title + " " + snippet + " " + link).lower()
            url = link.lower()

            official = ".gov.in" in url or ".nic.in" in url
            if not official:
                continue

            if "property/swm tax related only" in text:
                continue
            if "pmcgrivance/website/mobile.aspx" in url:
                continue

            relevant = any(word in text for word in [
                "grievance redressal cell",
                "urban local body",
                "municipal corporation",
                "road construction department",
                "road repair",
                "pothole",
            ])
            if not relevant:
                continue

            channels.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "official_domain": True,
            })

        return channels
