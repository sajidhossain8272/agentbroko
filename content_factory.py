from hype_filter import HypeFilter

class ContentFactory:
    @classmethod
    def repurpose_topic(cls, concept, core_explanation):
        """
        Repurposes one single core topic into multi-format educational assets.
        """
        beginner_exp = f"🔰 **Beginner Overview:**\n{core_explanation}\n\nThink of this as a fundamental concept in Web3."
        
        faq_asset = f"❓ **Frequently Asked Questions: {concept}**\n\n" \
                    f"Q: Why is {concept} important?\n" \
                    f"A: It guarantees cryptographic integrity and security across decentralized ledgers.\n\n" \
                    f"Q: How do I get started?\n" \
                    f"A: Learn self-custody principles and verify all transaction signatures."

        dev_tutorial = f"💻 **Developer Snippet: Interacting with {concept}**\n\n" \
                       f"```python\n" \
                       f"# Python RPC Query for {concept}\n" \
                       f"import urllib.request, json\n" \
                       f"req = urllib.request.Request('https://mainnet.base.org', headers={{'Content-Type': 'application/json'}})\n" \
                       f"print('RPC query initialized for {concept}')\n" \
                       f"```"

        social_post = f"⚡ **Short Guide: {concept}**\n\n{core_explanation[:180]}...\n\n#Crypto #Web3 #AgentBroko"

        return {
            "concept": concept,
            "beginner_explanation": HypeFilter.sanitize_content(beginner_exp),
            "faq_asset": HypeFilter.sanitize_content(faq_asset),
            "dev_tutorial": dev_tutorial,
            "social_post": HypeFilter.sanitize_content(social_post)
        }
