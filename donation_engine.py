from treasury import Treasury

class DonationEngine:
    DONATION_ADDRESSES = {
        "Bitcoin (BTC)": "1K4i91pJA9RHFUVVwFumpR8sASh1sAfEYq",
        "Solana (SOL)": "5Q5DTQ9bsitWXtgZXivUZZPYkwz6BsFQWJBKRGsgj5Wb",
        "EVM (ETH / BNB / MATIC / BASE / ARB)": "0xe74d4e103FE88B07eDf39664E74a99463D85Cfc6"
    }

    @classmethod
    def get_donation_info(cls):
        treasury = Treasury()
        t_data = treasury.sync_balances()

        btc_bal = t_data["wallets"]["bitcoin"]["balance_btc"]
        sol_bal = t_data["wallets"].get("solana", {}).get("balance_sol", 0.0)

        return {
            "addresses": cls.DONATION_ADDRESSES,
            "verified_received": {
                "BTC": btc_bal,
                "SOL": sol_bal,
                "EVM": t_data["wallets"]["evm"]["networks"]
            },
            "mission_statement": "AgentBroko is an independent open blockchain education project. If you find our technical guides and security tutorials helpful, voluntary donations help cover API compute costs, server infrastructure, and research."
        }
