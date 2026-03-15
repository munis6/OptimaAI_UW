def render_data_lineage(pdf, final_json):
    lineage = final_json.get("lineage", {})
    field_lineage = lineage.get("fieldLineage", [])
    missing_data = lineage.get("missingDataSummary", "N/A")

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Data Lineage & Field Traceability", ln=True)
    pdf.ln(2)

    # Field-Level Lineage Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Field-Level Lineage", ln=True)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(50, 8, "Field Name", border=1)
    pdf.cell(50, 8, "Source System", border=1)
    pdf.cell(45, 8, "Source Path", border=1)
    pdf.cell(45, 8, "Normalized Path", border=1, ln=True)

    pdf.set_font("Helvetica", "", 11)

    if field_lineage:
        for row in field_lineage:
            pdf.cell(50, 8, str(row.get("fieldName", "N/A")), border=1)
            pdf.cell(50, 8, str(row.get("sourceSystem", "N/A")), border=1)
            pdf.cell(45, 8, str(row.get("sourcePath", "N/A")), border=1)
            pdf.cell(45, 8, str(row.get("normalizedPath", "N/A")), border=1, ln=True)
    else:
        pdf.cell(50, 8, "N/A", border=1)
        pdf.cell(50, 8, "N/A", border=1)
        pdf.cell(45, 8, "N/A", border=1)
        pdf.cell(45, 8, "N/A", border=1, ln=True)

    pdf.ln(8)

    # Missing Data Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Missing Data Summary", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, missing_data if missing_data else "N/A")
    pdf.ln(10)
