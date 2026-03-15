from optimaai_uw.agents.scoring_agent import ScoringAgent

def test_scoring_agent_basic():
    agent = ScoringAgent()

    context = {
        "normalized": {
            "customerFirstName": "John",
            "customerLastName": "Doe"
        }
    }

    updated = agent.run(context)

    assert "scoring" in updated
    assert updated["scoring"]["score"] == 20
