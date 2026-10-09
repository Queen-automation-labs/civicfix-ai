from official_source_filter import OfficialSourceFilter

results = [
    {
        "title": "Patna Municipal Corporation",
        "link": "https://pmc.bihar.gov.in/",
        "snippet": "Official Patna Municipal Corporation website"
    },
    {
        "title": "Patna District Contact",
        "link": "https://www.indiacustomercare.com/patna-district-all-important-contact-no",
        "snippet": "Third-party information"
    },
    {
        "title": "Bihar Government",
        "link": "https://state.bihar.gov.in/",
        "snippet": "Government of Bihar"
    },
    {
        "title": "Random News",
        "link": "https://example.com/news",
        "snippet": "News article"
    }
]

filter_engine = OfficialSourceFilter()

official_results = filter_engine.filter_results(results)

print("\n=== OFFICIAL SOURCE FILTER TEST ===")
print("Total results:", len(results))
print("Official results:", len(official_results))

print("\nOfficial Sources:")

for item in official_results:
    print("-", item["title"])
    print(" ", item["link"])
