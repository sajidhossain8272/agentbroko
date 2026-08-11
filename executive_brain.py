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
from executive_value_function import ExecutiveValueFunction
from new_project_gate import NewProjectGate
from strategy_memory import StrategyMemory
from self_audit_engine import SelfAuditEngine
from task_manager import TaskManager
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
        self.value_function = ExecutiveValueFunction()
        self.project_gate = NewProjectGate()
        self.strategy_mem = StrategyMemory()
        self.audit_engine = SelfAuditEngine()
        self.task_mgr = TaskManager()
        self.bus = EventBus()

    def evaluate_world_and_select_action(self):
        logging.info("[EXECUTIVE BRAIN V10] Evaluating world state, self-audit, and evidence-driven value function...")

        # 1. Run periodic self-audit
        audit = self.audit_engine.run_self_audit()

        # 1b. Reload tasks from disk to pick up any tasks created by the self-audit
        self.task_mgr.reload_tasks()

        # 2. Check permissions & safe mode
        allowed, msg = self.permissions.is_action_allowed(required_level=2)
        if not allowed:
            self.bus.emit("brain.decision", f"Action restricted: {msg}", metadata={"action": "WAIT"})
            return {"action": "WAIT", "reason": msg}

        # 3. Consume highest-priority QUEUED task from TaskManager first
        queued_tasks = [t for t in self.task_mgr.tasks if t.get("status") == "QUEUED"]
        if queued_tasks:
            queued_tasks.sort(key=lambda x: x.get("priority", 0.0), reverse=True)
            top_task = queued_tasks[0]
            # Claim the task: QUEUED -> RUNNING
            self.task_mgr.update_task_status(top_task["id"], "RUNNING")
            decision = {
                "action": top_task.get("skill", "general"),
                "title": top_task["objective"],
                "priority_score": top_task.get("priority", 75.0),
                "task_id": top_task["id"],
                "task_objective": top_task["objective"],
                "task_description": top_task.get("description", ""),
                "reasons": f"Consumed highest-priority queued task #{top_task['id']} (Priority: {top_task.get('priority', 75.0)})"
            }
            self.bus.emit("brain.decision", f"ExecutiveBrain V10 Selected Task: '{decision['title']}' (Priority: {decision['priority_score']})", metadata=decision)
            return decision

        # 4. Generate candidate actions across 12 categories (fallback when queue is empty)
        candidate_actions = [
            {"id": "act_101", "title": "System Self-Healing & Log Error Remediation", "category": "agent_reliability", "expected_value": 90.0, "prob_success": 0.95, "strategic_fit": 9.5, "learning_value": 8.0, "cost": 2.0, "risk": 0.05},
            {"id": "act_102", "title": "Moltbook Technical Thread Conversation", "category": "moltbook_intelligence", "expected_value": 75.0, "prob_success": 0.85, "strategic_fit": 8.5, "learning_value": 7.5, "cost": 3.0, "risk": 0.10},
            {"id": "act_103", "title": "Domain-Agnostic Content Strategy Evaluation", "category": "decision_quality", "expected_value": 80.0, "prob_success": 0.90, "strategic_fit": 9.0, "learning_value": 8.5, "cost": 2.0, "risk": 0.05},
            {"id": "act_104", "title": "Create Unvalidated External Repo", "category": "external_project", "expected_value": 40.0, "prob_success": 0.30, "strategic_fit": 4.0, "learning_value": 3.0, "cost": 80.0, "risk": 0.60}
        ]

        # Filter out failed strategy patterns
        valid_candidates = []
        for c in candidate_actions:
            failed, lesson = self.strategy_mem.is_failed_pattern(c["title"])
            if not failed:
                valid_candidates.append(c)

        ranked = self.value_function.rank_candidate_actions(valid_candidates)
        top_act = ranked[0]

        decision = {
            "action": top_act["category"],
            "title": top_act["title"],
            "priority_score": top_act["value_score"],
            "value_function_rank": 1,
            "reasons": "Selected via ExecutiveValueFunction formula (Internal System Quality > Unvalidated Projects)"
        }

        self.bus.emit("brain.decision", f"ExecutiveBrain V10 Selected Action: '{decision['title']}' (Score: {decision['priority_score']})", metadata=decision)
        return decision
