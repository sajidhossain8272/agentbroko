import os
import time
import json
import logging
import threading
from event_bus import EventBus
from task_manager import TaskManager
from goal_manager import GoalManager

class AgentSupervisor:
    def __init__(self, state_file="agent_state.json"):
        self.state_file = state_file
        self.bus = EventBus()
        self.task_mgr = TaskManager()
        self.goal_mgr = GoalManager()
        self.status = "ONLINE" # ONLINE, THINKING, EXECUTING, PAUSED, ERROR
        self.current_task = "Unified Master OS Loop"
        self.current_goal = "Autonomous Education & Open-Source Factory"
        self.start_time = time.time()
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    st = json.load(f)
                    self.status = st.get("status", "ONLINE")
                    self.current_task = st.get("current_task", "Unified Master OS Loop")
                    self.current_goal = st.get("current_goal", "Autonomous Education & Open-Source Factory")
            except Exception:
                pass

    def save_state(self):
        try:
            st = {
                "status": self.status,
                "current_task": self.current_task,
                "current_goal": self.current_goal,
                "uptime_seconds": int(time.time() - self.start_time),
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.state_file, 'w') as f:
                json.dump(st, f, indent=2)
        except Exception:
            pass

    def set_status(self, new_status, task=None, goal=None):
        self.status = new_status
        if task: self.current_task = task
        if goal: self.current_goal = goal
        self.save_state()
        self.bus.emit("agent.status_change", f"Agent status changed to {new_status}", metadata={
            "status": self.status,
            "task": self.current_task,
            "goal": self.current_goal
        })

    def get_status_payload(self):
        uptime_sec = int(time.time() - self.start_time)
        hrs, rem = divmod(uptime_sec, 3600)
        mins, secs = divmod(rem, 60)
        uptime_str = f"{hrs:02d}h {mins:02d}m {secs:02d}s"

        return {
            "agent_id": "agentbroko-v7",
            "status": self.status,
            "current_task": self.current_task,
            "current_goal": self.current_goal,
            "uptime": uptime_str,
            "uptime_seconds": uptime_sec,
            "active_workers": 1,
            "queue_size": len([t for t in self.task_mgr.list_tasks() if t["status"] == "QUEUED"]),
            "health": "HEALTHY" if self.status != "ERROR" else "DEGRADED",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def emit_heartbeat(self):
        payload = self.get_status_payload()
        self.bus.emit("system.health", f"Heartbeat check | Health: {payload['health']}", metadata=payload)
        return payload
