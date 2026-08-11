import json
import time
from opportunity_queue import OpportunityQueue

class DecisionEngine:
    def __init__(self):
        self.opp_queue = OpportunityQueue()

    @staticmethod
    def calculate_0_100_score(opp):
        """
        Comprehensive 0-100 Economic Opportunity Scoring Model:
        + Revenue Potential (0-20)
        + Probability of Success (0-20)
        + Speed to Revenue (0-15)
        + Customer Demand (0-15)
        + Repeatability (0-10)
        + Scalability (0-10)
        + Learning Value (0-5)
        + Strategic Value (0-5)
        - Risk (0-10)
        - Cost (0-10)
        """
        # Extract or set default ratings (scaled 0-10 or normalized)
        rev_pot = min(opp.get('revenue_potential_rating', 15), 20)
        prob = min(opp.get('probability_rating', 12), 20)
        speed = min(opp.get('speed_rating', 12), 15)
        demand = min(opp.get('demand_rating', 12), 15)
        repeatability = min(opp.get('repeatability_rating', 8), 10)
        scalability = min(opp.get('scalability_rating', 8), 10)
        learning = min(opp.get('learning_rating', 4), 5)
        strategic = min(opp.get('strategic_rating', 4), 5)

        risk = min(opp.get('risk_rating', 2), 10)
        cost = min(opp.get('cost_rating', 2), 10)

        total_score = (rev_pot + prob + speed + demand + repeatability + scalability + learning + strategic) - (risk + cost)
        return max(min(round(total_score, 1), 100.0), 0.0)

    def evaluate_and_decide(self, observations=None):
        if observations is None:
            observations = [
                "Developer interest on Moltbook in Web3 API integrations is high.",
                "E-Commerce SMEs struggle with page load speeds and SEO optimization."
            ]

        opportunities = self.opp_queue.items
        scored_opps = []
        for opp in opportunities:
            opp['score_0_100'] = self.calculate_0_100_score(opp)
            scored_opps.append(opp)

        scored_opps.sort(key=lambda x: x['score_0_100'], reverse=True)
        top_opp = scored_opps[0] if scored_opps else None

        top_title = top_opp.get("title", top_opp.get("solution", "Opportunity")) if top_opp else "None"
        decision = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "observations": observations,
            "opportunities_evaluated": len(scored_opps),
            "top_opportunity": top_title,
            "top_score": top_opp["score_0_100"] if top_opp else 0,
            "chosen_action": top_opp.get("next_action", "Execute outreach & content delivery") if top_opp else "Research opportunities",
            "expected_outcome": "Generate qualified lead inquiry and affiliate engagement",
            "autonomy_level": 3 # Level 3: Execute low-risk actions automatically
        }

        return decision
