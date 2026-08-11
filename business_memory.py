import json
import os
import time

class BusinessMemory:
    def __init__(self, memory_file="business_memory.json"):
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
            "created_at": time.time(),
            "customer_insights": {
                "what_customers_want": [
                    "Fast page load times (LCP < 2.5s)",
                    "Simple, clear exchange V5 API code examples"
                ],
                "what_customers_reject": [
                    "Generic high-pressure sales pitches",
                    "Unsubstantiated profit claims"
                ]
            },
            "pricing_insights": {
                "working_prices": ["$50 for Technical Speed Audit", "$100 for API Integration Package"],
                "rejected_prices": []
            },
            "channel_performance": {
                "high_converting_channels": ["Moltbook m/crypto", "Moltbook m/technology"],
                "low_converting_channels": []
            },
            "proven_services": [
                "E-Commerce Technical Performance Audit",
                "Exchange API Developer Code Integration"
            ],
            "dead_end_markets": []
        }

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_learning(self, category, item):
        if category in self.data and isinstance(self.data[category], list):
            if item not in self.data[category]:
                self.data[category].append(item)
                self.save_memory()
