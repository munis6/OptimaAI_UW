from typing import Any, Dict
from optimaai_uw.core.base_agent import BaseAgent
import json
from datetime import datetime
import pytz  # pip install pytz


class IntakeAgent(BaseAgent):

    def name(self) -> str:
        return "data_intake"

    def requires(self):
        # First agent in the DAG — no dependencies
        return []

    def produces(self):
        # Produces the "intake" block used by all downstream agents
        return ["intake"]

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts either:
        - context["raw_json"] (string or dict)
        - OR the raw JSON directly as the context itself
        """

        # Case 1: Orchestrator passed {"raw_json": "..."}
        raw_json = context.get("raw_json")

        # Case 2: Orchestrator passed the raw JSON directly
        if raw_json is None:
            raw_json = context

        # Parse if string
        if isinstance(raw_json, str):
            payload = json.loads(raw_json)
        else:
            payload = raw_json

        # Convert to US Eastern Time with timezone abbreviation (EST/EDT)
        eastern = pytz.timezone("US/Eastern")
        now_est = datetime.now(eastern)
        formatted_time = now_est.strftime("Date: %Y-%m-%d, Time:%H:%M:%S %Z")

        context["intake"] = {
            "payload": payload,
            "sourceSystem": payload.get("sourceSystem"),
            "transactionId": payload.get("transactionId"),
            "receivedAt": formatted_time
        }

        return context
