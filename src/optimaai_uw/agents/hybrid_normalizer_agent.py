# src/optimaai_uw/agents/hybrid_normalizer_agent.py

from optimaai_uw.core.base_agent import BaseAgent

class NormalizationAgent(BaseAgent):

    def name(self):
        return "normalized"

    def requires(self):
        return ["intake"]

    def produces(self):
        return ["normalized"]

    def run(self, context):
        payload = context["intake"]["payload"]

        customer = payload.get("customer", {})
        if not isinstance(customer, dict):
            customer = {}

        # Build metadata block required by tests
        metadata = {
            "generatedBy": payload.get("sourceSystem"),
            "transactionId": payload.get("transactionId")
        }

        context["normalized"] = {
            "customer": {
                "firstName": customer.get("firstName", "").strip(),
                "lastName": customer.get("lastName", "").strip(),
                "dob": customer.get("dob"),
                "state": customer.get("state")
            },
            "metadata": metadata
        }

        return context


# Required helper for PDF test
def normalize_incoming_json(raw_json):
    return raw_json
