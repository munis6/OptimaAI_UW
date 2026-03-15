from typing import Any, Dict

class BaseAgent:
    name: str = "base"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
