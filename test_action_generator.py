from action_generator import ActionGenerator

problem = "Patna mein mere area ki road mein bade potholes hain"
location = "Patna, Bihar, India"

authority_result = {
    "recommended": {
        "authority": "Local Municipal Authority",
        "score": 90,
        "reason": "The problem is commonly handled at the local municipal level."
    }
}

google_results = [
    {
        "title": "Patna road complaint information",
        "link": "https://example.com"
    },
    {
        "title": "Municipal road services",
        "link": "https://example.com"
    }
]

maps_results = []
news_results = []

generator = ActionGenerator()

result = generator.generate(
    problem,
    location,
    authority_result,
    google_results,
    maps_results,
    news_results
)

print("\n=== ACTION GENERATOR TEST ===")
print("Authority:", result["authority"])
print("Confidence:", result["confidence"], "%")
print("Reason:", result["reason"])

print("\nComplaint Draft:")
print(result["complaint_draft"])

print("\nNext Action:")
print(result["next_action"])

print("\nEvidence:")
for item in result["evidence"]:
    print("-", item["title"])
