import json
import os
import time

class FundingLedger:
    def __init__(self, ledger_file="funding_ledger.json"):
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
            "summary": {
                "total_affiliate_revenue_usd": 0.0,
                "total_donations_usd": 0.0,
                "total_operating_costs_usd": 0.0,
                "net_funding_usd": 0.0,
                "educational_resources_published": 14,
                "questions_answered": 42
            },
            "transactions": []
        }

    def save_ledger(self):
        with open(self.ledger_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_entry(self, category, amount_usd, description, tx_id="", network=""):
        entry = {
            "id": f"ftx_{len(self.data['transactions']) + 1:04d}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "category": category, # affiliate_revenue, donation, operating_cost
            "amount_usd": float(amount_usd),
            "description": description,
            "tx_id": tx_id,
            "network": network
        }
        self.data["transactions"].append(entry)

        if category == "affiliate_revenue":
            self.data["summary"]["total_affiliate_revenue_usd"] += amount_usd
        elif category == "donation":
            self.data["summary"]["total_donations_usd"] += amount_usd
        elif category == "operating_cost":
            self.data["summary"]["total_operating_costs_usd"] += amount_usd

        self.data["summary"]["net_funding_usd"] = (
            self.data["summary"]["total_affiliate_revenue_usd"] +
            self.data["summary"]["total_donations_usd"] -
            self.data["summary"]["total_operating_costs_usd"]
        )
        self.save_ledger()
        return entry
