# src/optimaai_uw/pdf_renderer/pdf_orchestrator.py

from fpdf import FPDF
from typing import Dict, Any

from .header_layout import render_pdf_header
from .decision_block import render_decision_block
from .risk_narrative import render_risk_narrative
from .coverage_table import render_coverage_table
from .pricing_breakdown import render_pricing_breakdown
from .compliance_summary import render_compliance_summary


class UnderwritingPDF(FPDF):
    def header(self):
        pass  # We manually render header via render_pdf_header()


def generate_underwriting_pdf(final_json: Dict[str, Any], output_path: str):
    pdf = UnderwritingPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header
    render_pdf_header(pdf, final_json)

    # Executive Summary
    render_decision_block(pdf, final_json)

    # Risk Narrative
    render_risk_narrative(pdf, final_json)

    # Coverage Table
    render_coverage_table(pdf, final_json)

    # Pricing Breakdown
    render_pricing_breakdown(pdf, final_json)

    # Compliance Summary
    render_compliance_summary(pdf, final_json)

    # Save PDF
    pdf.output(output_path)


# =====================================================================
# MAIN EXECUTION BLOCK (ALWAYS RUNS WHEN USING -m)
# =====================================================================
if __name__ == "__main__":
    print("\n>>> Running PDF Orchestrator __main__ block")

    import json
    import os
    from optimaai_uw.core.DAG_orchestrator import DAGOrchestrator

    # Load sample input JSON
    base_dir = os.path.dirname(__file__)
    sample_path = os.path.join(base_dir, "sample_input.json")

    print(f">>> Loading sample input from: {sample_path}")

    if not os.path.exists(sample_path):
        raise FileNotFoundError(f"sample_input.json not found at: {sample_path}")

    with open(sample_path) as f:
        raw_json = json.load(f)

    # Run full underwriting pipeline
    print(">>> Executing DAG pipeline...")
    final_json = DAGOrchestrator().execute(raw_json)

    # Output PDF path
    output_path = "sample_report.pdf"

    # Generate PDF
    print(f">>> Generating PDF at: {output_path}")
    generate_underwriting_pdf(final_json, output_path)

    print(f"\nPDF generated successfully: {output_path}\n")
