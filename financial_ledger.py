import json
import os
import time

class FinancialLedger:
    def __init__(self, ledger_file="revenue.json"):
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
            "summary": {
                "total_revenue_usd": 0.0,
                "total_expenses_usd": 0.0,
                "net_profit_usd": 0.0
            },
            "revenue_entries": [],
            "expense_entries": []
        }

    def save_ledger(self):
        self.data["updated_at"] = time.time()
        rev = sum(entry.get("amount_usd", 0.0) for entry in self.data["revenue_entries"])
        exp = sum(entry.get("amount_usd", 0.0) for entry in self.data["expense_entries"])
        self.data["summary"]["total_revenue_usd"] = round(rev, 2)
        self.data["summary"]["total_expenses_usd"] = round(exp, 2)
        self.data["summary"]["net_profit_usd"] = round(rev - exp, 2)

        with open(self.ledger_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_revenue(self, source, customer, product, amount_usd, currency="USD", payment_method="EVM", wallet="", tx_id="", verified=True):
        entry = {
            "id": f"rev_{len(self.data['revenue_entries']) + 1}",
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": source.upper(), # SERVICE, PRODUCT, AFFILIATE, SPONSORSHIP, SUBSCRIPTION, OTHER
            "customer": customer,
            "product": product,
            "amount_usd": float(amount_usd),
            "currency": currency,
            "payment_method": payment_method,
            "wallet": wallet,
            "transaction_id": tx_id,
            "verified": verified
        }
        self.data["revenue_entries"].append(entry)
        self.save_ledger()
        return entry

    def record_expense(self, category, description, amount_usd):
        entry = {
            "id": f"exp_{len(self.data['expense_entries']) + 1}",
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "category": category, # API, HOSTING, FEES, ADVERTISING, OPERATING
            "description": description,
            "amount_usd": float(amount_usd)
        }
        self.data["expense_entries"].append(entry)
        self.save_ledger()
        return entry
