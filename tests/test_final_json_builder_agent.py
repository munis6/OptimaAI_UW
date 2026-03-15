from optimaai_uw.agents.final_json_builder_agent import FinalJsonBuilderAgent


def test_final_json_builder_agent_builds_final_json():
    agent = FinalJsonBuilderAgent()

    context = {
        "normalized": {
            "customerFirstName": "John",
            "customerLastName": "Doe",
            "customerDOB": "1990-01-01",
            "customerState": "CA"
        },
        "scoring": {
            "score": 22
        },
        "eligibility": {
            "eligible": True,
            "reason": "Score meets minimum threshold"
        },
        "underwritingSummary": {
            "decision": "APPROVE",
            "riskScore": 22,
            "humanReviewRequired": "No"
        },
        "raw_json": {
            "firstName": "John",
            "lastName": "Doe"
        },
        "timestamp": "2026-03-06T12:00:00Z"
    }

    updated = agent.run(context)
    final_json = updated.get("finalJson", {})

    # Customer block
    assert final_json["customer"]["firstName"] == "John"
    assert final_json["customer"]["lastName"] == "Doe"
    assert final_json["customer"]["dob"] == "1990-01-01"
    assert final_json["customer"]["state"] == "CA"

    # Scoring block
    assert final_json["scoring"]["score"] == 22

    # Eligibility block
    assert final_json["eligibility"]["eligible"] is True

    # Underwriting summary block
    assert final_json["underwritingSummary"]["decision"] == "APPROVE"

    # Metadata block
    assert final_json["metadata"]["pipelineVersion"] == "1.0.0"
    assert final_json["metadata"]["generatedBy"] == "OptimaAI Underwriting Engine"
    assert final_json["metadata"]["timestamp"] == "2026-03-06T12:00:00Z"
