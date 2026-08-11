import logging
import time
from event_bus import EventBus

class MasterStateMachine:
    STATES = [
        "STARTING", "OBSERVING", "PLANNING", "SELECTING",
        "EXECUTING", "VERIFYING", "LEARNING", "WAITING",
        "PAUSED", "RECOVERING", "ERROR", "STOPPING", "STOPPED"
    ]

    def __init__(self, initial_state="STARTING"):
        self.state = initial_state if initial_state in self.STATES else "STARTING"
        self.bus = EventBus()

    def transition_to(self, new_state, reason=None):
        if new_state not in self.STATES:
            logging.warning(f"[STATE MACHINE] Invalid state transition target: '{new_state}'")
            return self.state

        old_state = self.state
        self.state = new_state

        msg = f"State transition: {old_state} -> {new_state}"
        if reason:
            msg += f" ({reason})"

        logging.info(f"[STATE MACHINE] {msg}")
        self.bus.emit("agent.state.changed", msg, metadata={
            "old_state": old_state,
            "new_state": new_state,
            "reason": reason
        })
        return self.state

    def get_state(self):
        return self.state
