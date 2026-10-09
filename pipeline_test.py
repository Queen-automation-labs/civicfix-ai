from research_engine import CivicResearchEngine
from authority_matcher import AuthorityMatcher
from action_generator import ActionGenerator
from official_source_filter import OfficialSourceFilter

problem = "Patna mein mere area ki road mein bade potholes hain"
location = "Patna, Bihar, India"


print("\n=== CIVICFIX AI PIPELINE ===")
print("Problem:", problem)
print("Location:", location)


# 1. Live SerpApi research
print("\n[1] Researching live web data...")

research_engine = CivicResearchEngine()

research = research_engine.research(
    problem,
    location
)

google_results = research["google"].get("organic_results", [])
maps_results = research["maps"].get("local_results", [])
news_results = research["news"].get("news_results", [])
print("\n[1.5] Filtering official sources...")

filter_engine = OfficialSourceFilter()

official_google_results = filter_engine.filter_results(
    google_results
)

print("Official Google sources:", len(official_google_results))
print("Google results:", len(google_results))
print("Maps results:", len(maps_results))
print("News results:", len(news_results))


# 2. Authority matching
print("\n[2] Finding responsible authority...")

matcher = AuthorityMatcher()

authority_result = matcher.match(
    problem,
    google_results,
    maps_results,
    news_results
)

print(
    "Authority:",
    authority_result["recommended"]["authority"]
)

print(
    "Confidence:",
    authority_result["recommended"]["score"],
    "%"
)


# 3. Generate action
print("\n[3] Generating citizen action...")

generator = ActionGenerator()

action = generator.generate(
    problem,
    location,
    authority_result,
    official_google_results,
    maps_results,
    news_results
)


print("\n=== FINAL RESULT ===")

print("\nAuthority:")
print(action["authority"])

print("\nConfidence:")
print(action["confidence"], "%")

print("\nReason:")
print(action["reason"])

print("\nEvidence:")

for item in action["evidence"]:
    print("-", item["title"])
    print(" ", item["link"])

print("\nComplaint Draft:")
print(action["complaint_draft"])

print("\nNext Action:")
print(action["next_action"])
