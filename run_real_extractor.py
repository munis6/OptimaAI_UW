from optimaai_uw.compliance.smart_rule_extractor import SmartRuleExtractor
import json

# Florida DOI homepage
FL_URL = "https://www.floir.com/Sections/PandC/ProductReview/ProductReview.aspx"


extractor = SmartRuleExtractor()

result = extractor.build_rulebook(
    base_url=FL_URL,
    state_code="FL"
)

# Print JSON to console
print(json.dumps(result, indent=2))
