# src/optimaai_uw/agents/underwriting_summary_agent.py

from typing import Dict, Any
from optimaai_uw.core.base_agent import BaseAgent


class UnderwritingSummaryAgent(BaseAgent):

    def name(self) -> str:
        return "underwriting_summary"

    def requires(self):
        # Must run AFTER eligibility, but also uses normalized + score + compliance
        return ["eligibility", "normalized", "score", "compliance"]

    def produces(self):
        return ["uwSummary"]

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produces a clean, human-readable underwriting summary
        combining:
        - eligibility decision
        - risk score
        - compliance findings
        - key applicant attributes
        """

        normalized = context.get("normalized", {})
        score_block = context.get("score", {})
        compliance_block = context.get("compliance", {})
        eligibility_block = context.get("eligibility", {})

        # -------------------------
        # Build Summary
        #--------------------------

        summary = {
            "applicantName": f"{normalized.get('firstName', '')} {normalized.get('lastName', '')}".strip(),
            "state": normalized.get("state"),
            "productType": normalized.get("productType"),
            "coverageAmount": normalized.get("requestedCoverageAmount"),
            "term": normalized.get("requestedTerm"),
            "riskScore": score_block.get("riskScore"),
            "riskTier": score_block.get("riskTier"),
            "compliancePassed": len([r for r in compliance_block.get("results", []) if r.get("status") == "FAIL"]) == 0,
            "eligibilityDecision": eligibility_block.get("decision"),
            "eligibilityReason": eligibility_block.get("reason"),
        }

        context["uwSummary"] = summary
        return context
