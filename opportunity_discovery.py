import json
import os
import time
from event_bus import EventBus

class OpportunityDiscoveryEngine:
    def __init__(self, opp_file="discovered_opportunities.json"):
        self.opp_file = opp_file
        self.bus = EventBus()
        self.opportunities = self.load_opportunities()

    def load_opportunities(self):
        if os.path.exists(self.opp_file):
            try:
                with open(self.opp_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.discover_seed_opportunities()

    def save_opportunities(self):
        try:
            with open(self.opp_file, 'w') as f:
                json.dump(self.opportunities, f, indent=2)
        except Exception:
            pass

    def discover_seed_opportunities(self):
        return [
            {
                "opportunity_id": "opp_101",
                "name": "Web3 Developer Security Audit CLI & SDK",
                "category": "developer_tools",
                "problem": "Smart contract developers need automated local diff & secret scanning CLI tools before committing.",
                "proposed_solution": "Open-source Python CLI with optional premium team dashboard.",
                "estimated_revenue": 500.0,
                "estimated_cost": 20.0,
                "time_to_first_revenue_days": 7,
                "confidence": 0.88,
                "evidence_score": 8.5,
                "risk": 0.15,
                "platform_dependency": 0.10,
                "scalability": 9.0,
                "status": "VALIDATED",
                "discovered_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "opportunity_id": "opp_102",
                "name": "Autonomous B2B RPC Monitoring & Alerting Service",
                "category": "micro_saas",
                "problem": "Crypto dApps experience undetected RPC node outages.",
                "proposed_solution": "Automated uptime monitor with Webhook/Telegram alerts.",
                "estimated_revenue": 1200.0,
                "estimated_cost": 50.0,
                "time_to_first_revenue_days": 14,
                "confidence": 0.82,
                "evidence_score": 7.8,
                "risk": 0.20,
                "platform_dependency": 0.15,
                "scalability": 9.5,
                "status": "DISCOVERED",
                "discovered_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "opportunity_id": "opp_103",
                "name": "Interactive Bitcoin & EVM Security Curriculum",
                "category": "educational_products",
                "problem": "New Web3 users require clear non-promotional security guides.",
                "proposed_solution": "Open-source 5-level curriculum supported by voluntary community tips.",
                "estimated_revenue": 300.0,
                "estimated_cost": 0.0,
                "time_to_first_revenue_days": 3,
                "confidence": 0.95,
                "evidence_score": 9.0,
                "risk": 0.05,
                "platform_dependency": 0.20,
                "scalability": 8.5,
                "status": "VALIDATED",
                "discovered_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    def discover_new_opportunity(self, name, category, problem, solution, est_rev=400.0, est_cost=10.0, confidence=0.8, evidence_score=7.0):
        opp_id = f"opp_{len(self.opportunities) + 101:03d}"
        opp = {
            "opportunity_id": opp_id,
            "name": name,
            "category": category,
            "problem": problem,
            "proposed_solution": solution,
            "estimated_revenue": float(est_rev),
            "estimated_cost": float(est_cost),
            "time_to_first_revenue_days": 7,
            "confidence": float(confidence),
            "evidence_score": float(evidence_score),
            "risk": 0.15,
            "platform_dependency": 0.10,
            "scalability": 8.5,
            "status": "DISCOVERED",
            "discovered_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.opportunities.append(opp)
        self.save_opportunities()
        self.bus.emit("opportunity.discovered", f"Discovered new opportunity #{opp_id}: {name}", metadata=opp)
        return opp

    def list_opportunities(self):
        return self.opportunities
