import json
import os
import time

class TaskQueue:
    def __init__(self, queue_file="task_queue.json"):
        self.queue_file = queue_file
        self.tasks = self.load_queue()

    def load_queue(self):
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_tasks()

    def save_queue(self):
        with open(self.queue_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def get_seed_tasks(self):
        return [
            {
                "task_id": "task_001",
                "type": "moltbook_publish_lesson",
                "title": "Publish Level 1 Educational Lesson on Bitcoin & Proof of Work",
                "priority": 0.95,
                "status": "queued",
                "payload": {"level": "level_1", "submolt": "crypto"},
                "retry_count": 0,
                "max_retries": 3,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "task_id": "task_002",
                "type": "github_inspect_and_pr",
                "title": "Inspect agentbroko/agentbroko repository and create V7 release PR",
                "priority": 0.90,
                "status": "queued",
                "payload": {"repo": "agentbroko/agentbroko", "branch": "feature/v7-release"},
                "retry_count": 0,
                "max_retries": 3,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    def add_task(self, task_type, title, priority=0.8, payload=None):
        task = {
            "task_id": f"task_{len(self.tasks) + 1:03d}",
            "type": task_type,
            "title": title,
            "priority": float(priority),
            "status": "queued",
            "payload": payload or {},
            "retry_count": 0,
            "max_retries": 3,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_queue()
        return task

    def pop_highest_priority_task(self):
        queued_tasks = [t for t in self.tasks if t["status"] == "queued"]
        if not queued_tasks:
            return None
        queued_tasks.sort(key=lambda x: x["priority"], reverse=True)
        selected = queued_tasks[0]
        selected["status"] = "in_progress"
        self.save_queue()
        return selected

    def mark_completed(self, task_id, result="Completed"):
        for t in self.tasks:
            if t["task_id"] == task_id:
                t["status"] = "completed"
                t["result"] = result
                t["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                self.save_queue()
                return t
        return None
