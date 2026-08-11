import json
import os
import time

class RepositoryMap:
    def __init__(self, map_file="repository_map.json"):
        self.map_file = map_file
        self.data = self.load_map()

    def load_map(self):
        if os.path.exists(self.map_file):
            try:
                with open(self.map_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_map()

    def save_map(self):
        with open(self.map_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_seed_map(self):
        return {
            "repository": "agentbroko/agentbroko",
            "url": "https://github.com/agentbroko/agentbroko",
            "language": "Python 3.14",
            "framework": "AgentBroko V7 Autonomous Business OS",
            "default_branch": "main",
            "last_commit": "v7.0.0-release",
            "open_issues": 2,
            "open_prs": 1,
            "ci_status": "SUCCESS",
            "deployment": "24/7 Autonomous Scheduler (task-735)",
            "health": "HEALTHY",
            "core_modules": [
                "autonomous_scheduler.py",
                "decision_engine.py",
                "education_engine.py",
                "audience_engine.py",
                "github_engine.py",
                "security_engine.py"
            ],
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def update_map(self, open_issues=None, open_prs=None, ci_status=None):
        if open_issues is not None: self.data["open_issues"] = open_issues
        if open_prs is not None: self.data["open_prs"] = open_prs
        if ci_status is not None: self.data["ci_status"] = ci_status
        self.data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_map()
        return self.data
