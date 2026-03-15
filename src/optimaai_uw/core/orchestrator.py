from typing import Dict, Any, List

from optimaai_uw.core.base_agent import BaseAgent

# Import all agents used in the legacy linear pipeline
from optimaai_uw.agents.intake_agent import IntakeAgent
from optimaai_uw.agents.hybrid_normalizer_agent import HybridNormalizerAgent
from optimaai_uw.agents.eligibility_agent import EligibilityAgent
from optimaai_uw.agents.scoring_agent import ScoringAgent
from optimaai_uw.agents.compliance_agent import ComplianceAgent
from optimaai_uw.agents.final_json_builder_agent import FinalJSONBuilderAgent
from optimaai_uw.agents.underwriting_summary_agent import UnderwritingSummaryAgent


class Orchestrator:
    """
    Legacy orchestrator preserved ONLY for backward compatibility with older tests
    and the PDF generation pipeline. It runs agents in a fixed linear sequence.
    """

    def __init__(self):
        # Auto-load agents in the correct order
        self.agents: List[BaseAgent] = [
            IntakeAgent(),
            HybridNormalizerAgent(),
            EligibilityAgent(),
            ScoringAgent(),
            ComplianceAgent(),
            UnderwritingSummaryAgent(),
            FinalJSONBuilderAgent(),
        ]

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        for agent in self.agents:
            context = agent.run(context)
        return context
