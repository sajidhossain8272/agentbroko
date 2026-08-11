import time
import logging
from event_bus import EventBus

class ExecutiveValueFunction:
    CATEGORIES = [
        "agent_reliability", "failure_recovery", "decision_quality",
        "moltbook_intelligence", "opportunity_discovery", "monetization_intelligence",
        "engineering_capabilities", "memory_learning", "observability",
        "external_project", "research", "wait"
    ]

    def __init__(self):
        self.bus = EventBus()

    @classmethod
    def calculate_action_score(cls, action_item):
        """
        Formula:
        (EstValue * ProbSuccess * StrategicFit * LearningValue) / (Cost + Risk + ReversibilityPenalty)
        """
        category = action_item.get("category", "wait")
        est_val = action_item.get("expected_value", 50.0)
        prob_success = action_item.get("prob_success", 0.8)
        strategic_fit = action_item.get("strategic_fit", 8.0)
        learning_val = action_item.get("learning_value", 7.0)

        cost = max(action_item.get("cost", 5.0), 1.0)
        risk = max(action_item.get("risk", 0.2) * 10.0, 0.5)
        rev_penalty = 5.0 if category == "external_project" else 1.0 # High penalty for new repos/projects

        # Priority boost for internal system improvements over random external projects
        if category in ["agent_reliability", "failure_recovery", "decision_quality", "memory_learning"]:
            strategic_fit += 3.0

        numerator = est_val * prob_success * strategic_fit * learning_val
        denominator = cost + risk + rev_penalty
        score = round(numerator / denominator, 2)

        return score

    def rank_candidate_actions(self, candidate_actions):
        ranked = []
        for act in candidate_actions:
            sc = self.calculate_action_score(act)
            act_copy = dict(act)
            act_copy["value_score"] = sc
            ranked.append(act_copy)

        ranked.sort(key=lambda x: x["value_score"], reverse=True)
        if ranked:
            top = ranked[0]
            self.bus.emit("executive.action.scored", f"Top Value Action #{top.get('id', 'act')}: '{top.get('title', '')}' (Score: {top['value_score']})", metadata=top)
        return ranked
