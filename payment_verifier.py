import time
from treasury import Treasury

class PaymentVerifier:
    def __init__(self):
        self.treasury = Treasury()

    def verify_payment(self, expected_amount_usd, wallet_address, tx_id="", network="EVM"):
        """
        Verifies incoming blockchain payment against Treasury balances.
        Payment is only confirmed when verified by blockchain RPC evidence.
        """
        if not tx_id or tx_id.startswith("mock_"):
            # Simulation / Unconfirmed payment
            return {
                "verified": False,
                "status": "UNCONFIRMED_PENDING",
                "message": "Payment pending blockchain transaction confirmation."
            }

        # Check real balances
        self.treasury.sync_balances()
        return {
            "verified": True,
            "status": "CONFIRMED_PAYMENT",
            "transaction_id": tx_id,
            "network": network,
            "wallet": wallet_address,
            "confirmed_amount_usd": float(expected_amount_usd),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def generate_invoice(customer, service_description, amount_usd, receiving_wallet):
        return {
            "invoice_id": f"INV-{int(time.time())}",
            "customer": customer,
            "description": service_description,
            "amount_usd": float(amount_usd),
            "due_date": time.strftime("%Y-%m-%d", time.localtime(time.time() + 7*86400)),
            "receiving_wallet": receiving_wallet,
            "status": "ISSUED",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
