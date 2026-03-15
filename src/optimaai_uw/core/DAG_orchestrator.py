# src/optimaai_uw/core/DAG_orchestrator.py

from typing import Dict, Any, List, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

from optimaai_uw.agents.intake_agent import IntakeAgent
from optimaai_uw.agents.hybrid_normalizer_agent import HybridNormalizerAgent
from optimaai_uw.agents.scoring_agent import ScoringAgent
from optimaai_uw.agents.compliance_agent import ComplianceAgent
from optimaai_uw.agents.eligibility_agent import EligibilityAgent
from optimaai_uw.agents.underwriting_summary_agent import UnderwritingSummaryAgent
from optimaai_uw.agents.final_json_builder_agent import FinalJsonBuilderAgent
from optimaai_uw.agents.regulatory_intelligence.regulatory_intelligence_agent import RegulatoryIntelligenceAgent



class DAGOrchestrator:

    def __init__(self, agents=None):
        self.agents = agents or [
            IntakeAgent(),
            HybridNormalizerAgent(),
            ScoringAgent(),
            RegulatoryIntelligenceAgent(),   # ← NEW
            ComplianceAgent(),
            EligibilityAgent(),
            UnderwritingSummaryAgent(),
            FinalJsonBuilderAgent()
        ]


    # ---------------------------------------------------------
    # Build dependency graph
    # ---------------------------------------------------------
    def _build_graph(self):
        graph = {}
        for agent in self.agents:
            graph[agent.name()] = {
                "agent": agent,
                "requires": agent.requires(),
                "produces": agent.produces()
            }
        return graph

    # ---------------------------------------------------------
    # Detect cycles (safety)
    # ---------------------------------------------------------
    def _detect_cycles(self, graph):
        visited = set()
        stack = set()

        def visit(node):
            if node in stack:
                raise RuntimeError(f"Cyclic dependency detected at: {node}")
            if node in visited:
                return
            stack.add(node)
            for req in graph[node]["requires"]:
                if req in graph:  # only check agent-produced keys
                    visit(req)
            stack.remove(node)
            visited.add(node)

        for node in graph:
            visit(node)

    # ---------------------------------------------------------
    # Determine which agents are ready to run
    # ---------------------------------------------------------
    def _ready_agents(self, graph, completed: Set[str]):
        ready = []
        for name, meta in graph.items():
            if name in completed:
                continue
            if all(req in completed for req in meta["requires"]):
                ready.append(name)
        return ready

    # ---------------------------------------------------------
    # Execute DAG
    # ---------------------------------------------------------
    def execute(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        print(">>> DAG Orchestrator: Starting execution")

        graph = self._build_graph()
        self._detect_cycles(graph)

        context: Dict[str, Any] = {"raw_json": raw_json}
        completed: Set[str] = set()

        # Run until all agents complete
        while len(completed) < len(graph):
            ready = self._ready_agents(graph, completed)

            if not ready:
                missing = set(graph.keys()) - completed
                raise RuntimeError(f"No agents ready to run. Stuck on: {missing}")

            print(f">>> DAG Wave: Ready agents = {ready}")

            # Run ready agents in parallel
            with ThreadPoolExecutor(max_workers=len(ready)) as executor:
                futures = {
                    executor.submit(graph[name]["agent"].run, context.copy()): name
                    for name in ready
                }

                for future in as_completed(futures):
                    agent_name = futures[future]
                    result = future.result()

                    # Merge context safely
                    for k, v in result.items():
                        context[k] = v

                    completed.add(agent_name)
                    print(f"✔ Completed: {agent_name}")

        print(">>> DAG Orchestrator: All agents completed successfully")

        if "finalJson" not in context:
            raise RuntimeError("DAG completed but finalJson was not produced.")

        return context["finalJson"]
