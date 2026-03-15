from optimaai_uw.core.base_agent import BaseAgent

class FinalJsonBuilderAgent(BaseAgent):
    def name(self):
        return "finalJson"

    def requires(self):
        return ["summary", "compliance", "scoring", "eligibility", "normalized"]

    def produces(self):
        return ["finalJson"]

    def run(self, context):
        # Merge all agent outputs into a final JSON structure
        final_json = {
            "applicant": context.get("normalized", {}),
            "eligibility": context.get("eligibility", {}),
            "scoring": context.get("scoring", {}),
            "compliance": context.get("compliance", {}),
            "summary": context.get("summary", {}),
        }

        context["finalJson"] = final_json
        return context
