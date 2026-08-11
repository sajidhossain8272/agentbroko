import os
import sys
import time
import json
import logging

class AutonomousScheduler:
    RAPID_MONITOR = 60         # Speed 1: 60 seconds (lightweight notifications & health)
    BUSINESS_CYCLE = 300       # Speed 2: 300 seconds / 5 minutes (main thinking loop)
    DEEP_RESEARCH = 1800       # Speed 3: 1800 seconds / 30 minutes (market & content research)
    STRATEGIC_REVIEW = 7200    # Speed 4: 7200 seconds / 2 hours (strategic review)
    DAILY_REVIEW = 86400       # Daily review: 24 hours

    def __init__(self, lock_file="agentbroko.lock", heartbeat_file="heartbeat.json", state_file="agent_state.json"):
        self.lock_file = lock_file
        self.heartbeat_file = heartbeat_file
        self.state_file = state_file
        self.pid = os.getpid()
        self.acquire_lock()

    def acquire_lock(self):
        """
        Singleton process lock: ensures exactly ONE instance of AgentBroko runner can run.
        """
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, 'r') as f:
                    lock_data = json.load(f)
                    old_pid = lock_data.get('pid')
                    # Check if old process is still alive on Windows
                    if old_pid and old_pid != self.pid and self.is_pid_alive(old_pid):
                        logging.error(f"Singleton Lock Error: Runner PID {old_pid} is already active!")
                        print(f"❌ [LOCK ERROR] AgentBroko instance PID {old_pid} is already running. Exiting duplicate instance.")
                        sys.exit(0)
            except Exception:
                pass

        # Write lock file
        lock_info = {
            "pid": self.pid,
            "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "heartbeat": time.strftime("%Y-%m-%d %H:%M:%S"),
            "version": "v4"
        }
        with open(self.lock_file, 'w') as f:
            json.dump(lock_info, f, indent=2)

    @staticmethod
    def is_pid_alive(pid):
        import subprocess
        try:
            output = subprocess.check_output(f"tasklist /FI \"PID eq {pid}\"", shell=True).decode()
            return str(pid) in output
        except Exception:
            return False

    def update_heartbeat(self, last_cycle_type="business"):
        now = time.time()
        hb_data = {
            "status": "running",
            "version": "v4",
            "pid": self.pid,
            "last_cycle": time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_cycle_type": last_cycle_type,
            "next_business_cycle": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now + self.BUSINESS_CYCLE)),
            "next_deep_research": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now + self.DEEP_RESEARCH)),
            "next_strategic_review": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now + self.STRATEGIC_REVIEW))
        }
        with open(self.heartbeat_file, 'w') as f:
            json.dump(hb_data, f, indent=2)

        # Also refresh lock heartbeat timestamp
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, 'r') as f:
                    lock_info = json.load(f)
                lock_info["heartbeat"] = time.strftime("%Y-%m-%d %H:%M:%S")
                with open(self.lock_file, 'w') as f:
                    json.dump(lock_info, f, indent=2)
            except Exception:
                pass

    def set_agent_state(self, goal, task, opportunity, reason, expected_result, status="ACTIVE"):
        state_data = {
            "current_goal": goal,
            "current_task": task,
            "current_opportunity": opportunity,
            "reason": reason,
            "expected_result": expected_result,
            "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": status
        }
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=2)

    def release_lock(self):
        if os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
            except Exception:
                pass
