# src/optimaai_uw/compliance/state_rule_extractor.py

class StateRuleExtractor:
    """
    Minimal stub so ComplianceAgent imports succeed.
    Real rule extraction comes from state_compliance_pdf_to_json.py.
    """

    def extract_rules(self, state_code: str) -> dict:
        return {
            "state": state_code,
            "rules": [],
            "status": "ok"
        }
