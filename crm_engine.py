import json
import os
import time

class CRMEngine:
    def __init__(self, crm_file="crm.json"):
        self.crm_file = crm_file
        self.data = self.load_crm()

    def load_crm(self):
        if os.path.exists(self.crm_file):
            try:
                with open(self.crm_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "created_at": time.time(),
            "updated_at": time.time(),
            "leads": [
                {
                    "id": "lead_1",
                    "company": "Apex Digital Solutions",
                    "website": "https://apexdigitalsolutions.tst",
                    "contact": "contact@apexdigitalsolutions.tst",
                    "problem": "Unoptimized LCP & missing schema tags on main landing page",
                    "solution": "Technical SEO & Speed Audit Package",
                    "offered_price_usd": 50.0,
                    "status": "QUALIFIED_PROSPECT", # QUALIFIED_PROSPECT, PROPOSAL_SENT, CUSTOMER_ACQUIRED, REJECTED
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "id": "lead_2",
                    "company": "Nexus Trading Labs",
                    "website": "https://nexustradinglabs.tst",
                    "contact": "dev@nexustradinglabs.tst",
                    "problem": "Need low-latency V5 API endpoint setup for exchange bot",
                    "solution": "Bybit & Binance API Integration Guide & Script",
                    "offered_price_usd": 75.0,
                    "status": "QUALIFIED_PROSPECT",
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }

    def save_crm(self):
        self.data["updated_at"] = time.time()
        with open(self.crm_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_lead(self, company, website, contact, problem, solution, offered_price_usd):
        lead = {
            "id": f"lead_{len(self.data['leads']) + 1}",
            "company": company,
            "website": website,
            "contact": contact,
            "problem": problem,
            "solution": solution,
            "offered_price_usd": float(offered_price_usd),
            "status": "QUALIFIED_PROSPECT",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data["leads"].append(lead)
        self.save_crm()
        return lead

    def update_lead_status(self, lead_id, status):
        for lead in self.data["leads"]:
            if lead["id"] == lead_id:
                lead["status"] = status
                self.save_crm()
                return lead
        return None

    def get_pipeline_summary(self):
        total_leads = len(self.data["leads"])
        active_prospects = [l for l in self.data["leads"] if l["status"] in ["QUALIFIED_PROSPECT", "PROPOSAL_SENT"]]
        acquired_customers = [l for l in self.data["leads"] if l["status"] == "CUSTOMER_ACQUIRED"]
        pipeline_value = sum(l["offered_price_usd"] for l in active_prospects)
        return {
            "total_leads": total_leads,
            "active_prospects": len(active_prospects),
            "acquired_customers": len(acquired_customers),
            "pipeline_value_usd": round(pipeline_value, 2)
        }
