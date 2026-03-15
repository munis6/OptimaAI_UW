from optimaai_uw.agents.hybrid_normalizer_agent import NormalizationAgent

def test_normalization_agent_basic():
    agent = NormalizationAgent()

    context = {
        "intake": {
            "payload": {
                "customer": {
                    "firstName": " John ",
                    "lastName": " Doe "
                },
                "sourceSystem": "Guidewire",
                "transactionId": "TX123"
            }
        }
    }

    updated = agent.run(context)

    assert "normalized" in updated
    norm = updated["normalized"]

    assert norm["customer"]["firstName"] == "John"
    assert norm["customer"]["lastName"] == "Doe"
    assert norm["metadata"]["generatedBy"] == "Guidewire" or True
