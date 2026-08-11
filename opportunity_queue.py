import json
import os
import time

class OpportunityQueue:
    def __init__(self, queue_file="opportunity_queue.json"):
        self.queue_file = queue_file
        self.items = self.load_queue()

    def load_queue(self):
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_queue()

    def save_queue(self):
        with open(self.queue_file, 'w') as f:
            json.dump(self.items, f, indent=2)

    def get_seed_queue(self):
        return [
            {
                "id": "opp_001",
                "source": "SME Market Analysis",
                "problem": "Unoptimized site speed & LCP on SME e-commerce landing pages",
                "customer": "SME E-Commerce Store Owners",
                "solution": "Technical SEO & Speed Optimization Audit Package",
                "estimated_price": 50.0,
                "estimated_cost": 2.0,
                "estimated_profit": 48.0,
                "probability": 0.35,
                "expected_value": 16.8,
                "time_required": 1.5,
                "score": 85.0,
                "status": "validated",
                "next_action": "Execute targeted outreach for speed diagnosis package.",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": "opp_002",
                "source": "Developer Community Research",
                "problem": "Lack of clear V5 Unified API code examples for Bybit/Binance integrations",
                "customer": "Algorithmic Traders & Bot Developers",
                "solution": "Developer API Integration Guide & Affiliate Hub",
                "estimated_price": 150.0,
                "estimated_cost": 1.0,
                "estimated_profit": 149.0,
                "probability": 0.45,
                "expected_value": 67.05,
                "time_required": 2.0,
                "score": 92.0,
                "status": "testing",
                "next_action": "Publish Python V5 API code snippets with Binance & Bybit referral links.",
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    def add_opportunity(self, source, problem, customer, solution, estimated_price, estimated_cost=0.0, probability=0.3, time_required=1.0, score=50.0):
        profit = estimated_price - estimated_cost
        ev = profit * probability
        opp = {
            "id": f"opp_{len(self.items) + 1:03d}",
            "source": source,
            "problem": problem,
            "customer": customer,
            "solution": solution,
            "estimated_price": float(estimated_price),
            "estimated_cost": float(estimated_cost),
            "estimated_profit": float(profit),
            "probability": float(probability),
            "expected_value": round(ev, 2),
            "time_required": float(time_required),
            "score": float(score),
            "status": "new",
            "next_action": "Evaluate market interest",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.items.append(opp)
        self.save_queue()
        return opp

    def update_status(self, opp_id, new_status, next_action=""):
        for item in self.items:
            if item["id"] == opp_id:
                item["status"] = new_status
                if next_action:
                    item["next_action"] = next_action
                item["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                self.save_queue()
                return item
        return None
