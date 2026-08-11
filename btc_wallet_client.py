import urllib.request
import urllib.error
import socket
import json
import os
import logging
import time
from btc_address_deriver import mnemonic_to_seed, derive_master_key, pubkey_hash_to_addresses

class BTCWalletClient:
    def __init__(self, mnemonic=None):
        self.mnemonic = mnemonic or self.load_mnemonic()
        self.addresses = self.derive_btc_addresses(self.mnemonic)
        self.primary_address = self.addresses.get('legacy', '1K4i91pJA9RHFUVVwFumpR8sASh1sAfEYq')
        self.connection_timeout = 2.0
        self.read_timeout = 2.0
        self.max_retries = 2
        self.backoff_seconds = 0.25
        self.cache_ttl_seconds = 60.0
        self.cache = {}
        self.circuit_open = False
        self.next_retry = 0.0
        self.consecutive_failures = 0

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

    def _read_json_from_provider(self, url, target_addr):
        headers = {'User-Agent': 'AgentBroko/2.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=min(self.connection_timeout, self.read_timeout)) as resp:
            raw = resp.read(1048576)
            return json.loads(raw.decode('utf-8'))

    def _is_cache_fresh(self, target_addr):
        cache_entry = self.cache.get(target_addr)
        if not cache_entry:
            return False
        if time.time() - cache_entry.get("cached_at", 0.0) > self.cache_ttl_seconds:
            return False
        return cache_entry.get("status") == "AVAILABLE"

    def _cache_balance(self, target_addr, payload):
        self.cache[target_addr] = {
            "payload": payload,
            "status": payload.get("status", "AVAILABLE"),
            "cached_at": time.time()
        }

    def check_btc_balance(self, address=None):
        """
        Fail-soft BTC balance query with timeout, retry, fallback, circuit-breaker
        and stale-cache handling. Never raises to the runtime loop.
        """
        target_addr = address or self.primary_address
        now = time.time()

        if self.circuit_open and now < self.next_retry:
            logging.warning(f"[WALLET] Circuit breaker open for BTC provider; serving stale cache or unavailable result for {target_addr}")
            stale = self.cache.get(target_addr)
            if stale and stale.get("payload"):
                return dict(stale["payload"])
            return {
                'address': target_addr,
                'confirmed_btc': None,
                'unconfirmed_btc': None,
                'total_btc': None,
                'tx_count': None,
                'status': 'UNAVAILABLE'
            }

        if self._is_cache_fresh(target_addr):
            cached = self.cache[target_addr]["payload"]
            logging.info(f"[WALLET] Using fresh BTC balance cache for {target_addr}")
            return dict(cached)

        endpoints = [
            f"https://blockchain.info/rawaddr/{target_addr}",
            f"https://blockstream.info/api/address/{target_addr}",
            f"https://mempool.space/api/address/{target_addr}"
        ]

        last_error = None
        for attempt in range(self.max_retries):
            for url in endpoints:
                try:
                    data = self._read_json_from_provider(url, target_addr)
                    if "blockchain.info" in url:
                        final_bal_sats = data.get('final_balance', 0)
                        n_tx = data.get('n_tx', 0)
                        payload = {
                            'address': target_addr,
                            'confirmed_btc': final_bal_sats / 1e8,
                            'unconfirmed_btc': 0.0,
                            'total_btc': final_bal_sats / 1e8,
                            'tx_count': n_tx,
                            'status': 'AVAILABLE'
                        }
                    else:
                        stats = data.get('chain_stats', {})
                        mempool = data.get('mempool_stats', {})
                        funded = stats.get('funded_txo_sum', 0)
                        spent = stats.get('spent_txo_sum', 0)
                        confirmed_sats = funded - spent
                        unconfirmed_sats = mempool.get('funded_txo_sum', 0) - mempool.get('spent_txo_sum', 0)
                        payload = {
                            'address': target_addr,
                            'confirmed_btc': confirmed_sats / 1e8,
                            'unconfirmed_btc': unconfirmed_sats / 1e8,
                            'total_btc': (confirmed_sats + unconfirmed_sats) / 1e8,
                            'tx_count': stats.get('tx_count', 0),
                            'status': 'AVAILABLE'
                        }
                    self.consecutive_failures = 0
                    self.circuit_open = False
                    self._cache_balance(target_addr, payload)
                    logging.info(f"[WALLET] BTC provider succeeded for {target_addr} via {url}")
                    return payload
                except (urllib.error.URLError, socket.timeout, TimeoutError, json.JSONDecodeError, ValueError) as e:
                    last_error = e
                    logging.warning(f"[WALLET] BTC provider query timeout/error on {url}: {e}")
                    self.consecutive_failures += 1
                except Exception as e:
                    last_error = e
                    logging.warning(f"[WALLET] BTC provider query exception on {url}: {e}")
                    self.consecutive_failures += 1

            if attempt < self.max_retries - 1:
                backoff = self.backoff_seconds * (2 ** attempt)
                logging.warning(f"[WALLET] BTC provider retry attempt {attempt + 1}/{self.max_retries} for {target_addr}; backing off {backoff:.2f}s")
                time.sleep(min(backoff, 1.0))

        if self.consecutive_failures >= 3:
            self.circuit_open = True
            self.next_retry = now + 120.0
            logging.warning(f"[WALLET] BTC provider circuit breaker opened after {self.consecutive_failures} failures")
        logging.warning(f"[WALLET] BTC balance unavailable for {target_addr}: provider timeout/retry exhaustion. Continuing cycle without BTC balance. Error: {last_error}")
        unavailable = {
            'address': target_addr,
            'confirmed_btc': None,
            'unconfirmed_btc': None,
            'total_btc': None,
            'tx_count': None,
            'status': 'UNAVAILABLE'
        }
        self._cache_balance(target_addr, unavailable)
        return unavailable
