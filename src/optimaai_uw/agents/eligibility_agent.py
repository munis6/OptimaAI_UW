# src/optimaai_uw/agents/eligibility_agent.py

from typing import Dict, Any
from optimaai_uw.core.base_agent import BaseAgent


class EligibilityAgent(BaseAgent):

    def name(self) -> str:
        return "eligibility"

    def requires(self):
        # Must run AFTER scoring + compliance
        return ["score", "compliance"]

    def produces(self):
        return ["eligibility"]

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines underwriting eligibility based on:
        - risk score
        - compliance rule failures
        """

        score_block = context.get("score", {})
        compliance_block = context.get("compliance", {})

        risk_tier = score_block.get("riskTier", "Unknown")
        risk_score = score_block.get("riskScore", 0)

        compliance_results = compliance_block.get("results", [])
        failed_rules = [r for r in compliance_results if r.get("status") == "FAIL"]

        # -------------------------
        # Eligibility Logic
        # -------------------------

        # Rule 1: Any compliance failure = Decline
        if failed_rules:
            decision = "Decline"
            reason = "Compliance rule violations detected"
        else:
            # Rule 2: Risk-based eligibility
            if risk_tier == "Low":
                decision = "Approve"
                reason = "Low risk profile"
            elif risk_tier == "Medium":
                decision = "Review"
                reason = "Medium risk — requires manual review"
            else:
                decision = "Decline"
                reason = "High risk profile"

        context["eligibility"] = {
            "decision": decision,
            "reason": reason,
            "riskScore": risk_score,
            "riskTier": risk_tier,
            "failedComplianceRules": failed_rules
        }

        return context
