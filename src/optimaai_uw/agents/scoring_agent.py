# src/optimaai_uw/agents/scoring_agent.py

from typing import Dict, Any
from optimaai_uw.core.base_agent import BaseAgent


class ScoringAgent(BaseAgent):

    def name(self) -> str:
        return "scoring"

    def requires(self):
        # Must run AFTER normalization
        return ["normalized"]

    def produces(self):
        return ["score"]

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produces a simple underwriting risk score based on normalized data.
        Replace this logic with your real scoring model later.
        """

        normalized = context.get("normalized", {})

        # Example scoring logic (placeholder)
        score = 0

        # Age factor
        dob = normalized.get("dob")
        if dob:
            # crude age calc
            birth_year = int(dob.split("-")[0])
            age = 2026 - birth_year
            if age < 30:
                score += 10
            elif age < 50:
                score += 20
            else:
                score += 30

        # State factor
        state = normalized.get("state")
        if state in ["CA", "NY"]:
            score += 15
        else:
            score += 5

        # Coverage amount factor
        amount = normalized.get("requestedCoverageAmount") or 0

        if amount > 750000:
            score += 25
        elif amount > 250000:
            score += 15
        else:
            score += 5

        context["score"] = {
            "riskScore": score,
            "riskTier": (
                "Low" if score < 25 else
                "Medium" if score < 50 else
                "High"
            )
        }

        return context
