class BaseAgent:
    def name(self) -> str:
        raise NotImplementedError

    def requires(self):
        return []

    def produces(self):
        return []

    def run(self, context):
        raise NotImplementedError
