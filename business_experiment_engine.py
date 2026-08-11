import json
import os
import time
from event_bus import EventBus

class BusinessExperimentEngine:
    def __init__(self, exp_file="business_experiments.json"):
        self.exp_file = exp_file
        self.bus = EventBus()
        self.experiments = self.load_experiments()

    def load_experiments(self):
        if os.path.exists(self.exp_file):
            try:
                with open(self.exp_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_experiments()

    def save_experiments(self):
        try:
            with open(self.exp_file, 'w') as f:
                json.dump(self.experiments, f, indent=2)
        except Exception:
            pass

    def get_seed_experiments(self):
        return [
            {
                "experiment_id": "exp_101",
                "opportunity_id": "opp_101",
                "hypothesis": "Providing open-source Python diff scanning CLI tool builds developer trust and drives GitHub stargazers.",
                "strategy": "Open-Source Value First (Zero Affiliate Spam)",
                "status": "RUNNING",
                "success_metric": "GitHub Stargazers & Issue Feedback",
                "target_threshold": 10,
                "actual_result": 14,
                "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "decision": "KEEP"
            },
            {
                "experiment_id": "exp_102",
                "opportunity_id": "opp_103",
                "hypothesis": "Pure non-promotional Web3 security tutorials avoid platform spam flags and receive higher community upvotes.",
                "strategy": "Answer-First Educational Curriculum",
                "status": "COMPLETED",
                "success_metric": "Moltbook Post Approval & Karma",
                "target_threshold": 1,
                "actual_result": 1,
                "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "decision": "KEEP"
            }
        ]

    def create_experiment(self, opp_id, hypothesis, strategy, metric, target_val):
        exp_id = f"exp_{len(self.experiments) + 101:03d}"
        exp = {
            "experiment_id": exp_id,
            "opportunity_id": opp_id,
            "hypothesis": hypothesis,
            "strategy": strategy,
            "status": "RUNNING",
            "success_metric": metric,
            "target_threshold": target_val,
            "actual_result": 0,
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "decision": "PENDING"
        }
        self.experiments.append(exp)
        self.save_experiments()
        self.bus.emit("experiment.started", f"Started Business Experiment #{exp_id}: {hypothesis[:40]}...", metadata=exp)
        return exp

    def complete_experiment(self, exp_id, actual_val, decision="KEEP"):
        for e in self.experiments:
            if e["experiment_id"] == exp_id:
                e["status"] = "COMPLETED"
                e["actual_result"] = actual_val
                e["decision"] = decision
                e["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                self.save_experiments()
                self.bus.emit("experiment.completed", f"Experiment #{exp_id} completed | Decision: {decision}", metadata=e)
                return e
        return None

    def list_experiments(self):
        return self.experiments
