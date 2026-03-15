import os
import json

from optimaai_uw.agents.hybrid_normalizer_agent import normalize_incoming_json
from optimaai_uw.pdf_renderer.pdf_orchestrator import generate_underwriting_pdf
from optimaai_uw.core.orchestrator import Orchestrator


def test_generate_pdf():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "testdata", "sample_input.json")

    with open(json_path) as f:
        raw_json = json.load(f)

    final_json = Orchestrator().execute(raw_json)


    output_path = "sample_report.pdf"
    generate_underwriting_pdf(final_json, output_path)

    assert os.path.exists(output_path)
    print("PDF generated:", output_path)


if __name__ == "__main__":
    test_generate_pdf()
