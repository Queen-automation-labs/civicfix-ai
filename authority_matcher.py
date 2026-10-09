class AuthorityMatcher:
    def match(self, problem, google_results, maps_results, news_results):
        text = str(problem).lower()
        candidates = []
        if any(word in text for word in ['road', 'pothole', 'garbage', 'drain', 'street', 'park']):
            candidates.append({'authority': 'Local Municipal Authority', 'score': 90, 'reason': 'The problem is commonly handled at the local municipal level.'})
        if any(word in text for word in ['highway', 'state road', 'national highway', 'bridge']):
            candidates.append({'authority': 'Road Construction / Highway Authority', 'score': 85, 'reason': 'The problem appears related to a major road or highway.'})
        if not candidates:
            candidates.append({'authority': 'Relevant Local Government Authority', 'score': 50, 'reason': 'The available problem description does not identify a more specific authority.'})
        candidates.sort(key=lambda item: item['score'], reverse=True)
        return {'problem': problem, 'recommended': candidates[0], 'candidates': candidates, 'google_evidence_count': len(google_results or []), 'maps_evidence_count': len(maps_results or []), 'news_evidence_count': len(news_results or [])}
