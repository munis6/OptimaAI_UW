# src/optimaai_uw/agents/final_json_builder_agent.py

class FinalJsonBuilderAgent:
    def name(self):
        return "finalJson"

    def requires(self):
        return ["normalized", "scoring", "eligibility", "underwritingSummary"]

    def produces(self):
        return ["finalJson"]

    def run(self, context):
        n = context["normalized"]
        s = context["scoring"]
        e = context["eligibility"]
        u = context["underwritingSummary"]

        context["finalJson"] = {
            "customer": {
                "firstName": n.get("customerFirstName"),
                "lastName": n.get("customerLastName"),
                "dob": n.get("customerDOB"),
                "state": n.get("customerState")
            },
            "scoring": s,
            "eligibility": e,
            "underwritingSummary": u,
            "metadata": {
                "pipelineVersion": "1.0.0",
                "timestamp": context.get("timestamp"),
                "transactionId": context.get("intake", {}).get("transactionId"),
                "sourceSystem": context.get("intake", {}).get("sourceSystem"),
                "generatedBy": "OptimaAI Underwriting Engine"
            },
            "raw": context.get("raw_json", {})
        }

        return context


# Alias required by tests
class FinalJSONBuilderAgent(FinalJsonBuilderAgent):
    pass
