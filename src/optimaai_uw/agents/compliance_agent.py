# src/optimaai_uw/agents/compliance_agent.py

import json
from pathlib import Path

from optimaai_uw.core.base_agent import BaseAgent
from optimaai_uw.compliance.state_compliance_pdf_to_json import StateCompliancePDFExtractor
from optimaai_uw.compliance.state_rule_extractor import StateRuleExtractor
from optimaai_uw.compliance.rule_evaluator import RuleEvaluator


class ComplianceAgent(BaseAgent):

    # ---------------------------------------------------------
    # Agent identity
    # ---------------------------------------------------------
    def name(self) -> str:
        return "ComplianceAgent"

    def requires(self):
        # Now depends on normalized data AND regulatory intelligence output
        return ["normalized", "regulatory_data"]

    def produces(self):
        return ["compliance"]

    # ---------------------------------------------------------
    # Main execution
    # ---------------------------------------------------------
    def run(self, context):
        print(">>> ComplianceAgent: Starting compliance workflow")

        # -----------------------------------------------------
        # Inputs from DAG
        # -----------------------------------------------------
        normalized = context.get("normalized", {})
        regulatory_data = context.get("regulatory_data")   # ← NEW

        if regulatory_data is None:
            raise RuntimeError("ComplianceAgent: Missing 'regulatory_data' from RegulatoryIntelligenceAgent")

        state = normalized.get("state")
        if not state:
            raise RuntimeError("ComplianceAgent: Missing 'state' in normalized data")

        state = state.upper()

        # -----------------------------------------------------
        # Paths
        # -----------------------------------------------------
        pdf_path = f"src/optimaai_uw/data/state_pdfs/{state}.pdf"
        raw_json_path = f"src/optimaai_uw/data/rulebooks/{state}_raw.json"
        rulebook_path = f"src/optimaai_uw/data/rulebooks/{state}_rules.json"

        Path("src/optimaai_uw/data/rulebooks").mkdir(parents=True, exist_ok=True)

        # -----------------------------------------------------
        # Stage 1: PDF → Raw JSON
        # -----------------------------------------------------
        print(f">>> ComplianceAgent: Extracting raw rules from PDF {pdf_path}")

        pdf_extractor = StateCompliancePDFExtractor(
            pdf_path=pdf_path,
            output_json=raw_json_path
        )

        raw_text = pdf_extractor.extract_text()
        pdf_extractor.save_raw_json()

        print(f"✔ ComplianceAgent: Raw JSON saved → {raw_json_path}")

        # -----------------------------------------------------
        # Stage 2: Raw JSON → Structured Rulebook
        # -----------------------------------------------------
        print(">>> ComplianceAgent: Building structured rulebook")

        raw_json = json.load(open(raw_json_path))

        rule_extractor = StateRuleExtractor(
            raw_text=raw_text,
            raw_json=raw_json,
            state_code=state
        )

        rule_extractor.save(rulebook_path)

        print(f"✔ ComplianceAgent: Structured rulebook saved → {rulebook_path}")

        # -----------------------------------------------------
        # Stage 3: Evaluate rules
        # -----------------------------------------------------
        print(">>> ComplianceAgent: Evaluating compliance rules")

        evaluator = RuleEvaluator(
            rulebook_path=rulebook_path,
            context=context,
            regulatory_data=regulatory_data   # ← NEW
        )

        compliance_results = evaluator.evaluate()

        print("✔ ComplianceAgent: Compliance evaluation complete")

        # -----------------------------------------------------
        # Return results to DAG
        # -----------------------------------------------------
        return {"compliance": compliance_results}
