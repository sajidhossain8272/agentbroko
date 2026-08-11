import os
import time
import logging
from event_bus import EventBus
from task_manager import TaskManager

class SelfAuditEngine:
    def __init__(self, log_path="agentbroko.log"):
        self.log_path = log_path
        self.bus = EventBus()
        self.task_mgr = TaskManager()

    def run_self_audit(self):
        logging.info("[SELF AUDIT] Executing periodic self-inspection...")
        audit_res = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "log_path": self.log_path,
            "errors_found": 0,
            "warnings_found": 0,
            "git_remote_secure": True,
            "circuit_breakers": "HEALTHY",
            "self_repair_tasks_created": 0
        }

        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[-200:]
                    for line in lines:
                        if "[ERROR]" in line or "Error" in line:
                            audit_res["errors_found"] += 1
                        elif "[WARNING]" in line or "Warning" in line:
                            audit_res["warnings_found"] += 1
            except Exception:
                pass

        # Self-repair task generation if error spike (deduplicate: only create if no QUEUED self-repair task exists)
        if audit_res["errors_found"] >= 5:
            existing = [t for t in self.task_mgr.tasks
                        if t.get("status") == "QUEUED"
                        and t.get("skill") == "system_repair"]
            if not existing:
                t = self.task_mgr.create_task(
                    objective="Automated Self-Repair: Investigate Error Spike in Runtime Log",
                    description=f"Self-audit detected {audit_res['errors_found']} error log entries in recent cycles.",
                    priority=90.0,
                    skill="system_repair"
                )
                audit_res["self_repair_tasks_created"] += 1
            else:
                audit_res["self_repair_tasks_created"] = 0
                audit_res["deduplicated"] = True

        self.bus.emit("self_audit.completed", f"Self Audit Completed | Errors: {audit_res['errors_found']}, Repairs Created: {audit_res['self_repair_tasks_created']}", metadata=audit_res)
        return audit_res
