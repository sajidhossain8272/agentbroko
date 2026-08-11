class ServiceFactory:
    SERVICES = {
        "website_audit": {
            "name": "SME Technical PageSpeed & SEO Audit",
            "description": "Comprehensive performance analysis identifying LCP bottlenecks, unoptimized assets, and mobile viewport flaws with actionable remediation code.",
            "pricing": {
                "starter": {"name": "Basic Audit Report", "price_usd": 35.0},
                "standard": {"name": "Full Technical Audit + Remediation Snippets", "price_usd": 75.0},
                "premium": {"name": "Done-For-You Optimization & Speed Fix", "price_usd": 200.0}
            }
        },
        "api_integration": {
            "name": "Exchange V5 Unified API Integration Suite",
            "description": "Developer-ready Python/JS wrapper scripts for Binance and Bybit REST/WebSocket execution with hardware 2FA and sub-account isolation.",
            "pricing": {
                "starter": {"name": "Standard V5 Integration Code", "price_usd": 50.0},
                "standard": {"name": "Multi-Exchange API Wrapper + Rate Limit Handler", "price_usd": 120.0},
                "premium": {"name": "Turnkey Algorithmic Bot Architecture", "price_usd": 350.0}
            }
        },
        "evm_rpc_setup": {
            "name": "Multi-Chain EVM RPC Wallet Monitor",
            "description": "Automated monitoring script checking real-time balances and transactions across Base, Polygon, Arbitrum, and Ethereum mainnet.",
            "pricing": {
                "starter": {"name": "Single-Chain Wallet Monitor", "price_usd": 40.0},
                "standard": {"name": "4-Chain EVM Monitor + Discord/Telegram Alerts", "price_usd": 100.0},
                "premium": {"name": "Enterprise Treasury Tracker + Financial Accounting", "price_usd": 300.0}
            }
        }
    }

    @classmethod
    def get_service_offer(cls, service_key, tier="standard"):
        srv = cls.SERVICES.get(service_key, cls.SERVICES["website_audit"])
        pkg = srv["pricing"].get(tier, srv["pricing"]["standard"])
        return {
            "service_name": srv["name"],
            "tier_name": pkg["name"],
            "description": srv["description"],
            "price_usd": pkg["price_usd"]
        }
