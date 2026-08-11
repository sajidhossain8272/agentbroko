import json
import os
import time

class StrategyMemory:
    def __init__(self, memory_file="strategy_memory.json"):
        self.memory_file = memory_file
        self.data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_memory()

    def save_memory(self):
        try:
            self.data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(self.memory_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def get_seed_memory(self):
        return {
            "proven_patterns": [
                {
                    "strategy": "Open-Source Value-First Tooling & Education",
                    "context": "Moltbook community engagement",
                    "result": "High trust, zero platform spam flags",
                    "confidence": 0.95
                }
            ],
            "failed_patterns": [
                {
                    "strategy": "Repeated Hard-coded Affiliate Link Insertion",
                    "context": "Feed posts & CTAs",
                    "result": "Flagged as spam by community filters",
                    "lesson": "Drop affiliate links completely. Focus on value-first technical guides.",
                    "date": time.strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "strategy": "Blind Random Project Creation Without Evidence",
                    "context": "Repository creation",
                    "result": "Resource waste without validated user demand",
                    "lesson": "Require NewProjectGate proposal validation before creating new repos.",
                    "date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            ],
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def is_failed_pattern(self, strategy_description):
        desc_lower = strategy_description.lower()
        for fp in self.data["failed_patterns"]:
            if fp["strategy"].lower() in desc_lower or desc_lower in fp["strategy"].lower():
                return True, fp["lesson"]
        return False, None

    def record_strategy_result(self, strategy, context, success, result_summary, lesson=None):
        entry = {
            "strategy": strategy,
            "context": context,
            "result": result_summary,
            "date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        if success:
            entry["confidence"] = 0.90
            self.data["proven_patterns"].append(entry)
        else:
            entry["lesson"] = lesson or "Avoid repeating unvalidated approach"
            self.data["failed_patterns"].append(entry)
        self.save_memory()
        return entry
