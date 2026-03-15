def load_rulebook(state: str):
    """
    Minimal rulebook loader used by ComplianceAgent and tests.
    Returns a simple rulebook with two rules.
    """
    return {
        "state": state,
        "rules": [
            {
                "id": "R1",
                "description": "Applicant must have a valid state",
                "field": "state"
            },
            {
                "id": "R2",
                "description": "Coverage amount must be greater than zero",
                "field": "requestedCoverageAmount"
            }
        ]
    }
