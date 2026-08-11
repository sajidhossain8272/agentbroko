import json
import os
import time
from wallet_client import WalletClient
from btc_wallet_client import BTCWalletClient
from solana_wallet_client import SolanaWalletClient

class Treasury:
    def __init__(self, treasury_file="treasury.json"):
        self.treasury_file = treasury_file
        self.evm_wallet = WalletClient()
        self.btc_wallet = BTCWalletClient()
        self.sol_wallet = SolanaWalletClient()
        self.data = self.load_treasury()

    def load_treasury(self):
        if os.path.exists(self.treasury_file):
            try:
                with open(self.treasury_file, 'r') as f:
                    data = json.load(f)
                    data.setdefault("wallets", {})
                    data["wallets"].setdefault("solana", {"address": self.sol_wallet.address, "balance_sol": 0.0})
                    return data
            except Exception:
                pass
        return {
            "wallets": {
                "bitcoin": {
                    "addresses": self.btc_wallet.addresses,
                    "primary_address": self.btc_wallet.primary_address,
                    "balance_btc": 0.0
                },
                "solana": {
                    "address": self.sol_wallet.address,
                    "balance_sol": 0.0
                },
                "evm": {
                    "address": self.evm_wallet.address,
                    "networks": {
                        "Ethereum": 0.0,
                        "Base": 0.0,
                        "Polygon": 0.0,
                        "Arbitrum": 0.0,
                        "BNB Chain (BSC)": 0.0
                    }
                }
            },
            "revenue": {
                "total": 0.0,
                "services": 0.0,
                "products": 0.0,
                "affiliate": 0.0,
                "sponsorships": 0.0
            },
            "updated_at": time.time()
        }

    def save_treasury(self):
        self.data["updated_at"] = time.time()
        with open(self.treasury_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def sync_balances(self):
        # Fetch EVM balances (Ethereum, Base, Polygon, Arbitrum, BNB Chain)
        evm_bals = self.evm_wallet.check_all_balances()
        self.data["wallets"]["evm"]["networks"] = evm_bals

        # Fetch BTC balance
        btc_info = self.btc_wallet.check_btc_balance()
        self.data["wallets"]["bitcoin"]["primary_address"] = self.btc_wallet.primary_address
        self.data["wallets"]["bitcoin"]["addresses"] = self.btc_wallet.addresses
        self.data["wallets"]["bitcoin"]["balance_btc"] = btc_info["total_btc"]

        # Fetch SOL balance
        sol_info = self.sol_wallet.check_sol_balance()
        self.data["wallets"]["solana"]["balance_sol"] = sol_info["balance_sol"]

        self.save_treasury()
        return self.data
