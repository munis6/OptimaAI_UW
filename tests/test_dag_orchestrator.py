import pytest
from optimaai_uw.core.DAG_orchestrator import DAGOrchestrator
from optimaai_uw.core.base_agent import BaseAgent


class MockAgent(BaseAgent):
    def __init__(self, name, requires, produces, output):
        self._name = name
        self._requires = requires
        self._produces = produces
        self._output = output

    def name(self):
        return self._name

    def requires(self):
        return self._requires

    def produces(self):
        return self._produces

    def run(self, context):
        for k, v in self._output.items():
            context[k] = v
        return context


def test_dag_executes_in_correct_order():
    agents = [
        MockAgent("A", [], ["a"], {"a": 1}),
        MockAgent("B", ["a"], ["b"], {"b": 2}),
        MockAgent("C", ["b"], ["c"], {"c": 3}),
    ]

    orchestrator = DAGOrchestrator(agents)
    result = orchestrator.execute({"raw": True})

    assert result["c"] == 3
    assert result["b"] == 2
    assert result["a"] == 1


def test_parallel_execution():
    agents = [
        MockAgent("A", [], ["a"], {"a": 1}),
        MockAgent("B", ["a"], ["b"], {"b": 2}),
        MockAgent("C", ["a"], ["c"], {"c": 3}),
        MockAgent("D", ["b", "c"], ["d"], {"d": 4}),
    ]

    orchestrator = DAGOrchestrator(agents)
    result = orchestrator.execute({"raw": True})

    assert result["a"] == 1
    assert result["b"] == 2
    assert result["c"] == 3
    assert result["d"] == 4


def test_missing_dependency_raises_error():
    agents = [
        MockAgent("A", [], ["a"], {"a": 1}),
        MockAgent("B", ["x"], ["b"], {"b": 2}),
    ]

    orchestrator = DAGOrchestrator(agents)

    with pytest.raises(RuntimeError):
        orchestrator.execute({"raw": True})


def test_cycle_detection():
    agents = [
        MockAgent("A", ["C"], ["a"], {"a": 1}),
        MockAgent("B", ["A"], ["b"], {"b": 2}),
        MockAgent("C", ["B"], ["c"], {"c": 3}),
    ]

    orchestrator = DAGOrchestrator(agents)

    with pytest.raises(RuntimeError):
        orchestrator.execute({"raw": True})


def test_final_json_must_exist():
    agents = [
        MockAgent("A", [], ["a"], {"a": 1}),
        MockAgent("B", ["a"], ["b"], {"b": 2}),
    ]

    orchestrator = DAGOrchestrator(agents)

    with pytest.raises(RuntimeError):
        orchestrator.execute({"raw": True})


def test_full_pipeline_final_json():
    agents = [
        MockAgent("A", [], ["a"], {"a": 1}),
        MockAgent("B", ["a"], ["b"], {"b": 2}),
        MockAgent("C", ["b"], ["finalJson"], {"finalJson": {"ok": True}}),
    ]

    orchestrator = DAGOrchestrator(agents)
    result = orchestrator.execute({"raw": True})

    assert result["ok"] is True
