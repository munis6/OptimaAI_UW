# src/optimaai_uw/agents/underwriting_summary_agent.py

from optimaai_uw.core.base_agent import BaseAgent

class UnderwritingSummaryAgent(BaseAgent):

    def name(self):
        return "underwritingSummary"

    def requires(self):
        return ["normalized", "scoring", "eligibility"]

    def produces(self):
        return ["underwritingSummary"]

    def run(self, context):
        score = context["scoring"]["score"]
        eligible = context["eligibility"]["eligible"]

        if eligible:
            factors = [
                "Customer identity verified",
                "Risk score evaluated",
                "Eligibility rules applied",
                "Eligibility threshold met"
            ]
        else:
            factors = [
                "Customer identity verified",
                "Risk score evaluated",
                "Eligibility rules applied",
                "Eligibility threshold not met"
            ]

        context["underwritingSummary"] = {
            "decision": "APPROVE" if eligible else "REVIEW",
            "riskScore": score,
            "humanReviewRequired": "No" if eligible else "Yes",
            "factorsConsidered": "; ".join(factors)
        }

        return context
