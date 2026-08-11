import json
import os
import time

class ContentPerformanceEngine:
    def __init__(self, perf_file="content_performance.json"):
        self.perf_file = perf_file
        self.items = self.load_performance()

    def load_performance(self):
        if os.path.exists(self.perf_file):
            try:
                with open(self.perf_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_performance()

    def save_performance(self):
        with open(self.perf_file, 'w') as f:
            json.dump(self.items, f, indent=2)

    def get_seed_performance(self):
        return [
            {
                "content_id": "cnt_001",
                "topic": "What is Bitcoin?",
                "level": "level_1",
                "platform": "Moltbook m/crypto",
                "published_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "views": 240,
                "engagement": 18,
                "questions_generated": 5,
                "shares": 3,
                "clicks": 12,
                "affiliate_clicks": 2,
                "donation_page_visits": 1,
                "educational_value": 20,
                "audience_interest": 18,
                "engagement_quality": 15,
                "retention": 14,
                "conversion_relevance": 12,
                "content_score": 79.0
            },
            {
                "content_id": "cnt_002",
                "topic": "What is a Seed Phrase & Self-Custody Security?",
                "level": "level_2",
                "platform": "Moltbook m/technology",
                "published_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "views": 410,
                "engagement": 42,
                "questions_generated": 14,
                "shares": 9,
                "clicks": 28,
                "affiliate_clicks": 4,
                "donation_page_visits": 3,
                "educational_value": 20,
                "audience_interest": 20,
                "engagement_quality": 19,
                "retention": 18,
                "conversion_relevance": 15,
                "content_score": 92.0
            }
        ]

    @staticmethod
    def calculate_content_score(item):
        """
        Content Score formula:
        + Educational Value (0-20)
        + Audience Interest (0-20)
        + Engagement Quality (0-20)
        + Retention (0-20)
        + Conversion Relevance (0-20)
        """
        edu = min(item.get("educational_value", 15), 20)
        aud = min(item.get("audience_interest", 15), 20)
        eng = min(item.get("engagement_quality", 15), 20)
        ret = min(item.get("retention", 15), 20)
        conv = min(item.get("conversion_relevance", 10), 20)
        return float(round(edu + aud + eng + ret + conv, 1))

    def record_content_metrics(self, topic, level, platform, views, engagement, questions, affiliate_clicks=0):
        item = {
            "content_id": f"cnt_{len(self.items) + 1:03d}",
            "topic": topic,
            "level": level,
            "platform": platform,
            "published_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "views": views,
            "engagement": engagement,
            "questions_generated": questions,
            "shares": int(engagement * 0.2),
            "clicks": int(views * 0.05),
            "affiliate_clicks": affiliate_clicks,
            "donation_page_visits": int(views * 0.01),
            "educational_value": 18,
            "audience_interest": min(int(views / 20), 20),
            "engagement_quality": min(int(engagement / 2), 20),
            "retention": 15,
            "conversion_relevance": 12
        }
        item["content_score"] = self.calculate_content_score(item)
        self.items.append(item)
        self.save_performance()
        return item
