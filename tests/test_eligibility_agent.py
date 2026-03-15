from optimaai_uw.agents.eligibility_agent import EligibilityAgent

def test_eligibility_agent_basic():
    agent = EligibilityAgent()

    context = {
        "scoring": {
            "score": 20
        }
    }

    updated = agent.run(context)

    assert "eligibility" in updated
    assert updated["eligibility"]["eligible"] is True
    assert updated["eligibility"]["reason"] == "Score meets minimum threshold"


def test_eligibility_agent_low_score():
    agent = EligibilityAgent()

    context = {
        "scoring": {
            "score": 5
        }
    }

    updated = agent.run(context)

    assert updated["eligibility"]["eligible"] is False
    assert updated["eligibility"]["reason"] == "Score too low"
