class ActionGenerator:
    def generate(self, problem, location, authority_result, google_results, maps_results, news_results):
        recommended = authority_result.get("recommended", {})

        authority = recommended.get(
            "authority",
            "Relevant Local Government Authority"
        )

        score = recommended.get("score", 0)

        reason = recommended.get(
            "reason",
            "The available evidence suggests this authority is relevant."
        )

        evidence = []

        for item in (google_results or [])[:3]:
            title = item.get("title")
            link = item.get("link")

            if title:
                evidence.append({
                    "title": title,
                    "link": link
                })

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
            "reason": reason,
            "evidence": evidence,
            "complaint_draft": complaint,
            "next_action": (
                "Submit this complaint to "
                + authority
                + " and keep the complaint/reference number for follow-up."
            )
        }
