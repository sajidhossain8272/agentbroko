import json
import os
import time

class OpportunityEngine:
    def __init__(self, memory_file="opportunity_memory.json"):
        self.memory_file = memory_file
        self.opportunities = self.load_opportunities()

    def load_opportunities(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_opportunities()

    def save_opportunities(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.opportunities, f, indent=2)

    @staticmethod
    def calculate_priority_score(opp):
        """
        Score = (Revenue * Probability * Speed * Repeatability) / (Cost * Risk * Time)
        """
        rev = opp.get('revenue_potential', 10.0)
        prob = opp.get('probability', 0.5)
        speed = opp.get('speed', 5.0) # 1-10 scale
        repeatability = opp.get('repeatability', 5.0) # 1-10 scale
        
        cost = max(opp.get('cost', 1.0), 0.1)
        risk = max(opp.get('risk', 1.0), 0.1)
        time_est = max(opp.get('time_hours', 1.0), 0.1)

        numerator = rev * prob * speed * repeatability
        denominator = cost * risk * time_est
        return round(numerator / denominator, 2)

    def get_seed_opportunities(self):
        seed = [
            {
                "id": "opp_001",
                "title": "Technical Performance Audit for E-Commerce SMEs",
                "customer_segment": "SME E-Commerce Store Owners",
                "problem": "Slow page load times (LCP > 3.5s) reducing sales conversions.",
                "solution": "Automated PageSpeed & SEO performance audit report + optimization recommendations.",
                "revenue_potential": 75.0,
                "probability": 0.35,
                "speed": 8.0,
                "repeatability": 9.0,
                "cost": 2.0,
                "risk": 1.0,
                "time_hours": 1.5,
                "channel": "Direct Prospect Outreach / Developer Networks"
            },
            {
                "id": "opp_002",
                "title": "Binance & Bybit Developer API Integration Content Engine",
                "customer_segment": "Crypto Traders & Bot Developers",
                "problem": "Complex exchange V5 API migration and rate limit setup.",
                "solution": "In-depth code tutorials and developer tools featuring Binance and Bybit referral links.",
                "revenue_potential": 150.0,
                "probability": 0.25,
                "speed": 7.0,
                "repeatability": 8.0,
                "cost": 1.0,
                "risk": 1.0,
                "time_hours": 2.0,
                "channel": "Moltbook / Tech Blogs / Developer Forums"
            },
            {
                "id": "opp_003",
                "title": "Custom Web3 RPC & EVM Wallet Setup Service",
                "customer_segment": "Web3 Startup Founders",
                "problem": "Lack of in-house expertise for multi-chain wallet & RPC integration.",
                "solution": "Turnkey Python/JS EVM wallet monitoring script setup.",
                "revenue_potential": 120.0,
                "probability": 0.30,
                "speed": 6.0,
                "repeatability": 7.0,
                "cost": 2.0,
                "risk": 1.5,
                "time_hours": 2.5,
                "channel": "Moltbook / Freelance Inquiries"
            }
        ]

        for opp in seed:
            opp['score'] = self.calculate_priority_score(opp)
        
        seed.sort(key=lambda x: x['score'], reverse=True)
        return seed

    def discover_opportunities(self):
        for opp in self.opportunities:
            opp['score'] = self.calculate_priority_score(opp)
        self.opportunities.sort(key=lambda x: x['score'], reverse=True)
        self.save_opportunities()
        return self.opportunities

    def get_top_opportunity(self):
        opps = self.discover_opportunities()
        return opps[0] if opps else None
