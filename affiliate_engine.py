"""
AgentBroko Affiliate Revenue Module
Manages affiliate partnerships, educational content generation, comparison matrices,
and mandatory disclosure compliance for Binance and Bybit.
"""

class AffiliateEngine:
    DISCLOSURE_TEXT = (
        "\n\n*Disclosure: This includes an affiliate/referral link. "
        "AgentBroko's owner may receive a commission if you sign up or qualify through the link, at no extra cost to you.*"
    )

    PARTNERS = {
        'binance': {
            'name': 'Binance',
            'url': 'https://accounts.binance.com/en-ZA/register?ref=LZPXAPM5',
            'description': 'Global cryptocurrency ecosystem, deep liquidity, extensive spot/futures markets, and robust API infrastructure.',
            'highlights': ['Deepest Market Liquidity', 'Comprehensive API SDKs', 'Wide Asset Selection', 'Institutional Custody Options']
        },
        'bybit': {
            'name': 'Bybit',
            'url': 'https://www.bybit.com/en/invite/?ref=RX0WA2',
            'description': 'Advanced trading ecosystem specializing in derivative products, high-throughput execution, and automated trading tools.',
            'highlights': ['High-Speed API Execution', 'Advanced Derivatives Suite', 'Copy Trading Features', 'Intuitive UI/UX']
        }
    }

    EDUCATIONAL_TOPICS = [
        {
            'id': 'api_trading',
            'title': 'Guide: Setting Up Exchange API Keys for Automated Agents',
            'content': (
                "When building automated trading bots or AI agents, API rate limits, WebSocket feeds, and authentication security are critical.\n\n"
                "Key considerations when selecting an exchange API:\n"
                "1. **Rate Limits & Latency**: Look for REST rate limits >= 1200 req/min and dedicated WebSocket channels.\n"
                "2. **Sub-Account Management**: Isolate bot funds from primary storage.\n"
                "3. **IP Whitelisting**: Restrict API keys to specific server IPs.\n\n"
                "Top platforms with developer-friendly APIs:\n"
                "- **Binance**: Offers comprehensive Web3/REST APIs with extensive documentation.\n"
                "- **Bybit**: Features high-speed V5 Unified Trading API for low-latency execution."
            )
        },
        {
            'id': 'security_best_practices',
            'title': 'Cryptocurrency Exchange Security: Essential Best Practices',
            'content': (
                "Security is paramount in digital asset management. Follow these essential rules:\n\n"
                "1. **Enable Hardware 2FA**: Use YubiKey or authenticator apps rather than SMS.\n"
                "2. **Address Whitelisting**: Lock withdrawal destinations to known addresses.\n"
                "3. **Cold Storage Separation**: Keep operational funds separate from long-term reserves.\n\n"
                "Both Binance and Bybit provide institutional-grade security features including multi-party computation (MPC) and withdrawal whitelisting."
            )
        }
    ]

    @classmethod
    def get_disclaimer(cls):
        return cls.DISCLOSURE_TEXT

    @classmethod
    def get_comparison(cls):
        comparison = (
            "### Cryptocurrency Exchange Feature Comparison\n\n"
            "| Feature | Binance | Bybit |\n"
            "|---|---|---|\n"
            "| **Primary Focus** | Ecosystem & Liquidity | Derivatives & Automated Tools |\n"
            "| **API Standard** | REST / WebSocket / FIX | Unified V5 API |\n"
            "| **Security** | SAFU Fund / Hardware 2FA | Cold Wallet Storage / 2FA |\n"
            "| **Referral Link** | [Join Binance](" + cls.PARTNERS['binance']['url'] + ") | [Join Bybit](" + cls.PARTNERS['bybit']['url'] + ") |\n"
        )
        return comparison + cls.DISCLOSURE_TEXT

    @classmethod
    def get_educational_post(cls, topic_id=None):
        import random
        if not topic_id:
            topic = random.choice(cls.EDUCATIONAL_TOPICS)
        else:
            topic = next((t for t in cls.EDUCATIONAL_TOPICS if t['id'] == topic_id), cls.EDUCATIONAL_TOPICS[0])

        full_content = (
            f"### {topic['title']}\n\n"
            f"{topic['content']}\n\n"
            f"**Recommended Platforms:**\n"
            f"- [Explore Binance Ecosystem]({cls.PARTNERS['binance']['url']})\n"
            f"- [Explore Bybit Ecosystem]({cls.PARTNERS['bybit']['url']})"
        )
        return full_content + cls.DISCLOSURE_TEXT
