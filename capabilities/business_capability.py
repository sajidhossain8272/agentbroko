import logging
from opportunity_discovery import OpportunityDiscoveryEngine
from opportunity_scoring import OpportunityScoringEngine
from business_experiment_engine import BusinessExperimentEngine
from business_intelligence_memory import BusinessIntelligenceMemory
from event_bus import EventBus

class BusinessCapability:
    def __init__(self):
        self.discovery = OpportunityDiscoveryEngine()
        self.scoring = OpportunityScoringEngine()
        self.experiment = BusinessExperimentEngine()
        self.intel = BusinessIntelligenceMemory()
        self.bus = EventBus()

    def execute(self, payload=None):
        logging.info("[CAPABILITY] Executing BusinessCapability...")
        opps = self.discovery.list_opportunities()
        ranked = self.scoring.rank_opportunities(opps)

        if not ranked:
            return {"status": "IDLE", "message": "No opportunities to score"}

        top_opp = ranked[0]
        self.bus.emit("business.opportunity.scored", f"Top Opportunity: '{top_opp['name']}' (Score: {top_opp['score']})", metadata=top_opp)

        return {
            "status": "SUCCESS",
            "top_opportunity": top_opp["name"],
            "category": top_opp["category"],
            "opportunity_score": top_opp["score"],
            "expected_revenue": top_opp["estimated_revenue"],
            "validated_revenue": 0.0,
            "actual_revenue": 0.0
        }
