def render_pricing_breakdown(pdf, final_json):
    pricing = final_json.get("pricing", {})
    narrative = pricing.get("pricingNarrative", "N/A")

    components = pricing.get("components", {
        "Base Premium": "N/A",
        "Driver Impact": "N/A",
        "Vehicle Impact": "N/A",
        "ZIP Impact": "N/A",
        "Coverage Impact": "N/A",
        "Discounts/Surcharges": "N/A"
    })

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Pricing Breakdown", ln=True)
    pdf.ln(2)

    # Premium Components Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Premium Components", ln=True)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(80, 8, "Component", border=1)
    pdf.cell(40, 8, "Amount", border=1, ln=True)

    pdf.set_font("Helvetica", "", 11)

    for label, amount in components.items():
        pdf.cell(80, 8, f"{label}:", border=1)
        pdf.cell(40, 8, str(amount), border=1, ln=True)

    pdf.ln(8)

    # Pricing Narrative
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Pricing Narrative", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, narrative if narrative else "N/A")
    pdf.ln(10)
