def render_risk_narrative(pdf, final_json):
    risk = final_json.get("riskNarrative", {})
    ai = final_json.get("aiInsights", {})

    top_risk_drivers = risk.get("positiveFactors", [])
    top_pricing_factors = risk.get("negativeFactors", [])
    summary_narrative = risk.get("summary", "")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Top 3 Risk Drivers", ln=True)
    pdf.set_font("Helvetica", "", 11)

    if top_risk_drivers:
        for idx, item in enumerate(top_risk_drivers[:3], start=1):
            pdf.cell(0, 6, f"{idx}. {item}", ln=True)
    else:
        pdf.cell(0, 6, "N/A", ln=True)

    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Top 3 Pricing Factors", ln=True)
    pdf.set_font("Helvetica", "", 11)

    if top_pricing_factors:
        for idx, item in enumerate(top_pricing_factors[:3], start=1):
            pdf.cell(0, 6, f"{idx}. {item}", ln=True)
    else:
        pdf.cell(0, 6, "N/A", ln=True)

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Summary Narrative", ln=True)
    pdf.set_font("Helvetica", "", 11)

    if summary_narrative:
        pdf.multi_cell(0, 6, summary_narrative)
    else:
        pdf.cell(0, 6, "N/A", ln=True)

    pdf.ln(10)
