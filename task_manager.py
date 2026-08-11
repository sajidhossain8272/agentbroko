import json
import os
import time
from event_bus import EventBus

class TaskManager:
    def __init__(self, tasks_file="kanban_tasks.json"):
        self.tasks_file = tasks_file
        self.bus = EventBus()
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_tasks()

    def save_tasks(self):
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception:
            pass

    def get_seed_tasks(self):
        return [
            {
                "id": "task_101",
                "goal_id": "goal_001",
                "objective": "Publish Educational Lesson & Verification",
                "description": "Generate Level 1 Bitcoin education post and verify publication on Moltbook",
                "priority": 92.5,
                "status": "COMPLETED",
                "skill": "social_skill",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "attempt_count": 1,
                "max_attempts": 3,
                "verification_result": "PASSED (Post ID: 524786a9-432c-457b-8cb2-6e4da5f465af)"
            },
            {
                "id": "task_102",
                "goal_id": "goal_001",
                "objective": "Inspect agentbroko/agentbroko GitHub Repository",
                "description": "Continuous CI status check & security diff scanning",
                "priority": 88.0,
                "status": "RUNNING",
                "skill": "github_code_agent",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "attempt_count": 1,
                "max_attempts": 3,
                "verification_result": "IN_PROGRESS"
            },
            {
                "id": "task_103",
                "goal_id": "goal_002",
                "objective": "Serve Real-Time Web Control Center UI",
                "priority": 95.0,
                "status": "RUNNING",
                "skill": "control_center_skill",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "attempt_count": 1,
                "max_attempts": 3,
                "verification_result": "IN_PROGRESS"
            }
        ]

    @staticmethod
    def calculate_priority(goal_val=50.0, urgency=10.0, impact=15.0, dep_weight=5.0, success_prob=0.9, cost=1.0, risk=1.0):
        score = goal_val + urgency + impact + dep_weight + (success_prob * 20.0) - cost - risk
        return round(max(score, 1.0), 2)

    def create_task(self, objective, description, goal_id="goal_001", skill="general", priority=75.0):
        task_id = f"task_{len(self.tasks) + 101:03d}"
        new_task = {
            "id": task_id,
            "goal_id": goal_id,
            "objective": objective,
            "description": description,
            "priority": float(priority),
            "status": "QUEUED",
            "skill": skill,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "attempt_count": 0,
            "max_attempts": 3,
            "verification_result": "PENDING"
        }
        self.tasks.append(new_task)
        self.save_tasks()
        self.bus.emit("task.created", f"Created task #{task_id}: {objective}", metadata=new_task, skill=skill, task_id=task_id)
        return new_task

    def update_task_status(self, task_id, status, error=None, verification_result=None):
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = status
                if status == "RUNNING" and "started_at" not in t:
                    t["started_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                elif status in ["COMPLETED", "FAILED", "BLOCKED"]:
                    t["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                
                if error:
                    t["error"] = error
                if verification_result:
                    t["verification_result"] = verification_result

                self.save_tasks()
                self.bus.emit(f"task.{status.lower()}", f"Task #{task_id} transitioned to {status}", metadata=t, skill=t.get("skill"), task_id=task_id)
                return t
        return None

    def list_tasks(self):
        return self.tasks
