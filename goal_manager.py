import json
import os
import time
from event_bus import EventBus

class GoalManager:
    def __init__(self, goals_file="goals.json"):
        self.goals_file = goals_file
        self.bus = EventBus()
        self.goals = self.load_goals()

    def load_goals(self):
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_goals()

    def save_goals(self):
        try:
            with open(self.goals_file, 'w') as f:
                json.dump(self.goals, f, indent=2)
        except Exception:
            pass

    def get_seed_goals(self):
        return [
            {
                "goal_id": "goal_001",
                "objective": "Operate 24/7 Autonomous Blockchain Education & Open-Source Software Factory",
                "priority": 95.0,
                "status": "ACTIVE",
                "progress": 85,
                "success_criteria": "Published verified daily lessons & 100% passing GitHub CI builds",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "goal_id": "goal_002",
                "objective": "Build & Maintain Autonomous Real-Time Control Center UI",
                "priority": 90.0,
                "status": "ACTIVE",
                "progress": 90,
                "success_criteria": "Interactive Web UI on port 8000 with real-time WebSocket event streaming",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    def create_goal(self, objective, priority=80.0, success_criteria="Goal achieved"):
        goal_id = f"goal_{len(self.goals) + 1:03d}"
        new_goal = {
            "goal_id": goal_id,
            "objective": objective,
            "priority": float(priority),
            "status": "ACTIVE",
            "progress": 0,
            "success_criteria": success_criteria,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.goals.append(new_goal)
        self.save_goals()
        self.bus.emit("goal.created", f"New goal created: {objective}", metadata=new_goal)
        return new_goal

    def update_goal_status(self, goal_id, new_status):
        for g in self.goals:
            if g["goal_id"] == goal_id:
                g["status"] = new_status
                g["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                self.save_goals()
                self.bus.emit("goal.updated", f"Goal {goal_id} status updated to {new_status}", metadata=g)
                return g
        return None

    def list_goals(self):
        return self.goals
