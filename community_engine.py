import json
import os
import time
from hype_filter import HypeFilter

class CommunityEngine:
    def __init__(self, gaps_file="knowledge_gaps.json"):
        self.gaps_file = gaps_file
        self.gaps = self.load_gaps()

    def load_gaps(self):
        if os.path.exists(self.gaps_file):
            try:
                with open(self.gaps_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_seed_gaps()

    def save_gaps(self):
        with open(self.gaps_file, 'w') as f:
            json.dump(self.gaps, f, indent=2)

    def get_seed_gaps(self):
        return [
            {
                "topic": "What is a seed phrase?",
                "frequency": 42,
                "priority": "HIGH",
                "last_asked": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "answered"
            },
            {
                "topic": "How do I safely store cryptocurrency?",
                "frequency": 28,
                "priority": "HIGH",
                "last_asked": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "answered"
            },
            {
                "topic": "What is gas on Ethereum and EVM networks?",
                "frequency": 19,
                "priority": "MEDIUM",
                "last_asked": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending"
            }
        ]

    def format_answer_first_response(self, question, answer_text, educational_details, include_exchange_rec=False):
        """
        Pure Answer-First Principle (NO Affiliate Links):
        1. Direct Answer
        2. Educational Breakdown
        3. Security & Open-Source Learning Resource
        """
        response = f"❓ **Question:** {question}\n\n" \
                   f"1️⃣ **Direct Answer:**\n{answer_text}\n\n" \
                   f"2️⃣ **Educational Breakdown:**\n{educational_details}\n\n" \
                   f"3️⃣ **Security Best Practices:**\n" \
                   f"- Always double check domain URLs and contract approvals.\n" \
                   f"- Never input seed phrases or private keys into online forms."

        if include_exchange_rec:
            response += f"\n\n**Disclosure:** This educational content is provided for learning purposes only. " \
                        f"Always do your own research before making any financial decision."

        return HypeFilter.sanitize_content(response)
