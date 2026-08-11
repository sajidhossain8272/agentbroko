import logging
from moltbook_client import MoltbookClient
from moltbook_feed_intelligence import MoltbookFeedIntelligence
from moltbook_conversation_engine import MoltbookConversationEngine
from social_memory import SocialMemory
from content_brain import ContentBrain
from content_memory import ContentMemory
from event_bus import EventBus

class MoltbookCapability:
    def __init__(self):
        self.client = MoltbookClient()
        self.intel = MoltbookFeedIntelligence()
        self.engine = MoltbookConversationEngine()
        self.brain = ContentBrain()
        self.content_mem = ContentMemory()
        self.memory = SocialMemory()
        self.bus = EventBus()

    def execute(self, payload=None):
        logging.info("[CAPABILITY] Executing MoltbookCapability with ContentBrain...")
        feed_res = self.client.get_feed(sort='new', limit=15)
        posts = feed_res.get('posts', [])
        
        # 1. Check for active feed conversations first (Conversation-First Content)
        if posts:
            scored_posts = self.intel.process_feed(posts)
            high_value = [p for p in scored_posts if p["should_participate"]]
            if high_value:
                target_post = high_value[0]
                comment = self.engine.generate_comment(target_post)
                if target_post["score"] >= 18.0:
                    self.client.upvote_post(target_post["post_id"])
                    self.memory.record_upvote()
                return {
                    "status": "SUCCESS",
                    "action": "COMMENT",
                    "post_id": target_post["post_id"],
                    "comment": comment
                }

        # 2. Evaluate original publication via ContentBrain
        post_item = self.engine.generate_original_post(posts)
        if not post_item:
            self.bus.emit("moltbook.decision", "ContentBrain decided: No valuable topic to post right now | Status WAITING", metadata={"action": "WAIT"})
            return {"status": "SKIPPED", "reason": "NO_VALUABLE_TOPIC_OR_WAIT"}

        res = self.client.create_post(post_item["submolt"], post_item["title"], post_item["content"])
        if res.success:
            self.content_mem.record_publication(
                res.post_id,
                post_item["title"],
                post_item["category"],
                post_item["submolt"],
                post_item["format"],
                post_item["length"]
            )
            return {
                "status": "SUCCESS",
                "action": "POST",
                "post_id": res.post_id,
                "title": post_item["title"],
                "submolt": post_item["submolt"],
                "format": post_item["format"]
            }

        return {"status": "FAILED", "reason": res.message}
