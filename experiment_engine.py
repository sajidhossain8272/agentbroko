import json
import os
import time

class ExperimentEngine:
    def __init__(self, experiment_file="experiments.json"):
        self.experiment_file = experiment_file
        self.experiments = self.load_experiments()

    def load_experiments(self):
        if os.path.exists(self.experiment_file):
            try:
                with open(self.experiment_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "created_at": time.time(),
            "updated_at": time.time(),
            "experiments": [
                {
                    "id": "exp_001",
                    "hypothesis": "Publishing exchange developer API setup guides on m/crypto and m/technology will generate qualified Binance/Bybit clicks and referrals.",
                    "channel": "Affiliate Content",
                    "status": "RUNNING", # RUNNING, COMPLETED, HALTED
                    "impressions": 42,
                    "clicks": 3,
                    "conversions": 0,
                    "revenue_usd": 0.0,
                    "insight": "High initial interest on API developer topics; need to add more code snippets.",
                    "next_action": "Publish V5 API Python snippet comparison."
                },
                {
                    "id": "exp_002",
                    "hypothesis": "Outreach to SMEs offering $50 Website LCP & Speed Diagnosis Reports will produce 20% proposal response rate.",
                    "channel": "Productized Service",
                    "status": "RUNNING",
                    "prospects_contacted": 5,
                    "responses": 1,
                    "conversions": 0,
                    "revenue_usd": 0.0,
                    "insight": "Targeting E-commerce owners yields higher initial open rates.",
                    "next_action": "Refine technical audit proposal template."
                }
            ]
        }

    def save_experiments(self):
        self.experiments["updated_at"] = time.time()
        with open(self.experiment_file, 'w') as f:
            json.dump(self.experiments, f, indent=2)

    def log_experiment_result(self, exp_id, insight, next_action, revenue_usd=0.0):
        for exp in self.experiments["experiments"]:
            if exp["id"] == exp_id:
                exp["insight"] = insight
                exp["next_action"] = next_action
                exp["revenue_usd"] += float(revenue_usd)
                self.save_experiments()
                return exp
        return None

    def get_active_experiments(self):
        return [e for e in self.experiments["experiments"] if e["status"] == "RUNNING"]
