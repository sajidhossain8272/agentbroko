import logging
import time
from treasury import Treasury
from event_bus import EventBus

class WalletCapability:
    def __init__(self):
        self.treasury = Treasury()
        self.bus = EventBus()
        self.consecutive_failures = 0
        self.circuit_open = False
        self.next_retry = 0

    def execute(self, payload=None):
        logging.info("[CAPABILITY] Executing WalletCapability...")
        now = time.time()

        if self.circuit_open and now < self.next_retry:
            self.bus.emit("wallet.circuit_open", "BTC Circuit Breaker OPEN | Skipping provider query", metadata={
                "consecutive_failures": self.consecutive_failures,
                "next_retry_in_sec": int(self.next_retry - now)
            })
            return {
                "status": "DEGRADED",
                "circuit_open": True,
                "consecutive_failures": self.consecutive_failures,
                "message": "Circuit breaker open, using cached wallet state"
            }

        try:
            self.bus.emit("wallet.fetch.started", "Syncing multi-chain treasury balances...")
            data = self.treasury.sync_balances()
            btc_data = data["wallets"]["bitcoin"]

            if btc_data.get("status") == "UNAVAILABLE":
                self.consecutive_failures += 1
                if self.consecutive_failures >= 3:
                    self.circuit_open = True
                    self.next_retry = now + 120 # 2 minute backoff
                    self.bus.emit("wallet.fetch.failed", "BTC provider query timed out 3x | Circuit Breaker OPEN", metadata={
                        "consecutive_failures": self.consecutive_failures
                    })
                return {
                    "status": "DEGRADED",
                    "circuit_open": self.circuit_open,
                    "consecutive_failures": self.consecutive_failures,
                    "btc_status": "UNAVAILABLE"
                }

            # Success reset
            self.consecutive_failures = 0
            self.circuit_open = False
            self.bus.emit("wallet.fetch.success", "Treasury balances synced successfully", metadata={
                "btc_balance": btc_data.get("balance_btc"),
                "sol_balance": data["wallets"].get("solana", {}).get("balance_sol")
            })

            return {
                "status": "SUCCESS",
                "circuit_open": False,
                "consecutive_failures": 0,
                "balances": data["wallets"]
            }

        except Exception as e:
            self.consecutive_failures += 1
            logging.warning(f"[WALLET] Sync error: {e}")
            return {
                "status": "DEGRADED",
                "circuit_open": self.circuit_open,
                "consecutive_failures": self.consecutive_failures,
                "error": str(e)
            }
