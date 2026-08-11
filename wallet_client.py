import urllib.request
import json

class WalletClient:
    def __init__(self, address="0xe74d4e103FE88B07eDf39664E74a99463D85Cfc6"):
        self.address = address
        self.rpcs = {
            'Base': 'https://mainnet.base.org',
            'Polygon': 'https://polygon-rpc.com',
            'Arbitrum': 'https://arb1.arbitrum.io/rpc',
            'Ethereum': 'https://eth.llamarpc.com',
            'BNB Chain (BSC)': 'https://bsc-dataseed.binance.org/'
        }

    def get_balance(self, rpc_url):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [self.address, "latest"],
            "id": 1
        }
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(rpc_url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                hex_val = data.get('result', '0x0')
                wei = int(hex_val, 16)
                eth = wei / 10**18
                return eth
        except Exception:
            return 0.0

    def check_all_balances(self):
        balances = {}
        for chain, rpc in self.rpcs.items():
            balances[chain] = self.get_balance(rpc)
        return balances
