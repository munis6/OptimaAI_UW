class ScoringAgent:
    def name(self):
        return "scoring"

    def requires(self):
        return ["normalized"]

    def produces(self):
        return ["scoring"]

    def run(self, context):
        context["scoring"] = {
            "score": 20,
            "riskTier": "Low"
        }
        return context

