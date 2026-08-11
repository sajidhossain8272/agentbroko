import json
import os
import time

class RevenueLedger:
    def __init__(self, ledger_file="financial_ledger.json"):
        self.ledger_file = ledger_file
        self.data = self.load_ledger()

    def load_ledger(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "created_at": time.time(),
            "updated_at": time.time(),
            "ledger": [
                {
                    "channel": "affiliate",
                    "partner": "Binance",
                    "revenue": 0.0,
                    "clicks": 0,
                    "registrations": 0,
                    "qualified_referrals": 0,
                    "impressions": 0,
                    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "channel": "affiliate",
                    "partner": "Bybit",
                    "revenue": 0.0,
                    "clicks": 0,
                    "registrations": 0,
                    "qualified_referrals": 0,
                    "impressions": 0,
                    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }

    def save_ledger(self):
        self.data["updated_at"] = time.time()
        with open(self.ledger_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_impression(self, partner_name):
        for item in self.data["ledger"]:
            if item["partner"].lower() == partner_name.lower():
                item["impressions"] += 1
                item["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_ledger()

    def record_click(self, partner_name):
        for item in self.data["ledger"]:
            if item["partner"].lower() == partner_name.lower():
                item["clicks"] += 1
                item["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_ledger()

    def record_revenue(self, partner_name, amount, registrations=0, qualified=0):
        for item in self.data["ledger"]:
            if item["partner"].lower() == partner_name.lower():
                item["revenue"] += float(amount)
                item["registrations"] += int(registrations)
                item["qualified_referrals"] += int(qualified)
                item["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_ledger()
