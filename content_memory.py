import json
import os
import time

class ContentMemory:
    def __init__(self, memory_file="content_memory.json"):
        self.memory_file = memory_file
        self.data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_memory()

    def save_memory(self):
        try:
            self.data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(self.memory_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def get_seed_memory(self):
        return {
            "published_posts": [],
            "topic_counts": {
                "crypto_web3": 2,
                "security": 1,
                "ai_agents": 1
            },
            "recent_submolts": ["m/crypto", "m/technology"],
            "lessons_learned": [
                "Technical tutorials on developer security achieve 3x higher engagement than promotional announcements.",
                "Enforcing topic diversity prevents platform spam filters from flagging repetitive subjects."
            ],
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def calculate_topic_fatigue(self, category):
        cat_count = self.data["topic_counts"].get(category, 0)
        # Fatigue penalty increases if category posted repeatedly
        if cat_count >= 3:
            return 5.0 # High fatigue penalty
        elif cat_count >= 2:
            return 2.5
        return 0.0 # No fatigue penalty

    def record_publication(self, post_id, topic, category, submolt, format_type, length_type):
        entry = {
            "post_id": post_id,
            "topic": topic,
            "category": category,
            "submolt": submolt,
            "format": format_type,
            "length": length_type,
            "published_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data["published_posts"].append(entry)
        self.data["topic_counts"][category] = self.data["topic_counts"].get(category, 0) + 1
        if submolt not in self.data["recent_submolts"]:
            self.data["recent_submolts"].append(submolt)
        self.save_memory()
        return entry
