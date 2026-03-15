# tests/test_compliance_agent.py

import unittest
from src.optimaai_uw.agents.compliance_agent import ComplianceAgent

class TestComplianceAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ComplianceAgent()

    def test_requires(self):
        self.assertEqual(self.agent.requires(), ["normalized"])

    def test_produces(self):
        self.assertEqual(self.agent.produces(), ["compliance"])

    def test_run_creates_compliance_block(self):
        # Minimal normalized input
        context = {
            "normalized": {
                "customer": {"state": "MD"},
                "policy": {"type": "LIFE"}
            }
        }

        updated = self.agent.run(context)

        # Check compliance block exists
        self.assertIn("compliance", updated)

        compliance = updated["compliance"]

        # Validate structure
        self.assertIn("status", compliance)
        self.assertIn("rulesChecked", compliance)
        self.assertIn("rulesFailed", compliance)
        self.assertIn("details", compliance)

        # Validate expected placeholder values
        self.assertEqual(compliance["status"], "PASS")
        self.assertIsInstance(compliance["details"], list)

    def test_run_does_not_modify_other_context_fields(self):
        context = {
            "normalized": {"customer": {"state": "MD"}},
            "scoring": {"score": 88}
        }

        updated = self.agent.run(context)

        # scoring must remain untouched
        self.assertEqual(updated["scoring"], {"score": 88})

if __name__ == "__main__":
    unittest.main()
