import time
import logging

class HealthMonitor:
    def __init__(self, max_consecutive_repeats=3):
        self.max_consecutive_repeats = max_consecutive_repeats
        self.action_history = []
        self.errors = []

    def record_action(self, action_key):
        self.action_history.append({"action": action_key, "time": time.time()})
        if len(self.action_history) > 20:
            self.action_history.pop(0)

    def is_looping(self, action_key):
        """
        Detects anti-loop violation: if identical action repeats > max_consecutive_repeats times continuously
        """
        recent = [item["action"] for item in self.action_history[-self.max_consecutive_repeats:]]
        if len(recent) >= self.max_consecutive_repeats and all(a == action_key for a in recent):
            logging.warning(f"Anti-Loop Protection Triggered: Action '{action_key}' repeated {self.max_consecutive_repeats} times.")
            return True
        return False

    def record_error(self, error_msg):
        self.errors.append({"error": str(error_msg), "time": time.strftime("%Y-%m-%d %H:%M:%S")})
        if len(self.errors) > 50:
            self.errors.pop(0)
        logging.error(f"HealthMonitor logged error: {error_msg}")

    def get_health_status(self):
        return {
            "status": "HEALTHY" if len(self.errors) < 5 else "DEGRADED",
            "recent_error_count": len(self.errors),
            "recent_actions_tracked": len(self.action_history)
        }
