from optimaai_uw.agents.intake_agent import DataIntakeAgent
from datetime import datetime

def test_intake_agent_adds_intake_section():
    agent = DataIntakeAgent()

    raw = {
        "transactionId": "T123",
        "sourceSystem": "Guidewire",
        "customer": {"firstName": "John"}
    }

    context = {"raw_json": raw}
    result = agent.run(context)

    assert "intake" in result
    assert result["intake"]["transactionId"] == "T123"
    assert result["intake"]["sourceSystem"] == "Guidewire"
    assert "receivedAt" in result["intake"]
