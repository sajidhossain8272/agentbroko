import json
import os
import time

class AgentMemory:
    def __init__(self, memory_file="agent_memory.json"):
        self.memory_file = memory_file
        self.data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "episodic_memory": [],
            "semantic_memory": [
                "Bitcoin is a decentralized peer-to-peer digital currency.",
                "EVM compatibility enables standard Solidity deployments across Base, Polygon, and Arbitrum.",
                "Never expose or commit seed phrases, private keys, or GitHub tokens."
            ],
            "project_memory": [
                {
                    "name": "agentbroko",
                    "repo": "agentbroko/agentbroko",
                    "status": "DEVELOPMENT",
                    "stack": "Python 3.14 / Unified OS Architecture"
                }
            ],
            "technical_memory": {
                "ci_build_status": "SUCCESS",
                "test_suite_pass_rate": "100%",
                "github_mode": "LIVE"
            },
            "business_memory": {
                "proven_offers": ["SME PageSpeed Audit", "Exchange API Integration Suite"],
                "best_channel": "Moltbook m/crypto & m/technology"
            },
            "failure_memory": [],
            "strategy_memory": {
                "primary_mission": "Autonomous Blockchain Education, Open-Source Software Factory & Community Funding",
                "north_star_metric": "Educational Value & Code Quality Created"
            },
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def save_memory(self):
        self.data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.memory_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_event(self, category, event_data):
        if category in self.data and isinstance(self.data[category], list):
            self.data[category].append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": event_data
            })
            if len(self.data[category]) > 100:
                self.data[category].pop(0)
            self.save_memory()

    def log_failure(self, task, root_cause, lesson):
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "task": task,
            "root_cause": root_cause,
            "lesson": lesson
        }
        self.data["failure_memory"].append(entry)
        self.save_memory()
        return entry
