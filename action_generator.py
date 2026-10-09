class ActionGenerator:
    def generate(self, problem, location, authority_result, google_results, maps_results, news_results):
        recommended = authority_result.get("recommended", {})

        authority = recommended.get(
            "authority",
            "Relevant Local Government Authority"
        )

        score = recommended.get("score")

        reason = recommended.get(
            "reason",
            "The available evidence suggests this authority is relevant."
        )

        evidence = []

        problem_terms = [
            word.lower()
            for word in problem.split()
            if len(word) > 3
        ]

        for item in (google_results or []):
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "")

            text = (title + " " + snippet + " " + link).lower()

            official = (
                ".gov.in" in link.lower()
                or ".nic.in" in link.lower()
            )

            relevant = any(
                term in text for term in problem_terms
            )

            if title and link and official and relevant:
                evidence.append({
                    "title": title,
                    "link": link
                })

            if len(evidence) >= 3:
                break

        complaint = (
            "Subject: Complaint regarding "
            + problem
            + " in "
            + location
            + "\n\n"
            + "Dear Sir/Madam,\n\n"
            + "I would like to report the following civic issue: "
            + problem
            + ".\n"
            + "Location: "
            + location
            + ".\n\n"
            + "Please investigate the issue and take the necessary corrective action.\n"
            + "Kindly provide an update on the complaint.\n\n"
            + "Regards,\n"
            + "Citizen"
        )

        return {
            "authority": authority,
            "confidence": score,
            "authority_status": "Preliminary suggestion — not verified",
            "reason": reason,
            "evidence": evidence,
            "complaint_draft": complaint,
            "next_action": (
                "Submit this complaint to "
                + authority
                + " and keep the complaint/reference number for follow-up."
            )
        }
