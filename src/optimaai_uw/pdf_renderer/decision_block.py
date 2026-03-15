def render_decision_block(pdf, final_json):
    scoring = final_json.get("scoring", {})
    eligibility = final_json.get("eligibility", {})
    summary = final_json.get("underwritingSummary", {})
    coverage = final_json.get("coverage", {})

    risk_score = scoring.get("score", "N/A")
    decision = summary.get("decision", "N/A")
    premium = coverage.get("adjustedPremium", "N/A")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Risk Score: {risk_score}", ln=True)
    pdf.cell(0, 6, f"Eligibility Decision: {decision}", ln=True)
    pdf.cell(0, 6, f"Premium: {premium}", ln=True)
    pdf.ln(4)

    # Optional narrative
    narrative = summary.get("factorsConsidered", "")
    if narrative:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Summary Narrative", ln=True)

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, narrative)
        pdf.ln(4)
