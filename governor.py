"""
Governor — the executive guard layer.

Every significant external action must pass through the Governor before execution.
The Governor enforces rate limits, action budgets, Safe Mode, and risk controls.
It returns APPROVED / DEFERRED / REJECTED / REQUIRES_HUMAN_APPROVAL.
"""
import time
import json
import os
import logging
from event_bus import EventBus

class Governor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, state_file="governor_state.json"):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.state_file = state_file
        self.bus = EventBus()
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except Exception:
                pass
        return self._fresh_state()

    def _fresh_state(self):
        return {
            "safe_mode": False,
            "action_counts": {},         # action_type -> count today
            "action_limits": {           # max actions per 24h window
                "moltbook_post": 6,
                "moltbook_comment": 20,
                "moltbook_upvote": 50,
                "github_push": 10,
                "github_create_repo": 2,
                "ai_call_heavy": 40,
                "ai_call_light": 200,
                "experiment_start": 4,
                "external_api_call": 100,
            },
            "cooldowns": {},             # action_type -> ISO timestamp of last execution
            "cooldown_seconds": {
                "moltbook_post": 1800,   # 30 min between posts
                "moltbook_comment": 120, # 2 min between comments
                "moltbook_upvote": 30,   # 30s between upvotes
                "github_create_repo": 86400,  # 1 day
                "experiment_start": 3600,
            },
            "window_reset_at": time.strftime("%Y-%m-%d"),
            "decisions": []
        }

    def _save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=2)
        except Exception:
            pass

    def _reset_daily_counts_if_needed(self):
        today = time.strftime("%Y-%m-%d")
        if self.state.get("window_reset_at") != today:
            self.state["action_counts"] = {}
            self.state["window_reset_at"] = today

    def request_approval(self, action_type, metadata=None, requires_human=False):
        """
        Returns: dict with keys: verdict (APPROVED/DEFERRED/REJECTED/REQUIRES_HUMAN),
                                  reason, action_type
        """
        self._reset_daily_counts_if_needed()
        metadata = metadata or {}
        now = time.time()

        # Safe Mode check
        if self.state["safe_mode"]:
            return self._decision("REJECTED", action_type, "Safe Mode is active — all external actions blocked")

        # Human approval gate for high-risk actions
        high_risk = {"github_create_repo", "financial_transaction", "destructive_git_op"}
        if action_type in high_risk or requires_human:
            return self._decision("REQUIRES_HUMAN_APPROVAL", action_type,
                                  f"Action '{action_type}' requires human approval before execution")

        # Daily count limit
        limit = self.state["action_limits"].get(action_type)
        if limit is not None:
            count = self.state["action_counts"].get(action_type, 0)
            if count >= limit:
                return self._decision("REJECTED", action_type,
                                      f"Daily limit reached: {count}/{limit} '{action_type}' actions today")

        # Cooldown check
        cooldown_secs = self.state["cooldown_seconds"].get(action_type)
        if cooldown_secs:
            last_ts = self.state["cooldowns"].get(action_type, 0)
            elapsed = now - (last_ts if isinstance(last_ts, (int, float)) else 0)
            if elapsed < cooldown_secs:
                wait = int(cooldown_secs - elapsed)
                return self._decision("DEFERRED", action_type,
                                      f"Cooldown active for '{action_type}': {wait}s remaining")

        # Approved — update counts and cooldown
        self.state["action_counts"][action_type] = self.state["action_counts"].get(action_type, 0) + 1
        self.state["cooldowns"][action_type] = now
        self._save_state()
        return self._decision("APPROVED", action_type, "Action within limits and past cooldown")

    def _decision(self, verdict, action_type, reason):
        rec = {
            "verdict": verdict,
            "action_type": action_type,
            "reason": reason,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.state["decisions"] = self.state["decisions"][-50:]
        self.state["decisions"].append(rec)
        self._save_state()

        level = "INFO" if verdict == "APPROVED" else "WARNING"
        self.bus.emit("governor.decision", f"[GOVERNOR] {verdict}: {action_type} — {reason}", level=level)
        return rec

    def enable_safe_mode(self):
        self.state["safe_mode"] = True
        self._save_state()
        self.bus.emit("governor.safe_mode", "Safe Mode ENABLED — external actions blocked")

    def disable_safe_mode(self):
        self.state["safe_mode"] = False
        self._save_state()
        self.bus.emit("governor.safe_mode", "Safe Mode DISABLED — normal operations resumed")

    def set_safe_mode(self, enabled: bool):
        """Unified toggle — called from dashboard API."""
        if enabled:
            self.enable_safe_mode()
        else:
            self.disable_safe_mode()

    def get_status(self):
        self._reset_daily_counts_if_needed()
        return {
            "safe_mode": self.state["safe_mode"],
            "action_counts_today": self.state["action_counts"],
            "action_limits": self.state["action_limits"],
            "cooldown_seconds": self.state.get("cooldown_seconds", {}),
            "recent_decisions": self.state.get("decisions", [])[-10:],
            "window_reset_at": self.state.get("window_reset_at", "")
        }

