import json
import os

class TopicIntelligence:
    CATEGORIES = [
        "Bitcoin", "Blockchain Fundamentals", "Wallet Security", "Ethereum",
        "EVM", "DeFi", "Layer 2", "Smart Contracts", "Solidity",
        "Web3 Development", "AI + Blockchain", "Crypto Security",
        "Blockchain Research", "Zero-Knowledge Technology"
    ]

    def __init__(self, topic_file="topic_intelligence.json"):
        self.topic_file = topic_file
        self.topics = self.load_topics()

    def load_topics(self):
        if os.path.exists(self.topic_file):
            try:
                with open(self.topic_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_topics()

    def save_topics(self):
        with open(self.topic_file, 'w') as f:
            json.dump(self.topics, f, indent=2)

    def get_seed_topics(self):
        seed = []
        for idx, cat in enumerate(self.CATEGORIES, 1):
            seed.append({
                "id": f"top_{idx:02d}",
                "category": cat,
                "demand_score": 95.0 if cat in ["Bitcoin", "Wallet Security", "Crypto Security"] else 75.0,
                "questions_count": 42 if cat == "Wallet Security" else 15,
                "engagement_rate": "High" if cat in ["Wallet Security", "Bitcoin"] else "Medium",
                "conversion_relevance": "High" if cat in ["Bitcoin", "EVM", "DeFi"] else "Moderate"
            })
        return seed

    def get_highest_demand_topics(self, limit=5):
        sorted_topics = sorted(self.topics, key=lambda x: x["demand_score"], reverse=True)
        return sorted_topics[:limit]
