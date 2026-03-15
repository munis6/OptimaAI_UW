def render_coverage_table(pdf, final_json):
    coverage = final_json.get("coverage", {})
    riders = coverage.get("riders", [])
    full_coverage = coverage.get("fullCoverageIndicator", "N/A")
    narrative = coverage.get("coverageNarrative", "N/A")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Coverage Summary", ln=True)
    pdf.ln(2)

    # Selected Coverages Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Selected Coverages", ln=True)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(60, 8, "Coverage Type", border=1)
    pdf.cell(40, 8, "Limit", border=1)
    pdf.cell(40, 8, "Deductible", border=1)
    pdf.cell(40, 8, "Included", border=1, ln=True)

    pdf.set_font("Helvetica", "", 11)

    if riders:
        for r in riders:
            pdf.cell(60, 8, r.get("name", "N/A"), border=1)
            pdf.cell(40, 8, str(r.get("limit", "N/A")), border=1)
            pdf.cell(40, 8, str(r.get("deductible", "N/A")), border=1)
            pdf.cell(40, 8, str(r.get("included", "N/A")), border=1, ln=True)
    else:
        pdf.cell(60, 8, "N/A", border=1)
        pdf.cell(40, 8, "N/A", border=1)
        pdf.cell(40, 8, "N/A", border=1)
        pdf.cell(40, 8, "N/A", border=1, ln=True)

    pdf.ln(8)

    # Full Coverage Indicator
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Full Coverage Indicator", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, str(full_coverage), ln=True)
    pdf.ln(6)

    # Coverage Narrative
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Coverage Narrative", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, narrative if narrative else "N/A")
    pdf.ln(10)
