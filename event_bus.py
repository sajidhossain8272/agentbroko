import json
import os
import time
import logging
import threading

class EventBus:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, history_file="event_history.json"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance.history_file = history_file
                cls._instance.subscribers = []
                cls._instance.events = cls._instance.load_history()
            return cls._instance

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.events[-500:], f, indent=2)
        except Exception:
            pass

    def subscribe(self, callback):
        if callback not in self.subscribers:
            self.subscribers.append(callback)

    def unsubscribe(self, callback):
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    def emit(self, event_type, message, metadata=None, skill=None, task_id=None, level="INFO"):
        event_payload = {
            "id": f"evt_{len(self.events) + 1:05d}",
            "event": event_type,
            "level": level,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "agent_id": "agentbroko-v7",
            "task_id": task_id,
            "skill": skill,
            "message": message,
            "metadata": metadata or {}
        }

        self.events.append(event_payload)
        if len(self.events) > 500:
            self.events.pop(0)

        self.save_history()
        logging.info(f"[{event_type.upper()}] {message}")

        # Broadcast to all live subscribers (WebSockets / Web UI gateway)
        for cb in list(self.subscribers):
            try:
                cb(event_payload)
            except Exception as e:
                logging.warning(f"Error notifying event subscriber: {e}")

        return event_payload

    def get_recent_events(self, limit=100):
        return self.events[-limit:]
