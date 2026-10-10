from urllib.parse import urlparse
from serpapi_client import SerpApiClient


class OfficialChannelFinder:
    """Find relevant official complaint channels from live search results."""

    def __init__(self):
        self.serpapi = SerpApiClient()

    def find(self, problem, location):
        query = (
            f'{problem} "{location}" official complaint grievance '
            "department portal (site:gov.in OR site:nic.in)"
        )
        results = self.serpapi.google_search(query, location)
        organic = results.get("organic_results", [])

        problem_lower = problem.lower()
        stopwords = {
            "there", "their", "that", "this", "with", "from",
            "have", "main", "area", "near", "very", "dangerous",
            "issue", "please", "cause", "which", "what"
        }
        location_words = set(location.lower().replace(",", " ").split())
        terms = {
            word.strip(".,!?;:()")
            for word in problem_lower.split()
            if len(word.strip(".,!?;:()")) > 3
            and word.strip(".,!?;:()") not in stopwords
            and word.strip(".,!?;:()") not in location_words
        }

        groups = {
            "pothole": ["pothole", "road repair", "road construction", "public works"],
            "road": ["pothole", "road repair", "road construction", "public works"],
            "garbage": ["garbage", "waste collection", "sanitation"],
            "waste": ["garbage", "waste collection", "sanitation"],
            "drain": ["drainage", "sewer", "storm water"],
            "water": ["water supply", "water department"],
            "streetlight": ["street light", "streetlight", "public works"],
            "electricity": ["electricity", "power distribution"],
        }
        for key, synonyms in groups.items():
            if key in problem_lower:
                terms.update(synonyms)

        channels = []
        seen = set()

        for item in organic:
            link = item.get("link", "")
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            host = (urlparse(link).hostname or "").lower()
            text = f"{title} {snippet} {link}".lower()

            official = (
                host == "gov.in" or host.endswith(".gov.in")
                or host == "nic.in" or host.endswith(".nic.in")
            )
            relevant = any(term in text for term in terms)

            if not official or not relevant or link in seen:
                continue
            if "property/swm tax related only" in text:
                continue
            if "pmcgrivance/website/mobile.aspx" in link.lower():
                continue

            seen.add(link)
            channels.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "official_domain": True,
                "relevance_note": (
                    "Official domain and issue-related search terms matched; "
                    "confirm the responsible department and accepted complaint category."
                ),
            })

            if len(channels) >= 5:
                break

        if not channels and "bihar" in location.lower():
            channels.append({
                "title": "Bihar Sahyog RTMS — Public Grievance Portal",
                "link": "https://sahyog.bihar.gov.in/Sahyog/Default.aspx",
                "snippet": (
                    "Government of Bihar public grievance portal. "
                    "Check the available department and complaint category "
                    "before submitting this civic issue."
                ),
                "official_domain": True,
                "relevance_note": (
                    "General public grievance option; acceptance of this "
                    "specific road issue is not guaranteed."
                ),
            })

        return channels
