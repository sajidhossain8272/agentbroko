class CTAEngine:
    """
    Context-Aware CTA Engine (NO Affiliate Links Policy)
    All affiliate link insertion has been completely dropped to prevent platform spam flags.
    """

    @classmethod
    def get_contextual_cta(cls, topic_category, content_type="educational"):
        cat_lower = topic_category.lower()

        if "security" in cat_lower or "seed phrase" in cat_lower or "phishing" in cat_lower or "key" in cat_lower:
            return "\n\n🛡️ *Security Reminder: Never share your seed phrase, private keys, or passwords with anyone. Always verify transaction signatures on hardware devices.*"

        elif "developer" in cat_lower or "solidity" in cat_lower or "rpc" in cat_lower or "builder" in cat_lower:
            return "\n\n💻 *Developer Resource: Access public EVM RPC endpoints directly via standard JSON-RPC HTTP clients.*"

        else:
            return "\n\n📚 *Learn With AgentBroko: Open-source blockchain, Web3, and Bitcoin security education.*"
