# src/optimaai_uw/agents/hybrid_normalizer_agent.py

from typing import Any, Dict
from optimaai_uw.core.base_agent import BaseAgent


# ---------------------------------------------------------
# Helper: Safe nested getter
# ---------------------------------------------------------
def get_value(data: Dict[str, Any], *keys):
    """
    Safely retrieves nested values from a dictionary.
    Example: get_value(payload, "applicant", "firstName")
    """
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


# ---------------------------------------------------------
# Helper: Normalize incoming JSON
# ---------------------------------------------------------
def normalize_incoming_json(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts raw intake JSON into a normalized underwriting structure.
    This function is imported directly by tests and PDF generator.
    """
    return {
        "firstName": get_value(payload, "applicant", "firstName"),
        "lastName": get_value(payload, "applicant", "lastName"),
        "dob": get_value(payload, "applicant", "dob"),
        "state": get_value(payload, "applicant", "state"),

        "productType": get_value(payload, "product", "type"),
        "requestedCoverageAmount": get_value(payload, "product", "coverageAmount"),
        "requestedTerm": get_value(payload, "product", "term"),
        "effectiveDate": get_value(payload, "product", "effectiveDate"),
    }


# ---------------------------------------------------------
# Agent: HybridNormalizerAgent
# ---------------------------------------------------------
class HybridNormalizerAgent(BaseAgent):

    def name(self) -> str:
        return "normalized"

    def requires(self):
        return ["intake"]

    def produces(self):
        return ["normalized"]

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        payload = context.get("intake", {})
        normalized = normalize_incoming_json(payload)
        context["normalized"] = normalized
        return context
