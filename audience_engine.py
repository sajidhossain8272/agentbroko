import json
import os
import time

class AudienceEngine:
    def __init__(self, metrics_file="audience_metrics.json"):
        self.metrics_file = metrics_file
        self.data = self.load_metrics()

    def load_metrics(self):
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "summary": {
                "visitors": 142,
                "followers": 18,
                "subscribers": 12,
                "readers": 350,
                "commenters": 9,
                "repeat_visitors": 45,
                "community_members": 24,
                "educational_resource_users": 88,
                "affiliate_link_visitors": 14,
                "donation_page_visitors": 8
            },
            "history": []
        }

    def save_metrics(self):
        with open(self.metrics_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def record_interaction(self, metric_key, count=1):
        if metric_key in self.data["summary"]:
            self.data["summary"][metric_key] += count
            self.data["history"].append({
                "metric": metric_key,
                "count": count,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            self.save_metrics()
