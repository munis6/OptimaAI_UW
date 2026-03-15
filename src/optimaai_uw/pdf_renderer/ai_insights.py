def ensure_list(value):
    """Guarantee list output for PDF rendering."""
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [value]
    return []


def render_ai_insights(pdf, final_json):
    ai = final_json.get("aiInsights", {})

    # FORCE LISTS — this fixes the vertical text bug
    driver_factors = ensure_list(ai.get("driverRiskFactors"))
    pricing_rationale = ai.get("pricingRationale", "N/A")
    underwriting_explanation = ai.get("underwritingExplanation", "N/A")
    improvement_suggestions = ai.get("improvementSuggestions", "N/A")
    ai_narrative = ai.get("aiNarrative", "N/A")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "AI Insights Summary", ln=True)
    pdf.ln(2)

    # Driver Risk Factors
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Driver Risk Factors", ln=True)

    pdf.set_font("Helvetica", "", 11)
    if driver_factors:
        for idx, item in enumerate(driver_factors, start=1):
            pdf.cell(0, 6, f"{idx}. {item}", ln=True)
    else:
        pdf.cell(0, 6, "N/A", ln=True)

    pdf.ln(6)

    # Pricing Rationale
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Pricing Rationale", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, pricing_rationale if pricing_rationale else "N/A")
    pdf.ln(6)

    # Underwriting Explanation
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Underwriting Explanation", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, underwriting_explanation if underwriting_explanation else "N/A")
    pdf.ln(6)

    # Improvement Suggestions
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Improvement Suggestions", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, improvement_suggestions if improvement_suggestions else "N/A")
    pdf.ln(6)

    # AI Narrative
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "AI Narrative", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, ai_narrative if ai_narrative else "N/A")
    pdf.ln(10)
