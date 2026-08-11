import logging
import time
from goal_manager import GoalManager
from opportunity_discovery import OpportunityDiscoveryEngine
from opportunity_scoring import OpportunityScoringEngine
from business_experiment_engine import BusinessExperimentEngine
from content_brain import ContentBrain
from ai_provider_router import AIProviderRouter
from revenue_engine import RevenueEngine
from permission_manager import PermissionManager
from event_bus import EventBus

class ExecutiveBrain:
    def __init__(self):
        self.goal_mgr = GoalManager()
        self.opp_engine = OpportunityDiscoveryEngine()
        self.scorer = OpportunityScoringEngine()
        self.exp_engine = BusinessExperimentEngine()
        self.content_brain = ContentBrain()
        self.ai_router = AIProviderRouter()
        self.revenue_engine = RevenueEngine()
        self.permissions = PermissionManager()
        self.bus = EventBus()

    def evaluate_world_and_select_action(self):
        logging.info("[EXECUTIVE BRAIN] Evaluating world state, goals, and opportunities...")
        
        # 1. Check permissions & safe mode
        allowed, msg = self.permissions.is_action_allowed(required_level=2)
        if not allowed:
            self.bus.emit("brain.decision", f"Action restricted: {msg}", metadata={"action": "WAIT"})
            return {"action": "WAIT", "reason": msg}

        # 2. Check high-priority goals
        goals = self.goal_mgr.list_goals()
        high_priority_goals = [g for g in goals if g.get("status") == "IN_PROGRESS"]

        # 3. Discover & score business opportunities
        opps = self.opp_engine.list_opportunities()
        ranked_opps = self.scorer.rank_opportunities(opps)
        top_opp = ranked_opps[0] if ranked_opps else None

        # 4. Check ContentBrain for publication candidates
        content_decision = self.content_brain.evaluate_and_select_action()

        # 5. Synthesize Executive Decision
        if content_decision.get("action") == "POST" and top_opp and top_opp["score"] > 800:
            decision = {
                "action": "autonomous_business_content_execution",
                "title": f"Execute Business-Value Content: '{content_decision['topic']}'",
                "priority_score": 92.5,
                "opportunity": top_opp["name"],
                "content_decision": content_decision
            }
        else:
            decision = {
                "action": "autonomous_master_execution",
                "title": "Master Unified OS Heartbeat Execution",
                "priority_score": 85.0,
                "opportunity": top_opp["name"] if top_opp else "System Operations"
            }

        self.bus.emit("brain.decision", f"ExecutiveBrain Selected Action: '{decision['title']}' (Score: {decision['priority_score']})", metadata=decision)
        return decision
