import logging
from event_bus import EventBus

class PermissionManager:
    LEVELS = {
        0: "OBSERVE",
        1: "RECOMMEND",
        2: "LOW_RISK_LOCAL",
        3: "EXTERNAL_CONTENT",
        4: "BUSINESS_EXPERIMENTS",
        5: "FINANCIAL_TRANSACTIONS"
    }

    def __init__(self, current_level=3, safe_mode=False):
        self.current_level = current_level
        self.safe_mode = safe_mode
        self.bus = EventBus()

    def set_level(self, level):
        if level in self.LEVELS:
            old = self.current_level
            self.current_level = level
            self.bus.emit("permission.level.changed", f"Permission level set to Level {level} ({self.LEVELS[level]})", metadata={
                "old_level": old,
                "new_level": level
            })
            return True
        return False

    def toggle_safe_mode(self, enabled=True):
        self.safe_mode = enabled
        status = "ENABLED" if enabled else "DISABLED"
        self.bus.emit("permission.safemode.changed", f"Safe Mode {status}", metadata={"safe_mode": enabled})
        return self.safe_mode

    def is_action_allowed(self, required_level=3):
        if self.safe_mode and required_level >= 3:
            return False, "Safe Mode is ENABLED. External mutations blocked."
        if self.current_level < required_level:
            return False, f"Current permission level ({self.LEVELS[self.current_level]}) is below required ({self.LEVELS[required_level]})"
        return True, "Action allowed"
