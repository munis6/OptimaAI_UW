# src/optimaai_uw/compliance/rule_evaluator.py

import json
from typing import Dict, Any, List


class RuleEvaluator:
    """
    Stage 3 of the compliance pipeline:
    - Input: structured rulebook (JSON from PDF)
    - Input: normalized policy context (from HybridNormalizerAgent)
    - Output: pass/fail results for each rule with evidence
    """

    def __init__(self, rulebook_path: str, context: Dict[str, Any]):
        self.rulebook_path = rulebook_path
        self.context = context
        self.rulebook = self._load_rulebook()

    # ---------------------------------------------------------
    # Load structured rulebook JSON
    # ---------------------------------------------------------
    def _load_rulebook(self) -> Dict[str, Any]:
        with open(self.rulebook_path, "r") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # Evaluate a single rule
    # ---------------------------------------------------------
    def evaluate_single_rule(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        rule_id = rule.get("ruleId")
        description = rule.get("description")
        required_value = rule.get("requiredValue")
        category = rule.get("category")

        policy_data = self.context.get("normalized", {})

        result = {
            "ruleId": rule_id,
            "category": category,
            "description": description,
            "requiredValue": required_value,
            "observedValue": None,
            "passed": None,
            "reason": None,
            "page": rule.get("page"),
            "severity": rule.get("severity"),
            "sourceText": rule.get("sourceText"),
        }

        # If rule has no required value → cannot evaluate
        if not required_value:
            result["passed"] = None
            result["reason"] = "No required value extracted — rule not evaluated"
            return result

        # Try to find a matching field in normalized policy data
        observed = None
        for key, value in policy_data.items():
            if isinstance(value, (str, int, float)) and str(required_value) in str(value):
                observed = value
                break

        result["observedValue"] = observed

        # Determine pass/fail
        if observed is None:
            result["passed"] = False
            result["reason"] = "Required value not found in policy data"
        else:
            result["passed"] = True
            result["reason"] = "Policy meets or exceeds required value"

        return result

    # ---------------------------------------------------------
    # Evaluate all rules in the rulebook
    # ---------------------------------------------------------
    def evaluate(self) -> Dict[str, Any]:
        rules = self.rulebook.get("rules", [])
        results: List[Dict[str, Any]] = []

        for rule in rules:
            results.append(self.evaluate_single_rule(rule))

        return {
            "state": self.rulebook.get("state"),
            "rulesChecked": results,
        }
