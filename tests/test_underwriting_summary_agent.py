from optimaai_uw.agents.underwriting_summary_agent import UnderwritingSummaryAgent


def test_underwriting_summary_agent_eligible():
    agent = UnderwritingSummaryAgent()

    context = {
        "normalized": {
            "customerFirstName": "John",
            "customerLastName": "Doe"
        },
        "scoring": {
            "score": 20
        },
        "eligibility": {
            "eligible": True
        }
    }

    updated = agent.run(context)

    summary = updated.get("underwritingSummary", {})

    assert summary["riskScore"] == 20
    assert summary["decision"] == "APPROVE"
    assert summary["humanReviewRequired"] == "No"
    assert "Customer identity verified" in summary["factorsConsidered"]
    assert "Eligibility threshold met" in summary["factorsConsidered"]


def test_underwriting_summary_agent_not_eligible():
    agent = UnderwritingSummaryAgent()

    context = {
        "normalized": {
            "customerFirstName": "Jane",
            "customerLastName": "Smith"
        },
        "scoring": {
            "score": 5
        },
        "eligibility": {
            "eligible": False
        }
    }

    updated = agent.run(context)

    summary = updated.get("underwritingSummary", {})

    assert summary["riskScore"] == 5
    assert summary["decision"] == "REVIEW"
    assert summary["humanReviewRequired"] == "Yes"
    assert "Eligibility threshold not met" in summary["factorsConsidered"]
