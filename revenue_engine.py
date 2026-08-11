import json
import os
import time
from event_bus import EventBus

class RevenueEngine:
    STRATEGIES = [
        "Software SaaS & Micro-SaaS",
        "Developer Tools & Utilities",
        "Open-Source Sponsorship & Grants",
        "Educational Products & Interactive Guides",
        "B2B Automation & Lead Gen",
        "Data APIs & Reusable Software Templates",
        "Affiliate Marketing (Optional Candidate)"
    ]

    def __init__(self, ledger_file="revenue_ledger.json"):
        self.ledger_file = ledger_file
        self.bus = EventBus()
        self.ledger = self.load_ledger()

    def load_ledger(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_ledger()

    def save_ledger(self):
        try:
            self.ledger["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(self.ledger_file, 'w') as f:
                json.dump(self.ledger, f, indent=2)
        except Exception:
            pass

    def get_seed_ledger(self):
        return {
            "potential_revenue": 2600.0,
            "expected_revenue": 800.0,
            "confirmed_revenue": 0.0,
            "received_revenue": 0.0,
            "expenses": 0.0,
            "net_profit": 0.0,
            "confirmed_transactions": [],
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def record_confirmed_revenue(self, amount, source, tx_id):
        entry = {
            "tx_id": tx_id,
            "amount": float(amount),
            "source": source,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.ledger["confirmed_transactions"].append(entry)
        self.ledger["confirmed_revenue"] += float(amount)
        self.ledger["received_revenue"] += float(amount)
        self.ledger["net_profit"] = self.ledger["confirmed_revenue"] - self.ledger["expenses"]
        self.save_ledger()
        self.bus.emit("revenue.recorded", f"Confirmed Real Revenue: ${amount} via {source}", metadata=entry)
        return entry

    def get_financial_summary(self):
        return {
            "potential_revenue": self.ledger["potential_revenue"],
            "expected_revenue": self.ledger["expected_revenue"],
            "confirmed_revenue": self.ledger["confirmed_revenue"],
            "received_revenue": self.ledger["received_revenue"],
            "expenses": self.ledger["expenses"],
            "net_profit": self.ledger["net_profit"],
            "transaction_count": len(self.ledger["confirmed_transactions"])
        }
