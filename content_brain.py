import time
import logging
from event_bus import EventBus
from trend_detector import TrendDetector
from content_memory import ContentMemory

class ContentBrain:
    CATEGORIES = {
        "ai_agents": {"submolt": "m/technology", "format": "Technical Breakdown"},
        "security": {"submolt": "m/tooling", "format": "Problem + Solution"},
        "software_engineering": {"submolt": "m/technology", "format": "Tutorial"},
        "business_automation": {"submolt": "m/agentfinance", "format": "Case Study"},
        "crypto_web3": {"submolt": "m/crypto", "format": "Analysis"},
        "tech_trends": {"submolt": "m/todayilearned", "format": "Discovery"}
    }

    def __init__(self):
        self.detector = TrendDetector()
        self.memory = ContentMemory()
        self.bus = EventBus()

    def generate_candidate_topics(self, feed_posts=None):
        trends = self.detector.detect_trends(feed_posts)
        candidates = []

        for t in trends:
            cat = t["category"]
            fatigue = self.memory.calculate_topic_fatigue(cat)
            heat = t["heat"]
            relevance = 8.5
            novelty = 8.0
            usefulness = 9.0
            spam_risk = 1.0 if cat != "crypto_web3" else 3.0

            # Formula: (Heat + Relevance + Novelty + Usefulness) - Fatigue - SpamRisk
            score = round((heat + relevance + novelty + usefulness) - fatigue - spam_risk, 2)
            config = self.CATEGORIES.get(cat, {"submolt": "m/general", "format": "Analysis"})

            candidates.append({
                "topic": t["topic"],
                "category": cat,
                "score": score,
                "heat": heat,
                "fatigue": fatigue,
                "suggested_submolt": config["submolt"],
                "suggested_format": config["format"],
                "suggested_length": "MEDIUM" if len(t["topic"]) < 30 else "LONG"
            })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates

    def evaluate_and_select_action(self, feed_posts=None):
        candidates = self.generate_candidate_topics(feed_posts)
        if not candidates:
            self.bus.emit("content.decision", "No candidate topics found", metadata={"action": "WAIT"})
            return {"action": "WAIT", "reason": "NO_CANDIDATE_TOPICS"}

        top_candidate = candidates[0]
        
        # High quality threshold for publishing
        if top_candidate["score"] < 20.0:
            self.bus.emit("content.decision", f"Top candidate score too low ({top_candidate['score']}) | Decided to WAIT", metadata={
                "action": "WAIT",
                "top_candidate": top_candidate
            })
            return {
                "action": "WAIT",
                "reason": "TOPIC_SCORE_BELOW_THRESHOLD",
                "top_candidate": top_candidate
            }

        decision = {
            "action": "POST",
            "topic": top_candidate["topic"],
            "category": top_candidate["category"],
            "score": top_candidate["score"],
            "submolt": top_candidate["suggested_submolt"],
            "format": top_candidate["suggested_format"],
            "length": top_candidate["suggested_length"],
            "reason": f"Top ranked topic across multi-domain candidate pool (Score: {top_candidate['score']})"
        }

        self.bus.emit("content.selected", f"Selected Topic: '{top_candidate['topic']}' for {top_candidate['suggested_submolt']}", metadata=decision)
        return decision
