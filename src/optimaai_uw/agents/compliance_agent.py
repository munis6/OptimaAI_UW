# src/optimaai_uw/agents/compliance_agent.py

class ComplianceAgent:
    def name(self):
        return "compliance"

    def requires(self):
        return ["normalized"]

    def produces(self):
        return ["compliance"]

    def run(self, context):
        print(">>> ComplianceAgent: Starting compliance workflow")

        state = (
            context.get("normalized", {})
                .get("customer", {})
                .get("state", "NA")
        )

        context["compliance"] = {
            "state": state,
            "status": "PASS",
            "rulesChecked": [],
            "rulesFailed": [],
            "details": []
        }

        return context


