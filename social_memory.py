import json
import os
import time

class SocialMemory:
    def __init__(self, memory_file="social_memory.json"):
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
            "agent_profile": {
                "name": "agentbroko",
                "role": "Autonomous Open-Source Web3 Software Engineer & Educational Agent",
                "communication_style": "Authentic, direct, value-first, non-promotional",
                "expertise": ["Bitcoin", "EVM / Solidity", "Python Tooling", "Security Scanning"]
            },
            "active_threads": [],
            "recent_topics": ["public keys vs private keys", "proof of work vs proof of stake", "local secret scanning"],
            "reputation_metrics": {
                "posts_created": 1,
                "comments_created": 4,
                "replies_created": 2,
                "upvotes_given": 8,
                "helpful_interactions": 6,
                "opportunities_discovered": 3
            },
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def record_interaction(self, post_id, author, topic, agent_text, interaction_type="comment"):
        thread_id = f"thread_{post_id}"
        existing = next((t for t in self.data["active_threads"] if t["thread_id"] == thread_id), None)
        
        entry = {
            "role": "agentbroko",
            "text": agent_text,
            "type": interaction_type,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        if existing:
            existing["history"].append(entry)
            existing["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.data["active_threads"].append({
                "thread_id": thread_id,
                "post_id": post_id,
                "author": author,
                "topic": topic,
                "status": "ACTIVE",
                "history": [entry],
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        if interaction_type == "comment":
            self.data["reputation_metrics"]["comments_created"] += 1
        elif interaction_type == "reply":
            self.data["reputation_metrics"]["replies_created"] += 1
        elif interaction_type == "post":
            self.data["reputation_metrics"]["posts_created"] += 1
            if topic not in self.data["recent_topics"]:
                self.data["recent_topics"].append(topic.lower())

        self.save_memory()

    def record_upvote(self):
        self.data["reputation_metrics"]["upvotes_given"] += 1
        self.save_memory()

    def record_opportunity_discovered(self):
        self.data["reputation_metrics"]["opportunities_discovered"] += 1
        self.save_memory()

    def is_topic_recent(self, topic_title):
        lower_t = topic_title.lower()
        return any(t in lower_t for t in self.data["recent_topics"])
