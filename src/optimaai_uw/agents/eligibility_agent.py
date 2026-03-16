# src/optimaai_uw/agents/eligibility_agent.py

class EligibilityAgent:
    def name(self):
        return "eligibility"

    def requires(self):
        return ["scoring"]

    def produces(self):
        return ["eligibility"]

    def run(self, context):
        score = context.get("scoring", {}).get("score", 0)
        eligible = score >= 10

        context["eligibility"] = {
            "eligible": eligible,
            "reason": "Score meets minimum threshold" if eligible else "Score too low"
        }

        return context

