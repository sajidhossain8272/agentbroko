import time
import logging
from event_bus import EventBus

class OpportunityScoringEngine:
    def __init__(self):
        self.bus = EventBus()

    @staticmethod
    def calculate_score(opp):
        """
        Formula:
        (Est Revenue * Confidence * SpeedFactor * Scalability * EvidenceScore) / (Cost + Risk + PlatformDep)
        """
        est_rev = opp.get("estimated_revenue", 100.0)
        conf = opp.get("confidence", 0.7)
        speed = max(30.0 - opp.get("time_to_first_revenue_days", 14), 1.0) / 10.0
        scale = opp.get("scalability", 5.0)
        evidence = opp.get("evidence_score", 5.0)
        cost = max(opp.get("estimated_cost", 10.0), 1.0)
        risk = max(opp.get("risk", 0.2) * 10.0, 0.5)
        plat_dep = max(opp.get("platform_dependency", 0.1) * 10.0, 0.5)

        numerator = est_rev * conf * speed * scale * evidence
        denominator = cost + risk + plat_dep
        score = round(numerator / denominator, 2)
        return min(score, 2000.0)

    def rank_opportunities(self, opportunities):
        ranked = []
        for opp in opportunities:
            sc = self.calculate_score(opp)
            opp_copy = dict(opp)
            opp_copy["score"] = sc
            ranked.append(opp_copy)

        ranked.sort(key=lambda x: x["score"], reverse=True)
        if ranked:
            top = ranked[0]
            self.bus.emit("opportunity.scored", f"Top Ranked Opportunity #{top['opportunity_id']}: '{top['name']}' (Score: {top['score']})", metadata=top)
        return ranked
