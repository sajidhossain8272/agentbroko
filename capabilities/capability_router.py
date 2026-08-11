import logging
from capabilities.moltbook_capability import MoltbookCapability
from capabilities.github_capability import GitHubCapability
from capabilities.business_capability import BusinessCapability
from capabilities.wallet_capability import WalletCapability

class CapabilityRouter:
    def __init__(self):
        self.moltbook = MoltbookCapability()
        self.github = GitHubCapability()
        self.business = BusinessCapability()
        self.wallet = WalletCapability()

    def route_and_execute(self, action_name, payload=None):
        act_lower = action_name.lower()
        if "moltbook" in act_lower or "social" in act_lower or "lesson" in act_lower:
            return self.moltbook.execute(payload)
        elif "github" in act_lower or "repo" in act_lower or "code" in act_lower or "pr" in act_lower:
            return self.github.execute(payload)
        elif "business" in act_lower or "opp" in act_lower or "monetiz" in act_lower:
            return self.business.execute(payload)
        elif "wallet" in act_lower or "treasury" in act_lower or "btc" in act_lower:
            return self.wallet.execute(payload)
        else:
            logging.info(f"[ROUTER] Defaulting to Moltbook + Business execution for '{action_name}'")
            res_m = self.moltbook.execute(payload)
            res_b = self.business.execute(payload)
            return {"moltbook": res_m, "business": res_b}
