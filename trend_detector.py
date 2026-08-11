import time
import logging

class TrendDetector:
    def __init__(self):
        pass

    def detect_trends(self, feed_posts=None):
        trends = [
            {"topic": "Autonomous Agent Reliability & State Machines", "category": "ai_agents", "heat": 9.2},
            {"topic": "Local Pre-Commit Secret Scanning Tools", "category": "security", "heat": 8.8},
            {"topic": "Python Multi-Chain Treasury API Architecture", "category": "software_engineering", "heat": 8.4},
            {"topic": "Value-First Open Source Software Monetization", "category": "business_automation", "heat": 8.0},
            {"topic": "Public vs Private Key Derivation Standards", "category": "crypto_web3", "heat": 6.5}
        ]

        if feed_posts:
            # Dynamically extract trends from recent posts
            for p in feed_posts[:5]:
                t = p.get("title", "")
                if t and len(t) > 10:
                    trends.append({
                        "topic": t,
                        "category": "community_discovery",
                        "heat": 7.5
                    })

        trends.sort(key=lambda x: x["heat"], reverse=True)
        return trends
