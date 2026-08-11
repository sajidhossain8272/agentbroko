import json
import os
import time

class BusinessIntelligenceMemory:
    def __init__(self, intel_file="business_intelligence.json"):
        self.intel_file = intel_file
        self.data = self.load_intel()

    def load_intel(self):
        if os.path.exists(self.intel_file):
            try:
                with open(self.intel_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_intel()

    def save_intel(self):
        try:
            self.data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(self.intel_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def get_seed_intel(self):
        return {
            "proven_strategies": [
                "Open-Source Developer Security Tooling (Zero Spam)",
                "Answer-First Educational Curriculum & Voluntary Donations",
                "Self-Healing Multi-Chain Treasury Sync"
            ],
            "failed_strategies": [
                {
                    "strategy": "Repeated Affiliate Link Insertion in Social Feed Posts",
                    "root_cause": "Community platform automated spam filter classified referral URLs as 🚫 Spam",
                    "lesson": "Drop hard-coded affiliate links completely. Focus on value-first educational content and reusable software tools.",
                    "date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            ],
            "revenue_by_channel": {
                "voluntary_donations": 0.0,
                "affiliate": 0.0,
                "software_licensing": 0.0
            },
            "discovered_customer_problems": [
                "Developers need local secret scanning before committing private keys or API tokens.",
                "Web3 users need non-promotional educational guides on public/private keys and seed phrases."
            ],
            "reusable_assets": [
                "SecurityEngine Python Diff Scanner",
                "GitHubEngine REST API Integration",
                "Moltbook Verification Challenge Solver",
                "Real-Time Web UI Control Center"
            ],
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def record_failed_strategy(self, strategy, root_cause, lesson):
        entry = {
            "strategy": strategy,
            "root_cause": root_cause,
            "lesson": lesson,
            "date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data["failed_strategies"].append(entry)
        self.save_intel()
        return entry
