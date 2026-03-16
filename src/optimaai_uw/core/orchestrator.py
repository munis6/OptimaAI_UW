# src/optimaai_uw/core/orchestrator.py

from optimaai_uw.core.DAG_orchestrator import DAGOrchestrator
from optimaai_uw.agents.intake_agent import DataIntakeAgent
from optimaai_uw.agents.hybrid_normalizer_agent import NormalizationAgent
from optimaai_uw.agents.compliance_agent import ComplianceAgent
from optimaai_uw.agents.eligibility_agent import EligibilityAgent
from optimaai_uw.agents.scoring_agent import ScoringAgent
from optimaai_uw.agents.underwriting_summary_agent import UnderwritingSummaryAgent
from optimaai_uw.agents.final_json_builder_agent import FinalJsonBuilderAgent


class Orchestrator:
    """
    High-level orchestrator used by the PDF test.
    It simply wires all agents into the DAG orchestrator.
    """

    def __init__(self):
        self.agents = [
            DataIntakeAgent(),
            NormalizationAgent(),
            ComplianceAgent(),
            EligibilityAgent(),
            ScoringAgent(),
            UnderwritingSummaryAgent(),
            FinalJsonBuilderAgent()
        ]

    def execute(self, raw_json):
        dag = DAGOrchestrator(self.agents)
        return dag.execute(raw_json)


