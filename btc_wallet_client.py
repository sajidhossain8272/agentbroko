import urllib.request
import json
import os
import logging
from btc_address_deriver import mnemonic_to_seed, derive_master_key, pubkey_hash_to_addresses

class BTCWalletClient:
    def __init__(self, mnemonic=None):
        self.mnemonic = mnemonic or self.load_mnemonic()
        self.addresses = self.derive_btc_addresses(self.mnemonic)
        self.primary_address = self.addresses.get('legacy', '1K4i91pJA9RHFUVVwFumpR8sASh1sAfEYq')

    def load_mnemonic(self):
        # 1. Check environment variable / .env
        if os.environ.get("MNEMONIC_PHRASE"):
            return os.environ.get("MNEMONIC_PHRASE").strip()
        if os.environ.get("EVM_MNEMONIC"):
            return os.environ.get("EVM_MNEMONIC").strip()

        # 2. Check .env file directly
        if os.path.exists(".env"):
            try:
                with open(".env", "r") as f:
                    for line in f:
                        if line.strip().startswith("MNEMONIC_PHRASE="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception:
                pass

        return "frown tonight accident rigid ready finish turtle double puzzle fuel capable spread"

    def derive_btc_addresses(self, mnemonic):
        try:
            seed = mnemonic_to_seed(mnemonic)
            priv, chain = derive_master_key(seed)
            return pubkey_hash_to_addresses(priv)
        except Exception as e:
            logging.error(f"Error deriving BTC addresses: {e}")
            return {
                'legacy': '1K4i91pJA9RHFUVVwFumpR8sASh1sAfEYq',
                'native_segwit': 'bc1qccja5du70v74upzd665x3r5ptkfx9emjhxhjpc',
                'nested_segwit': '3DwBN7KQSxrBXrskkyCBN2DGSppRfQ2zk6'
            }

    def check_btc_balance(self, address=None):
        """
        Fail-soft BTC balance query: 2-second timeout per provider.
        If provider times out, logs notice and returns total_btc: None without raising exceptions.
        """
        target_addr = address or self.primary_address

        # 1. Try blockchain.info with 2s timeout
        try:
            url = f"https://blockchain.info/rawaddr/{target_addr}"
            headers = {'User-Agent': 'AgentBroko/2.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                final_bal_sats = data.get('final_balance', 0)
                n_tx = data.get('n_tx', 0)
                return {
                    'address': target_addr,
                    'confirmed_btc': final_bal_sats / 1e8,
                    'unconfirmed_btc': 0.0,
                    'total_btc': final_bal_sats / 1e8,
                    'tx_count': n_tx,
                    'status': 'AVAILABLE'
                }
        except Exception as e:
            logging.warning(f"[WALLET] blockchain.info query notice for {target_addr}: {e}")

        # 2. Fallback endpoints with 2s timeout
        endpoints = [
            f"https://blockstream.info/api/address/{target_addr}",
            f"https://mempool.space/api/address/{target_addr}"
        ]
        for url in endpoints:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'AgentBroko/2.0'})
                with urllib.request.urlopen(req, timeout=2) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    stats = data.get('chain_stats', {})
                    mempool = data.get('mempool_stats', {})
                    funded = stats.get('funded_txo_sum', 0)
                    spent = stats.get('spent_txo_sum', 0)
                    confirmed_sats = funded - spent
                    unconfirmed_sats = mempool.get('funded_txo_sum', 0) - mempool.get('spent_txo_sum', 0)
                    return {
                        'address': target_addr,
                        'confirmed_btc': confirmed_sats / 1e8,
                        'unconfirmed_btc': unconfirmed_sats / 1e8,
                        'total_btc': (confirmed_sats + unconfirmed_sats) / 1e8,
                        'tx_count': stats.get('tx_count', 0),
                        'status': 'AVAILABLE'
                    }
            except Exception as e:
                logging.warning(f"[WALLET] BTC Provider {url} timeout/error: {e}")

        logging.warning(f"[WALLET] BTC balance unavailable: provider timeout. Continuing cycle without BTC balance.")
        return {
            'address': target_addr,
            'confirmed_btc': None,
            'unconfirmed_btc': None,
            'total_btc': None,
            'tx_count': None,
            'status': 'UNAVAILABLE'
        }
