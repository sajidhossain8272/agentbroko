import time
import logging
from skill_registry import SkillRegistry
from agent_memory import AgentMemory
from task_queue import TaskQueue

class Brain:
    def __init__(self):
        self.skills = SkillRegistry()
        self.memory = AgentMemory()
        self.queue = TaskQueue()

    @staticmethod
    def score_action(action_payload):
        """
        Priority Formula:
        (Revenue Potential * Probability * Strategic Value * Urgency * Learning Value) / (Cost * Risk)
        """
        rev = action_payload.get("revenue_potential", 10.0)
        prob = action_payload.get("probability", 0.8)
        strat = action_payload.get("strategic_value", 5.0)
        urgency = action_payload.get("urgency", 5.0)
        learning = action_payload.get("learning_value", 5.0)
        cost = max(action_payload.get("cost", 1.0), 0.1)
        risk = max(action_payload.get("risk", 1.0), 0.1)

        numerator = rev * prob * strat * urgency * learning
        denominator = cost * risk
        priority = round(numerator / denominator, 2)
        return min(priority, 1000.0)

    def evaluate_and_select_action(self):
        # 1. Pop highest priority task from Task Queue
        queued_task = self.queue.pop_highest_priority_task()
        if queued_task:
            return {
                "action": queued_task["type"],
                "title": queued_task["title"],
                "reason": f"Highest priority task in queue ({queued_task['priority']})",
                "priority_score": queued_task["priority"] * 100,
                "payload": queued_task["payload"],
                "task_id": queued_task["task_id"]
            }

        # 2. Autonomous Opportunity Selection fallback
        candidate = {
            "revenue_potential": 50.0,
            "probability": 0.85,
            "strategic_value": 8.0,
            "urgency": 7.0,
            "learning_value": 8.0,
            "cost": 1.0,
            "risk": 1.0
        }
        score = self.score_action(candidate)

        return {
            "action": "autonomous_education_and_engineering",
            "title": "Publish Level 1 Educational Lesson & Inspect GitHub Repositories",
            "reason": "Autonomous business & engineering execution loop",
            "priority_score": score,
            "payload": {"level": "level_1", "repo": "agentbroko/agentbroko"},
            "task_id": None
        }
