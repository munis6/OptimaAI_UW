def render_compliance_summary(pdf, final_json):
    compliance = final_json.get("compliance", {})
    rules = compliance.get("rulesChecked", [])
    narrative = compliance.get("complianceNarrative", "N/A")

    state = compliance.get("state", "N/A")
    status = compliance.get("overallStatus", "N/A")
    notes = compliance.get("notes", "N/A")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Compliance Summary", ln=True)
    pdf.ln(2)

    # Basic Compliance Info
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"State: {state}", ln=True)
    pdf.cell(0, 6, f"Overall Status: {status}", ln=True)
    pdf.cell(0, 6, f"Notes: {notes}", ln=True)
    pdf.ln(6)

    # Rules Checked Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Rules Checked", ln=True)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Rule ID", border=1)
    pdf.cell(80, 8, "Description", border=1)
    pdf.cell(30, 8, "Passed", border=1)
    pdf.cell(30, 8, "Severity", border=1, ln=True)

    pdf.set_font("Helvetica", "", 11)

    if rules:
        for r in rules:
            pdf.cell(40, 8, str(r.get("ruleId", "N/A")), border=1)
            pdf.cell(80, 8, str(r.get("description", "N/A")), border=1)
            pdf.cell(30, 8, str(r.get("passed", "N/A")), border=1)
            pdf.cell(30, 8, str(r.get("severity", "N/A")), border=1, ln=True)
    else:
        pdf.cell(40, 8, "N/A", border=1)
        pdf.cell(80, 8, "N/A", border=1)
        pdf.cell(30, 8, "N/A", border=1)
        pdf.cell(30, 8, "N/A", border=1, ln=True)

    pdf.ln(8)

    # Compliance Narrative
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Compliance Narrative", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, narrative if narrative else "N/A")
    pdf.ln(10)
