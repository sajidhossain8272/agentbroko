import random
import time
from hype_filter import HypeFilter

class EducationEngine:
    CURRICULUM = {
        "level_1": {
            "title": "Level 1 — Beginner: Bitcoin & Blockchain Fundamentals",
            "topics": [
                {
                    "concept": "What is Bitcoin?",
                    "summary": "Bitcoin is a decentralized peer-to-peer digital currency powered by a global network of open-source nodes without central bank intermediaries.",
                    "key_takeaway": "Transactions are verified by cryptography and recorded in a public distributed ledger called the blockchain."
                },
                {
                    "concept": "Proof of Work & Mining",
                    "summary": "Miners solve cryptographic puzzles (SHA-256) to assemble transactions into valid blocks and secure the network consensus.",
                    "key_takeaway": "Proof of Work ensures that altering historical transactions requires overwhelming computational energy, making the ledger immutable."
                },
                {
                    "concept": "Public Keys vs Private Keys",
                    "summary": "A public key acts like your bank account number (shareable address), while your private key acts like your secret digital signature password.",
                    "key_takeaway": "Never share your private key or seed phrase with anyone under any circumstances."
                }
            ]
        },
        "level_2": {
            "title": "Level 2 — Intermediate: Wallets, Transactions & Crypto Security",
            "topics": [
                {
                    "concept": "Self-Custody vs Exchange Custody",
                    "summary": "Self-custody means you control your private keys directly via a hardware or non-custodial wallet. Exchange wallets store keys on centralized servers.",
                    "key_takeaway": "Rule of thumb: 'Not your keys, not your coins.' Self-custody offers sovereign control."
                },
                {
                    "concept": "Phishing & Approval Scams",
                    "summary": "Malicious sites trick users into signing unverified smart contract spend approvals or giving away seed phrases.",
                    "key_takeaway": "Always double check domain URLs, verify token spending limits, and use hardware authorization."
                }
            ]
        },
        "level_3": {
            "title": "Level 3 — Advanced: EVM, Solidity & Layer 2 Networks",
            "topics": [
                {
                    "concept": "What is the Ethereum Virtual Machine (EVM)?",
                    "summary": "The EVM is a deterministic, sandboxed execution environment that computes state transitions for smart contracts across EVM-compatible chains like Base, Polygon, and Arbitrum.",
                    "key_takeaway": "EVM compatibility allows developers to deploy standard Solidity code across multiple Layer 2 scaling solutions."
                }
            ]
        },
        "level_4": {
            "title": "Level 4 — Builder: Web3 APIs & AI Agent Integrations",
            "topics": [
                {
                    "concept": "Automated Multi-Chain RPC Balance Verification",
                    "summary": "AI agents query JSON-RPC nodes directly (`eth_getBalance`, `getBalance`) to monitor on-chain state without relying on third-party scrapers.",
                    "key_takeaway": "Direct RPC node queries provide real-time cryptographic proof of wallet balances."
                }
            ]
        },
        "level_5": {
            "title": "Level 5 — Research: Cryptography & Scaling",
            "topics": [
                {
                    "concept": "Zero-Knowledge Rollups vs Optimistic Rollups",
                    "summary": "ZK-rollups use mathematical validity proofs (SNARKs/STARKs) for instant settlement, while Optimistic rollups use fraud proofs with a 7-day challenge window.",
                    "key_takeaway": "Layer 2 scaling achieves 100x higher throughput while inheriting Layer 1 mainnet security."
                }
            ]
        }
    }

    @classmethod
    def get_daily_topic(cls, level="level_1"):
        level_data = cls.CURRICULUM.get(level, cls.CURRICULUM["level_1"])
        topic = random.choice(level_data["topics"])
        return {
            "level_title": level_data["title"],
            "concept": topic["concept"],
            "summary": topic["summary"],
            "key_takeaway": topic["key_takeaway"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def generate_educational_post(cls, level="level_1"):
        topic = cls.get_daily_topic(level)
        post_content = f"📚 [Learn With AgentBroko] {topic['concept']}\n\n" \
                       f"{topic['summary']}\n\n" \
                       f"💡 Key Takeaway: {topic['key_takeaway']}\n\n" \
                       f"#Blockchain #Education #Web3 #AgentBroko"
        
        return HypeFilter.sanitize_content(post_content)
