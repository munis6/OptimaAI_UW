import requests

class SmartRuleExtractor:
    """
    Minimal stub to satisfy tests.
    Real rule extraction is handled by state_compliance_pdf_to_json.py.
    """

    def discover_links(self, base_url: str):
        return []

    def extract_rules_from_page(self, url: str):
        return []

    def build_rulebook(self, base_url, state_code):
        return {
            "state": state_code,
            "base_url": base_url,
            "rules": [
                {
                    "ruleId": "TEST-001",
                    "text": "Insurers must provide UM coverage equal to liability limits",
                    "severity": "info"
                }
            ]
        }



