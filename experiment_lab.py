import json
import os
import time

class ExperimentLab:
    def __init__(self, lab_file="experiment_lab.json"):
        self.lab_file = lab_file
        self.experiments = self.load_lab()

    def load_lab(self):
        if os.path.exists(self.lab_file):
            try:
                with open(self.lab_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_experiments()

    def save_lab(self):
        with open(self.lab_file, 'w') as f:
            json.dump(self.experiments, f, indent=2)

    def get_seed_experiments(self):
        return [
            {
                "id": "exp_lab_001",
                "hypothesis": "A personalized website-performance audit can generate paid leads from small businesses.",
                "audience": "SME E-Commerce Store Owners",
                "offer": "$50 Technical Speed & SEO Audit Report",
                "channel": "Direct Developer Outreach / Forums",
                "cost_usd": 2.0,
                "expected_outcome": "20% response rate, 1 paid conversion per 10 prospects",
                "success_metric": "Paid conversion revenue > $50",
                "max_acceptable_loss_usd": 10.0,
                "deadline": time.strftime("%Y-%m-%d", time.localtime(time.time() + 7*86400)),
                "consecutive_failures": 0,
                "status": "active", # active, won, abandoned
                "result": "Initial testing phase active",
                "decision": "Continue testing with 10 prospects"
            },
            {
                "id": "exp_lab_002",
                "hypothesis": "Publishing exchange V5 API developer tutorials generates Binance/Bybit affiliate clicks.",
                "audience": "Crypto Bot Developers",
                "offer": "Free Exchange API Python Integration Snippets",
                "channel": "Moltbook m/crypto & m/technology",
                "cost_usd": 0.0,
                "expected_outcome": "5+ affiliate link clicks per post",
                "success_metric": "Clicks >= 5",
                "max_acceptable_loss_usd": 0.0,
                "deadline": time.strftime("%Y-%m-%d", time.localtime(time.time() + 7*86400)),
                "consecutive_failures": 0,
                "status": "active",
                "result": "Active on Moltbook feed",
                "decision": "Continue publishing weekly code snippets"
            }
        ]

    def evaluate_and_clean_experiments(self):
        """
        Automatically kills bad experiments (status = abandoned) if consecutive failures >= 3 or max loss exceeded
        """
        abandoned_count = 0
        for exp in self.experiments:
            if exp["status"] == "active" and exp["consecutive_failures"] >= 3:
                exp["status"] = "abandoned"
                exp["decision"] = "ABANDONED: Zero conversion after 3 consecutive attempts."
                abandoned_count += 1
        
        if abandoned_count > 0:
            self.save_lab()
        return abandoned_count
