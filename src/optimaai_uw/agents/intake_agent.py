# src/optimaai_uw/agents/intake_agent.py

from optimaai_uw.core.base_agent import BaseAgent

class DataIntakeAgent(BaseAgent):

    def name(self):
        return "intake"

    def requires(self):
        return []

    def produces(self):
        return ["intake"]

    def run(self, context):
        raw = context.get("raw_json", {})

        context["intake"] = {
            "transactionId": raw.get("transactionId"),
            "sourceSystem": raw.get("sourceSystem"),
            "receivedAt": context.get("timestamp"),
            "payload": raw
        }

        return context

