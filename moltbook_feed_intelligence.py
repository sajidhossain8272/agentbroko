import re
import time
import logging
from event_bus import EventBus

class MoltbookFeedIntelligence:
    def __init__(self):
        self.bus = EventBus()

    @classmethod
    def classify_post(cls, post):
        title = (post.get("title") or "").lower()
        content = (post.get("content") or "").lower()
        full_text = f"{title} {content}"

        if "problem" in full_text or "need" in full_text or "help" in full_text or "struggle" in full_text or "looking for" in full_text:
            return "problem"
        elif "how to" in full_text or "what is" in full_text or "why" in full_text or "?" in title:
            return "question"
        elif "opportunity" in full_text or "hiring" in full_text or "grant" in full_text or "bounty" in full_text:
            return "opportunity"
        elif "code" in full_text or "python" in full_text or "evm" in full_text or "solidity" in full_text or "api" in full_text or "git" in full_text:
            return "technical_discussion"
        elif "release" in full_text or "announcing" in full_text or "v1" in full_text or "v2" in full_text:
            return "announcement"
        elif len(full_text.strip()) < 20:
            return "noise"
        else:
            return "general_discussion"

    @classmethod
    def score_conversation(cls, post):
        category = cls.classify_post(post)
        title = post.get("title", "")
        content = post.get("content", "")
        author = post.get("author", {}).get("name", "") if isinstance(post.get("author"), dict) else str(post.get("author", ""))

        relevance = 8.0 if category in ["problem", "question", "technical_discussion", "opportunity"] else 3.0
        add_value = 8.0 if len(content) > 50 else 4.0
        quality = 9.0 if "http" not in content.lower() else 5.0 # Higher quality for non-spam posts
        opp_value = 9.0 if category == "problem" or category == "opportunity" else 2.0
        spam_risk = 8.0 if "crypto affiliate" in content.lower() or "referral" in content.lower() else 1.0

        priority = (relevance + add_value + quality + opp_value) - spam_risk
        score = round(max(priority, 1.0), 2)

        return {
            "post_id": post.get("id"),
            "title": title,
            "author": author,
            "category": category,
            "score": score,
            "should_participate": score >= 15.0 and author != "agentbroko"
        }

    def process_feed(self, feed_posts):
        analyzed = []
        for p in feed_posts:
            scored = self.score_conversation(p)
            analyzed.append(scored)

        analyzed.sort(key=lambda x: x["score"], reverse=True)
        high_value = [a for a in analyzed if a["should_participate"]]

        self.bus.emit("moltbook.feed.updated", f"Analyzed {len(feed_posts)} feed items | {len(high_value)} High-Value Conversations", metadata={
            "total_analyzed": len(feed_posts),
            "high_value_count": len(high_value),
            "top_conversation": high_value[0] if high_value else None
        })

        return analyzed
