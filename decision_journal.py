import json
import os
import time

class DecisionJournal:
    def __init__(self, journal_file="decision_journal.json"):
        self.journal_file = journal_file
        self.entries = self.load_journal()

    def load_journal(self):
        if os.path.exists(self.journal_file):
            try:
                with open(self.journal_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def save_journal(self):
        with open(self.journal_file, 'w') as f:
            json.dump(self.entries, f, indent=2)

    def log_decision(self, decision_text, alternatives, selected, reason, expected_value, risk=1.0, result="", lesson=""):
        entry = {
            "id": f"dec_{len(self.entries) + 1:04d}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "decision": decision_text,
            "alternatives": alternatives,
            "selected": selected,
            "reason": reason,
            "expected_value": float(expected_value),
            "risk": float(risk),
            "result": result,
            "lesson": lesson
        }
        self.entries.append(entry)
        self.save_journal()
        return entry
