import json
from unittest.mock import patch, Mock

from optimaai_uw.compliance.smart_rule_extractor import SmartRuleExtractor


# -----------------------------
# Fake HTML pages for testing
# -----------------------------
FAKE_HOME_HTML = """
<html>
<body>
    <a href="/auto-insurance-requirements">Auto Insurance Requirements</a>
    <a href="/random-page">Random Page</a>
</body>
</html>
"""

FAKE_RULE_PAGE_HTML = """
<html>
<body>
    <p>Insurers must provide UM coverage equal to liability limits.</p>
    <p>This is a random sentence with no rules.</p>
    <p>The minimum limits are 25/50/10 for bodily injury liability.</p>
</body>
</html>
"""

FAKE_RANDOM_PAGE_HTML = """
<html>
<body>
    <p>This page has nothing useful.</p>
</body>
</html>
"""


# -----------------------------
# Mock requests.get behavior
# -----------------------------
def mock_requests_get(url, timeout=15, headers=None):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.headers = {"Content-Type": "text/html"}

    if "auto-insurance-requirements" in url:
        mock_resp.text = FAKE_RULE_PAGE_HTML
    elif "random-page" in url:
        mock_resp.text = FAKE_RANDOM_PAGE_HTML
    else:
        mock_resp.text = FAKE_HOME_HTML

    return mock_resp


# -----------------------------
# The actual test
# -----------------------------
@patch("optimaai_uw.compliance.smart_rule_extractor.requests.get", side_effect=mock_requests_get)
def test_smart_rule_extractor(mock_get):
    extractor = SmartRuleExtractor()

    result = extractor.build_rulebook(
        base_url="https://insurance.test.gov",
        state_code="DE"
    )

    print(json.dumps(result, indent=2))

    # Assertions
    assert result["state"] == "DE"
    assert len(result["rules"]) == 1  # Only 1 rule-like sentence expected

    rule_texts = [r["text"].lower() for r in result["rules"]]

    assert "insurers must provide um coverage equal to liability limits" in rule_texts[0]

