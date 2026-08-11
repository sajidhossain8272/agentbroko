import logging
import time
from event_bus import EventBus
from social_memory import SocialMemory
from opportunity_discovery import OpportunityDiscoveryEngine
from content_brain import ContentBrain
from content_memory import ContentMemory

class MoltbookConversationEngine:
    def __init__(self):
        self.bus = EventBus()
        self.memory = SocialMemory()
        self.opp_engine = OpportunityDiscoveryEngine()
        self.content_brain = ContentBrain()
        self.content_memory = ContentMemory()

    def generate_original_post(self, feed_posts=None):
        decision = self.content_brain.evaluate_and_select_action(feed_posts)
        if decision.get("action") != "POST":
            return None

        topic = decision["topic"]
        fmt = decision["format"]
        length = decision["length"]
        submolt = decision["submolt"]

        # Generate authentic content based on format & length
        if fmt == "Technical Breakdown":
            title = f"Technical Breakdown: {topic}"
            content = f"In building autonomous software agents, state machine isolation prevents race conditions across concurrent task loops. Here is how we structured explicit state transitions in AgentBroko."
        elif fmt == "Problem + Solution":
            title = f"Developer Guide: {topic}"
            content = f"Detecting secrets before commit is critical for open-source safety. Using a lightweight local scanner prevents secret leaks before git push."
        else:
            title = f"Engineering Insights: {topic}"
            content = f"Building domain-agnostic autonomous systems requires separating execution logic from content selection. Value-first contributions create long-term trust."

        post_payload = {
            "title": title,
            "content": content,
            "submolt": submolt,
            "format": fmt,
            "length": length,
            "category": decision["category"]
        }
        return post_payload

    def generate_comment(self, scored_post):
        category = scored_post.get("category")
        title = scored_post.get("title", "")
        post_id = scored_post.get("post_id")
        author = scored_post.get("author", "community_member")

        if category == "question":
            comment = f"Great question @{author}! In Web3 software engineering, standard practice is to isolate key derivation from network operations. For instance, using environment variable injection for seed phrases ensures keys never touch source code diffs."
        elif category == "problem":
            comment = f"Hi @{author}! If you are encountering this workflow bottleneck, building a lightweight local CLI validator in Python can automate pre-commit security checks before broadcasting transactions."
            # Automatically feed problem into Opportunity Discovery Engine!
            self.extract_opportunity(title, author)
        elif category == "technical_discussion":
            comment = f"Interesting perspective @{author}! We implemented automated diff scanning in our AgentBroko open-source engine, which caught zero-day secret leaks prior to PR creation."
        else:
            comment = f"Thanks for sharing this insights @{author}! Value-first open-source tooling is critical for Web3 security."

        self.memory.record_interaction(post_id, author, title, comment, interaction_type="comment")
        self.bus.emit("moltbook.comment.created", f"Published comment on post #{post_id} by @{author}", metadata={
            "post_id": post_id,
            "author": author,
            "category": category,
            "comment": comment
        })
        return comment

    def generate_reply(self, thread_item, user_text):
        post_id = thread_item.get("post_id")
        author = thread_item.get("author", "community_member")
        topic = thread_item.get("topic", "")

        reply = f"Thanks @{author}! Appreciate your follow-up. Feel free to inspect our open-source AgentBroko repository or test our local validation suite!"
        self.memory.record_interaction(post_id, author, topic, reply, interaction_type="reply")
        self.bus.emit("moltbook.reply.created", f"Replied to @{author} in active thread #{post_id}", metadata={
            "post_id": post_id,
            "author": author,
            "reply": reply
        })
        return reply

    def extract_opportunity(self, problem_title, author):
        opp_name = f"Moltbook Community Pain Point: {problem_title[:35]}"
        opp = self.opp_engine.discover_new_opportunity(
            name=opp_name,
            category="developer_tools",
            problem=f"Community member @{author} reported: '{problem_title}'",
            solution="Automated Python CLI / SDK utility",
            est_rev=600.0,
            confidence=0.85,
            evidence_score=8.5
        )
        self.memory.record_opportunity_discovered()
        self.bus.emit("moltbook.opportunity.discovered", f"Extracted business opportunity from Moltbook problem: '{problem_title}'", metadata=opp)
        return opp
