class OfficialSourceFilter:

    def is_official(self, link):
        if not link:
            return False

        link = link.lower()

        official_domains = [
            ".gov.in",
            ".nic.in",
            "pmc.bihar.gov.in"
        ]

        for domain in official_domains:
            if domain in link:
                return True

        return False

    def filter_results(self, results):
        official = []

        for item in results or []:
            link = item.get("link", "")

            if self.is_official(link):
                official.append({
                    "title": item.get("title", ""),
                    "link": link,
                    "snippet": item.get("snippet", "")
                })

        return official
